"""
li-workspace Refactoring: 深度根目录重构
按 P2(SRP) 原则：根目录只留入口文件 + 核心职责目录
"""
import os
import shutil
import subprocess
from datetime import datetime

WORKSPACE = r"E:\ai产出文件\牛马\mutual\mutual"
ARCHIVE = r"E:\ai产出文件\牛马\归档\2026-06-22-mutual-deep-refactor"
TODAY = "2026-06-22"


def git_checkpoint():
    git_dir = os.path.join(WORKSPACE, ".git")
    if not os.path.isdir(git_dir):
        print("[GIT] No repo, skip")
        return
    try:
        subprocess.run(["git", "add", "-A"], cwd=WORKSPACE, capture_output=True, timeout=30)
        subprocess.run(["git", "commit", "-m",
                        f"checkpoint: pre-deep-refactor ({datetime.now().strftime('%Y-%m-%d %H:%M')})",
                        "--allow-empty"],
                       cwd=WORKSPACE, capture_output=True, timeout=30)
        print("[GIT] Checkpoint committed")
    except Exception as e:
        print(f"[GIT] Warning: {e}")


def safe_move(src, dst):
    """移动文件/目录，目标已存在则跳过"""
    if not os.path.exists(src):
        print(f"  SKIP (not found): {os.path.basename(src)}")
        return False
    if os.path.exists(dst):
        print(f"  SKIP (target exists): {os.path.basename(src)}")
        return False
    try:
        shutil.move(src, dst)
        print(f"  MOVED: {os.path.basename(src)}")
        return True
    except Exception as e:
        print(f"  FAILED: {os.path.basename(src)} -> {e}")
        return False


def merge_and_remove(src_dir, dst_dir):
    """合并源目录内容到目标目录，然后删除源目录"""
    if not os.path.exists(src_dir):
        return
    os.makedirs(dst_dir, exist_ok=True)
    moved = 0
    for item in os.listdir(src_dir):
        src = os.path.join(src_dir, item)
        dst = os.path.join(dst_dir, item)
        if os.path.exists(dst):
            print(f"  SKIP (exists in target): {item}")
            continue
        shutil.move(src, dst)
        moved += 1
        print(f"  MERGED: {item}")
    # 删除空源目录
    try:
        remaining = os.listdir(src_dir)
        if not remaining:
            os.rmdir(src_dir)
            print(f"  REMOVED EMPTY DIR: {os.path.basename(src_dir)}/")
        else:
            print(f"  KEEP (not empty): {os.path.basename(src_dir)}/ ({len(remaining)} remaining)")
    except:
        pass
    return moved


def main():
    print("=== li-workspace: Deep Root Refactor ===\n")
    print("原则: 根目录只留入口文件 + 核心职责目录\n")

    git_checkpoint()
    os.makedirs(ARCHIVE, exist_ok=True)

    moved_count = 0

    # ========== 1. .tmp/ 全部归档（都超过2周） ==========
    print("[1/7] .tmp/ -> archive (all >2 weeks old)")
    src = os.path.join(WORKSPACE, ".tmp")
    dst = os.path.join(ARCHIVE, ".tmp")
    if os.path.exists(src):
        if safe_move(src, dst):
            moved_count += 1

    # ========== 2. conversations/ -> memory/conversations/ ==========
    print("\n[2/7] conversations/ -> memory/conversations/")
    src = os.path.join(WORKSPACE, "conversations")
    dst = os.path.join(WORKSPACE, "memory", "conversations")
    if os.path.exists(src):
        count = merge_and_remove(src, dst)
        if count:
            moved_count += 1
            print(f"  Merged {count} conversation dirs")

    # ========== 3. drafts/ -> outputs/drafts/ ==========
    print("\n[3/7] drafts/ -> outputs/drafts/")
    src = os.path.join(WORKSPACE, "drafts")
    dst = os.path.join(WORKSPACE, "outputs", "drafts")
    if os.path.exists(src):
        count = merge_and_remove(src, dst)
        if count:
            moved_count += 1

    # ========== 4. handoffs/ -> 删除（空目录） ==========
    print("\n[4/7] handoffs/ -> delete (empty)")
    src = os.path.join(WORKSPACE, "handoffs")
    if os.path.exists(src):
        items = os.listdir(src)
        if not items:
            os.rmdir(src)
            print("  DELETED empty handoffs/")
            moved_count += 1
        else:
            safe_move(src, os.path.join(ARCHIVE, "handoffs"))

    # ========== 5. skill-calls/ -> memory/skill-calls/ ==========
    print("\n[5/7] skill-calls/ -> memory/skill-calls/")
    src = os.path.join(WORKSPACE, "skill-calls")
    dst = os.path.join(WORKSPACE, "memory", "skill-calls")
    if os.path.exists(src):
        count = merge_and_remove(src, dst)
        if count:
            moved_count += 1

    # ========== 6. scaffold-workspace/ -> skills/scaffold-workspace/ ==========
    print("\n[6/7] scaffold-workspace/ -> skills/scaffold-workspace/")
    src = os.path.join(WORKSPACE, "scaffold-workspace")
    dst = os.path.join(WORKSPACE, "skills", "scaffold-workspace")
    if os.path.exists(src):
        if safe_move(src, dst):
            moved_count += 1

    # ========== 7. 合并重复 + 归档旧版 ==========
    print("\n[7/7] Merge duplicates + archive legacy")

    # 7a. 自我进化/ -> self-evolution/ (合并后删除)
    print("\n  7a. 自我进化/ -> self-evolution/ (merge)")
    src = os.path.join(WORKSPACE, "自我进化")
    dst = os.path.join(WORKSPACE, "self-evolution")
    if os.path.exists(src):
        count = merge_and_remove(src, dst)
        if count:
            moved_count += 1

    # 7b. 归档/ -> E:\归档 (根目录不应该有归档目录)
    print("\n  7b. 归档/ -> archive (root should not have archive dir)")
    src = os.path.join(WORKSPACE, "归档")
    dst = os.path.join(ARCHIVE, "根目录归档文件夹")
    if os.path.exists(src):
        if safe_move(src, dst):
            moved_count += 1

    # 7c. 文书文档/ -> outputs/文书文档/ (内容产出归 outputs)
    print("\n  7c. 文书文档/ -> outputs/文书文档/")
    src = os.path.join(WORKSPACE, "文书文档")
    dst = os.path.join(WORKSPACE, "outputs", "文书文档")
    if os.path.exists(src):
        if safe_move(src, dst):
            moved_count += 1

    # 7d. _system/ -> 保留（系统目录）
    print("\n  7d. _system/ -> KEEP (system infra)")

    # 7e. cross-workspace-sync/ -> knowledge-hub 或保留
    print("\n  7e. cross-workspace-sync/ -> KEEP (shared rules infra)")

    # 7f. unified-index/ -> _system/unified-index/ (系统级索引)
    print("\n  7f. unified-index/ -> _system/unified-index/")
    src = os.path.join(WORKSPACE, "unified-index")
    dst = os.path.join(WORKSPACE, "_system", "unified-index")
    if os.path.exists(src):
        if safe_move(src, dst):
            moved_count += 1

    # 7g. knowledge-base/ -> knowledge-hub/knowledge-base/ (如果knowledge-hub存在)
    print("\n  7g. knowledge-base/ -> keep (knowledge infra)")
    # knowledge-base 有 layer0/1/2 结构，是独立知识系统，保留

    # ========== 验证 ==========
    print("\n" + "=" * 60)
    print("VERIFICATION: Root directory final state")
    print("=" * 60)

    items = sorted(os.listdir(WORKSPACE))
    dirs = []
    files = []
    for item in items:
        path = os.path.join(WORKSPACE, item)
        if os.path.isdir(path):
            dirs.append(item)
        else:
            files.append(item)

    print(f"\n总项数: {len(items)} (之前 31)")
    print(f"\n文件 ({len(files)}):")
    for f in files:
        print(f"  {f}")
    print(f"\n目录 ({len(dirs)}):")
    for d in dirs:
        print(f"  {d}/")

    # 归档统计
    archive_items = os.listdir(ARCHIVE) if os.path.isdir(ARCHIVE) else []
    print(f"\n归档: {len(archive_items)} items -> {ARCHIVE}")
    print(f"\n本次操作: {moved_count} structural changes")
    print("\n=== DONE ===")


if __name__ == "__main__":
    main()
