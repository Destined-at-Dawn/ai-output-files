# Context Essentials（Compaction 后自动注入）

> 压缩后 Claude Code 重新加载 CLAUDE.md 时，本文件提供最小铁律 + 恢复路径。
> < 30 行，确保即使上下文被大幅压缩，关键规则仍存活。

## 铁律
- **No Blind Overwrite**：写已存在文件前必须先 Read
- **做了才说**：工具返回成功才能说"已做"
- **验了才断**：断言前必须验证

## 快速恢复
1. `.claude/session-checkpoint.md` → PreCompact hook 自动写入的检查点
2. 项目根目录的 CLAUDE.md → 项目约束
3. 项目根目录的 project.md → 项目状态（如存在）

## 压缩后注意
- CLAUDE.md 会自动重新加载
- 压缩前修改的文件需要重新 Read 确认
- 如果任务中断，从 session-checkpoint.md 的「最新用户请求」恢复
