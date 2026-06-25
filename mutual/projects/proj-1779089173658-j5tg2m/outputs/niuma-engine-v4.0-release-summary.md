# niuma-engine v4.0 发布总结

## 核心变化：v1.0 → v4.0

| 维度 | v1.0 (5月26日) | v4.0 (6月22日) |
|------|---------------|---------------|
| 规则数量 | 10 条 | 29 条 |
| 代码量 | ~20KB | ~124KB |
| 核心理念 | 单体AI工程师纪律 | 多Agent协作生态纪律 |
| 规则分发 | **未分发** (.gitignore 排除了 .claude/) | **已分发** (.claude/* + !.claude/rules/) |

## 新增规则（19条，按类别）

### Agent 管理三件套
- agent-concurrency-fallback.md -- 并发降级协议（429限流→零等待切换）
- agent-prompt-ironclad.md -- Agent Prompt 三要素铁律
- subagent-strategy.md -- Sub-Agent 策略（模型选择+故障恢复）

### 搜索与信息纪律
- search-decision-tree.md -- 搜索决策树+深度分级
- lesson-auto-update.md -- 教训闭环自动更新

### Skill 生态治理（4条）
- skill-auto-activation.md v2.0 -- 三层路由+联动链+自我学习
- skill-route-enforcement.md -- 创建必注册路由
- skill-execution-discipline.md -- 执行协议不可跳过
- skill-logging-enforcement.md -- 调用日志强制记录

### 安全与运维（5条）
- chinese-path-safety.md -- Windows中文路径铁律
- powershell-safety.md -- PowerShell安全规则
- pre-action-check.md -- 动手前检查门禁
- git-recovery.md -- 删前commit+30秒恢复
- mcp-config-protocol.md -- MCP配置四铁律

### 架构与治理（5条）
- competition-workspace-architecture.md -- 竞赛项目工作区架构
- dual-write-protocol.md -- 双写协议
- no-root-rules-dir.md -- 防回退规则
- _MIGRATED-TO-RULES.md -- 迁移说明

## 移除规则（3条，太个人化）
- identity-consistency.md -- 太泛泛
- preference-memory.md -- 信息密度不足
- voice-dna-auto-inject.md -- 个人文风

## 隐私清理
- 全局路径脱敏（`{workspace}/`、`{user-home}/`、`{newmax-home}/`等）
- 名称移除（"小黎团队"→"工程实践"，"小黎的5个工作区"→"5个真实工作区"）
- 零个人信息残留（最终扫描确认）

## 结构性修复
- .gitignore：`.claude/` → `.claude/*` + `!.claude/rules/`
- README 法则编号："法则6 边界声明" → "边界声明（独立规则）"

## 推送命令（需手动执行）
```bash
cd C:\Users\13975\AppData\Local\Temp\niuma-engine
git push origin main --tags
```
