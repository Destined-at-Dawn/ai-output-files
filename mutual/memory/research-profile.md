# 调研画像（Research Profile）

> 基于 2026-05-25 ~ 2026-05-31 的实际调研记录自动提炼。AI 读取后可直接了解调研偏好，不需要每次重新问。
> 创建日期：2026-05-31
> 数据来源：memory/ 长期+每日记忆 + outputs/ 历次调研报告 + 路由表使用记录

## 基本偏好

- **默认深度**：深度（用户要求"3 小时 100 次迭代"，说明偏好深度穿透而非快速概览）
- **首选平台**：GitHub > X/Twitter > Reddit > YouTube > 知乎 > ArXiv
  - 历次调研均覆盖 GitHub + X + Reddit + YouTube 四平台
  - 学术平台按需（涉及技术方案时才搜）
- **迭代习惯**：通常需要多轮迭代（工作流优化用了 70+ 轮），偏好先广后深
- **信息密度**：高密度、结论先行、列表优于表格
- **最看重**：可执行建议 > 数据 > 案例 > 分析

## 关注领域

- **技术方向**：FPGA、具身智能、AI Agent、Claude Code 生态、上下文压缩、自动化工作流
- **商业方向**：小红书变现、公众号运营、知识付费
- **学术方向**：考研（上交/东南电气）、电气工程、集成电路
- **产品方向**：AI 读论文工具（最近核心需求）

## 历次调研索引

| 日期 | 主题 | 模式 | 轮次 | 平台 | 报告路径 |
|------|------|------|------|------|---------|
| 2026-05-27 | 上下文压缩自动化 | 调研 | 28 轮 | GitHub/YouTube/X/Reddit | outputs/context-compression-research-2026-05-27.md |
| 2026-05-28 | 工作流优化深度研究 | 调研 | 70+ 轮 | GitHub/YouTube/X/Reddit | outputs/workflow-optimization-research-2026-05-28.md |
| 2026-05-28 | comemo 仓库安全审计 | 调研 | 1 轮 | GitHub | outputs/security-audit-comemo-2026-05-28.md |
| 2026-05-30 | AI 学习工具深度调研 | 调研 | 多轮 | Web | outputs/AI学习工具深度调研-*-2026-05-30.md |
| 2026-05-30 | 诊断报告-规则膨胀 | 调研 | 2 版 | 本地文件 | outputs/诊断报告-规则膨胀与注意力竞争危机-2026-05-30.md |
| 2026-05-31 | AI读论文工具深度调研 | 调研 v1 | 8次搜索+4网页 | GitHub/X/Reddit/YouTube/产品/学术/中文 | outputs/AI读论文工具深度调研报告-2026-05-31.md |

## 调研习惯观察

- **多平台并行**：用户偏好同时搜 4+ 个平台，不喜欢单平台深度
- **重视落地**：调研完了必须产出改进方案或直接实施，不要停在"信息收集"阶段
- **迭代驱动**：用户说"迭代"时，期望的是实质性深化，不是格式调整
- **报告要落盘**：调研结果必须保存为 .md 文件，口头汇报不算完成
- **重视来源**：每个数字/结论必须标注来源 URL
- **关注竞品痛点**：特别关注"现有工具满足不了需求"的分析

## 痛点和禁忌

- **最讨厌**：
  - 声称"够了"但没产出文件（第八条事故教训）
  - 只堆搜索结果不做分析（"所以呢？"缺失）
  - 格式调整冒充迭代（"复制粘贴 270 个模板"教训）
- **禁止**：
  - 搜索摘要不点开网页（必须 WebFetch 至少 5 个）
  - 不问要不要迭代就结束
  - 调研和迭代路由混在一起
- **特别在意**：
  - 数据必须标来源和口径
  - 需求区分刚需 vs 伪需求（ROI 思维）
  - 道法术器穿透分析（不停在表面信息）

## 已下载的参考 skill 清单（v3 更新：8 个已融合）

| skill | 位置 | 核心价值 | 融入 deep-research v3 |
|-------|------|---------|----------------------|
| jc-clarifier | .shared | 行动锁 + 镜像复述 | ✅ Phase 1 行动锁 |
| skill-creator | .shared/profess | SKILL.md 结构 + Progressive Disclosure | ✅ 文件结构规范 |
| write-a-skill | .shared/profess | description 写法 + 自由度匹配 | ✅ 描述规范 |
| deep-review | .shared/profess | 长时间跨度分析 + Roadmap | ✅ 分析维度 |
| li-workflow | .shared/profess | 自动化编排 + CI/CD | ✅ 工作流思维 |
| handoff | .shared/profess | 对话交接文档 | ✅ 调研→迭代上下文传递 |
| diagnose | .shared/profess | 分阶段诊断 + 反馈环 | ✅ 搜索饱和检测 |
| chinese-natural-voice-revision | .shared | 中文文风修订 | ✅ 报告中文质量 |
| dbs-diagnosis | 创作区 github/dbskill | Phase 0 模式选择 |
| auto-evolution | mutual skills | eval.json + 递增迭代 |
| chinese-natural-voice-revision | .shared | 中文文风修订 |

---

## 使用习惯 → Skill 行为映射

> 以下是从 7 天使用记录中提炼的"用户期望 AI 怎么做"。
> 每条映射 = 用户的一个痛点/习惯 → skill 应该怎么做。

| # | 用户习惯/痛点 | 来源日期 | Skill 应该怎么做 |
|---|-------------|---------|-----------------|
| 1 | 声称完成但文件未落盘（6 次事故） | 05-25~05-30 | Phase 4 强制落盘 + PowerShell Test-Path 验证，验证通过才能说"完成" |
| 2 | 迭代凑数无差异（28 轮复制粘贴） | 05-25 | 每轮必须列出具体修改点（哪个文件、哪行、改了什么），无差异 = 跳过该轮 |
| 3 | 调研完不问要不要迭代 | 05-30 | Phase 4.3 强制提问"要不要迭代？给你 3 小时 100 轮" |
| 4 | 每次新会话不读历史记录 | 05-28 | Phase 0 读 research-profile + long-term + today，不重新问偏好 |
| 5 | 调研和迭代是独立但相辅相成的 | 05-31 | 路由拆分 r032（调研）/ r033（迭代），迭代模式读取已有报告 |
| 6 | 要多平台搜索，不接受单平台 | 05-27~05-30 | 默认 GitHub + X + Reddit + YouTube，每平台 5 热门 + 5 新鲜 |
| 7 | 搜索摘要不够，要点开网页读全文 | 05-31 | Phase 2 强制 WebFetch ≥5 个网页 |
| 8 | 要道法术器穿透分析，不停在表面 | 05-30 | 每个调研必须有道法术器四层穿透 |
| 9 | 要刚需判断，不是少数人的小众需求 | 05-30 | 刚需三问：频率 × 痛度 × 付费意愿 |
| 10 | 要和生态互联，不是孤岛任务 | 05-31 | 一鱼多吃协议：调研完自动更新 7 个生态文件 |
| 11 | AI 不读历史就重复搜索已覆盖内容 | 05-28 | 读 research-profile 历史调研索引，去重后再搜索 |
| 12 | 使用习惯应该沉淀成文件 | 05-31 | 每次调研后自动更新本文件，新会话直接读取 |

## 生态互联图

```
research-profile.md（本文件）
    ↑↓ 读写
deep-research skill (SKILL.md)
    ├── 启动时读：research-profile + long-term + today
    ├── 执行时写：outputs/*.md（调研报告）
    ├── 结束时写：
    │   ├── memory/{today}.md（今日记忆追加）
    │   ├── research-profile.md（本文件追加历史索引）
    │   ├── skill-usage-log.md（技能使用记录）
    │   ├── artifact-registry.md（产出登记）
    │   ├── memory-candidate（长期记忆候选）
    │   └── evolution-calendar.md（进化信号写入 workflow-inbox）
    └── 与 .claude/rules/ 共享：
        ├── 十条工程法则（法则 1 证据分层、法则 9 结构墙）
        ├── think-before-act（新问题必须研究先行）
        └── negative-results（死路归档）
```

---

*最后更新：2026-05-31 v3（deep-research v4 升级：60+ 参考 skill + 6 大场景 + YouTube 字幕 + 黄金法则）*
*数据来源：memory/2026-05-25.md ~ 2026-05-31.md + memory/long-term.md + 对话历史 + 5 个并行 Agent 扫描 187 个 skill*

---

## deep-research v4.0 参考 skill 清单

**调研/搜索类（10 个）**：step-search、research-daily、li-industry、find-skills、web-access、lazyweb-skill、follow-builders、X搜索语法生成器、全能网页采集器、baoyu-url-to-markdown

**DBS+认知框架（15 个）**：dbs-diagnosis（问题消解）、dbs-goal（发动机空转）、dbs-slowisfast（摩擦是信息）、dao-fa-shu-qi、li-devil（触发词从数据长出来）、karpathy-guidelines、cold-water、BROK提示词优化器、prompt-optimizer、taste-skill、gpt-tasteskill、dbs-action、li-content、dbs-deconstruct、dbs-hook

**迭代/工作流/记忆（15 个）**：li-improve（Promotion Pipeline）、longmemory（唯一写入者）、conversation-to-knowledge（教训必须有载体）、post-task-audit（第1次就强制执行）、li-sync（真源+分发）、li-memory、session-summary、daily-review、executing-plans、smart-task-planner-skill、li-plan、writing-plans、li-plan、li-workflow、skill-creator

**学习/教育/内容（15 个）**：interactive-learning（诊断起点）、thinking-coach（费曼技巧）、learning-boost、AI方法论学习器、shizhanying-coach、li-mindcoach、nature-skills、blog-post-writer、khazix-writer（四层自检）、viral-content-tools、案例拆解生成器（版本化迭代+黄金法则）、文风DNA分析、chinese-natural-voice-revision、niuma-voice-dna、jc-clarifier（行动锁）

**工具/采集/社媒（10 个）**：baoyu-danger-x-to-markdown、wechat-article-collector、transcript-cleaner、pdf、deepl、data-analysis、deep-review、personal-rag-qa、anything-to-notebooklm、output-skill
