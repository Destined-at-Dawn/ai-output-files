# Auto-commit script for Niuma mutual workspace
# Runs every 2 hours via Windows Task Scheduler
# Created: 2026-05-20
# Updated: 2026-05-20 - Fix repo root + dual push (GitHub + Gitee)

# Find git repo root by walking up from script location
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoPath = $scriptDir
while ($repoPath -and -not (Test-Path (Join-Path $repoPath ".git"))) {
    $repoPath = Split-Path -Parent $repoPath
}
if (-not $repoPath) {
    Write-Error "Cannot find .git directory"
    exit 1
}
$logFile = Join-Path $scriptDir "git-auto-commit.log"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Out-File -FilePath $logFile -Append -Encoding UTF8
}

try {
    Set-Location $repoPath
    Write-Log "Repo root: $repoPath"

    # Check for changes
    $status = git status --porcelain
    if ([string]::IsNullOrWhiteSpace($status)) {
        Write-Log "No changes detected"
        exit 0
    }

    # Count changes
    $changeCount = ($status -split "`n").Count
    Write-Log "Detected $changeCount changed files"

    # Stage all changes
    git add -A

    # Create commit with timestamp
    $commitMsg = "auto: batch commit $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git commit -m $commitMsg

    Write-Log "Committed: $commitMsg"

    # Push to GitHub (primary)
    try {
        $env:GH_TOKEN = (gh auth token 2>$null)
        $pushResult = git push origin main 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Log "Push to GitHub (origin) succeeded"
        } else {
            Write-Log "Push to GitHub failed: $pushResult"
        }
    } catch {
        Write-Log "GitHub push exception: $_"
    }

    # Push to Gitee (backup) - non-blocking
    try {
        $giteeExists = git remote get-url gitee 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pushResult2 = git push gitee main 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Log "Push to Gitee (backup) succeeded"
            } else {
                Write-Log "Push to Gitee failed (non-critical): $pushResult2"
            }
        }
    } catch {
        Write-Log "Gitee push exception (non-critical): $_"
    }

} catch {
    Write-Log "ERROR: $_"
}
