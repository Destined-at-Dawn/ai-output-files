# AGENT.md — Agent 团队规范手册

> **用途**：Agent 的行为规范入口，每次任务开始时读取并遵循
> **适用范围**：日常学习工作区的所有 Agent（Claude Code、定时任务等）
> **版本**: v1.0 | **创建日期**: 2026-06-10

---

## 工作区定位

**日常学习** = 快速解题 + 学习方法 + 日常学习记录

| 场景 | 优先级 | 参考文件 |
|------|--------|---------|
| 物理/电路/电磁学题目 | 最高 | `SOPs/物理电路解题格式SOP.md` |
| 学习方法/策略 | 高 | `SOPs/SOP总索引.md` |
| 概念分析/知识解析 | 中 | 道理先行 → 例题演示 → 易错点警示 |

---

## Git Workflow

### Branch Naming

- Use `agent/<task-id>-<description>` for all agent-initiated branches
- Never commit directly to `main` or `develop`
- Example: `agent/daily-study-physics-sop-update`

### Commit Guidelines

#### Conventional Commits
Follow Conventional Commits: https://www.conventionalcommits.org

**Format**:
```
<type>(<scope>): <summary>

<正文：描述本次变更的背景与动机>

Agent-Task: <原始任务描述或任务 ID>
Agent-Model: <使用的模型>
Agent-Decision: <关键设计决策及理由>
Agent-Limitation: <已知局限或后续 TODO>
```

**Types**:
- `feat`: 新功能/新内容
- `fix`: 修复问题
- `chore`: 杂务（清理、移动文件等）
- `docs`: 文档更新
- `memory`: 记忆文件更新
- `sop`: SOP 新增/修改
- `config`: 配置变更
- `refactor`: 重构
- `test`: 测试相关

#### Atomic Commits

Each commit must represent exactly one logical change:
- Each commit must leave the codebase in a buildable, testable state
- Do not mix refactoring with feature changes in the same commit
- Do not mix changes to multiple unrelated modules in the same commit

#### Checkpoint Commits

For tasks expected to take more than 15 minutes:
- Commit after completing each major logical unit
- Use `[WIP]` prefix in message
- Clean up history with interactive rebase before opening PR

**Example**:
```
[WIP] feat(scope): partial implementation - completed model definition

Agent-Task: <task-id>
Agent-Progress: 1/4 checkpoints
```

### PR Process

- Open PR against `main` using the agent PR template
- Ensure all CI checks pass before requesting review
- Do not merge your own PRs
- Wait for at least one human approval

### What NOT to Commit

- API keys, tokens, passwords (use environment variables)
- Build artifacts, `node_modules`, `__pycache__`
- Local config files (`.env`, `*.local`)
- Large binary files (use Git LFS if necessary)
- Agent session logs (`.agent-logs/`)

### Worktree Usage

When working on complex tasks or when multiple agents run concurrently:
- Use `git worktree` to isolate work directories
- Each agent gets an independent worktree
- Clean up worktrees after task completion

**Claude Code**: Use `EnterWorktree` / `ExitWorktree` tools for automatic isolation

### History Cleanup

Before opening a PR:
```bash
# View commits
git log --oneline main..HEAD

# Interactive rebase to clean up
git rebase -i main

# Squash WIP commits, keep meaningful ones
# Ensure each commit follows Conventional Commits + Agent Trailer
```

### Auto Commit Scripts

Located in `scripts/` directory:

| Script | Purpose | Platform |
|--------|---------|----------|
| `agent-commit.sh` | Basic auto commit (manual params) | Linux/Mac/Git Bash |
| `agent-commit.ps1` | Basic auto commit (Windows) | Windows PowerShell |
| `smart-commit.sh` | Smart auto commit (auto-detect type) | Linux/Mac/Git Bash |

**Usage**:
```bash
# Smart commit (recommended)
./scripts/smart-commit.sh "Update memory files"

# With environment variables
AGENT_TASK_ID="proj-123" ./scripts/smart-commit.sh "Update memory files"
```

**Auto-detection logic**:
- `memory/` → type: memory
- `SOPs/` → type: sop
- `*.md` → type: docs
- `*.json` → type: config
- `*.sh` → type: feat

See `scripts/README.md` for full documentation.

---

## Think Before Act

每个非平凡任务前，必须先判断"这是已知路径还是新问题"。

**决策门**：
1. 能引用出具体范式 → 已知路径，按 SOP 执行
2. 只能模糊感觉"应该这样做" → 新问题，必须先研究
3. 从来没见过这类问题 → 高度新问题，加大研究力度

**日常学习特化**：
- 物理/电路题目 → 必须按 SOP-01 八步格式（已知路径）
- 学习方法讨论 → 先查 SOPs/ 总索引，看是否有现成框架

---

## No Blind Overwrite

**任何写操作施加到已存在的文件上之前，必须先读取该文件当前内容。**

流程：
1. Read 文件当前内容
2. 确认：新内容 = 旧内容 + 新增部分（而非只有新增部分）
3. 写入

能用 Edit 精确替换的，绝不用 Write 全文覆写。

---

## 记录即记忆

重要决策和经验必须写入 memory 文件：
- `memory/long-term.md` — 持久知识、用户偏好（只读，由 longmemory skill 归档）
- `memory/{YYYY-MM-DD}.md` — 每日任务进展（对话中随写随记）

**日常学习特化**：
- 解题经验 → 写入 `self-evolution/lessons.md`
- 有效方法 → 保存到 `self-evolution/做得好的鼓励/`
- 失败模式 → 保存到 `self-evolution/做得差的避免/`

---

## 信息密度

- 结论先行 → 原因分析 → 引用来源（Source: path#line）
- 高信息密度，避免水词，移动端友好（用列表不用表格）
- 需要深层解释时，保持简洁

**日常学习特化**：
- 解题过程必须按 SOP-01 八步格式输出
- 概念解释必须有认知科学支撑（引用百大认知书籍）

---

## 迭代日志

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-06-10 | v1.0 | 初版，基于个人工作区 AGENT.md + 日常学习特化 |

---

## 认知科学支撑：Agent规范的认知科学（百大认知书籍）

| 认知机制 | 来源 | 在AGENT.md中的应用 |
|---------|------|----------------------|
| **分布式认知** | 008-协同智能 §概念1 | AGENT.md=Agent团队的"共享心智模型"——所有Agent共用同一份行为规范→行为一致性>90%。没有AGENT.md=各做各的→混乱 |
| **原子化认知** | 025-认知负荷理论 §概念3 | atomic commit=认知原子——每个commit只含一个逻辑变更→理解成本最小→排查bug最快。混合commit=认知分子→理解难度×N |
| **外部化工作记忆** | 025-认知负荷理论 §概念1 | commit message中的Agent-Task trailer=工作记忆的外部化——"我为什么做这个"被固化在git history中→日后不需要回忆→直接读 |
| **预承诺策略** | 051-WOOP §概念1 | "禁止commit到main"=预承诺——在Agent产生"直接push到main"的冲动之前，先用分支规则"绑住手"→决策时的冷静>行动时的冲动 |
| **隔离-整合节律** | 012-心流 §概念1 | worktree隔离+PR整合=隔离-整合的工作节律——隔离=深度工作(心流)不被打扰；整合=知识共享+质量审查。交替进行=效率最大化 |
| **习惯回路** | 016-习惯的力量 §概念1 | Think Before Act+No Blind Overwrite=习惯回路的触发器——信号(收到任务)→例行(先判断+先读文件)→奖励(不犯错)。三要素齐全=习惯固化 |
| **检索式练习** | 027-认知天性 §概念1 | SOP-01八步格式=检索式练习的结构化框架——先尝试自己解（检索），再看答案（反馈），最后总结规律（间隔重复）|
| **元认知监控** | 023-认知觉醒 §概念1 | Think Before Act=元认知监控的实践——在行动前先监控自己的认知状态："我真的知道怎么做吗？还是在假装知道？"|
