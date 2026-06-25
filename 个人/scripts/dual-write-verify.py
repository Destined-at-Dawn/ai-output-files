#!/usr/bin/env python3
"""双写验证脚本 — 检查自我进化文件是否同步到位

用法：
  python dual-write-verify.py              # 检查全部
  python dual-write-verify.py --module 社群运营  # 只检查一个模块
  python dual-write-verify.py --fix        # 自动补全缺失的副本

设计原则（来自教训E27）：
  - 用 os.path.exists() 验证，不用 PowerShell/Test-Path（中文路径静默失败）
  - 用 Python shutil 复制，不用 PowerShell Copy-Item
  - 用 UTF-8 编码，不用 GBK
"""

import os
import sys
import shutil
from datetime import datetime

# 强制 UTF-8 输出（Windows GBK 控制台兼容）
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# === 路径配置 ===
ROOT_WORKSPACE = r"E:\ai产出文件\牛马\创作\创作"
ROOT_EVOLUTION = os.path.join(ROOT_WORKSPACE, "自我进化")

# 模块级经验库映射：模块名 → 模块路径（相对于 20260425-内容创作系统/）
MODULE_MAP = {
    "社群运营": os.path.join(ROOT_WORKSPACE, "projects", "20260425-内容创作系统", "社群运营", "经验库"),
    # 未来扩展：
    # "公众号": os.path.join(ROOT_WORKSPACE, "projects", "20260425-内容创作系统", "公众号", "经验库"),
    # "图片提示词": os.path.join(ROOT_WORKSPACE, "projects", "20260425-内容创作系统", "图片提示词", "经验库"),
}

def get_files(directory, subdir=""):
    """获取目录下所有文件名"""
    target = os.path.join(directory, subdir) if subdir else directory
    if not os.path.exists(target):
        return set()
    return set(f for f in os.listdir(target) if os.path.isfile(os.path.join(target, f)))

def verify_dual_write(module_name=None, fix=False):
    """验证双写完整性"""
    results = {"matched": 0, "missing_in_module": 0, "missing_in_root": 0, "fixed": 0}
    modules_to_check = {module_name: MODULE_MAP[module_name]} if module_name and module_name in MODULE_MAP else MODULE_MAP

    for mod_name, mod_path in modules_to_check.items():
        print(f"\n{'='*60}")
        print(f"模块: {mod_name}")
        print(f"{'='*60}")

        # 做得好的
        for category, root_sub, mod_sub in [
            ("成功经验", "做得好的", "做得好的"),
            ("失败教训", "做得差的避免", "做得差的"),
        ]:
            root_dir = os.path.join(ROOT_EVOLUTION, root_sub)
            mod_dir = os.path.join(mod_path, mod_sub)

            root_files = get_files(root_dir)
            mod_files = get_files(mod_dir)

            # 检查根级 → 模块级（社群运营相关的是否同步到了模块）
            for f in sorted(root_files):
                # 只检查与当前模块相关的文件
                if not _is_relevant(f, mod_name):
                    continue

                if f in mod_files:
                    results["matched"] += 1
                    # 验证文件大小一致（防止空文件假阳性）
                    root_size = os.path.getsize(os.path.join(root_dir, f))
                    mod_size = os.path.getsize(os.path.join(mod_dir, f))
                    if root_size != mod_size:
                        print(f"  ⚠️ 大小不一致: {f} (根:{root_size}B vs 模块:{mod_size}B)")
                else:
                    results["missing_in_module"] += 1
                    print(f"  ❌ {category}缺失(模块级): {f}")
                    if fix:
                        src = os.path.join(root_dir, f)
                        dst = os.path.join(mod_dir, f)
                        os.makedirs(mod_dir, exist_ok=True)
                        shutil.copy2(src, dst)
                        if os.path.exists(dst):
                            results["fixed"] += 1
                            print(f"     ✅ 已自动补全")
                        else:
                            print(f"     ❌ 补全失败")

            # 检查模块级 → 根级（有没有只写了模块没写根的）
            for f in sorted(mod_files):
                if f not in root_files:
                    results["missing_in_root"] += 1
                    print(f"  ❌ {category}缺失(根级): {f}")
                    if fix:
                        src = os.path.join(mod_dir, f)
                        dst = os.path.join(root_dir, f)
                        os.makedirs(root_dir, exist_ok=True)
                        shutil.copy2(src, dst)
                        if os.path.exists(dst):
                            results["fixed"] += 1
                            print(f"     ✅ 已自动补全")

    # 汇总
    print(f"\n{'='*60}")
    print(f"验证结果")
    print(f"{'='*60}")
    print(f"  ✅ 已同步: {results['matched']}")
    print(f"  ❌ 缺失(模块级): {results['missing_in_module']}")
    print(f"  ❌ 缺失(根级): {results['missing_in_root']}")
    if fix:
        print(f"  🔧 自动补全: {results['fixed']}")

    total = results['matched'] + results['missing_in_module'] + results['missing_in_root']
    if total > 0:
        sync_rate = results['matched'] / total * 100
        print(f"  📊 同步率: {sync_rate:.0f}%")
    else:
        print(f"  📊 无相关文件可检查")

    return results

def _is_relevant(filename, module_name):
    """判断根级自我进化文件是否与某模块相关"""
    keywords = {
        "社群运营": ["社群", "群公告", "嘉宾", "引流", "分享", "向阳", "双写", "经验库"],
    }
    if module_name not in keywords:
        return True  # 未定义关键词的模块，假设全部相关
    for kw in keywords[module_name]:
        if kw in filename:
            return True
    return False

if __name__ == "__main__":
    fix = "--fix" in sys.argv
    module = None
    for i, arg in enumerate(sys.argv):
        if arg == "--module" and i + 1 < len(sys.argv):
            module = sys.argv[i + 1]

    verify_dual_write(module_name=module, fix=fix)
