import {readdir} from 'fs/promises';
import StreamZip from 'node-stream-zip';
import type {BackupArchive, BackupFile} from "../../../types.js";


async function extractManifest(path: string) {
    const zip = new StreamZip.async({file: path});
    const manifestData = await zip.entryData('manifest.json');
    const manifest = JSON.parse(manifestData.toString());

    const filenameSplits = path.replace('\\', '/').split('/');
    try {
        const manifest_files = manifest['files'];
        const files = Object.keys(manifest_files).map(filename => ({
            filename: filename,
            checksum: manifest_files[filename].checksum,
            size: manifest_files[filename].size,
        } satisfies BackupFile))

        return {
            filename: filenameSplits[filenameSplits.length - 1],
            timestamp: manifest['timestamp'],
            files: files.sort((a, b) => b.size - a.size),
            size: manifest['size'],
        } satisfies BackupArchive;
    } catch (e) {
        console.warn(`Failed to extract manifest: ${e}`);
    }

    return {
        filename: filenameSplits[filenameSplits.length - 1],
        timestamp: manifest['timestamp'],
        files: [],
        size: 0,
    } satisfies BackupArchive;
}


export async function GET({url, params}) {
    const type = params.type;
    if (!["daily", "weekly", "monthly", "yearly"].includes(type)) {
        throw new Error("Invalid type value");
    }

    if (process.env.BACKUPS_DIR == undefined) {
        throw new Error("Invalid BACKUPS_DIR");
    }

    let path = process.env.BACKUPS_DIR + '/' + type;
    let rawFiles: string[] = await readdir(path);

    let asyncFiles = rawFiles.map(f => extractManifest(path + '/' + f));
    let files = await Promise.all(asyncFiles);
    files.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());

    return Response.json({
        'files': files,
    });
}
