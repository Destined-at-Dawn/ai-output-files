# Skill 路由表

> 最后更新：2026-06-17
> 规则：每个 skill 由唯一工具负责，其他工具只读不写

## Hermes 记忆中枢负责的 Skills

| Skill | 用途 | 触发场景 |
|-------|------|----------|
| li-memory | 记忆引擎，四层架构 | 事实提取、矛盾检测、自动遗忘、记忆检索 |
| li-improve | 进化引擎，教训闭环 | 用户纠正、命令失败、会话结束自审 |
| li-sync | 跨工作区同步 | 一改全改、文档体检、收尾整理 |
| li-manage | 全局记忆管家 | 启动序列、对话后记录、上下文注入 |
| li-triage | 任务分流状态机 | issue/任务分级、待办整理 |
| li-skills-mgmt | Skill 生命周期管理 | 创建/审核/融合/弃用 skill |
| li-local-search | 本地 skill 搜索 | 搜索已安装的 230+ skills |
| li-intent | SOP 驱动意图引擎 | 用户意图识别、skill 链路由 |
| li-bestskill | 技能雷达 | 搜索外部最佳 skill 方案 |
| daily-review | 每日工作回顾 | 生成每日记忆摘要 |
| deep-review | 深度工作分析 | 长期记忆分析、项目洞察 |
| li-plan | 任务和项目规划 | 任务管理、里程碑追踪 |

## Newmax 负责的 Skills

| Skill | 用途 |
|-------|------|
| li-design | 设计 |
| li-visual | 视觉 |
| li-image | 图片生成 |
| baoyu-* | 小红书/微信/图片/信息图等 |
| li-xhs | 小红书 |
| li-wechat | 微信 |
| li-video | 视频 |
| li-storyboard | 分镜 |
| li-consultant | 咨询回复 |
| li-office | 文档生成 |

## Codex 负责的 Skills

| Skill | 用途 |
|-------|------|
| li-code | 编程规范 |
| li-debug | 调试 |
| li-embedded | 嵌入式 |
| li-hardware | 硬件 |

## 路由规则

1. **单一负责**：每个 skill 有且仅有一个工具负责
2. **只读共享**：其他工具可以读取，但不能修改
3. **冲突上报**：发现跨工具冲突时，上报给用户决定
4. **定期同步**：每月检查路由表是否需要更新

## 跨工具协作模式

```
用户请求 → Hermes 意图识别(li-intent) → 路由到对应工具
    ↓
Hermes 提供上下文（li-memory/li-manage）
    ↓
目标工具执行任务
    ↓
Hermes 记录结果（事实提取/li-improve）
```
