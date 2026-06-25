#!/usr/bin/env python3
"""
双写验证脚本（Dual-Write Verify）
检查经验库文件是否与 self-evolution 同步。

用法：
  python dual-write-verify.py                    # 全量检查
  python dual-write-verify.py --module 社群运营   # 只检查一个模块
  python dual-write-verify.py --fix               # 自动修复缺失的副本
  python dual-write-verify.py --fix --module 社群运营

规则：
  - self-evolution/做得差的避免/ 中的每个教训
    必须在对应模块的 经验库/做得差的/ 中有对应案例文件
  - 反之亦然
  - 案例文件必须包含教训编号引用（E{NNN}）
"""

import os
import re
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# === 路径配置 ===
WORKSPACE = r"E:\ai产出文件\牛马\创作\创作"
SELF_EVOLUTION_BAD = os.path.join(WORKSPACE, "self-evolution", "做得差的避免")
SELF_EVOLUTION_GOOD = os.path.join(WORKSPACE, "self-evolution", "做得好的")

# 模块注册表（与 SKILL.md 保持一致）
MODULE_REGISTRY = {
    "社群运营": {
        "经验库路径": os.path.join(WORKSPACE, "projects", "20260425-内容创作系统", "社群运营", "经验库"),
        "self-evolution映射": True,
    },
    "公众号": {
        "经验库路径": os.path.join(WORKSPACE, "公众号", "经验库"),
        "self-evolution映射": True,
    },
    "视频提示词": {
        "经验库路径": os.path.join(WORKSPACE, "视频提示词", "经验库"),
        "self-evolution映射": True,
    },
}


def scan_dir(dir_path):
    """扫描目录中的所有 .md 文件，返回文件名列表"""
    if not os.path.exists(dir_path):
        return []
    return [f for f in os.listdir(dir_path) if f.endswith(".md") and not f.startswith("INDEX")]


def extract_lesson_id(filepath):
    """从案例文件中提取教训编号（E{NNN}）"""
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
        match = re.search(r"E(\d+)", content)
        if match:
            return f"E{match.group(1)}"
    except Exception:
        pass
    return None


def extract_case_id(filepath):
    """从文件名中提取案例编号（CASE-{NNN}）"""
    match = re.search(r"CASE-(\d+)", os.path.basename(filepath))
    if match:
        return f"CASE-{match.group(1).zfill(3)}"
    return None


def check_module(module_name, module_config):
    """检查单个模块的双写同步状态"""
    results = {
        "模块": module_name,
        "做得差的": {"self-evolution": [], "经验库": [], "缺失": []},
        "做得好的": {"self-evolution": [], "经验库": [], "缺失": []},
        "同步率": 0,
    }

    经验库路径 = module_config["经验库路径"]

    # 扫描 self-evolution
    se_bad = scan_dir(SELF_EVOLUTION_BAD)
    se_good = scan_dir(SELF_EVOLUTION_GOOD)

    # 扫描经验库
    exp_bad_dir = os.path.join(经验库路径, "做得差的")
    exp_good_dir = os.path.join(经验库路径, "做得好的")
    exp_bad = scan_dir(exp_bad_dir)
    exp_good = scan_dir(exp_good_dir)

    # 检查做得差的
    results["做得差的"]["self-evolution"] = se_bad
    results["做得差的"]["经验库"] = exp_bad

    for f in se_bad:
        # 检查 self-evolution 中的教训是否在经验库中有对应案例
        lesson_id = extract_lesson_id(os.path.join(SELF_EVOLUTION_BAD, f))
        found = False
        for cf in exp_bad:
            cf_content = ""
            try:
                with open(os.path.join(exp_bad_dir, cf), encoding="utf-8") as fh:
                    cf_content = fh.read()
            except Exception:
                pass
            if lesson_id and lesson_id in cf_content:
                found = True
                break
        if not found and lesson_id:
            results["做得差的"]["缺失"].append({"教训": f, "编号": lesson_id})

    # 检查做得好的
    results["做得好的"]["self-evolution"] = se_good
    results["做得好的"]["经验库"] = exp_good

    for f in se_good:
        lesson_id = extract_lesson_id(os.path.join(SELF_EVOLUTION_GOOD, f))
        found = False
        for cf in exp_good:
            cf_content = ""
            try:
                with open(os.path.join(exp_good_dir, cf), encoding="utf-8") as fh:
                    cf_content = fh.read()
            except Exception:
                pass
            if lesson_id and lesson_id in cf_content:
                found = True
                break
        if not found and lesson_id:
            results["做得好的"]["缺失"].append({"教训": f, "编号": lesson_id})

    # 计算同步率
    total = len(se_bad) + len(se_good)
    missing = len(results["做得差的"]["缺失"]) + len(results["做得好的"]["缺失"])
    if total > 0:
        results["同步率"] = round((total - missing) / total * 100)
    else:
        results["同步率"] = 100  # 无教训 = 100% 同步

    return results


def fix_module(module_name, module_config, results):
    """自动修复缺失的副本"""
    经验库路径 = module_config["经验库路径"]
    fixed = 0

    for missing in results["做得差的"]["缺失"]:
        src = os.path.join(SELF_EVOLUTION_BAD, missing["教训"])
        if os.path.exists(src):
            dst_dir = os.path.join(经验库路径, "做得差的")
            os.makedirs(dst_dir, exist_ok=True)
            dst = os.path.join(dst_dir, missing["教训"])
            if not os.path.exists(dst):
                shutil.copy2(src, dst)
                fixed += 1
                print(f"  [FIX] 复制 {missing['教训']} -> {dst_dir}")

    for missing in results["做得好的"]["缺失"]:
        src = os.path.join(SELF_EVOLUTION_GOOD, missing["教训"])
        if os.path.exists(src):
            dst_dir = os.path.join(经验库路径, "做得好的")
            os.makedirs(dst_dir, exist_ok=True)
            dst = os.path.join(dst_dir, missing["教训"])
            if not os.path.exists(dst):
                shutil.copy2(src, dst)
                fixed += 1
                print(f"  [FIX] 复制 {missing['教训']} -> {dst_dir}")

    return fixed


def main():
    parser = argparse.ArgumentParser(description="双写验证脚本")
    parser.add_argument("--module", help="只检查指定模块")
    parser.add_argument("--fix", action="store_true", help="自动修复缺失的副本")
    args = parser.parse_args()

    print("=" * 50)
    print("双写验证脚本 v1.0")
    print(f"运行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    modules = MODULE_REGISTRY
    if args.module:
        if args.module not in modules:
            print(f"\n❌ 未知模块：{args.module}")
            print(f"   可用模块：{', '.join(modules.keys())}")
            sys.exit(1)
        modules = {args.module: modules[args.module]}

    all_results = []
    total_sync = 0

    for name, config in modules.items():
        print(f"\n--- 模块：{name} ---")

        if not os.path.exists(config["经验库路径"]):
            print(f"  ⚠️  经验库路径不存在：{config['经验库路径']}")
            print(f"  跳过此模块（需要先初始化经验库目录）")
            continue

        results = check_module(name, config)
        all_results.append(results)

        print(f"  self-evolution（差）：{len(results['做得差的']['self-evolution'])} 个教训")
        print(f"  经验库（差）：{len(results['做得差的']['经验库'])} 个案例")
        print(f"  self-evolution（好）：{len(results['做得好的']['self-evolution'])} 个经验")
        print(f"  经验库（好）：{len(results['做得好的']['经验库'])} 个案例")

        if results["做得差的"]["缺失"]:
            print(f"  🔴 缺失（差）：{len(results['做得差的']['缺失'])} 个")
            for m in results["做得差的"]["缺失"]:
                print(f"     - {m['教训']} ({m['编号']}) -> 经验库/做得差的/")

        if results["做得好的"]["缺失"]:
            print(f"  🔴 缺失（好）：{len(results['做得好的']['缺失'])} 个")
            for m in results["做得好的"]["缺失"]:
                print(f"     - {m['教训']} ({m['编号']}) -> 经验库/做得好的/")

        sync_rate = results["同步率"]
        total_sync += sync_rate
        status = "✅" if sync_rate == 100 else "⚠️"
        print(f"  {status} 同步率：{sync_rate}%")

        if args.fix and sync_rate < 100:
            fixed = fix_module(name, config, results)
            print(f"  🔧 已修复 {fixed} 个缺失文件")
            # 重新检查
            results_after = check_module(name, config)
            print(f"  🔄 修复后同步率：{results_after['同步率']}%")

    # 汇总
    print("\n" + "=" * 50)
    if all_results:
        avg_sync = total_sync / len(all_results)
        status = "✅" if avg_sync == 100 else "❌"
        print(f"{status} 平均同步率：{avg_sync:.0f}%")
    else:
        print("⚠️  没有可检查的模块（经验库目录不存在）")

    if not args.fix and any(r["同步率"] < 100 for r in all_results):
        print("\n💡 提示：运行 --fix 自动修复缺失的副本")

    print("=" * 50)


if __name__ == "__main__":
    main()
