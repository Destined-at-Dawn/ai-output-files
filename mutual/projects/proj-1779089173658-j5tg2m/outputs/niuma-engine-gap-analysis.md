# niuma-engine v4.0 缺陷全量分析

## P0 致命缺陷（用户克隆后 AI 无入口）

| # | 缺陷 | 后果 |
|---|------|------|
| 1 | 仓库根目录 **无 CLAUDE.md** | 用户克隆后 AI 无入口文件，agent-install.md 写的"Read the CLAUDE.md"是死指令 |
| 2 | .gitignore 原版排除了 CLAUDE.md | 修复了规则目录但 CLAUDE.md 仍被排除 |
| 3 | README 第88行"法则 10 + 身份一致性" | 引用已删除的 identity-consistency.md |

## P1 高危缺陷

| # | 缺陷 | 后果 |
|---|------|------|
| 4 | adapters/ 只引用 5 条规则 | 用户按 adapter 配置后只有 5 条规则生效，其余 24 条浪费 |
| 5 | docs/compatibility.md 说"10 engineering laws" | 与实际 29 条规则不符 |
| 6 | docs/agent-install.md "Copy CLAUDE.md" | 文件不存在 |
| 7 | 进化日志含"文风DNA自动注入"条目 | 该规则已删除但日志声称 v4.0 包含 |

## P2 体验缺陷

| # | 缺陷 | 后果 |
|---|------|------|
| 8 | 无 evolution-calendar 轻量版 | 用户不知如何持续更新规则 |
| 9 | 无 skill-routing-table.json 示例 | 用户不知道技能路由概念 |
| 10 | templates/ 内容过时 | MEMORY.md 模板是 v1.0 格式 |
| 11 | "10条工程法则"措辞 vs 29条规则 | 框架描述不清——10条核心法则+19条专项规则 |

## 修复方案

### P0: 创建 CLAUDE.md + 修复 README 死引用
- 从 mutual CLAUDE.md 提取通用骨架，去个人化 → 仓库 CLAUDE.md
- README 第88行改"法则 10 + 纪律框架"——不引具体文件名
- 移除进化日志中 voice-dna 条目

### P1: 更新适配器 + 安装文档
- 每个 adapter 改为引用完整的 .claude/rules/ 目录
- agent-install.md 改为优先自动安装（AI 自己读 .claude/rules/）
- compatibility.md 更新规则数量

### P2: 轻量化机制
- 添加 EVOLUTION.md 简单版本
- 添加 skill-routing-table.example.json
- 更新 MEMORY.md 模板
