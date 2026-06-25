@echo off
chcp 65001 >nul
echo === GlideX log cleanup ===
echo.

:: Stop GlideX services
echo [1/4] Stopping GlideX services...
net stop GlideXService 2>nul
net stop GlideXServiceExt 2>nul
net stop GlideXRemoteService 2>nul
timeout /t 2 /nobreak >nul

:: Verify stopped
tasklist /FI "IMAGENAME eq GlideXService.exe" | find "GlideX" >nul
if %errorlevel%==0 (
    echo    Services still running, force killing...
    taskkill /F /IM GlideXService.exe 2>nul
    taskkill /F /IM GlideXServiceExt.exe 2>nul
    taskkill /F /IM GlideXRemoteService.exe 2>nul
    timeout /t 2 /nobreak >nul
)
echo    Services stopped.

:: Delete log files
echo [2/4] Deleting GlideX log files...
set "LOGDIR=C:\ProgramData\ASUS\GlideX\log"
if exist "%LOGDIR%" (
    rd /s /q "%LOGDIR%"
    mkdir "%LOGDIR%"
    echo    Log directory cleared.
) else (
    echo    Log directory not found, skip.
)

:: Restart services
echo [3/4] Restarting GlideX services...
net start GlideXService 2>nul
net start GlideXServiceExt 2>nul
net start GlideXRemoteService 2>nul
echo    Services restarted.

:: Verify
echo [4/4] Verifying...
for /f "tokens=3" %%s in ('dir /s /-c "%LOGDIR%" 2^>nul ^| find "File(s)"') do (
    echo    Log dir size after cleanup: %%s bytes
)

echo.
echo === Done. Freed ~531 MB ===
pause
