"""
mutual 工作区根目录垃圾清理脚本
- 34 个垃圾文件移入归档
- 根目录只保留核心目录和文件
"""
import os
import shutil
import subprocess
from datetime import datetime

WORKSPACE = r"E:\ai产出文件\牛马\mutual\mutual"
ARCHIVE_DIR = r"E:\ai产出文件\牛马\归档\2026-06-22-mutual-root-cleanup"

# 垃圾文件清单（34 个）
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

# 需要保留的核心项
KEEP_ITEMS = {
    "memory",
    "outputs",
    "share",
    ".claude",
    ".git",
    ".gitignore",
    "CLAUDE.md",
    "AGENT.md",
    "skill-routing-table.json",
    "runtime-snapshot.md",
    "self-evolution",
    "ecosystem-manual",
    "knowledge-hub",
    "script-library",
    "project-context",
    "workflow-inbox.md",
    "artifact-registry.md",
    "negative-results.md",
    "hermes-workspace-governance",
    "hermes-memory",
    "plans",
}

# 以下是模糊匹配的保留项（包含这些关键词的文件保留）
KEEP_PATTERNS = [
    "impeccable",  # impeccable-23-commands.json
    "sync_web",    # sync_web_design.py
    "plan.md",     # plan.md (如果有)
]


def main():
    print("=== mutual 根目录垃圾清理 ===\n")

    # Step 1: Git checkpoint
    git_dir = os.path.join(WORKSPACE, ".git")
    if os.path.isdir(git_dir):
        print("[1/4] Git checkpoint...")
        try:
            subprocess.run(
                ["git", "add", "-A"],
                cwd=WORKSPACE, capture_output=True, timeout=30
            )
            subprocess.run(
                ["git", "commit", "-m",
                 f"checkpoint: pre-cleanup root directory ({datetime.now().strftime('%Y-%m-%d %H:%M')})",
                 "--allow-empty"],
                cwd=WORKSPACE, capture_output=True, timeout=30
            )
            print("  -> checkpoint committed")
        except Exception as e:
            print(f"  -> git checkpoint failed: {e}, continuing anyway")
    else:
        print("[1/4] No git repo, skipping checkpoint")

    # Step 2: Create archive dir
    print("[2/4] Creating archive dir...")
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    print(f"  -> {ARCHIVE_DIR}")

    # Step 3: Move trash files
    print("[3/4] Moving trash files...")
    moved = 0
    skipped = 0
    not_found = 0

    for fname in TRASH_FILES:
        src = os.path.join(WORKSPACE, fname)
        dst = os.path.join(ARCHIVE_DIR, fname)
        if os.path.exists(src):
            try:
                shutil.move(src, dst)
                print(f"  -> MOVED: {fname}")
                moved += 1
            except Exception as e:
                print(f"  -> FAILED: {fname} ({e})")
                skipped += 1
        else:
            print(f"  -> NOT FOUND: {fname}")
            not_found += 1

    # Also check for pattern-matched items that should stay
    # but move anything that's NOT in KEEP_ITEMS and NOT matching KEEP_PATTERNS
    remaining_trash = []
    for item in os.listdir(WORKSPACE):
        if item in KEEP_ITEMS:
            continue
        item_path = os.path.join(WORKSPACE, item)
        # Check if it matches any keep pattern
        kept = False
        for pattern in KEEP_PATTERNS:
            if pattern in item.lower() or pattern in item:
                kept = True
                break
        if not kept and os.path.isfile(item_path):
            remaining_trash.append(item)

    if remaining_trash:
        print(f"\n  Found {len(remaining_trash)} additional unclassified files:")
        for f in remaining_trash:
            dst = os.path.join(ARCHIVE_DIR, f)
            try:
                shutil.move(os.path.join(WORKSPACE, f), dst)
                print(f"  -> MOVED (unclassified): {f}")
                moved += 1
            except Exception as e:
                print(f"  -> SKIPPED: {f} ({e})")
                skipped += 1

    # Step 4: Verify
    print(f"\n[4/4] Verification...")
    print(f"  Moved: {moved}")
    print(f"  Skipped: {skipped}")
    print(f"  Not found: {not_found}")
    print(f"\n  Root directory now contains:")
    for item in sorted(os.listdir(WORKSPACE)):
        item_path = os.path.join(WORKSPACE, item)
        kind = "DIR " if os.path.isdir(item_path) else "FILE"
        print(f"    [{kind}] {item}")

    print(f"\n  Archive contains {len(os.listdir(ARCHIVE_DIR))} files")
    print("\n=== DONE ===")


if __name__ == "__main__":
    main()
