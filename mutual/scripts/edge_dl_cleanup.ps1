[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$edgeDir = Get-ChildItem "D:\" -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match 'edge' }
$targetDir = $edgeDir.FullName
$keepFile = "openrelay-windows-x64.exe"

Write-Output ("=== Edge Download Cleanup ===")
Write-Output ("Target: {0}" -f $targetDir)
Write-Output ("Keeping: {0}" -f $keepFile)
Write-Output ""

$totalFreed = 0

# Delete all files EXCEPT the keep file
Get-ChildItem $targetDir -File -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.Name -ne $keepFile } | ForEach-Object {
    $sizeMB = [math]::Round($_.Length/1MB, 1)
    Write-Output ("  DELETE: {0} ({1} MB)" -f $_.Name, $sizeMB)
    $totalFreed += $_.Length
    Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue
}

# Delete all subdirectories
Get-ChildItem $targetDir -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $s = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    Write-Output ("  DELETE DIR: {0} ({1:N0} MB)" -f $_.Name, ($s/1MB))
    $totalFreed += $s
    Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
}

$freedGB = [math]::Round($totalFreed/1GB, 2)
Write-Output ""
Write-Output ("=== Freed: {0} GB ===" -f $freedGB)

# Verify kept file
if (Test-Path (Join-Path $targetDir $keepFile)) {
    Write-Output ("OK: {0} preserved" -f $keepFile)
}

# Disk check
$d = Get-PSDrive D
Write-Output ("D Drive free: {0:N2} GB" -f ($d.Free/1GB))
