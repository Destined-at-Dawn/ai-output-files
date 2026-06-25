# 任务：在 .claude/CLAUDE.md 追加 Hermes 记忆中枢协作规则

> 把下面的内容追加到 `C:\Users\13975\.claude\CLAUDE.md` 文件末尾（最后一个 CRITICAL RULE 之后）。
> 用 patch 精确追加，不要覆盖全文。

---

## 要追加的内容（复制此代码块之后的内容）

```markdown
---

## 🔴 CRITICAL RULE: Hermes 记忆中枢协作规则

**适用条件**：所有 Claude Code 工作区，无条件生效。

### 1. 读取规则

创建/优化 Skill 或 SOP 前，优先读取 Hermes 记忆：
- `E:\ai产出文件\牛马\知识中枢\01-工作区记忆\hermes-memory\facts\atomic-facts.md` — 原子事实库
- `E:\ai产出文件\牛马\知识中枢\01-工作区记忆\hermes-memory\state-tracking\cross-tool-state.md` — 跨工具状态
- `E:\ai产出文件\牛马\知识中枢\01-工作区记忆\hermes-memory\state-tracking\tool-ecosystem-scan.md` — 工具生态全景

### 2. 写入规则

- ❌ **禁止**写入 `hermes-memory/` 目录（Hermes 专属写入区）
- ✅ 需要交接给 Hermes 的内容写到：`E:\ai产出文件\牛马\知识中枢\05-每日记忆\`
- 文件命名规范：`YYYY-MM-DD-{来源工具}-{主题}.md`

### 3. 触发场景

| 场景 | 操作 |
|------|------|
| 创建新 Skill | 先读 atomic-facts + tool-ecosystem-scan |
| 修改 SOP | 先读 cross-tool-state 确认当前状态 |
| 发现事实变更 | 写交接文件到 05-每日记忆/ |
| 发现矛盾 | 写交接文件，标记 [矛盾] |
```

---

## 完成后

1. 确认追加成功（Read 验证文件末尾内容）
2. 回复"Hermes 协作规则已追加"

---
> [auto-consumed] 2026-06-21 by Hermes cron — 任务已验证完成（协作规则已部署、pre-action-check 已创建），归档处理。
