@echo off
chcp 65001 >nul 2>&1
setlocal EnableDelayedExpansion

:: ============================================================
:: NiumaAutoCommit - Auto commit script
:: Called every 2 hours by Windows Task Scheduler
:: Uses chcp 65001 (UTF-8) to handle CJK paths correctly
:: ============================================================

set "GIT_ROOT=E:\ai产出文件\牛马"
set "LOG_DIR=%GIT_ROOT%\logs"
set "LOG_FILE=%LOG_DIR%\auto-commit.log"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo [%date% %time%] INFO: Script started >> "%LOG_FILE%"

:: Switch to git root
cd /d "%GIT_ROOT%" 2>nul
if errorlevel 1 (
    echo [%date% %time%] ERROR: Cannot cd to GIT_ROOT >> "%LOG_FILE%"
    exit /b 1
)

:: Verify git repo
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo [%date% %time%] ERROR: Not a git repo >> "%LOG_FILE%"
    exit /b 1
)

:: Check for changes
git status --porcelain > "%TEMP%\niuma_status.txt" 2>&1
set "TOTAL=0"
for /f %%A in ('type "%TEMP%\niuma_status.txt" ^| find /c /v ""') do set "TOTAL=%%A"

if "%TOTAL%"=="0" (
    echo [%date% %time%] INFO: No changes to commit >> "%LOG_FILE%"
    exit /b 0
)

echo [%date% %time%] INFO: Found %TOTAL% changed files >> "%LOG_FILE%"

:: Stage all
git add -A

:: Auto-detect scope
set "SCOPE=auto"
set "TYPE=chore"

git diff --cached --name-only | findstr /i "memory/" >nul 2>&1
if not errorlevel 1 set "SCOPE=memory"

git diff --cached --name-only | findstr /i "sop SOP" >nul 2>&1
if not errorlevel 1 if "!SCOPE!"=="auto" set "SCOPE=sop"

git diff --cached --name-only | findstr /i ".json .yaml .yml CLAUDE.md" >nul 2>&1
if not errorlevel 1 if "!SCOPE!"=="auto" set "SCOPE=config"

:: Build commit message
set "DATESTR=%date:~0,10%"
set "TIMESTR=%time:~0,5%"
set "MSG=%TYPE%(%SCOPE%): auto batch commit %DATESTR% %TIMESTR%"

:: Commit with multi-line message
(
echo %MSG%
echo.
echo Changes: %TOTAL% files
echo Auto-committed by NiumaAutoCommit scheduled task
echo.
echo Agent-Task: auto-scheduled
echo Agent-Model: auto-commit.bat
echo Agent-Decision: batch commit %TOTAL% changes
echo Agent-Limitation: no semantic review, auto-detected type=%TYPE% scope=%SCOPE%
) > "%TEMP%\niuma_commit_msg.txt"

git commit -F "%TEMP%\niuma_commit_msg.txt"

if errorlevel 1 (
    echo [%date% %time%] WARN: Commit failed >> "%LOG_FILE%"
    git reset HEAD >nul 2>&1
    exit /b 1
)

echo [%date% %time%] OK: Committed %TYPE%(%SCOPE%): %TOTAL% files >> "%LOG_FILE%"

:: Push to remote
git remote | findstr "origin" >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=*" %%b in ('git branch --show-current') do set "BRANCH=%%b"
    git push origin !BRANCH! >nul 2>&1
    if not errorlevel 1 (
        echo [%date% %time%] OK: Pushed to origin/!BRANCH! >> "%LOG_FILE%"
    ) else (
        echo [%date% %time%] WARN: Push failed to origin/!BRANCH! >> "%LOG_FILE%"
    )
)

echo [%date% %time%] INFO: Script finished >> "%LOG_FILE%"
del "%TEMP%\niuma_status.txt" >nul 2>&1
del "%TEMP%\niuma_commit_msg.txt" >nul 2>&1
exit /b 0
