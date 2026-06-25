# -*- coding: utf-8 -*-
"""扫描牛马目录下网站设计相关文件夹 + 读取两个参考样例结构。只读，不动文件。"""
import os

ROOT = r"E:\ai产出文件\牛马"
OUT = r"E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs\scan_result.txt"
L = []
def w(s=""): L.append(s)

KEYWORDS = ["网站", "网页", "web", "website", "html", "css", "前端",
            "frontend", "landing", "页面", "站点", "ui设计", "homepage", "官网", "site"]

def is_web_related(name):
    low = name.lower()
    return any(k.lower() in low for k in KEYWORDS)

w("=" * 70)
w("【1】牛马顶层目录")
w("=" * 70)
for d in sorted(os.listdir(ROOT)):
    if os.path.isdir(os.path.join(ROOT, d)):
        w(f"  [DIR] {d}")

w("")
w("=" * 70)
w("【2】递归查找网站设计相关文件夹（深度<=5，跳过第三方/归档）")
w("=" * 70)
SKIP = {"node_modules", ".git", "归档", "__pycache__", ".obsidian", "github",
        "tools", ".shared", "mempalace-palace", "runs", "logs", "script-library"}
hits = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    depth = dirpath[len(ROOT):].count(os.sep)
    if depth > 6:
        dirnames[:] = []
        continue
    dirnames[:] = [d for d in dirnames if d not in SKIP]
    for d in list(dirnames):
        if is_web_related(d):
            full = os.path.join(dirpath, d)
            try:
                nfiles = sum(len(f) for _, _, f in os.walk(full))
                size = 0
                for r, _, fs in os.walk(full):
                    for f in fs:
                        try: size += os.path.getsize(os.path.join(r, f))
                        except: pass
            except Exception:
                nfiles, size = -1, -1
            hits.append((full, nfiles, size))

for full, nfiles, size in hits:
    rel = full[len(ROOT)+1:]
    w(f"  {rel}")
    w(f"      文件数~{nfiles}  大小~{size/1024/1024:.1f}MB")
w(f"\n  共 {len(hits)} 个候选")

def dump(title, path, maxdepth=2):
    w("")
    w("=" * 70)
    w(title)
    w("=" * 70)
    if not os.path.exists(path):
        w("  (不存在) " + path)
        return
    for dp, dn, fn in os.walk(path):
        depth = dp[len(path):].count(os.sep)
        if depth > maxdepth:
            dn[:] = []
            continue
        indent = "  " * (depth + 1)
        w(f"{indent}[{os.path.basename(dp)}]/")
        for f in sorted(fn)[:40]:
            w(f"{indent}  - {f}")

dump("【3】参考样例1：图片提示词",
     r"E:\ai产出文件\牛马\创作\创作\projects\20260425-内容创作系统\图片提示词")
dump("【4】参考样例2：简历修改",
     r"E:\ai产出文件\牛马\求职\求职\projects\proj-1777554288697-9e2i8z\简历修改")

# 额外：小猫睡眠网站项目（深度命中的重点候选）展开
dump("【5】重点候选展开：小猫睡眠网站",
     r"E:\ai产出文件\牛马\创作\创作\projects\20260609-小猫睡眠网站", maxdepth=2)

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L))
print("DONE ->", OUT)
