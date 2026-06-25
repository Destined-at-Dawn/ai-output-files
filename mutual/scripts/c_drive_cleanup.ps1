# C Drive Cleanup Script - 2026-05-11
# Estimated free: ~26.4 GB

param([switch]$Execute)

$totalFreed = 0
$UserHome = "C:\Users\13975"

function Remove-TargetPath {
    param([string]$Path, [string]$Desc)
    if (Test-Path $Path) {
        $size = (Get-ChildItem $Path -Recurse -ErrorAction SilentlyContinue |
                 Where-Object { -not $_.PSIsContainer } |
                 Measure-Object -Property Length -Sum).Sum
        $sizeGB = [math]::Round($size / 1GB, 2)
        if ($Execute) {
            Write-Output ("DELETING: {0} ({1} GB) - {2}" -f $Path, $sizeGB, $Desc)
            Remove-Item $Path -Recurse -Force -ErrorAction SilentlyContinue
            Write-Output "  Done."
        } else {
            Write-Output ("[DRY RUN] {0} ({1} GB) - {2}" -f $Path, $sizeGB, $Desc)
        }
        $script:totalFreed += $size
    } else {
        Write-Output ("[SKIP] Not found: {0}" -f $Path)
    }
}

Write-Output "=== C Drive Cleanup ==="
Write-Output ("Mode: {0}" -f $(if ($Execute) { "EXECUTE" } else { "DRY RUN (preview)" }))
Write-Output ""

# 1. Temp Installers (~1.8 GB)
Write-Output ">>> [1/4] Temp Installers"
Remove-TargetPath "$UserHome\AppData\Local\Temp\trae-cn-user-x64" "Trae installer cache"
Remove-TargetPath "$UserHome\AppData\Local\Temp\workbuddy-update-x64" "WorkBuddy installer cache"
Remove-TargetPath "$UserHome\AppData\Local\Temp\windsurf-stable-user-x64" "Windsurf installer cache"
Remove-TargetPath "$UserHome\AppData\Local\Temp\1akfx51d" "VS2022 component installers"
Write-Output ""

# 2. NVIDIA DXCache (~4.83 GB)
Write-Output ">>> [2/4] NVIDIA Shader Cache"
Remove-TargetPath "$UserHome\AppData\Local\NVIDIA\DXCache" "DX shader cache (auto-regenerates)"
Remove-TargetPath "$UserHome\AppData\Local\NVIDIA\GLCache" "GL shader cache (auto-regenerates)"
Write-Output ""

# 3. Recordly Recordings (~13.36 GB)
Write-Output ">>> [3/4] Recordly Recordings"
Write-Output "  WARNING: Recordings are NOT recoverable!"
Remove-TargetPath "$UserHome\AppData\Roaming\Recordly\recordings" "Historical screen recordings"
Write-Output ""

# 4. WeChat Web Cache (~6.42 GB)
Write-Output ">>> [4/4] WeChat Web Cache"
Remove-TargetPath "$UserHome\AppData\Roaming\Tencent\xwechat\radium\web" "WeChat built-in browser cache"
Write-Output ""

# Summary
$freedGB = [math]::Round($totalFreed / 1GB, 2)
Write-Output "=== Summary ==="
Write-Output ("Estimated freed: {0} GB" -f $freedGB)
if (-not $Execute) {
    Write-Output "Preview only. To execute:"
    Write-Output '  powershell -ExecutionPolicy Bypass -File .\c_drive_cleanup.ps1 -Execute'
} else {
    Write-Output "Cleanup complete!"
}
