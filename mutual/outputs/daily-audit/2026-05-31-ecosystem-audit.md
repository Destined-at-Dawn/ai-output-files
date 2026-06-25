# 生态系统每日健康报告 2026-05-31

> **审计类型**：每日自动健康检查（定时任务）
> **扫描范围**：186 skill 目录 × 5 工作区 + .claude/rules/ 一致性 + 路由表完整性
> **上次快照**：2026-05-26 审计报告（间隔 5 天）
> **重大事件**：v1.0.288 升级 + Temp 配置残留修复 + 第八/九条事故

---

## 系统指标（对比 05-26）

| 指标 | 今日(05-31) | 上次(05-26) | 变化 |
|------|-------------|-------------|------|
| skill 目录总数 | **186** | 189 | -3 |
| 有 SKILL.md 的 skill | **184** | 177 | +7 ✅ |
| 缺 SKILL.md | **2** | 12 | -10 ✅ 大幅改善 |
| 缺 description（扫描方式修正） | **63** | 5 | ⚠️ 方法变更，见注 |
| 超大 skill (>500行) | **18** | 17 | +1（guizang-ppt-skill） |
| 断裂路由 | **5** | 0 | 🔴 新增 |
| .claude/rules/ 一致性 | **10/27 共享** | 14/区一致 | 🔴 严重分裂 |
| 跨区三件套部署率 | **0/4** | 未检查 | 🔴 完全缺失 |
| skill-rules.json 覆盖 | **0/5 区** | 1/5 区(mutual无) | 🔴 全线缺失 |

**注**：description 缺失数从 5→63 是因为本次用 Python 解析 SKILL.md 内容（更严格），上次只检查了文件头部标记。实际无变化的 skill 约 9 个。

### CLAUDE.md 行数对比

| 工作区 | 今日(05-31) | 上次(05-26) | 变化 | 风险 |
|--------|-------------|-------------|------|------|
| **mutual** | 305 | 174 | +131 (+75%) | 🔴 翻倍增长 |
| **个人** | 609 | 539 | +70 (+13%) | 🔴 超 600 |
| **创作** | 692 | 568 | +124 (+22%) | 🔴 超 690 |
| **求职** | 655 | 585 | +70 (+12%) | 🔴 超 650 |
| **竞赛** | 668 | 598 | +70 (+12%) | 🔴 超 660 |
| **五区总计** | **2929** | 2464 | **+465** (+19%) | 🔴 全线膨胀 |

**趋势**：5 天增长 465 行（日均 +93 行）。按此速率，2 周内全线破 800 行。

---

## 🔴 断裂路由（5 条）

| 路由 ID | 名称 | 指向 skill | 状态 |
|---------|------|-----------|------|
| r001 | 小红书内容创作 | xhs-content-strategist | ❌ 未安装 |
| r008 | 天气查询 | weather-forecast | ❌ 未安装 |
| r026 | 上下文压缩 | context-compression | ❌ 未安装 |
| r028 | 工作流优化/自动化 | context-compression | ❌ 未安装（与 r026 同源） |
| r029 | 深度迭代研究 | auto-evolution | ❌ 未安装 |

**影响**：r001（小红书）是小黎核心变现场景的路由，confidence 0.95，但 skill 根本没装。r026/r028 共享同一个不存在的 skill。**路由表声称覆盖 31 条，实际可用 26 条（84%）。**

---

## 🔴 .claude/rules/ 严重分裂

上次报告称"5 个工作区 .claude/rules/ 完全一致（14 文件），跨区同步率 100%"。**今日核实：该结论是错误的。**

### 实际状态

| 工作区 | 规则文件数 | 说明 |
|--------|-----------|------|
| mutual | **20** | 最完整，含 skill-auto-activation、subagent-strategy、git-recovery |
| 竞赛 | **18** | 含 rtl-fpga-lessons.md（独有） |
| 个人 | **17** | 标准集 |
| 求职 | **17** | 标准集 |
| 创作 | **16** | 最少，且有 6 个独有规则 |

### 分裂详情（27 个唯一规则，仅 10 个五区共享）

**五区共享（10 个）**：10-engineering-laws、anti-info-overload、lifecycle-sop、mcp-config-protocol、memory-candidate-protocol、memory-confidence、no-root-rules-dir、powershell-safety、script-safety-check、think-before-act

**mutual 独有（4 个）**：skill-auto-activation、subagent-strategy、git-recovery、negative-results

**创作区独有（6 个）**：git-auto-sync、identity-and-preference、lesson-sink-checklist、privacy-sanitization、verification-and-archival-rules、RULES-INDEX

**竞赛区独有（1 个）**：rtl-fpga-lessons.md

**分裂影响**：
- 创作区有 `identity-and-preference.md`，其他区有 `identity-consistency.md` → 两套身份规则
- `negative-results`（负结果归档）只在 mutual/个人/求职/竞赛 4 区 → 创作区无负结果保护
- `anti-illusion-audit`（防假象）和 `boundary-declaration`（边界声明）不在创作区 → 创作区交付无审计门禁

---

## 跨区三件套部署状态（05-28 声称已落地）

| 文件 | mutual | 个人 | 创作 | 求职 | 竞赛 |
|------|--------|------|------|------|------|
| project-context/ | ✅ | ❌ | ❌ | ❌ | ❌ |
| artifact-registry.md | ✅ | ❌ | ❌ | ❌ | ❌ |
| workflow-inbox.md | ✅ | ❌ | ❌ | ❌ | ❌ |

**结论**：跨区三件套只在 mutual（管理区）存在，其他 4 个工作区**完全没有部署**。05-28 的"落地"声称违反了 PK-VERIFY-002（声称完成多文件同步前必须逐文件验证）。

---

## 其他工作区教训同步状态

| 工作区 | 最近 memory 活动 | 新教训（需同步到 mutual） |
|--------|-----------------|------------------------|
| 个人 | 05-29（9.6KB） | 有新内容，未扫描 |
| 创作 | 05-25（105B） | 低活跃，无新教训 |
| 求职 | 05-28（3.3KB） | 有新内容，未扫描 |
| 竞赛 | 05-29~30（ADC 结项 + STAR 研究） | 🔴 ADC closeout 9.9KB 新教训 + STAR 研究记录 |

**竞赛区**最活跃：ADC 工程结项报告（05-29）+ STAR 赛道研究记录（05-30），需要扫描是否有可复用经验。

---

## Skill 健康详情

### 缺 SKILL.md（2 个，大幅改善）

`AI分身迁移包/`、`_archive/` — 均非合法 skill 目录，建议归档或删除。

### 新增超大 skill（+1）

`guizang-ppt-skill`：542 行（新增超 500 行阈值）。

### 18 个超大 skill（行数变化微小）

`remotion-video(1575), imagegen-frontend-mobile(1466), image-to-code-skill(1229), hardware-design(1097), imagegen-frontend-web(988), hue(832), brandkit(799), dbs-xhs-title(737), office-hours(725), baoyu-slide-deck(699), NanoBanana-PPT-Skills(673), anything-to-notebooklm(633), openclawmp(596), x-article-publisher(546), guizang-ppt-skill(542), ffmpeg-usage(529), li-mindcoach(514), dbs-diagnosis(502)`

行数变化与 05-26 基本持平（每个 ±1-2 行），说明近期无大规模 skill 更新。

---

## Git 状态

| 工作区 | 最近提交 | 自 05-26 提交数 | 状态 |
|--------|---------|----------------|------|
| mutual | 05-31 08:31 | 43 | 🟢 活跃（NiumaAutoCommit 正常） |
| 个人 | 未确认 | — | 🟡 低活跃 |
| 创作 | 未确认 | — | 🟡 低活跃 |
| 求职 | 未确认 | — | 🟡 低活跃 |
| 竞赛 | 未确认 | — | 🟡 有新内容 |

**注意**：mutual 的 git status 显示 3 个跨工作区 untracked 文件（个人区 + 创作区的项目文件），说明 git repo 的工作树跨越了多个工作区。

---

## 待处理问题（按优先级）

### P0 — .claude/rules/ 严重分裂（10/27 共享）

5 个工作区只有 10 个规则文件完全一致。创作区有 6 个独有规则，其中 `identity-and-preference.md` 与其他区的 `identity-consistency.md` 冲突。**需要规则合并/统一行动。**

### P0 — 跨区三件套零部署

05-28 声称"落地"的 project-context/ + artifact-registry.md + workflow-inbox.md 只存在于 mutual，其他 4 区完全没有。需要补部署或重新评估是否需要。

### P1 — 5 条断裂路由

r001（小红书核心路由）指向不存在的 xhs-content-strategist。建议：安装该 skill 或将路由改为已有的相关 skill（如 dbs-xhs-title、投流帖改写）。

### P1 — CLAUDE.md 全线膨胀

五区总计 2929 行（5 天前 2464），日均 +93 行。上次审计建议的"方案 A：规则详情移入 .claude/rules/"尚未执行。

### P2 — skill-rules.json 全线缺失

05-26 报告已标记创作区 39 rules 覆盖 81 skills、mutual 缺失。现在 5 个区全部缺失 skill-rules.json。

### P2 — 9 个无 description 的常见 skill

`cold-water, karpathy-guidelines, lazyweb-skill, nature-skills, niuma-voice-dna, ppt-generator-pro, vercel-composition-patterns, vercel-react-native-skills, web-access` — 这些是系统提示词中列出的 skill，无 description 会影响路由匹配。

### P3 — 竞赛区 ADC closeout + STAR 研究教训未同步

竞赛区 05-29~30 有 ~11KB 新内容，需要扫描提取可复用经验。

---

## 趋势信号

- **🟢 正面**：SKILL.md 缺失从 12→2，大改善
- **🟢 正面**：mutual Git 活跃度正常（43 commits/5天），NiumaAutoCommit 无停摆
- **🟢 正面**：超大 skill 行数基本稳定，无失控增长
- **🟡 关注**：mutual CLAUDE.md 从 174→305 行（+75%），增速最快
- **🔴 风险**：.claude/rules/ 分裂比 05-26 报告描述的严重得多（上次报告错误声称"100%一致"）
- **🔴 风险**：跨区三件套部署率为 0%，上次"落地"声称不实
- **🔴 风险**：5 条断裂路由含核心场景（小红书变现 r001）
- **🔴 风险**：CLAUDE.md 膨胀未受控，治理注入本身正在制造膨胀

---

## 今日建议行动

1. **修复 r001 路由**：安装 xhs-content-strategist 或改路由指向 dbs-xhs-title（5 min）
2. **清理断裂路由**：r008/r026/r028/r029 指向不存在的 skill，需要安装或删除路由（10 min）
3. **统一 .claude/rules/**：以 mutual 的 20 个为基准，确定哪些应该五区共享、哪些是区特有（30 min，需用户决策）
4. **重新评估跨区三件套**：是否还需要在其他 4 区部署？还是只在 mutual 管理？（需用户决策）
5. **CLAUDE.md 瘦身**：执行方案 A（规则详情移入 .claude/rules/），优先处理个人区（609 行）和创作区（692 行）

---

## 防假象审计（本报告自检）

| 检查项 | 结果 |
|--------|------|
| N 选 1？ | 否，全部 skill 全量扫描 |
| 挑最高？ | 否，报告所有指标 |
| 取峰值？ | 否 |
| In-sample？ | N/A（磁盘扫描，非训练数据） |
| 流程完整？ | ✅ 五区全覆盖 + 路由表验证 + rules 一致性对比 |

**可信度**：全签核（Python os 模块直接读文件系统，非 Read 工具缓存）

---

> 本报告由 Daily Ecosystem Audit 定时任务自动生成
> 生成时间：2026-05-31 CST
> 审计工具：Python os.listdir + os.path.getsize（ground truth）
> 上次报告：2026-05-26-ecosystem-audit.md
