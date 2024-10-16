# Raspberry Pi Backup Dashboard

## Backup script
The backup script creates a full backup for the specified folders each run and 
stores it in a backup path. It requires a config file to work.

Each folder that should be backed up, must contain a file called ``backup.yaml``, which can be empty or contain information
on how to back up the folder it's in.

### Config file
````yaml
# The path where the backups shall be stored. Should be an external device
output_path: "/media/pi/Backups"
# How much of the available space of the backup storage device can be used. 0.8 = 80%
disk_usage_limit: 0.8
# The list of paths, which should be monitored for backups
input_paths:
  - "/home/pi/Docker"
  - "/home/pi/Certificates"
  - "/backup"
````

### backup.yaml config
````yaml
# (Optional) A command to execute before creating the backup. Can be used to trigger an export etc.
command: docker exec paperless-webserver document_exporter ../export
# (Optional) What to exclude. Syntax is like a .gitignore file
exclude: |
  consume/
  data/
  media/
  pgdata/
# (Optional) Ignore this folder
ignore: false
````

### Cron job


## Build dashboard
The following command compiles and runs the node server
```bash
pnpm run build
node build 
```

## Use the docker image

