from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import math
import shutil
import textwrap
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont, JpegImagePlugin


ROOT = Path(r"E:\ai产出文件\牛马\日常学习\projects\20260603-电路分析")
OUT_ROOT = ROOT / "outputs" / "circuit_final_sprint_image_pages"
PDF_OUT = ROOT / "outputs" / "PDF"
MEMORY = ROOT / "memory" / "2026-06-21.md"

W, H = 1055, 1491
M = 42
PURPLE = (91, 42, 145)
PURPLE_2 = (132, 82, 190)
LIGHT = (250, 247, 255)
LIGHT_2 = (244, 238, 255)
RED = (203, 24, 42)
BLUE = (34, 95, 170)
CYAN = (0, 138, 164)
GOLD = (186, 126, 0)
BLACK = (31, 29, 38)
GRAY = (92, 86, 105)
LINE = (176, 137, 221)
PALE_RED = (255, 244, 244)
WHITE = (255, 255, 255)

FONT_DIR = Path(r"C:\Windows\Fonts")
FONT_CANDIDATES = [
    FONT_DIR / "Noto Sans SC (TrueType).otf",
    FONT_DIR / "msyh.ttc",
    FONT_DIR / "simsun.ttc",
]
FONT_BOLD_CANDIDATES = [
    FONT_DIR / "Noto Sans SC Bold (TrueType).otf",
    FONT_DIR / "msyhbd.ttc",
    FONT_DIR / "simhei.ttf",
]


def choose_font(candidates: list[Path]) -> Path:
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("No Chinese font found in C:\\Windows\\Fonts")


FONT_REG = choose_font(FONT_CANDIDATES)
FONT_BOLD = choose_font(FONT_BOLD_CANDIDATES)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REG), size)


F = {
    "title": font(44, True),
    "subtitle": font(23, True),
    "h": font(28, True),
    "h2": font(23, True),
    "body": font(21),
    "bodyb": font(21, True),
    "small": font(17),
    "smallb": font(17, True),
    "tiny": font(14),
    "formula": font(20, True),
}


@dataclass(frozen=True)
class Chapter:
    no: str
    title: str
    subtitle: str
    scope: str
    position: str
    route: list[str]
    concepts: list[tuple[str, str]]
    traps: list[tuple[str, str, str]]
    templates: list[tuple[str, str]]
    quick: list[str]
    questions: list[tuple[str, str, str]]
    advanced: list[tuple[str, str]]
    sources: list[str]

    @property
    def slug(self) -> str:
        return f"ch{self.no}_{self.title}".replace("/", "_").replace("\\", "_")

    @property
    def pdf_name(self) -> str:
        return f"第{self.no}章_{self.title}_期末冲刺专用版.pdf"


CHAPTERS = [
    Chapter(
        "01",
        "电路模型和电路定律",
        "参考方向先行，功率/KCL/KVL不丢基础分",
        "必考；服务所有后续计算题。",
        "基础章：小题陷阱高频，大题第一步的符号来源。",
        ["标参考方向", "判关联/非关联", "列KCL/KVL", "算功率吸收/发出", "用功率守恒复核"],
        [
            ("参考方向", "电压电流方向是人为约定；先按约定列式，结果为负才说明实际方向相反。"),
            ("关联参考方向", "电流流入电压正端时 p=ui 表示吸收；否则 p=-ui 或先改成统一约定。"),
            ("KCL/KVL", "KCL管节点电流代数和，KVL管回路电压代数和；和元件类型无关。"),
            ("功率守恒", "全电路吸收功率代数和为0，是检查符号的最快方法。"),
        ],
        [
            ("功率正负", "p>0 不是一定“电源”，要看参考方向；关联方向下 p>0 才是吸收。", "先写参考方向口径。"),
            ("KVL符号", "沿回路遇到正端到负端是电压降；别一会儿按升、一会儿按降。", "全题只用一套规则。"),
            ("电压源电流", "独立电压源电流不是由电压值单独决定。", "必须由外电路约束求。"),
        ],
        [
            ("功率判定题", "画电压极性和电流方向 -> 判关联 -> 写p=ui或p=-ui -> 看正负。"),
            ("KCL/KVL基础题", "先选节点/回路方向 -> 写代数和为0 -> 统一未知量方向。"),
            ("守恒复核", "所有元件功率求完后相加；不为0优先查符号。"),
        ],
        ["参考方向不是实际方向。", "关联方向下 p=ui；p>0吸收，p<0发出。", "KCL/KVL是拓扑约束，不依赖R/L/C。", "大题第一行先画方向，后面符号才有依据。"],
        [
            ("Q1", "某元件电压电流为关联参考方向，u=10V，i=-2A，元件是吸收还是发出功率？", "发出20W。"),
            ("Q2", "KVL能不能用于含电流源的回路？", "能，KVL是拓扑定律。"),
            ("Q3", "参考方向选错会不会导致最终物理答案一定错？", "不会；只要全程一致，负号会反映实际方向。"),
        ],
        [
            ("受控源功率", "受控源也可能吸收或发出功率，不能因为是源就默认发出。"),
            ("多源电路复核", "若题目给多个电源，最后用功率守恒检查每个电源的状态。"),
        ],
        ["Source: CLAUDE.md#当前考试范围", "Source: 第01章-电路模型和电路定律\\知识点\\核心知识点.md#待整理知识点", "Source: 第01章-电路模型和电路定律\\习题\\exercise_index.md#已定位资料"],
    ),
    Chapter(
        "02",
        "电阻电路的等效变换",
        "等效不是乱合并，端口外特性必须不变",
        "必考；与第4章戴维南/诺顿联动。",
        "基础计算章：等效电阻、源变换、输入电阻是后面大题的工具。",
        ["确定端口", "串并联先化简", "电源等效变换", "含受控源用测试源", "检查端口外特性"],
        [
            ("串并联", "只有同一电流才串联，只有同一电压才并联；图形挨着不等于可合并。"),
            ("源变换", "电压源串R与电流源并R可等效，方向和极性必须匹配。"),
            ("输入电阻", "独立源置零后从端口看入；含受控源时必须加测试源。"),
            ("端口等效", "等效只保证外部端口关系，不保证内部功率和支路量相同。"),
        ],
        [
            ("乱合并电阻", "桥式结构常常不是串并联。", "先标同节点。"),
            ("源变换方向", "Is=Us/R 的方向由电压源正端指向负端对应。", "变换后画箭头。"),
            ("受控源置零", "受控源不能像独立源一样置零。", "保留控制关系。"),
        ],
        [
            ("等效电阻题", "关独立源 -> 保留受控源 -> 端口加测试源 -> Rin=Ut/It。"),
            ("源变换题", "电压源串R <-> 电流源并R；R不变，数值U=IR。"),
            ("桥式判断", "先找节点编号，只有节点完全相同才可并联。"),
        ],
        ["串联看同流，并联看同压。", "独立电压源置零为短路，独立电流源置零为开路。", "含受控源求Rin，测试源是默认动作。", "等效是端口等效，不是内部完全相同。"],
        [
            ("Q1", "理想电压源置零后等效为什么？", "短路。"),
            ("Q2", "理想电流源置零后等效为什么？", "开路。"),
            ("Q3", "含受控源求输入电阻时能否直接把受控源关掉？", "不能。"),
        ],
        [
            ("桥式网络", "无法串并联时，转入节点法或源变换，不硬合并。"),
            ("负输入电阻", "含受控源网络可能出现负等效电阻，不要因为结果负就直接否定。"),
        ],
        ["Source: CLAUDE.md#资料优先级", "Source: 第02章-电阻电路的等效变换\\知识点\\核心知识点.md#待整理知识点", "Source: 第02章-电阻电路的等效变换\\习题\\exercise_index.md#已定位资料"],
    ),
    Chapter(
        "03",
        "电阻电路的一般分析",
        "节点法/网孔法是70分计算题的主干工具",
        "必考；大题优先级最高之一。",
        "大题主线章：节点电压法、网孔/回路电流法、支路法。",
        ["选方法", "设未知量", "处理电源约束", "列KCL/KVL", "解方程并回代"],
        [
            ("节点电压法", "以参考节点为零电位，对非参考节点列KCL；适合电流源多的电路。"),
            ("网孔电流法", "平面电路设网孔电流列KVL；适合电压源多的电路。"),
            ("超节点", "电压源夹在两个非参考节点之间，合成超节点列KCL，再补电压约束。"),
            ("超网孔", "电流源夹在两个网孔之间，绕开电流源列KVL，再补电流约束。"),
        ],
        [
            ("参考节点", "参考节点选得差会让方程变复杂。", "优先选连接支路最多或接地节点。"),
            ("受控源", "受控源要保留，并补控制量表达式。", "不能当独立源消掉。"),
            ("电源支路", "节点法遇电压源别硬写支路电流。", "用超节点。"),
        ],
        [
            ("节点法大题", "选参考点 -> 标节点电压 -> 每个节点写流出电流和 -> 处理超节点 -> 求支路量。"),
            ("网孔法大题", "设同向网孔电流 -> 公共电阻写差值 -> 电流源用超网孔 -> 回代。"),
            ("方法选择", "电流源多用节点法；电压源多用网孔法；非平面电路不用网孔法。"),
        ],
        ["节点法本质是KCL+VCR。", "网孔法本质是KVL+VCR。", "超节点/超网孔不是新定理，只是电源约束的处理技巧。", "受控源必须补控制方程。"],
        [
            ("Q1", "节点法中参考节点电压是多少？", "0。"),
            ("Q2", "电压源连接两个非参考节点时怎么处理？", "用超节点并补电压约束。"),
            ("Q3", "网孔法是否适用于所有电路？", "不适用于非平面电路。"),
        ],
        [
            ("节点+受控源", "大题常见扣分点是忘写控制量与节点电压的关系。"),
            ("综合方程检查", "方程数量必须等于未知量数量；少一个约束必错。"),
        ],
        ["Source: CLAUDE.md#大题策略", "Source: 第03章-电阻电路的一般分析\\知识点\\核心知识点.md#待整理知识点", "Source: 第03章-电阻电路的一般分析\\习题\\exercise_index.md#已定位资料"],
    ),
    Chapter(
        "04",
        "电路定理",
        "叠加、戴维南/诺顿、最大功率传输是大题高频",
        "必考；大题优先级最高之一。",
        "定理章：把复杂网络压缩成可计算的等效模型。",
        ["识别线性电路", "叠加分源", "断开负载求Uoc", "关源求Req", "接回负载求目标量"],
        [
            ("叠加定理", "线性电路中每次只保留一个独立源，其他独立源置零，最后代数相加响应。"),
            ("戴维南", "任意线性有源一端口可等效为电压源Uoc串Req。"),
            ("诺顿", "等效为电流源Isc并Req，且 Uoc=Isc Req。"),
            ("最大功率", "直流电阻负载取RL=Rth；交流阻抗负载取共轭匹配。"),
        ],
        [
            ("叠加功率", "功率不能直接叠加。", "先叠加电压/电流，再算功率。"),
            ("忘断负载", "求戴维南电压时必须断开负载。", "端口开路求Uoc。"),
            ("Req含受控源", "独立源置零后受控源保留。", "用测试源求Req。"),
        ],
        [
            ("戴维南大题", "断负载 -> 求Uoc -> 关独立源求Req -> 接RL -> 求电流/功率。"),
            ("叠加题", "每次留一个独立源 -> 目标量带符号相加 -> 不叠加功率。"),
            ("最大功率", "先求等效源，再用RL=Rth和Pmax=Uth^2/(4Rth)。"),
        ],
        ["叠加只叠加线性响应，不叠加功率。", "戴维南第一步是断开负载。", "有受控源时Req常用测试源。", "最大功率不是最大效率。"],
        [
            ("Q1", "叠加定理中不作用的独立电压源如何处理？", "短路。"),
            ("Q2", "戴维南等效电压是什么？", "端口开路电压Uoc。"),
            ("Q3", "最大功率传输时效率是否最高？", "不是，常为50%左右。"),
        ],
        [
            ("受控源戴维南", "不能关受控源；若端口无独立源，仍可能有非零输入电阻。"),
            ("诺顿互换", "Isc方向与Uoc极性要对应，否则接回负载符号错。"),
        ],
        ["Source: CLAUDE.md#大题策略", "Source: 第04章-电路定理\\知识点\\核心知识点.md#待整理知识点", "Source: 第04章-电路定理\\习题\\exercise_index.md#已定位资料"],
    ),
    Chapter(
        "06",
        "储能元件",
        "电容电感是暂态和正弦稳态的共同入口",
        "必考；第7章和第9章前置。",
        "概念桥梁章：VCR、能量、初值连续性。",
        ["认元件VCR", "判初值连续", "写能量公式", "直流稳态等效", "进入一阶电路"],
        [
            ("电容VCR", "i=C du/dt；电压不能突变，直流稳态相当开路。"),
            ("电感VCR", "u=L di/dt；电流不能突变，直流稳态相当短路。"),
            ("储能", "电容能量1/2Cu^2，电感能量1/2Li^2，永远非负。"),
            ("初始条件", "换路瞬间 uC(0+)=uC(0-)，iL(0+)=iL(0-)。"),
        ],
        [
            ("连续量混淆", "电容电流可突变，电感电压可突变。", "只记uC、iL连续。"),
            ("直流稳态", "稳态不是换路瞬间。", "t<0稳态先求初值。"),
            ("能量符号", "能量不带正负方向。", "平方项保证非负。"),
        ],
        [
            ("初值题", "t<0画稳态等效 -> 求uC/iL -> 写0+连续量。"),
            ("能量题", "代Wc=1/2Cu^2或WL=1/2Li^2，单位统一。"),
            ("VCR判断", "看到du/dt找电容，看到di/dt找电感。"),
        ],
        ["电容记电压，电感记电流。", "直流稳态：C开路，L短路。", "换路瞬间：uC连续，iL连续。", "储能公式都是1/2乘参数乘状态量平方。"],
        [
            ("Q1", "电容电压能否突变？", "不能。"),
            ("Q2", "电感电流能否突变？", "不能。"),
            ("Q3", "直流稳态下电容等效为什么？", "开路。"),
        ],
        [
            ("多储能初值", "多个电容/电感时逐个写连续量，不要只写一个总初值。"),
            ("等效电阻入口", "第7章时间常数需要从电容/电感端口看等效电阻。"),
        ],
        ["Source: CLAUDE.md#当前考试范围", "Source: 第06章-储能元件\\知识点\\核心知识点.md#待整理知识点", "Source: 第06章-储能元件\\习题\\exercise_index.md#已定位资料"],
    ),
    Chapter(
        "07",
        "一阶电路",
        "三要素法是暂态大题的最短路线",
        "只到7-4；大题高频。",
        "动态电路主线章：初值、稳态值、时间常数三件事。",
        ["求初值f(0+)", "求稳态f(inf)", "求时间常数tau", "套三要素公式", "检查单位和极限"],
        [
            ("三要素法", "f(t)=f(inf)+[f(0+)-f(inf)]e^{-t/tau}。"),
            ("时间常数", "RC电路tau=Req C；RL电路tau=L/Req。Req从储能元件端口看入。"),
            ("零输入/零状态", "零输入只由初始储能引起；零状态由外加激励引起。"),
            ("全响应", "全响应=零输入响应+零状态响应，也可直接用三要素法。"),
        ],
        [
            ("初值", "把0-和0+混用。", "先求0-稳态，再用连续性到0+。"),
            ("时间常数", "RC和RL公式写反。", "C乘电阻，L除电阻。"),
            ("终值", "终值要看换路后的新稳态。", "不是t<0旧稳态。"),
        ],
        [
            ("三要素大题", "画t<0 -> 求f(0+) -> 画t>inf -> 求f(inf) -> 求Req和tau -> 套公式。"),
            ("分段换路", "每次换路都重新定义新的0时刻和新初值。"),
            ("求电容/电感外量", "先求状态量uC/iL，再用电路关系回代目标量。"),
        ],
        ["三要素：初值、终值、时间常数。", "RC: tau=ReqC；RL: tau=L/Req。", "电容电压和电感电流连续。", "终值来自换路后稳态。"],
        [
            ("Q1", "一阶RC电路时间常数是什么？", "ReqC。"),
            ("Q2", "一阶RL电路时间常数是什么？", "L/Req。"),
            ("Q3", "三要素公式中的f(inf)来自换路前还是换路后？", "换路后稳态。"),
        ],
        [
            ("含受控源暂态", "求Req时若有受控源，仍保留受控源并用测试源。"),
            ("目标量非状态量", "若求电阻电流，不能直接套三要素给它，除非它确为同一一阶变量的线性函数。"),
        ],
        ["Source: CLAUDE.md#当前考试范围", "Source: 第07章-一阶电路\\知识点\\核心知识点.md#待整理知识点", "Source: 第07章-一阶电路\\习题\\exercise_index.md#已定位资料"],
    ),
    Chapter(
        "08",
        "相量法",
        "把同频正弦量变成复数，先统一参考再计算",
        "必考；第9章前置。",
        "工具章：相量、阻抗、导纳，为正弦稳态铺路。",
        ["确认同频", "统一有效值/最大值", "选参考相位", "写阻抗", "复数运算后还原时域"],
        [
            ("相量", "同频正弦量可用复数表示幅值与相位；不同频率不能合成一个相量。"),
            ("有效值相量", "电路计算常用有效值相量，题给最大值时要除以sqrt(2)。"),
            ("阻抗", "R为R，L为jωL，C为1/(jωC)。"),
            ("导纳", "Y=1/Z；并联电路常用导纳更省事。"),
        ],
        [
            ("不同频率", "把ω和3ω相量直接相加。", "只能同频相量运算。"),
            ("最大值/有效值", "题给Um却当U使用。", "先看题目口径。"),
            ("相位还原", "计算用cos口径，时域用sin口径时要换相位。", "全题统一口径。"),
        ],
        [
            ("相量转换", "u=Um cos(ωt+φ) -> U=Um/sqrt(2)∠φ。"),
            ("阻抗计算", "串联阻抗相加，并联导纳相加。"),
            ("时域还原", "有效值相量U∠φ -> u(t)=sqrt(2)U cos(ωt+φ)。"),
        ],
        ["相量法只服务同频正弦稳态。", "有效值相量是默认计算口径。", "ZL=jωL，ZC=1/(jωC)。", "并联优先用导纳。"],
        [
            ("Q1", "不同频率正弦量能否直接相量相加？", "不能。"),
            ("Q2", "若u=100cos(ωt+30°)，有效值相量是多少？", "100/sqrt(2)∠30°。"),
            ("Q3", "电容阻抗是什么？", "1/(jωC)。"),
        ],
        [
            ("参考相位选择", "选电压或电流为0°后，所有相位都要相对它表达。"),
            ("复功率前置", "第9章功率公式依赖相量有效值口径。"),
        ],
        ["Source: CLAUDE.md#当前考试范围", "Source: 第08章-相量法\\知识点\\核心知识点.md#待整理知识点", "Source: 第08章-相量法\\习题\\exercise_index.md#已定位资料"],
    ),
    Chapter(
        "09",
        "正弦稳态电路分析",
        "相量法+功率三角形是电气工程核心计算",
        "必考；大题高频。",
        "正弦稳态主线章：阻抗网络、功率、功率因数。",
        ["转相量", "算等效阻抗", "求相量电压/电流", "算P/Q/S", "判断功率因数和补偿"],
        [
            ("正弦稳态", "所有量同频，微分方程变为复数代数方程。"),
            ("复功率", "S=UI*，P为实部，Q为虚部，|S|为视在功率。"),
            ("功率因数", "cosφ=P/|S|；滞后通常对应感性负载。"),
            ("补偿", "并联电容用于提高感性负载功率因数，减少无功。"),
        ],
        [
            ("共轭", "复功率公式要用电流相量共轭。", "S=U I*。"),
            ("功率单位", "P用W，Q用var，S用VA。", "单位混写会扣分。"),
            ("感容符号", "感性Q为正、容性Q为负。", "按课程口径统一。"),
        ],
        [
            ("正弦稳态大题", "时域转相量 -> 求Zeq -> 分压/分流/节点法 -> 回代功率。"),
            ("功率因数题", "由P、U、I求cosφ -> 判断补偿前后Q -> 求电容。"),
            ("最大功率交流版", "负载阻抗取源内阻抗共轭。"),
        ],
        ["所有相量用有效值。", "S=UI*，P=Re(S)，Q=Im(S)。", "感性负载电流滞后，容性负载电流超前。", "补偿电容只补无功，不改变有功负载本质。"],
        [
            ("Q1", "复功率公式中电流要不要取共轭？", "要。"),
            ("Q2", "视在功率单位是什么？", "VA。"),
            ("Q3", "感性负载提高功率因数通常并什么？", "电容。"),
        ],
        [
            ("节点法+相量", "复杂交流网络仍可用节点法，只是电导换成导纳。"),
            ("补偿边界", "不能把功率因数补偿理解成有功功率变大。"),
        ],
        ["Source: CLAUDE.md#大题策略", "Source: 第09章-正弦稳态电路分析\\知识点\\核心知识点.md#待整理知识点", "Source: 第09章-正弦稳态电路分析\\习题\\exercise_index.md#已定位资料"],
    ),
    Chapter(
        "10",
        "含有耦合电感的电路",
        "同名端决定互感项正负，变压器题先定方向",
        "10-3不考；理想/空心变压器是大题候选。",
        "互感与变压器章：符号判断比计算更容易扣分。",
        ["标同名端", "设电流参考方向", "判互感电压正负", "列相量方程", "用变比/反映阻抗"],
        [
            ("互感", "一个线圈电流变化在另一个线圈中感应电压；互感项大小为jωM I。"),
            ("同名端", "两电流同时流入同名端时互感项取助磁正号；一入一出取反号。"),
            ("空心变压器", "按耦合电感方程列相量方程，不能直接套理想变压器。"),
            ("理想变压器", "电压比等于匝比，电流比反比且方向由同名端决定。"),
        ],
        [
            ("互感符号", "只看M正负，不看电流是否流入同名端。", "先画点标和箭头。"),
            ("理想/空心混用", "空心变压器不能直接用理想变比。", "看题目是否写理想。"),
            ("反映阻抗", "阻抗折算比例写反。", "阻抗按匝比平方折算。"),
        ],
        [
            ("耦合电感方程", "设电流 -> 判同名端 -> 写自感项+jωL I，互感项±jωM I。"),
            ("理想变压器", "按n=N1/N2写电压比，再由功率守恒/电流方向写电流比。"),
            ("反映阻抗", "副边负载折到原边：Z'=n^2 ZL。"),
        ],
        ["先同名端，后方程。", "同时流入同名端互感助磁。", "理想变压器阻抗折算是匝比平方。", "10-3不考，别把低频内容做成主线。"],
        [
            ("Q1", "两电流同时流入同名端，互感项一般取什么号？", "助磁正号。"),
            ("Q2", "理想变压器阻抗折算是否按匝比一次方？", "不是，按平方。"),
            ("Q3", "空心变压器能否直接当理想变压器？", "不能。"),
        ],
        [
            ("互感+功率", "若题目求功率，先统一相量有效值并处理互感符号。"),
            ("含源变压器", "反映阻抗后可回到正弦稳态网络计算。"),
        ],
        ["Source: CLAUDE.md#当前考试范围", "Source: 第10章-含有耦合电感的电路\\知识点\\核心知识点.md#待整理知识点", "Source: 第10章-含有耦合电感的电路\\习题\\exercise_index.md#已定位资料"],
    ),
    Chapter(
        "11",
        "电路的频率响应",
        "只抓11-2/11-3：串联RLC谐振与频率选择",
        "只考11-2、11-3；串联RLC谐振高频。",
        "频域章：谐振条件、品质因数、带宽。",
        ["写Z(ω)", "令虚部为0", "求ω0", "求Q和带宽", "判断滤波特性"],
        [
            ("串联谐振", "RLC串联在ω0=1/sqrt(LC)时总阻抗最小且为R，电流最大。"),
            ("并联谐振", "并联网络谐振时输入阻抗大，具体公式按电路结构判断。"),
            ("品质因数", "Q反映选择性；串联RLC常用Q=ω0L/R=1/(ω0CR)。"),
            ("带宽", "带宽与Q反比，Q越大通带越窄、选择性越强。"),
        ],
        [
            ("谐振条件", "只背ω0不检查电路是否标准RLC。", "先写Z或Y虚部为0。"),
            ("最大量", "串联谐振是电流最大，不是阻抗最大。", "看串/并联。"),
            ("电压放大", "谐振时L/C电压可能很大。", "别误以为各元件电压都等于电源。"),
        ],
        [
            ("串联RLC题", "写Z=R+j(ωL-1/ωC) -> 虚部为0 -> ω0 -> Imax=U/R。"),
            ("Q与带宽", "先求ω0，再按Q公式和BW=ω0/Q。"),
            ("滤波判断", "看输出取在R/L/C哪个元件上，判断低通/高通/带通。"),
        ],
        ["串联谐振：Z最小，I最大。", "ω0=1/sqrt(LC)。", "Q=ω0L/R=1/(ω0CR)。", "Q越大，选择性越强，带宽越窄。"],
        [
            ("Q1", "串联RLC谐振时电路总阻抗等于什么？", "R。"),
            ("Q2", "串联谐振角频率是什么？", "1/sqrt(LC)。"),
            ("Q3", "Q变大，带宽如何变化？", "变窄。"),
        ],
        [
            ("第11+13综合", "谐振可用来筛选非正弦谐波：每个频率分别看阻抗。"),
            ("电压谐振", "L、C两端电压可能远大于电源电压，是选择题陷阱。"),
        ],
        ["Source: CLAUDE.md#当前考试范围", "Source: outputs\\07_第11章_第13章综合大题专题.md#结论", "Source: 第11章-电路的频率响应\\知识点\\核心知识点.md#待整理知识点"],
    ),
    Chapter(
        "13",
        "非正弦周期电流电路",
        "先分频，再逐频率计算，最后按规则合成",
        "只到13-4；有效值、平均功率、分谐波计算高频。",
        "综合章：第11章频响 + 第9章相量 + 非正弦分解。",
        ["傅里叶分解", "按频率单独等效", "同频相量计算", "有效值平方相加", "平均功率同频相加"],
        [
            ("频谱", "非正弦周期量拆成直流、基波和各次谐波；频谱记录幅值和相位。"),
            ("有效值", "不同频率正交，最终按平方和开方；同频分量先相量合并。"),
            ("平均功率", "只计算直流与同频项功率，不同频率交叉项周期平均为0。"),
            ("分频计算", "直流、ω、kω分别画等效电路；L/C阻抗随k变化。"),
        ],
        [
            ("不同频率相量", "把ω和3ω直接相量相加。", "不同频率只能最后按规则合成。"),
            ("有效值", "把峰值、有效值、最大值混用。", "先统一口径。"),
            ("功率", "把3ω电压和5ω电流拿来算平均功率。", "只圈同频项。"),
        ],
        [
            ("非正弦RLC大题", "拆激励 -> 每个频率算Zk -> 求Ik/Uk -> 合成瞬时量/有效值/P。"),
            ("频谱题", "先找基波ω1，再列谐波次数、幅值、相位。"),
            ("小题", "有效值与初相无关；不同频率不能合成一个相量。"),
        ],
        ["不同频率不能直接相量合并。", "有效值平方相加，同频先合并。", "平均功率只算直流和同频项。", "13章只到13-4，后面只作降权参考。"],
        [
            ("Q1", "不同频率电压能否写成一个相量？", "不能。"),
            ("Q2", "有效值是否与单个正弦量初相有关？", "无关。"),
            ("Q3", "平均功率能否跨频相乘？", "不能。"),
        ],
        [
            ("第11+13综合", "先按谐波频率看谐振/滤波，再计算各频率输出。"),
            ("仪表读数", "电压表/电流表通常读有效值，按平方和合成。"),
        ],
        ["Source: CLAUDE.md#当前考试范围", "Source: outputs\\第13章_非正弦周期电流电路_复习PDF\\source_pack.md#结论", "Source: 第13章-非正弦周期电流电路\\习题\\exercise_index.md#原题 ID：CH13-TB-13-4"],
    ),
    Chapter(
        "16",
        "二端口网络",
        "降权处理：只抓概念、Z/Y参数和端口条件",
        "只到16-2；按选择/判断概念题处理。",
        "降权章：不投入复杂计算，防止选择判断失分。",
        ["认二端口", "写端口电流方向", "区分Z/Y参数", "判断开短路条件", "做概念题"],
        [
            ("二端口", "两个端口、四个端子，端口电流满足从端口正端流入的约定。"),
            ("Z参数", "用电流表示电压：U1=Z11I1+Z12I2，U2=Z21I1+Z22I2。"),
            ("Y参数", "用电压表示电流：I1=Y11U1+Y12U2，I2=Y21U1+Y22U2。"),
            ("参数测量", "Z参数常用开路条件，Y参数常用短路条件。"),
        ],
        [
            ("端口方向", "电流方向画反导致参数符号错。", "统一从端口正端流入。"),
            ("Z/Y混淆", "把Z参数的开路条件和Y参数的短路条件混用。", "Z开路，Y短路。"),
            ("降权", "把第16章做成复杂大题。", "只保留选择判断。"),
        ],
        [
            ("Z参数判断", "看到U由I线性表示，选Z参数；测Zij时让另一个端口开路。"),
            ("Y参数判断", "看到I由U线性表示，选Y参数；测Yij时让另一个端口短路。"),
            ("概念题", "端口条件、互易/对称只做定义级判断。"),
        ],
        ["Z参数：电流作自变量，开路测。", "Y参数：电压作自变量，短路测。", "端口电流默认从正端流入。", "第16章降权，不做复杂计算主线。"],
        [
            ("Q1", "Z参数用什么变量表示什么变量？", "用I表示U。"),
            ("Q2", "Y参数测量常用什么条件？", "短路条件。"),
            ("Q3", "第16章本次复习是否按复杂计算题处理？", "不，按选择/判断。"),
        ],
        [
            ("参数转换", "若出现Z与Y互换，只记矩阵可逆时Y=Z^-1，考试小题级别即可。"),
            ("端口口径", "四端网络不一定满足二端口端口条件，先判断端口电流关系。"),
        ],
        ["Source: CLAUDE.md#当前考试范围", "Source: outputs\\08_第16章选择题专题.md#结论", "Source: 第16章-二端口网络\\知识点\\核心知识点.md#待整理知识点"],
    ),
]


def text_w(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont) -> int:
    return int(draw.textbbox((0, 0), text, font=f)[2])


def line_h(f: ImageFont.FreeTypeFont, extra: int = 7) -> int:
    box = f.getbbox("国")
    return box[3] - box[1] + extra


def wrap(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    lines: list[str] = []
    for para in str(text).split("\n"):
        para = para.strip()
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


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    f: ImageFont.FreeTypeFont,
    max_w: int,
    fill: tuple[int, int, int] = BLACK,
    spacing: int = 7,
    max_lines: int | None = None,
) -> int:
    x, y = xy
    lines = wrap(draw, text, f, max_w)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        if lines:
            lines[-1] = lines[-1].rstrip("，。；、") + "..."
    for line in lines:
        draw.text((x, y), line, font=f, fill=fill)
        y += line_h(f, spacing)
    return y


def new_page(ch: Chapter, page_no: int, title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((18, 18, W - 18, H - 18), radius=20, outline=PURPLE, width=3)
    d.rounded_rectangle((M, 34, W - M, 132), radius=16, fill=LIGHT_2, outline=LINE, width=2)
    d.text((M + 24, 52), f"第{ch.no}章", font=F["subtitle"], fill=RED)
    d.text((M + 118, 48), title, font=F["title"], fill=PURPLE)
    d.text((M + 118, 101), subtitle, font=F["smallb"], fill=GRAY)
    d.rounded_rectangle((W - 200, 54, W - M - 18, 108), radius=12, fill=PURPLE)
    d.text((W - 178, 68), "期末冲刺专用", font=F["smallb"], fill=WHITE)
    d.line((M, H - 62, W - M, H - 62), fill=PURPLE, width=2)
    d.text((M, H - 43), "source-first sprint pack", font=F["small"], fill=GRAY)
    foot = f"{page_no} / 8"
    d.text(((W - text_w(d, foot, F["bodyb"])) // 2, H - 46), foot, font=F["bodyb"], fill=PURPLE)
    d.text((W - 310, H - 43), "电路分析 | 分章节PDF", font=F["small"], fill=PURPLE)
    return img, d


def tag(d: ImageDraw.ImageDraw, x: int, y: int, text: str, color: tuple[int, int, int] = PURPLE) -> tuple[int, int]:
    tw = text_w(d, text, F["h2"]) + 34
    d.rounded_rectangle((x, y, x + tw, y + 48), radius=8, fill=color)
    d.text((x + 17, y + 9), text, font=F["h2"], fill=WHITE)
    return x + tw, y + 58


def card(
    d: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    h: int,
    title: str | None = None,
    fill: tuple[int, int, int] = LIGHT,
    outline: tuple[int, int, int] = LINE,
    core: bool = False,
) -> None:
    d.rounded_rectangle((x, y, x + w, y + h), radius=12, fill=fill, outline=outline, width=2)
    if title:
        d.text((x + 20, y + 14), title, font=F["h"], fill=PURPLE)
    if core:
        d.rounded_rectangle((x + w - 100, y + 18, x + w - 22, y + 48), radius=15, fill=RED)
        d.text((x + w - 82, y + 22), "核心", font=F["smallb"], fill=WHITE)


def bullets(
    d: ImageDraw.ImageDraw,
    x: int,
    y: int,
    items: Iterable[str],
    max_w: int,
    size: str = "body",
    color: tuple[int, int, int] = BLACK,
    gap: int = 6,
) -> int:
    f = F[size]
    for item in items:
        d.ellipse((x, y + 9, x + 10, y + 19), fill=PURPLE)
        y = draw_wrapped(d, item, (x + 24, y), f, max_w - 24, fill=color, spacing=gap)
        y += 5
    return y


def table(
    d: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    rows: list[tuple[str, str]],
    col1: int = 170,
    row_h: int = 86,
    core_rows: Iterable[int] = (),
) -> int:
    core = set(core_rows)
    total = row_h * len(rows)
    d.rounded_rectangle((x, y, x + w, y + total), radius=10, fill=WHITE, outline=LINE, width=2)
    for i, (left, right) in enumerate(rows):
        yy = y + i * row_h
        if i:
            d.line((x, yy, x + w, yy), fill=LINE, width=1)
        d.line((x + col1, yy, x + col1, yy + row_h), fill=LINE, width=1)
        d.text((x + 16, yy + 18), left, font=F["bodyb"], fill=PURPLE)
        reserve = 90 if i in core else 0
        draw_wrapped(d, right, (x + col1 + 18, yy + 15), F["body"], w - col1 - 38 - reserve, spacing=5, max_lines=3)
        if i in core:
            d.rounded_rectangle((x + w - 80, yy + 24, x + w - 24, yy + 54), radius=14, fill=RED)
            d.text((x + w - 70, yy + 28), "必会", font=F["tiny"], fill=WHITE)
    return y + total


def source_box(d: ImageDraw.ImageDraw, y: int, sources: list[str]) -> None:
    y = min(y, H - 205)
    tag(d, M, y, "引用来源", BLUE)
    y += 58
    text = "；".join(sources[:3])
    table(d, M, y, W - 2 * M, [("Source", text)], col1=130, row_h=94)


def draw_mini_circuit(d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, mode: int) -> None:
    d.rounded_rectangle((x, y, x + w, y + h), radius=12, fill=WHITE, outline=LINE, width=2)
    cx, cy = x + w // 2, y + h // 2
    d.line((x + 28, cy, x + w - 28, cy), fill=PURPLE, width=4)
    if mode % 4 == 0:
        for k in range(5):
            xx = x + 78 + k * 28
            d.line((xx, cy, xx + 12, cy - 18), fill=RED, width=3)
            d.line((xx + 12, cy - 18, xx + 24, cy + 18), fill=RED, width=3)
            d.line((xx + 24, cy + 18, xx + 36, cy), fill=RED, width=3)
        d.text((cx - 18, cy + 32), "R", font=F["h2"], fill=RED)
    elif mode % 4 == 1:
        d.line((cx - 16, y + 34, cx - 16, y + h - 34), fill=RED, width=4)
        d.line((cx + 16, y + 34, cx + 16, y + h - 34), fill=RED, width=4)
        d.text((cx - 18, cy + 36), "C", font=F["h2"], fill=RED)
    elif mode % 4 == 2:
        for k in range(5):
            d.arc((x + 78 + k * 34, cy - 25, x + 112 + k * 34, cy + 25), 180, 0, fill=RED, width=4)
        d.text((cx - 18, cy + 36), "L", font=F["h2"], fill=RED)
    else:
        d.ellipse((cx - 34, cy - 34, cx + 34, cy + 34), outline=RED, width=4)
        d.text((cx - 18, cy - 18), "源", font=F["h2"], fill=RED)


def page_1(ch: Chapter) -> Image.Image:
    img, d = new_page(ch, 1, f"第{ch.no}章：{ch.title}", ch.subtitle)
    y = 158
    tag(d, M, y, "0. 本章定位")
    y += 62
    table(d, M, y, W - 2 * M, [
        ("范围", ch.scope),
        ("定位", ch.position),
        ("路线", " -> ".join(ch.route)),
        ("一句话", ch.subtitle),
    ], col1=130, row_h=88, core_rows=[0, 2])
    y += 390
    tag(d, M, y, "1小时路线")
    y += 62
    phases = [
        ("10min", "看总图", "先知道本章解决什么问题。"),
        ("20min", "背核心", "只背会做题的定义和公式。"),
        ("15min", "刷题型", "把看到什么先做什么固定下来。"),
        ("15min", "查陷阱", "最后用小题和答案页查漏。"),
    ]
    x = M
    for i, (t, name, desc) in enumerate(phases):
        card(d, x, y, 225, 175, fill=WHITE, outline=LINE, core=i == 1)
        d.text((x + 20, y + 22), t, font=F["h"], fill=RED)
        d.text((x + 20, y + 68), name, font=F["h2"], fill=PURPLE)
        draw_wrapped(d, desc, (x + 20, y + 108), F["body"], 185, spacing=5)
        x += 248
    y += 230
    tag(d, M, y, "概念地图")
    y += 62
    card(d, M, y, W - 2 * M, 250, "从本章到考场", fill=LIGHT, core=True)
    cx, cy = W // 2, y + 128
    d.ellipse((cx - 82, cy - 44, cx + 82, cy + 44), fill=PURPLE)
    d.text((cx - text_w(d, ch.title[:8], F["h2"]) // 2, cy - 15), ch.title[:8], font=F["h2"], fill=WHITE)
    nodes = ch.concepts[:4]
    positions = [(M + 120, y + 58), (W - M - 270, y + 58), (M + 120, y + 170), (W - M - 270, y + 170)]
    for idx, ((name, _), (nx, ny)) in enumerate(zip(nodes, positions)):
        d.line((cx, cy, nx + 95, ny + 24), fill=LINE, width=3)
        d.rounded_rectangle((nx, ny, nx + 190, ny + 52), radius=16, fill=WHITE, outline=LINE, width=2)
        d.text((nx + 18, ny + 13), name, font=F["bodyb"], fill=[PURPLE, RED, BLUE, CYAN][idx])
    source_box(d, 1200, ch.sources)
    return img


def page_2(ch: Chapter) -> Image.Image:
    img, d = new_page(ch, 2, "核心概念：先讲边界", "每个公式只在它该出现的地方出现")
    y = 158
    tag(d, M, y, "必会概念")
    y += 62
    table(d, M, y, W - 2 * M, ch.concepts[:4], col1=170, row_h=118, core_rows=[0, 1])
    y += 510
    tag(d, M, y, "为什么这样考")
    y += 62
    card(d, M, y, W - 2 * M, 260, "隐藏连接", fill=WHITE, core=True)
    why = [
        f"{ch.title}不是孤立知识点，它在期末卷里通常承担“把题目翻译成方程/等效/模板”的作用。",
        "电路分析的共同底层是：参考方向 + KCL/KVL + 元件约束。任何章节只是把这三件事换了一种计算形式。",
        "因此复习时不要按教材顺序死背，优先背“看到什么 -> 先做什么”。",
    ]
    bullets(d, M + 24, y + 64, why, W - 2 * M - 54)
    source_box(d, 1125, ch.sources)
    return img


def page_3(ch: Chapter) -> Image.Image:
    img, d = new_page(ch, 3, "大题模板：考场可复写", "把解法压成固定动作，减少临场乱试")
    y = 158
    tag(d, M, y, "题型模板")
    y += 62
    rows = ch.templates[:3]
    table(d, M, y, W - 2 * M, rows, col1=190, row_h=132, core_rows=[0])
    y += 435
    tag(d, M, y, "标准答题版式")
    y += 62
    card(d, M, y, W - 2 * M, 360, "闭卷步骤", fill=LIGHT, core=True)
    for i, step in enumerate(ch.route, 1):
        yy = y + 68 + (i - 1) * 55
        d.ellipse((M + 28, yy, M + 62, yy + 34), fill=PURPLE)
        d.text((M + 40, yy + 4), str(i), font=F["smallb"], fill=WHITE)
        draw_wrapped(d, step, (M + 80, yy + 1), F["bodyb"], W - 2 * M - 125, fill=BLACK, spacing=4, max_lines=1)
    draw_mini_circuit(d, W - M - 300, y + 190, 250, 120, int(ch.no))
    source_box(d, 1170, ch.sources)
    return img


def page_4(ch: Chapter) -> Image.Image:
    img, d = new_page(ch, 4, "选择判断陷阱", "小题不是背定义，是训练边界条件")
    y = 158
    tag(d, M, y, "高频易错")
    y += 62
    trap_rows = [(name, f"错误说法：{wrong} 正确抓手：{fix}") for name, wrong, fix in ch.traps[:3]]
    table(d, M, y, W - 2 * M, trap_rows, col1=160, row_h=132, core_rows=[0, 1, 2])
    y += 440
    tag(d, M, y, "3道自测")
    y += 62
    for i, (qid, question, answer) in enumerate(ch.questions[:3]):
        x = M + i * 322
        card(d, x, y, 295, 285, f"{qid}", fill=WHITE, outline=LINE)
        draw_wrapped(d, question, (x + 20, y + 62), F["body"], 255, spacing=6, max_lines=5)
        d.line((x + 20, y + 218, x + 275, y + 218), fill=LINE, width=2)
        draw_wrapped(d, f"答案：{answer}", (x + 20, y + 232), F["smallb"], 255, fill=RED, spacing=4, max_lines=2)
    source_box(d, 1170, ch.sources)
    return img


def page_5(ch: Chapter) -> Image.Image:
    img, d = new_page(ch, 5, "A4速查：考前10分钟只看这里", "公式必须带条件，口令必须能直接做题")
    y = 158
    tag(d, M, y, "速查口令")
    y += 62
    rows = [(f"{i:02d}", item) for i, item in enumerate(ch.quick[:4], 1)]
    table(d, M, y, W - 2 * M, rows, col1=100, row_h=105, core_rows=[0, 1])
    y += 460
    tag(d, M, y, "考前自检")
    y += 62
    card(d, M, y, W - 2 * M, 340, "如果只剩5分钟", fill=PALE_RED, outline=(235, 175, 175), core=True)
    checklist = [
        "我能不能说出本章最常见题型的第一步？",
        "我有没有把本章最容易混的两个概念分开？",
        "我能不能写出本章至少一个完整大题模板？",
        "我有没有确认考试范围内的降权/不考内容？",
    ]
    bullets(d, M + 28, y + 72, checklist, W - 2 * M - 70, color=BLACK)
    source_box(d, 1170, ch.sources)
    return img


def page_6(ch: Chapter) -> Image.Image:
    img, d = new_page(ch, 6, "原题与资料锚点", "旧图只借版式，事实回到当前资料")
    y = 158
    tag(d, M, y, "资料优先级")
    y += 62
    table(d, M, y, W - 2 * M, [
        ("1", "最终复习题、老师划重点、明确考试说明。"),
        ("2", "PPT例题和老师强调内容。"),
        ("3", "习题答案、习题原题、教材例题和课后题。"),
        ("4", "AI补充只做解释，不冒充资料原文。"),
    ], col1=90, row_h=98, core_rows=[0, 1])
    y += 430
    tag(d, M, y, "本章Source")
    y += 62
    card(d, M, y, W - 2 * M, 370, "引用锚点", fill=WHITE, core=True)
    bullets(d, M + 24, y + 65, ch.sources, W - 2 * M - 55, size="small")
    draw_wrapped(d, "提醒：本批PDF继承source-first逻辑；若后续要嵌入原题截图，应回到对应PDF页渲染截图后再替换本页锚点区。", (M + 24, y + 245), F["bodyb"], W - 2 * M - 58, fill=RED)
    return img


def page_7(ch: Chapter) -> Image.Image:
    img, d = new_page(ch, 7, "拔高页：综合与边界", "防止整章只停留在基础选择判断")
    y = 158
    tag(d, M, y, "拔高1")
    y += 62
    adv1, adv2 = ch.advanced[:2]
    card(d, M, y, W - 2 * M, 285, adv1[0], fill=WHITE, core=True)
    draw_wrapped(d, adv1[1], (M + 24, y + 68), F["body"], W - 2 * M - 60, spacing=7)
    draw_mini_circuit(d, W - M - 310, y + 145, 250, 105, int(ch.no) + 1)
    y += 330
    tag(d, M, y, "拔高2")
    y += 62
    card(d, M, y, W - 2 * M, 285, adv2[0], fill=LIGHT, core=True)
    draw_wrapped(d, adv2[1], (M + 24, y + 68), F["body"], W - 2 * M - 60, spacing=7)
    y += 330
    tag(d, M, y, "高区分度提醒")
    y += 62
    card(d, M, y, W - 2 * M, 180, "别只背答案形状", fill=PALE_RED, outline=(235, 175, 175))
    draw_wrapped(d, "拔高题真正考的是：能不能先识别题型边界，再调用对应模板。答案数值不是核心，步骤口令才是稳定得分点。", (M + 24, y + 62), F["bodyb"], W - 2 * M - 60, fill=RED)
    source_box(d, 1210, ch.sources)
    return img


def page_8(ch: Chapter) -> Image.Image:
    img, d = new_page(ch, 8, "答案附页与最后复盘", "题目先做，答案集中看，保留主动回忆")
    y = 158
    tag(d, M, y, "自测答案")
    y += 62
    answer_rows = [(qid, answer) for qid, _, answer in ch.questions[:3]]
    table(d, M, y, W - 2 * M, answer_rows, col1=120, row_h=95, core_rows=[0, 1, 2])
    y += 335
    tag(d, M, y, "最后复盘")
    y += 62
    card(d, M, y, W - 2 * M, 430, "闭卷前必须能复述", fill=LIGHT, core=True)
    recap = [
        f"本章定位：{ch.position}",
        f"本章路线：{' -> '.join(ch.route)}",
        f"最高频陷阱：{ch.traps[0][0]} - {ch.traps[0][1]}",
        f"最该背的口令：{ch.quick[0]}",
    ]
    bullets(d, M + 28, y + 72, recap, W - 2 * M - 70)
    y += 485
    tag(d, M, y, "产物说明")
    y += 62
    card(d, M, y, W - 2 * M, 190, "本PDF用途", fill=WHITE)
    draw_wrapped(d, "这是电路分析期末冲刺专用的分章节复习PDF：用大学物理成功的8页结构，换成电路分析自己的题型口令、考试范围和Source锚点。", (M + 24, y + 58), F["body"], W - 2 * M - 56)
    source_box(d, 1240, ch.sources)
    return img


PAGE_BUILDERS = [page_1, page_2, page_3, page_4, page_5, page_6, page_7, page_8]


def save_pdf(images: list[Image.Image], path: Path) -> None:
    rgb = [img.convert("RGB") for img in images]
    rgb[0].save(path, save_all=True, append_images=rgb[1:], resolution=144.0)


def make_contact_sheet(paths: list[Path], out: Path) -> None:
    thumbs: list[Image.Image] = []
    for path in paths:
        img = Image.open(path).convert("RGB")
        img.thumbnail((220, 310))
        canvas = Image.new("RGB", (240, 330), WHITE)
        canvas.paste(img, ((240 - img.width) // 2, 10))
        thumbs.append(canvas)
    sheet = Image.new("RGB", (4 * 240, 2 * 330), (245, 242, 250))
    for idx, thumb in enumerate(thumbs):
        x = (idx % 4) * 240
        y = (idx // 4) * 330
        sheet.paste(thumb, (x, y))
    sheet.save(out, quality=95)


def write_source_pack(ch: Chapter, out_dir: Path, page_paths: list[Path], pdf: Path, contact: Path) -> None:
    lines = [
        f"# 第{ch.no}章 {ch.title} 期末冲刺专用版 source pack",
        "",
        "## 结论",
        "",
        "本章按大学物理成功版的8页结构生成：总图、一小时路线、核心概念、大题模板、小题陷阱、A4速查、拔高页、答案附页。",
        "视觉风格继承电路分析第13章样章的紫色分块、红色核心提醒和页脚Source结构；事实来源回到本项目当前资料索引。",
        "",
        "## 考试边界",
        "",
        f"- 范围：{ch.scope}",
        f"- 定位：{ch.position}",
        "",
        "## 页序",
        "",
    ]
    for i, path in enumerate(page_paths, 1):
        lines.append(f"{i}. {path.name}")
    lines += [
        "",
        "## 输出",
        "",
        f"- PDF：{pdf}",
        f"- 总览图：{contact}",
        "",
        "## Source",
        "",
        *[f"- {source}" for source in ch.sources],
        "",
    ]
    (out_dir / "source_pack.md").write_text("\n".join(lines), encoding="utf-8")


def build_chapter(ch: Chapter) -> dict[str, str | int]:
    out_dir = OUT_ROOT / f"第{ch.no}章_{ch.title}"
    pages_dir = out_dir / "pages"
    preview_dir = out_dir / "preview"
    final_dir = out_dir / "final_pdf"
    for p in [pages_dir, preview_dir, final_dir, PDF_OUT]:
        p.mkdir(parents=True, exist_ok=True)

    images = [builder(ch) for builder in PAGE_BUILDERS]
    page_paths: list[Path] = []
    for idx, img in enumerate(images, 1):
        path = pages_dir / f"ch{ch.no}_p{idx:02d}_sprint.png"
        img.save(path, quality=95)
        page_paths.append(path)

    final_pdf = final_dir / ch.pdf_name
    save_pdf(images, final_pdf)
    copied_pdf = PDF_OUT / ch.pdf_name
    shutil.copyfile(final_pdf, copied_pdf)

    contact = preview_dir / f"第{ch.no}章_{ch.title}_8p_contact_sheet.png"
    make_contact_sheet(page_paths, contact)
    write_source_pack(ch, out_dir, page_paths, copied_pdf, contact)

    return {
        "chapter": ch.no,
        "title": ch.title,
        "pages": len(page_paths),
        "pdf": str(copied_pdf),
        "contact_sheet": str(contact),
        "source_pack": str(out_dir / "source_pack.md"),
    }


def write_memory(results: list[dict[str, str | int]]) -> None:
    MEMORY.parent.mkdir(parents=True, exist_ok=True)
    existing = MEMORY.read_text(encoding="utf-8") if MEMORY.exists() else "# 2026-06-21 电路分析 memory\n\n"
    marker = "## 电路分析期末冲刺分章节PDF批量生成"
    if marker in existing:
        existing = existing.split(marker)[0].rstrip() + "\n\n"
    lines = [
        marker,
        "",
        "### 结论",
        "",
        "已生成电路分析期末冲刺专用版分章节PDF，统一汇总到 `outputs/PDF`。本轮迁移大学物理成功结构：每章8页、含A4速查、拔高页、答案附页和总览图；视觉采用电路分析第13章样章的紫色分块+红色核心提醒。",
        "",
        "### 产物",
        "",
    ]
    for item in results:
        lines.append(f"- 第{item['chapter']}章 {item['title']}：{item['pdf']}；页数：{item['pages']}；总览图：{item['contact_sheet']}")
    lines += [
        "",
        "### 经验教训",
        "",
        "- 章节PDF最有效的结构不是长篇摘要，而是：定位 -> 概念边界 -> 题型模板 -> 陷阱 -> A4速查 -> 拔高 -> 答案。",
        "- 第16章按项目规则降权，只做选择/判断概念，不做复杂计算主线。",
        "- 若后续升级为严格原题截图融合版，应从每章 `原来/` PDF 渲染对应题图，替换当前Source锚点页。",
        "",
        "Source: CLAUDE.md#期末原题复现型复习引擎",
        "Source: SOPs/06_复习PDF制作SOP.md#PDF / 图片制作流程",
        "",
    ]
    MEMORY.write_text(existing + "\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    PDF_OUT.mkdir(parents=True, exist_ok=True)
    results = [build_chapter(ch) for ch in CHAPTERS]
    write_memory(results)
    manifest = OUT_ROOT / "manifest.json"
    manifest.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
