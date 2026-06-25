@echo off
chcp 65001 >nul 2>&1
title 牛马AI 工作区启动器

echo ============================================
echo   牛马AI 工作区启动器
echo ============================================
echo.
echo  1. mutual    [管理/优化] — 当前位置
echo  2. 个人      [个人成长/数字先知]
echo  3. 创作      [内容创作/公众号/小红书]
echo  4. 求职      [实习/简历/求职策略]
echo  5. 竞赛      [FPGA/电赛/竞赛]
echo.
echo  0. 退出
echo ============================================
echo.

set /p choice="选择工作区 [1-5]: "

if "%choice%"=="1" (
    cd /d "E:\ai产出文件\牛马\mutual\mutual"
    goto :launch
)
if "%choice%"=="2" (
    cd /d "E:\ai产出文件\牛马\个人\个人"
    goto :launch
)
if "%choice%"=="3" (
    cd /d "E:\ai产出文件\牛马\创作\创作"
    goto :launch
)
if "%choice%"=="4" (
    cd /d "E:\ai产出文件\牛马\求职\求职"
    goto :launch
)
if "%choice%"=="5" (
    cd /d "E:\ai产出文件\牛马\竞赛\竞赛"
    goto :launch
)
if "%choice%"=="0" exit
echo [错误] 无效选择
pause
exit /b 1

:launch
echo.
echo 工作区: %cd%
echo 启动 Claude Code...
echo.
claude
