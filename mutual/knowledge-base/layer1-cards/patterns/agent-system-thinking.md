# Agent系统思维 vs 模型思维

> 来源: 12篇文章信息差总结-道法术器版 § 信息差1
> 日期: 2026-06-10
> 置信度: [高置信]
> 失效条件: Agent工程范式发生根本性变化

## 核心结论

Agent = 系统，不是模型。优化系统比换模型收益更大。

## 七层框架

| 层 | 说明 | 我们的实现 |
|----|------|-----------|
| 模型 | LLM选择 | Claude/Sonnet/Opus/Haiku |
| 上下文 | 信息注入 | CLAUDE.md + memory/ + knowledge-base/ |
| 工具 | 外部能力 | MCP tools + Bash/Read/Write/Edit |
| 编排 | 调度逻辑 | li-intent (Phase 0-4) + skill-routing-table |
| 安全 | 防护机制 | .claude/rules/ (script-safety-check等) |
| 评估 | 质量度量 | skill-usage-log.md (待加强) |
| 日志 | 追踪记录 | memory/{date}.md + session-checkpoint.md |

## 实践指导

1. **优化顺序**: 编排 > 上下文 > 工具 > 安全 > 评估 > 日志 > 模型
2. **诊断方法**: 系统出问题时，从最外层（编排）开始排查，不要先怀疑模型
3. **投资回报**: 编排优化（路由表、DAG链）的投资回报率最高

## 与我们工作流的关系

- CLAUDE.md = Harness层（上下文+安全+日志）
- skill-routing-table.json = 编排层
- skills/ = 工具层
- 优化重点应放在编排层（DAG路由、选择性激活）
