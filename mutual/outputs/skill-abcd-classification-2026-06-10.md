# Skill ABCD 分类 + 冗余审计

> 日期: 2026-06-10
> 方法论: 信息差5 — Skill选择是结构推理，不是相似匹配
> 治理策略: 不同类别不同生命周期管理

---

## 分类框架

| 类型 | 含义 | 治理策略 | 审查频率 |
|------|------|----------|---------|
| **A 原子** | 一步到位，Input→Output | 只维护，不优化 | 季度 |
| **B 组合** | 多步有状态，有生命周期 | 定期优化 | 月度 |
| **C 调度** | 编排其他skill | 优先优化 | 周度 |
| **D 衍生** | 从C中派生，不独立存在 | 可合并/淘汰 | 月度 |

---

## 本地 Skill 分类（30个）

### A 类 — 原子技能（8个）

| Skill | 功能 | Input | Output | 路由数 |
|-------|------|-------|--------|--------|
| code | 写代码 | 代码需求 | 代码文件 | 1 |
| transcript-cleaner | 转录清理 | 视频/音频 | 文字稿 | 3 |
| self-intro-writer | 自我介绍 | 个人信息 | 介绍文档 | 3 |
| storage-analyzer | 磁盘分析 | 路径 | 报告 | 3 |
| internal-comms | 内部沟通 | 消息类型 | 文案 | 3 |
| feishu-doc-reader | 飞书读取 | 文档token | 内容 | 3 |
| feishu-doc-writer | 飞书写入 | 内容 | 文档 | 3 |
| prompt-optimizer | Prompt优化 | 原始prompt | 优化prompt | 3 |

### B 类 — 组合技能（16个）

| Skill | 功能 | 步骤数 | 有状态 | 路由数 |
|-------|------|--------|--------|--------|
| auto-evolution | 自我进化 | 4 | ✅记忆 | 3 |
| competition-workflow | 竞赛 | 6 | ✅项目 | 3 |
| context-compression | 上下文压缩 | 3 | ✅session | 3 |
| daily-review | 日回顾 | 3 | ✅日记 | 3 |
| dao-fa-shu-qi | 道法术器分析 | 4 | ❌ | 3 |
| deep-research | 深度研究 | 5 | ✅项目 | 3 |
| devils-advocate | 魔鬼辩护 | 3 | ❌ | 3 |
| doc-coauthoring | 文档共著 | 4 | ✅文档 | 3 |
| hardware-design | 硬件设计 | 6 | ✅项目 | 3 |
| hv-analysis | 高压分析 | 5 | ✅分析 | 3 |
| interactive-learning | 互动学习 | 4 | ✅知识 | 3 |
| learning-boost | 学习加速 | 3 | ✅知识 | 3 |
| thinking-coach | 思维教练 | 5 | ✅认知 | 3 |
| shizhanying-coach | 实战营教练 | 3 | ✅进度 | 3 |
| university-planner | 大学规划 | 4 | ✅规划 | 3 |
| writing-plans | 写作计划 | 3 | ✅计划 | 3 |
| jc-jiaocheng | 教程生成 | 4 | ✅教程 | 3 |
| neat-freak | 整理清理 | 5 | ✅目录 | 3 |
| session-summary | 会话总结 | 3 | ✅记忆 | 3 |
| ai-yuyi | AI语义 | 3 | ❌ | 3 |
| aihot | AI热点 | 3 | ✅追踪 | 3 |
| siyuliebian | 四域裂变 | 4 | ✅IP | 3 |

### C 类 — 调度技能（3个）

| Skill | 功能 | 编排的子skill | 路由数 |
|-------|------|-------------|--------|
| **li** | 总路由器 | 所有skill | 3 |
| **li-intent** | 意图理解引擎 | li-*系列 | 3 |
| **li-sop-manage** | SOP管理 | SOP相关 | 3 |

### D 类 — 衍生技能（27个，全部在li/下）

| Skill | 来源 | 功能 | 独立性 |
|-------|------|------|--------|
| li-analyze | li-intent | 分析 | 低 |
| li-bestskill | li-manage | 技能评估 | 中 |
| li-brand | li | 品牌 | 低 |
| li-debug | li | 调试 | 中 |
| li-devil | li | 魔鬼辩护 | 低(=devils-advocate的衍生) |
| li-diagnose | li | 诊断 | 中 |
| li-hardware | li | 硬件 | 低(=hardware-design的衍生) |
| li-health | li | 健康 | 低 |
| li-hook-cleanup | li | 钩子清理 | 低 |
| li-improve | li | 改进 | 低 |
| li-local-search | li | 本地搜索 | 中 |
| li-manage | li | 管理 | 中 |
| li-memory | li-intent | 记忆 | 低 |
| li-mindcoach | li-intent | 思维教练 | 低(=thinking-coach的衍生) |
| li-optimize | li | 优化 | 低 |
| li-playbook | li | 剧本 | 低 |
| li-quickstart | li | 快速启动 | 低 |
| li-report | li | 报告 | 低 |
| li-research | li | 研究 | 低(=deep-research的衍生) |
| li-safe | li | 安全 | 低 |
| li-scan-meta | li | 元扫描 | 低 |
| li-security-scan | li | 安全扫描 | 低(=li-safe的衍生) |
| li-skillcreate | li-manage | 技能创建 | 中 |
| li-skillfusion | li-manage | 技能融合 | 中 |
| li-sync | li | 同步 | 中 |
| li-transcript | li | 转录 | 低(=transcript-cleaner的衍生) |
| li-tuiwen | li | 推文 | 低 |
| li-writer | li | 写作 | 低 |
| xhs-account-planner | li | 小红书规划 | 中 |
| xhs-content-strategist | li | 小红书内容 | 中 |
| xhs-title-generator | li | 小红书标题 | 低 |

---

## 冗余审计结果

### 🔴 建议合并（功能高度重叠）

| 重叠组 | 涉及skill | 建议 | 理由 |
|--------|-----------|------|------|
| **思维教练组** | interactive-learning + thinking-coach + li-mindcoach | 合并为 thinking-coach | 三者功能本质相同：引导式学习/思考 |
| **研究组** | deep-research + li-research | 保留 deep-research，li-research作为衍生 | deep-research有独立SKILL.md，li-research只是调用它 |
| **调试组** | devils-advocate + li-devil | 保留 devils-advocate，li-devil作为衍生 | 同上 |
| **硬件组** | hardware-design + li-hardware | 保留 hardware-design，li-hardware作为衍生 | 同上 |
| **总结组** | daily-review + session-summary | 保留 session-summary，daily-review合并进去 | session-summary更通用 |
| **AI内容组** | ai-yuyi + aihot | 保留 aihot（更大），ai-yuyi合并进去 | aihot覆盖了AI语义功能 |
| **安全组** | li-safe + li-security-scan | 合并为 li-safe | 完全重叠 |
| **写作组** | writing-plans + doc-coauthoring + li-writer | 保留 doc-coauthoring（最大），其余合并 | doc-coauthoring覆盖最广 |

### 🟡 建议保留但标注关系

| Skill | 关系 | 处理 |
|-------|------|------|
| prompt-optimizer | 与li-optimize功能类似但面向不同场景 | 保留，标注"Prompt专项" |
| xhs-content-strategist + xhs-title-generator + xhs-account-planner | 三个小红书skill | 保留独立，但标注"小红书三件套" |
| siyuliebian | 独立IP裂变方法论 | 保留，标注"独立方法论" |

### 🟢 明确保留（无冗余）

auto-evolution, competition-workflow, context-compression, feishu-doc-reader, feishu-doc-writer, hv-analysis, jc-jiaocheng, learning-boost, neat-freak, self-intro-writer, shizhanying-coach, storage-analyzer, transcript-cleaner, university-planner, viral-content-tools, code, internal-comms

---

## 合并执行计划

| 步骤 | 操作 | 影响 |
|------|------|------|
| 1 | interactive-learning → thinking-coach | 3个路由更新 |
| 2 | ai-yuyi → aihot | 3个路由更新 |
| 3 | li-safe + li-security-scan → li-safe | 路由合并 |
| 4 | writing-plans → doc-coauthoring | 3个路由更新 |
| 5 | daily-review → session-summary | 3个路由更新 |
| 6 | D类衍生skill标注"不独立调用" | 路由表标注 |

**合并后预期**: 30个 → ~24个本地skill，D类27个保留但标注依赖关系。
