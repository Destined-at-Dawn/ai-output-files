# Context Essentials（Compaction 后自动注入）

> SessionStart(compact) hook 在每次压缩后将本文件指针注入上下文。
> 本文件自身由 CLAUDE.md 保证 compaction 后重新加载（root CLAUDE.md 自动重载）。
> < 50 行铁律 + 恢复路径。

## 铁律
- **No Blind Overwrite**：写已存在文件前必须先 Read
- **防回退**：禁止创建根目录 rules/，规则只在 .claude/rules/
- **PowerShell 安全**：禁止 inline `$_`，必须用 .ps1 文件
- **记忆候选**：写 memory/ 前走 mcp__ask-user__ask_user 确认
- **做了才说**：工具返回成功才能说"已做"
- **验了才断**：断言前必须验证

## 快速恢复
1. `.claude/session-checkpoint.md` → PreCompact hook 自动写入的检查点
2. `memory/long-term.md` → 长期记忆
3. `memory/{today}.md` → 今日记忆
4. `project.md` → 项目状态

## 压缩后注意力
- CLAUDE.md 启动序列 Step 0-6 会自动重新执行
- skill descriptions 不会重载（已加载的 skill body 保留，上限 5K/skill）
- path-scoped rules 需要再次读取对应文件才会加载
