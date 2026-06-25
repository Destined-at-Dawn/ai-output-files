@echo off
chcp 65001 >nul
set GIT_ROOT=E:\ai产出文件\牛马
set GIT_DIR=%GIT_ROOT%\.git
set PATH=C:\Program Files\Git\cmd;C:\Program Files\Git\bin;%PATH%

cd /d "%GIT_ROOT%"

:: Check for changes
git status --porcelain > "%TEMP%\git_status.txt" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] ERROR: git status failed >> "%GIT_ROOT%\logs\auto-commit.log"
    exit /b 1
)

:: Count lines
for /f %%a in ('type "%TEMP%\git_status.txt" ^| find /c /v ""') do set TOTAL=%%a
if "%TOTAL%"=="0" (
    echo [%date% %time%] INFO: No changes >> "%GIT_ROOT%\logs\auto-commit.log"
    exit /b 0
)

:: Stage and commit
git add -A
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set DATESTR=%%a-%%b-%%c
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set TIMESTR=%%a:%%b
git commit -m "chore(auto): batch commit %DATESTR% %TIMESTR% — %TOTAL% files"
if %ERRORLEVEL% EQU 0 (
    echo [%date% %time%] OK: Committed %TOTAL% files >> "%GIT_ROOT%\logs\auto-commit.log"
    :: Push to GitHub
    git push origin main 2>>"%GIT_ROOT%\logs\auto-commit.log"
    if %ERRORLEVEL% EQU 0 (
        echo [%date% %time%] OK: Pushed to GitHub >> "%GIT_ROOT%\logs\auto-commit.log"
    ) else (
        echo [%date% %time%] WARN: GitHub push failed >> "%GIT_ROOT%\logs\auto-commit.log"
    )
    :: Push to Gitee
    git push gitee main 2>>"%GIT_ROOT%\logs\auto-commit.log"
    if %ERRORLEVEL% EQU 0 (
        echo [%date% %time%] OK: Pushed to Gitee >> "%GIT_ROOT%\logs\auto-commit.log"
    ) else (
        echo [%date% %time%] WARN: Gitee push failed >> "%GIT_ROOT%\logs\auto-commit.log"
    )
) else (
    echo [%date% %time%] WARN: Commit failed >> "%GIT_ROOT%\logs\auto-commit.log"
)
