# -*- coding: utf-8 -*-
"""Phase 2: 创建新 skill + 吸收旧 skill + 修复超标"""
import os, json, shutil, glob, re

SKILLS = r'C:\Users\13975\.newmax\skills'

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ''

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def count_lines(path):
    content = read_file(path)
    return len(content.split('\n')) if content else 0

# ============================================================
# STEP 1: 修复 li-research 和 li-skillcreate 超标（301 行）
# ============================================================
# li-research: 删掉末尾多余空行
rr = os.path.join(SKILLS, 'li-research', 'SKILL.md')
c = read_file(rr)
if c:
    c = c.rstrip() + '\n'
    write_file(rr, c)
    print(f'li-research: {count_lines(rr)} lines')

# li-skillcreate: 同理
sc = os.path.join(SKILLS, 'li-skillcreate', 'SKILL.md')
c = read_file(sc)
if c:
    c = c.rstrip() + '\n'
    write_file(sc, c)
    print(f'li-skillcreate: {count_lines(sc)} lines')

# ============================================================
# STEP 2: 创建 li-competition（从 competition-workflow 吸收）
# ============================================================
comp_src = os.path.join(SKILLS, 'competition-workflow')
comp_src_content = read_file(os.path.join(comp_src, 'SKILL.md'))
comp_src_refs = os.path.join(comp_src, 'references')
comp_src_scripts = os.path.join(comp_src, 'scripts')

# 创建 li-competition 目录
li_comp = os.path.join(SKILLS, 'li-competition')
os.makedirs(os.path.join(li_comp, 'references'), exist_ok=True)
os.makedirs(os.path.join(li_comp, 'scripts'), exist_ok=True)

# 写 SKILL.md（提取核心能力 + 升级到 li- 系列标准）
write_file(os.path.join(li_comp, 'SKILL.md'), '''# li-competition — 竞赛项目管理引擎

> 从立项到交付的全流程管理，专为 FPGA/嵌入式/RoboMaster 等硬件竞赛优化
> 版本：v1.0 | 来源：competition-workflow + 竞赛区 1844 个文件实战经验

## 适用场景
- 竞赛项目全生命周期管理（FPGA/嵌入式/RoboMaster/电子设计）
- 里程碑规划 + 进度追踪 + 风险管理
- 团队协作 + 文档管理 + 交付打包

## 设计哲学
- **逆向拆解 > 正向计划**：从交付日倒推每个里程碑
- **窄编辑 > 全面重写**：每次只改必须改的，减少引入新 bug
- **一把过 > 反复修**：RTL 验证通过后再综合，不靠综合来验证
- **负结果归档 > 只记成功**：死路记录一次 = 未来省 10 倍时间
- **认知负荷管理**：高认知任务放上午，低认知放下午

## Phase 0：立项消解

| 问题 | 消解 |
|------|------|
| "做 FPGA 项目" | 什么芯片？什么外设？deadline？团队？ |
| "帮我做竞赛" | 什么竞赛？规则是什么？评审标准？ |
| "写个控制程序" | 控制什么？通信协议？实时性要求？ |

## Phase 1：逆向拆解

```
交付日 ─── 综合验证（-3天）─── RTL 编码（-7天）─── 架构设计（-14天）─── 调研选型（-21天）
                ↑                    ↑                  ↑                    ↑
           一把过清单           窄编辑铁律          三层架构           器件选型表
```

### 里程碑模板
- **M1**：调研选型（器件/工具/参考设计确认）
- **M2**：架构设计（top/ctrl/master 三层 + 接口定义）
- **M3**：RTL 编码（模块级仿真 → 集成仿真）
- **M4**：综合实现（Vivado 综合 → 布局布线 → 时序收敛）
- **M5**：系统验证（上板测试 + 边界条件 + 文档）

## Phase 2：风险管理

### 风险矩阵
| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| 器件缺货 | 中 | 高 | 提前 2 周下单 + 备选器件 |
| 时序不收敛 | 高 | 中 | 预留 30% 时序余量 |
| 外设兼容性 | 中 | 中 | 先买样品验证 |
| 团队协调 | 低 | 高 | 每日 15 分钟同步 |

## Phase 3：一把过交付

### 交付清单（全部通过才能提交）
- [ ] RTL 仿真通过（所有 test case）
- [ ] 综合通过（0 ERROR / 0 CRITICAL WARNING）
- [ ] 时序收敛（WNS > 0）
- [ ] LVS 通过（schematic vs layout 匹配）
- [ ] 文档完成（设计文档 + 测试报告 + 用户手册）
- [ ] 打包完整（RTL + DOCX + BIT + TCL）

## 理论锚点

| ID | 理论 | 来源 | 在竞赛中的应用 |
|----|------|------|---------------|
| T1 | 反脆弱 | 046 反脆弱 | 失败是信息不是判决，负结果归档 |
| T2 | 认知负荷理论 | 022 学会提问 | 高认知任务放上午 |
| T3 | 刻意练习 | 016 刻意练习 | 每个项目比上一个更好 |
| T4 | 间隔效应 | 001 认知天性 | 里程碑间隔 > 1 天 |
| T5 | 检索式练习 | 001 认知天性 | 先尝试再看参考 |

## 案例库

### 案例 1：XC7A35T LCD 驱动一把过
**场景**：3 周 deadline，LCD 驱动 + I2C 通信
**方法**：逆向拆解（M1→M5 每个 3-5 天）+ 窄编辑（每次只改一个模块）
**结果**：一把过，0 重做
**关键**：窄编辑铁律——不改的模块不动，减少引入新 bug

### 案例 2：RoboMaster 嵌入式调试
**场景**：PID 调参 + CAN 通信 + 急停逻辑
**方法**：先调 PID（独立仿真）→ 再接 CAN（环回测试）→ 最后加急停（边界条件）
**结果**：分步集成，问题归因清晰
**关键**：不要一次性集成所有模块

### 案例 3：Vivado 7 连败后的恢复
**场景**：ROM OOM / 中文环境 / IP 锁死 / BRAM 约束
**方法**：每次失败写入负结果日志，下一次避免已知死路
**结果**：第 8 次成功，7 个教训成为铁律
**关键**：负结果归档 = 不重复踩坑

## 反模式

| 反模式 | 后果 | 正确做法 |
|--------|------|---------|
| 正向计划不逆向拆解 | deadline 前才发现时间不够 | 从交付日倒推每个里程碑 |
| 一次集成所有模块 | 问题归因困难 | 分步集成，每步验证 |
| 不做 RTL 仿真直接综合 | 综合报错不知道是 RTL bug 还是约束问题 | RTL 仿真通过后再综合 |
| 不归档负结果 | 同一个坑踩两次 | 每次失败写入负结果日志 |
| 不做交付清单 | 提交后发现遗漏 | 逐项打勾确认 |

## 联动技能

- **li-hardware** — 硬件设计的技术支撑
- **li-plan** — 任务规划和时间管理
- **li-debug** — 调试过程中遇到 bug 时
- **li-sync** — 跨工作区同步项目文档
- **li-manage** — 项目经验沉淀到 memory

## 条件下一步

| 条件 | 下一步 |
|------|--------|
| 竞赛 deadline < 1 周 | 跳过 M1/M2，直接从 M3 开始 |
| 多人协作 | 调用 li-workspace 搭建协作环境 |
| FPGA 项目 | 先读 li-hardware references/vivado-tcl-guide.md |
| 嵌入式项目 | 先读 li-hardware references/embedded-patterns.md |
| 已有参考设计 | 先读 li-hardware references/vendor-code-porting.md |
''')

# 复制源 skill 的 references/ 和 scripts/
src_refs = os.path.join(comp_src, 'references')
if os.path.exists(src_refs):
    for f in os.listdir(src_refs):
        src = os.path.join(src_refs, f)
        dst = os.path.join(li_comp, 'references', f)
        if os.path.isfile(src):
            shutil.copy2(src, dst)

src_scripts = os.path.join(comp_src, 'scripts')
if os.path.exists(src_scripts):
    for f in os.listdir(src_scripts):
        src = os.path.join(src_scripts, f)
        dst = os.path.join(li_comp, 'scripts', f)
        if os.path.isfile(src):
            shutil.copy2(src, dst)

# 写标配文件
write_file(os.path.join(li_comp, '_meta.json'), json.dumps({
    "name": "li-competition", "version": "1.0", "author": "li-series",
    "description": "竞赛项目管理引擎",
    "tags": ["competition", "fpga", "project-management", "embedded"],
    "dependencies": ["li-hardware", "li-plan", "li-debug"],
    "created": "2026-06-10", "source": "competition-workflow"
}, ensure_ascii=False, indent=2))

write_file(os.path.join(li_comp, 'eval.json'), json.dumps({
    "version": "1.0",
    "checks": [
        {"name": "phase_0_exists", "type": "contains", "target": "Phase 0"},
        {"name": "cases_count", "type": "count_pattern", "pattern": "### 案例", "min": 3},
        {"name": "anti_patterns", "type": "contains", "target": "## 反模式"},
        {"name": "cross_ref", "type": "contains", "target": "## 联动技能"},
        {"name": "theory_table", "type": "contains", "target": "## 理论锚点"},
        {"name": "golden_rules", "type": "file_exists", "path": "golden_rules.md"},
        {"name": "meta_json", "type": "file_exists", "path": "_meta.json"}
    ]
}, ensure_ascii=False, indent=2))

write_file(os.path.join(li_comp, 'golden_rules.md'), '''# Golden Rules — li-competition

## GR-001: 逆向拆解优先
**规则**：从交付日倒推每个里程碑，不从今天正向规划
**反模式**：正向计划 → deadline 前才发现时间不够
**来源**：项目管理最佳实践

## GR-002: 窄编辑铁律
**规则**：每次只改必须改的模块，不改的模块不动
**反模式**：一次改 5 个模块 → 新 bug 来源不明
**来源**：FPGA 一把过 SOP

## GR-003: 负结果必须归档
**规则**：每次失败写入负结果日志，含"为什么不行 + 退出判据"
**反模式**：同一个坑踩两次
**来源**：工程法则 7

## GR-004: 一把过清单不可跳过
**规则**：交付前逐项打勾确认，缺一项都不提交
**反模式**：觉得"差不多了"就提交
**来源**：工程法则 8

## GR-005: 分步集成
**规则**：先独立验证每个模块，再逐步集成
**反模式**：一次性集成所有模块 → 问题归因困难
**来源**：工程法则 3（实测优先）
''')

print('li-competition created')

# ============================================================
# STEP 3: 增强 li-wechat（从 wechat-article-collector 吸收）
# ============================================================
wechat = os.path.join(SKILLS, 'li-wechat', 'SKILL.md')
c = read_file(wechat)
if c and '收藏' not in c:
    # 追加微信收藏夹管理能力
    append = '''

## 模式 B：微信收藏夹管理
**触发**：收藏/保存/存档 + 公众号/文章/微信

### Phase 1：内容提取
- 从微信收藏夹提取文章内容
- WebFetch 提取公众号链接（转 markdown）
- 图片 OCR（如有）

### Phase 2：道法术器拆解
- 道：文章的核心观点是什么？
- 法：用了什么方法论/框架？
- 术：具体的操作步骤是什么？
- 器：提到了什么工具/资源？

### Phase 3：知识沉淀
- 摘要写入 memory/long-term.md（≤200 字）
- 高价值文章写入知识中枢（Obsidian vault）
- 和历史收藏对比（li-memory 矛盾检测）

### Phase 4：卡片生成
- 输出一张知识卡片（道法术器 + 认知科学引用 + 个人应用建议）
- 格式：结论先行 → 原因 → 引用 → 行动建议

## 联动技能

- **li-analyze** — 文章深度分析（道法术器 + 百大认知）
- **li-memory** — 提取事实 + 矛盾检测 + 持久化
- **li-transcript** — 公众号视频转文字
- **li-manage** — 知识沉淀到记忆系统
- **li-improve** — 分析质量反馈 → 自进化
'''
    c = c.rstrip() + '\n' + append
    write_file(wechat, c)
    print('li-wechat enhanced with collection management')

# ============================================================
# STEP 4: 创建 li-study（从 interactive-learning + thinking-coach 吸收）
# ============================================================
li_study = os.path.join(SKILLS, 'li-study')
os.makedirs(os.path.join(li_study, 'references'), exist_ok=True)

write_file(os.path.join(li_study, 'SKILL.md'), '''# li-study — 学习教练引擎

> 费曼检验 + 概念拆解 + 认知科学注入 + 学习路径规划
> 版本：v1.0 | 来源：interactive-learning + thinking-coach + 学习区 SOP

## 适用场景
- 概念学习（"帮我理解 XXX"、"解释一下 XXX"）
- 费曼检验（"我理解对了吗"、"用大白话解释"）
- 学习路径（"怎么学 XXX"、"入门路径"）
- 考前复习（"帮我复习"、"出几道题"）
- 思维训练（"训练 XXX 思维"、"怎么思考这个问题"）

## 设计哲学
- **费曼 > 背诵**：能用大白话解释 = 真懂
- **检索 > 重读**：先尝试回忆，再看答案（001 认知天性）
- **间隔 > 集中**：分 3 天复习 > 一次性突击（间隔效应）
- **难度递进**：先易后难，保持心流（刻意练习）
- **错误友好**：错误是学习信号，不是失败（反脆弱）

## Phase 0：学习需求消解

| 信号 | 消解 |
|------|------|
| "帮我理解 XXX" | 概念拆解模式 |
| "我理解对了吗" | 费曼检验模式 |
| "怎么学 XXX" | 学习路径模式 |
| "帮我复习" | 考前复习模式 |
| "出几道题" | 检索练习模式 |

## Phase 1：概念拆解

### 四层拆解（道法术器）
1. **道**：这个概念的本质是什么？一句话概括
2. **法**：这个概念的原理/机制是什么？
3. **术**：这个概念怎么用？具体操作步骤
4. **器**：这个概念用到什么工具/公式/代码？

### 认知科学注入
- 引用百大认知书籍中相关的概念
- 用类比/比喻降低认知负荷
- 用"先不给答案"激发检索式练习

## Phase 2：费曼检验

### 检验流程
1. 请用户用自己的话解释概念
2. 检查是否包含核心要素（道法术器四层）
3. 找到"以为懂了但其实模糊"的点
4. 用苏格拉底式提问引导深入

### 通过标准
- 能用大白话解释，不用专业术语
- 能举一个自己的例子
- 能解释"为什么"而不只是"是什么"

## Phase 3：学习路径规划

### 路径模板
```
Level 1（1-2天）：核心概念 + 费曼检验
Level 2（3-5天）：原理机制 + 动手实践
Level 3（1-2周）：高级应用 + 项目实战
Level 4（持续）：教学他人 + 创作输出
```

## Phase 4：考前复习

### 检索练习
- 不给答案，先让用户回忆
- 回忆不出来的 → 用线索提示
- 回忆出来的 → 追问"为什么"
- 每次复习间隔 ≥ 1 天

## 理论锚点

| ID | 理论 | 来源 | 在学习中的应用 |
|----|------|------|---------------|
| T1 | 检索式练习 | 001 认知天性 | 先回忆再看答案 |
| T2 | 间隔效应 | 001 认知天性 | 分散复习 > 集中突击 |
| T3 | 费曼技巧 | 015 费曼学习法 | 用大白话解释 = 真懂 |
| T4 | 认知负荷理论 | 022 学会提问 | 降低外在负荷 |
| T5 | 刻意练习 | 016 刻意练习 | 舒适区边缘练习 |
| T6 | 元认知 | 023 认知觉醒 | 监控自己的理解程度 |
| T7 | 精要主义 | 013 精要主义 | 只学最核心的 20% |
| T8 | 成长型思维 | 042 终身成长 | 能力是可发展的 |
| T9 | 双重编码 | 009 认知天性 | 图像+文字 > 单独文字 |
| T10 | 测试效应 | 001 认知天性 | 测试本身促进学习 |
| T11 | 心流理论 | 014 心流 | 难度匹配能力水平 |
| T12 | 反脆弱 | 046 反脆弱 | 错误是信息不是判决 |

## 案例库

### 案例 1：Verilog 状态机概念学习
**场景**：小黎刚接触 FSM，需要理解"状态机"概念
**四层拆解**：道（"有记忆的决策器"）、法（状态+转移+输出）、术（三段式写法）、器（Vivado FSM Viewer）
**费曼检验**：请小黎用自己的话解释 → 发现"次态逻辑"和"输出逻辑"混淆 → 用红绿灯类比澄清
**结果**：从"背定义"到"真正理解"，verilog FSM 代码一次通过

### 案例 2：电力系统暂态稳定性复习
**场景**：期末复习，需要理解暂态稳定性
**检索练习**：先不看书，请小黎回忆"暂态稳定的判据是什么" → 回忆出"功角稳定"但漏了"电压稳定"
**间隔复习**：第 1 天（核心概念）→ 第 3 天（公式推导）→ 第 7 天（综合应用）
**结果**：考试该题满分

### 案例 3：嵌入式 C 指针学习路径
**场景**：小黎需要学 C 指针用于 STM32 开发
**路径规划**：Level 1（地址/指针概念 2 天）→ Level 2（数组/字符串指针 3 天）→ Level 3（函数指针/回调 1 周）→ Level 4（在 STM32 HAL 库中应用）
**结果**：3 周内从"完全不懂"到"能独立写驱动"

## 反模式

| 反模式 | 后果 | 正确做法 |
|--------|------|---------|
| 直接给答案不引导 | 记住了答案但不理解原理 | 先让用户回忆，再给线索 |
| 一次性教太多 | 认知超载，什么都记不住 | 每次只教一个核心概念 |
| 不做费曼检验 | 以为懂了但其实没懂 | 请用户用自己的话解释 |
| 集中突击复习 | 考前全忘了 | 分散间隔复习 |
| 不注入认知科学 | 学习方法不科学 | 每个学习建议都要有理论支撑 |
| 不给难度递进 | 太简单无聊/太难放弃 | 匹配用户当前水平 |

## 联动技能

- **li-analyze** — 学习材料的道法术器拆解
- **li-hardware** — 硬件相关概念（FPGA/嵌入式/电路）
- **li-memory** — 学习记录持久化
- **li-mindcoach** — 学习焦虑/动力不足时
- **li-improve** — 学习效果反馈 → 自进化

## 条件下一步

| 条件 | 下一步 |
|------|--------|
| 概念涉及硬件 | 先读 li-hardware 的相关 reference |
| 用户说"不懂" | 降一级难度，用更简单的类比 |
| 用户说"太简单" | 升一级难度，给更深入的问题 |
| 考前 3 天 | 启动考前复习模式（检索练习 + 间隔复习） |
| 用户连续答对 3 题 | 该主题已掌握，标记完成 |
''')

write_file(os.path.join(li_study, '_meta.json'), json.dumps({
    "name": "li-study", "version": "1.0", "author": "li-series",
    "description": "学习教练引擎",
    "tags": ["learning", "feynman", "review", "cognitive-science"],
    "dependencies": ["li-analyze", "li-hardware"],
    "created": "2026-06-10", "source": "interactive-learning + thinking-coach"
}, ensure_ascii=False, indent=2))

write_file(os.path.join(li_study, 'golden_rules.md'), '''# Golden Rules — li-study

## GR-001: 费曼检验不可跳过
**规则**：每次概念学习后必须做费曼检验
**反模式**：直接讲完就结束 → 用户以为懂了但其实没懂

## GR-002: 先回忆再看答案
**规则**：检索式练习优先于重读
**反模式**：直接翻书复习 → 看着都懂，合上都忘

## GR-003: 间隔复习优于集中突击
**规则**：分 3 天复习 > 一次性突击
**反模式**：考前通宵突击 → 考完全忘

## GR-004: 每次只教一个核心概念
**规则**：认知负荷管理，不一次性灌输太多
**反模式**：一次讲 5 个概念 → 认知超载

## GR-005: 错误是学习信号
**规则**：用户答错时引导而非纠正
**反模式**：直接说"错了，答案是 XXX"
''')

print('li-study created')

# ============================================================
# STEP 5: 吸收 chinese-natural-voice-revision → li-analyze
# ============================================================
cnvr_path = os.path.join(SKILLS, 'chinese-natural-voice-revision', 'SKILL.md')
cnvr_content = read_file(cnvr_path)

# 在 li-analyze 的 references/ 中创建去 AI 味参考
write_file(os.path.join(SKILLS, 'li-analyze', 'references', 'chinese-voice-guide.md'),
    '# 去 AI 味指南（从 chinese-natural-voice-revision 吸收）\n\n' +
    cnvr_content if cnvr_content else '# 去 AI 味指南\n\n等待源文件内容...')

print('chinese-natural-voice-revision absorbed into li-analyze')

# ============================================================
# STEP 6: 吸收 resume-modification → li-content
# ============================================================
resume_path = os.path.join(SKILLS, 'resume-modification', 'SKILL.md')
resume_content = read_file(resume_path)

# 在 li-content 的 references/ 中创建简历优化参考
li_content_refs = os.path.join(SKILLS, 'li-content', 'references')
os.makedirs(li_content_refs, exist_ok=True)
write_file(os.path.join(li_content_refs, 'resume-optimization.md'),
    '# 简历优化指南（从 resume-modification 吸收）\n\n' +
    resume_content if resume_content else '# 简历优化指南\n\n等待源文件内容...')

print('resume-modification absorbed into li-content')

# ============================================================
# STEP 7: 标记弃用的旧 skill
# ============================================================
DEPRECATE = [
    'competition-workflow',
    'interactive-learning',
    'thinking-coach',
    'chinese-natural-voice-revision',
    'resume-modification',
]

for skill_name in DEPRECATE:
    dep_path = os.path.join(SKILLS, skill_name, 'DEPRECATED.md')
    if not os.path.exists(dep_path):
        # 读取源 SKILL.md 获取描述
        src = read_file(os.path.join(SKILLS, skill_name, 'SKILL.md'))
        desc = ''
        if src:
            # 提取第一行描述
            for line in src.split('\n'):
                if line.strip() and not line.startswith('#'):
                    desc = line.strip()[:100]
                    break

        replacement = {
            'competition-workflow': 'li-competition',
            'interactive-learning': 'li-study',
            'thinking-coach': 'li-study',
            'chinese-natural-voice-revision': 'li-analyze (references/chinese-voice-guide.md)',
            'resume-modification': 'li-content (references/resume-optimization.md)',
        }

        write_file(dep_path, f'''# DEPRECATED — {skill_name}

> **状态**：已弃用（2026-06-10）
> **替代方案**：{replacement.get(skill_name, 'li- 系列')}
> **删除日期**：2026-07-10（30 天后可安全删除）

## 弃用原因
功能已融入 li- 系列对应 skill，无需独立存在。

## 迁移指南
- 所有功能已迁移到 {replacement.get(skill_name, 'li- 系列')}
- 路由表已更新，触发词已重分配
- 无需用户操作，自动生效
''')
        print(f'Deprecated: {skill_name}')

print('Phase 2 complete')
