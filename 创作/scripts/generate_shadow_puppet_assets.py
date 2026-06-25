from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"E:\ai产出文件\牛马\竞赛\竞赛\2026跨校协作新场景赛项\皮影\5.28")
OUT_OVERVIEW = ROOT / "总览图"
OUT_PARTS = ROOT / "零件"
WORK = ROOT / "制作中"
OUT_COLOR = WORK / "彩色零件图"
OUT_BW = WORK / "黑白零件图"
OUT_WORK_OVERVIEW = WORK / "总览图"
OUT_DOC = WORK / "提示词与清单"


FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\simsun.ttc",
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [r"C:\Windows\Fonts\msyhbd.ttc"] + FONT_CANDIDATES if bold else FONT_CANDIDATES
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


F_TITLE = font(46, True)
F_H1 = font(34, True)
F_H2 = font(26, True)
F_BODY = font(22)
F_SMALL = font(18)
F_TINY = font(15)


GOLD = (207, 158, 65)
AMBER = (232, 160, 48)
BG = (10, 10, 10)
PANEL = (24, 18, 10)
WHITE = (245, 240, 230)
INK = (20, 20, 20)
LINE = (42, 42, 42)
BRASS = (192, 137, 45)


@dataclass(frozen=True)
class Role:
    act: int
    act_name: str
    name: str
    short: str
    age: str
    height: int
    colors: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]
    prop: str
    action_a: str
    action_b: str
    note: str
    control: str = "manual"
    family: str = ""
    shared_head: str = ""


ROLES: list[Role] = [
    Role(1, "梦从光里起飞", "蔡俊青年态", "青年蔡俊", "20岁", 176, ((26, 39, 68), (200, 164, 92), (241, 214, 180)), "书本", "抬头听课", "举手回应", "第一幕：同头模主角-学生外壳", "servo", "cai-jun", "C1-A 共用头模"),
    Role(1, "梦从光里起飞", "老教授", "教授", "70岁", 175, ((24, 30, 42), (190, 150, 75), (229, 190, 145)), "粉笔", "激情授课", "殷切期望", "第一幕：启发者"),
    Role(1, "梦从光里起飞", "招飞面试官", "面试官", "50岁", 180, ((28, 34, 52), (194, 147, 68), (235, 205, 180)), "通知单", "递出材料", "沉思判断", "第一幕：转折点"),
    Role(2, "灯火里的协奏", "总设计师", "总设", "65岁", 180, ((218, 212, 194), (28, 38, 56), (232, 198, 150)), "图纸", "俯身审图", "举目远望", "第二幕：定方向"),
    Role(2, "灯火里的协奏", "系统协调工程师", "协调", "45岁", 178, ((26, 39, 68), (30, 30, 28), (232, 190, 135)), "手机+记录本", "边走边记", "快步攻关", "第二幕：跨系统闭环"),
    Role(2, "灯火里的协奏", "青年装配工", "装配", "25岁", 176, ((35, 66, 105), (212, 130, 42), (238, 202, 160)), "扭矩扳手", "精准装配", "举手庆祝", "第二幕：执行落地"),
    Role(3, "驾驶舱里的登台", "蔡俊中年机长态", "中年蔡俊", "35岁", 176, ((20, 48, 88), (230, 230, 220), (232, 192, 150)), "操纵杆", "检查仪表", "拉杆起飞", "第三幕：同头模主角-机长外壳", "servo", "cai-jun", "C1-A 共用头模"),
    Role(3, "驾驶舱里的登台", "副驾驶", "副驾", "35岁", 176, ((29, 45, 82), (226, 226, 214), (235, 198, 160)), "检查单", "核对清单", "口令确认", "第三幕：协同确认"),
    Role(3, "驾驶舱里的登台", "飞行试验观察员", "观察员", "40岁", 178, ((23, 38, 60), (70, 90, 105), (232, 190, 145)), "记录板+耳麦", "记录参数", "举手确认", "第三幕：数据监测"),
    Role(4, "盛世华章", "记者", "记者", "30岁", 175, ((43, 94, 165), (225, 225, 220), (245, 205, 168)), "话筒", "现场播报", "举手欢呼", "第四幕：公共见证"),
    Role(4, "盛世华章", "儿童", "儿童", "8岁", 140, ((203, 34, 34), (42, 76, 105), (245, 205, 168)), "C919模型", "双手托举", "跳跃仰望", "第四幕：未来传承"),
    Role(4, "盛世华章", "老航空人", "老人", "70岁", 170, ((105, 105, 110), (160, 125, 78), (230, 190, 150)), "拐杖", "挥手致意", "抬头微笑", "第四幕：历史见证"),
]


PARTS = [
    ("C1", "头部", "45×28mm", "1孔：N 颈"),
    ("C2", "上身", "40×55mm", "4孔：N/SA/SB/W"),
    ("C3", "下身", "35×30mm", "3孔：W/HA/HB"),
    ("C4", "左上臂", "30×14mm", "2孔：SA/EA"),
    ("C5", "右上臂", "30×14mm", "2孔：SB/EB"),
    ("C6", "左前臂+手", "35×22mm", "2孔：EA/WB"),
    ("C7", "右前臂+手", "35×22mm", "2孔：EB/WA"),
    ("C8", "左腿", "65×18mm", "1孔：HA"),
    ("C9", "右腿", "65×18mm", "1孔：HB"),
    ("C10", "道具", "15×55mm", "手持/非铆钉"),
]


def ensure_dirs() -> None:
    for p in [OUT_OVERVIEW, OUT_PARTS, OUT_COLOR, OUT_BW, OUT_WORK_OVERVIEW, OUT_DOC]:
        p.mkdir(parents=True, exist_ok=True)


def draw_text(draw: ImageDraw.ImageDraw, xy, text: str, fill=WHITE, fnt=F_BODY, anchor=None) -> None:
    draw.text(xy, text, fill=fill, font=fnt, anchor=anchor)


def round_box(draw: ImageDraw.ImageDraw, box, outline=GOLD, fill=None, width=2, r=16) -> None:
    draw.rounded_rectangle(box, radius=r, outline=outline, fill=fill, width=width)


def glow_background(size: tuple[int, int]) -> Image.Image:
    w, h = size
    img = Image.new("RGB", size, BG)
    pix = img.load()
    for y in range(h):
        for x in range(w):
            dx = (x - w * 0.5) / w
            dy = (y - h * 0.48) / h
            r = max(0, 1 - math.sqrt(dx * dx * 5.0 + dy * dy * 5.5))
            a = int(85 * r)
            pix[x, y] = (BG[0] + a, BG[1] + int(a * 0.58), BG[2] + int(a * 0.22))
    return img


def joint(draw, x, y, r=11, color=GOLD, fill=(45, 32, 15)) -> None:
    draw.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline=color, width=3)
    draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=color)


def limb(draw, p1, p2, width, fill, outline=GOLD, bw=False) -> None:
    if bw:
        fill = (252, 252, 252)
        outline = INK
    draw.line((p1, p2), fill=outline, width=width + 6)
    draw.line((p1, p2), fill=fill, width=width)
    joint(draw, *p1, r=max(6, width // 3), color=outline if bw else GOLD, fill=(255, 255, 255) if bw else (45, 32, 15))
    joint(draw, *p2, r=max(6, width // 3), color=outline if bw else GOLD, fill=(255, 255, 255) if bw else (45, 32, 15))


def draw_prop(draw, role: Role, x, y, scale=1.0, bw=False) -> None:
    fill = (245, 245, 245) if bw else role.colors[1]
    outline = INK if bw else GOLD
    p = role.prop
    if "书" in p:
        draw.rounded_rectangle((x - 20 * scale, y - 12 * scale, x + 24 * scale, y + 16 * scale), 4, fill=fill, outline=outline, width=2)
        draw.line((x + 2 * scale, y - 10 * scale, x + 2 * scale, y + 14 * scale), fill=outline, width=2)
    elif "粉笔" in p:
        draw.rounded_rectangle((x - 5 * scale, y - 28 * scale, x + 7 * scale, y + 28 * scale), 4, fill=(250, 250, 240), outline=outline, width=2)
    elif "通知" in p or "检查单" in p or "记录" in p:
        draw.rounded_rectangle((x - 22 * scale, y - 30 * scale, x + 25 * scale, y + 30 * scale), 5, fill=(250, 246, 230), outline=outline, width=2)
        for i in range(4):
            draw.line((x - 14 * scale, y - 15 * scale + i * 10 * scale, x + 17 * scale, y - 15 * scale + i * 10 * scale), fill=outline, width=1)
    elif "图纸" in p:
        draw.rectangle((x - 38 * scale, y - 20 * scale, x + 42 * scale, y + 22 * scale), fill=(230, 220, 190), outline=outline, width=2)
        draw.line((x - 30 * scale, y, x + 35 * scale, y), fill=outline, width=1)
        draw.arc((x - 20 * scale, y - 13 * scale, x + 20 * scale, y + 13 * scale), 0, 180, fill=outline, width=1)
    elif "手机" in p:
        draw.rounded_rectangle((x - 12 * scale, y - 24 * scale, x + 12 * scale, y + 25 * scale), 4, fill=(30, 30, 32), outline=outline, width=2)
    elif "扳手" in p or "操纵杆" in p:
        draw.line((x - 30 * scale, y + 20 * scale, x + 30 * scale, y - 20 * scale), fill=outline, width=max(2, int(5 * scale)))
        draw.ellipse((x + 24 * scale, y - 28 * scale, x + 42 * scale, y - 10 * scale), outline=outline, width=3)
    elif "话筒" in p:
        draw.ellipse((x - 12 * scale, y - 34 * scale, x + 12 * scale, y - 10 * scale), fill=fill, outline=outline, width=2)
        draw.line((x, y - 8 * scale, x, y + 28 * scale), fill=outline, width=max(2, int(5 * scale)))
    elif "C919" in p:
        draw.polygon([(x - 42 * scale, y + 4 * scale), (x + 40 * scale, y - 2 * scale), (x - 42 * scale, y - 10 * scale)], fill=fill, outline=outline)
        draw.polygon([(x - 8 * scale, y - 4 * scale), (x - 25 * scale, y - 28 * scale), (x + 8 * scale, y - 6 * scale)], fill=fill, outline=outline)
        draw.polygon([(x + 18 * scale, y - 2 * scale), (x + 36 * scale, y - 22 * scale), (x + 26 * scale, y - 1 * scale)], fill=fill, outline=outline)
    elif "拐杖" in p:
        draw.arc((x - 16 * scale, y - 35 * scale, x + 16 * scale, y - 5 * scale), 180, 360, fill=outline, width=3)
        draw.line((x, y - 5 * scale, x, y + 45 * scale), fill=outline, width=3)
    else:
        draw.rectangle((x - 15 * scale, y - 15 * scale, x + 15 * scale, y + 15 * scale), fill=fill, outline=outline, width=2)


def draw_puppet(draw, role: Role, cx: int, cy: int, scale=1.0, pose="neutral", bw=False, ghost=False) -> None:
    main, accent, skin = role.colors
    if bw:
        main, accent, skin = (252, 252, 252), (245, 245, 245), (252, 252, 252)
    outline = INK if bw else GOLD
    alpha_fill = tuple(max(0, int(c * (0.55 if ghost else 1))) for c in main)
    sx = lambda v: int(v * scale)

    head = (cx, cy - sx(150))
    neck = (cx, cy - sx(114))
    waist = (cx, cy + sx(10))
    l_sh = (cx - sx(42), cy - sx(92))
    r_sh = (cx + sx(42), cy - sx(92))
    if pose == "a":
        l_el, l_hand = (cx - sx(75), cy - sx(40)), (cx - sx(105), cy + sx(10))
        r_el, r_hand = (cx + sx(84), cy - sx(58)), (cx + sx(112), cy - sx(20))
        head = (cx + sx(4), cy - sx(152))
    elif pose == "b":
        l_el, l_hand = (cx - sx(25), cy - sx(148)), (cx - sx(8), cy - sx(205))
        r_el, r_hand = (cx + sx(80), cy - sx(36)), (cx + sx(118), cy - sx(14))
        head = (cx + sx(10), cy - sx(158))
    else:
        l_el, l_hand = (cx - sx(70), cy - sx(34)), (cx - sx(76), cy + sx(45))
        r_el, r_hand = (cx + sx(70), cy - sx(34)), (cx + sx(76), cy + sx(45))

    l_hip, r_hip = (cx - sx(28), cy + sx(28)), (cx + sx(28), cy + sx(28))
    l_knee, r_knee = (cx - sx(44), cy + sx(116)), (cx + sx(44), cy + sx(116))
    l_foot, r_foot = (cx - sx(54), cy + sx(190)), (cx + sx(54), cy + sx(190))

    if not bw:
        draw.ellipse((cx - sx(135), cy - sx(215), cx + sx(135), cy + sx(210)), fill=(80, 48, 10))
    limb(draw, l_sh, l_el, sx(22), alpha_fill, outline, bw)
    limb(draw, l_el, l_hand, sx(20), alpha_fill, outline, bw)
    limb(draw, r_sh, r_el, sx(22), alpha_fill, outline, bw)
    limb(draw, r_el, r_hand, sx(20), alpha_fill, outline, bw)

    torso = [(cx - sx(52), cy - sx(108)), (cx + sx(52), cy - sx(108)), (cx + sx(44), cy + sx(22)), (cx - sx(44), cy + sx(22))]
    draw.polygon(torso, fill=alpha_fill, outline=outline)
    draw.line((cx, cy - sx(102), cx, cy + sx(18)), fill=outline, width=max(1, sx(2)))
    for i in range(4):
        joint(draw, cx, cy - sx(70 - i * 28), r=max(5, sx(5)), color=outline, fill=(255, 255, 255) if bw else accent)

    draw.rounded_rectangle((cx - sx(44), cy + sx(18), cx + sx(44), cy + sx(78)), sx(6), fill=alpha_fill, outline=outline, width=max(1, sx(2)))
    limb(draw, l_hip, l_knee, sx(24), alpha_fill, outline, bw)
    limb(draw, l_knee, l_foot, sx(24), alpha_fill, outline, bw)
    limb(draw, r_hip, r_knee, sx(24), alpha_fill, outline, bw)
    limb(draw, r_knee, r_foot, sx(24), alpha_fill, outline, bw)

    draw.ellipse((head[0] - sx(30), head[1] - sx(36), head[0] + sx(30), head[1] + sx(34)), fill=skin, outline=outline, width=max(1, sx(2)))
    if role.family == "cai-jun":
        # Cai Jun keeps the same recognizable head mold across youth and captain states.
        draw.arc((head[0] - sx(26), head[1] - sx(34), head[0] + sx(26), head[1] - sx(2)), 180, 360, fill=INK if bw else (24, 20, 18), width=max(2, sx(7)))
        draw.line((head[0] - sx(12), head[1] - sx(22), head[0] + sx(18), head[1] - sx(24)), fill=INK if bw else (24, 20, 18), width=max(1, sx(3)))
    draw.arc((head[0] - sx(18), head[1] - sx(4), head[0] + sx(18), head[1] + sx(18)), 0, 180, fill=INK if bw else (82, 45, 25), width=max(1, sx(2)))
    draw.line((head[0] - sx(9), head[1] - sx(8), head[0] - sx(2), head[1] - sx(8)), fill=INK, width=max(1, sx(2)))
    draw.line((head[0] + sx(2), head[1] - sx(8), head[0] + sx(10), head[1] - sx(8)), fill=INK, width=max(1, sx(2)))
    draw.line((head[0], head[1] - sx(2), head[0] - sx(4), head[1] + sx(10)), fill=INK, width=max(1, sx(2)))

    for pt in [neck, l_sh, r_sh, l_el, r_el, waist]:
        joint(draw, *pt, r=max(7, sx(8)), color=outline, fill=(255, 255, 255) if bw else (45, 32, 15))
    draw_prop(draw, role, r_hand[0] + sx(18), r_hand[1] - sx(8), scale=scale, bw=bw)


def part_card(draw, role: Role, x, y, code, name, size, note, color=True, bw=False) -> None:
    main, accent, skin = role.colors
    fill = (252, 252, 252) if bw else (skin if code == "C1" else main if code not in {"C10"} else accent)
    outline = INK if bw else GOLD
    draw_text(draw, (x, y - 56), code, fill=outline if bw else WHITE, fnt=F_H2, anchor="mm")
    draw_text(draw, (x, y - 28), name, fill=outline if bw else WHITE, fnt=F_SMALL, anchor="mm")
    if code == "C1":
        draw.ellipse((x - 36, y - 18, x + 36, y + 62), fill=fill, outline=outline, width=3)
        if role.family == "cai-jun":
            draw.arc((x - 31, y - 18, x + 31, y + 20), 180, 360, fill=INK if bw else (24, 20, 18), width=5)
            draw.line((x - 14, y + 2, x + 16, y), fill=INK if bw else (24, 20, 18), width=2)
        draw.arc((x - 18, y + 10, x + 18, y + 32), 0, 180, fill=INK, width=2)
        holes = [(x, y + 55)]
    elif code == "C2":
        draw.polygon([(x - 54, y - 10), (x + 54, y - 10), (x + 44, y + 95), (x - 44, y + 95)], fill=fill, outline=outline)
        draw.line((x, y - 8, x, y + 92), fill=outline, width=2)
        holes = [(x, y - 4), (x - 42, y + 14), (x + 42, y + 14), (x, y + 88)]
    elif code == "C3":
        draw.rounded_rectangle((x - 44, y, x + 44, y + 75), 8, fill=fill, outline=outline, width=3)
        holes = [(x, y + 5), (x - 32, y + 65), (x + 32, y + 65)]
    elif code in {"C4", "C5", "C8", "C9"}:
        h = 86 if code in {"C4", "C5"} else 118
        w = 22 if code in {"C4", "C5"} else 28
        draw.rounded_rectangle((x - w, y, x + w, y + h), 16, fill=fill, outline=outline, width=3)
        holes = [(x, y + 10), (x, y + h - 10)] if code in {"C4", "C5"} else [(x, y + 12)]
    elif code in {"C6", "C7"}:
        draw.rounded_rectangle((x - 22, y + 20, x + 22, y + 96), 14, fill=fill, outline=outline, width=3)
        draw.ellipse((x - 30, y - 4, x + 30, y + 32), fill=role.colors[2] if not bw else fill, outline=outline, width=3)
        holes = [(x, y + 32), (x, y + 86)]
    else:
        draw_prop(draw, role, x, y + 45, scale=1.1, bw=bw)
        holes = []
    for hx, hy in holes:
        joint(draw, hx, hy, r=8, color=outline, fill=(255, 255, 255) if bw else (45, 32, 15))
    draw_text(draw, (x, y + 138), size, fill=outline if bw else WHITE, fnt=F_TINY, anchor="mm")
    draw_text(draw, (x, y + 160), note, fill=outline if bw else WHITE, fnt=F_TINY, anchor="mm")


def generate_parts(role: Role, bw=False) -> Image.Image:
    w, h = 1536, 2048
    img = Image.new("RGB", (w, h), (250, 250, 248) if bw else BG)
    draw = ImageDraw.Draw(img)
    if not bw:
        img.paste(glow_background((w, h)))
    title = f"{role.name} · {'黑白零件图' if bw else '彩色零件图'}（10件）"
    draw_text(draw, (w // 2, 54), title, fill=INK if bw else GOLD, fnt=F_H1, anchor="mm")
    draw_text(draw, (w // 2, 100), "2mm PC膜｜6关节可动｜C1-C10零件体系｜单位：mm", fill=INK if bw else GOLD, fnt=F_BODY, anchor="mm")

    outline = INK if bw else GOLD
    txt = INK if bw else WHITE
    round_box(draw, (28, 22, 340, 210), outline=outline, fill=None if bw else PANEL, width=3)
    draw_text(draw, (54, 52), "材料 / MATERIAL", fill=outline, fnt=F_H2)
    material = ["PC膜 2mm × 10pc", "黄铜铆钉 Φ1.5mm × 19pc", f"颜料：主色/辅助色/肤色", "背光：3500K 暖琥珀"]
    if role.family == "cai-jun":
        material[2] = "头模共用：青年/机长仅换装"
    for i, line in enumerate(material):
        draw_text(draw, (58, 92 + i * 28), "• " + line, fill=txt, fnt=F_SMALL)
    round_box(draw, (1180, 22, 1506, 210), outline=outline, fill=None if bw else PANEL, width=3)
    draw_text(draw, (1210, 52), "铆钉 / RIVET", fill=outline, fnt=F_H2)
    for i, line in enumerate(["黄铜 Φ1.5mm", "共 19 颗", "预留0.3mm活动间隙"]):
        draw_text(draw, (1216, 94 + i * 32), "• " + line, fill=txt, fnt=F_SMALL)

    positions = [
        (760, 235), (760, 455), (760, 675),
        (360, 455), (1160, 455), (360, 735), (1160, 735),
        (560, 1010), (960, 1010), (760, 1250),
    ]
    for (part, pos) in zip(PARTS, positions):
        part_card(draw, role, pos[0], pos[1], *part, bw=bw)

    round_box(draw, (40, 1510, 520, 1845), outline=outline, fill=None if bw else PANEL, width=3)
    draw_text(draw, (68, 1540), "装配顺序 / ASSEMBLY", fill=outline, fnt=F_H2)
    steps = ["① C2 上身", "② C1 头部", "③ C3 下身", "④ C4+C5 上臂", "⑤ C6+C7 前臂+手", "⑥ C8+C9 腿", "⑦ C10 道具"]
    for i, s in enumerate(steps):
        draw_text(draw, (70, 1588 + i * 34), s, fill=txt, fnt=F_SMALL)

    round_box(draw, (570, 1510, 1020, 1845), outline=outline, fill=None if bw else PANEL, width=3)
    if role.control == "servo":
        mapping_title = "6路舵机 / SERVO MAPPING"
        mapping = ["1 颈 N：SG90 点头/偏转", "2 肩 SA+SB：连杆抬臂", "3 肘 EA+EB：连杆屈伸", "4 腕 WA+WB：手势/握持", "5 腰 W：前倾/后仰", "6 髋 H：站姿/重心"]
    else:
        mapping_title = "人工操控 / MANUAL RODS"
        mapping = ["主杆：连接躯干/腰部", "左手杆：控制左臂动作", "右手杆：控制右臂动作", "头部：可独立点头/偏转", "腿部：被动悬挂或连动", "不占用舵机通道"]
    draw_text(draw, (598, 1540), mapping_title, fill=outline, fnt=F_H2)
    for i, s in enumerate(mapping):
        draw_text(draw, (600, 1588 + i * 36), s, fill=txt, fnt=F_SMALL)

    round_box(draw, (1070, 1510, 1504, 1845), outline=outline, fill=None if bw else PANEL, width=3)
    draw_text(draw, (1098, 1540), "制作提示 / TIPS", fill=outline, fnt=F_H2)
    tips = ["每人独立装配，避免混件", "所有铆钉孔位先预留", "手持道具C10不铆死", "正式提交去除真实校名/姓名"]
    for i, s in enumerate(tips):
        draw_text(draw, (1100, 1588 + i * 40), f"{i+1}. {s}", fill=txt, fnt=F_SMALL)

    extra = f"｜{role.shared_head}" if role.shared_head else ""
    ctrl = "舵机控制" if role.control == "servo" else "人工操控"
    draw_text(draw, (w // 2, 1935), f"角色：第{role.act}幕《{role.act_name}》｜{role.note}{extra}｜{ctrl}｜总高 {role.height}mm｜比例 1:1 制作参考", fill=INK if bw else GOLD, fnt=F_H2, anchor="mm")
    return img


def arc(draw, center, radius, start, end, fill=GOLD, width=3) -> None:
    x, y = center
    draw.arc((x - radius, y - radius, x + radius, y + radius), start, end, fill=fill, width=width)


def generate_overview(role: Role) -> Image.Image:
    w, h = 2048, 1152
    img = glow_background((w, h))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, w - 1, h - 1), outline=GOLD, width=4)
    draw_text(draw, (46, 30), f"{role.name} · MOTION REFERENCE SHEET", fill=GOLD, fnt=F_TITLE)
    ctrl_label = "SERVO 主角" if role.control == "servo" else "MANUAL 人工操控"
    draw_text(draw, (w - 46, 38), f"第{role.act}幕《{role.act_name}》 · {ctrl_label}", fill=GOLD, fnt=F_H1, anchor="ra")
    for x in [682, 1365]:
        draw.line((x, 94, x, 850), fill=GOLD, width=2)
    draw.line((0, 94, w, 94), fill=GOLD, width=2)
    draw.line((0, 850, w, 850), fill=GOLD, width=2)

    panels = [
        (340, 485, "中立姿态 · HOME POSITION", "neutral"),
        (1024, 485, f"{role.action_a} · ACTION A", "a"),
        (1705, 485, f"{role.action_b} · ACTION B", "b"),
    ]
    for cx, cy, label, pose in panels:
        draw_text(draw, (cx, 118), label, fill=WHITE, fnt=F_H2, anchor="mm")
        if pose != "neutral":
            arc(draw, (cx + 58, cy - 195), 90, 210, 330, fill=(214, 142, 32), width=4)
            arc(draw, (cx - 60, cy - 60), 92, 120, 250, fill=(214, 142, 32), width=4)
            draw_text(draw, (cx + 162, cy - 215), "N ±20°", fill=GOLD, fnt=F_SMALL)
            draw_text(draw, (cx + 148, cy - 75), "S 0-120°", fill=GOLD, fnt=F_SMALL)
        draw_puppet(draw, role, cx, cy, scale=1.28, pose=pose)
        draw_text(draw, (cx, 810), f"总高 {role.height}mm｜道具：{role.prop}", fill=GOLD, fnt=F_BODY, anchor="mm")

    round_box(draw, (28, 870, 660, 1122), outline=GOLD, fill=PANEL, width=3)
    draw_text(draw, (54, 900), "① 关节系统（标准6关节）", fill=GOLD, fnt=F_H2)
    for i, line in enumerate(["N 颈：±20° 点头/偏转", "S 肩：0~120° 抬臂", "E 肘：0~120° 屈伸", "W 腕：±22.5° 手势", "Waist 腰：±12° 前后倾", "H 髋：±15° 重心摆动"]):
        draw_text(draw, (64, 940 + i * 28), line, fill=WHITE, fnt=F_SMALL)

    round_box(draw, (694, 870, 1360, 1122), outline=GOLD, fill=PANEL, width=3)
    if role.control == "servo":
        control_title = "② 舵机映射 / SERVO MAPPING"
        controls = ["舵机1 → 颈 N（SG90）", "舵机2 → 肩 SA+SB（连杆）", "舵机3 → 肘 EA+EB（连杆）", "舵机4 → 腕 WA+WB（连杆）", "舵机5 → 腰 W（SG90）", "舵机6 → 髋 H（SG90）"]
    else:
        control_title = "② 人工操控 / MANUAL RODS"
        controls = ["主操控杆 → 躯干/腰", "左手杆 → 左臂", "右手杆 → 右臂", "头部可用细杆辅助点头", "腿部可被动悬挂/连动", "不接舵机，减少控制负担"]
    draw_text(draw, (720, 900), control_title, fill=GOLD, fnt=F_H2)
    for i, line in enumerate(controls):
        draw_text(draw, (730, 940 + i * 28), line, fill=WHITE, fnt=F_SMALL)

    round_box(draw, (1394, 870, 2020, 1122), outline=GOLD, fill=PANEL, width=3)
    draw_text(draw, (1420, 900), "③ 性能参数 / PERFORMANCE", fill=GOLD, fnt=F_H2)
    head_note = "｜同C1-A头模" if role.family == "cai-jun" else ""
    perf = [f"总高：{role.height}mm｜零件：10件｜铆钉：19颗{head_note}", "材料：2mm PC膜｜背光：3500K暖琥珀", f"场次：第{role.act}幕｜用途：视频demo动作参考", "动作速度：0.8~2秒/动作", "注意：正式提交图不出现真实学校/姓名"]
    for i, line in enumerate(perf):
        draw_text(draw, (1430, 940 + i * 34), line, fill=WHITE, fnt=F_SMALL)
    return img


def write_manifest() -> None:
    lines = [
        "# 5.28 皮影角色图纸交付清单",
        "",
        "## 标准",
        "- 每幕至少3个角色：已按四幕×3人配置，共12人。",
        "- 每个角色统一6关节：N颈、SA/SB肩、EA/EB肘、W腰、H髋。",
        "- 蔡俊青年态与蔡俊中年机长态使用同一C1-A头模和同一骨架，只更换C2-C10服装/道具外壳，降低主角前后割裂感。",
        "- 控制方式区分：蔡俊两态为舵机控制主角；其他角色为人工手持/联动杆控制参考，不再占用舵机通道。",
        "- 每个角色输出3张：总览图、彩色零件图、黑白零件图。",
        "- 零件统一C1-C10：头部、上身、下身、左右上臂、左右前臂+手、左右腿、道具。",
        "- 黑白图用于人工比对手画；彩色图用于后续上色；总览图用于AI视频demo动作参考。",
        "",
        "## 角色清单",
    ]
    for role in ROLES:
        ctrl = "舵机控制" if role.control == "servo" else "人工操控"
        shared = f"｜{role.shared_head}" if role.shared_head else ""
        lines.append(f"- 第{role.act}幕《{role.act_name}》：{role.name}｜{ctrl}{shared}｜道具：{role.prop}｜动作：{role.action_a} / {role.action_b}")
    lines += [
        "",
        "## 文件位置",
        f"- 总览图：`{OUT_OVERVIEW}`",
        f"- 彩色零件图：`{OUT_PARTS}`（文件名含“彩色零件图”）",
        f"- 黑白零件图：`{OUT_PARTS}`（文件名含“黑白零件图”）",
        f"- 制作中备份：`{WORK}`",
        "",
        "## 归档说明",
        "- 原图已移动到 `5.28/归档/原图_20260528_230505/`，未删除。",
    ]
    (OUT_DOC / "交付清单.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    for role in ROLES:
        overview = generate_overview(role)
        color = generate_parts(role, bw=False)
        bw = generate_parts(role, bw=True)
        overview_name = f"第{role.act}幕_{role.name}_总览图.png"
        color_name = f"第{role.act}幕_{role.name}_彩色零件图.png"
        bw_name = f"第{role.act}幕_{role.name}_黑白零件图.png"
        overview.save(OUT_OVERVIEW / overview_name)
        overview.save(OUT_WORK_OVERVIEW / overview_name)
        color.save(OUT_PARTS / color_name)
        color.save(OUT_COLOR / color_name)
        bw.save(OUT_PARTS / bw_name)
        bw.save(OUT_BW / bw_name)
    write_manifest()
    print(f"generated_roles={len(ROLES)}")
    print(f"overview_dir={OUT_OVERVIEW}")
    print(f"parts_dir={OUT_PARTS}")
    print(f"manifest={OUT_DOC / '交付清单.md'}")


if __name__ == "__main__":
    main()
