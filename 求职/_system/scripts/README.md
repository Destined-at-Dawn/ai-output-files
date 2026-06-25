# Agent Commit 脚本

## 脚本列表

| 脚本 | 用途 | 平台 |
|------|------|------|
| `agent-commit.sh` | 基础自动提交（需指定参数） | Linux/Mac/Git Bash |
| `agent-commit.ps1` | 基础自动提交（Windows 版） | Windows PowerShell |
| `smart-commit.sh` | 智能自动提交（自动检测变更类型） | Linux/Mac/Git Bash |

## 使用方法

### 1. 基础提交（agent-commit.sh）

```bash
# 基本用法
./scripts/agent-commit.sh feat memory "Add daily summary"

# 带环境变量
AGENT_TASK_ID="proj-123" AGENT_MODEL="claude-3.5" \
  ./scripts/agent-commit.sh feat memory "Add daily summary"
```

### 2. 智能提交（smart-commit.sh）

```bash
# 自动检测变更类型和范围
./scripts/smart-commit.sh "Update memory files"

# 带任务信息
AGENT_TASK_ID="proj-123" AGENT_MODEL="claude-3.5" \
  ./scripts/smart-commit.sh "Update memory files"
```

### 3. Windows 版本（agent-commit.ps1）

```powershell
# 基本用法
.\scripts\agent-commit.ps1 -Type feat -Scope memory -Summary "Add daily summary"

# 带参数
.\scripts\agent-commit.ps1 -Type feat -Scope memory -Summary "Add daily summary" `
  -TaskId "proj-123" -Model "claude-3.5"
```

## 自动检测逻辑（smart-commit.sh）

### Commit Type 检测

| 文件路径模式 | Commit Type |
|-------------|-------------|
| `memory/` | memory |
| `SOPs/` | sop |
| `*.md`, `*.txt` | docs |
| `*.json`, `*.yaml` | config |
| `*.sh`, `*.ps1`, `*.py` | feat |
| 其他 | chore |

### Scope 检测

| 文件路径模式 | Scope |
|-------------|-------|
| `projects/{id}/` | {project-id} |
| `.shared/` | shared |
| 根目录 `*.md`, `*.json` | root |
| 其他 | auto |

## Agent Trailer 格式

所有脚本都遵循以下 commit message 格式：

```
<type>(<scope>): <summary>

Agent-Task: <任务 ID>
Agent-Model: <使用的模型>
Agent-Decision: <关键设计决策>
Agent-Limitation: <已知局限>
```

## 在定时任务中使用

在定时任务的 prompt 中，可以这样调用：

```bash
# 先执行任务，然后提交
cd /path/to/workspace
./scripts/smart-commit.sh "Scheduled task: daily summary"
```

## 注意事项

1. **脚本会提交所有更改** - 使用前请确认没有不需要提交的文件
2. **Agent Trailer 是必需的** - 所有 commit 都必须包含 Agent 元数据
3. **分支规范** - Agent 应在 `agent/<task-id>-<description>` 分支上工作
