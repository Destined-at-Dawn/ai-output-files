$ErrorActionPreference = "Continue"

Get-Process -Name "xray", "v2rayN" -ErrorAction SilentlyContinue |
    Stop-Process -Force

Start-Sleep -Seconds 5

Start-Process -FilePath "C:\v2rayN\v2rayN.exe" -WorkingDirectory "C:\v2rayN"
