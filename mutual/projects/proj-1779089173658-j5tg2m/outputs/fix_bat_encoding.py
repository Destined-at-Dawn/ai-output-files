# -*- coding: utf-8 -*-
"""Create GBK-encoded bat files for Windows cmd.exe"""
import os

desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# Workspace paths
WS = [
    ("ws1", "E:\\ai产出文件\\牛马\\mutual\\mutual"),
    ("ws2", "E:\\ai产出文件\\牛马\\个人\\个人"),
    ("ws3", "E:\\ai产出文件\\牛马\\创作\\创作"),
    ("ws4", "E:\\ai产出文件\\牛马\\求职\\求职"),
    ("ws5", "E:\\ai产出文件\\牛马\\竞赛\\竞赛"),
]

# === Main launcher ===
lines = [
    "@echo off",
    "chcp 65001 >nul 2>&1",
    "title Claude Code Launcher",
    "",
    "echo ============================================",
    "echo   Workspace Launcher",
    "echo ============================================",
    "echo.",
    "echo   1. mutual       [management]",
    "echo   2. geren        [personal]",
    "echo   3. chuangzuo    [creation]",
    "echo   4. qiuzhi       [career]",
    "echo   5. jingsai      [competition]",
    "echo   0. Exit",
    "echo ============================================",
    "echo.",
    "set /p choice=\"Select [1-5]: \"",
    "",
    "if \"%choice%\"==\"1\" goto :ws1",
    "if \"%choice%\"==\"2\" goto :ws2",
    "if \"%choice%\"==\"3\" goto :ws3",
    "if \"%choice%\"==\"4\" goto :ws4",
    "if \"%choice%\"==\"5\" goto :ws5",
    "if \"%choice%\"==\"0\" exit",
    "echo Invalid choice",
    "pause",
    "exit /b 1",
    "",
]

for label, path in WS:
    lines.append(f":{label}")
    lines.append(f'cd /d "{path}"')
    lines.append("goto :launch")
    lines.append("")

lines += [
    ":launch",
    "echo.",
    "echo Workspace: %cd%",
    "echo Starting Claude Code...",
    "echo.",
    "claude",
]

content = "\r\n".join(lines)
bat_path = os.path.join(desktop, "claude.bat")
with open(bat_path, "wb") as f:
    f.write(content.encode("gbk"))
print(f"OK: claude.bat ({os.path.getsize(bat_path)}B)")

# === Per-workspace quick launchers ===
for i, (label, path) in enumerate(WS, 1):
    fname = f"claude-ws{i}.bat"
    bat = f'@echo off\r\nchcp 65001 >nul 2>&1\r\ntitle Claude - {label}\r\ncd /d "{path}"\r\necho Workspace: %cd%\r\nclaude\r\n'
    fp = os.path.join(desktop, fname)
    with open(fp, "wb") as f:
        f.write(bat.encode("gbk"))
    print(f"OK: {fname}")

# === Verify paths exist ===
print("\nPath check:")
for label, path in WS:
    exists = os.path.isdir(path)
    print(f"  {label}: {path[-30:]} -> {'OK' if exists else 'MISSING'}")

# === Verify bat content ===
print("\nBat content check:")
with open(bat_path, "rb") as f:
    text = f.read().decode("gbk")
for label, path in WS:
    found = path in text
    print(f"  {label}: path_in_bat={'YES' if found else 'NO'}")
