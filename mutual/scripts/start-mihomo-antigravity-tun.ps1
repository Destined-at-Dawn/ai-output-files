$ErrorActionPreference = "Stop"

$workDir = "E:\ai产出文件\牛马\mutual\mutual\.tmp\mihomo-antigravity"
$mihomo = "C:\v2rayN\bin\mihomo\mihomo.exe"
$config = Join-Path $workDir "config.yaml"

Get-Process -Name "mihomo" -ErrorAction SilentlyContinue |
    Stop-Process -Force

Start-Sleep -Seconds 2

Start-Process -FilePath $mihomo -WorkingDirectory $workDir -ArgumentList @(
    "-d", $workDir,
    "-f", $config
)
