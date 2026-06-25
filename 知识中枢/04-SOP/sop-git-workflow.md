# Git 工作流 SOP

> 基于《AI Agent 时代的 Git 工作流最佳实践》升级，适配牛马AI多工作区生态

**版本**: v2.0
**升级日期**: 2026-05-18
**适用范围**: 所有工作区（创作/求职/竞赛/个人/mutual）
**核心原则**: 隔离 · 透明 · 自动化

---

## 1. 触发条件

以下场景必须执行本 SOP：
- Agent 开始执行任务前
- Agent 完成一个有意义的工作单元后
- Agent 完成长任务的每个关键节点（Checkpoint）
- 切换工作区前
- 结束一天工作前
- Agent 定时任务产出新文件后

---

## 2. 分支策略

### 2.1 分支命名规范

**强制规则**：Agent 不得直接推送到 `main` 或 `master` 分支。

```
# Agent 分支命名
agent/<task-id>-<brief-description>

# 示例
agent/PROJ-234-update-git-sop
agent/PROJ-301-optimize-memory-system
```

### 2.2 分支保护规则

在 GitHub/GitLab 配置：
- ✅ Require pull request before merging
- ✅ Require approvals: 1（至少一个人工审查）
- ✅ Dismiss stale pull request approvals when new commits are pushed
- ✅ Require status checks to pass before merging
- ✅ Restrict who can push to matching branches

---

## 3. Commit 规范

### 3.1 Agent-Aware Commit Message

**格式**（Conventional Commits + Agent Trailer）：

```
<type>(<scope>): <summary>

<正文：描述本次变更的背景与动机>

Agent-Task: <原始任务描述或任务 ID>
Agent-Model: <使用的模型，如 claude-3.5-sonnet、gpt-4o>
Agent-Decision: <关键设计决策及理由>
Agent-Limitation: <已知局限或后续 TODO>
```

**示例**：

```
feat(git-sop): upgrade to v2.0 with agent best practices

Add Agent-Aware commit conventions, checkpoint commits,
and structured PR templates based on AI coding guide.

Agent-Task: proj-1779089173658 - Optimize Git workflow
Agent-Model: claude-3.5-sonnet
Agent-Decision: Use Git Trailer for agent metadata (built-in git mechanism)
Agent-Limitation: Stacked PR workflow requires manual branch management
```

### 3.2 Commit 类型

| 类型 | 用途 | 示例 |
|------|------|------|
| `feat` | 新功能/新内容 | 新增 SOP、新 skill |
| `fix` | 修复问题 | 修复路由断裂、修复 bug |
| `chore` | 杂务 | 清理文件、移动目录 |
| `docs` | 文档更新 | 更新 README、更新注释 |
| `memory` | 记忆文件更新 | 更新 long-term.md |
| `sop` | SOP 新增/修改 | 创建/优化 SOP |
| `config` | 配置变更 | 更新 CLAUDE.md、更新 skill-rules |
| `refactor` | 重构 | 代码重构、结构调整 |
| `test` | 测试相关 | 添加测试用例 |

### 3.3 Atomic Commit（原子提交）

**核心原则**：一个 commit 只表达一个可解释、可回滚、可验证的语义变化。

✅ **正确示范**：
```
feat(auth): add RefreshToken domain model
feat(auth): implement JWT refresh token issuance
feat(auth): expose POST /auth/refresh endpoint
test(auth): add unit tests for refresh token rotation
```

❌ **错误示范**：
```
feat(auth): implement refresh token（把所有改动混在一起）
```

**Agent 系统提示**：
```
When implementing a feature, break your work into atomic commits:
- Each commit must represent exactly one logical change
- Each commit must leave the codebase in a buildable, testable state
- Do not mix refactoring with feature changes in the same commit
- Do not mix changes to multiple unrelated modules in the same commit
```

### 3.4 Checkpoint Commit（检查点提交）

对于耗时较长的 agent 任务（>15 分钟），在关键节点进行检查点提交：

**指令示例**：
```
在完成以下关键节点时，执行一次 git commit：
1. 完成数据模型/接口定义
2. 完成核心逻辑实现
3. 完成测试编写
4. 完成文档更新
```

**Checkpoint Commit 格式**：
```
[WIP] feat(scope): partial implementation

Agent-Task: <task-id>
Agent-Progress: <当前完成进度，如 3/4 checkpoints>
```

**好处**：
- 任务中断时可以从最近的 checkpoint 恢复
- Checkpoint commit 天然成为 code review 的切分点
- 便于 `git bisect` 定位引入问题的具体阶段

### 3.5 按工作区分批提交

不要把所有工作区的变更混在一个 commit 里：
1. 先提交 `mutual/` 的变更（跨工作区配置）
2. 再逐个提交各工作区的变更
3. 最后提交清理类变更（删除旧文件等）

---

## 4. Git Worktree 隔离

### 4.1 为什么需要 Worktree

当多个 Agent 并行工作时，`git worktree` 是比多个 clone 更轻量的隔离手段：
- 每个 Agent 有独立的工作目录，不会相互干扰
- 共享同一个 `.git` 目录，分支管理统一
- 与 CI/CD 结合时，可以为每个 worktree 独立运行测试

### 4.2 Worktree 操作

```bash
# 为每个 agent 任务创建独立 worktree
git worktree add ../agent-task-234 -b agent/PROJ-234-update-sop
git worktree add ../agent-task-301 -b agent/PROJ-301-optimize-memory

# 查看当前所有 worktree
git worktree list

# 任务完成后清理
git worktree remove ../agent-task-234
```

### 4.3 在牛马AI中使用

牛马AI 的 Claude Code 已内置 `EnterWorktree` / `ExitWorktree` 工具：
- 当任务复杂或需要隔离时，自动使用 worktree
- 避免污染主工作区的 dirty worktree

---

## 5. Interactive Rebase 整理历史

### 5.1 何时整理

Agent 工作完成后，在合并前对 branch 历史进行整理：

```bash
# 查看当前 branch 的提交历史
git log --oneline main..HEAD

# 交互式 rebase 整理最近 N 个提交
git rebase -i main
```

### 5.2 整理策略

- 将 `[WIP]` checkpoint commits 合并（squash）为有意义的语义 commit
- 确保最终历史中每个 commit 都能独立理解和回滚
- 不要对已经推送到远程的分支做 force push（除非团队有明确约定）

### 5.3 让 Agent 辅助整理

**Prompt 示例**：
```
请帮我整理当前分支相对于 main 的提交历史，准备开 PR。

步骤：
1. 运行 git log --oneline main..HEAD 查看当前所有提交
2. 分析哪些提交属于同一个逻辑变更（尤其是 [WIP] 前缀的检查点提交）
3. 给我一份整理方案：哪些应该 squash、哪些保留、message 应该改成什么
4. 等我确认方案后，执行 git rebase -i main 完成整理
5. 整理完成后再次运行 git log --oneline main..HEAD 展示最终结果

要求：每个保留的 commit 需符合 Conventional Commits 格式，并包含 Agent-Task、Agent-Decision trailer。
```

---

## 6. 结构化 PR 模板

### 6.1 Agent PR 模板

创建 `.github/pull_request_template/agent.md`：

```markdown
## Task Description
<!-- 原始任务描述 -->

## What Changed
<!-- 核心变更摘要，聚焦「做了什么」而非「改了哪些文件」 -->

## Key Design Decisions
<!-- Agent 做出的关键设计决策及理由 -->
- Decision 1: ... because ...
- Decision 2: ... because ...

## Alternatives Considered
<!-- 考虑过但未采用的方案 -->

## Test Coverage
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed: <描述>

## Known Limitations / Follow-up Tasks
<!-- 当前实现的局限，后续需要跟进的工作 -->

## Review Guidance
<!-- 建议 reviewer 重点关注的部分 -->
```

---

## 7. AGENT.md（Agent 团队规范手册）

创建 `AGENT.md`，作为 Agent 的行为规范入口：

```markdown
# AGENT.md

## Git Workflow

### Branch Naming
- Use `agent/<task-id>-<description>` for all agent-initiated branches
- Never commit directly to `main` or `develop`

### Commit Guidelines
- Follow Conventional Commits: https://www.conventionalcommits.org
- Each commit must be atomic: one logical change, buildable and testable in isolation
- Include Agent-Task, Agent-Decision trailers in commit body

### PR Process
- Open PR against `main` using the agent PR template
- Ensure all CI checks pass before requesting review
- Do not merge your own PRs

### What NOT to Commit
- API keys, tokens, passwords (use environment variables)
- Build artifacts, `node_modules`, `__pycache__`
- Local config files (`.env`, `*.local`)
- Large binary files (use Git LFS if necessary)

### Checkpoint Commits
For tasks expected to take more than 15 minutes:
- Commit after completing each major logical unit
- Use `[WIP]` prefix in message
- Clean up history with interactive rebase before opening PR
```

---

## 8. 可追溯性链路

### 8.1 追溯链路设计

```
任务系统（project-tools）
    ↓ task-id
Git Branch / PR
    ↓ commit message 中的 Agent-Task trailer
Agent Session Log（可选：存储在 .agent-logs/ 目录，加入 .gitignore）
    ↓ 包含完整的 prompt 和 agent reasoning
代码变更
```

### 8.2 实践建议

- 在任务管理系统中为 agent 任务打标签（如 `ai-generated`）
- 对于高风险变更，在 PR 中附上关键的 agent 推理过程摘要
- 定期审计 `git log --grep="^Agent-Task:"` 的产出

---

## 9. 每日工作流

### 9.1 开始工作时

```bash
cd "${LEGACY_ROOT}"
git status          # 查看当前状态
git log --oneline -5  # 查看最近提交
```

### 9.2 Agent 执行任务时

```
1. 从 main 创建新分支：git checkout -b agent/<task-id>-<description>
2. 在关键节点执行 checkpoint commit
3. 每个 commit 包含 Agent-Task / Agent-Decision trailer
4. 完成后整理历史：git rebase -i main
5. 开 PR 并使用 Agent PR 模板
```

### 9.3 结束工作时（或定时任务前）

```bash
git status              # 检查是否有未提交的变更
# 如果有未提交变更，按逻辑分批提交
git push origin <branch>  # 推送到远程（如有）
```

---

## 10. 错误恢复

### 10.1 改崩了想回退

```bash
# 方案1：撤销工作区的修改（未提交的）
git checkout -- <文件名>

# 方案2：撤销最近一次提交（保留文件改动）
git reset --soft HEAD~1

# 方案3：完全回退到某个提交
git log --oneline    # 找到目标提交的 hash
git reset --hard <hash>
```

### 10.2 不确定改了什么

```bash
git diff              # 查看具体改动
git diff --stat       # 只看改动概览
```

---

## 11. .gitignore 规则

当前已排除：
- 媒体文件（jpg/png/mp4 等）
- 构建产物（Vivado/Quartus/Node.js）
- 数据库文件（*.db, *.db-shm, *.db-wal）
- 备份/归档目录
- 编辑器配置
- 大型文件（PDF/Office）
- Agent session logs（.agent-logs/）

**新增文件时的判断**：
- 如果是最终产出（文章、代码、配置）→ 提交
- 如果是临时文件/缓存 → 检查 .gitignore 是否已覆盖
- 如果是大型二进制文件 → 添加到 .gitignore

---

## 12. 远程仓库同步（GitHub）

### 仓库信息
- 仓库名：`niuma-ai-ecosystem`
- 远程地址：待配置
- 主分支：`main`
- 开发分支：按 agent 任务分支管理

### 推送流程
```bash
git push origin <branch>  # 推送当前分支
```

### 拉取更新
```bash
git pull origin main      # 拉取远程 main 更新
```

---

## 13. 检查清单

### Agent 执行任务前
- [ ] 从 main 创建新分支（`agent/<task-id>-<description>`）
- [ ] 确认 AGENT.md 已读取

### Agent 执行任务中
- [ ] 每完成一个关键节点执行 checkpoint commit
- [ ] Commit message 包含 Agent-Task / Agent-Decision trailer
- [ ] 每个 commit 是 atomic（一个逻辑变化）

### Agent 任务完成后
- [ ] 整理历史（rebase -i main，合并 WIP commits）
- [ ] 确认最终历史每个 commit 可独立理解和回滚
- [ ] 使用 Agent PR 模板开 PR
- [ ] 等待人工审查后合并

---

## 14. 关联文件

- `.gitignore`: `E:\ai产出文件\牛马\.gitignore`
- `AGENT.md`: `E:\ai产出文件\牛马\mutual\mutual\AGENT.md`（待创建）
- Agent PR 模板: `.github/pull_request_template/agent.md`（待创建）
- Git 备份归档: `E:\ai产出文件\牛马\归档\20260518_git_sop_backup\`
- 文章来源: [AI Agent 时代的 Git 工作流最佳实践](https://mp.weixin.qq.com/s/70hz6sYNwxErRkP7dkY8-Q)

---

## 15. 迭代日志

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-05-18 | v1.0 | 初版，基于《给AI编程小白的Git指南》 |
| 2026-05-18 | v2.0 | 重大升级：Agent-Aware Commit、Atomic Commit、Checkpoint Commit、Worktree 隔离、AGENT.md、PR 模板、可追溯性链路 |


---

## 认知科学支撑（百大认知书籍）

| 认知机制 | 来源 | 在Git工作流SOP中的应用 |
|---------|------|----------------------|
| **分布式认知** | 008-协同智能 §概念1 | Git=分布式认知的基础设施——多个Agent并行工作=多个认知节点。分支=认知隔离(不互相干扰)；PR=认知整合(合并时互相审查)；main=共享认知(最终真相源) |
| **时间旅行** | 018-算法之美 §概念1 | Git history=时间旅行的能力——任何时刻都可以"回到过去"查看"当时是怎么想的"。checkpoint commit=时间线上的"书签"→精确定位决策点 |
| **外部化记忆** | 025-认知负荷理论 §概念1 | commit message=工作记忆的外部化——Agent在commit时将"我为什么做这个"写入message→日后不需要"回忆"→直接读message→记忆永不失效 |
| **原子化原则** | 025-认知负荷理论 §概念3 | atomic commit=认知原子——每个commit只包含一个"逻辑变更"→认知负荷最小。混合commit=认知分子→理解难度×N→排查bug时必须"拆解" |
| **可追溯性** | 022-认知神经科学 §概念1 | Agent-Task trailer=可追溯性的工程化——从"代码变更"追溯到"Agent决策"追溯到"原始任务"。没有trailer=黑盒→出了问题不知道"谁做的、为什么" |
| **隔离-整合节律** | 012-心流 §概念1 | worktree隔离+PR整合=隔离-整合的工作节律——隔离阶段=深度工作(心流)→不被打扰；整合阶段=社交协调→知识共享。交替进行=效率最大化 |

---

## 🔗 相关链接
- [[sop-cross-workspace-modification]] · [[sop-skill-creation]] · [[sop-template]]
- 🟣 [[MASTER-路由中枢]]
