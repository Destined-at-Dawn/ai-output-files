# Sub-Agent 策略规则

> 来源：Claude Code 官方最佳实践 + 17 篇 Agentic AI 论文综述 + Spec Workflow
> 核心原则：先单后多，只在测量到显著性能差距时才扩展

---

## 何时用 Sub-Agent

### 必须用 Sub-Agent 的场景

| 场景 | 原因 | 典型用法 |
|------|------|----------|
| **调查/研究任务** | 独立上下文，不污染主对话 | 搜索代码、查找文件、分析日志 |
| **并行独立任务** | 多个无依赖任务可同时执行 | 多平台搜索、多文件验证 |
| **耗时 >5 分钟的任务** | 避免主对话阻塞 | 大型重构、批量操作 |
| **需要不同模型的任务** | 调查用 haiku，执行用 sonnet | 快速搜索 vs 深度分析 |

### 不用 Sub-Agent 的场景

| 场景 | 原因 |
|------|------|
| 简单查询（<1 分钟） | overhead > 收益 |
| 需要完整上下文的决策 | sub-agent 看不到主对话历史 |
| 用户交互密集的任务 | sub-agent 无法直接问用户 |

---

## Sub-Agent 配置策略

### 模型选择（参考 Felix Rieseberg）

- **haiku**：快速搜索、文件扫描、格式检查
- **sonnet**：范围明确的执行任务、代码生成、文件修改
- **opus**：需要理解意图的深度任务、架构决策、复杂分析

### 上下文隔离

- 每个 sub-agent 有独立上下文，看不到主对话
- 必须在 prompt 中包含足够的背景信息
- 结果返回主对话后，由主 agent 综合判断

### 层次化上下文管理（参考 Spec Workflow）

```
主 Agent（完整上下文）
  → 加载全部项目上下文
  → 分发选择性子集给 sub-agent
  → 收集结果并综合判断
```

好处：减少 60-80% token 使用（Spec Workflow 声称）

---

## 性能基准

### 单 Agent 起步原则（17 篇论文共识）

1. **始终从单个 agent 开始**
2. **只在能测量到显著性能差距（>45% of optimal）时才扩展**
3. **Reviewer agent 比直接 multi-agent 更有效**

### 扩展判据

```
if 单 agent 完成时间 > 预期的 2x:
    考虑 sub-agent
if 单 agent 质量不达标:
    先优化 prompt，再考虑 sub-agent
if 任务可拆分为正交子空间:
    用 sub-agent 并行
```

---

## 最佳实践

1. **Sub-agent 做调查，主 agent 做决策**
2. **每个 sub-agent 有明确的终止条件**
3. **结果必须可验证（不只是"看起来对"）**
4. **失败的 sub-agent 不应阻断主流程**
5. **记录 sub-agent 的 token 消耗到 metrics**

---

## 模型混合策略（v2.0 — 2026-06-09 新增）

> 场景：主会话使用 mimo（免费额度），但 mimo 不支持 multimodal（PDF/图片/文件读取）

### Agent 模型选择决策树

```
Agent 需要读 PDF/图片/文件？
  ├── 是 → 指定 model: "opus"（Claude Opus 4.7, 支持 multimodal）
  │       调用: Agent(description="...", prompt="...", model="opus")
  │
  └── 否 → 不指定 model，继承主会话模型（mimo，免费额度）
           调用: Agent(description="...", prompt="...")
```

### 具体场景对照

| 任务 | 推荐 Agent 类型 | 推荐模型 | 理由 |
|------|----------------|---------|------|
| 搜代码库找关键字 | Explore (quick) | 继承（mimo） | 纯文本 |
| 搜多个目录找文件 | Explore (medium/very thorough) | 继承（mimo） | 纯文本 |
| 读取 PDF 论文 | general-purpose | `opus` | 需要 multimodal |
| 读取图片/截图 | general-purpose | `opus` | 需要 multimodal |
| 多文件综合分析 | general-purpose | 继承（mimo）或 `opus` | 看是否需要读图片 |
| 代码审查 | code-reviewer | 继承（mimo） | 纯代码文本 |
| 写代码 | general-purpose | 继承（mimo） | 纯文本 |
| 架构设计 | Plan | `opus` | 需要深度理解 |

### 故障自动恢复

```
Agent 调用失败后：
  1. 判断失败类型：
     - multimodal 任务 + 未指定 model → 重试，指定 model: "opus"
     - 超时 → 缩小搜索范围，重试
     - 类型不匹配 → 换 Agent 类型，重试
     - 结果不可用 → 优化 prompt（补三要素），重试
  2. 同类故障 ≥ 2 次 → 记录到 memory/long-term.md
```

---

> 创建日期：2026-05-28
> v2.0 更新：2026-06-09（增加模型混合策略 + 故障自动恢复）
> 来源：Claude Code 官方 + 17 篇论文 + Spec Workflow + Felix Rieseberg
> 关联规则：agent-prompt-ironclad.md（Agent Prompt 三要素铁律）
