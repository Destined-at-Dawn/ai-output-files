# -*- coding: utf-8 -*-
"""展开重点候选文件夹的文件清单，判断是否真的是网站设计。只读。"""
import os
OUT = r"E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs\scan2_result.txt"
L = []
def w(s=""): L.append(s)

targets = [
    r"E:\ai产出文件\牛马\html",
    r"E:\ai产出文件\牛马\创作\创作\projects\20260609-小黎个人网站",
    r"E:\ai产出文件\牛马\创作\创作\projects\20260521-AI创作与视觉设计\outputs\web-design-kit",
    r"E:\ai产出文件\牛马\创作\创作\projects\20260521-AI创作与视觉设计\outputs\website_materials",
    r"E:\ai产出文件\牛马\创作\创作\projects\20260425-内容创作系统\讲座HTML",
    r"E:\ai产出文件\牛马\创作\创作\projects\20260425-内容创作系统\社群运营\html",
    r"E:\ai产出文件\牛马\创作\创作\社群运营\html",
    r"E:\ai产出文件\牛马\创作\创作\讲座\html_output",
]

for t in targets:
    w("=" * 70)
    w(t.replace(r"E:\ai产出文件\牛马" + "\\", ""))
    w("=" * 70)
    if not os.path.exists(t):
        w("  (不存在)")
        w("")
        continue
    for dp, dn, fn in os.walk(t):
        depth = dp[len(t):].count(os.sep)
        if depth > 2:
            dn[:] = []
            continue
        ind = "  " * (depth + 1)
        w(f"{ind}[{os.path.basename(dp)}]/")
        for f in sorted(fn)[:40]:
            try: sz = os.path.getsize(os.path.join(dp, f))
            except: sz = 0
            w(f"{ind}  - {f}  ({sz//1024}KB)")
    w("")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L))
print("DONE")
