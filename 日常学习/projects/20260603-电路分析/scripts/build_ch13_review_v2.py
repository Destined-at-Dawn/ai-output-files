from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont, JpegImagePlugin


ROOT = Path(r"E:\ai产出文件\牛马\日常学习\projects\20260603-电路分析")
OUT = ROOT / "outputs" / "第13章_非正弦周期电流电路_复习PDF"
PAGES = OUT / "pages_v2"
PDF = OUT / "第13章_非正弦周期电流电路_复习PDF_v2.pdf"
PACK = OUT / "source_pack_v2.md"

W, H = 1055, 1491
M = 38
PURPLE = (96, 35, 142)
PURPLE_2 = (137, 80, 190)
LIGHT = (250, 246, 255)
RED = (210, 0, 0)
YELLOW = (222, 150, 0)
BLACK = (28, 24, 31)
GRAY = (92, 82, 105)
LINE = (169, 113, 217)

FONT_DIR = Path(r"C:\Windows\Fonts")
FONT_REG = FONT_DIR / "Noto Sans SC (TrueType).otf"
FONT_MED = FONT_DIR / "Noto Sans SC Medium (TrueType).otf"
FONT_BOLD = FONT_DIR / "Noto Sans SC Bold (TrueType).otf"
if not FONT_REG.exists():
    FONT_REG = FONT_DIR / "msyh.ttc"
    FONT_MED = FONT_DIR / "msyhbd.ttc"
    FONT_BOLD = FONT_DIR / "msyhbd.ttc"


def font(size, bold=False, medium=False):
    fp = FONT_BOLD if bold else FONT_MED if medium else FONT_REG
    return ImageFont.truetype(str(fp), size)


F = {
    "title": font(48, bold=True),
    "subtitle": font(25, medium=True),
    "h": font(28, bold=True),
    "tag": font(25, bold=True),
    "body": font(21),
    "bodyb": font(21, bold=True),
    "small": font(17),
    "smallb": font(17, bold=True),
    "tiny": font(14),
    "formula": font(20),
}


def text_w(draw, text, f):
    return draw.textbbox((0, 0), text, font=f)[2]


def line_h(f, extra=7):
    box = f.getbbox("国")
    return box[3] - box[1] + extra


def wrap(draw, text, f, max_w):
    lines = []
    for para in str(text).split("\n"):
        if not para:
            lines.append("")
            continue
        cur = ""
        for ch in para:
            if text_w(draw, cur + ch, f) <= max_w:
                cur += ch
            else:
                if cur:
                    lines.append(cur)
                cur = ch
        if cur:
            lines.append(cur)
    return lines


def draw_wrapped(draw, text, xy, f, max_w, fill=BLACK, spacing=7):
    x, y = xy
    for ln in wrap(draw, text, f, max_w):
        draw.text((x, y), ln, font=f, fill=fill)
        y += line_h(f, spacing)
    return y


def new_page(title, subtitle, page_no, total=8):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    tw = text_w(d, title, F["title"])
    d.text(((W - tw) / 2, 30), title, font=F["title"], fill=PURPLE)
    sw = text_w(d, subtitle, F["subtitle"])
    d.text(((W - sw) / 2, 92), subtitle, font=F["subtitle"], fill=RED)
    d.line((M, H - 58, W - M, H - 58), fill=PURPLE, width=2)
    foot = f"{page_no} / {total}"
    d.text(((W - text_w(d, foot, F['body'])) / 2, H - 42), foot, font=F["body"], fill=PURPLE)
    d.text((W - 330, H - 40), "source-first exam mode", font=F["small"], fill=PURPLE)
    return img, d


def tag(d, x, y, text, color=PURPLE):
    w = text_w(d, text, F["tag"]) + 28
    d.rounded_rectangle((x, y, x + w, y + 48), radius=7, fill=color)
    d.text((x + 14, y + 8), text, font=F["tag"], fill="white")
    return x + w, y + 58


def card(d, x, y, w, h, title=None, core=False):
    d.rounded_rectangle((x, y, x + w, y + h), radius=9, fill=LIGHT, outline=LINE, width=2)
    if title:
        d.text((x + 18, y + 12), title, font=F["h"], fill=PURPLE)
    if core:
        cx = x + w - 52
        cy = y + 28
        d.ellipse((cx, cy, cx + 25, cy + 25), fill=RED)
        d.text((cx + 33, cy - 2), "核心", font=F["smallb"], fill=RED)


def table(d, x, y, w, rows, col1=160, row_h=86, core_rows=None):
    core_rows = set(core_rows or [])
    total_h = row_h * len(rows)
    d.rounded_rectangle((x, y, x + w, y + total_h), radius=8, fill="white", outline=LINE, width=2)
    for i, (k, v) in enumerate(rows):
        yy = y + i * row_h
        if i > 0:
            d.line((x, yy, x + w, yy), fill=LINE, width=1)
        d.line((x + col1, yy, x + col1, yy + row_h), fill=LINE, width=1)
        d.text((x + 18, yy + 17), k, font=F["bodyb"], fill=PURPLE)
        reserve = 112 if i in core_rows else 0
        draw_wrapped(d, v, (x + col1 + 18, yy + 15), F["body"], w - col1 - 42 - reserve)
        if i in core_rows:
            cx = x + w - 82
            cy = yy + 21
            d.ellipse((cx, cy, cx + 22, cy + 22), fill=RED)
            d.text((cx + 30, cy - 2), "核心", font=F["smallb"], fill=RED)
    return y + total_h


def bullets(d, x, y, items, max_w, size="body", color=BLACK, gap=6):
    f = F[size]
    for item in items:
        d.text((x, y), ">", font=f, fill=PURPLE)
        y = draw_wrapped(d, item, (x + 28, y), f, max_w - 28, fill=color, spacing=gap)
        y += 4
    return y


def two_col_cards(d, y, cards):
    x1, x2 = M, W // 2 + 10
    cw, ch = W // 2 - 55, 150
    for i, (num, title, desc, src) in enumerate(cards):
        x = x1 if i % 2 == 0 else x2
        yy = y + (i // 2) * (ch + 18)
        card(d, x, yy, cw, ch)
        d.ellipse((x + 18, yy + 24, x + 58, yy + 64), fill=PURPLE)
        d.text((x + 32, yy + 28), str(num), font=F["bodyb"], fill="white")
        d.text((x + 76, yy + 21), title, font=F["h"], fill=PURPLE)
        draw_wrapped(d, desc, (x + 76, yy + 59), F["body"], cw - 96, fill=BLACK, spacing=4)
        d.text((x + 76, yy + 118), src, font=F["small"], fill=GRAY)
    return y + 2 * (ch + 18)


def source_box(d, y, text):
    tag(d, M, y, "引用来源")
    y += 58
    table(d, M, y, W - 2 * M, [("Source", text)], col1=150, row_h=76)
    return y + 92


def page1():
    img, d = new_page("第13章：非正弦周期电流电路", "先分频，再逐频率计算，最后按规则合成。", 1)
    y = 135
    tag(d, M, y, "0. 本章总图")
    y += 62
    y = two_col_cards(d, y, [
        (1, "傅里叶分解", "把非正弦周期量拆成直流、基波、各次谐波。", "教材13-1~13-2"),
        (2, "频谱与对称", "看幅度、相位、奇偶/半波对称，判断哪些项存在。", "教材13-1~13-3"),
        (3, "有效值与功率", "有效值平方相加；功率只算直流与同频项。", "教材13-4 + 学校小题"),
        (4, "分频率计算", "直流、ω、kω分别画等效电路，再合成答案。", "教材13-4"),
    ])
    y += 18
    tag(d, M, y, "13.0 原题复现路线")
    y += 60
    y = table(d, M, y, W - 2 * M, [
        ("主体来源", "只用教材13-1到13-4做主体。教材主体占比100%；学校/PPT题单独放最后附加题。"),
        ("考试边界", "第13章只到13-4；13-5及以后不进入主体复习页，只作降权参考。"),
        ("做题口令", "拆频率 -> 单频等效 -> 分别计算 -> 有效值平方和 / 功率同频加。"),
        ("高频提醒", "不同频率不能直接相量相加；有效值不看初相；平均功率不跨频相乘。"),
    ], col1=150, row_h=84, core_rows=[0, 3])
    source_box(d, 1060, "教材：shared\\教材\\电路_邱关源_内嵌教材.pdf#pdfpage=359-360/题13-1~13-4；考试边界：shared\\CODEX_电路期末资料整理指令.md#第13章只考到13-4")
    return img


def page2():
    img, d = new_page("13.1 傅里叶分解与频谱", "核心目标：看懂一个非正弦量由哪些频率组成。", 2)
    y = 132
    tag(d, M, y, "13.1 核心公式")
    y += 62
    y = table(d, M, y, W - 2 * M, [
        ("是什么", "周期非正弦量 = 直流分量 + 基波 + 高次谐波。频谱就是把每个频率的幅值和相位列出来。"),
        ("常用式", "f(t)=A0 + Σ Akm cos(kω1t + φk)。也可写成 ak cos(kω1t)+bk sin(kω1t)。"),
        ("怎么考", "教材13-1：给函数或波形，求频谱函数并画频谱图。教材13-2：平移、反折、取负、微分后频谱怎么变。"),
        ("易错点", "时间平移改变相位，不改变幅值；反折改变相位符号；微分会让第k次谐波幅值乘kω1。"),
    ], col1=150, row_h=94, core_rows=[1])
    y += 28
    tag(d, M, y, "原题抓手")
    y += 60
    y = table(d, M, y, W - 2 * M, [
        ("教材13-1", "看到 cos4t+sin6t：先找基波角频率，再把每一项写成幅值+相位，最后画离散谱线。"),
        ("教材13-2", "频谱变换题不重新积分，直接用性质：延时乘相位因子；取负整体乘-1；微分乘jkω1。"),
        ("训练目标", "会从时域表达式直接报出：直流项、基波、谐波次数、幅值、相位。"),
    ], col1=150, row_h=92)
    y += 26
    tag(d, M, y, "30秒判断")
    y += 58
    bullets(d, M + 16, y, [
        "只要题目问“频谱/频谱图/谐波次数”，先别碰电路，先拆成 A0、1ω、2ω、3ω……",
        "如果是波形图，先看周期T和对称性，再决定哪些 ak、bk 必为0。",
    ], W - 2 * M - 30)
    source_box(d, 1160, "教材：shared\\教材\\电路_邱关源_内嵌教材.pdf#pdfpage=359/书页=340/题13-1,13-2；答案：pdfpage=574/书页=555")
    return img


def page3():
    img, d = new_page("13.2 波形对称性与谐波保留", "核心目标：不用积分，先判断哪些谱线一定为零。", 3)
    y = 132
    tag(d, M, y, "13.2 判断规则")
    y += 62
    y = table(d, M, y, W - 2 * M, [
        ("直流项", "a0=0 代表平均值为0；波形关于时间轴正负面积抵消。"),
        ("偶函数", "若波形关于纵轴对称，通常只含余弦项，bk=0。"),
        ("奇函数", "若波形关于原点对称，通常只含正弦项，ak=0。"),
        ("半波对称", "f(t+T/2)=-f(t) 时，偶次谐波消失，只剩奇次谐波。"),
    ], col1=150, row_h=90, core_rows=[3])
    y += 28
    tag(d, M, y, "教材13-3怎么抓")
    y += 60
    y = table(d, M, y, W - 2 * M, [
        ("题目动作", "给出题13-3的原波形，再分别附加条件：a0=0、bk=0、ak=0、偶数k项为零，要求画完整周期波形。"),
        ("解题顺序", "先画一个周期骨架 -> 套条件改造对称性 -> 检查周期延拓是否连续/符合题图。"),
        ("扣分点", "把“偶次谐波为零”误认为“偶函数”；把“bk=0”误认为“没有正弦波形”。"),
    ], col1=150, row_h=92, core_rows=[2])
    y += 28
    card(d, M, y, W - 2 * M, 190, "记忆钩子", core=True)
    bullets(d, M + 20, y + 56, [
        "a0管平均值；ak/bk管余弦/正弦；奇偶次管频率序号。",
        "对称性题的本质不是算数，是“哪些项不能出现”。",
        "如果不确定，先写出 f(t+T/2) 与 -f(t) 比较，这是半波对称最快检验。",
    ], W - 2 * M - 44, size="body")
    source_box(d, 1160, "教材：shared\\教材\\电路_邱关源_内嵌教材.pdf#pdfpage=360/书页=341/题13-3")
    return img


def page4():
    img, d = new_page("13.3 有效值、平均值、平均功率", "核心目标：会合成读数，会判断哪些项对功率有贡献。", 4)
    y = 132
    tag(d, M, y, "13.3 核心公式")
    y += 62
    y = table(d, M, y, W - 2 * M, [
        ("有效值", "X = sqrt(X0^2 + X1^2 + X2^2 + ...)。不同频率正交，平方相加再开方。"),
        ("同频先合", "同一频率、不同初相的项，必须先按相量合并，再参与有效值平方和。"),
        ("平均功率", "P = U0I0 + Σ Uk Ik cos(φuk-φik)。只加直流功率和同频项功率。"),
        ("平均值", "一个周期平均值只看直流分量；纯正弦及各次谐波平均值为0。"),
    ], col1=150, row_h=94, core_rows=[0, 2])
    y += 26
    tag(d, M, y, "小题秒杀")
    y += 60
    y = table(d, M, y, W - 2 * M, [
        ("判断", "“有效值与初相有关”是错；初相影响同频合并，不影响单个正弦项有效值。"),
        ("选择", "i1=4sqrt(2)sin10t、i2=3sqrt(2)sin20t，则i3有效值=sqrt(4^2+3^2)=5A。"),
        ("填空", "u、i含直流/基波/高次时，平均功率只拿同频项配对，学校填空答案P=60W。"),
    ], col1=150, row_h=92)
    y += 28
    card(d, M, y, W - 2 * M, 150, "核心提醒", core=True)
    bullets(d, M + 22, y + 58, [
        "“同频”是能不能相量合并、能不能算功率交叉项的唯一门槛。",
        "表读数通常是有效值，所以最后要平方和，不是瞬时值相加。",
    ], W - 2 * M - 60)
    source_box(d, 1170, "PPT：第13章 非正弦周期电流电路和信号的频谱.pdf#page=21-23；学校作业：第13章 非正弦周期电流电路-学生作业修改.pdf#page=1-2；答案：第十三章习题答案-有删减.pdf#page=1-2")
    return img


def page5():
    img, d = new_page("13.4 非正弦电路大题模板", "核心目标：把一道题写成阅卷老师认的标准格式。", 5)
    y = 132
    tag(d, M, y, "闭卷标准步骤")
    y += 62
    y = table(d, M, y, W - 2 * M, [
        ("1 拆激励", "把u(t)或i(t)写成：直流分量 + 基波分量 + k次谐波分量。每一项单独标频率。"),
        ("2 画等效", "直流：L短路、C开路；kω：ZL=jkωL，ZC=1/(jkωC)。不同k必须分别算。"),
        ("3 求分量", "对每个频率用相量法求 Ik、Uk；最后还原为对应频率的瞬时正弦项。"),
        ("4 合成结果", "瞬时量可按时间函数直接相加；有效值按平方和；平均功率只加同频项。"),
        ("5 写Source", "答案参考学校解析风格：分“直流/基波/k次谐波”列小标题，最后统一合成。"),
    ], col1=145, row_h=92, core_rows=[1, 3])
    y += 25
    tag(d, M, y, "一眼识别")
    y += 58
    y = bullets(d, M + 16, y, [
        "题中出现 f(t)、方波/三角波、sinωt+sin3ωt、有效值、平均功率，就是第13章模板。",
        "题中出现RLC串联/并联、谐振、滤波，优先怀疑第11章+第13章综合。",
        "题中出现电流表/电压表读数，默认问有效值；别用瞬时值直接代。",
    ], W - 2 * M - 30)
    y += 22
    card(d, M, y, W - 2 * M, 134, "答题版式", core=True)
    draw_wrapped(d, "建议每道大题固定写：① 分解激励；② 各频率等效电路；③ 各频率相量计算；④ 合成 i(t)/u(t)；⑤ 计算有效值或P。", (M + 22, y + 58), F["body"], W - 2 * M - 70)
    source_box(d, 1170, "教材：shared\\教材\\电路_邱关源_内嵌教材.pdf#pdfpage=360/题13-4；学校答案：第十三章习题答案-有删减.pdf#page=3-7")
    return img


def page6():
    img, d = new_page("教材13-4：标准大题展开", "核心目标：用教材原题校准第13章计算题书写。", 6)
    y = 132
    tag(d, M, y, "题设抓取")
    y += 62
    y = table(d, M, y, W - 2 * M, [
        ("原题", "RLC串联，R=1Ω，ω1L=10Ω，1/(ω1C)=90Ω；外加电压 us(t)=f(t-T/2)+Um/2，Um=100V，ω1=10rad/s。求 i(t) 与电路消耗功率。"),
        ("考点", "非正弦激励分解 + 串联RLC不同频率阻抗 + 平均功率。"),
    ], col1=130, row_h=96, core_rows=[0])
    y += 24
    tag(d, M, y, "标准书写骨架")
    y += 58
    y = table(d, M, y, W - 2 * M, [
        ("第1步", "由题13-1(b)及平移项写出 us(t) 的各次谐波分量；列出10t、20t、30t、40t等分量。"),
        ("第2步", "分别计算 Zk = R + jkω1L - j/(kω1C)。注意k变，感抗和容抗都变。"),
        ("第3步", "逐项求 Ik = Uk / Zk，并把相量结果还原为 sin(kω1t+φk)。"),
        ("第4步", "功率只由电阻消耗：P = Σ Ik^2 R。教材答案 P=56.69W。"),
    ], col1=130, row_h=92)
    y += 24
    tag(d, M, y, "教材答案核对")
    y += 58
    card(d, M, y, W - 2 * M, 205, "答案形态", core=True)
    ans = "i(t)=[-0.4sin(10t+89.28°)-0.636sin(20t+87.71°)-10.61sin(30t)-0.454sin(40t-86.73°)] A；P=56.69W。"
    draw_wrapped(d, ans, (M + 20, y + 58), F["formula"], W - 2 * M - 64, fill=BLACK)
    draw_wrapped(d, "得分关键不是背这个答案，而是能把每个频率分开算；闭卷时先写模板，再带数。", (M + 20, y + 122), F["body"], W - 2 * M - 64, fill=RED)
    source_box(d, 1170, "教材题目：shared\\教材\\电路_邱关源_内嵌教材.pdf#pdfpage=360/书页=341/题13-4；教材答案：pdfpage=574/书页=555/13-4")
    return img


def page7():
    img, d = new_page("附加题：学校资料与PPT例题", "定位：最后冲刺使用，参考学校答案的标准书写格式。", 7)
    y = 132
    tag(d, M, y, "附加题怎么用")
    y += 62
    y = table(d, M, y, W - 2 * M, [
        ("学校小题", "判断：有效值与初相有关？错。不同频率电压能写成一个相量？错。"),
        ("学校选择", "i1=4sqrt(2)sin10t，i2=3sqrt(2)sin20t，i3有效值=5A。"),
        ("同频合并", "30sqrt(2)sinωt + 两个80sqrt(2)三次项 + 30sqrt(2)cos5ωt，先合并同频三次项，答案U=90.55V。"),
        ("学校填空", "u含直流/基波/高次，i含直流/基波/高次，平均功率只取直流与同频基波项，答案P=60W。"),
        ("PPT例题", "PPT page=28-41主要校准方法：分频率激励、有效值读数、滤波/仪表题。"),
    ], col1=145, row_h=92, core_rows=[0, 3])
    y += 24
    tag(d, M, y, "附加题入口")
    y += 58
    card(d, M, y, W - 2 * M, 250, "最后一天只练这三类", core=True)
    bullets(d, M + 20, y + 58, [
        "判断/选择：只练“不同频率不能相量相加、有效值不看初相、同频先合并”。",
        "填空：只练平均功率P，先圈出u和i里频率相同的项。",
        "大题：只看学校答案格式，学习“直流、基波、k次谐波分栏计算”。",
    ], W - 2 * M - 64)
    source_box(d, 1170, "学校作业：第13章 非正弦周期电流电路-学生作业修改.pdf#page=1-3；答案：第十三章习题答案-有删减.pdf#page=1-7；PPT：第13章 非正弦周期电流电路和信号的频谱.pdf#page=28-41")
    return img


def page8():
    img, d = new_page("第13章考前错题卡", "核心目标：闭卷时少犯低级错，计算题拿步骤分。", 8)
    y = 132
    tag(d, M, y, "看到什么 -> 先做什么")
    y += 62
    y = table(d, M, y, W - 2 * M, [
        ("频谱图", "先找ω1和k，再列幅值/相位；不要先想电路。"),
        ("有效值", "先按频率分组；同频先相量合并，不同频平方相加。"),
        ("平均功率", "先圈同频项；不同频率平均功率交叉项为0。"),
        ("RLC非正弦", "先分直流、基波、k次谐波；每个频率单独写阻抗。"),
        ("仪表读数", "默认读有效值；最后做平方和，不写瞬时值相加。"),
    ], col1=145, row_h=86, core_rows=[1, 2, 3])
    y += 26
    tag(d, M, y, "必须背下来的三句话")
    y += 58
    card(d, M, y, W - 2 * M, 220, "考场口令", core=True)
    bullets(d, M + 24, y + 58, [
        "非正弦周期量不能整体用一个相量；只能同频率用相量。",
        "有效值是能量等效，不同频率正交，所以平方相加。",
        "平均功率只算直流与同频项，不同频率项一个周期平均为0。",
    ], W - 2 * M - 72)
    y += 248
    tag(d, M, y, "本版取舍")
    y += 58
    y = table(d, M, y, W - 2 * M, [
        ("主体", "教材13-1~13-4：频谱、频谱性质、对称性、非正弦RLC计算。"),
        ("附加", "学校/PPT题只放最后冲刺，不和教材主体混排。"),
        ("降权", "教材13-5及之后不进入主体，因为当前考试范围明确第13章只到13-4。"),
    ], col1=145, row_h=78)
    source_box(d, 1180, "范围依据：shared\\CODEX_电路期末资料整理指令.md#第13章只考到13-4；SOP：SOPs\\06_复习PDF制作SOP.md#Source-First Exam Mode")
    return img


def write_pack():
    PACK.write_text(
        """# 第13章复习PDF source pack v2

## 结论

v2 版已按用户反馈重做：主体严格限定教材 13-1 到 13-4，教材主体占比 100%；学校资料与 PPT 例题不混入主体，单独放在最后附加题页。旧图片/PDF 只参考紫色标题、表格分区、红色提醒和页脚结构，不作为事实来源。

## 主体题

- CH13-TB-13-1：频谱函数与频谱图。Source: shared\\教材\\电路_邱关源_内嵌教材.pdf#pdfpage=359/书页=340/题13-1
- CH13-TB-13-2：频谱性质变换。Source: shared\\教材\\电路_邱关源_内嵌教材.pdf#pdfpage=359/书页=340/题13-2；答案pdfpage=574/书页=555
- CH13-TB-13-3：波形对称性与完整周期波形。Source: shared\\教材\\电路_邱关源_内嵌教材.pdf#pdfpage=360/书页=341/题13-3
- CH13-TB-13-4：RLC串联非正弦电路，求 i(t) 与平均功率。Source: shared\\教材\\电路_邱关源_内嵌教材.pdf#pdfpage=360/书页=341/题13-4；答案pdfpage=574/书页=555

## 附加题

- 学校判断/选择/填空/计算题单列为附加题。Source: 第13章 非正弦周期电流电路-学生作业修改.pdf#page=1-3；第十三章习题答案-有删减.pdf#page=1-7
- PPT 例题用于方法校准。Source: 第13章 非正弦周期电流电路和信号的频谱.pdf#page=21-23,page=28-41

## v2 质量修正

- 修正 v1 中红色“核心”压住正文的问题。
- 修正页底提示与 Source 溢出问题。
- 修正主体范围：13-5及以后不进入主体。
- 增加教材13-4标准大题展开页。
""",
        encoding="utf-8",
    )


def main():
    PAGES.mkdir(parents=True, exist_ok=True)
    pages = [page1(), page2(), page3(), page4(), page5(), page6(), page7(), page8()]
    paths = []
    for i, img in enumerate(pages, 1):
        p = PAGES / f"第13章复习页_v2_{i:02d}.png"
        img.save(p, quality=95)
        paths.append(p)
    pages[0].save(PDF, save_all=True, append_images=pages[1:], resolution=144.0)
    write_pack()
    print(PDF)
    for p in paths:
        print(p)


if __name__ == "__main__":
    main()
