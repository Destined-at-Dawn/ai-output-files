# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
import math
import textwrap

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(r"E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理")
OUT = ROOT / "outputs" / "ch06_static_review_v3_imagegen" / "final_pdf"
OUT.mkdir(parents=True, exist_ok=True)
PDF_PATH = OUT / "第06章_静电场_蓝白电磁风复习.pdf"

PAGE_W, PAGE_H = A4
BLUE = colors.HexColor("#0B5DB8")
DEEP = colors.HexColor("#083B7A")
CYAN = colors.HexColor("#10A7C9")
RED = colors.HexColor("#D83A3A")
LIGHT = colors.HexColor("#EAF4FF")
PALE = colors.HexColor("#F7FBFF")
TEXT = colors.HexColor("#16233A")
GRAY = colors.HexColor("#5A6B82")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("SimHei", r"C:\Windows\Fonts\simhei.ttf"))
    pdfmetrics.registerFont(TTFont("SimSun", r"C:\Windows\Fonts\simsun.ttc"))
    pdfmetrics.registerFont(TTFont("Kai", r"C:\Windows\Fonts\simkai.ttf"))


def set_font(c: canvas.Canvas, name: str = "SimSun", size: int = 10, color=TEXT) -> None:
    c.setFont(name, size)
    c.setFillColor(color)


def rounded(c, x, y, w, h, r=6, stroke=BLUE, fill=colors.white, lw=0.8):
    c.setStrokeColor(stroke)
    c.setFillColor(fill)
    c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, stroke=1, fill=1)


def wrap_cn(text: str, max_chars: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        para = para.strip()
        if not para:
            lines.append("")
            continue
        lines.extend(textwrap.wrap(para, max_chars, break_long_words=True, replace_whitespace=False))
    return lines


def draw_text(c, text, x, y, size=10, font="SimSun", color=TEXT, max_chars=28, leading=14):
    set_font(c, font, size, color)
    yy = y
    for line in wrap_cn(text, max_chars):
        c.drawString(x, yy, line)
        yy -= leading
    return yy


def draw_lines(c, lines, x, y, size=10, font="SimSun", color=TEXT, leading=14):
    set_font(c, font, size, color)
    yy = y
    for line in lines:
        c.drawString(x, yy, line)
        yy -= leading
    return yy


def draw_header(c, title: str, subtitle: str, page_no: int, total: int = 6) -> None:
    # Outer thin border.
    c.setStrokeColor(BLUE)
    c.setLineWidth(0.9)
    c.roundRect(10, 12, PAGE_W - 20, PAGE_H - 24, 8, stroke=1, fill=0)

    # Top electric-field style banner.
    rounded(c, 18, PAGE_H - 116, 140, 82, 8, stroke=BLUE, fill=colors.HexColor("#073B7A"), lw=1)
    c.setStrokeColor(colors.white)
    c.setLineWidth(0.5)
    cx, cy = 52, PAGE_H - 75
    for a in range(0, 360, 25):
        r = 38 + (a % 3) * 6
        x2 = cx + r * math.cos(math.radians(a))
        y2 = cy + r * math.sin(math.radians(a))
        c.line(cx, cy, x2, y2)
    set_font(c, "SimHei", 16, colors.white)
    c.drawCentredString(cx, cy - 5, "+")
    set_font(c, "SimHei", 9, colors.white)
    c.drawString(78, PAGE_H - 53, "Electric Field")
    c.drawString(78, PAGE_H - 68, "Chapter 06")

    # Main title box.
    rounded(c, 168, PAGE_H - 112, 286, 74, 4, stroke=BLUE, fill=colors.white, lw=1.2)
    set_font(c, "SimHei", 23, DEEP)
    c.drawCentredString(311, PAGE_H - 68, title)
    set_font(c, "SimSun", 11, GRAY)
    c.drawCentredString(311, PAGE_H - 90, subtitle)

    # Right decorative equipotential rings.
    rounded(c, 462, PAGE_H - 116, 114, 82, 8, stroke=BLUE, fill=PALE, lw=1)
    c.setStrokeColor(colors.HexColor("#8DBAF1"))
    for r in [10, 18, 26, 34]:
        c.circle(520, PAGE_H - 76, r, stroke=1, fill=0)
    set_font(c, "SimHei", 14, RED)
    c.drawCentredString(520, PAGE_H - 80, "+")
    set_font(c, "SimHei", 13, BLUE)
    c.drawCentredString(555, PAGE_H - 80, "-")

    # Divider line.
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.1)
    c.line(22, PAGE_H - 130, PAGE_W - 22, PAGE_H - 130)
    c.setFillColor(CYAN)
    c.circle(205, PAGE_H - 130, 2.2, fill=1, stroke=0)
    c.setFillColor(RED)
    c.rect(PAGE_W - 132, PAGE_H - 134, 86, 5, fill=1, stroke=0)
    set_font(c, "SimSun", 8, GRAY)
    c.drawRightString(PAGE_W - 25, 24, f"{page_no} / {total}｜第06章 静电场")


def title_bar(c, x, y, w, label, color=BLUE, icon="●"):
    c.setFillColor(color)
    c.roundRect(x, y, w, 22, 5, stroke=0, fill=1)
    set_font(c, "SimHei", 11, colors.white)
    c.drawString(x + 10, y + 6, label)


def problem_card(c, x, y, w, h, no, title, problem, options, tip, diagram=None, accent=BLUE):
    rounded(c, x, y, w, h, 6, stroke=accent, fill=colors.white, lw=1)
    title_bar(c, x, y + h - 24, w, f"{no}  {title}", accent, "◆")
    yy = y + h - 42
    yy = draw_text(c, problem, x + 10, yy, 9.2, "SimSun", TEXT, max_chars=max(16, int(w / 10)), leading=12)
    if diagram:
        diagram(c, x + w - 72, y + h - 100, 58, 48)
    set_font(c, "SimSun", 8.7, TEXT)
    for opt in options:
        c.drawString(x + 10, yy, opt)
        yy -= 12
    c.setStrokeColor(colors.HexColor("#BFD7F4"))
    c.line(x + 10, y + 31, x + w - 10, y + 31)
    draw_text(c, f"抓手：{tip}", x + 10, y + 20, 8.4, "SimHei", RED, max_chars=max(16, int(w / 9)), leading=10)


def answer_strip(c, answers: str, y=42):
    rounded(c, 22, y, PAGE_W - 44, 34, 6, stroke=BLUE, fill=colors.white, lw=1)
    set_font(c, "SimHei", 12, colors.white)
    c.setFillColor(DEEP)
    c.roundRect(34, y + 7, 112, 20, 4, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.drawString(44, y + 12, "答案区（仅题号）")
    set_font(c, "SimHei", 12, DEEP)
    c.drawString(165, y + 12, answers)


def minute_panel(c, x, y, w, h, title, items, accent=BLUE):
    rounded(c, x, y, w, h, 6, stroke=accent, fill=PALE, lw=0.9)
    title_bar(c, x, y + h - 24, w, title, accent, "◎")
    yy = y + h - 42
    for i, item in enumerate(items, 1):
        c.setFillColor(accent)
        c.circle(x + 15, yy + 3, 7, stroke=0, fill=1)
        set_font(c, "SimHei", 8.8, colors.white)
        c.drawCentredString(x + 15, yy, str(i))
        yy = draw_text(c, item, x + 29, yy + 3, 8.7, "SimSun", TEXT, max_chars=max(18, int((w - 45) / 8.7)), leading=11)
        yy -= 2


def draw_parallel(c, x, y, w, h):
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.2)
    c.line(x + 16, y + 8, x + 16, y + h - 8)
    c.line(x + w - 16, y + 8, x + w - 16, y + h - 8)
    set_font(c, "SimHei", 10, RED)
    c.drawString(x + 8, y + h - 16, "+")
    c.drawString(x + w - 23, y + h - 16, "+")
    c.setStrokeColor(RED)
    for yy in [y + 16, y + 26, y + 36]:
        c.line(x + 24, yy, x + w - 24, yy)
        c.line(x + w - 29, yy + 3, x + w - 24, yy)
        c.line(x + w - 29, yy - 3, x + w - 24, yy)


def draw_sphere(c, x, y, w, h):
    c.setStrokeColor(BLUE)
    c.circle(x + w / 2, y + h / 2, min(w, h) / 2 - 6, stroke=1, fill=0)
    c.setStrokeColor(colors.HexColor("#8DBAF1"))
    c.circle(x + w / 2, y + h / 2, min(w, h) / 2 - 16, stroke=1, fill=0)
    set_font(c, "SimHei", 12, RED)
    c.drawCentredString(x + w / 2, y + h / 2 - 4, "+")


def draw_conductor(c, x, y, w, h):
    c.setStrokeColor(BLUE)
    c.setFillColor(colors.HexColor("#E9F5FF"))
    c.ellipse(x + 8, y + 9, x + w - 8, y + h - 9, stroke=1, fill=1)
    set_font(c, "SimHei", 8, RED)
    for px, py in [(x + 18, y + 17), (x + w - 22, y + 20), (x + 26, y + h - 20), (x + w - 28, y + h - 17)]:
        c.drawString(px, py, "+")
    set_font(c, "SimSun", 8, DEEP)
    c.drawCentredString(x + w / 2, y + h / 2 - 3, "E=0")


def draw_dipole(c, x, y, w, h):
    set_font(c, "SimHei", 13, RED)
    c.drawCentredString(x + 15, y + h / 2, "+")
    set_font(c, "SimHei", 13, BLUE)
    c.drawCentredString(x + w - 15, y + h / 2, "-")
    c.setStrokeColor(colors.HexColor("#8DBAF1"))
    for off in [-16, -8, 0, 8, 16]:
        c.bezier(x + 18, y + h / 2 + off, x + 35, y + h + off / 2, x + w - 35, y + h + off / 2, x + w - 18, y + h / 2 + off)
        c.bezier(x + 18, y + h / 2 + off, x + 35, y - off / 2, x + w - 35, y - off / 2, x + w - 18, y + h / 2 + off)


def page1(c):
    draw_header(c, "第六章 静电场", "思维导图｜从“场”到“题型”的一小时路线", 1)
    # Left panels.
    rounded(c, 18, 592, 140, 100, 6, stroke=BLUE, fill=colors.white)
    title_bar(c, 18, 670, 140, "本章物理图像", BLUE, "✦")
    draw_text(c, "电荷在空间建立电场；试探电荷只是用来读出这个场的强弱和方向。", 30, 650, 8.3, max_chars=14, leading=11)
    draw_dipole(c, 45, 600, 88, 34)

    minute_panel(c, 18, 392, 140, 178, "易混辨析", [
        "电场强度 E 是矢量，电势 U 是标量。",
        "电通量不是场强；通量看穿过面积的总效果。",
        "高斯定理永远成立，但只在高对称时好算 E。",
        "导体静电平衡：内部 E=0，不是外部 E=0。"
    ], RED)
    rounded(c, 18, 272, 140, 100, 6, stroke=CYAN, fill=colors.white)
    title_bar(c, 18, 350, 140, "前后联系", CYAN, "↔")
    draw_text(c, "前接：库仑力、矢量叠加。后接：电流、磁场、电磁感应。电容/导体题会直接服务电路分析。", 30, 330, 9, max_chars=17, leading=12)

    # Mind map.
    rounded(c, 170, 270, 405, 422, 8, stroke=BLUE, fill=colors.white, lw=1.1)
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.2)
    c.circle(372, 486, 48, stroke=1, fill=0)
    set_font(c, "SimHei", 14, DEEP)
    c.drawCentredString(372, 494, "静电场")
    c.drawCentredString(372, 476, "做题地图")
    branches = [
        ("场强叠加", "点电荷/连续体积分", 250, 630),
        ("高斯定理", "球/柱/面对称", 470, 630),
        ("电势与做功", "U 标量先算", 245, 520),
        ("导体平衡", "内部 E=0 表面等势", 480, 520),
        ("电介质与D", "有介质用 D 分流", 250, 405),
        ("电容能量", "C=Q/U, W=CU^2/2", 475, 405),
    ]
    for a, b, bx, by in branches:
        c.setStrokeColor(BLUE)
        c.line(372, 486, bx, by)
        rounded(c, bx - 58, by - 18, 116, 36, 10, stroke=colors.HexColor("#99BFF0"), fill=PALE)
        set_font(c, "SimHei", 9.5, DEEP)
        c.drawCentredString(bx, by + 4, a)
        set_font(c, "SimSun", 7.6, GRAY)
        c.drawCentredString(bx, by - 9, b)
    draw_dipole(c, 315, 300, 120, 58)

    problem_card(c, 18, 112, 176, 132, "Q1", "判断", "高斯面上各点场强大小相等，就一定能把 E 提出积分号。（ ）",
                 ["A. 对", "B. 错"], "还要方向与 dS 关系固定。", draw_sphere, BLUE)
    problem_card(c, 210, 112, 176, 132, "Q2", "选择", "电势为零的点，电场强度一定为零。（ ）",
                 ["A. 对", "B. 错"], "U 是人为选零，E 看空间变化率。", None, CYAN)
    problem_card(c, 402, 112, 176, 132, "Q3", "判断", "静电平衡导体表面一定是等势面。（ ）",
                 ["A. 对", "B. 错"], "否则表面自由电荷还会运动。", draw_conductor, BLUE)
    answer_strip(c, "Q1【B】  Q2【B】  Q3【A】")


def page2(c):
    draw_header(c, "高斯定理小题速通", "只在“对称性足够强”时把积分题变成代数题", 2)
    problem_card(c, 22, 590, 176, 142, "1", "无限大平面", "无限大均匀带电平面，面密度为 σ，单侧电场强度大小为（ ）",
                 ["A. 0", "B. σ/(2ε0)", "C. σ/ε0", "D. σ/(4π ε0)"], "单平面双侧分场：E=σ/(2ε0)。", draw_parallel, BLUE)
    problem_card(c, 210, 590, 176, 142, "2", "两平面叠加", "两无限大平面均带 +σ，在两板之间的合场大小为（ ）",
                 ["A. 0", "B. σ/(2ε0)", "C. σ/ε0", "D. 2σ/ε0"], "方向相反抵消；外侧相加。", draw_parallel, CYAN)
    problem_card(c, 398, 590, 176, 142, "3", "球面对称", "均匀带电球壳内任一点的电场强度为（ ）",
                 ["A. 0", "B. kQ/r^2", "C. kQr/R^3", "D. 不能确定"], "壳内包围电荷为零，E=0。", draw_sphere, BLUE)

    minute_panel(c, 22, 365, 552, 194, "1 分钟抓手：高斯题四步", [
        "看对称：球对称、柱对称、面对称才优先高斯。",
        "选高斯面：球面/柱面/盒面，让 E 大小恒定或通量为零。",
        "写通量：ΦE=∮E·dS，不要把 E 和 ΦE 混成一个量。",
        "写包围电荷：只数高斯面内部，外部电荷不进 q_in。",
        "代数求 E：如果 E 不能提出积分号，就换积分法或叠加法。"
    ])
    minute_panel(c, 22, 152, 266, 176, "易错点", [
        "高斯定理成立 ≠ 高斯法好算。",
        "球壳内 E=0，但电势通常不为零。",
        "无限大平面单侧是 σ/(2ε0)，导体表面外侧才常见 σ/ε0。",
        "两平面中间还是外侧，先画方向箭头再相加。"
    ], RED)
    minute_panel(c, 308, 152, 266, 176, "本页题型模板", [
        "看到“无限大平面”：直接先写单面场，再叠加方向。",
        "看到“均匀球壳”：分 r<R 与 r>R。",
        "看到“均匀球体”：球内 E 正比于 r，球外像点电荷。",
        "看到“通量”：先判断问的是 Φ 还是 E。"
    ], CYAN)
    answer_strip(c, "1【B】  2【A】  3【A】")


def page3(c):
    draw_header(c, "场强叠加与连续带电体", "先取 dq，再决定算 dE 还是 dU", 3)
    problem_card(c, 22, 594, 176, 138, "4", "点电荷叠加", "正方形四顶点放等量同号电荷，中心 O 点场强大小为（ ）",
                 ["A. 0", "B. 4kq/a^2", "C. kq/a^2", "D. 方向不定"], "先看对称抵消，别急着套公式。", draw_sphere, BLUE)
    problem_card(c, 210, 594, 176, 138, "5", "半圆弧带电", "半径 R 的均匀带电半圆弧，圆心处场强方向应沿（ ）",
                 ["A. 直径方向", "B. 切线方向", "C. 垂直纸面", "D. 无法判断"], "对称分量抵消，保留轴向分量。", None, CYAN)
    problem_card(c, 398, 594, 176, 138, "6", "积分策略", "连续带电体求某点电势，通常比求场强更容易，因为电势是（ ）",
                 ["A. 矢量", "B. 标量", "C. 张量", "D. 方向量"], "U 直接标量相加，少做分量。", draw_dipole, BLUE)

    minute_panel(c, 22, 370, 552, 184, "1 分钟抓手：连续体积分", [
        "取元：线电荷 dq=λdl，面电荷 dq=σdS，体电荷 dq=ρdV。",
        "求场强：dE=k dq/r^2，必须拆分量，利用对称性消掉一部分。",
        "求电势：dU=k dq/r，标量直接积分；最后再由 E=-grad U 求场也行。",
        "常见几何：圆环轴线、半圆弧圆心、均匀线段延长线/垂直平分线。"
    ])
    rounded(c, 22, 145, 552, 186, 8, stroke=BLUE, fill=colors.white)
    title_bar(c, 22, 309, 552, "大题模板：半圆弧/圆环类", BLUE, "▣")
    draw_text(c, "标准步骤：① 画对称轴；② 取电荷元 dq；③ 写 dE 的大小；④ 拆成 dEx、dEy；⑤ 判断哪一项积分为零；⑥ 统一变量积分。", 40, 288, 10, max_chars=48, leading=14)
    draw_text(c, "半圆弧圆心：左右分量抵消，轴向分量累加；整圆圆心：所有方向完全抵消，E=0。", 40, 238, 10, font="SimHei", color=RED, max_chars=48, leading=14)
    draw_text(c, "判断题：连续带电体求电势时也必须先把矢量拆成 x、y 分量。（ ）", 40, 192, 10, max_chars=45, leading=14)
    answer_strip(c, "4【A】  5【A】  6【B】  判断【错】")


def page4(c):
    draw_header(c, "电势、做功与等势面", "标量先行：能用 U 的题不要硬拆 E", 4)
    problem_card(c, 22, 594, 176, 138, "7", "电势零点", "某点电势 U=0，则该点电势能一定为零吗？（ ）",
                 ["A. 一定", "B. 不一定", "C. 与电荷无关", "D. 只和路径有关"], "Ep=qU；U 的零点可选，Ep 也随之变。", None, BLUE)
    problem_card(c, 210, 594, 176, 138, "8", "做功符号", "电场力把正电荷从 A 移到 B，若 UA>UB，则电场力做功（ ）",
                 ["A. 正", "B. 负", "C. 零", "D. 无法判断"], "W=q(UA-UB)，正电荷从高势到低势做正功。", draw_dipole, CYAN)
    problem_card(c, 398, 594, 176, 138, "9", "E 与 U", "场强方向总是沿电势（ ）最快的方向。",
                 ["A. 升高", "B. 降低", "C. 不变", "D. 任意"], "E=-grad U，负号就是方向信息。", draw_sphere, BLUE)

    minute_panel(c, 22, 370, 552, 184, "1 分钟抓手：电势题", [
        "电势 U：单位正电荷的电势能，标量，可选零点。",
        "电势差：UA-UB 与零点无关，才是做功题真正要用的量。",
        "电场力做功：WAB=q(UA-UB)，路径无关。",
        "等势面：沿等势面移动电荷，电场力做功为 0；E 垂直等势面。",
        "由 U 求 E：Ex=-dU/dx，Ey=-dU/dy，符号最容易错。"
    ])
    rounded(c, 22, 145, 552, 186, 8, stroke=CYAN, fill=colors.white)
    title_bar(c, 22, 309, 552, "概念辨析：电势 vs 电势能", CYAN, "◇")
    draw_text(c, "教材口径：电势是场本身在空间点的性质；电势能是某个电荷放在该点后具有的能量。", 40, 286, 10, max_chars=50, leading=14)
    draw_text(c, "一句话区分：U 不带测试电荷 q 的身份，Ep=qU 带 q 的正负和大小。", 40, 246, 10, font="SimHei", color=RED, max_chars=48, leading=14)
    draw_text(c, "自测：负电荷从低电势点移到高电势点，电势能一定增大。（ ）", 40, 206, 10, max_chars=46, leading=14)
    answer_strip(c, "7【B】  8【A】  9【B】  自测【错】")


def page5(c):
    draw_header(c, "导体、电容与能量", "静电平衡题先写三句话，再算球壳/电容", 5)
    problem_card(c, 22, 594, 176, 138, "10", "导体内部", "静电平衡导体内部任一点场强为（ ）",
                 ["A. 0", "B. σ/ε0", "C. kQ/r^2", "D. 与形状有关"], "自由电荷不再定向运动的条件。", draw_conductor, BLUE)
    problem_card(c, 210, 594, 176, 138, "11", "导体表面", "静电平衡导体表面附近电场方向应（ ）导体表面。",
                 ["A. 平行", "B. 垂直", "C. 任意", "D. 沿切线"], "若有切向分量，表面电荷会继续移动。", draw_conductor, CYAN)
    problem_card(c, 398, 594, 176, 138, "12", "电容定义", "孤立导体或电容器的电容主要由（ ）决定。",
                 ["A. 几何与介质", "B. 是否带电", "C. 电荷量", "D. 电势大小"], "C=Q/U 是定义，不是说 C 随 Q 变。", None, BLUE)

    minute_panel(c, 22, 370, 552, 184, "1 分钟抓手：导体静电平衡", [
        "三句话：导体内部 E=0；导体整体等势；净电荷分布在外表面。",
        "空腔无内电荷：腔内 E=0；空腔有电荷：内表面感应等量异号电荷。",
        "导体表面外侧：E 垂直表面；尖端曲率大，面电荷密度更大。",
        "球壳题分区：先按半径分 r，再逐区用高斯定理或电势连续。"
    ])
    rounded(c, 22, 145, 552, 186, 8, stroke=BLUE, fill=colors.white)
    title_bar(c, 22, 309, 552, "计算模板：同心导体球壳", BLUE, "▣")
    draw_text(c, "识别信号：出现 R1、R2、R3，多层球壳，求不同区域 E 或 U。", 40, 288, 10, max_chars=50, leading=14)
    draw_text(c, "标准动作：① 分区；② 每区画高斯面；③ 写 q_in；④ 求 E(r)；⑤ 由 U=∫E dr 并保证边界电势连续。", 40, 250, 10, max_chars=50, leading=14)
    draw_text(c, "判断题：导体处于静电平衡时，导体表面电势处处相等。（ ）", 40, 202, 10, max_chars=48, leading=14)
    answer_strip(c, "10【A】  11【B】  12【A】  判断【对】")


def page6(c):
    draw_header(c, "考前 A4 速查 + 答案附页", "公式条件、题型触发、最后 1 分钟复盘", 6)
    rounded(c, 22, 568, 552, 164, 8, stroke=BLUE, fill=colors.white)
    title_bar(c, 22, 710, 552, "公式速查：只背带条件的公式", BLUE, "▣")
    formulas = [
        ("库仑场", "E=kq/r^2；方向看 q 正负"),
        ("高斯定理", "∮E·dS=q_in/ε0；先看对称"),
        ("无限大平面", "E=σ/(2ε0)；两平面画方向"),
        ("电势", "U=kq/r；WAB=q(UA-UB)"),
        ("场势关系", "E=-grad U；Ex=-dU/dx"),
        ("导体平衡", "内部 E=0；表面等势"),
        ("电容", "C=Q/U；平行板 C=εS/d"),
        ("能量", "W=Q^2/(2C)=CU^2/2=QU/2"),
    ]
    x1, y = 40, 686
    for i, (name, form) in enumerate(formulas):
        col = i % 2
        row = i // 2
        x = x1 + col * 270
        yy = y - row * 30
        set_font(c, "SimHei", 9.5, DEEP)
        c.drawString(x, yy, name)
        set_font(c, "SimSun", 8.2, TEXT)
        c.drawString(x + 68, yy, form)

    problem_card(c, 22, 392, 176, 140, "13", "最后判断", "若电场强度处处为零，则该区域内电势一定处处相等。（ ）",
                 ["A. 对", "B. 错"], "E=-grad U，梯度为零则 U 为常量。", None, BLUE)
    problem_card(c, 210, 392, 176, 140, "14", "最后选择", "均匀带电球体内部电场强度随 r 的关系是（ ）",
                 ["A. E 正比于 r", "B. E 正比于 1/r^2", "C. E=0", "D. E 正比于 r^2"], "球内 q_in∝r^3，除以 r^2 后 E∝r。", draw_sphere, CYAN)
    problem_card(c, 398, 392, 176, 140, "15", "最后填空", "沿等势面移动电荷时，电场力做功为 ______。",
                 ["A. 0", "B. qU", "C. qE", "D. 不确定"], "等势面上 ΔU=0，所以 W=0。", draw_dipole, BLUE)

    minute_panel(c, 22, 190, 266, 166, "计算题四模板", [
        "点电荷组：先矢量图，再分量相加。",
        "连续带电体：dq -> dE/dU -> 对称性积分。",
        "高斯题：对称性 -> 高斯面 -> q_in -> E。",
        "导体球壳：分区求 E，再积分求 U。"
    ], BLUE)
    minute_panel(c, 308, 190, 266, 166, "答案附页", [
        "Q1 B；Q2 B；Q3 A；1 B；2 A；3 A。",
        "4 A；5 A；6 B；7 B；8 A；9 B。",
        "10 A；11 B；12 A；13 A；14 A；15 A。",
        "关键判断：电势零不代表场强零；导体内部 E=0。"
    ], RED)
    answer_strip(c, "13【A】  14【A】  15【A】")


def build_pdf() -> Path:
    register_fonts()
    c = canvas.Canvas(str(PDF_PATH), pagesize=A4)
    for fn in [page1, page2, page3, page4, page5, page6]:
        fn(c)
        c.showPage()
    c.save()
    return PDF_PATH


if __name__ == "__main__":
    print(build_pdf())
