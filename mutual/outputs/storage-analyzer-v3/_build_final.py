#!/usr/bin/env python3
"""Final build: macOS sh + READMEs + all 3 ZIP packages."""
import sys, os, shutil, zipfile
sys.stdout.reconfigure(encoding='utf-8')

base = r'E:\ai产出文件\牛马\mutual\mutual\outputs\storage-analyzer-v3'
skill_src = r'E:\ai产出文件\牛马\mutual\mutual\skills\storage-analyzer'
packages_dir = os.path.join(base, 'packages')
_tmp = os.path.join(base, '_tmp_pack')

os.makedirs(packages_dir, exist_ok=True)
os.makedirs(_tmp, exist_ok=True)

def copy_tree(src_root, dst_root, file_list):
    for f in file_list:
        src = os.path.join(src_root, f)
        dst = os.path.join(dst_root, f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            shutil.copy(src, dst)

def zip_dir(src_dir, zip_path, prefix):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(src_dir):
            for f_name in files:
                full = os.path.join(root, f_name)
                arcname = os.path.join(prefix, os.path.relpath(full, src_dir))
                z.write(full, arcname)
    return os.path.getsize(zip_path)

# ============================================================
# 1. macOS shell script
# ============================================================
macos_sh = """#!/bin/bash
# Storage Analyzer V4 — One-Click Clean (macOS)
set -e

echo
echo "    ╔══════════════════════════════════════════╗"
echo "    ║   Storage Analyzer — 磁盘清理工具 V4     ║"
echo "    ║   295条规则 · 回收站保护 · 3秒确认即清   ║"
echo "    ╚══════════════════════════════════════════╝"
echo

# Check Python3
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found. Please install Python 3.8+"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "Select mode:"
echo
echo "  [1] One-Click Clean (auto-clean all safe items)  RECOMMENDED"
echo "  [2] Full Report (scan + interactive report)"
echo "  [3] Scan Only (analysis only, no deletion)"
echo "  [4] Exit"
echo

read -p "Enter choice (1/2/3/4): " choice

case $choice in
  1)
    echo
    echo "[Scan] Scanning all disks..."
    python3 scripts/scan.py --all-drives --output raw_scan.json

    echo "[Analyze] Running 295 rules..."
    python3 scripts/auto_analyze.py raw_scan.json analysis_result.json

    echo "[Clean] One-click clean mode..."
    python3 scripts/direct_clean.py --no-scan --yes
    ;;
  2)
    echo
    echo "[Scan] Scanning all disks..."
    python3 scripts/scan.py --all-drives --output raw_scan.json
    echo "[Analyze] Running 295 rules..."
    python3 scripts/auto_analyze.py raw_scan.json analysis_result.json
    echo "[Report] Generating report..."
    python3 scripts/build_report.py analysis_result.json
    open report.html 2>/dev/null || xdg-open report.html 2>/dev/null
    ;;
  3)
    echo
    echo "[Scan] Scanning all disks..."
    python3 scripts/scan.py --all-drives --output raw_scan.json
    echo "[Analyze] Running 295 rules..."
    python3 scripts/auto_analyze.py raw_scan.json analysis_result.json
    python3 scripts/build_report.py analysis_result.json
    open report.html 2>/dev/null || xdg-open report.html 2>/dev/null
    ;;
  4) exit 0 ;;
  *) echo "Invalid choice"; exit 1 ;;
esac

echo
echo "    ╔══════════════════════════════════════════╗"
echo "    ║  Cleanup complete!                       ║"
echo "    ║  Files moved to Trash, restorable anytime ║"
echo "    ╚══════════════════════════════════════════╝"
"""

with open(os.path.join(_tmp, '一键清理.sh'), 'w', encoding='utf-8') as f:
    f.write(macos_sh)
print('[OK] macOS script')

# ============================================================
# 2. V1 README
# ============================================================
v1_readme = """# Storage Analyzer - AI Enhanced Edition (V1)

Requires an AI agent (Claude Code / ChatGPT / etc.) for the analysis step.

## How to use

1. Scan your disks:
   ```
   python scripts/scan.py --all-drives --output raw_scan.json
   ```

2. Feed raw_scan.json to your AI agent. Tell it:
   > Analyze this disk scan data. Classify each entry as GREEN (safe cache, auto-clean),
   > YELLOW (needs judgment), or RED (never delete). Output as analysis_result.json.

3. Generate the interactive report:
   ```
   python scripts/build_report.py analysis_result.json
   ```

4. Open report.html in your browser.

## For a simpler experience (no AI needed)
Use the V2 Standalone Edition instead — just double-click the .bat file.
"""

with open(os.path.join(_tmp, 'v1-readme.md'), 'w', encoding='utf-8') as f:
    f.write(v1_readme)

# ============================================================
# 3. V2 README
# ============================================================
v2_readme = """# Storage Analyzer - Standalone Edition V4

One-click disk cleanup. No AI. No tech skills needed. Just double-click.

## Quick Start (Windows)

1. Double-click: `一键清理.bat`
2. Choose [1] for one-click clean
3. Wait ~1-3 minutes for scan
4. Press Enter to confirm
5. Done! Files go to Recycle Bin (recoverable)

## Quick Start (macOS)

1. Double-click: `一键清理.sh`
2. Follow prompts

## What gets cleaned (GREEN light only)

- Browser caches (Chrome, Edge, Firefox, Brave...)
- System temp files (%TEMP%, /tmp)
- Dev caches (npm, pip, pnpm, uv, cargo, gradle, maven, cmake...)
- IDE caches (JetBrains, VSCode, Android Studio...)
- App caches (WeChat, QQ, Douyin, Bilibili, NetEase, WPS, DingTalk, Feishu...)
- Game caches (Steam, Epic, Unity, Unreal...)
- Error reports & logs
- Installer caches & updaters
- Docker builder cache
- AI/ML caches (PyTorch, TF, HuggingFace...)
- Windows Update cache, Prefetch, Thumbnails

## What is NEVER touched (RED light)

- System directories (C:\\\\Windows, System32)
- Program installations (Program Files)
- Your documents, photos, music, videos
- Git repositories (.git)
- App configurations (AppData/Roaming)
- Drivers & firmware
- Antivirus software
- OneDrive / cloud sync folders

## Safety Guarantees

1. **295 verification rules** — only verified-safe cache files
2. **Recycle Bin** — all deletions go to Recycle Bin (Windows) / Trash (macOS)
3. **Recoverable** — restore any file from Recycle Bin anytime
4. **Read-only scan** — scanning never modifies any files
5. **No permanent delete** — uses send2trash, not os.remove()

## Menu Options

| Option | Description |
|--------|-------------|
| [1] One-Click Clean | Scan → Auto-clean all GREEN items → Done |
| [2] Full Report | Scan → Interactive HTML report → Choose items → Clean |
| [3] Scan Only | Scan → Analysis → View report (no deletion) |

## Advanced

### Install as AI skill (for Newmax / Claude Code users)

Copy the `skill/` folder to `~/.newmax/skills/storage-analyzer/`.
Then say "C盘满了" or "帮我清理磁盘" and it auto-triggers.

### Command-line usage

```bash
# Full one-click clean
python scripts/direct_clean.py --all-drives --yes

# Scan only
python scripts/scan.py --all-drives --output raw_scan.json

# Analyze only
python scripts/auto_analyze.py raw_scan.json analysis_result.json

# Generate HTML report
python scripts/build_report.py analysis_result.json

# Start web server (interactive cleanup)
python scripts/server.py analysis_result.json
```
"""

with open(os.path.join(_tmp, 'v2-readme.md'), 'w', encoding='utf-8') as f:
    f.write(v2_readme)

# ============================================================
# 4. Build V1 package
# ============================================================
v1_dir = os.path.join(_tmp, 'v1-build')
os.makedirs(v1_dir, exist_ok=True)

v1_files = [
    'SKILL.md',
    'assets/report_template.html',
    'references/macos.md', 'references/windows.md',
    'scripts/scan.py', 'scripts/server.py', 'scripts/build_report.py',
]
copy_tree(skill_src, v1_dir, v1_files)
shutil.copy(os.path.join(_tmp, 'v1-readme.md'), os.path.join(v1_dir, 'README.md'))

# Add skill/ subdir (full copy of skill source)
skill_dst = os.path.join(v1_dir, 'skill')
if os.path.exists(skill_dst):
    shutil.rmtree(skill_dst)
shutil.copytree(skill_src, skill_dst)

v1_zip = os.path.join(packages_dir, 'Storage-Analyzer-V1-AI增强版+技能.zip')
size1 = zip_dir(v1_dir, v1_zip, 'Storage-Analyzer-V1-AI-Enhanced')
print(f'[OK] V1: {size1//1024} KB')

# ============================================================
# 5. Build V2 package
# ============================================================
v2_dir = os.path.join(_tmp, 'v2-build')
os.makedirs(v2_dir, exist_ok=True)

v2_files = v1_files + ['scripts/auto_analyze.py', 'scripts/direct_clean.py']
copy_tree(skill_src, v2_dir, v2_files)
shutil.copy(os.path.join(_tmp, 'v2-readme.md'), os.path.join(v2_dir, 'README.md'))
shutil.copy(os.path.join(_tmp, '一键清理.bat'), os.path.join(v2_dir, '一键清理.bat'))
shutil.copy(os.path.join(_tmp, '一键清理.sh'), os.path.join(v2_dir, '一键清理.sh'))

# Add skill/ subdir
skill_dst2 = os.path.join(v2_dir, 'skill')
if os.path.exists(skill_dst2):
    shutil.rmtree(skill_dst2)
shutil.copytree(skill_src, skill_dst2)

v2_zip = os.path.join(packages_dir, 'Storage-Analyzer-V2-独立版+技能.zip')
size2 = zip_dir(v2_dir, v2_zip, 'Storage-Analyzer-V2-Standalone')
print(f'[OK] V2: {size2//1024} KB')

# ============================================================
# 6. Build Complete package
# ============================================================
complete_dir = os.path.join(_tmp, 'complete-build')
os.makedirs(complete_dir, exist_ok=True)

# Copy V1
v1_dst = os.path.join(complete_dir, 'V1-AI增强版')
if os.path.exists(v1_dst):
    shutil.rmtree(v1_dst)
shutil.copytree(v1_dir, v1_dst)

# Copy V2
v2_dst = os.path.join(complete_dir, 'V2-独立版')
if os.path.exists(v2_dst):
    shutil.rmtree(v2_dst)
shutil.copytree(v2_dir, v2_dst)

# Add tutorial
tutorial_paths = [
    os.path.join(base, '..', 'tutorials', 'Storage-Analyzer-学员教程-行动手册.md'),
    r'E:\ai产出文件\牛马\mutual\mutual\outputs\tutorials\Storage-Analyzer-学员教程-行动手册.md',
]
for tp in tutorial_paths:
    if os.path.exists(tp):
        shutil.copy(tp, os.path.join(complete_dir, '学员教程.md'))
        print('[OK] Tutorial added')
        break
else:
    print('[WARN] Tutorial not found')

complete_zip = os.path.join(packages_dir, 'Storage-Analyzer-完整包+技能.zip')
size3 = zip_dir(complete_dir, complete_zip, 'Storage-Analyzer-Complete')
print(f'[OK] Complete: {size3//1024} KB')

# ============================================================
# 7. Final verification
# ============================================================
print()
print('=== Final Verification ===')
for fname in sorted(os.listdir(packages_dir)):
    fpath = os.path.join(packages_dir, fname)
    size_kb = os.path.getsize(fpath) // 1024
    # Check contents
    with zipfile.ZipFile(fpath, 'r') as z:
        names = z.namelist()
        has_skill = any('skill/' in n for n in names)
        has_auto = any('auto_analyze.py' in n for n in names)
        has_direct = any('direct_clean.py' in n for n in names)
        has_bat = any(n.endswith('.bat') for n in names)
        print(f'  {fname}')
        print(f'    Size: {size_kb} KB | Files: {len(names)}')
        print(f'    skill/: {has_skill} | auto_analyze: {has_auto} | direct_clean: {has_direct} | .bat: {has_bat}')

print()
print('=== DONE ===')
