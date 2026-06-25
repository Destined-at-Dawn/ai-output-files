# 进化修改日志（永久追加，不删除）

> 记录每次进化任务的执行详情，用于追溯和审计。

---

## 2025-06-05 工作区初始化

- **操作**：从零搭建「日常学习」工作区基础设施
- **触发**：用户指出"也没有建立对应的SOP也没有建立对应的文件夹，也没有建立对应的自我进化文件，你就在敷衍我"
- **创建文件**：
  - CLAUDE.md（工作区规则，含物理电路解题格式嵌入）
  - SOPs/物理电路解题格式SOP.md（SOP-01，八步格式规范）
  - SOPs/SOP总索引.md
  - self-evolution/evolution-log.md（本文件）
  - self-evolution/evolution-calendar.md
  - self-evolution/lessons.md
  - self-evolution/patterns.md
  - self-evolution/做得好的鼓励/
  - self-evolution/做得差的避免/
  - memory/long-term.md
  - memory/MEMORY.md
  - 归档/
  - outputs/
- **教训**：用户提出规则时，不能只写 memory 就完事。必须同步建 SOP + 目录结构 + 自我进化文件。"记录 ≠ 建设"。
- **升级**：教训004 写入 lessons.md + 追加到 SOP-01 迭代日志

---

## 2026-06-10 并发 Agent 429 降级规则建设

- **操作**：建立跨工作区 Agent 并发降级协议
- **触发**：工作区全量扫描任务中，连续 2 次并发 Agent 调用触发 429 限流，浪费 2 整轮对话。用户要求"彻底解决，不准问问题"
- **创建文件**：
  - 知识中枢/02-共享规则/19-agent-concurrency-fallback.md（R19 共享规则）
  - lessons.md 教训005
  - evolution-log.md（本条记录）
  - evolution-calendar.md 更新
  - memory/2026-06-10.md 每日记忆
- **教训**：并发是锦上添花，不是必需品。429 = 并发能力被收回 → 立即切顺序执行。等待重试 = 用错误策略反复撞墙。
- **升级**：教训005 直接升级为共享规则 R19（首次出现即跳过"第1次只记录"，因为同日连续 2 次 = 已满足升级条件）
- **认知科学**：沉没成本谬误 + 计划谬误 + 工具定律（马斯洛）
