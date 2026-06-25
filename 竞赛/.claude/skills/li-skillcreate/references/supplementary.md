## 案例库

| # | 案例 | 场景 | 结果 | 关键教训 |
|---|------|------|------|---------|
| 1 | 创建 li-hardware | 用户说"FPGA 相关的技能"，Phase 1 搜本地发现无硬件类 skill，Phase 1.1b 联网搜到 Verilog-AI(356★)等参考 | 成功创建，触发词从 5 个扩展到 18 个，路由命中率 85% | 不搜外部就造 = 闭门造车；先读 5 个已有 skill 提取设计模式 |
| 2 | 创建 li-analyze | 用户说"数据分析技能"，Phase 0 消解发现 li-content 已覆盖部分内容，但缺乏结构化分析能力 | 成功创建，与 li-content 形成互补（内容创作 vs 数据分析） | Phase 0 消解能发现重叠，避免重复造轮子 |
| 3 | 融合 li-content → li-analyze | 用户发现 li-content 和 li-analyze 功能重叠 60%，触发 li-skillfusion | 融合后 li-analyze 接管分析能力，li-content 专注内容创作，触发词合并去重 | 融合比新建好——减少 skill 总数，提高每个 skill 的触发精度 |

> 详细案例 → `references/anti-failure-patterns.md` § 消解案例

## 反模式（8 条）

| # | 反模式 | 为什么错 | 正确做法 |
|---|--------|---------|---------|
| A1 | 不搜外部就创建 | 闭门造车，可能已有更好的现成方案 | Phase 1.1b 四阶段全平台搜索，至少搜 skills.sh + GitHub |
| A2 | 不注册路由表 | 技能存在但永远不会被触发 = 磁盘垃圾 | Phase 5 ① 强制注册路由表，≥15 触发词 |
| A3 | 批量创建低质量 skill | 每个 skill 都有维护成本，低质量 = 负资产 | 先消解（Phase 0），确认需要才创建；质量门禁 < 20 分重做 |
| A4 | 不读已有 skill 就造新的 | 看不到生态中已有的设计模式和最佳实践 | Phase 1 强制读取 ≥5 个相关 skill，每个提取 1-3 个设计决策 |
| A5 | 触发词是猜的 | 路由不生效，用户得手动说"用 xxx 技能" | 从用户真实对话中采集触发词；创建后观察 1 周调整 |
| A6 | 迭代只改版本号 | 28 轮迭代中 27 轮复制粘贴 = 假迭代 | 每轮修改 ≥25% 内容，必须有实质性差异 |
| A7 | 创建完不问迭代 | 用户不满意但不好意思说，技能就废了 | 创建完成后必须问"要迭代吗？"并说明迭代窗口 |
| A8 | Write 后不 Read 验证 | 断言"已创建"但磁盘可能为空（6 次事故） | Write → ls → Read → 检查大小 → 全过才能说"已创建" |

> 详细失败模式（12 个）→ `references/anti-failure-patterns.md`

## 联动技能（7 个）

| 技能 | 联动方式 | 触发场景 |
|------|---------|---------|
| li-bestskill | 上游（搜索） | Phase 1 联网搜索时调用，发现外部优秀 skill 作为参考 |
| li-skillfusion | 下游（融合） | 发现功能重叠的 skill 时，融合而非新建 |
| li-manage | 并行（生命周期） | 创建后注册到画像、更新工作流数据 |
| li-local-search | 上游（本地查重） | Phase 1.1a 扫描本地生态，避免重复创建 |
| li-devil | 内置（预验尸） | Phase 0 + Phase 3 = 先想"做错了会怎样" |
| li-improve | 下游（进化） | 教训固化，Phase 7 沉淀规则 |
| li-memory | 下游（知识沉淀） | 创建经验提取为原子事实存入 L2 |

> 触发条件和联动方式 → `references/ecosystem-integration.md`

## 参考技能 & 外部研究

**融合 21 个参考**：13 个本地 skill + 8 个外部项目（Letta 23.2K★ / HyperAgents 2.6K★ / Hue 3.7K★ 等）。详见 `references/reference-skills.md` + `references/external-research.md`

---

> See references/ for conditional-next-steps, external-research, and notes.


## Conditional Next Steps
| Signal | Action | Chain |
|--------|--------|-------|
| [Phase complete] | Determine next phase | Continue within this skill |
| [External data needed] | Call li-research or li-bestskill | Research phase |
| [Quality check needed] | Call li-devil for cold water review | Devil review |
| [User unhappy] | Call li-mindcoach for mindset shift | Mindcoach |
| [Memory update needed] | Call li-memory for fact extraction | Memory |
| [Cross-workspace sync] | Call li-sync | Sync |
