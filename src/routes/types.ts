export interface BackupArchive {
    filename: string
    timestamp: string
    files: BackupFile[]
    size: number
}

export interface BackupFile {
    filename: string
    checksum: string
    size: number
}
