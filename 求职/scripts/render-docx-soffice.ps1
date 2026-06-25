param(
    [Parameter(Mandatory = $true)]
    [string]$InputDocx,

    [Parameter(Mandatory = $false)]
    [string]$OutputDir = ""
)

$ErrorActionPreference = "Stop"

$sofficeCandidates = @(
    "C:\Program Files\LibreOffice\program\soffice.exe",
    "C:\Program Files (x86)\LibreOffice\program\soffice.exe"
)

$soffice = $sofficeCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $soffice) {
    throw "LibreOffice soffice.exe not found. Install LibreOffice, then rerun this script."
}

$inputPath = (Resolve-Path -LiteralPath $InputDocx).Path
if (-not $OutputDir) {
    $OutputDir = Join-Path ([System.IO.Path]::GetTempPath()) "codex_docx_render"
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$stableInput = Join-Path $OutputDir "input.docx"
Copy-Item -LiteralPath $inputPath -Destination $stableInput -Force

# Use the absolute soffice.exe path directly. On this Windows environment,
# render_docx.py can fail when it relies on PATH plus -env:UserInstallation.
$pdfProc = Start-Process `
    -FilePath $soffice `
    -ArgumentList @("--headless", "--norestore", "--convert-to", "pdf", "--outdir", $OutputDir, $stableInput) `
    -NoNewWindow `
    -Wait `
    -PassThru

if ($pdfProc.ExitCode -ne 0) {
    throw "LibreOffice PDF export failed with exit code $($pdfProc.ExitCode)."
}

$pngProc = Start-Process `
    -FilePath $soffice `
    -ArgumentList @("--headless", "--norestore", "--convert-to", "png", "--outdir", $OutputDir, $stableInput) `
    -NoNewWindow `
    -Wait `
    -PassThru

if ($pngProc.ExitCode -ne 0) {
    throw "LibreOffice PNG export failed with exit code $($pngProc.ExitCode)."
}

Get-ChildItem -LiteralPath $OutputDir -File | Sort-Object LastWriteTime
