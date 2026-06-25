# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json

ROOT = Path(r"E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理")
ASSETS = ROOT / "outputs" / "ch06_static_review_assets"
OUT = ROOT / "outputs" / "ch06_static_review_v2" / "preview_pages"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1800, 2546
M = 76
FONT_DIR = Path(r"C:\Windows\Fonts")
FONT = FONT_DIR / "msyh.ttc"
BOLD = FONT_DIR / "msyhbd.ttc"
MATH = FONT_DIR / "DejaVuSans.ttf"
if not FONT.exists():
    FONT = FONT_DIR / "simhei.ttf"
if not BOLD.exists():
    BOLD = FONT
if not MATH.exists():
    MATH = FONT

COL = {
    "bg": (245, 248, 251),
    "ink": (23, 33, 43),
    "muted": (89, 106, 121),
    "blue": (28, 87, 132),
    "teal": (0, 126, 137),
    "red": (200, 71, 68),
    "green": (44, 136, 93),
    "purple": (107, 87, 166),
    "yellow": (245, 181, 62),
    "line": (203, 217, 228),
    "card": (255, 255, 255),
    "soft": (236, 244, 250),
    "warn": (255, 247, 224),
}


def f(size, bold=False, math=False):
    return ImageFont.truetype(str(MATH if math else (BOLD if bold else FONT)), size)


def wh(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def wrap(draw, text, font, width):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur)
            cur = ""
            continue
        test = cur + ch
        if not cur or wh(draw, test, font)[0] <= width:
            cur = test
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


def text(draw, x, y, content, font, fill=COL["ink"], width=None, gap=7):
    lines = wrap(draw, content, font, width) if width else content.split("\n")
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += wh(draw, line or " ", font)[1] + gap
    return y


def card(img, box, fill=COL["card"], outline=COL["line"], r=12):
    x1, y1, x2, y2 = box
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((x1 + 6, y1 + 8, x2 + 6, y2 + 8), radius=r, fill=(36, 64, 84, 28))
    sh = sh.filter(ImageFilter.GaussianBlur(8))
    img.alpha_composite(sh)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=2)


def header(img, title, subtitle):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 178), fill=COL["blue"])
    d.rectangle((0, 158, W, 178), fill=COL["yellow"])
    d.text((M, 38), title, font=f(54, True), fill="white")
    d.text((M, 112), subtitle, font=f(25), fill=(225, 240, 250))
    d.rounded_rectangle((W - M - 220, 45, W - M, 103), radius=8, outline=(240, 248, 255), width=2)
    d.text((W - M - 190, 58), "第06章 静电场", font=f(24, True), fill="white")


def footer(img, source):
    d = ImageDraw.Draw(img)
    d.line((M, H - 66, W - M, H - 66), fill=COL["line"], width=2)
    d.text((M, H - 48), source, font=f(18), fill=COL["muted"])
    d.text((W - M - 150, H - 48), "v2 sample", font=f(18), fill=COL["muted"])


def paste_img(img, path, box):
    x1, y1, x2, y2 = box
    src = Image.open(path).convert("RGB")
    src.thumbnail((x2 - x1, y2 - y1), Image.Resampling.LANCZOS)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, radius=10, fill=(255, 255, 255), outline=COL["line"], width=2)
    img.paste(src, (x1 + (x2 - x1 - src.width) // 2, y1 + (y2 - y1 - src.height) // 2))


def mini_title(draw, x, y, label, color):
    draw.rounded_rectangle((x, y, x + 46, y + 46), radius=23, fill=color)
    draw.text((x + 13, y + 7), label, font=f(24, True), fill="white")


def page1():
    img = Image.new("RGBA", (W, H), COL["bg"] + (255,))
    d = ImageDraw.Draw(img)
    header(img, "静电场：1小时吃透路线图", "从电荷到 E，再到高斯定理、电势 U、导体静电平衡")

    card(img, (M, 230, W - M, 560))
    d.text((M + 28, 256), "本章核心问题", font=f(32, True), fill=COL["blue"])
    text(d, M + 28, 312, "给定电荷分布，如何求空间中的电场强度 E？如果题目换成电势 U、做功或导体球壳，又该如何换工具？", f(31), width=W - 2 * M - 56, gap=10)
    text(d, M + 28, 428, "考试路线：先判断题型，不先套公式。E 看方向和对称性；U 看零势点和路径无关；导体题先画电荷分布。", f(27, True), fill=COL["teal"], width=W - 2 * M - 56)

    # four-stage timeline
    y = 635
    stages = [
        ("1", "场强 E", "点电荷 E=kQ/r²；点电荷系矢量叠加；连续体切元 dq 积分。", "易混：E=F/q0 是定义式，不说明 E 由试探电荷决定。", COL["teal"]),
        ("2", "高斯定理", "∮E·dS=Q_in/ε0。只有球/柱/面对称时，E 才能从积分中提出。", "易混：通量由 Q_in 决定，面上 E 由所有电荷共同决定。", COL["red"]),
        ("3", "电势 U", "U 是标量，优先代数叠加；电势差和静电力做功绑定。", "易混：电势正负取决于零势点，不取决于试探电荷。", COL["purple"]),
        ("4", "导体静电平衡", "导体内部总场 E=0，导体等势；球壳题先画内外表面电荷。", "易混：总场为零，不等于外电荷不产生分场。", COL["green"]),
    ]
    for idx, title, body, trap, color in stages:
        card(img, (M, y, W - M, y + 205))
        mini_title(d, M + 30, y + 32, idx, color)
        d.text((M + 96, y + 26), title, font=f(32, True), fill=color)
        text(d, M + 96, y + 78, body, f(25), width=900)
        d.rounded_rectangle((W - M - 565, y + 38, W - M - 28, y + 158), radius=8, fill=COL["warn"], outline=(238, 203, 119), width=1)
        d.text((W - M - 540, y + 56), "辨析自测入口", font=f(22, True), fill=(126, 82, 20))
        text(d, W - M - 540, y + 92, trap, f(21), fill=(92, 67, 27), width=490, gap=4)
        y += 230

    card(img, (M, 1580, W - M, 1998))
    d.rectangle((M, 1580, W - M, 1642), fill=COL["blue"])
    d.text((M + 26, 1596), "1小时安排：不是读完本章，是练会考试动作", font=f(30, True), fill="white")
    plan = [
        ("10分钟", "看主线图，先分清 E、通量、U、导体四套工具。"),
        ("20分钟", "攻克 P0：高斯定理三模型 + 连续带电体切元积分。"),
        ("15分钟", "攻克 P1：电势/做功/零势点 + 导体静电平衡。"),
        ("15分钟", "小题速通 + 大题模板：每题先说识别信号，再写步骤。"),
    ]
    x = M + 34
    for i, (t, desc) in enumerate(plan):
        bx = x + i * 410
        d.rounded_rectangle((bx, 1688, bx + 365, 1928), radius=10, fill=(247, 250, 252), outline=COL["line"], width=2)
        d.text((bx + 22, 1710), t, font=f(28, True), fill=[COL["teal"], COL["red"], COL["purple"], COL["green"]][i])
        text(d, bx + 22, 1762, desc, f(22), width=320)

    paste_img(img, ASSETS / "total_review_p48.png", (M, 2050, W - M, 2385))
    footer(img, "Source: 大物B1总复习.pdf p48; Ch06-静电场-高频考点.md; ch06_static_review_v2/00_制作规格与页序.md")
    return img


def page2():
    img = Image.new("RGBA", (W, H), COL["bg"] + (255,))
    d = ImageDraw.Draw(img)
    header(img, "高斯定理：概念辨析 + 题型模板", "通量、场强、对称性必须分开想")

    card(img, (M, 230, W - M, 610))
    d.text((M + 30, 260), "教材定义与考试口令", font=f(34, True), fill=COL["blue"])
    d.text((M + 450, 252), "∮_S E · dS = Q_in / ε0", font=f(50, True, True), fill=COL["red"])
    text(d, M + 30, 345, "定义：闭合曲面的电通量等于曲面内电荷代数和除以真空介电常量。考试时先问：这个电荷分布有没有球/柱/面对称？如果没有，不能硬套高斯面。", f(27), width=W - 2 * M - 60)
    text(d, M + 30, 465, "一句话辨析：通量只看 Q_in；面上某一点的 E 要看空间所有电荷；E 能不能提出积分号取决于对称性。", f(27, True), fill=COL["teal"], width=W - 2 * M - 60)

    paste_img(img, ASSETS / "total_review_p52.png", (M, 660, W - M, 1115))
    paste_img(img, ASSETS / "total_review_p53.png", (M, 1155, W - M, 1610))

    card(img, (M, 1665, W - M, 2040))
    d.rectangle((M, 1665, W - M, 1728), fill=COL["blue"])
    d.text((M + 28, 1682), "三类题型模板：看到什么 -> 先做什么", font=f(30, True), fill="white")
    templates = [
        ("柱对称", "无限长线电荷、长圆柱", "取同轴圆柱面；侧面有通量，上下底无通量。"),
        ("面对称", "无限大平面、平板", "取穿过平面的短圆柱；两端面通量相加。"),
        ("球对称", "均匀球体、球面、球壳", "取同心球面；内部外部通常分段。"),
    ]
    for i, (name, signal, action) in enumerate(templates):
        x = M + 34 + i * 545
        d.rounded_rectangle((x, 1770, x + 500, 1988), radius=10, fill=(247, 250, 252), outline=COL["line"], width=2)
        d.text((x + 22, 1792), name, font=f(27, True), fill=[COL["teal"], COL["red"], COL["purple"]][i])
        text(d, x + 22, 1840, "识别：" + signal, f(22), width=450)
        text(d, x + 22, 1900, "动作：" + action, f(22), fill=COL["muted"], width=450)

    card(img, (M, 2095, W - M, 2385), fill=(255, 255, 255))
    d.rectangle((M, 2095, W - M, 2158), fill=COL["red"])
    d.text((M + 28, 2112), "自测题：答案放附页，不在本页暴露", font=f(30, True), fill="white")
    qs = [
        "1. 判断：闭合面内净电荷为 0 时，闭合面上各点场强一定为 0。",
        "2. 选择：闭合面外移动一个点电荷，闭合面的总通量和面上场强分别如何变化？",
        "3. 判断：只要题目出现闭合面，就一定可以用高斯定理直接求 E。",
    ]
    y = 2195
    for q in qs:
        y = text(d, M + 36, y, q, f(25), width=W - 2 * M - 72, gap=8) + 6

    footer(img, "Source: 大物B1总复习.pdf p52-p53; PPT课堂练习-结构化.md slide 2; ch06_static_review_v2/03_概念辨析与自测题.md")
    return img


pages = [
    ("ch06_v2_sample_01_one_hour_map.png", page1()),
    ("ch06_v2_sample_02_gauss_dense.png", page2()),
]
paths = []
for name, img in pages:
    p = OUT / name
    img.convert("RGB").save(p, quality=96)
    paths.append(str(p))

(OUT / "manifest.json").write_text(json.dumps({"pages": paths, "status": "v2 sample images only, not final PDF"}, ensure_ascii=False, indent=2), encoding="utf-8")
for p in paths:
    print(p)
