#!/usr/bin/env python3
"""
direct_clean.py — 一键清理引擎（无需手动勾选）

流程：扫描 → 分析 → 展示绿灯清单 → 确认 → 清理 → 报告结果

安全设计：
- 只清理绿灯项目（经过295条规则验证的安全缓存/临时文件）
- 使用 send2trash 移入回收站（可撤销，非永久删除）
- 黄灯/红灯项目不碰
- 确认后才执行
"""

import json, os, sys, time, subprocess, shutil, re
from pathlib import Path

# ── 终端颜色 ──
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

    @staticmethod
    def enable():
        """Enable colors on Windows."""
        if sys.platform == 'win32':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetConsoleHandle(-11), 7)
            except:
                pass

# ── 安全的回收站删除 ──
def safe_delete(path):
    """Move file/directory to recycle bin. Returns True on success."""
    if not os.path.exists(path):
        return False

    # Method 1: send2trash (best, cross-platform)
    try:
        import send2trash
        send2trash.send2trash(path)
        return True
    except ImportError:
        pass
    except Exception:
        pass

    # Method 2: Windows Shell COM
    if sys.platform == 'win32':
        try:
            import pythoncom
            from win32com.shell import shell, shellcon

            pythoncom.CoInitialize()
            full_path = os.path.abspath(path)
            result = shell.SHFileOperation(
                0, shellcon.FO_DELETE, full_path, None,
                shellcon.FOF_SILENT | shellcon.FOF_NOCONFIRMATION | shellcon.FOF_ALLOWUNDO
            )
            if result == 0:
                return True
        except ImportError:
            pass
        except Exception:
            pass

    # Method 3: PowerShell (sends to recycle bin on Windows)
    if sys.platform == 'win32':
        try:
            ps_script = f'''
            $shell = New-Object -ComObject Shell.Application
            $folder = $shell.Namespace((Get-Item "{path}").DirectoryName)
            $item = $folder.ParseName((Get-Item "{path}").Name)
            $item.InvokeVerb("delete")
            '''
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', ps_script],
                capture_output=True, timeout=30
            )
            if result.returncode == 0 and not os.path.exists(path):
                return True
        except Exception:
            pass

    return False

def ensure_send2trash():
    """Try to install send2trash if not available."""
    try:
        import send2trash
        return True
    except ImportError:
        print(f"\n  {Colors.YELLOW}安装安全删除库 (send2trash)...{Colors.RESET}")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'send2trash', '-q'],
                         capture_output=True, timeout=30)
            import send2trash
            print(f"  {Colors.GREEN}✓ send2trash 安装成功{Colors.RESET}")
            return True
        except Exception:
            print(f"  {Colors.YELLOW}⚠ send2trash 安装失败，将使用系统回收站方式删除{Colors.RESET}")
            return False

# ── 格式化 ──
def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}" if unit not in ('B',) else f"{int(size_bytes)} B"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"

def plural(n, word):
    return f"{n} {word}{'s' if n != 1 else ''}"

# ── 扫描 ──
def run_scan(scan_all=True, drive=None):
    """Run scan.py and return the raw data path."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    scan_script = os.path.join(script_dir, 'scan.py')

    if not os.path.exists(scan_script):
        # Try scripts/ subdirectory
        scan_script = os.path.join(script_dir, 'scripts', 'scan.py')

    if not os.path.exists(scan_script):
        print(f"{Colors.RED}[错误] 找不到 scan.py{Colors.RESET}")
        sys.exit(1)

    raw_path = os.path.join(os.getcwd(), 'raw_scan.json')

    args = [sys.executable, scan_script]
    if drive:
        args.extend(['--drive', drive])
    else:
        args.append('--all-drives')
    args.extend(['--output', raw_path])

    print(f"\n  {Colors.CYAN}扫描磁盘中...{Colors.RESET}")
    result = subprocess.run(args, capture_output=True, text=True)

    if result.returncode != 0 or not os.path.exists(raw_path):
        print(f"{Colors.RED}[错误] 扫描失败{Colors.RESET}")
        if result.stderr:
            print(result.stderr[:500])
        sys.exit(1)

    return raw_path

# ── 分析 ──
def run_analyze(raw_path):
    """Run auto_analyze.py and return the analysis dict."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    analyze_script = os.path.join(script_dir, 'auto_analyze.py')
    if not os.path.exists(analyze_script):
        analyze_script = os.path.join(script_dir, 'scripts', 'auto_analyze.py')

    analysis_path = os.path.join(os.getcwd(), 'analysis_result.json')

    args = [sys.executable, analyze_script, raw_path, analysis_path]

    print(f"  {Colors.CYAN}分析中 (295条规则)...{Colors.RESET}")
    result = subprocess.run(args, capture_output=True, text=True)

    if result.returncode != 0 or not os.path.exists(analysis_path):
        print(f"{Colors.RED}[错误] 分析失败{Colors.RESET}")
        if result.stderr:
            print(result.stderr[:500])
        sys.exit(1)

    with open(analysis_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# ── 主流程 ──
def main():
    Colors.enable()

    print(f"""
  {Colors.BOLD}{Colors.CYAN}╔════════════════════════════════════════════╗
  ║   Storage Analyzer — 一键清理模式 V4      ║
  ║   295条规则 · 只清绿灯 · 回收站可恢复     ║
  ╚════════════════════════════════════════════╝{Colors.RESET}
""")

    # Parse args
    scan_all = '--all' in sys.argv or '--all-drives' in sys.argv
    drive_only = None
    for i, arg in enumerate(sys.argv):
        if arg == '--drive' and i + 1 < len(sys.argv):
            drive_only = sys.argv[i + 1]
        elif arg.startswith('--drive='):
            drive_only = arg.split('=', 1)[1]

    # Check if we have an existing scan
    raw_path = os.path.join(os.getcwd(), 'raw_scan.json')
    skip_scan = '--no-scan' in sys.argv or '--skip-scan' in sys.argv

    if skip_scan and os.path.exists(raw_path):
        print(f"  {Colors.CYAN}使用已有扫描数据: raw_scan.json{Colors.RESET}")
    else:
        raw_path = run_scan(scan_all, drive_only)

    # Analyze
    analysis = run_analyze(raw_path)

    overview = analysis.get('overview', {})
    green_items = analysis.get('categories', {}).get('green', [])
    yellow_items = analysis.get('categories', {}).get('yellow', [])
    red_items = analysis.get('categories', {}).get('red', [])

    green_total = overview.get('green_total_gb', 0)
    green_count = overview.get('green_count', 0)

    # Show disk overview
    print(f"\n  {Colors.BOLD}═══ 磁盘总览 ═══{Colors.RESET}")
    for d in analysis.get('drives', []):
        pct = d['used_gb'] / d['total_gb'] * 100 if d['total_gb'] > 0 else 0
        bar_len = int(pct / 5)
        bar = '█' * bar_len + '░' * (20 - bar_len)
        color = Colors.RED if pct > 85 else Colors.YELLOW if pct > 70 else Colors.GREEN
        print(f"  {d['letter']}: [{color}{bar}{Colors.RESET}] {d['used_gb']:.0f}/{d['total_gb']:.0f} GB ({pct:.0f}%)")

    print(f"\n  {Colors.BOLD}═══ 分析结果 ═══{Colors.RESET}")
    print(f"  {Colors.GREEN}🟢 可安全清理: {green_count} 项, {format_size(int(green_total * 1024**3))}{Colors.RESET}")
    print(f"  {Colors.YELLOW}🟡 需手动确认: {overview.get('yellow_count', 0)} 项, {overview.get('yellow_total_human', '0')}{Colors.RESET}")
    print(f"  {Colors.RED}🔴 禁止删除:   {overview.get('red_count', 0)} 项, {overview.get('red_total_human', '0')}{Colors.RESET}")

    if green_count == 0:
        print(f"\n  {Colors.GREEN}🎉 没有可清理的安全项目，磁盘状态良好！{Colors.RESET}")
        return

    # Show green items detail
    print(f"\n  {Colors.BOLD}{Colors.GREEN}═══ 以下 {green_count} 项将被清理 ═══{Colors.RESET}")
    print(f"  {'项目':<30} {'大小':>10}  {'位置'}")
    print(f"  {'─'*30} {'─'*10}  {'─'*50}")

    for item in green_items[:30]:  # Show top 30
        name = item.get('label', item.get('name', '未知'))[:28]
        size = format_size(item.get('size_bytes', 0))
        path = item.get('full_path', item.get('path', ''))[:48]
        print(f"  {Colors.GREEN}{name:<30}{Colors.RESET} {size:>10}  {path}")

    if len(green_items) > 30:
        print(f"  {Colors.CYAN}  ... 还有 {len(green_items) - 30} 项 (可在完整报告中查看详情){Colors.RESET}")

    # Confirm
    print(f"\n  {Colors.BOLD}{Colors.GREEN}══════════════════════════════════════════{Colors.RESET}")
    print(f"  {Colors.BOLD}总计释放: {format_size(int(green_total * 1024**3))}{Colors.RESET}")
    print(f"  {Colors.YELLOW}⚠ 所有删除的文件将进入回收站，可随时恢复{Colors.RESET}")
    print()

    # Non-interactive mode support
    if '--yes' in sys.argv or '-y' in sys.argv:
        choice = 'y'
        print(f"  {Colors.CYAN}自动确认模式{Colors.RESET}")
    else:
        choice = input(f"  {Colors.BOLD}确认清理以上 {green_count} 项？(Y/n): {Colors.RESET}").strip().lower()

    if choice and choice not in ('y', 'yes', '是', ''):
        print(f"\n  {Colors.YELLOW}已取消清理。{Colors.RESET}")
        # Still generate report for manual review
        generate_report(analysis)
        return

    # Ensure send2trash is available
    ensure_send2trash()

    # Clean all green items
    print(f"\n  {Colors.CYAN}正在清理...{Colors.RESET}")

    cleaned = 0
    cleaned_size = 0
    failed = []
    skipped = []

    for i, item in enumerate(green_items):
        path = item.get('full_path', item.get('path', ''))
        name = item.get('label', item.get('name', '未知'))
        size = item.get('size_bytes', 0)
        action = item.get('action', 'safe_delete')

        # Skip items that should not be auto-deleted
        if action == 'skip' or action == 'NEVER_DELETE':
            skipped.append((name, path, '规则要求跳过'))
            continue

        # Skip items that need a command (like npm cache clean)
        if action and action != 'safe_delete' and not action.startswith('del '):
            # Try to run the command
            if action.startswith('npm ') or action.startswith('pnpm ') or action.startswith('pip '):
                try:
                    parts = action.split()
                    result = subprocess.run(parts, capture_output=True, timeout=60)
                    if result.returncode == 0:
                        cleaned += 1
                        cleaned_size += size
                        print(f"  {Colors.GREEN}✓{Colors.RESET} {name} ({action})")
                    else:
                        failed.append((name, path, result.stderr.decode('utf-8', errors='replace')[:100]))
                        print(f"  {Colors.RED}✗{Colors.RESET} {name} ({action} 失败)")
                except Exception as e:
                    failed.append((name, path, str(e)))
                    print(f"  {Colors.RED}✗{Colors.RESET} {name} (命令执行失败: {e})")
                continue
            else:
                skipped.append((name, path, f'需要执行: {action}'))
                continue

        # Direct file/directory deletion
        if os.path.exists(path):
            progress = f"[{i+1}/{len(green_items)}]"
            if safe_delete(path):
                cleaned += 1
                cleaned_size += size
                print(f"  {Colors.GREEN}✓{Colors.RESET} {progress} {name} ({format_size(size)})")
            else:
                failed.append((name, path, '删除失败'))
                print(f"  {Colors.RED}✗{Colors.RESET} {progress} {name} — 删除失败")
        else:
            # Path doesn't exist (already cleaned or wrong path)
            skipped.append((name, path, '路径不存在'))
            if i < 5:  # Only show first few to avoid noise
                print(f"  {Colors.YELLOW}~{Colors.RESET} {name} — 路径不存在，跳过")

    # Results
    print(f"\n  {Colors.BOLD}═══ 清理完成 ═══{Colors.RESET}")
    print(f"  {Colors.GREEN}✓ 已清理: {cleaned} 项, 释放 {format_size(cleaned_size)}{Colors.RESET}")

    if skipped:
        print(f"  {Colors.YELLOW}~ 已跳过: {len(skipped)} 项 ({', '.join(s[0] for s in skipped[:3])}{'...' if len(skipped) > 3 else ''}){Colors.RESET}")

    if failed:
        print(f"  {Colors.RED}✗ 失败: {len(failed)} 项{Colors.RESET}")
        for name, path, reason in failed[:5]:
            print(f"    - {name}: {reason}")

    if filled_skipped:
        print(f"\n  {Colors.YELLOW}💡 提示: 部分项目需要通过命令行清理(如 npm cache clean){Colors.RESET}")
        print(f"  {Colors.YELLOW}   这些命令需要对应的工具(npm/pnpm/pip)已安装{Colors.RESET}")

    # Show disk space change
    try:
        remaining_scan = json.load(open(raw_path, 'r', encoding='utf-8'))
        drives_info = remaining_scan.get('drives', [])
        if not drives_info and 'system' in remaining_scan:
            drives_info = [remaining_scan['system']]

        print(f"\n  {Colors.BOLD}═══ 磁盘现状 ═══{Colors.RESET}")
        for d in drives_info:
            letter = d.get('drive', d.get('letter', '?'))
            total = d.get('total_gb', 0)
            used = d.get('used_gb', 0)
            free = d.get('free_gb', 0)
            pct = used / total * 100 if total > 0 else 0
            print(f"  {letter}: {used:.0f}/{total:.0f} GB ({pct:.0f}%) — 可用 {free:.0f} GB")
    except:
        pass

    print(f"\n  {Colors.CYAN}💡 如果需要恢复: 打开回收站 → 找到对应文件 → 右键还原{Colors.RESET}")
    print(f"  {Colors.CYAN}💡 黄灯项目(需手动确认)请运行完整报告模式查看{Colors.RESET}")
    print()

def generate_report(analysis):
    """Generate interactive HTML report for manual review."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        build_script = os.path.join(script_dir, 'build_report.py')
        if not os.path.exists(build_script):
            build_script = os.path.join(script_dir, 'scripts', 'build_report.py')

        subprocess.run([sys.executable, build_script, 'analysis_result.json'],
                      capture_output=True, timeout=30)

        report_path = os.path.join(os.getcwd(), 'report.html')
        if os.path.exists(report_path):
            if sys.platform == 'win32':
                os.startfile(report_path)
            elif sys.platform == 'darwin':
                subprocess.run(['open', report_path])
            else:
                subprocess.run(['xdg-open', report_path])
            print(f"  {Colors.CYAN}📊 完整报告已生成: report.html{Colors.RESET}")
    except Exception as e:
        print(f"  {Colors.YELLOW}⚠ 报告生成失败: {e}{Colors.RESET}")

if __name__ == '__main__':
    main()
