"""迁移 .mempalace 从 C 盘到 D 盘 + 创建 junction point"""
import os
import shutil
import subprocess
import sys

SRC = os.path.expanduser(r"~\.mempalace")  # C:\Users\13975\.mempalace
DST = r"D:\mempalace"

def main():
    # 1. 预检
    print(f"[1/5] 预检...")
    if not os.path.isdir(SRC):
        print(f"  ERROR: 源目录不存在: {SRC}")
        sys.exit(1)
    if os.path.exists(DST):
        print(f"  ERROR: 目标已存在: {DST}")
        sys.exit(1)

    # D盘空间
    _, _, free_bytes = shutil.disk_usage("D:/")
    free_gb = free_bytes / 1024 / 1024 / 1024
    total = sum(os.path.getsize(os.path.join(r, f)) for r, _, files in os.walk(SRC) for f in files)
    total_gb = total / 1024 / 1024 / 1024
    print(f"  D盘剩余: {free_gb:.1f} GB, 需迁移: {total_gb:.2f} GB")
    if free_gb < total_gb + 1:
        print("  ERROR: D盘空间不足")
        sys.exit(1)
    print("  OK")

    # 2. 移动目录
    print(f"[2/5] 移动 {SRC} -> {DST} ...")
    shutil.move(SRC, DST)
    if not os.path.isdir(DST):
        print("  ERROR: 移动失败")
        sys.exit(1)
    print(f"  OK ({total_gb:.2f} GB)")

    # 3. 创建 junction point
    print(f"[3/5] 创建 junction: {SRC} -> {DST} ...")
    result = subprocess.run(
        ["cmd", "/c", "mklink", "/J", SRC, DST],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ERROR: junction 创建失败: {result.stderr}")
        # 回滚
        shutil.move(DST, SRC)
        print("  已回滚")
        sys.exit(1)
    print(f"  OK")

    # 4. 验证 junction
    print(f"[4/5] 验证 junction...")
    if not os.path.isdir(SRC):
        print("  ERROR: junction 不可访问")
        sys.exit(1)
    # 验证 chroma.sqlite3 可通过原路径访问
    sqlite_path = os.path.join(SRC, "palace", "chroma.sqlite3")
    if os.path.isfile(sqlite_path):
        sz = os.path.getsize(sqlite_path) / 1024 / 1024 / 1024
        print(f"  chroma.sqlite3 可访问: {sz:.2f} GB")
    else:
        print(f"  WARNING: chroma.sqlite3 未找到于 {sqlite_path}")
    print("  OK")

    # 5. 验证 config.json 中的 palace_path 仍指向正确位置
    print(f"[5/5] 检查 config.json...")
    import json
    cfg_path = os.path.join(SRC, "config.json")
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    old_palace = cfg.get("palace_path", "")
    print(f"  palace_path: {old_palace}")
    # palace_path 使用 ~ 展开，junction 保证路径仍然有效
    print("  OK (junction 透明代理，无需修改配置)")

    print("\n=== 迁移完成 ===")
    print(f"  原路径 (junction): {SRC}")
    print(f"  实际位置: {DST}")
    print(f"  释放 C 盘: ~{total_gb:.2f} GB")
    print(f"  MCP 配置无需修改")

if __name__ == "__main__":
    main()
