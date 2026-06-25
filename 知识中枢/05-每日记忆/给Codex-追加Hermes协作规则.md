# 任务：在 .codex/AGENTS.md 追加 Hermes 记忆中枢协作规则

> 把下面的内容追加到 `C:\Users\13975\.codex\AGENTS.md` 文件末尾。
> 用 patch 精确追加，不要覆盖全文。

---

## 要追加的内容（复制此代码块之后的内容）

```markdown

### **Hermes 记忆中枢协作**
- **读取**：创建/优化 Skill 或 SOP 前，读取 `E:\ai产出文件\牛马\知识中枢\01-工作区记忆\hermes-memory\` 下的 atomic-facts.md、cross-tool-state.md、tool-ecosystem-scan.md
- **不写入** hermes-memory/（Hermes 专属写入区）
- **交接**：需要 Hermes 处理的内容写到 `E:\ai产出文件\牛马\知识中枢\05-每日记忆\YYYY-MM-DD-Codex-{主题}.md`
- **触发**：创建 Skill、修改 SOP、发现事实变更、发现矛盾时
```

---

## 完成后

1. 确认追加成功（Read 验证文件末尾内容）
2. 回复"Hermes 协作规则已追加"

---
> [auto-consumed] 2026-06-21 by Hermes cron — 任务已验证完成（协作规则已部署、pre-action-check 已创建），归档处理。
