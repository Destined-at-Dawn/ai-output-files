# Hermes 记忆存储

> 此目录是 Hermes（记忆中枢）的专属写入区域。
> 其他工具只读不写。

## 目录结构

```
hermes-memory/
├── facts/
│   └── atomic-facts.md          # 原子事实库（核心）
├── contradictions/
│   └── contradiction-log.md     # 矛盾检测日志
├── state-tracking/
│   ├── cross-tool-state.md      # 跨工具状态追踪
│   └── workspace-scan-log.md    # 工作区扫描记录
└── archived/                    # 过期记忆归档
```

## 事实格式

```
[事实] {一条可独立验证的陈述} [来源: {path}#{line}] [置信度: 高/中/低] [时间: {YYYY-MM-DD}]
```

## 遗忘规则

- 超过 90 天 + [低置信] → 归档
- 超过 180 天所有记忆 → 评估
- 标记 `[失效条件: xxx]` 且条件满足 → 归档

---

> 创建：2026-06-11 | Hermes v1.0 初始化
