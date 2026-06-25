# R12: Hermes Agent Integration Protocol

## 概述

Hermes Agent 是牛马AI 生态的补充智能体，负责自动化监控、长时任务和多平台消息投递。

## 角色分工

| 任务类型 | 执行者 | 原因 |
|----------|--------|------|
| 交互式编程/规划 | 牛马AI (Claude Code) | 需要实时反馈和审批 |
| AI 资讯监控 | Hermes Agent | 适合 cron 定时 + 自动摘要 |
| 内容初稿起草 | Hermes Agent | 长时任务，可后台运行 |
| 多平台消息推送 | Hermes Agent | 原生支持 Telegram/Discord/微信 |
| 跨工作区同步 | 牛马AI (Claude Code) | 复杂规则引擎 |
| 技能自学习 | Hermes Agent | 内置学习闭环 |

## 文件共享规则

1. **Hermes 配置目录**: `~/.hermes/` (config.yaml, SOUL.md, memories/, skills/, cron/)
2. **牛马AI 配置目录**: `~/.claude/telos/` + 各工作区 memory/
3. **共享工作区**: `${LEGACY_ROOT}/`

## 记忆同步协议

### 从牛马AI → Hermes
当 telos 文件更新时，手动或自动同步到 `~/.hermes/memories/USER.md` 和 `~/.hermes/SOUL.md`。

### 从 Hermes → 牛马AI
Hermes 的记忆文件（`~/.hermes/memories/MEMORY.md`）中的新发现，应定期提取到对应工作区的 `memory/MEMORY.md`。

## 冲突解决

- 两个系统不应同时编辑同一文件
- Hermes 的工作目录默认为 `${LEGACY_ROOT}/`
- 牛马AI 各工作区有独立的 CLAUDE.md 规则
- 冲突时以牛马AI 的 MASTER.md 规则为准

## 变更记录

| 日期 | 变更 | 来源 |
|------|------|------|
| 2026-05-11 | 初始化 R12：Hermes Agent 集成协议 | mutual 工作区 |
