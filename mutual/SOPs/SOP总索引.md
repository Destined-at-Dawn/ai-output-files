# mutual SOP 总索引

> 本工作区所有 SOP 的入口。R16 规范：SOP 只放根目录，项目目录不重复。

---

## SOP 路由

| 场景 | SOP 文件 | 说明 |
|------|---------|------|
| 文件操作 | `sop-file-operations.md` | 读写、归档、删除流程 |
| 会话生命周期 | `sop-session-lifecycle.md` | 会话启动→执行→结束流程 |
| 记忆管理 | `sop-memory-management.md` | 记忆读写、归档规则 |
| 仓库安全审计 | `security-audit.md` | API泄露/代理泄露/硬编码检查（参考 comemo） |
| 微信聊天分析 | `wechat-analysis.md` | 密钥提取→DB解密→聊天导出→社群过滤→心理蒸馏 |
| 生态监控 | `ecosystem-monitoring.md` | 工作区健康检查、规则一致性、记忆同步、产出质量 |
| 内容分析 | `sop-content-analysis.md` | 内容分析流程 |
| 内容创作 | `sop-content-creation.md` | 内容创作流程 |
| 调研 | `sop-research.md` | 调研流程 |
| 技能生命周期 | `sop-skill-lifecycle.md` | 技能创建、更新、弃用流程 |

## SOP 执行规则

1. SOP 只读根目录 `SOPs/`，不读项目目录的 SOP 副本
2. SOP 修改只在根目录进行
3. 项目特殊流程写在项目 `.claude/rules/` 中，标注"仅本项目适用"

---

> 创建日期：2026-05-25
> 来源：R16 根目录优先约束架构
