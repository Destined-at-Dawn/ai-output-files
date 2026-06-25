# Claude Fable 5 系统提示分析报告

> 来源：https://github.com/elder-plinius/CL4R1T4S/blob/main/ANTHROPIC/CLAUDE-FABLE-5.md
> 分析日期：2026-06-12
> 目的：提取可复用机制，改善我们的 CLAUDE.md / skills / 工作流

---

## 仓库概览

CL4R1T4S 仓库（28.4K stars, 5.3K forks）收集了 25+ 家 AI 公司的系统提示词。

**已保存文件**：
- `CLAUDE-FABLE-5.md`（1585 行，120KB）— Claude Fable 5 完整系统提示
- `Claude-Opus-4.7.txt` — Claude Opus 4.7 系统提示
- `Claude_Code_03-04-24.md` — Claude Code CLI 系统提示（51行，极简）
- `Claude-Design-Sys-Prompt.txt` — Claude 设计系统提示

**Claude Code 系统提示对比**：只有 51 行，极其简洁。这意味着我们 CLAUDE.md 中的 1000+ 行规则是**用户层扩展**，不是 Anthropic 官方的。官方只给了一句话：`CLAUDE.md will be automatically added to context`。

---

## 六大可复用机制

### 机制 1：Skills 前置于工具选择

**Fable 5 设计**：Skills 在 planning/reasoning 阶段就注入，模型先看到 Skill 描述（`Use when...`），决定用哪个 Skill，然后才选工具执行。

**我们的差距**：
- skill-routing-table.json 的触发词匹配是前置的 ✅
- 但 Skill 仅被当作"调用哪个"的路由决策，没有影响模型对任务的**理解方式**
- Fable 5 的 Skills 会告诉模型"这个任务的优先级是什么""用户要的是产出不是过程"

**改善方案**：
- 在每个 li-* SKILL.md 的 frontmatter 中增加 `priority_hint` 和 `user_goal` 字段
- 路由匹配后，不仅调用 Skill，还注入"用户真正想要什么"的上下文

### 机制 2：Skills 四原则（写入规则）

| 原则 | 含义 | 我们的行动 |
|------|------|-----------|
| 产出 > 格式 | 不向用户展示 Skill 名 | 已有，保持 |
| 少即是多 | 不用 Skill 就能搞定就不激活 | 审计 41 个 li-* skill，标记哪些可以合并 |
| 目标导向 | Skill 服务于用户目标 | 在 SKILL.md 中增加 `user_goal` 字段 |
| 不假设 | 扫一眼再决定，不预判 | 已在 skill-execution-discipline 中覆盖 |

**行动**：将这四原则写入 `.claude/rules/skill-auto-activation.md` 作为补充。

### 机制 3：持久存储的不可变数据规则

**Fable 5 设计**：
- 事实键（含 is/was/are）永远不可覆盖，只能追加新事实
- 时间键（如 `project.x.status`）是唯一可更新的
- 每个 artifact 一个 SQLite 数据库，最多 1000 键

**我们的差距**：memory/long-term.md 用纯 Markdown，没有结构化的不可变约束。

**改善方案**：
- 在 memory-candidate-protocol.md 中增加"事实不可变"规则
- 写入 long-term.md 的事实型记忆，不能被后续 Edit 覆盖，只能追加新版本
- 用 `[已更新]` 标记过时事实，不删除

### 机制 4：搜索重试机制

**Fable 5 设计**：
```
搜索失败 → 重新措辞查询 → 仍失败 → 告知用户
限制：最多 3 次搜索尝试，之后如实告知
```

**我们的差距**：没有显式的搜索重试规则。

**行动**：创建 `.claude/rules/search-retry-policy.md`，规定：
1. 第一次搜索失败 → 换关键词重试
2. 第二次仍失败 → 换搜索引擎/数据源
3. 第三次仍失败 → 告知用户"搜索未找到相关信息，建议手动查找"
4. 禁止无限重试

### 机制 5：文件创建确定性

**Fable 5 设计**：
- 路径必须运行时可验证
- 每次调用产出相同结构
- Python 脚本必须 shebang
- 禁止占位符内容

**我们的差距**：script-safety-check 覆盖安全性，但缺少"确定性验证"。

**行动**：在 script-safety-check.md 中增加确定性检查项：
- [ ] 文件路径是否可验证？
- [ ] 内容是否包含占位符？
- [ ] 每次执行是否产出一致？

### 机制 6：产出质量评分标准（9 级制）

**Fable 5 评分锚点**：
| 分数 | 锚点 |
|------|------|
| 9 | 改变我对这个主题的看法 |
| 8 | 学到了新东西 |
| 7 | 让我从不同角度思考 |
| 6 | 有帮助但没改变看法 |
| 5 | 有点用，但不够深 |
| 4 | 基本正确但表面 |
| 3 | 有缺陷 |
| 2 | 不准确 |
| 1 | 完全不正确或有害 |

**行动**：在 li-improve 的评分系统中采用这套锚点定义，替代原来的 1-10 分模糊标准。

---

## Claude Code 系统提示对比

Claude Code 的官方系统提示只有 **51 行**，内容极简：

| 维度 | 官方 Claude Code | 我们的 CLAUDE.md |
|------|-----------------|-----------------|
| 行数 | 51 行 | 1000+ 行 |
| 规则数 | ~10 条 | 50+ 条 |
| 记忆系统 | 只提 CLAUDE.md | 三层记忆 + 置信度 + 过期机制 |
| Skill 系统 | 无 | 41 个 li-* skill + 路由表 |
| 安全检查 | 2 条（拒绝恶意代码） | 6 个安全规则文件 |

**结论**：我们的 CLAUDE.md 是**重度用户扩展层**。官方给的是一个极简骨架，我们往里塞了一整套工程方法论。这个方向是对的——Claude Code 的设计就是让用户通过 CLAUDE.md 自定义行为。

**风险**：CLAUDE.md 越长，每次对话启动时注入的 context 越多，可能影响推理质量。建议定期审计，删除不再需要的规则。

---

## 建议的优先行动

### P0（立即）
1. 将 Skills 四原则写入 skill-auto-activation.md
2. 在 SKILL.md 中增加 `user_goal` 字段

### P1（本周）
3. 创建 search-retry-policy.md
4. 更新 li-improve 评分标准为 9 级制
5. 在 memory-candidate-protocol 中增加"事实不可变"规则

### P2（本月）
6. 审计 41 个 li-* skill，标记可合并/弃用候选
7. 定期审计 CLAUDE.md，删除过时规则
8. 对比其他已保存的系统提示（Opus 4.7 等）提取更多洞察

---

## 文件索引

| 文件 | 路径 | 内容 |
|------|------|------|
| Fable 5 完整提示 | outputs/system-prompts/ANTHROPIC/CLAUDE-FABLE-5.md | 1585 行，120KB |
| Opus 4.7 提示 | outputs/system-prompts/ANTHROPIC/Claude-Opus-4.7.txt | Claude Opus 4.7 |
| Claude Code 提示 | outputs/system-prompts/ANTHROPIC/Claude_Code_03-04-24.md | CLI 版，51 行 |
| Design System 提示 | outputs/system-prompts/ANTHROPIC/Claude-Design-Sys-Prompt.txt | 设计系统 |
| 本分析报告 | outputs/system-prompts-analysis.md | 本文件 |
