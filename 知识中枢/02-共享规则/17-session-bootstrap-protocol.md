# R17 新会话启动协议

> R16 定义了"读什么、写哪里"，R17 定义"怎么保证一定读了"。
> 来源：2026-05-25 防回退治理中发现——即使规则写好了，AI 也可能跳过读取步骤。

---

## 问题

R16 在 CLAUDE.md 中定义了读取顺序，但以下场景会导致跳过：

1. **上下文截断**：如果 R16 段落放在 CLAUDE.md 末尾（500+ 行之后），AI 可能看不到
2. **路径不可达**：引用的文件不存在（如 self-evolution/evolution-calendar.md 缺失）
3. **指令模糊**："按需读取"给了 AI 太多跳过借口
4. **缺少验证**：没有机制确认读取步骤是否真的执行了

## 核心规则

### 1. 启动序列必须放在 CLAUDE.md 最顶部

```markdown
# ⛔ 启动强制读取序列（最高优先级）

以下 Step 不可跳过。跳过任何一步 = 本次对话违规。

| Step | 操作 | 工具 |
|------|------|------|
| 1 | Read `memory/long-term.md` | 获取长期记忆 |
| 2 | Read `memory/{今天日期}.md` | 获取今日上下文 |
| 3 | Read `self-evolution/evolution-calendar.md` | 检查进化任务 |
| 4 | 若 Step 3 匹配 → 先执行进化任务 | auto-evolution Phase 1/2 |
```

### 2. 路径必须可达

- 所有引用的文件必须在实际路径存在
- 如果文件不存在，启动序列应报错而非静默跳过
- 使用绝对路径或相对于工作区根目录的路径

### 3. 禁止"按需读取"作为跳过借口

- Step 1-4 是**强制步骤**，不是"按需"
- 只有 SOPs/ 和 index.md 可以"按需读取"
- 任何标记为"必须执行"的步骤，不得以"用户没要求"为由跳过

### 4. 防回退自检

每次对话启动后，执行以下检查：

- [ ] `memory/long-term.md` 是否已 Read？
- [ ] `memory/{今天日期}.md` 是否已 Read？
- [ ] `self-evolution/evolution-calendar.md` 是否已 Read？
- [ ] `.claude/rules/no-root-rules-dir.md` 是否已加载？
- [ ] 当前写入路径是否包含孤立的 `rules/`（无 `.claude/` 前缀）？

### 5. 哨兵验证

- `.NO-RULES-DIR-HERE.md` 存在于每个工作区根目录
- `.claude/rules/_MIGRATED-TO-RULES.md` 是反向防御规则
- `.claude/rules/no-root-rules-dir.md` 明确禁止创建 `rules/`

---

## 五大工作区实施状态

| 工作区 | 启动序列在顶部 | memory/ 完整 | self-evolution/ 完整 | 防回退铁律 |
|--------|-------------|-------------|--------------------|----------|
| mutual | ✅ | ✅ | ✅ | ✅ |
| 个人 | ✅ | ✅ | ✅ | ✅ |
| 创作 | ✅ | ✅ | ✅ | ✅ |
| 求职 | ✅ | ✅ | ✅ | ✅ |
| 竞赛 | ✅ | ✅ | ✅ | ✅ |

---

## 关联规则

- R16 根目录优先约束架构
- `.claude/rules/no-root-rules-dir.md`
- `.claude/rules/_MIGRATED-TO-RULES.md`
- `CLAUDE.md` § ⛔ 防回退铁律

---

> 创建日期：2026-05-25
> 优先级：P0 — 所有工作区必须遵守
