import os
from pathlib import Path
import sys
import time
import traceback
from argparse import ArgumentParser
import yaml
import json
import logging
from logging.config import dictConfig as logger_dict_config
import tempfile
import shutil
import zipfile
from datetime import datetime, date
from subprocess import Popen, PIPE
import fnmatch
import zlib
import re


RE_BACKUP_FILE = re.compile(f'backup_(\d+-\d+-\d+)\.zip')


class ConfigurationError(Exception):
    pass


class CommandError(Exception):
    pass


class _ExcludeErrorsFilter(logging.Filter):
    def filter(self, record):
        """Only lets through log messages with log level below ERROR ."""
        return record.levelno < logging.ERROR


class _ColorfulFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s [%(levelname)8s] | %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%d-%b-%Y %H:%M:%S')
        return formatter.format(record)


log: logging.Logger = None
logger_config = {
    'version': 1,
    'filters': {
        'exclude_errors': {
            '()': _ExcludeErrorsFilter
        }
    },
    'formatters': {
        # Modify log message format here or replace with your custom formatter class
        'my_formatter': {
            '()': _ColorfulFormatter,
        }
    },
    'handlers': {
        'console_stderr': {
            # Sends log messages with log level ERROR or higher to stderr
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
            'formatter': 'my_formatter',
            'stream': sys.stderr
        },
        'console_stdout': {
            # Sends log messages with log level lower than ERROR to stdout
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'my_formatter',
            'filters': ['exclude_errors'],
            'stream': sys.stdout
        },
        # File handler is added in __main__
    },
    'root': {
        # In general, this should be kept at 'NOTSET'.
        # Otherwise, it would interfere with the log levels set for each handler.
        'level': 'NOTSET',
        'handlers': ['console_stderr', 'console_stdout']
    },
}


def _get_folders_files(path: str, absolute=False):
    elements = os.listdir(path)
    directories = [e for e in elements if os.path.isdir(os.path.join(path, e))]
    files = [e for e in elements if os.path.isfile(os.path.join(path, e))]

    if absolute:
        directories = [os.path.join(path, d) for d in directories]
        files = [os.path.join(path, f) for f in files]

    return directories, files


def _process_exclude_text(text: str):
    if text is None:
        return []

    res = list()
    exclude_lines = [l.strip().lower() for l in text.strip().replace('\r', '').split('\n')]

    for line in exclude_lines:
        if line.endswith('/'):
            res.append(line + "*")
        else:
            res.append(line)

    return res


def _create_zip_from_directory(directory_path: str, output_zip: str, to_exclude: str, compression=5):
    """
    Create a zip file from a directory.
    """

    exclude_lines = _process_exclude_text(to_exclude)

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=compression) as zipf:
        # Walk through the directory
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, directory_path)

                # Handle excluded paths / files
                for exl in exclude_lines:
                    if fnmatch.fnmatch(relative_path, exl):
                        break
                else:
                    # Add the file to the zip file, using a relative path
                    relative_path = os.path.relpath(full_path, directory_path)
                    zipf.write(full_path, relative_path)


def run_command_before_backup(command: str):
    log.info(f"    Running command: '{command}'")
    t1 = time.time()
    p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    returncode = p.wait(timeout=600)
    duration = round(time.time() - t1, 4)

    if returncode != 0:
        raise CommandError(f"Command '{command}' failed with exit code {returncode}.\nStdout: {p.stdout.read()}\nStderr: {p.stderr.read()}")

    log.info(f"    Command finished after {duration} seconds")


def handle_backup_folder(config: dict, output_dir: str, path: str):
    folder_name = Path(path).name
    with open(os.path.join(path, 'backup.yaml'), 'r') as f:
        folder_config = yaml.safe_load(f) or dict()

    if folder_config.get('ignore', 'false') in (True, 'true', 'True'):
        log.info(f"  Folder '{folder_name}' is ignored.")
        return

    log.info(f"  Creating backup for folder '{folder_name}'")

    if (command := folder_config.get('command')) is not None:
        run_command_before_backup(command)

    to_exclude = folder_config.get('exclude', '')
    t1 = time.time()
    _create_zip_from_directory(path, os.path.join(output_dir, folder_name + '.zip'), to_exclude)
    duration = round(time.time() - t1, 4)

    log.info(f'  -> Backup took {duration} seconds')


def check_disk_size(path: Path, max_percentage: float):
    stats = shutil.disk_usage(path)
    used_percent = round(stats.used / stats.total, 4)

    if used_percent > max_percentage:
        log.critical(f"Not enough free disk space. {used_percent * 100}% > {max_percentage * 100}%")
        return False

    log.info(f"Enough disk space available. Only {used_percent * 100}% / {max_percentage * 100}% are used.")
    return True


def process_input_path(config: dict, temp_dir: str, path: str):
    """
    Analyze all input folders and submit them to backup if required.
    """

    log.info(f'Checking input path: {path}')

    directories, files = _get_folders_files(path)

    if 'backup.yaml' in files:
        handle_backup_folder(config, temp_dir, path)
    else:
        for directory in directories:
            _, files = _get_folders_files(os.path.join(path, directory))
            if 'backup.yaml' in files:
                handle_backup_folder(config, temp_dir, os.path.join(path, directory))
            else:
                log.warning(f"  Folder '{directory}' does not contain a backup.yaml file")


def _calculate_checksum(filename, chunksize=65536):
    """ Compute the CRC-32 checksum of the contents of the given filename """

    with open(filename, "rb") as f:
        checksum = 0
        while (chunk := f.read(chunksize)) :
            checksum = zlib.crc32(chunk, checksum)
        return hex(checksum)


def create_manifest_file(temp_dir: Path):
    """ Creates a manifest file, which contains information about the backup archive """

    zipfiles = [f for f in _get_folders_files(temp_dir, absolute=True)[1] if f.endswith('.zip')]

    manifest_data = {
        'timestamp': datetime.now().isoformat(),
        'checksums': {Path(f).name: _calculate_checksum(f) for f in zipfiles},
        'size': sum([os.path.getsize(f) for f in zipfiles]),
    }

    with open(f'{temp_dir}/manifest.json', 'w', encoding='UTF-8') as mf:
        json.dump(manifest_data, mf)


def remove_outdated_backups(path: Path, max_age: int):
    """
    :param max_age: In days
    """

    today = datetime.today().date()

    file_matches = [RE_BACKUP_FILE.match(f) for f in _get_folders_files(path)[1]]
    backup_archives = [f for f in file_matches if f is not None]

    for m in backup_archives:
        filename = m.string
        dt = datetime.strptime(m.group(1), '%Y-%m-%d').date()
        age = (today - dt).days

        if age > max_age:
            log.info(f"Removing outdated file '{path.name}/{filename}' (is {age} days old)")
            os.remove(path / filename)

    return


def on_backup_completed(config: dict, output_path: Path, temp_dir: str):
    """ Handles the finished backup and copies it to the required folders """

    today = datetime.now().date()
    timestamp = today.strftime('%Y-%m-%d')
    final_filename = f'backup_{timestamp}.zip'

    log.info('--- Backup file created successfully ---');

    # Daily
    remove_outdated_backups(output_path / 'daily', 7)
    shutil.copy(f'{temp_dir}/backup_final.zip', output_path / 'daily' / final_filename)
    log.info(f"Saved daily backup")

    # Weekly
    if today.weekday() == 6:
        remove_outdated_backups(output_path / 'weekly', 31)
        shutil.copy(f'{temp_dir}/backup_final.zip', output_path / 'weekly' / final_filename)
        log.info(f"Saved weekly backup")

    # Monthly
    if today.day == 1:
        remove_outdated_backups(output_path / 'monthly', 31 * 12)
        shutil.copy(f'{temp_dir}/backup_final.zip', output_path / 'monthly' / final_filename)
        log.info(f"Saved monthly backup")

    # Yearly
    if today.day == 1 and today.month == 1:
        shutil.copy(f'{temp_dir}/backup_final.zip', output_path / 'yearly' / final_filename)
        log.info(f"Saved yearly backup")


def main(config_path: str):
    try:
        if not os.path.exists(config_path):
            raise FileNotFoundError(config_path)

        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        today = datetime.now().strftime('%Y-%m-%d')
        log.info("")
        log.info(f"--------  Started Backup at {today}  --------")

        # --- Validate config
        if 'output_path' not in config:
            raise ConfigurationError("Missing attribute 'output_path'")

        output_path = Path(config['output_path'])
        if not os.path.exists(output_path):
            raise ConfigurationError(f"Output path '{output_path}' does not exist")

        os.makedirs(output_path / 'daily', exist_ok=True)
        os.makedirs(output_path / 'weekly', exist_ok=True)
        os.makedirs(output_path / 'monthly', exist_ok=True)
        os.makedirs(output_path / 'yearly', exist_ok=True)

        disk_usage_limit = config.get('disk_usage_limit', 1.0)
        if not (0.0 <= disk_usage_limit <= 1.0):
            raise ConfigurationError("Invalid disk_usage_limit. Must be between 0.0 and 1.0")

        if not check_disk_size(output_path, disk_usage_limit):
            exit()

        # --- Perform the actual backup
        t1 = time.time()
        with tempfile.TemporaryDirectory() as temp_dir:
            for input_path in config['input_paths']:
                process_input_path(config, temp_dir, input_path.replace('\\', '/').replace('/', os.sep))

            # shutil.make_archive(f'{temp_dir}/backup_final', 'zip', temp_dir)
            with tempfile.TemporaryDirectory() as temp_out_dir:
                create_manifest_file(temp_dir)
                _create_zip_from_directory(temp_dir, f'{temp_out_dir}/backup_final.zip', '', compression=0)
                on_backup_completed(config, output_path, temp_out_dir)

            duration = round(time.time() - t1, 4)
            log.info(f"Finished backup process after {duration} seconds")

    except Exception as e:
        stacktrace_info = traceback.TracebackException.from_exception(e)
        stack_of_this_file = [s for s in stacktrace_info.stack if s.filename == __file__]
        stacktrace = ''.join(stacktrace_info.format()).strip()
        log.fatal(f'{type(e).__name__} @ line {stack_of_this_file[-1].lineno}: \n{stacktrace}')
        raise


def setup_logger():
    if sys.platform == 'linux':
        if os.geteuid() == 0:
            logger_config['handlers']['rotating_file_handler'] = {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'my_formatter',
                'filename': '/var/log/backup/backup.log',
                'maxBytes': 1024 * 1024,  # 1 MB
                'backupCount': 5,  # Keep up to 5 backup log files
                'encoding': 'utf8',
            }
            logger_config['root']['handlers'].append('rotating_file_handler')

            os.makedirs('/var/log/backup', exist_ok=True)
        else:
            log.warning("Can't write to log file. Please run as root to be able to write logs to /var/log")


if __name__ == '__main__':
    setup_logger()

    logger_dict_config(logger_config)
    log = logging.getLogger(__name__)
    parser = ArgumentParser()
    parser.add_argument('config', type=str, help='Path to the config file')

    args = parser.parse_args()

    main(args.config)

    print('Done.')
