[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Get exact folder paths dynamically
Write-Output "=== E Drive Folder Scan ==="
Get-ChildItem "E:\" -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $folder = $_
    $s = (Get-ChildItem $folder.FullName -Recurse -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
    if ($s -gt 1GB) {
        Write-Output ("`n=== {0} ({1:N2} GB) ===" -f $folder.Name, ($s/1GB))
        # Show top sub-items
        Get-ChildItem $folder.FullName -Directory -ErrorAction SilentlyContinue | ForEach-Object {
            $ss = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
            if ($ss -gt 500MB) {
                Write-Output ("  {0} -> {1:N2} GB" -f $_.Name, ($ss/1GB))
            }
        }
        # Show large files
        Get-ChildItem $folder.FullName -File -ErrorAction SilentlyContinue | Where-Object { $_.Length -gt 500MB } | Sort-Object Length -Descending | ForEach-Object {
            Write-Output ("  [FILE] {0} ({1:N0} MB)" -f $_.Name, ($_.Length/1MB))
        }
    }
}

# Steam games detail
Write-Output "`n=== SteamLibrary detail ==="
Get-ChildItem "E:\SteamLibrary\steamapps" -File -Filter "*.acf" -ErrorAction SilentlyContinue | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
    $nameMatch = [regex]::Match($content, '"name"\s+"([^"]+)"')
    $sizeMatch = [regex]::Match($content, '"SizeOnDisk"\s+"(\d+)"')
    if ($nameMatch.Success -and $sizeMatch.Success) {
        $sizeGB = [math]::Round([long]$sizeMatch.Groups[1].Value/1GB, 2)
        Write-Output ("  {0}: {1:N2} GB" -f $nameMatch.Groups[1].Value, $sizeGB)
    }
}

# WeChat files detail
Write-Output "`n=== WeChat files detail ==="
Get-ChildItem "E:\xwechat_files" -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $dir = $_
    Get-ChildItem $dir.FullName -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        $ss = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum
        if ($ss -gt 500MB) {
            Write-Output ("  {0}\{1} -> {2:N2} GB" -f $dir.Name, $_.Name, ($ss/1GB))
        }
    }
}

# 网盘下载
Write-Output "`n=== net disk downloads ==="
Get-ChildItem "E:\" -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name.Length -gt 1 -and $_.Name.Length -lt 10 } | ForEach-Object {
    $dir = $_
    Get-ChildItem $dir.FullName -File -ErrorAction SilentlyContinue | Where-Object { $_.Length -gt 200MB } | Sort-Object Length -Descending | ForEach-Object {
        Write-Output ("  {0}\{1} ({2:N0} MB) - {3}" -f $dir.Name, $_.Name, ($_.Length/1MB), $_.LastWriteTime.ToString('yyyy-MM-dd'))
    }
}
