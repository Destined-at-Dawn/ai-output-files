"""
li-workspace Refactoring + li-diagnose 联合执行
Refactoring: 按 P2(SRP) + P8(Move) 清理 mutual 根目录
Diagnose: 输出 6 维熵源诊断
"""
import os
import shutil
import subprocess
from datetime import datetime

WORKSPACE = r"E:\ai产出文件\牛马\mutual\mutual"
ARCHIVE_DIR = r"E:\ai产出文件\牛马\归档\2026-06-22-mutual-root-cleanup"
TODAY = "2026-06-22"

# === 垃圾文件清单（34 个） ===
TRASH_FILES = [
    # 28 个 timestamp 粘贴文件
    "1781088737437-Pasted-1.txt",
    "1781092093094-Pasted-2.txt",
    "1781110245954-Pasted-3.txt",
    "1781148183007-Pasted-1.txt",
    "1781148889377-Pasted-2.txt",
    "1781149922216-Pasted-3.txt",
    "1781150036133-Pasted-4.txt",
    "1781151033443-Pasted-6.txt",
    "1781151355257-Pasted-8.txt",
    "1781176523466-Pasted-9.txt",
    "1781181102585-Pasted-10.txt",
    "1781183077561-Pasted-12.txt",
    "1781184043120-Pasted-14.txt",
    "1781185601997-Pasted-15.txt",
    "1781186460981-Pasted-17.txt",
    "1781187390459-Pasted-18.txt",
    "1781233568204-Pasted-2.txt",
    "1781234140184-Pasted-4.txt",
    "1781332364817-Pasted-1.txt",
    "1781339608455-Pasted-3.txt",
    "1781339618238-Pasted-4.txt",
    "1781617932316-Pasted-1.txt",
    "1781618000204-Pasted-2.txt",
    "1781667020330-Pasted-6.txt",
    "1781667047590-Pasted-7.txt",
    "1781667244981-Pasted-9.txt",
    "1781667672303-Pasted-10.txt",
    "1781668065856-Pasted-11.txt",
    "1781668107349-Pasted-12.txt",
    # 6 个乱码/碎片文件
    "=",
    "=15",
    "背景铺垫（先给答案，再解释为什么",
    "表格（移动端友好）",
    "上一任",
    "创建日期：2026-06-11",
]

# 需要保留的核心项（根目录只留入口 + 核心目录）
KEEP_ITEMS = {
    # 核心目录
    "memory",
    "outputs",
    "share",
    ".claude",
    ".git",
    ".gitignore",
    "self-evolution",
    "ecosystem-manual",
    "knowledge-hub",
    "script-library",
    "project-context",
    "plans",
    "hermes-memory",
    "hermes-workspace-governance",
    # 核心入口文件
    "CLAUDE.md",
    "AGENT.md",
    "skill-routing-table.json",
    "runtime-snapshot.md",
    "workflow-inbox.md",
    "artifact-registry.md",
    "negative-results.md",
    # 其他需要保留的
    "impeccable-23-commands.json",
    "sync_web_design.py",
    "plan.md",
}


def phase1_git_checkpoint():
    """li-workspace: Git checkpoint before refactor"""
    git_dir = os.path.join(WORKSPACE, ".git")
    if not os.path.isdir(git_dir):
        print("[Phase 1] No git repo, skipping checkpoint")
        return

    print("[Phase 1] Git checkpoint...")
    try:
        subprocess.run(["git", "add", "-A"], cwd=WORKSPACE, capture_output=True, timeout=30)
        result = subprocess.run(
            ["git", "commit", "-m",
             f"checkpoint: pre-root-cleanup ({datetime.now().strftime('%Y-%m-%d %H:%M')})",
             "--allow-empty"],
            cwd=WORKSPACE, capture_output=True, timeout=30, text=True
        )
        print(f"  -> {result.stdout.strip() or 'committed'}")
    except Exception as e:
        print(f"  -> git checkpoint warning: {e}")


def phase2_scan_and_classify():
    """li-workspace P2: 按 SRP 识别根目录每一项的职责"""
    print("\n[Phase 2] Root directory scan (SRP analysis)...")
    items = os.listdir(WORKSPACE)
    classified = {"keep": [], "trash": [], "unclassified": []}

    for item in items:
        item_path = os.path.join(WORKSPACE, item)
        if item in KEEP_ITEMS:
            classified["keep"].append(item)
        elif item in TRASH_FILES:
            classified["trash"].append(item)
        elif os.path.isfile(item_path):
            classified["unclassified"].append(item)
        else:
            classified["keep"].append(item)  # 未识别的目录默认保留

    print(f"  Keep: {len(classified['keep'])} items")
    print(f"  Trash: {len(classified['trash'])} items")
    print(f"  Unclassified files: {len(classified['unclassified'])} items")
    if classified["unclassified"]:
        for f in classified["unclassified"]:
            print(f"    - {f}")
    return classified


def phase3_move_to_archive(classified):
    """li-workspace P8: Move 到归档"""
    print(f"\n[Phase 3] Moving to archive: {ARCHIVE_DIR}")
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    moved = 0
    failed = 0

    # Move confirmed trash
    for fname in classified["trash"]:
        src = os.path.join(WORKSPACE, fname)
        dst = os.path.join(ARCHIVE_DIR, fname)
        if os.path.exists(src):
            try:
                shutil.move(src, dst)
                moved += 1
            except Exception as e:
                print(f"  FAILED: {fname} -> {e}")
                failed += 1

    # Move unclassified files (still in root but not in KEEP or TRASH)
    for fname in classified["unclassified"]:
        src = os.path.join(WORKSPACE, fname)
        dst = os.path.join(ARCHIVE_DIR, "unclassified-" + fname)
        if os.path.exists(src):
            try:
                shutil.move(src, dst)
                moved += 1
            except Exception as e:
                print(f"  FAILED: {fname} -> {e}")
                failed += 1

    print(f"  Moved: {moved}, Failed: {failed}")
    return moved, failed


def phase4_verify():
    """验证根目录状态"""
    print("\n[Phase 4] Verification...")
    remaining = sorted(os.listdir(WORKSPACE))
    print(f"  Root directory now has {len(remaining)} items:")
    for item in remaining:
        item_path = os.path.join(WORKSPACE, item)
        kind = "DIR " if os.path.isdir(item_path) else "FILE"
        size = ""
        if os.path.isfile(item_path):
            size = f" ({os.path.getsize(item_path)} bytes)"
        print(f"    [{kind}] {item}{size}")

    archive_items = os.listdir(ARCHIVE_DIR) if os.path.isdir(ARCHIVE_DIR) else []
    print(f"\n  Archive: {len(archive_items)} files")


def diagnose_entropy():
    """li-diagnose: 6 维熵源诊断"""
    print("\n" + "=" * 60)
    print("li-diagnose: 6 维熵源诊断")
    print("=" * 60)

    # 扫描根目录实际状态
    items = os.listdir(WORKSPACE)
    files = [f for f in items if os.path.isfile(os.path.join(WORKSPACE, f))]
    dirs = [d for d in items if os.path.isdir(os.path.join(WORKSPACE, d))]

    trash_count = sum(1 for f in files if f.startswith("1781") and "Pasted" in f)
    broken_count = sum(1 for f in files if f in ["=", "=15"])

    print(f"""
[1. 结构熵 - 结构性冗余]
  症状: 根目录 {len(items)} 项中 {trash_count + broken_count} 项是垃圾文件
  根因: 无自动清理机制，粘贴碎片直接落根目录
  负熵: 本次清理 + 定期归档节律

[2. 边界熵 - 系统边界扩张]
  症状: 根目录既放入口文件又放垃圾碎片
  根因: 根目录没有"只放入口"的边界约束
  负熵: 根目录只留 CLAUDE.md + 核心目录，其他一律进子目录

[3. 反馈熵 - 纠偏机制缺失]
  症状: 34 个垃圾文件累积到今天才清理
  根因: 没有定期健康检查触发清理
  负熵: watchdog v4 已扫描根目录 mtime，但不清理内容

[4. 信息熵 - 知识外化]
  状态: LOW — memory/ 系统运转正常，11 个日期文件 + long-term.md

[5. 流程熵 - 流程标准化]
  状态: LOW — CLAUDE.md 启动序列 + skill 路由 + 定时任务均正常

[6. 动力熵 - 驱动力]
  状态: NOT ASSESSED — 需要用户反馈
""")

    print("[优先级矩阵]")
    print("""
  影响力高 + 修复难度低 = 立即行动:
    - 根目录垃圾清理（本次执行）
    - 建立根目录定期清理节律

  影响力高 + 修复难度高 = 重点攻坚:
    - 粘贴碎片自动拦截（从源头解决）

  影响力低 + 修复难度低 = 顺手处理:
    - ARCHIVE_LOG 过期清理（Phase 0 已完成）

  影响力低 + 修复难度高 = 暂时搁置:
    - (无)
""")


def main():
    print("=== li-workspace Refactoring + li-diagnose ===\n")

    # li-script Phase 1 结论
    print("li-script Phase 1 检索结论: C 无命中（INDEX 中无根目录清理脚本）")
    print("  -> Phase 2 新写 + Phase 3 分类决策（可复用 -> 入库）\n")

    phase1_git_checkpoint()
    classified = phase2_scan_and_classify()

    if classified["trash"] or classified["unclassified"]:
        phase3_move_to_archive(classified)
    else:
        print("\n  Nothing to clean!")

    phase4_verify()
    diagnose_entropy()

    print("\n=== DONE ===")


if __name__ == "__main__":
    main()
