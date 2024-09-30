export interface BackupArchive {
    filename: string
    timestamp: string
    checksums: FileChecksum[]
}

export interface FileChecksum {
    file: string
    checksum: string
}