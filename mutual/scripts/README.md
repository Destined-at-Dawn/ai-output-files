# Agent Git Scripts

自动化 Agent Git 工作流的脚本集合。

## 脚本列表

### agent-commit.sh

Agent-Aware Git 提交脚本，严格遵循 AGENT.md 规范。

```bash
# 基础用法
./scripts/agent-commit.sh <type> <scope> <summary>

# 完整用法（带 Agent 元数据）
./scripts/agent-commit.sh feat auth "add login endpoint" "proj-123-auth" "use JWT for stateless auth"
```

**支持的 commit type**：
- `feat` - 新功能
- `fix` - Bug 修复
- `refactor` - 重构
- `docs` - 文档更新
- `sop` - SOP 更新
- `memory` - 记忆文件更新
- `config` - 配置更新
- `chore` - 杂项（脚本等）
- `test` - 测试
- `style` - 代码风格
- `perf` - 性能优化

**自动添加的 Agent Trailer**：
```
Agent-Task: <task-id>
Agent-Model: <model-name>
Agent-Decision: <decision-description>
Agent-Limitation: <known-limitations>
```

### smart-commit.sh

智能自动提交脚本，根据文件变更自动检测 commit type 和 scope。

```bash
# 基础用法
./scripts/smart-commit.sh

# 带 Agent 信息
./scripts/smart-commit.sh "proj-123-memory-fix" "use read-modify-write pattern"
```

**自动检测规则**：
| 文件路径模式 | Commit Type | Scope |
|------------|-------------|-------|
| `memory/*` | memory | memory |
| `*SOP*`, `*sop*` | sop | sop |
| `*.md`, `README`, `CHANGELOG` | docs | docs |
| `*.json`, `*.yaml`, `config*` | config | config |
| `test/*`, `*spec*` | test | test |
| `scripts/*`, `*.sh` | chore | scripts |

**环境变量**：
- `AGENT_MODEL` - Agent 模型名称（默认：claude-3.5-sonnet）

## 工作流示例

### 场景 1：日常记忆更新

```bash
# 1. 编辑记忆文件
vim memory/2026-05-22.md

# 2. 智能提交
./scripts/smart-commit.sh "daily-memory-update" "record today's learnings"
```

### 场景 2：SOP 迭代

```bash
# 1. 更新 SOP
vim SOPs/02_文章采集与分析SOP.md

# 2. 显式提交
./scripts/agent-commit.sh sop article-sop "add browser_use extraction method" "proj-xxx" "add step-by-step browser workflow"
```

### 场景 3：长任务（Checkpoint Commit）

```bash
# 1. 开始任务
git checkout -b agent/proj-123-feature

# 2. 第一个检查点
./scripts/agent-commit.sh feat core "implement basic structure" "proj-123" "initial implementation"
git push origin agent/proj-123-feature

# 3. 继续工作...
./scripts/agent-commit.sh feat core "add validation" "proj-123" "add input validation"

# 4. 完成后创建 PR
gh pr create --title "feat: implement feature" --body "..."
```

## 与 AGENT.md 的关系

这些脚本是 AGENT.md 规范的自动化实现：
- **Atomic Commit** - 每次提交一个语义化变更
- **Conventional Commits** - 遵循 type(scope): summary 格式
- **Agent Trailer** - 自动添加 Agent 元数据
- **Checkpoint Commit** - 支持长任务分段提交

## 注意事项

1. **分支保护**：pre-push hook 会阻止直接推送到 main（除非是 [WIP] commit）
2. **WIP 例外**：commit message 包含 "WIP" 时允许推送到 main（用于检查点）
3. **Agent Model**：可通过 `AGENT_MODEL` 环境变量自定义
4. **交互确认**：在 main 分支提交时会要求确认

## 安装

```bash
# 确保脚本可执行
chmod +x scripts/*.sh

# 配置 Git hooks
git config core.hooksPath .githooks
```

## 参考

- [AGENT.md](../AGENT.md) - Agent 工作流规范
- [outputs/sop-git-workflow.md](../outputs/sop-git-workflow.md) - Git 工作流 SOP
- [AI Agent Git 最佳实践](https://mp.weixin.qq.com/s/70hz6sYNwxErRkP7dkY8-Q)
