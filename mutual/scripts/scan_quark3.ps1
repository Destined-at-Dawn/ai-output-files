[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Get ALL D:\ folders, scan each for large files
Get-ChildItem "D:\" -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $folder = $_
    $bigFiles = Get-ChildItem $folder.FullName -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Length -gt 500MB } |
        Sort-Object Length -Descending |
        Select-Object -First 3

    if ($bigFiles) {
        Write-Output ("`n=== {0} ===" -f $folder.FullName)
        $bigFiles | ForEach-Object {
            Write-Output ("  {0} ({1:N2} GB) - {2}" -f $_.Name, ($_.Length/1GB), $_.LastWriteTime.ToString('yyyy-MM-dd'))
        }
    }
}
