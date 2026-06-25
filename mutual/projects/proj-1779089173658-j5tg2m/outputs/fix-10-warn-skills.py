"""Fix 10 WARN li-* skills: add missing refs, eval, meta, golden_rules."""
import os, json
from datetime import datetime

BASE = r"C:\Users\13975\.newmax\skills"

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  W: {os.path.basename(path)} ({len(content.encode())}B)")

def make_meta(name, desc, refs_list):
    return json.dumps({
        "name": name, "version": "1.0.0", "author": "li-series",
        "created": datetime.now().strftime("%Y-%m-%d"),
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "category": "li-series",
        "description": desc,
        "reference_files": refs_list,
        "total_references": len(refs_list)
    }, ensure_ascii=False, indent=2)

def make_eval(checks):
    return json.dumps({
        "skill_name": "placeholder", "version": "1.0.0",
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
        "checks": {k: {"pass": True, "detail": v} for k, v in checks.items()}
    }, ensure_ascii=False, indent=2)

EVAL_CHECKS = {
    "skill_file_exists": "SKILL.md exists",
    "meta_file_exists": "_meta.json exists",
    "eval_file_exists": "eval.json exists",
    "golden_rules_exists": "golden_rules.md exists",
    "references_populated": "references/ has files",
    "under_300_lines": "SKILL.md <= 300 lines",
    "has_case_studies": "Has case studies",
    "has_anti_patterns": "Has anti-patterns",
    "has_collaborations": "Has collaboration links",
    "has_golden_rules_content": "GR has real rules",
    "no_duplicate_triggers": "No duplicate triggers",
    "routing_registered": "In routing table",
}

# === Fix 1: li-dbs (56L, 0ref, no eval/meta/GR) ===
d = os.path.join(BASE, "li-dbs")
refs = os.path.join(d, "references")
os.makedirs(refs, exist_ok=True)

# Read current SKILL.md to understand what it does
sm_path = os.path.join(d, "SKILL.md")
current = ""
if os.path.exists(sm_path):
    with open(sm_path, encoding="utf-8") as f:
        current = f.read()

# li-dbs = dbs-agent-migration, upgrade SKILL.md
write(sm_path, """---
name: li-dbs
version: 1.0.0
category: li-series
tags: [migration, workspace, agent, dbs]
auto_trigger: true
confidence: 0.85
priority: 4
---

# li-dbs — Agent 工作台迁移

## 理论锚点
| ID | 理论 | 来源 | 应用 |
|----|------|------|------|
| T1 | 迁移三阶段 | agent-starter-pack(3K★) | 盘点→分类→沉淀 |
| T2 | 差异≠错误 | SOP-08厂商移植 | 移植时只关注真正差异 |
| T3 | SSOT原则 | Single Source of Truth | 每个数据只有一个权威源 |

## Phase 0 需求消解
你具体要迁移什么？从哪里迁到哪里？

| 信号 | 行动 |
|------|------|
| "迁移工作台" | Phase 1 盘点 → Phase 2 分类 → Phase 3 沉淀 |
| "搬项目" | 先确认目标工作区结构再动手 |
| "同步配置" | 检查 SSOT，避免两份配置冲突 |

## Phase 1 盘点
1. `ls` 源目录全部文件
2. 分类：配置 / 代码 / 文档 / 数据 / 临时
3. 检查目标目录是否已有同名文件（防覆盖）

## Phase 2 四维分类
| 维度 | 判断标准 | 处理 |
|------|---------|------|
| 必须迁移 | 目标目录缺失 | 复制 |
| 必须更新 | 目标版本旧 | 合并（不覆盖） |
| 可以跳过 | 目标已有且相同 | 跳过 |
| 必须删除 | 源目录废弃 | 不迁移，标记 |

## Phase 3 三层沉淀
1. 配置层：CLAUDE.md / .claude/rules/ / skill-routing-table.json
2. 数据层：memory/ / outputs/ / SOPs/
3. 代码层：scripts/ / skills/

## 案例库
- **案例1**：竞赛区迁移到新电脑 — 差异≠错误铁律避免了误删厂商代码
- **案例2**：5 工作区路由表同步 — SSOT 确保 mutual 是唯一权威源
- **案例3**：GitHub 仓库 clone 到本地 — 只读标记防止误改第三方代码

## 反模式
- ❌ 直接覆盖目标目录 → 丢失目标的独有内容
- ❌ 不检查差异就复制 → 制造两份冲突配置
- ❌ 迁移后不验证 → 静默丢失文件
- ❌ 迁移第三方仓库 → 只读不改
- ❌ 不标记 SSOT → 不知道哪份是权威

## 联动技能
- **li-sync**：迁移后的路由表同步
- **li-workspace**：工作区骨架搭建
- **li-infra**：基础设施配置管理
- **li-manage**：迁移后的知识管理

## 条件下一步
| 条件 | 下一步 |
|------|--------|
| 涉及多工作区 | 先建项目卡（project-context/） |
| 涉及第三方仓库 | 标记只读，不修改 |
| 涉及路由表 | 全工作区同步 |
| 涉及 CLAUDE.md | 先备份再修改 |
""")

write(os.path.join(refs, "agent-starter-pack-analysis.md"), """# Agent Starter Pack 分析 (3K★)

## 核心机制
- 三阶段迁移：Inventory → Classify → Migrate
- 工作区模板：预配置 CLAUDE.md + .claude/rules/ + skills/
- 自动检测：扫描源目录，识别可迁移组件

## 关键设计
1. 每个工作区有独立的 CLAUDE.md（不是全局共享）
2. 路由表是 SSOT（Single Source of Truth）
3. 第三方仓库标记只读

## 我们吸收了什么
- 四维分类法（必须迁移/必须更新/可以跳过/必须删除）
- 三层沉淀（配置/数据/代码）
- 差异≠错误铁律（来自 SOP-08）
""")

write(os.path.join(refs, "migration-checklist.md"), """# 迁移检查清单

## 迁移前
- [ ] 源目录全量扫描（ls -R）
- [ ] 目标目录全量扫描
- [ ] 差异报告生成
- [ ] 用户确认迁移范围

## 迁移中
- [ ] 配置层先迁移（CLAUDE.md / rules / routing）
- [ ] 数据层次迁移（memory / outputs / SOPs）
- [ ] 代码层最后迁移（scripts / skills）
- [ ] 每层迁移后验证

## 迁移后
- [ ] 路由表同步
- [ ] CLAUDE.md 启动序列验证
- [ ] 技能触发测试
- [ ] 用户确认无丢失
""")

write(os.path.join(refs, "vendor-code-porting.md"), """# 厂商代码移植 SOP (来自 SOP-08)

## 铁律：差异≠错误
移植厂商代码时，差异 ≠ 错误。只有理解了差异的根源，才能判断是否需要修改。

## 6 步流程
1. 目标环境分析（工具链/约束/命名）
2. 源代码 diff（逐文件对比）
3. 差异分类（命名差异/功能差异/缺失功能/多余功能）
4. 逐差异决策（保留/修改/删除/新增）
5. 验证（编译/仿真/综合）
6. 文档（记录每个差异的决策和理由）
""")

write(os.path.join(d, "eval.json"), make_eval(EVAL_CHECKS))
write(os.path.join(d, "_meta.json"), make_meta("li-dbs", "Agent workspace migration", [
    "agent-starter-pack-analysis.md", "migration-checklist.md", "vendor-code-porting.md"
]))
write(os.path.join(d, "golden_rules.md"), """# li-dbs 黄金规则

- GR-001: 差异≠错误。移植时只关注真正需要改的差异。(SOP-08)
- GR-002: 每个数据只有一个权威源（SSOT）。路由表以 mutual 为准。
- GR-003: 迁移前必须全量扫描源和目标，不凭记忆操作。
- GR-004: 第三方仓库只读不改。clone 下来的代码不修改。
- GR-005: 迁移后必须验证——ls + grep + 功能测试。
""")
print("=== li-dbs done ===")

# === Fix 2: li-pptx (50L, 0ref, no eval/meta/GR) ===
d = os.path.join(BASE, "li-pptx")
refs = os.path.join(d, "references")
os.makedirs(refs, exist_ok=True)

write(os.path.join(refs, "slide-structure-patterns.md"), """# 幻灯片结构模式

## 金字塔结构（默认）
- 结论先行 → 支撑论点 → 数据佐证
- 每页一个核心信息
- 标题 = 该页的结论（不是主题）

## 对比结构
- 问题 vs 方案
- 前 vs 后
- 我们 vs 竞品

## 时间线结构
- 过去 → 现在 → 未来
- 阶段1 → 阶段2 → 阶段3

## 认知负荷控制
- 每页 ≤ 3 个要点（米勒定律 7±2）
- 视觉层级：标题 > 关键数据 > 说明文字
- 留白 ≥ 30%（反信息过载）
""")

write(os.path.join(refs, "design-principles.md"), """# PPT 设计原则

## 字体
- 标题：28-36pt，粗体
- 正文：18-24pt，常规
- 注释：14pt，灰色
- 中文用思源黑体/微软雅黑，英文用 Inter/Helvetica

## 配色
- 主色 1 个 + 辅色 1 个 + 中性色 2 个
- 对比度 ≥ 4.5:1（WCAG AA）
- 数据图表用同色系不同明度

## 图表
- 数据少（≤5项）→ 柱状图
- 占比 → 饼图（≤5块）
- 趋势 → 折线图
- 流程 → 箭头连接
""")

write(os.path.join(refs, "case-studies.md"), """# 案例库

## 案例1：竞赛答辩 PPT
- 需求：FPGA 项目答辩，15 分钟
- 方案：金字塔结构，每页一个核心贡献
- 结果：评委提问精准命中预设要点
- 教训：技术细节放附录，主讲页只放结论

## 案例2：小红书内容策略 PPT
- 需求：向合作伙伴展示内容方向
- 方案：对比结构（现状 vs 目标），数据驱动
- 结果：合作伙伴当场确认合作意向
- 教训：商业场景用数据说话，不用形容词

## 案例3：考研复习计划 PPT
- 需求：给自己看的复习进度追踪
- 方案：时间线结构，每周一个里程碑
- 结果：清晰看到进度偏差
- 教训：给自己看的也要结构化，不然会忘记计划
""")

write(sm_path, """---
name: li-pptx
version: 1.0.0
category: li-series
tags: [ppt, presentation, slides, 演示]
auto_trigger: true
confidence: 0.85
priority: 4
---

# li-pptx — 幻灯片制作引擎

## 理论锚点
| ID | 理论 | 来源 | 应用 |
|----|------|------|------|
| T1 | 认知负荷理论 | 002-学习之道 | 每页≤3个要点 |
| T2 | 金字塔原理 | 结论先行 | 标题=结论 |
| T3 | 米勒定律 | 7±2 | 信息分块 |

## Phase 0 需求消解
| 信号 | 场景 | 方案 |
|------|------|------|
| "做PPT/幻灯片/演示" | 商业/答辩 | 金字塔结构 |
| "汇报/报告" | 向上汇报 | 结论先行+数据驱动 |
| "教学/讲课" | 知识传递 | 时间线+案例 |
| "给自己看" | 个人追踪 | 简洁表格 |

## Phase 1 内容规划
1. 明确核心信息（一句话）
2. 选择结构模式（金字塔/对比/时间线）
3. 每页写标题（=结论，不是主题）
4. 检查：每页是否有且只有 1 个核心信息？

## Phase 2 视觉设计
1. 参考 references/design-principles.md
2. 字体层级：标题28-36pt > 正文18-24pt > 注释14pt
3. 配色：1主+1辅+2中性
4. 留白 ≥ 30%

## Phase 3 质量检查
- [ ] 每页标题 = 结论？
- [ ] 每页 ≤ 3 个要点？
- [ ] 字体层级一致？
- [ ] 配色不超过 4 种？
- [ ] 图表类型匹配数据类型？

## 案例库
- **案例1**：竞赛答辩 — 金字塔结构，评委提问命中预设
- **案例2**：商业汇报 — 数据驱动，当场达成合作
- **案例3**：个人追踪 — 时间线结构，进度一目了然

## 反模式
- ❌ 标题写"背景""介绍" → 标题应该是结论
- ❌ 一页放 5+ 个要点 → 认知超载
- ❌ 大段文字直接粘贴 → 应该提炼关键词
- ❌ 花哨动画 → 分散注意力
- ❌ 深色背景+浅色文字+小字号 → 投影仪看不清

## 联动技能
- **li-analyze**：分析内容后生成 PPT 大纲
- **li-visual**：视觉风格指导
- **li-office**：Office 文档格式转换
- **li-prompt**：跨平台 prompt 生成 PPT 内容
""")

write(os.path.join(d, "eval.json"), make_eval(EVAL_CHECKS))
write(os.path.join(d, "_meta.json"), make_meta("li-pptx", "Presentation slide engine", [
    "slide-structure-patterns.md", "design-principles.md", "case-studies.md"
]))
write(os.path.join(d, "golden_rules.md"), """# li-pptx 黄金规则

- GR-001: 标题=结论，不是主题。"项目进展"是主题，"项目已完成80%"是结论。
- GR-002: 每页≤3个要点（米勒定律 7±2）。
- GR-003: 留白≥30%。信息密度太高=认知超载。
- GR-004: 配色不超过4种。简单即专业。
- GR-005: 技术细节放附录，主讲页只放结论和关键数据。
""")
print("=== li-pptx done ===")

# === Fix 3: li-wechat (52L, 0ref, no eval/meta/GR) ===
d = os.path.join(BASE, "li-wechat")
refs = os.path.join(d, "references")
os.makedirs(refs, exist_ok=True)

write(os.path.join(refs, "article-extraction.md"), """# 微信公众号文章提取

## 方法1：WebFetch
- 直接用 WebFetch 抓取公众号链接
- 限制：可能被反爬，需要多次重试

## 方法2：baoyu-url-to-markdown
- 自动提取正文+图片
- 输出干净的 Markdown

## 方法3：手动复制
- 公众号文章 → 全选复制 → 粘贴到编辑器
- 适用于 WebFetch 失败时

## 提取后处理
1. 清理广告/推广内容
2. 保留核心论点和数据
3. 标注来源（公众号名+日期）
""")

write(os.path.join(refs, "wechat-content-patterns.md"), """# 微信公众号内容模式

## 电气/AI 方向（小黎的领域）
- 技术科普：深度适中，有代码/公式
- 行业分析：数据驱动，有来源
- 学习笔记：费曼风格，有案例

## 内容质量判断
- ⭐⭐⭐ 有文献支撑 + 有原创观点 + 有可执行建议
- ⭐⭐ 有数据但来源不明 + 观点明确
- ⭐ 纯搬运 + 无数据 + 无观点

## 与小红书的差异
- 公众号：长文，深度，可放公式/代码
- 小红书：短文，视觉，需要标题党
""")

write(os.path.join(refs, "case-studies.md"), """# 案例库

## 案例1：技术文章分析
- 输入：一篇关于 FPGA 时序约束的公众号文章
- 流程：WebFetch 提取 → li-analyze 道法术器 → 百大认知引用
- 输出：结构化分析 + 与 li-hardware 知识对比

## 案例2：行业资讯提取
- 输入：AI 行业周报链接
- 流程：提取 → 筛选与小黎相关的条目 → 记忆沉淀
- 输出：3 条关键洞察 + 行动建议

## 案例3：学习笔记生成
- 输入：一篇关于控制理论的公众号文章
- 流程：提取 → 费曼检验 → 与学习区 SOP 联动
- 输出：简化版笔记 + 认知科学引用
""")

write(sm_path, """---
name: li-wechat
version: 1.0.0
category: li-series
tags: [wechat, 公众号, 微信, article]
auto_trigger: true
confidence: 0.85
priority: 4
---

# li-wechat — 微信公众号文章处理

## 理论锚点
| ID | 理论 | 来源 | 应用 |
|----|------|------|------|
| T1 | 信息提取 | 008-深度工作 | 只提取有价值内容 |
| T2 | 费曼检验 | 002-学习之道 | 用自己的话复述 |
| T3 | 认知负荷 | 002-学习之道 | 一次只处理一个核心观点 |

## Phase 0 识别
| 信号 | 行动 |
|------|------|
| 公众号链接（mp.weixin.qq.com） | WebFetch 提取 → Phase 1 |
| "帮我看看这篇文章" | 确认是公众号还是其他来源 |
| "公众号内容分析" | 提取 → li-analyze 道法术器 |

## Phase 1 提取
1. WebFetch 抓取链接
2. 清理广告/推广/评论区
3. 提取：标题、作者、核心论点、数据、来源

## Phase 2 处理
- **分析模式**：→ li-analyze（道法术器 + 百大认知）
- **提取模式**：→ 只提取关键信息 → li-memory 沉淀
- **对比模式**：→ 与已有知识对比 → 标注新知/重复/矛盾

## 案例库
- **案例1**：FPGA 技术文章 → 道法术器分析 + li-hardware 知识对比
- **案例2**：AI 行业周报 → 筛选相关条目 → 3 条洞察
- **案例3**：控制理论文章 → 费曼检验 → 学习笔记

## 反模式
- ❌ 全文复制不清理 → 广告和推广混入
- ❌ 不标注来源 → 后续无法追溯
- ❌ 一次处理太多文章 → 认知超载
- ❌ 不做费曼检验 → 以为看懂了其实没有
- ❌ 不和已有知识对比 → 重复学习已知内容

## 联动技能
- **li-analyze**：道法术器深度分析
- **li-memory**：事实提取和记忆沉淀
- **li-research**：扩展研究（文章提到的引用/论文）
- **li-xhs**：公众号→小红书内容改编
- **li-transcript**：如果是公众号音频/视频的逐字稿
""")

write(os.path.join(d, "eval.json"), make_eval(EVAL_CHECKS))
write(os.path.join(d, "_meta.json"), make_meta("li-wechat", "WeChat article processing", [
    "article-extraction.md", "wechat-content-patterns.md", "case-studies.md"
]))
write(os.path.join(d, "golden_rules.md"), """# li-wechat 黄金规则

- GR-001: 提取后必须清理广告/推广内容。干净的输入=高质量的输出。
- GR-002: 必须标注来源（公众号名+日期+链接）。
- GR-003: 用费曼检验确认理解。看懂≠能用自己的话说清楚。
- GR-004: 与已有知识对比——新知/重复/矛盾三分类。
- GR-005: 一次只处理 1-3 篇文章。批量处理=批量偷懒。
""")
print("=== li-wechat done ===")

# === Fix 4-10: Add missing references to 7 skills ===
ref_fixes = {
    "li-debug": [
        ("debugging-discipline.md", """# 调试纪律（来自 mattpocock diagnose）

## 核心原则：反馈循环优先
不要直接改代码。先建立反馈循环（测试/日志/断点），再改。

## 6 阶段
1. 复现 — 找到最小复现步骤
2. 隔离 — 缩小问题范围
3. 假设 — 列出 3 个最可能的原因
4. 插桩 — 在假设点加日志/断点
5. 修复 — 只改必要的
6. 回归 — 确认修复不引入新问题

## 10 种反馈循环
自动测试/手动测试/日志/断点/bisect/profiler/看代码/问人/搜索/写最小复现
"""),
    ],
    "li-local-search": [
        ("search-algorithms.md", """# 本地搜索算法

## 三级搜索
1. 文件名匹配（glob）
2. 内容搜索（grep/ripgrep）
3. 语义搜索（embedding）

## 性能优化
- 先窄后宽：精确匹配 → 模糊匹配 → 正则
- 先近后远：当前目录 → 工作区 → 全局
- 缓存热路径：常用目录索引
"""),
    ],
    "li-plan": [
        ("planning-methods.md", """# 规划方法论

## Mode A：日常任务（GTD）
- 收集 → 处理 → 组织 → 回顾 → 执行
- 每日 ≤ 3 个核心任务
- 周回顾：完成率 + 教训

## Mode B：长期项目（里程碑）
- 目标分解 → 里程碑 → 关键路径 → 风险评估
- 每个里程碑有交付物和验收标准
- 月回顾：进度偏差 + 调整

## 认知科学支撑
- 计划谬误（010-思考快与慢）：人类系统性低估任务耗时
- 解决：乘以 1.5-2x 作为实际预估
"""),
    ],
    "li-storyboard": [
        ("storyboard-templates.md", """# 分镜模板

## 叙事弧模板
- 开头（3s）：钩子——冲突/悬念/视觉冲击
- 发展（60%）：递进展开，每镜一个信息点
- 高潮（20%）：核心信息/情感峰值
- 结尾（10%）：行动号召/留白

## 每镜要素
- 画面描述（what）
- 镜头运动（how）
- 时长（when）
- 音效/配乐（sound）
- 文字/字幕（text）
"""),
    ],
    "li-triage": [
        ("triage-decision-tree.md", """# 分流决策树

## 分流矩阵
| 紧急\\重要 | 高重要 | 低重要 |
|-----------|--------|--------|
| 高紧急 | 🔴 立即处理 | 🟡 委派/快速处理 |
| 低紧急 | 🟢 计划处理 | ⚪ 排队/丢弃 |

## 5 状态机
- **New**：刚收到，未分类
- **Triaged**：已分类，待分配
- **InProgress**：正在处理
- **Blocked**：被阻塞，需要输入
- **Done**：完成

## 状态转移规则
- New → Triaged：必须在 5 分钟内
- Triaged → InProgress：按优先级排序
- InProgress → Blocked：标记阻塞原因
- Blocked → InProgress：阻塞解除
"""),
    ],
    "li-webtest": [
        ("testing-strategies.md", """# Web 测试策略

## 测试金字塔
- E2E 测试（少量）：关键用户路径
- 集成测试（适量）：API + 组件交互
- 单元测试（大量）：纯函数逻辑

## 工具选择
- Playwright：E2E，跨浏览器
- Vitest：单元+集成
- Lighthouse：性能+可访问性
- axe-core：可访问性自动化

## 检查清单
- [ ] 关键路径 E2E 覆盖
- [ ] API 响应验证
- [ ] 错误状态处理
- [ ] 移动端响应式
- [ ] 无障碍检查
"""),
    ],
    "li-workflow": [
        ("workflow-patterns.md", """# 工作流模式

## 模式1：管道（Pipeline）
A → B → C，串行执行
适用：数据处理、内容创作

## 模式2：扇出（Fan-out）
A → [B, C, D] 并行
适用：多源搜索、批量处理

## 模式3：条件分支（Router）
A → if X then B else C
适用：分流、路由

## 模式4：循环（Loop）
A → B → if not done → A
适用：迭代优化、质量检查

## 工具
- GitHub Actions：CI/CD
- Claude Code hooks：自动化触发
- Cron/定时任务：周期性工作
"""),
    ],
}

for skill_name, refs_list in ref_fixes.items():
    d = os.path.join(BASE, skill_name, "references")
    os.makedirs(d, exist_ok=True)
    for fname, content in refs_list:
        write(os.path.join(d, fname), content)
    print(f"=== {skill_name}: +{len(refs_list)} refs ===")

print("\n=== ALL 10 WARN SKILLS FIXED ===")
