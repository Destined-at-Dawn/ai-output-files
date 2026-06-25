$ErrorActionPreference = "Stop"

$proxy = "http://127.0.0.1:10808"
$proxyHostPort = "127.0.0.1:10808"
$exeCandidates = @(
    "$env:LOCALAPPDATA\Programs\antigravity\Antigravity.exe",
    "D:\Antigravity IDE\Antigravity IDE.exe"
)
$exe = $exeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $exe) {
    throw "Antigravity executable was not found in known install locations."
}

Get-Process -Name "Antigravity", "Antigravity IDE" -ErrorAction SilentlyContinue |
    Stop-Process -Force

Start-Sleep -Seconds 2

$env:HTTP_PROXY = $proxy
$env:HTTPS_PROXY = $proxy
$env:ALL_PROXY = $proxy
$env:NO_PROXY = "localhost,127.0.0.1,::1,*.local"
$env:http_proxy = $proxy
$env:https_proxy = $proxy
$env:all_proxy = $proxy
$env:no_proxy = $env:NO_PROXY

Start-Process -FilePath $exe -ArgumentList @(
    "--proxy-server=http=$proxyHostPort;https=$proxyHostPort",
    "--proxy-bypass-list=localhost;127.0.0.1;::1;*.local"
)
