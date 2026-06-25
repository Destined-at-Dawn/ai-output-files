# 生态手册（Ecosystem Manual）

> 小黎的 AI 生态统一索引。每周日晚 22:00 自动刷新。
> 任何工作区的 AI 都可以读这个目录来了解小黎的完整工具链。

## 快速导航

| 文件 | 内容 | 更新频率 |
|------|------|----------|
| [skill-inventory.md](skill-inventory.md) | 160 个 Skill 完整清单（按类别，1639 触发词） | 每周 |
| [sop-index.md](sop-index.md) | 96 个 SOP 跨工作区索引 | 每周 |
| [mcp-tools.md](mcp-tools.md) | MCP 工具清单 + 状态 | 每周 |
| [work-groups.md](work-groups.md) | 微信群活跃度统计 Top 50 | 每周 |
| [distillations/self-voice-dna.md](distillations/self-voice-dna.md) | 小黎文风DNA（自动注入） | 每周 |
| [distillations/contacts/](distillations/contacts/) | 联系人蒸馏结果 | 增量 |

## 文风DNA自动注入规则

**写作时自动加载 `distillations/self-voice-dna.md`，除非是正式文体（论文/报告/PRD）。**

见 `.claude/rules/voice-dna-auto-inject.md`

## 定时刷新

- 频率：每周日 22:00
- 任务ID：见 `meta.json`
- 刷新内容：skill/SOP/MCP 索引 + 工作群统计 + 文风DNA增量更新

## 元数据

见 `meta.json`
