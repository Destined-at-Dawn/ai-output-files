# 12篇文章信息差 × 牛马工作流 差距分析

> 日期: 2026-06-10
> 来源: 12篇文章信息差总结-道法术器版.md
> 分析对象: mutual 工作区工作流（CLAUDE.md + 109条路由 + 30个skill + SOP体系）

---

## 道层（4条）— 决定"做不做、做什么"

### 信息差1: Agent = 系统, 不是模型

| 维度 | 文章标准 | 当前状态 | 差距 |
|------|----------|----------|------|
| 认知框架 | Agent = 模型+上下文+工具+编排+安全+评估+日志 | CLAUDE.md 覆盖了大部分，但没有用7层框架组织 | 🟡 中 |
| 具体表现 | 每个决策都要考虑7层 | 我们的CLAUDE.md是扁平的规则列表，没有分层 | 需重构 |

**优化动作**: 无需重构CLAUDE.md为7层格式（过度工程），但需要在li-intent的SOP匹配中引入"系统级思考"——每次skill调用前考虑：上下文是否充分？工具选择对不对？日志是否记录？

### 信息差2: Harness 工程 > 模型工程

| 维度 | 文章标准 | 当前状态 | 差距 |
|------|----------|----------|------|
| Harness层 | MEMORY/TOOLS/SKILLS/KNOWLEDGE/LOG/PLAN独立优化 | 各层都有但互相独立，没有统一的优化视角 | 🟡 中 |
| Agent Loop | research→plan→build→review | li-intent有Phase 0-4，但不是强制的 | 需加强 |

**优化动作**: 在li-intent中强制引入Agent Loop四阶段（research→plan→build→review），每个复合意图必须走完整个循环。

### 信息差3: Skill 选择 = 结构推理, 不是相似匹配

| 维度 | 文章标准 | 当前状态 | 差距 |
|------|----------|----------|------|
| 推理方式 | Skill DAG + 类型化接口 + 结构推理 | 纯关键词匹配（trigger词） | 🔴 大 |
| 接口规范 | Input/Output类型化 | 无接口规范，skill之间通过文件传递 | 🔴 大 |
| 调用方式 | DAG自动编排 | 手动在li-intent中写死调用链 | 🔴 大 |

**这是最大的差距。** 当前109条路由全是"trigger词→skill名"的扁平映射，完全没有：
- skill之间的数据流关系
- 输入输出类型匹配
- DAG编排能力

**优化动作**: 
1. 为核心skill链定义Input/Output接口（简化版，不做类型系统）
2. 在li-intent中实现简单DAG：定义skill之间的数据流依赖
3. 路由表增加 `chain` 字段，支持多skill链式调用

### 信息差4: 合成数据不是万能的

| 维度 | 文章标准 | 当前状态 | 差距 |
|------|----------|----------|------|
| 合成数据质量 | 奖励模型+少而精+半自动 | 无质量控制 | 🟡 中 |
| 人工审核 | Agent先审，关键再人工 | memory-candidate-protocol有类似机制 | ✅ 基本满足 |

**优化动作**: 在auto-evolution skill中增加合成数据质量门禁——自动生成的规则/记忆必须经过"5条法则审计"才能入库。

---

## 法层（5条）— 决定"系统性问题的系统解"

### 信息差5: Skill ABCD 分类法

| 维度 | 文章标准 | 当前状态 | 差距 |
|------|----------|----------|------|
| 分类框架 | A(Atomic)/B(Bundled)/C(Composite)/D(Derived) | 无分类 | 🔴 大 |
| 治理方式 | 按类别不同治理策略 | 一刀切治理 | 需改进 |

**ABCD分类结果**（基于30个本地skill）:

| 类型 | 含义 | Skill列表 |
|------|------|-----------|
| **A 原子技能** | 独立任务一步到位 | weather-forecast, markitdown, pdf, xlsx, pptx, baoyu-image-gen, baoyu-post-to-wechat, baoyu-post-to-twitter, baoyu-mcp-build, baoyu-post-zh, baoyu-suno, baoyu-luma, baoyu-openclaw, jina-reader, svg-to-png, ppt-generator-pro, mcp-creator, feishu-doc-reader, feishu-doc-writer, transcript-cleaner, self-intro-writer, storage-analyzer, internal-comms, code |
| **B 组合技能** | 多步有状态 | baoyu-url-to-markdown, li-local-search, session-summary, daily-review, context-compression, auto-evolution, competition-workflow, shizhanying-coach, university-planner, writing-plans, jc-jiaocheng, learning-boost, interactive-learning, ai-yuyi, aihot, hv-analysis, prompt-optimizer, siyuliebian, devils-advocate, hardware-design, doc-coauthoring, dao-fa-shu-qi, thinking-coach, deep-research, neat-freak |
| **C 复合技能** | 调度多个skill | li, li-intent, li-sop-manage |
| **D 衍生技能** | 从C中派生 | li-sync, li-memory, li-bestskill, li-skillcreate, li-skillfusion, li-manage, li-diagnose, li-improve, li-transcript, li-scan-meta, li-tuiwen, li-writer, li-brand, li-research, li-debug, li-hardware, li-devil, li-analyze, li-report, li-mindcoach, li-health, li-safe, li-hook-cleanup, li-optimize, li-playbook, li-security-scan, li-quickstart, xhs-content-strategist, xhs-title-generator, xhs-account-planner |

**优化动作**: 在路由表中增加 `category` 字段（A/B/C/D），不同类别不同治理策略。

### 信息差6: 知识库三层结构

| 维度 | 文章标准 | 当前状态 | 差距 |
|------|----------|----------|------|
| Layer 0 | 模板/碎片（提炼后的通用知识） | 无独立层 | 🔴 大 |
| Layer 1 | 知识卡（独立文档） | memory/ + outputs/ 部分覆盖 | 🟡 中 |
| Layer 2 | Skill/SOP（可执行） | skills/ + SOPs/ 覆盖 | ✅ 基本满足 |

**当前知识散布**: memory/long-term.md（混合了偏好+教训+知识）、outputs/（混合了产出+分析）、.claude/rules/（混合了约束+工程法则+认知科学）

**优化动作**: 
1. 创建 `knowledge-base/` 目录，存放Layer 0模板和Layer 1知识卡
2. 将memory/long-term.md中可复用的知识提取为知识卡
3. 将.claude/rules/中的认知科学支撑提取为模板

### 信息差7: Pass@k vs Pass^k

| 维度 | 文章标准 | 当前状态 | 差距 |
|------|----------|----------|------|
| 可靠性指标 | Pass@1 vs Pass^1区分 | 无指标 | 🟡 中 |
| Skill评分 | 通过率/失败率追踪 | skill-usage-log.md有记录但无评分 | 需改进 |

**优化动作**: 在skill-usage-log.md中增加成功率统计，每月汇总。

### 信息差8: Skill 治理三层

| 维度 | 文章标准 | 当前状态 | 差距 |
|------|----------|----------|------|
| 检索 | 多路召回+交叉验证 | li-local-search有但未强制 | 🟡 中 |
| 进化 | 淘汰+合并+生成新skill | li-manage Flow E有但未强制执行 | 🟡 中 |
| 瘦身 | 不用的skill定期清理 | 无机制 | 🔴 大 |

**当前30个skill中可能冗余的**:
- interactive-learning ↔ thinking-coach（功能重叠）
- ai-yuyi ↔ aihot（AI内容方向重叠）
- daily-review ↔ session-summary（总结类重叠）
- writing-plans ↔ doc-coauthoring（写作类重叠）

**优化动作**: 在li-manage Flow E中增加强制瘦身——每季度审查，连续30天未使用的skill标记为"沉睡"，90天未使用标记为"待淘汰"。

### 信息差9: Agentic Workflow 四阶段

| 维度 | 文章标准 | 当前状态 | 差距 |
|------|----------|----------|------|
| Research | 先调研再动手 | li-intent Phase 1有SOP查找 | ✅ |
| Plan | 有计划再执行 | 无强制计划阶段 | 🟡 |
| Build | 执行 | li-intent Phase 3有执行 | ✅ |
| Review | 复盘验证 | li-intent Phase 4有模式晋升 | 🟡 |

**优化动作**: 在li-intent的Phase 0中增加强制"Plan"阶段——复合意图必须先输出执行计划（哪个skill、什么顺序、预期输出），然后执行。

---

## 术层（3条）— 决定"怎么做"

### 信息差10: 受众优先原则

| 维度 | 文章标准 | 当前状态 | 差距 |
|------|----------|----------|------|
| 受众分析 | 先想清楚给谁看 | content_create意图无受众分析 | 🟡 中 |
| 应用范围 | 所有内容创作 | 只在小红书skill中有受众概念 | 需扩展 |

**优化动作**: 在li-intent的content_create意图中增加"受众分析"步骤——自动判断目标受众并调整输出风格。

### 信息差11: 安全红灯

| 维度 | 文章标准 | 当前状态 | 差距 |
|------|----------|----------|------|
| Vibe Coding安全 | 不是边界，是红灯 | .claude/rules/script-safety-check.md覆盖 | ✅ |
| 执行前确认 | 强制确认 | dry-run+确认机制已有 | ✅ |

**当前已覆盖的安全机制**: script-safety-check.md, no-blind-overwrite.md, chinese-path-safety.md, powershell-safety.md, R19并发降级

**优化动作**: 基本满足，但需要在li-safe skill中增加"vibe coding"场景的专项检查（AI生成代码的安全审计）。

### 信息差12: 拼屏/断联 workarounds

| 维度 | 文章标准 | 当前状态 | 差距 |
|------|----------|----------|------|
| 拼屏 | Agent+Duet并行 | Workflow工具支持多Agent | ✅ |
| 断联 | Mosh+tmux+AgentMail | 未使用（本地开发不需要） | N/A |

**优化动作**: 无需。本地开发不涉及远程断联问题。

---

## 器层（3条）— 决定"用什么工具"

### 信息差13: Prompt→URL 快速部署

| 维度 | 文章标准 | 当前状态 | 差距 |
|------|----------|----------|------|
| 快速部署 | Prompt→网页工具 | baoyu-openclaw支持但未常用 | 🟡 低 |
| 应用场景 | 简单工具类skill | 无 | 可选 |

**优化动作**: 低优先级。记录为可选优化。

### 信息差14: 软件工程基底

| 维度 | 文章标准 | 当前状态 | 差距 |
|------|----------|----------|------|
| 基底复用 | 别重复造轮子 | CLAUDE.md+规则+skill大部分基于现有框架 | ✅ |

**优化动作**: 无需。

### 信息差15: 远程工作基础设施

| 维度 | 文章标准 | 当前状态 | 差距 |
|------|----------|----------|------|
| 远程工具 | Mosh/tmux/AgentMail | 未使用 | N/A |

**优化动作**: 无需。本地开发场景不适用。

---

## 差距总结: 优先级排序

| 优先级 | 差距 | 影响范围 | 预计工作量 |
|--------|------|----------|-----------|
| 🔴 P0 | 信息差3: Skill DAG + 接口规范 | 全部路由 | 大（重构路由逻辑） |
| 🔴 P0 | 信息差5: ABCD分类 | 全部30个skill | 中（分类+治理策略） |
| 🔴 P0 | 信息差6: 知识库三层结构 | 全部知识 | 中（目录重构+迁移） |
| 🔴 P0 | 信息差8: Skill瘦身 | 冗余skill | 小（审查+合并） |
| 🟡 P1 | 信息差2: Agent Loop强制 | li-intent | 小（增加Plan阶段） |
| 🟡 P1 | 信息差7: 可靠性指标 | skill-usage-log | 小（增加统计） |
| 🟡 P1 | 信息差9: Plan阶段强制 | li-intent | 小（增加Phase） |
| 🟡 P1 | 信息差10: 受众优先 | content_create | 小（增加分析步骤） |
| 🟢 P2 | 信息差1/4/11/13/14/15 | 各种 | 微小或N/A |

