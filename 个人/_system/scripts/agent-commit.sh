#!/bin/bash
# agent-commit.sh - Agent 自动提交脚本（Agent Trailer 格式）
#
# 用法：
#   ./scripts/agent-commit.sh [commit-type] [scope] [summary]
#
# 示例：
#   ./scripts/agent-commit.sh feat memory "Add daily summary"
#   ./scripts/agent-commit.sh chore cleanup "Remove temp files"
#
# 环境变量（可选）：
#   AGENT_TASK_ID    - 任务 ID
#   AGENT_MODEL      - 使用的模型
#   AGENT_DECISION   - 关键设计决策
#   AGENT_LIMITATION - 已知局限

set -e

# 默认值
COMMIT_TYPE="${1:-chore}"
SCOPE="${2:-auto}"
SUMMARY="${3:-Auto commit by agent}"
AGENT_TASK_ID="${AGENT_TASK_ID:-scheduled-task}"
AGENT_MODEL="${AGENT_MODEL:-claude-code}"
AGENT_DECISION="${AGENT_DECISION:-Automated commit}"
AGENT_LIMITATION="${AGENT_LIMITATION:-None}"

# 检查是否有更改
if git diff --quiet && git diff --cached --quiet; then
    echo "No changes to commit."
    exit 0
fi

# 生成 commit message（Agent Trailer 格式）
COMMIT_MSG="${COMMIT_TYPE}(${SCOPE}): ${SUMMARY}

Agent-Task: ${AGENT_TASK_ID}
Agent-Model: ${AGENT_MODEL}
Agent-Decision: ${AGENT_DECISION}
Agent-Limitation: ${AGENT_LIMITATION}"

# 添加所有更改
git add -A

# 提交
git commit -m "$COMMIT_MSG"

echo "✅ Committed: ${COMMIT_TYPE}(${SCOPE}): ${SUMMARY}"
