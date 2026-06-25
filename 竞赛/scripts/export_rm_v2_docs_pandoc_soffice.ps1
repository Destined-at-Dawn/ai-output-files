param(
    [Parameter(Mandatory = $true)]
    [string]$Root,
    [Parameter(Mandatory = $true)]
    [string]$Pandoc,
    [Parameter(Mandatory = $true)]
    [string]$Soffice,
    [Parameter(Mandatory = $true)]
    [string]$PdfToPpm,
    [Parameter(Mandatory = $true)]
    [string]$PdfInfo
)

$ErrorActionPreference = "Stop"

$rootPath = Resolve-Path -LiteralPath $Root
$docxDir = Join-Path $rootPath "docs_docx"
$pdfDir = Join-Path $rootPath "docs_pdf"
$renderDir = Join-Path $rootPath "_render_check"
$tmpDir = Join-Path $rootPath "_pandoc_tmp"

Remove-Item -LiteralPath $docxDir, $pdfDir, $renderDir, $tmpDir -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $docxDir, $pdfDir, $renderDir, $tmpDir | Out-Null

$docs = @(
    @{Stem="00_v2_overview"; Title="v2 Overview"; Path="README.md"},
    @{Stem="01_research_report"; Title="Deep Research and Iteration Report"; Path="research_report.md"},
    @{Stem="02_pack_readme"; Title="Learning Pack README"; Path="improved_pack/README.md"},
    @{Stem="03_technical_report"; Title="Technical Report"; Path="improved_pack/docs/technical_report.md"},
    @{Stem="04_design"; Title="Design Notes"; Path="improved_pack/docs/design.md"},
    @{Stem="05_code_walkthrough"; Title="Code Walkthrough"; Path="improved_pack/docs/code_walkthrough.md"},
    @{Stem="06_step_by_step_tutorial"; Title="Step by Step Tutorial"; Path="improved_pack/docs/tutorial_step_by_step.md"},
    @{Stem="07_test_plan"; Title="Test Plan"; Path="improved_pack/docs/test_plan.md"},
    @{Stem="08_reflection_template"; Title="Reflection Template"; Path="improved_pack/docs/reflection.md"},
    @{Stem="09_submit_checklist"; Title="Submit Checklist"; Path="improved_pack/docs/submit_checklist.md"}
)

function New-PandocMarkdown {
    param(
        [string]$Title,
        [string]$InputPath,
        [string]$OutputPath
    )

    $body = Get-Content -LiteralPath $InputPath -Raw -Encoding UTF8
    $yaml = @"
---
title: "$Title"
lang: zh-CN
---

"@
    Set-Content -LiteralPath $OutputPath -Value ($yaml + $body) -Encoding UTF8
}

$combinedPath = Join-Path $tmpDir "10_full_combined_document.md"
Set-Content -LiteralPath $combinedPath -Value "---`ntitle: `"Full Combined Document`"`nlang: zh-CN`n---`n" -Encoding UTF8

foreach ($doc in $docs) {
    $input = Join-Path $rootPath $doc.Path
    if (!(Test-Path -LiteralPath $input)) {
        throw "Missing markdown: $input"
    }

    $tmpMd = Join-Path $tmpDir ($doc.Stem + ".md")
    New-PandocMarkdown -Title $doc.Title -InputPath $input -OutputPath $tmpMd

    $outDocx = Join-Path $docxDir ($doc.Stem + ".docx")
    & $Pandoc $tmpMd `
        --from markdown+pipe_tables+fenced_code_blocks `
        --to docx `
        --standalone `
        --toc `
        --metadata "lang=zh-CN" `
        --output $outDocx
    if ($LASTEXITCODE -ne 0) { throw "pandoc failed: $($doc.Stem)" }

    Add-Content -LiteralPath $combinedPath -Value "`n# $($doc.Title)`n" -Encoding UTF8
    Add-Content -LiteralPath $combinedPath -Value (Get-Content -LiteralPath $input -Raw -Encoding UTF8) -Encoding UTF8
    Add-Content -LiteralPath $combinedPath -Value "`n\newpage`n" -Encoding UTF8
}

$combinedDocx = Join-Path $docxDir "10_full_combined_document.docx"
& $Pandoc $combinedPath `
    --from markdown+pipe_tables+fenced_code_blocks `
    --to docx `
    --standalone `
    --toc `
    --metadata "lang=zh-CN" `
    --output $combinedDocx
if ($LASTEXITCODE -ne 0) { throw "pandoc failed: combined document" }

$loProfile = Join-Path $tmpDir "lo-profile"
New-Item -ItemType Directory -Force -Path $loProfile | Out-Null
& $Soffice "-env:UserInstallation=file:///$($loProfile.Replace('\','/'))" --headless --convert-to pdf --outdir $pdfDir (Join-Path $docxDir "*.docx")
if ($LASTEXITCODE -ne 0) { throw "soffice conversion failed" }

$pdfs = Get-ChildItem -LiteralPath $pdfDir -Filter *.pdf | Sort-Object Name
if ($pdfs.Count -ne 11) {
    throw "Expected 11 PDFs, got $($pdfs.Count)"
}

$combinedPdf = Join-Path $pdfDir "10_full_combined_document.pdf"
& $PdfInfo $combinedPdf | Out-File -LiteralPath (Join-Path $renderDir "10_full_combined_document_pdfinfo.txt") -Encoding UTF8

& $PdfToPpm -png -f 1 -l 1 -r 120 $combinedPdf (Join-Path $renderDir "combined_page_1") | Out-Null
& $PdfToPpm -png -f 3 -l 3 -r 120 $combinedPdf (Join-Path $renderDir "combined_page_3") | Out-Null

Get-ChildItem -LiteralPath $docxDir -Filter *.docx | Select-Object Name, Length | ConvertTo-Json | Out-File -LiteralPath (Join-Path $renderDir "docx_manifest.json") -Encoding UTF8
Get-ChildItem -LiteralPath $pdfDir -Filter *.pdf | Select-Object Name, Length | ConvertTo-Json | Out-File -LiteralPath (Join-Path $renderDir "pdf_manifest.json") -Encoding UTF8

Write-Output "generated_docx=$((Get-ChildItem -LiteralPath $docxDir -Filter *.docx).Count)"
Write-Output "generated_pdf=$((Get-ChildItem -LiteralPath $pdfDir -Filter *.pdf).Count)"
Write-Output "render_dir=$renderDir"
