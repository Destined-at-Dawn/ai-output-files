# Skill 执行纪律（最高优先级 — 防跳过机制）

> 每个 li- skill 的 SKILL.md 顶部有「执行协议」段，列出了必读的 references/ 文件。
> 本规则确保 AI 不会为了"效率"跳过这些协议。

---

## 铁律 1：调用 skill 时必须先读执行协议

**触发**：AI 通过 `mcp__skill-handler__Skill` 调用任何 li- skill。

**执行**：
1. skill-handler 会将 SKILL.md 内容注入上下文
2. AI 必须先找到 `## ⚡ 执行协议` 或 `## [LIGHTNING] 执行协议` 段
3. 识别其中的「必读」文件列表
4. **在执行任何 Phase 之前**，用 `Read` 工具读取所有必读 references/ 文件

**不可跳过**。没有"我已经知道内容了"的例外。没有"太长了不读"的例外。

---

## 铁律 2：必读文件 = 执行前置条件

**定义**：SKILL.md 执行协议中标注为「必读」的 references/ 文件，是该 skill 执行的**前置条件**。

**违反后果**：
- 不读必读文件就执行 Phase → 产出基于不完整的方法论 → 质量不可信
- 等同于工程师不看设计规范就开始写代码

**正确流程**：
```
调用 li-xhs
  → SKILL.md 注入，看到执行协议
  → 必读: references/xiaohongshu-rules.md
  → Read references/xiaohongshu-rules.md
  → 确认已读取
  → 开始执行 Phase 1
```

---

## 铁律 3：按需文件 = 场景匹配时强制读取

**定义**：SKILL.md 执行协议中标注为「按需」的 references/ 文件，在匹配对应场景时**必须读取**。

**判断标准**：
- 用户请求涉及该场景 → 读取对应文件
- 用户请求不涉及 → 不读（节省上下文）

**示例**：
- 调用 li-analyze，用户要写小红书内容 → 必须读 `references/content-creation.md`
- 调用 li-analyze，用户要做诊断 → 必须读 `references/content-diagnosis.md`

---

## 铁律 4：门禁不可绕过

SKILL.md 执行协议中的门禁检查：
- Phase 执行前确认已读取必读文件 → 未读 = 禁止继续
- 输出结论前确认有 Source: path#line → 无证据 = 禁止声称
- 跳过执行协议 = 违反工程法则 8（门禁不可跳过）

---

## 违规检测

以下信号说明执行协议被跳过了：
- [ ] 调用了 li- skill 但没有 Read 任何 references/ 文件
- [ ] 输出了结论但没有 Source 引用
- [ ] 用户问"你读了 xxx.md 吗"时答不上来
- [ ] 执行 Phase 1 前没有确认必读文件

---

## 为什么需要这个规则

**背景**：38 个 li- skill 的 SKILL.md 都已注入执行协议（2026-06-11）。但 SKILL.md 是**被动文档**——它告诉 AI 应该做什么，但不强制 AI 做。

**本规则**是**主动约束**——它在 .claude/rules/ 中，Claude Code 每次对话自动加载。当 AI 看到 SKILL.md 的执行协议时，本规则提醒它"这不是建议，是强制"。

**类比**：
- SKILL.md 的执行协议 = 安全操作手册（放在工位上）
- 本规则 = 安全检查员（站在旁边看着你操作）

---

> 创建日期：2026-06-11
> 来源：38 个 li- skill 执行协议注入 + 用户对防跳过机制的需求
> 关联：skill-auto-activation.md, skill-logging-enforcement.md
