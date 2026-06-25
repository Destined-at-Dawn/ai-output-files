# 任务：在 Marvis rules.md 追加 Hermes 记忆中枢协作规则

> 把下面的内容追加到 `E:\Marvis\MarvisAgent\1.0.1000.104\prompts\core\rules.md` 文件末尾。
> 用 patch 精确追加，不要覆盖全文。

---

## 要追加的内容（复制此代码块之后的内容）

```markdown

## Hermes 记忆中枢协作

### 读取规则
执行文档处理或桌面操作前，可读取 Hermes 记忆获取上下文：
- `E:\ai产出文件\牛马\知识中枢\01-工作区记忆\hermes-memory\facts\atomic-facts.md`
- `E:\ai产出文件\牛马\知识中枢\01-工作区记忆\hermes-memory\state-tracking\tool-ecosystem-scan.md`

### 写入规则
- ❌ 禁止写入 hermes-memory/
- ✅ 交接内容写到 `E:\ai产出文件\牛马\知识中枢\05-每日记忆\YYYY-MM-DD-Marvis-{主题}.md`

### 触发场景
- 文档处理完成 → 写交接文件记录产出
- 桌面操作产生有价值的结果 → 写交接文件
```

---

## 完成后

1. 确认追加成功（Read 验证文件末尾内容）
2. 回复"Hermes 协作规则已追加"

---
> [auto-consumed] 2026-06-21 by Hermes cron — 任务已验证完成（协作规则已部署、pre-action-check 已创建），归档处理。
