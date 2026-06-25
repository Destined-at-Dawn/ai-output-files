# 工作流效率仪表盘

> 自动生成于 daily-health-check.py
> 更新频率：每日会话启动时

## 📊 核心指标（5 维度）

### 1. Token 效率
- **目标**: 压缩节省率 ≥50%
- **当前**: 待首次测量
- **趋势**: —

### 2. 任务完成质量
- **目标**: 首次成功率 ≥80%
- **当前**: 待首次测量
- **趋势**: —

### 3. 自动化覆盖率
- **目标**: 自动处理率 ≥90%
- **当前**: 待首次测量
- **趋势**: —

### 4. 上下文健康度
- **目标**: 恢复成功率 ≥95%
- **当前**: 待首次测量
- **趋势**: —

### 5. 进化速度
- **目标**: 每周 ≥2 条新规则
- **当前**: 待首次测量
- **趋势**: —

## 🔧 Hook 状态

| Hook | 脚本 | 状态 |
|------|------|------|
| PreToolUse | pre-tool-use.py | ✅ 就绪 |
| PostToolUse | post-tool-use.py | ✅ 就绪 |
| PreCompact | pre-compact.py v2 | ✅ 就绪 |
| PostCompact | (echo) | ✅ 就绪 |
| SessionStart | on-compact.py v2 | ✅ 就绪 |
| Stop | stop-metrics.py | ✅ 就绪 |

## 📈 评估断言

- **总断言**: 10
- **通过**: 6
- **失败**: 0
- **未知**: 2
- **待测**: 2
- **通过率**: 75%

## 📁 文件清单

| 文件 | 类型 | 大小 | 用途 |
|------|------|------|------|
| .claude/hooks/pre-tool-use.py | Hook | 6KB | 安全守卫 |
| .claude/hooks/post-tool-use.py | Hook | 2KB | 文件验证 |
| .claude/hooks/stop-metrics.py | Hook | 5KB | 指标追踪 |
| .claude/hooks/pre-compact.py | Hook | 11KB | 九段式检查点 |
| .claude/hooks/on-compact.py | Hook | 5KB | 50K 重读恢复 |
| .claude/hooks/collect-metrics.py | 脚本 | 4KB | 指标采集 |
| .claude/hooks/daily-health-check.py | 脚本 | 4KB | 健康检查 |
| .claude/metrics-config.json | 配置 | 2KB | 指标配置 |
| .claude/settings.json | 配置 | 2KB | Hook 部署 |
| skills/auto-evolution/eval.json | 评估 | 3KB | 10 个断言 |
| skills/auto-evolution/ralph-loop-config.json | 配置 | 2KB | 自主循环 |
| .claude/rules/subagent-strategy.md | 规则 | 2KB | Sub-Agent 策略 |

## 🎯 下一步行动

1. [ ] 在实际长会话中验证所有 Hook
2. [ ] 观察量化指标首次采集
3. [ ] 将改进同步到其他 4 个工作区
4. [ ] 继续迭代优化

---
*最后更新: 2026-05-28*
