# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json

BASE = Path(r"E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理")
ASSETS = BASE / "outputs" / "ch06_static_review_assets"
OUT = BASE / "outputs" / "ch06_static_review_preview"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1600, 2263
M = 72
FONT_DIR = Path(r"C:\Windows\Fonts")
FONT_CN = FONT_DIR / "msyh.ttc"
FONT_BOLD = FONT_DIR / "msyhbd.ttc"
FONT_MATH = FONT_DIR / "DejaVuSans.ttf"
if not FONT_CN.exists():
    FONT_CN = FONT_DIR / "simhei.ttf"
if not FONT_BOLD.exists():
    FONT_BOLD = FONT_CN
if not FONT_MATH.exists():
    FONT_MATH = FONT_CN

COL = {
    "bg": (247, 250, 252),
    "ink": (21, 32, 43),
    "muted": (91, 107, 122),
    "blue": (35, 99, 155),
    "teal": (0, 126, 137),
    "red": (196, 72, 72),
    "yellow": (245, 184, 67),
    "green": (48, 140, 95),
    "line": (206, 218, 228),
    "card": (255, 255, 255),
    "softred": (253, 235, 232),
    "purple": (116, 91, 168),
}


def font(size, bold=False, math=False):
    return ImageFont.truetype(str(FONT_MATH if math else (FONT_BOLD if bold else FONT_CN)), size)


def text_wh(draw, text, ft):
    box = draw.textbbox((0, 0), text, font=ft)
    return box[2] - box[0], box[3] - box[1]


def wrap(draw, text, ft, max_w):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for ch in para:
            test = cur + ch
            if not cur or text_wh(draw, test, ft)[0] <= max_w:
                cur = test
            else:
                lines.append(cur)
                cur = ch
        lines.append(cur)
    return lines


def draw_text(draw, xy, text, ft, fill=COL["ink"], max_w=None, gap=8):
    x, y = xy
    lines = wrap(draw, text, ft, max_w) if max_w else text.split("\n")
    for line in lines:
        draw.text((x, y), line, font=ft, fill=fill)
        y += text_wh(draw, line or " ", ft)[1] + gap
    return y


def round_rect(draw, xy, fill, outline=None, width=2, r=8):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def shadow_card(img, xy, fill=(255, 255, 255), outline=(211, 222, 232), r=8):
    x1, y1, x2, y2 = xy
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((x1 + 5, y1 + 7, x2 + 5, y2 + 7), radius=r, fill=(40, 70, 90, 32))
    sh = sh.filter(ImageFilter.GaussianBlur(7))
    img.alpha_composite(sh)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=2)


def page_bg():
    return Image.new("RGBA", (W, H), COL["bg"] + (255,))


def header(img, title, subtitle=None, tag="第06章 静电场"):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 160), fill=(28, 83, 122))
    d.rectangle((0, 142, W, 160), fill=COL["yellow"])
    d.text((M, 36), title, font=font(46, True), fill="white")
    if subtitle:
        d.text((M, 102), subtitle, font=font(22), fill=(226, 240, 250))
    tw = text_wh(d, tag, font(22, True))[0]
    round_rect(d, (W - M - tw - 42, 42, W - M, 92), fill=(28, 83, 122), outline=(255, 255, 255), width=1)
    d.text((W - M - tw - 22, 53), tag, font=font(22, True), fill="white")


def footer(img, src):
    d = ImageDraw.Draw(img)
    d.line((M, H - 58, W - M, H - 58), fill=COL["line"], width=2)
    d.text((M, H - 44), src, font=font(16), fill=COL["muted"])
    d.text((W - M - 155, H - 44), "preview image only", font=font(16), fill=COL["muted"])


def paste_fit(img, src_path, box):
    x1, y1, x2, y2 = box
    src = Image.open(src_path).convert("RGB")
    src.thumbnail((x2 - x1, y2 - y1), Image.Resampling.LANCZOS)
    d = ImageDraw.Draw(img)
    round_rect(d, box, fill=(255, 255, 255), outline=COL["line"], width=2)
    px = x1 + (x2 - x1 - src.width) // 2
    py = y1 + (y2 - y1 - src.height) // 2
    img.paste(src, (px, py))


def bullet_card(img, xy, title, bullets, color, note=None):
    shadow_card(img, xy)
    d = ImageDraw.Draw(img)
    x1, y1, x2, y2 = xy
    d.rectangle((x1, y1, x2, y1 + 58), fill=color)
    d.text((x1 + 22, y1 + 14), title, font=font(25, True), fill="white")
    y = y1 + 78
    for item in bullets:
        d.ellipse((x1 + 24, y + 10, x1 + 34, y + 20), fill=color)
        y = draw_text(d, (x1 + 48, y), item, font(22), max_w=x2 - x1 - 76, gap=7) + 8
    if note:
        round_rect(d, (x1 + 22, y2 - 72, x2 - 22, y2 - 20), fill=(247, 250, 252), outline=COL["line"], width=1)
        draw_text(d, (x1 + 38, y2 - 60), note, font(18), fill=COL["muted"], max_w=x2 - x1 - 76, gap=4)


def make_page_1():
    img = page_bg()
    header(img, "第六章 静电场：期末高频复习地图", "P0：高斯定理对称分布  /  P1：电势叠加与导体静电平衡")
    d = ImageDraw.Draw(img)
    cx, cy = W // 2, 620
    round_rect(d, (cx - 210, cy - 92, cx + 210, cy + 92), fill=(255, 255, 255), outline=COL["blue"], width=4, r=12)
    d.text((cx - 155, cy - 42), "静电场主线", font=font(40, True), fill=COL["blue"])
    d.text((cx - 130, cy + 14), "电荷 → E → U → 导体", font=font(25, True), fill=COL["ink"])

    branches = [
        ((115, 300, 560, 520), "1 场强 E 怎么算？", ["点电荷：E = kQ/r²", "点电荷系：矢量叠加", "连续体：切元 dq，再积分"], COL["teal"]),
        ((1040, 300, 1485, 520), "2 高斯定理怎么用？", ["先看对称性：球/柱/面", "选高斯面，使 E 可提出积分", "只看 Q_in，不等于只看内部场源"], COL["red"]),
        ((115, 760, 560, 1010), "3 电势 U 怎么算？", ["电势是标量，优先叠加", "U_a = ∫_a^∞ E·dl", "电势差只看始末点"], COL["purple"]),
        ((1040, 760, 1485, 1010), "4 导体怎么判断？", ["静电平衡：导体内 E=0", "导体整体等势", "空腔/外表面电荷守恒"], COL["green"]),
    ]
    for box, title, bullets, color in branches:
        x1, y1, x2, y2 = box
        d.line((cx, cy, (x1 + x2) // 2, (y1 + y2) // 2), fill=(154, 171, 185), width=5)
        bullet_card(img, box, title, bullets, color)

    shadow_card(img, (M, 1190, W - M, 1745))
    d.rectangle((M, 1190, W - M, 1255), fill=COL["blue"])
    d.text((M + 28, 1208), "考试 DNA：看到题先分类，不要先套公式", font=font(30, True), fill="white")
    labels = [
        ("A. 判断题/选择题", "高斯定理里的通量由 Q_in 决定；曲面上 E 由所有电荷决定。", "常错：Q_in=0 就误以为面上处处 E=0。"),
        ("B. 计算题/填空题", "球对称、柱对称、面对称优先高斯；非强对称再积分。", "常错：没有先证明对称性就把 E 提出来。"),
        ("C. 电势/能量题", "电势是标量，功和电势差绑定；零势点必须先说明。", "常错：把 E 的矢量叠加方法照搬到 U。"),
    ]
    cols = [(M + 35, 1295, 505, 1695), (565, 1295, 1035, 1695), (1095, 1295, W - M - 35, 1695)]
    for box, (title, body, note) in zip(cols, labels):
        x1, y1, x2, y2 = box
        round_rect(d, box, fill=(247, 250, 252), outline=COL["line"], width=2)
        d.text((x1 + 20, y1 + 18), title, font=font(25, True), fill=COL["blue"])
        draw_text(d, (x1 + 20, y1 + 70), body, font(22), max_w=x2 - x1 - 40)
        round_rect(d, (x1 + 20, y2 - 98, x2 - 20, y2 - 24), fill=(255, 248, 225), outline=(242, 205, 119), width=1)
        draw_text(d, (x1 + 34, y2 - 84), note, font(18), fill=(111, 77, 20), max_w=x2 - x1 - 68, gap=4)

    paste_fit(img, ASSETS / "total_review_p48.png", (M, 1810, W - M, 2110))
    footer(img, "Source: Ch06-静电场-高频考点.md; Codex_Knowledge_Base.md; 大物B1总复习.pdf p48")
    return img


def make_page_2():
    img = page_bg()
    header(img, "高斯定理：三种对称模型一页过", "先证明对称性，再选高斯面，最后算 Q_in")
    d = ImageDraw.Draw(img)
    shadow_card(img, (M, 210, W - M, 455))
    d.text((M + 28, 232), "核心公式", font=font(30, True), fill=COL["blue"])
    d.text((M + 265, 230), "∮_S E · dS = Q_in / ε0", font=font(43, True, True), fill=COL["red"])
    draw_text(d, (M + 28, 312), "解题口令：电荷分布对称 → E 的方向/大小对称 → 选高斯面 → 通量积分 → 包围电荷。", font(25), max_w=W - 2 * M - 56)
    draw_text(d, (M + 28, 374), "判断题口令：通量只由闭合面内电荷决定；面上各点场强由空间所有电荷共同决定。", font(24), fill=COL["teal"], max_w=W - 2 * M - 56)

    paste_fit(img, ASSETS / "total_review_p52.png", (M, 500, W - M, 990))
    paste_fit(img, ASSETS / "total_review_p53.png", (M, 1030, W - M, 1520))

    cards = [
        ("柱对称：无限长线电荷", "E·2πrL = λL/ε0  →  E = λ/(2π ε0 r)", "高斯面：同轴圆柱面。侧面有通量，上下底无通量。"),
        ("面对称：无限大带电平面", "2E·ΔS = σΔS/ε0  →  E = σ/(2ε0)", "高斯面：穿过平面的短圆柱。两侧场强等大反向。"),
        ("球对称：均匀带电球/球面", "E·4πr² = Q_in/ε0", "高斯面：同心球面。内部外部要分段。"),
    ]
    xs = [M, M + 500, M + 1000]
    colors = [COL["teal"], COL["red"], COL["purple"]]
    for i, (title, formula, note) in enumerate(cards):
        x = xs[i]
        x2 = x + 430 if i < 2 else W - M
        y = 1585
        round_rect(d, (x, y, x2, 1900), fill=(255, 255, 255), outline=COL["line"], width=2)
        d.text((x + 20, y + 18), title, font=font(22, True), fill=colors[i])
        draw_text(d, (x + 20, y + 72), formula, font(20, True, True), max_w=x2 - x - 40, gap=6)
        draw_text(d, (x + 20, y + 160), note, font(19), fill=COL["muted"], max_w=x2 - x - 40, gap=6)

    shadow_card(img, (M, 1945, W - M, 2110), fill=COL["softred"])
    d.text((M + 28, 1968), "最容易丢分的点", font=font(25, True), fill=COL["red"])
    draw_text(d, (M + 28, 2015), "没有高对称性时，不允许直接把 E 从 ∮E·dS 中提出；这类题回到库仑定律叠加或切元积分。", font(23), max_w=W - 2 * M - 56)
    footer(img, "Source: 大物B1总复习.pdf p52-p53; Ch06-静电场-高频考点.md")
    return img


def make_page_3():
    img = page_bg()
    header(img, "电势与电势能：标量思维，先定零势点", "U 比 E 更适合叠加；电场力做功只看始末位置")
    d = ImageDraw.Draw(img)
    cards = [
        ("电势定义", ["U_a = ∫_a^∞ E · dl", "零势点通常取无穷远；若不是，题目必须说明。"], COL["blue"]),
        ("电势差", ["U_ab = U_a - U_b = ∫_a^b E · dl", "静电力做功 W_ab = q(U_a-U_b)。"], COL["teal"]),
        ("场强关系", ["E = -grad U", "一维时 E_x = -dU/dx，方向指向电势降低最快处。"], COL["purple"]),
    ]
    for i, (title, bullets, color) in enumerate(cards):
        x = M + i * 500
        x2 = x + 455 if i < 2 else W - M
        bullet_card(img, (x, 220, x2, 520), title, bullets, color)

    paste_fit(img, ASSETS / "total_review_p54.png", (M, 575, W - M, 1075))
    paste_fit(img, ASSETS / "total_review_p55.png", (M, 1125, W - M, 1575))

    shadow_card(img, (M, 1635, W - M, 2020))
    d.rectangle((M, 1635, W - M, 1698), fill=COL["teal"])
    d.text((M + 28, 1652), "均匀带电球体电势分布：考试步骤", font=font(30, True), fill="white")
    steps = [
        "先用高斯定理分段求 E：r<R 与 r>R 不同。",
        "再从无穷远积分到目标点：跨过边界时必须分段积分。",
        "最后检查连续性：r=R 处内外电势应该相等。",
        "别把电势当矢量：多个点电荷电势直接代数相加。",
    ]
    y = 1738
    for i, item in enumerate(steps, start=1):
        d.ellipse((M + 32, y, M + 70, y + 38), fill=COL["yellow"])
        d.text((M + 45, y + 4), str(i), font=font(20, True), fill=(75, 53, 8))
        draw_text(d, (M + 88, y + 2), item, font(24), max_w=W - 2 * M - 120)
        y += 62
    footer(img, "Source: 大物B1总复习.pdf p54-p55; PPT课堂练习-结构化.md p91-p92题型")
    return img


def make_page_4():
    img = page_bg()
    header(img, "导体静电平衡 + 课堂高频题型", "本页把概念判断题和球壳计算题连起来")
    d = ImageDraw.Draw(img)
    paste_fit(img, ASSETS / "total_review_p56.png", (M, 215, W - M, 725))
    paste_fit(img, ASSETS / "total_review_p57.png", (M, 765, W - M, 1255))

    shadow_card(img, (M, 1310, W - M, 1568))
    d.rectangle((M, 1310, W - M, 1372), fill=COL["green"])
    d.text((M + 28, 1327), "导体静电平衡三条硬规则", font=font(30, True), fill="white")
    rules = [
        "导体内部 E = 0；导体整体为等势体。",
        "空腔内无电荷：电荷只在外表面；空腔内有电荷：内表面感应等量异号。",
        "球壳题先画电荷分布，再分区域写 E，最后积分求 U。",
    ]
    y = 1410
    for item in rules:
        d.rectangle((M + 32, y + 6, M + 48, y + 22), fill=COL["green"])
        y = draw_text(d, (M + 64, y), item, font(24), max_w=W - 2 * M - 96) + 6

    shadow_card(img, (M, 1628, W - M, 2065))
    d.rectangle((M, 1628, W - M, 1690), fill=COL["blue"])
    d.text((M + 28, 1645), "课堂练习高频陷阱：先会判断，再做计算", font=font(30, True), fill="white")
    exs = [
        ("通量判断", "点电荷 q 在立方体中心：总通量 q/ε0，每个面 q/(6ε0)。若在顶角，要用 8 个立方体拼成大立方体。"),
        ("高斯概念", "Q_in=0 只说明总通量为 0，不说明闭合面上各点 E=0。E 受面内外所有电荷影响。"),
        ("电势正负", "某点电势正负取决于零势点选择，不取决于试探电荷正负。"),
        ("等势做功", "从 A 到同一等势圆周上的 B/C/D，电场力做功相同，因为只看电势差。"),
    ]
    for idx, (title, body) in enumerate(exs):
        x = M + 28 + (idx % 2) * 720
        y = 1728 + (idx // 2) * 155
        x2 = x + 680
        y2 = y + 125
        round_rect(d, (x, y, x2, y2), fill=(247, 250, 252), outline=COL["line"], width=2)
        d.text((x + 18, y + 14), title, font=font(23, True), fill=COL["red"] if idx == 1 else COL["blue"])
        draw_text(d, (x + 18, y + 50), body, font(19), max_w=x2 - x - 36, gap=4)
    footer(img, "Source: 大物B1总复习.pdf p56-p57; 第06章-静电场/习题/PPT课堂练习-结构化.md slides 1-7,21")
    return img


pages = [
    ("ch06_static_review_01_mindmap.png", make_page_1()),
    ("ch06_static_review_02_gauss.png", make_page_2()),
    ("ch06_static_review_03_potential.png", make_page_3()),
    ("ch06_static_review_04_conductor_exercises.png", make_page_4()),
]
paths = []
for name, img in pages:
    path = OUT / name
    img.convert("RGB").save(path, quality=95)
    paths.append(str(path))

(OUT / "manifest.json").write_text(
    json.dumps(
        {
            "pages": paths,
            "source_pages": ["大物B1总复习.pdf p48", "大物B1总复习.pdf p52-p57"],
            "status": "preview images only; PDF generation intentionally paused until user approval",
        },
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)

for path in paths:
    print(path)
