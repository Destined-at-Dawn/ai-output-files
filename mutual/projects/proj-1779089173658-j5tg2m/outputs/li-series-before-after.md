# li- 系列 Skill 生态：完整对照表

> 文档版本：v1.0 | 日期：2026-06-11
> 对比范围：2026-06-07（对话开始）→ 2026-06-11（当前）
> 数据来源：实际文件系统扫描 + memory/*.md + 对话历史

---

## 一、总体指标对照

| 指标 | 对话前（6/7） | 当前（6/11） | 变化 |
|------|--------------|-------------|------|
| **活跃 li- skill 数** | 9 | **41** | +32 |
| **已弃用 li- skill** | 0 | 5 | li-content/li-migrate/li-redesign/li-scaffold/li-workflow |
| **已删除（物理）** | 0 | 2 | li-evolve/li-skillcraft |
| **Tier 1 核心引擎** | 0（无分层） | 5 | li-research/li-hardware/li-analyze/li-improve/li-manage |
| **Tier 2 能力模块** | 9（平铺） | 36 | 详见下方完整清单 |
| **Tier 3 SOP 编排** | 0 | 4 个 SOP + li-intent | sop-content-analysis/sop-content-creation/sop-skill-lifecycle/sop-research |
| **SKILL.md** | 9/9 | 41/41 | 全部 ≤300 行 |
| **golden_rules.md** | 0/9 | 41/41 | 全部 ≥500B 真实内容 |
| **eval.json** | 0/9 | 41/41 | 全部有 12+ 项断言 |
| **_meta.json** | 0/9 | 41/41 | 全部有版本/依赖/触发词声明 |
| **references/ 非空** | ~3/9 | 41/41 | 全部有 ≥1 个参考文件 |
| **路由表总条目** | ~50（估） | 88 | 0 跨 skill 重复触发词 |
| **li- 路由条目** | 9 | 41 | 全部注册 |
| **li- 触发词总数** | ~180（估） | 1115 | 覆盖 80%+ 常见任务场景 |
| **工作区路由表同步** | 1（仅 mutual） | 69 | os.walk() 全递归扫描 |
| **Progressive Disclosure 架构** | 0/9 | 41/41 | 主文件 ≤300 行 + references/ 按需加载 |

---

## 二、每个 li- Skill 对照

### Tier 1：核心引擎（5 个）

| Skill | 对话前状态 | 当前状态 | 核心变化 |
|-------|----------|---------|---------|
| **li-research** | ✅ 存在（标杆质量） | v10+, 277 行, 7 refs | 从 731 行瘦身到 277 行（Progressive Disclosure），新增搜索饱和检测、迭代协议、外部研究库 |
| **li-hardware** | ❌ 不存在 | v3.1, 298 行, 25 refs | 从零创建。吸收 D:\AMD 实战（FPGA 三层架构/Vivado TCL 陷阱/I2C 带宽计算）+ 竞赛区 1844 文件（17 Bug 审计/CRC 调试/嵌入式模式）+ hardware-design（Verilog 规范/FSM/CDC/Yosys/FPGABuilder） |
| **li-analyze** | ❌ 不存在 | v1.1, 164 行, 4 refs | 新建。融合道法术器框架 + ai-reading-deep（62 本认知书籍）+ case-study-extractor + content-analysis。自进化引擎（用户评分→模式采集→规则更新） |
| **li-improve** | self-improving v3.5（286 行） | v4.1, 271 行, 16 refs | 从 self-improving → li-evolve（668行臃肿）→ li-improve（Progressive Disclosure）。吸收 peterskoett（Hook 驱动/递归度追踪/自动 Skill 提取）+ HyperAgents（元认知自修改） |
| **li-manage** | ✅ 存在（675 行超标） | v4.0, 209 行, 12 refs | 瘦身 675→209 行。新增 Flow K（文档洁癖）+ Flow L（知识结构化，吸收 dbs-structured-knowledge）+ neat-freak 功能吸收 |

### Tier 2：能力模块（36 个）

#### 从零创建的新 Skill（17 个）

| Skill | 来源 | 行数 | 核心功能 |
|-------|------|------|---------|
| **li-sync** | cross-workspace-sync 融合 | 262 | 跨工作区规则同步 + telos 映射 + 一致性检查 |
| **li-devil** | devils-advocate 融合 | 275 | 泼冷水协议 + 预验尸 + 反讨好 + 信号追踪 |
| **li-mindcoach** | 心力跃迁教练升级 | 227 | 四阶段心力教练 + 62 本书引用 + 杠铃式收尾 |
| **li-memory** | three-tier-memory + Supermemory | 142 | 事实提取 + 矛盾检测 + 自动遗忘 + 混合检索 |
| **li-plan** | jc-plan + long-term-plan 合并 | 134 | Mode A 日常任务 + Mode B 长期规划 |
| **li-industry** | 行业研究重命名 | 194 | 行业研究框架 |
| **li-webtest** | webapp-testing 重命名 | 298 | Web 应用测试自动化 |
| **li-storyboard** | seedance-storyboard 重命名 | 227 | 分镜脚本生成 |
| **li-visual** | 视觉风格提示词重命名 | 299 | 视觉风格提取与应用 |
| **li-hardware** | 从零创建 | 298 | 嵌入式/Arduino/FPGA 全栈 |
| **li-diagnose** | system-diagnosis 升级 | 170 | 系统熵增诊断（五层消解） |
| **li-debug** | mattpocock/skills diagnose | 182 | 纪律化调试循环 |
| **li-triage** | mattpocock/skills triage | 171 | 5 状态 issue 分流 |
| **li-prompt** | hue 融合 | 230 | 六维跨 AI 平台 prompt 构建 |
| **li-competition** | competition-workflow 吸收 | 299 | 竞赛项目管理（FPGA/RoboMaster） |
| **li-study** | interactive-learning 吸收 | 243 | 费曼检验 + 复盘分析 + 考前复习 |
| **li-intent** | SOP 驱动意图引擎 | 171 | SOP 读取 → 意图匹配 → skill 链编排 |

#### 从非 li- skill 融合创建（12 个）

| Skill | 融合的旧 Skill | 行数 |
|-------|---------------|------|
| **li-dbs** | dbs-agent-migration + dbs-content + dbs-structured-knowledge | 264 |
| **li-wechat** | wechat-article-collector + 4 个微信分析工具 | 196 |
| **li-design** | design-extract + visual-design-prompt | 290 |
| **li-image** | baoyu-image-gen + image-editing | 273 |
| **li-video** | seedance-storyboard + video-creator | 292 |
| **li-office** | xlsx + docx + csv 吸收 | 299 |
| **li-web** | web-access + step-search + web-artifacts-builder | 212 |
| **li-xhs** | 投流帖改写 + 小红书留学求职ip号帖子改编 | 243 |
| **li-data** | data-analysis + 12 种数据可视化 | 116 |
| **li-skills-mgmt** | 技能管理（li-manage 的技能管理子集） | 56 |
| **li-infra** | CLAUDE.md/memory/SOP 基础设施管理 | 304 |
| **li-workspace** | li-migrate + li-redesign + li-scaffold 合并 | 287 |

#### 原有保留（7 个）

| Skill | 对话前 | 当前 | 变化 |
|-------|--------|------|------|
| **li** | 路由器（7 子 skill） | 路由器（41 子 skill） | 入口扩充 |
| **li-transcript** | 2039 行超标 | 132 行 + 6 refs | 瘦身 93%，Progressive Disclosure |
| **li-local-search** | 499 行 | 93 行 + 2 refs | 瘦身 81% |
| **li-bestskill** | 358 行 | 182 行 + 4 refs | +四阶段全平台搜索策略（修复"只搜 GitHub"问题） |
| **li-skillcreate** | 554 行 | 300 行 + 10 refs | 10 轮迭代到 v10.0 + Phase 3.5 质量门禁 |
| **li-skillfusion** | 381 行 | 217 行 + 6 refs | +依赖分析 + 工作区定制 |
| **li-workflow** | 110 行 | 110 行（独立保留） | 恢复为独立 skill（"行数少不是弃用理由"） |

### 弃用/删除（7 个）

| Skill | 操作 | 去向 |
|-------|------|------|
| li-evolve | 物理删除（已归档） | → li-improve（Progressive Disclosure 版） |
| li-skillcraft | 物理删除（已归档） | → li-skillfusion（完全吸收） |
| li-content | 弃用 | → li-analyze（Mode A/B 双模式） |
| li-migrate | 弃用 | → li-workspace（Setup/Migration/Refactoring） |
| li-redesign | 弃用 | → li-workspace |
| li-scaffold | 弃用 | → li-workspace |
| li-workflow | 弃用后恢复 | 独立保留（用户纠正"行数少不是弃用理由"） |

### 弃用（6/11 第二轮，8 个）

| Skill | 操作 | 去向 | 原因 |
|-------|------|------|------|
| li-writing | 标记 DEPRECATED | → li-manage | Trigs=0，从未触发 |
| li-session | 标记 DEPRECATED | → li-manage | Trigs=0，从未触发 |
| li-voice | 标记 DEPRECATED | → li-transcript | Trigs=0，从未触发 |
| li-search | 标记 DEPRECATED | → li-research | Trigs=0，从未触发 |
| li-personal | 标记 DEPRECATED | → li-manage | Trigs=0，从未触发 |
| li-docs | 标记 DEPRECATED | → li-infra | Trigs=0，从未触发 |
| li-frontend | 标记 DEPRECATED | → li-web | Trigs=0，从未触发 |
| li-platform | 标记 DEPRECATED | → li-manage | Trigs=0，从未触发 |

**合计**：活跃 48 → 40（-8），弃用 0 → 8

---

## 三、路由系统对照

| 指标 | 对话前 | 当前 |
|------|--------|------|
| 路由表总条目 | ~50 | 88 |
| li- 路由 | 9 | 41 |
| 非 li- 路由 | ~41 | 47 |
| **跨 skill 重复触发词** | **35** | **0** |
| 触发词总数 | ~809 | 1115 |
| 工作区同步 | 1（仅 mutual） | 69（os.walk() 全递归） |
| 第三方仓库保护 | 未区分 | 明确标记只读 |
| 幽灵路由（指向不存在目录） | 未检查 | 0（全部清除） |

---

## 四、架构模式对照

| 维度 | 对话前 | 当前 |
|------|--------|------|
| **文件结构** | 不统一（有的有 golden_rules，有的没有） | 41/41 统一：SKILL.md + _meta.json + eval.json + golden_rules.md + references/ |
| **行数控制** | 无限制（li-transcript 2039 行） | **41/41 ≤300 行**（Progressive Disclosure：主文件精简，详细在 references/） |
| **质量门禁** | 无 | eval.json（12+ 项断言）+ golden_rules.md（5-10 条领域特化规则） |
| **理论基础** | 无 | 12 项认知科学锚点（T1-T12，每个 skill 标注来源书籍编号） |
| **案例库** | 无 | 35/41 有 ≥3 个真实案例（6 个待验证的新建 skill） |
| **反模式** | 无 | 35/41 有 5-10 条反模式（每条带理论来源） |
| **联动技能** | 无 | 35/41 有 4-6 个实质联动（触发条件+联动方式） |
| **外部研究** | 无 | 关键 skill 有外部对标（最高 23.2K★） |
| **搜索策略** | 只搜 skills.sh/GitHub | 四阶段全平台覆盖（GitHub/skills.sh/Agent Skills Hub/MCP Registry/中文生态/社区论坛） |
| **路由注册** | 无强制 | `.claude/rules/skill-route-enforcement.md`（5 条铁律：创建后必须注册/弃用后必须清除/全量验证） |
| **执行纪律** | 无 | `.claude/rules/skill-execution-discipline.md`（调用时必须先读 references/ 必读文件） |
| **Tier 分层** | 无（9 个平铺） | 三层：Tier 1 核心引擎（5）/ Tier 2 能力模块（36）/ Tier 3 SOP 编排（li-intent + 4 SOP） |

---

## 五、SOP 编排层对照

| 维度 | 对话前 | 当前 |
|------|--------|------|
| **意图理解** | 纯关键词匹配 | li-intent（SOP 驱动意图引擎，读取 5 工作区 SOP 总索引） |
| **SOP 编排** | 无 | 4 个全局 SOP（content-analysis/content-creation/skill-lifecycle/research） |
| **链式调用** | 无 | SOP 定义 skill 调用链（如：li-research → li-devil → li-memory） |
| **自学习闭环** | 无 | 各工作区 SOP 总索引内置（1 次→记录, 2 次→升级, 3 次→铁律） |
| **对话日志** | conversation-journal/ 有 2 个文件 | 同前（5/26 断了，待恢复） |

---

## 六、非 li- Skill 处理对照

| 类别 | 对话前数量 | 当前状态 |
|------|----------|---------|
| **已融入 li- 系列** | 0 | **~35 个**（被吸收进对应 li- skill） |
| **已弃用** | 0 | **~46 个**（有 DEPRECATED.md） |
| **保留为独立工具** | 0 | **~51 个**（第三方平台工具：baoyu-*/pdf/xlsx/step-search 等） |
| **路由覆盖** | 158/199 零路由（79%） | **所有活跃 skill 均有路由** |

---

## 七、工程法则和硬规则对照

| 规则 | 对话前 | 当前 |
|------|--------|------|
| skill-route-enforcement.md | 不存在 | 5 条铁律（创建/修改/弃用/合并后必须注册路由） |
| skill-execution-discipline.md | 不存在 | 4 条铁律（调用 skill 时必须先读执行协议） |
| skill-logging-enforcement.md | 存在但无协议执行检查 | 新增铁律 6（日志增加「协议执行」列） |
| R19 Agent 并发降级协议 | 不存在 | 3 步降级（识别→零等待切换→记录） |

---

## 八、关键教训（从对话中提炼）

| # | 教训 | 发生次数 | 当前状态 |
|---|------|---------|---------|
| 1 | **"行数少"不是弃用理由**（7 行 zoom-out 有独立价值，110 行 li-workflow 也有） | 1 | li-workflow 已恢复 |
| 2 | **创建 skill 后必须注册路由**（文件存在但路由缺失 = 不存在） | ≥6 | skill-route-enforcement.md 已创建 |
| 3 | **第三方仓库 = 只读**（误改 4 个 GitHub 仓库 CLAUDE.md） | 1 | 已回滚 + 标记只读 |
| 4 | **不能编造案例**（9 个空壳 skill 案例全编的 → 诚实删除） | ≥2 | 9 个已删 + 归档 |
| 5 | **批量创建 = 低质量**（11 个 skill 质量远差于 li-research） | ≥2 | 已建质量门禁 |
| 6 | **搜索不能只搜一个平台**（只搜 GitHub 漏掉 23.2K★ 项目） | 1 | li-bestskill v1.2 四阶段全平台 |
| 7 | **深度扫描不是表面扫**（竞赛区 468 目录只扫了顶层） | ≥3 | os.walk() 全递归 |
| 8 | **裁判员和运动员不能是同一个人**（自定义标准自验收 = 自嗨） | 1 | li-devil 泼冷水协议 |
| 9 | **已有 SOP 是现成的意图模式库**（188 个 SOP 不读，凭空设计 intent-patterns.json） | 1 | li-intent 读取 SOP 总索引 |
| 10 | **Progressive Disclosure 是唯一正确架构**（668 行 li-evolve 塞所有 → 失败） | 1 | 41/41 全部 ≤300 行 + references/ |

---

## 九、文件系统变化

| 目录 | 对话前 | 当前 |
|------|--------|------|
| `~/.newmax/skills/li-*/` | 9 个目录 | **41 个目录** |
| `mutual/skills/` | 0 个 skill | 0 个 skill（skill 在 `~/.newmax/skills/`，不在 mutual） |
| `mutual/SOPs/` | 4 个 SOP | **8 个 SOP** |
| `mutual/skill-routing-table.json` | ~50 条路由 | **88 条路由** |
| `mutual/.claude/rules/` | 12 个规则 | **17 个规则**（+5） |
| `outputs/li-series-ecosystem-handoff.md` | 不存在 | 411 行，14KB（AI 继承交接文档） |
| `归档/li-*` | 无 | 多个备份目录（每个重大变更前归档） |

---

## 十、当前未完成项（按优先级）

| 优先级 | 任务 | 详情 |
|--------|------|------|
| **P0** | conversation-journal 恢复 | 5/26 断了，35 天没更新。自进化闭环缺对话日志 |
| **P0** | SOP 编排层完善 | li-intent 只读取 SOP 总索引，不读具体 SOP 文件内容 |
| **P1** | 6 个新 skill 案例验证 | li-competition/li-study/li-dbs/li-wechat/li-design/li-image 案例待实际使用后补充 |
| **P1** | 非 li- skill 路由质量 | 47 条非 li- 路由的触发词质量参差不齐 |
| **P2** | SOP→Skill 映射自动化 | 从 SOP 总索引的 IF/ELSE 路由规则自动更新 skill-routing-table.json |
| **P2** | 百大认知引用均衡 | 每个 skill 至少引用 3 本不同书籍，避免锚定在 2-3 本 |
