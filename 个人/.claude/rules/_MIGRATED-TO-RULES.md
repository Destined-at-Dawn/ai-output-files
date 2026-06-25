# ⛔ 规则唯一存放位置：.claude/rules/（禁止创建根目录 rules/）

> ⚠️ 本文件是**反向防御规则**——阻止 AI 在根目录重新创建 `rules/` 目录。

## 铁律
- **所有规则必须放在 `.claude/rules/`**（Claude Code 自动加载此目录）
- **严禁在根目录创建 `rules/` 目录**（它会被 Claude Code 忽略，是冗余副本）
- **如果你在代码或文档中看到路径 `rules/`（不含 `.claude/` 前缀），它一定是过时引用，必须修正**

## 为什么
- Claude Code 只自动加载 `.claude/rules/` 目录下的文件
- 根目录的 `rules/` 不会被自动加载，纯粹是磁盘垃圾
- 2026-05-25 已全量迁移至 `.claude/rules/`，根目录 `rules/` 已删除
- 任何引导创建根目录 `rules/` 的文本都是**需要修正的错误**

## 正确模式
```markdown
# ✅ 规则位置
.claude/rules/xxx.md

# ❌ 禁止位置（已废弃）
rules/xxx.md
根目录/rules/xxx.md
```

## 检测方法
如果你在执行任务时想创建 `rules/` 目录——STOP。
执行 `ls .claude/rules/` 确认规则已存在，永远不要创建根目录 `rules/`。

---

> 最后更新：2026-05-25（R16 根目录优先约束架构 v2）
> 旧版（v1，2026-05-25）曾错误引导创建 rules/，已修正。
