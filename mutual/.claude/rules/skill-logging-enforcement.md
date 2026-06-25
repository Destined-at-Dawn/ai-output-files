# Skill 调用日志强制执行规则

> 优先级：最高（与 script-safety-check 同级）
> 创建：2026-06-05
> 根因：li-local-search Layer 3 和 li-manage Flow A-F 写在 SKILL.md 里但从不被执行。
>        SKILL.md 是参考文档，不是执行约束。只有 .claude/rules/ 才是 AI 的行为强制层。

---

## 铁律 1：每次 skill 调用后必须记录

**触发**：AI 通过 `mcp__skill-handler__Skill` 调用了任何 skill。

**执行**：调用完成后，立即追加一行到 `C:\Users\13975\.newmax\skill-usage-log.md` 的"调用记录"表：

```markdown
| {YYYY-MM-DD} | {HH:MM} | {工作区} | {skill名} | {触发词/场景} | {✅成功/❌失败/⚠️部分} | {一句话结果} |
```

**不可跳过**。没有"这次太简单不用记录"的例外。

---

## 铁律 2：对话结束前必须回检漏调

**触发**：对话即将结束（用户说"结束"/"再见"/最后一条回复前）。

**执行**：
1. 回顾本次对话做了什么任务
2. 检查是否有"应该用 skill 但用了原生能力"的情况
3. 如果有 → 追加到 skill-usage-log.md 的"漏调记录"表
4. 如果没有 → 不记录

**判断标准**：如果任务涉及"内容创作/文档处理/图片生成/视频/学习/商业分析"且没有调用对应 skill → 算漏调。

---

## 铁律 3：每日首次对话必须检查 skill-usage-log.md

**触发**：每日第一次对话开始时（CLAUDE.md 启动序列 Step 4.5 之后）。

**执行**：
1. Read `C:\Users\13975\.newmax\skill-usage-log.md`
2. 检查"每日统计"区域是否有昨天的汇总
3. 如果没有 → 补写昨天的每日统计
4. 如果文件不存在 → 创建文件并初始化

---

## 铁律 4：SOP 候选必须检测

**触发**：每次对话结束前。

**执行**：
1. 读取 skill-usage-log.md 的"原生能力处理"区域
2. 检查是否有同一类任务出现 ≥ 3 次且无对应 SOP
3. 如果有 → 追加到"SOP 候选"区域，并告知用户
4. 如果没有 → 不记录

---

## 铁律 5：沉睡技能必须在 li-manage Flow E 中处理

**触发**：每周六（与 li-bestskill 周报同日）或用户说"优化技能"/"哪些skill没用"。

**执行**：
1. 读取 skill-usage-log.md 的"月度分析"区域
2. 找出"沉睡技能 Top 10"
3. 对每个沉睡技能执行泼冷水审查：
   - 真的需要这个 skill 吗？（精要主义 013）
   - 有更好的替代品吗？（li-bestskill 外部搜索）
   - 是不是路由没配对导致没被触发？（检查 skill-routing-table.json）
4. 生成优化建议（杠铃式：保守端 + 激进端）
5. 追加到 skill-usage-log.md 的"月度分析"区域

---

## 数据文件位置

| 文件 | 路径 | 用途 |
|------|------|------|
| **技能使用日志** | `C:\Users\13975\.newmax\skill-usage-log.md` | 所有调用记录+统计+分析 |
| **对话日志** | `C:\Users\13975\.newmax\conversation-journal\{date}.md` | 每日对话记录 |
| **用户全局画像** | `C:\Users\13975\.newmax\user-profile.md` | 跨工作区用户信息 |
| **路由表** | `E:\ai产出文件\牛马\mutual\mutual\skill-routing-table.json` | 技能触发词配置 |

---

## 与 SKILL.md 的关系

- **SKILL.md**（li-local-search/li-manage）：描述"怎么做"（算法、模板、数据流）
- **本规则**（.claude/rules/skill-logging-enforcement.md）：强制"必须做"（行为约束）

SKILL.md 里的 Layer 3 和 Flow A-F 是详细实现指南。本规则是执行保障。
没有本规则，SKILL.md 里的流程永远不会被执行（2026-06-05 已验证）。

---

## 铁律 6：skill 调用日志必须记录协议执行状态（2026-06-11 新增）

**触发**：AI 调用任何 li- skill。

**执行**：在 skill-usage-log.md 的调用记录中，增加一列「协议执行」：

```markdown
| {日期} | {时间} | {工作区} | {skill名} | {触发词} | {结果} | {一句话} | {协议: ✅已读/❌跳过/⚠️部分} |
```

**判断标准**：
- ✅ 已读：执行前 Read 了 SKILL.md 执行协议中列出的所有必读 references/ 文件
- ⚠️ 部分：读了部分但遗漏了某些必读文件
- ❌ 跳过：没有读任何 references/ 就执行了 Phase

**每月审查**：li-manage Flow E 中增加「协议执行率」指标：
- 协议执行率 = ✅ / (✅ + ⚠️ + ❌)
- 目标：≥90%
- <70% → 触发 skill-execution-discipline.md 专项审查

---

## 违规检测

如果出现以下情况，说明本规则被违反了：
- [ ] skill-usage-log.md 不存在或为空
- [ ] 对话中调用了 skill 但日志中没有记录
- [ ] 连续 3 天没有"每日统计"
- [ ] 沉睡技能超过 30 天未被 li-manage Flow E 审查
- [ ] li- skill 调用记录中「协议执行」列全部为空或 ❌
