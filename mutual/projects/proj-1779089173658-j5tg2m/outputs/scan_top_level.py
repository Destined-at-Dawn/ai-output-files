"""扫描 E:\ai产出文件\ 顶层目录结构"""
import os
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

root = r"E:\ai产出文件"

def get_dir_size(path):
    """递归计算目录大小"""
    total = 0
    count = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                total += entry.stat().st_size
                count += 1
            elif entry.is_dir(follow_symlinks=False):
                s, c = get_dir_size(entry.path)
                total += s
                count += c
    except PermissionError:
        pass
    return total, count

results = []
for entry in os.scandir(root):
    if entry.is_dir():
        size, fcount = get_dir_size(entry.path)
        results.append({
            "name": entry.name,
            "type": "dir",
            "size_mb": round(size / 1024 / 1024, 2),
            "file_count": fcount,
            "path": entry.path
        })
    elif entry.is_file():
        size = entry.stat().st_size
        results.append({
            "name": entry.name,
            "type": "file",
            "size_mb": round(size / 1024 / 1024, 2),
            "file_count": 1,
            "path": entry.path
        })

# 按大小倒序
results.sort(key=lambda x: x["size_mb"], reverse=True)

print(f"=== E:\\ai产出文件\\ 顶层扫描结果 ===")
print(f"共 {len(results)} 个条目\n")

total_size = 0
for r in results:
    total_size += r["size_mb"]
    icon = "📁" if r["type"] == "dir" else "📄"
    print(f"{icon} {r['name']:40s} {r['size_mb']:>10.2f} MB  ({r['file_count']} files)")

print(f"\n总计: {total_size:.2f} MB ({total_size/1024:.2f} GB)")
