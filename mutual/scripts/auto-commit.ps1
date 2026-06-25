# ============================================================
# NiumaAutoCommit - Auto commit script (Windows PowerShell)
# Called every 2 hours by Windows Task Scheduler
# Follows AGENT.md Conventional Commits + Agent Trailer
# ============================================================

# Fix CJK path encoding for git
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

$ErrorActionPreference = "Continue"
$gitRoot = "E:\ai产出文件\牛马"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$logDir = Join-Path $gitRoot "logs"
$logFile = Join-Path $logDir "auto-commit.log"

if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

function Write-Log {
    param([string]$Message)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts | $Message" | Out-File -Append -FilePath $logFile -Encoding UTF8
    Write-Output "$ts | $Message"
}

try {
    Set-Location $gitRoot
} catch {
    Write-Log "ERROR: Cannot cd to $gitRoot"
    exit 1
}

# Use git itself to verify repo (Test-Path has encoding issues with CJK paths)
$gitDir = git rev-parse --git-dir 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Log "ERROR: Not a git repo at $gitRoot"
    exit 1
}

$status = git status --porcelain 2>&1
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Log "INFO: No changes to commit"
    exit 0
}

$lines = ($status -split "`n") | Where-Object { $_.Trim() -ne "" }
$modified = ($lines | Where-Object { $_ -match "^ M|^M " }).Count
$untracked = ($lines | Where-Object { $_ -match "^\?\?" }).Count
$deleted = ($lines | Where-Object { $_ -match "^ D|^D " }).Count
$total = $lines.Count

Write-Log "INFO: Found $total changes (M:$modified U:$untracked D:$deleted)"

git add -A 2>&1 | Out-Null

$date = Get-Date -Format "yyyy-MM-dd HH:mm"

$commitType = "chore"
$scope = "auto"
if ($modified -gt 0 -and $untracked -eq 0 -and $deleted -eq 0) {
    $commitType = "fix"
    $scope = "sync"
} elseif ($untracked -gt $modified) {
    $commitType = "feat"
    $scope = "auto"
}

$hasMemory = $status -match "memory/"
$hasSop = $status -match "(?i)sop"
$hasConfig = $status -match "\.json|\.yaml|\.yml|CLAUDE\.md"

if ($hasMemory) { $scope = "memory" }
if ($hasSop) { $scope = "sop" }
if ($hasConfig -and -not $hasMemory -and -not $hasSop) { $scope = "config" }

$commitMsg = "$commitType($scope): auto batch commit $date`n`nChanges: $total files ($modified modified, $untracked new, $deleted deleted)`nAuto-committed by NiumaAutoCommit scheduled task`n`nAgent-Task: auto-scheduled`nAgent-Model: auto-commit.ps1`nAgent-Decision: batch commit $total changes`nAgent-Limitation: no semantic review, auto-detected type=$commitType scope=$scope"

$result = git commit -m $commitMsg 2>&1
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Log "OK: Committed - $commitType($scope): $total files"

    $branch = git branch --show-current 2>&1

    # Push to GitHub (origin)
    $remote = git remote 2>&1
    if ($remote -and $remote -match "origin") {
        $pushResult = git push origin $branch 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Log "OK: Pushed to GitHub (origin/$branch)"
        } else {
            Write-Log "WARN: GitHub push failed: $pushResult"
        }
    }

    # Push to Gitee
    if ($remote -and $remote -match "gitee") {
        $pushResult = git push gitee $branch 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Log "OK: Pushed to Gitee (gitee/$branch)"
        } else {
            Write-Log "WARN: Gitee push failed: $pushResult"
        }
    }
} else {
    Write-Log "WARN: Commit exit $exitCode : $result"
    git reset HEAD 2>&1 | Out-Null
}

Write-Log "INFO: Script finished"
