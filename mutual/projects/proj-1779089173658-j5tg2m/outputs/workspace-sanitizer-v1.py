"""workspace-sanitizer v1.0 — 四个工作区深度清理"""
import os
import shutil
import sys
from datetime import datetime

TODAY = "2026-06-22"
ARCHIVE_BASE = r"E:\ai产出文件\牛马\归档"

# 工作区路径
WORKSPACES = {
    "创作": r"E:\ai产出文件\牛马\创作\创作",
    "求职": r"E:\ai产出文件\牛马\求职\求职",
    "竞赛": r"E:\ai产出文件\牛马\竞赛\竞赛",
    "个人": r"E:\ai产出文件\牛马\个人\个人",
}

results = {}

def safe_mkdir(path):
    os.makedirs(path, exist_ok=True)

def safe_move(src, dst):
    """移动文件/目录，如果目标已存在则合并"""
    if not os.path.exists(src):
        return False
    if os.path.exists(dst):
        # 目标已存在——如果是目录则合并
        if os.path.isdir(src) and os.path.isdir(dst):
            for item in os.listdir(src):
                safe_move(os.path.join(src, item), os.path.join(dst, item))
            # 源目录应该空了
            try:
                os.rmdir(src)
            except:
                pass
            return True
        else:
            # 文件冲突——改名
            base, ext = os.path.splitext(dst)
            dst = f"{base}_冲突_{datetime.now().strftime('%H%M%S')}{ext}"
    shutil.move(src, dst)
    return True

def count_dir(path):
    """计算目录中的文件数和总大小"""
    count = 0
    size = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            try:
                size += os.path.getsize(os.path.join(root, f))
                count += 1
            except:
                pass
    return count, size

def clean_workspace(name, ws_path):
    print(f"\n{'='*60}")
    print(f"  清理工作区: {name}")
    print(f"  路径: {ws_path}")
    print(f"{'='*60}")

    stats = {
        "deleted": [],
        "archived": [],
        "moved": [],
        "merged": [],
        "errors": [],
    }

    before_count = len(os.listdir(ws_path))
    print(f"  清理前: {before_count} 项")

    # ===== Phase 1: 卫生清理 =====
    print(f"\n  [Phase 1] 卫生清理")

    # 1.1 删除 __pycache__
    for pycache in [os.path.join(ws_path, "__pycache__")]:
        if os.path.exists(pycache):
            shutil.rmtree(pycache)
            stats["deleted"].append("__pycache__/")
            print(f"    删除 __pycache__/")

    # 1.2 删除空目录（排除核心目录）
    CORE_DIRS = {'.claude', '.Codex', '_system', 'memory', 'outputs', 'projects',
                 'skills', 'scripts', 'SOPs', '.git', '.github', '.learnings', '.shared'}
    for item in sorted(os.listdir(ws_path)):
        full = os.path.join(ws_path, item)
        if not os.path.isdir(full):
            continue
        if item in CORE_DIRS:
            continue
        count, _ = count_dir(full)
        if count == 0:
            shutil.rmtree(full)
            stats["deleted"].append(f"{item}/ (空目录)")
            print(f"    删除空目录: {item}/")

    # 1.3 删除 0 字节非必要文件
    KEEP_FILES = {'.gitkeep', '.gitignore', '__init__.py', '.NO-RULES-DIR-HERE.md'}
    for item in os.listdir(ws_path):
        full = os.path.join(ws_path, item)
        if os.path.isfile(full) and os.path.getsize(full) == 0 and item not in KEEP_FILES:
            os.remove(full)
            stats["deleted"].append(f"{item} (0字节)")
            print(f"    删除 0字节文件: {item}")

    # ===== Phase 2: 结构重组 =====
    print(f"\n  [Phase 2] 结构重组")

    # 2.1 归档目录 -> 全局归档
    archive_dir = os.path.join(ws_path, "归档")
    if os.path.exists(archive_dir):
        count, size = count_dir(archive_dir)
        if count > 0:
            global_archive = os.path.join(ARCHIVE_BASE, f"{TODAY}-{name}-归档迁移")
            safe_mkdir(global_archive)
            for item in os.listdir(archive_dir):
                safe_move(os.path.join(archive_dir, item), os.path.join(global_archive, item))
            try:
                os.rmdir(archive_dir)
            except:
                pass
            stats["archived"].append(f"归档/ -> {global_archive} ({count}文件)")
            print(f"    归档/ -> 全局归档 ({count}文件)")

    # _归档 同理
    _archive_dir = os.path.join(ws_path, "_归档")
    if os.path.exists(_archive_dir):
        count, size = count_dir(_archive_dir)
        if count > 0:
            global_archive = os.path.join(ARCHIVE_BASE, f"{TODAY}-{name}-_归档迁移")
            safe_mkdir(global_archive)
            for item in os.listdir(_archive_dir):
                safe_move(os.path.join(_archive_dir, item), os.path.join(global_archive, item))
            try:
                os.rmdir(_archive_dir)
            except:
                pass
            stats["archived"].append(f"_归档/ -> 全局归档 ({count}文件)")
            print(f"    _归档/ -> 全局归档 ({count}文件)")

    # 2.2 自我进化/ -> 合并到 self-evolution/
    old_evo = os.path.join(ws_path, "自我进化")
    new_evo = os.path.join(ws_path, "self-evolution")
    if os.path.exists(old_evo):
        count, _ = count_dir(old_evo)
        if count > 0:
            safe_mkdir(new_evo)
            for item in os.listdir(old_evo):
                safe_move(os.path.join(old_evo, item), os.path.join(new_evo, item))
            try:
                os.rmdir(old_evo)
            except:
                pass
            stats["merged"].append(f"自我进化/ ({count}文件) -> self-evolution/")
            print(f"    自我进化/ ({count}文件) -> self-evolution/")

    # 2.3 conversations/ -> memory/conversations/
    conv_dir = os.path.join(ws_path, "conversations")
    mem_conv = os.path.join(ws_path, "memory", "conversations")
    if os.path.exists(conv_dir):
        count, _ = count_dir(conv_dir)
        if count > 0:
            safe_mkdir(mem_conv)
            for item in os.listdir(conv_dir):
                safe_move(os.path.join(conv_dir, item), os.path.join(mem_conv, item))
            try:
                os.rmdir(conv_dir)
            except:
                pass
            stats["moved"].append(f"conversations/ ({count}文件) -> memory/conversations/")
            print(f"    conversations/ ({count}文件) -> memory/conversations/")

    # 2.4 skill-calls/ -> memory/skill-calls/
    sc_dir = os.path.join(ws_path, "skill-calls")
    mem_sc = os.path.join(ws_path, "memory", "skill-calls")
    if os.path.exists(sc_dir):
        count, _ = count_dir(sc_dir)
        if count > 0:
            safe_mkdir(mem_sc)
            for item in os.listdir(sc_dir):
                safe_move(os.path.join(sc_dir, item), os.path.join(mem_sc, item))
            try:
                os.rmdir(sc_dir)
            except:
                pass
            stats["moved"].append(f"skill-calls/ ({count}文件) -> memory/skill-calls/")
            print(f"    skill-calls/ ({count}文件) -> memory/skill-calls/")

    # 2.5 drafts/ -> outputs/drafts/
    drafts_dir = os.path.join(ws_path, "drafts")
    out_drafts = os.path.join(ws_path, "outputs", "drafts")
    if os.path.exists(drafts_dir):
        count, _ = count_dir(drafts_dir)
        if count > 0:
            safe_mkdir(out_drafts)
            for item in os.listdir(drafts_dir):
                safe_move(os.path.join(drafts_dir, item), os.path.join(out_drafts, item))
            try:
                os.rmdir(drafts_dir)
            except:
                pass
            stats["moved"].append(f"drafts/ ({count}文件) -> outputs/drafts/")
            print(f"    drafts/ ({count}文件) -> outputs/drafts/")

    # 2.6 handoffs/ -> 删除（如果还存在）
    handoffs = os.path.join(ws_path, "handoffs")
    if os.path.exists(handoffs):
        count, _ = count_dir(handoffs)
        if count == 0:
            os.rmdir(handoffs)
            stats["deleted"].append("handoffs/ (空)")
            print(f"    删除 handoffs/ (空)")

    after_count = len(os.listdir(ws_path))
    print(f"\n  清理后: {after_count} 项 (减少 {before_count - after_count})")
    results[name] = stats
    return stats


# ===== 主程序 =====
if __name__ == "__main__":
    print("workspace-sanitizer v1.0")
    print(f"日期: {TODAY}")
    print(f"工作区数: {len(WORKSPACES)}")

    for name, path in WORKSPACES.items():
        if not os.path.exists(path):
            print(f"\n{name}: 路径不存在，跳过")
            continue
        clean_workspace(name, path)

    # ===== 总结 =====
    print(f"\n{'='*60}")
    print("  清理总结")
    print(f"{'='*60}")
    for name, stats in results.items():
        ws = WORKSPACES[name]
        count = len(os.listdir(ws))
        print(f"\n  {name}: {count} 项")
        print(f"    删除: {len(stats['deleted'])} 项")
        print(f"    归档: {len(stats['archived'])} 项")
        print(f"    移动: {len(stats['moved'])} 项")
        print(f"    合并: {len(stats['merged'])} 项")
