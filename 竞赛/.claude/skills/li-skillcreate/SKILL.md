---
name: li-skillcreate
description: >
  小黎的技能锻造器——从真实需求到生态感知的完整 skill 创建/迭代系统。
  不是通用 skill 模板生成器，而是从 187+ 个已有 skill 中学习模式、从对话教训中提炼规则、
  创建后自动注册到路由表+画像+记忆系统的「一鱼多吃」技能工厂。

  触发词：创建技能/造技能/新技能/skill创建/建skill/写技能/做一个技能/锻造技能/
  技能迭代/优化技能/改进技能/升级技能/skill迭代/改skill

  核心理念：技能不是孤岛——创建时参考已有优秀技能、产出后喂回生态系统、
  迭代时从真实使用数据中学习。造一个技能 = 至少读 5 个已有技能 + 更新 5 个生态文件。
---

> **必读（执行前必须 Read）**：`references/skill-linkage.md` — li- 系列联动规则。不读 = 跳过联动 = 产出不完整。500 万 token 上下文中本文件可能被压缩，但 references/ 不会被压缩。


## [LIGHTNING] 执行协议（强制 - 禁止跳过）

> **本段是执行约束，不是参考建议。违反 = 产出质量不可信。**

### [RED] 必读（执行前必须读取，不可跳过）

- 执行前**必须** `Read references/skill-structure.md` - 不读 = 不了解核心方法论 = 产出不合格

### [YELLOW] 按需（匹配场景时必须读取）

- 场景[防失败模式] -> **必须** `Read references/anti-failure-patterns.md`
- 场景[自动进化] -> **必须** `Read references/auto-evolution.md`
- 场景[认知框架] -> **必须** `Read references/cognitive-frameworks.md`
- 场景[生态集成] -> **必须** `Read references/ecosystem-integration.md`
- 场景[生态更新] -> **必须** `Read references/ecosystem-update.md`
- 场景[外部研究] -> **必须** `Read references/external-research.md`
- 场景[迭代协议] -> **必须** `Read references/iteration-protocol.md`
- 场景[参考技能] -> **必须** `Read references/reference-skills.md`
- 场景[搜索方法论] -> **必须** `Read references/search-methodology.md`
- 场景[补充] -> **必须** `Read references/supplementary.md`

### [STOP] 门禁

- Phase 执行前：确认已读取 references/skill-structure.md。未读 -> **禁止继续**
- 输出结论前：确认有 evidence path (Source: path#line)。无证据 -> **禁止声称**
- 跳过本协议 = 违反工程法则 8（门禁不可跳过）

# li-skillcreate：小黎的技能锻造器

> 造一个好技能的最快路径：先学别人的，再结合你的生态，最后让技能自己进化。
> 一个技能 = 它的 SKILL.md + 它读过的参考技能 + 它在生态中的连接 + 它从使用中学到的教训。

---
## References 地图

本文件是骨架。详细内容在 `references/` 目录：

| 文件 | 内容 | 何时读取 |
|------|------|---------|
| `references/search-methodology.md` | 联网搜索平台矩阵、关键词生成、结果评估、汇报格式 | Phase 1 联网搜索时 |
| `references/skill-structure.md` | SKILL.md 六层结构详述、references/ 规范、_meta.json 格式 | Phase 3 构建时 |
| `references/ecosystem-update.md` | 一鱼多吃完整流程（6 个生态副作用） | Phase 5 生态更新时 |
| `references/iteration-protocol.md` | 1.25 倍递增规则、迭代类型、黄金法则、汇报模板 | Phase 6 迭代时 |
| `references/auto-evolution.md` | 触发词进化、画像更新、教训固化、质量评分 | Phase 7 自动沉淀时 |
| `references/cognitive-frameworks.md` | 百大认知书籍在技能创建中的应用 | 设计决策时 |
| `references/reference-skills.md` | 16 个融合参考 skill 的完整清单和提取机制 | 了解来源时 |
| `references/anti-failure-patterns.md` | 12 个真实失败模式 + 自检清单 | 全程自检时 |
| `references/ecosystem-integration.md` | 生态集成完整流程（6 个副作用联动） | Phase 5 校验时 |
| `references/external-research.md` | 外部研究平台矩阵、关键词策略 | Phase 1 外部研究时 |
| `references/quality-gate.md` | 15 项强制质量门禁完整清单 | Phase 3.5 质量检查时 |
| `references/skill-linkage.md` | li- 系列联动规则（必读，最高优先级） | 每次执行前 |
| `references/supplementary.md` | 补充材料和扩展参考 | 按需 |

---
## 设计哲学（7 条）

1. **先搜后学后造**（deep-research v4）：网上搜+本地读5+已有技能 2. **行动锁**（jc-clarifier）：不澄清不创建 3. **一鱼多吃**：创建=至少更新5个生态文件 4. **落盘验证**（6次事故）：Write后必须Read 5. **版本化迭代**（28轮事故）：迭代≠改版本号 6. **触发词从数据中长出来**（li-devil）：不猜 7. **生态感知**：技能读画像，画像记录技能

---
## 理论锚点（12 项）

| 编号 | 理论 | 来源 | 在技能创建中的应用 |
|------|------|------|-------------------|
| T1 | 认知负荷理论 | 007 | 主文件≤300行防过载，detail按需加载 |
| T2 | 生成效应 | 034 | 用户参与创建的skill记忆更深，Phase 0强制问答 |
| T3 | 专家幻觉 | 043 | "我需要Xskill"可能是假需求，Phase 0消解90% |
| T4 | 具身认知 | 003 | skill执行=身体化体验，Phase 4实际任务验证 |
| T5 | 间隔重复 | 002 | golden_rules迭代=间隔强化，防回归 |
| T6 | 元认知监控 | 023 | eval.json=外部化元认知，自检不依赖记忆 |
| T7 | 心智模型 | 026 | SKILL.md=AI的心智模型，必须自含完整 |
| T8 | 锚定效应 | 010 | 搜索结果按stars排序防首因偏见 |
| T9 | 过度自信 | 010 | Phase 3.5质量门禁=对抗"我觉得够好了" |
| T10 | 技能习得 | 001 | 从模仿到创新：先读5+已有skill再动手 |
| T11 | 模块化 | 005 | Progressive Disclosure=信息系统的模块化设计 |
| T12 | 反脆弱 | 046 | 教训沉淀=从失败中获益，golden_rules越踩越强 |

---
## Phase 0：需求消解（dbs-diagnosis）

> 90% 的"我要造个技能"是假需求。先消解，再动手。

### Step 0.1：问题消解

收到"创建技能"请求后，三连检测：

1. **语言陷阱**：用户说的"技能"具体指什么？skill？MCP tool？脚本？SOP？
2. **假设错误**：用户假设"需要新技能"→ 也许已有技能能解决？调路由表就行？
3. **发动机空转**（dbs-goal）：用户描述的需求中哪些是装饰词？去掉后句子还成立吗？

**评分量化**：0-4 分→追问禁止搜索；5-7 分→先给低置信建议；8-10 分→进入 Phase 1

**消解结果**：成立+需要新技能→Phase 1；已有技能能解决→推荐+更新路由；不成立→消解

> 消解案例（5 个真实场景）→ `references/anti-failure-patterns.md` § 消解案例

### Step 0.2：安全审查（skill-vetter）

如果用户要安装/引用外部技能作为参考：
- 来源可信？无恶意代码？权限范围合理？无 obfuscated code？
- 风险等级：🟢 低 → 基本审查 | 🟡 中 → 完整代码审查 | 🔴 高 → 需用户确认

---
## Phase 1：调研已有技能（至少读 5 个）

> 来源：deep-research "先学后造" + 读了 60+ 个 skill 的经验

### Step 1.1a：扫描本地生态

```powershell
ls ${NEWMAX_HOME}/skills/ | Select-Object Name
ls C:/Users/13975/.codex/skills/ | Select-Object Name
ls "E:\ai产出文件\牛马\mutual\mutual\skills\" | Select-Object Name
```

### Step 1.1b：四阶段全平台搜索（铁律 — 必须执行，不可跳过）

**搜索策略铁律**：宽泛优先 → 不限定平台 → 按 Stars 排序 → 结果不够好就换更宽泛的词重搜

| 阶段 | 平台 | 搜索方式 | 目标 |
|------|------|---------|------|
| **1. 技能库搜索** | skills.sh（61K+）/ Agent Skills Hub / ToolSDK（4547+ MCP） | WebFetch 搜索 | 找现成可用的 |
| **2. GitHub 全局** | GitHub（按 Stars 降序，**不限定** claude/skill 关键词） | `keyword` + `&s=stars&o=desc` | 找高星参考项目 |
| **3. 中文生态** | AIHot / 腾讯 SkillHub / 阶跃星辰 / 微信公众号 | WebFetch 搜索 | 找中文社区方案 |
| **4. 社区论坛** | Reddit / Hacker News / 知乎 / GitHub Discussions | WebFetch 搜索 | 找实战经验和踩坑 |

**搜索质量自检**：结果最高 <100★→关键词太窄换词重搜；只搜一个平台→违规；没点开网页→违规

**反模式**：`claude-code self-improving skill`（太窄，13★）→ ✅ `self-improving agent`（宽泛，23.2K★）

> 详细搜索矩阵 → `references/search-methodology.md` + `references/external-research.md`

### Step 1.2：分类并深入读取

综合本地 + 联网结果，深入读取至少 5 个最相关的 SKILL.md/README（本地 + 网上各至少 2 个）。

### Step 1.3：提取设计模式

从每个参考 skill 中提取 1-3 个核心设计决策（模板见 `references/search-methodology.md`）。

**铁律：不读 5 个以上已有技能就动手 = 违规。**

---
## Phase 2：澄清需求（行动锁）

> 来源：jc-clarifier 澄清漏斗 + 行动锁

### Step 2.1：镜像复述

输出：技能名 / 核心问题 / 与已有技能区别 / 参考的设计模式。用户确认后才进 Phase 3。

> 镜像复述模板 → `references/skill-structure.md`

### Step 2.2：行动锁解除

用户确认后才进入 Phase 3。用户说"直接造"→ 提醒一次风险，第二次直接执行。

---
## Phase 3：构建技能（六层结构）

> 来源：skill-creator 的 Progressive Disclosure + output-skill 的完整输出

目录结构：SKILL.md（≤300行）+ _meta.json + eval.json + golden_rules.md + references/ + scripts/。**禁止**：README.md / CHANGELOG.md

六层结构：YAML frontmatter（必须）→ 设计哲学（推荐）→ Phase 工作流（核心）→ 认知框架（按需）→ 参考清单 → 说话风格（必须）

> 详细规范 → `references/skill-structure.md`
## Phase 3.5: Quality Gate
Must pass 15 checks before submission. See `references/quality-gate.md` for full checklist.
Key: routing registered, trigger words ≥15, eval.json assertions pass, no phantom references.
## Phase 4：落盘验证（Write → Read → 断言）

> 来源：6 次"声称完成但未落盘"事故 — 最高优先级门禁

### 铁律

**Write 后必须 Read，Read 返回成功才能说"已创建"。**

### 验证流程

Write → ls 目录结构 → Read 内容 → 检查大小（SKILL.md >2KB，总 >5KB）→ 全过才能说"已创建"

> 12 个事故模式 → `references/anti-failure-patterns.md`

---
## Phase 5：一鱼多吃（生态副作用写入）

> 来源：deep-research v4 的 7 个生态副作用

**必须**执行至少 5 个生态更新：① 路由表（≥15 触发词 + 全工作区同步，见 `.claude/rules/skill-route-enforcement.md`） ② 今日记忆 ③ skill-catalog ④ artifact-registry ⑤ 调研画像 ⑥ 记忆候选

> 详细流程 → `references/ecosystem-update.md` + `references/ecosystem-integration.md`

---
## Phase 6：迭代模式（1.25 倍递增 + 黄金法则）

> 来源：deep-research Phase 6 + auto-evolution

### 触发

用户说"迭代/优化/改进/升级 + 技能名"时进入。

### 四条铁律

1. 每次迭代必须比上一轮多修改 25% 的文件/内容
2. 每轮迭代必须提炼至少 1 条黄金法则
3. 迭代不是改版本号——必须有实质性内容差异
4. 迭代后必须落盘验证（Phase 4）

| 轮次 | 最少修改量 | 黄金法则 |
|------|-----------|---------|
| 第 1 轮 | 20 处 | ≥1 条 |
| 第 2 轮 | 25 处 | ≥1 条 |
| 第 N 轮 | ceil(prev × 1.25) | ≥1 条 |

### 终止条件

1. 用户说"停"/"够了"/"就这样"
2. 连续 3 轮搜索饱和（无新参考技能可学习）
3. 技能已满足所有 Phase 0 确认的需求
4. 质量评分 ≥ 25/30（优秀）
5. 时间上限 3 小时（同一技能）

### 迭代类型

A 功能迭代（加新能力）/ B 质量迭代（改已有）/ C 生态迭代（修连接）/ D 重构迭代（改结构）

**黄金法则标准**：可执行 + 有来源 + 有反模式 + 跨技能通用

> 详细流程、汇报模板 → `references/iteration-protocol.md`

---
## Phase 7：使用习惯沉淀（自动进化）

> 来源：li-devil 自我进化模块 + conversation-to-knowledge + peterskoett(641★) + HyperAgents(2.6K★)

### 六条沉淀规则

| 规则 | 触发条件 | 动作 |
|------|---------|------|
| 触发词进化 | 用户手动指定技能名 / 连续 3 次跳过 / 连续 5 次成功 | 更新路由 / 降 confidence / 升 confidence |
| 使用画像更新 | 每次创建/迭代后 | 更新 research-profile.md |
| 教训固化 | 踩坑 ≥2 次 | 升级为规则；≥3 次升级为独立 Skill |
| 质量评分 | 每次创建/迭代后 | 6 维度评分，总分 < 20/30 → 继续迭代 |
| Recurrence-Count | 同教训跨 ≥2 任务出现 ≥3 次 | 自动晋升为 golden_rules.md 永久规则 |
| Meta-AutoEvolve | 每月 1 次 | 审查"进化流程本身"是否有效（Phase 通过率/Hook 有效性/引用均衡） |

> Recurrence-Count + Meta-AutoEvolve 详细机制 → `references/auto-evolution.md`

---
## 案例库
**案例 1：li-hardware v1→v3（最成功案例）**
- 背景：用户需要 Arduino 舵机控制 skill
- 流程：Phase 1 搜 GitHub（Jeffallan 459★ + ezrover 7★）→ 读 D:\AMD 3 个 FPGA 项目 → 读竞赛区 1844 个文件 → Phase 3 构建（25 个 references）→ Phase 5 注册路由（132 触发词）→ 迭代 v2→v3 吸收 hardware-design 1096 行精华
- 结果：241 行主文件 + 25 个 reference 文件，覆盖 Arduino/ESP32/FPGA/Vivado/I2C/SPI 全栈
- 关键决策：先搜后学后造（Step 1.1b 搜 3 个平台）+ 从用户真实项目提取知识（不是编造）

**案例 2：v1→v10 自我迭代** — 10 轮迭代（补 golden_rules → 扩 references → 理论锚点 → 搜索策略 → 质量门禁 15 项 → 外部研究 → 联动）。结果：质量门禁 0→15 项。教训：Phase 3.5 质量门禁 = 核心。

**案例 3：9 个空壳反面案例** — 批量创建 9 个 skill，案例全是编造 → li-devil 审计后删除。教训：没有真实使用记录 = 编造。
## 反模式（5 条）
| # | 反模式 | 后果 | 来源 |
|---|--------|------|------|
| 1 | 跳过 Phase 0 直接造 | 造了不该造的 + 重复造轮子 | dbs-diagnosis + li-bestskill |
| 2 | 创建后不注册路由 | skill 永远不触发 | skill-route-enforcement |
| 3 | 案例靠编造 | li-devil 审计暴露，9 个空壳被删 | 2026-06-11 事故 |
| 4 | 批量创建不逐个验证 | 质量参差不齐 | 11 个 skill 事故 |
| 5 | references/ 放占位符 | 主文件膨胀但实质空洞 | Progressive Disclosure 违反 |
## 联动技能（6 个）
| Skill | 触发条件 | 联动方式 |
|-------|---------|---------|
| li-bestskill | Phase 1 外部搜索 | 跨平台发现 |
| li-skillfusion | 合并/拆分决策 | 依赖分析 |
| li-manage | 全生命周期 | 管理 + 退化检测 |
| li-devil | 泼冷水审查 | 预验尸 |
| li-research | 先调研再创建 | 多源搜索 |
| li-sync | 路由变更 | 全工作区同步 |
