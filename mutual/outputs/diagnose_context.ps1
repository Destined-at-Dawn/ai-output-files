# Diagnostic script - measure context pressure
$rulesDir = 'E:\ai产出文件\牛马\mutual\mutual\.claude\rules\'
$claudeMd = 'E:\ai产出文件\牛马\mutual\mutual\CLAUDE.md'

Write-Output "=== CLAUDE.md ==="
$claudeSize = (Get-Content $claudeMd -Raw).Length
$claudeLines = (Get-Content $claudeMd).Count
Write-Output "Size: $claudeSize bytes, Lines: $claudeLines"

Write-Output "`n=== .claude/rules/ files ==="
$totalRulesSize = 0
$totalRulesLines = 0
$ruleFiles = Get-ChildItem $rulesDir -Filter *.md | Sort-Object Length -Descending
foreach ($f in $ruleFiles) {
    $size = $f.Length
    $lines = (Get-Content $f.FullName).Count
    $totalRulesSize += $size
    $totalRulesLines += $lines
    Write-Output "  $($f.Name): $size bytes, $lines lines"
}
Write-Output "Total rules: $totalRulesSize bytes, $totalRulesLines lines across $($ruleFiles.Count) files"

Write-Output "`n=== .claude/ all files ==="
$allFiles = Get-ChildItem 'E:\ai产出文件\牛马\mutual\mutual\.claude\' -Recurse -File
$totalAllSize = ($allFiles | Measure-Object Length -Sum).Sum
Write-Output "Total: $($allFiles.Count) files, $totalAllSize bytes"

Write-Output "`n=== Combined context pressure ==="
Write-Output "CLAUDE.md + rules = $($claudeSize + $totalRulesSize) bytes ($($claudeLines + $totalRulesLines) lines)"
Write-Output "All .claude/ = $($claudeSize + $totalAllSize) bytes"

Write-Output "`n=== Hook scripts ==="
Get-ChildItem 'E:\ai产出文件\牛马\mutual\mutual\.claude\hooks\*.py' | ForEach-Object {
    $size = (Get-Content $_.FullName -Raw).Length
    Write-Output "  $($_.Name): $size bytes"
}
