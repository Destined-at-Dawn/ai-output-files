[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# ai产出文件/牛马 detail (36.87 GB!)
Write-Output "=== ai产出文件\牛马 (36.87 GB) ==="
$niumaPath = Get-ChildItem "E:\ai产出文件" -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -eq '牛马' }
if ($niumaPath) {
    Get-ChildItem $niumaPath.FullName -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        $s = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
        [PSCustomObject]@{Name=$_.Name; SizeGB=[math]::Round($s/1GB,2)}
    } | Sort-Object SizeGB -Descending | Format-Table -AutoSize
}

# 网盘下载/百度 detail
Write-Output "`n=== 网盘下载\百度 (7.8 GB) ==="
$baiduPath = Get-ChildItem "E:\" -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name.Length -le 6 }
Get-ChildItem $baiduPath.FullName -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $s = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 100MB) {
        Write-Output ("  {0} -> {1:N2} GB" -f $_.Name, ($s/1GB))
    }
}

# WeChat msg detail
Write-Output "`n=== WeChat msg breakdown ==="
$msgPath = Get-ChildItem "E:\xwechat_files\wxid_3nvidmluot0a22_72ff\msg" -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '^[a-f0-9]{32}$' } | ForEach-Object {
    $s = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{Name=$_.Name; SizeGB=[math]::Round($s/1GB,2)}
} | Sort-Object SizeGB -Descending | Select-Object -First 10
$msgPath | Format-Table -AutoSize

# WeChat Backup detail
Write-Output "`n=== WeChat Backup ==="
Get-ChildItem "E:\xwechat_files\Backup" -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $s = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    Write-Output ("  {0} -> {1:N2} GB" -f $_.Name, ($s/1GB))
}

# Cache contents
Write-Output "`n=== Cache ==="
Get-ChildItem "E:\Cache" -File -ErrorAction SilentlyContinue | Where-Object { $_.Length -gt 100MB } | Sort-Object Length -Descending | ForEach-Object {
    Write-Output ("  {0} ({1:N0} MB)" -f $_.Name, ($_.Length/1MB))
}

# 通用skill
Write-Output "`n=== 通用skill (1.28 GB) ==="
$skillPath = Get-ChildItem "E:\ai产出文件" -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match 'skill' }
Get-ChildItem $skillPath.FullName -File -ErrorAction SilentlyContinue | Where-Object { $_.Length -gt 50MB } | Sort-Object Length -Descending | ForEach-Object {
    Write-Output ("  {0} ({1:N0} MB)" -f $_.Name, ($_.Length/1MB))
}
