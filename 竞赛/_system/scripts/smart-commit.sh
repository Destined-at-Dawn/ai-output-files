#!/bin/bash
# smart-commit.sh - 智能自动提交脚本（自动检测变更类型）
#
# 用法：
#   ./scripts/smart-commit.sh [summary]
#
# 功能：
#   1. 自动检测变更类型（根据文件路径和内容）
#   2. 自动生成 scope
#   3. 按 Agent Trailer 格式提交

set -e

SUMMARY="${1:-Auto commit by agent}"

# 检查是否有更改
if git diff --quiet && git diff --cached --quiet; then
    echo "No changes to commit."
    exit 0
fi

# 获取变更文件列表
CHANGED_FILES=$(git diff --name-only)
STAGED_FILES=$(git diff --cached --name-only)
ALL_FILES="$CHANGED_FILES $STAGED_FILES"

# 自动检测 commit type
detect_type() {
    local files="$1"

    # 检查是否是 memory 文件
    if echo "$files" | grep -q "memory/"; then
        echo "memory"
        return
    fi

    # 检查是否是 SOP 文件
    if echo "$files" | grep -q "SOPs/"; then
        echo "sop"
        return
    fi

    # 检查是否是文档文件
    if echo "$files" | grep -qE "\.(md|txt|doc)$"; then
        echo "docs"
        return
    fi

    # 检查是否是配置文件
    if echo "$files" | grep -qE "\.(json|yaml|yml|toml|ini)$"; then
        echo "config"
        return
    fi

    # 检查是否是脚本文件
    if echo "$files" | grep -qE "\.(sh|ps1|py|js)$"; then
        echo "feat"
        return
    fi

    # 默认
    echo "chore"
}

# 自动检测 scope
detect_scope() {
    local files="$1"

    # 检查是否是项目文件
    if echo "$files" | grep -q "projects/"; then
        # 提取项目 ID
        local project_id=$(echo "$files" | grep -oP "projects/[^/]+" | head -1 | sed 's/projects\///')
        echo "$project_id"
        return
    fi

    # 检查是否是共享文件
    if echo "$files" | grep -q ".shared/"; then
        echo "shared"
        return
    fi

    # 检查是否是根目录文件
    if echo "$files" | grep -qE "^[^/]+\.(md|json)$"; then
        echo "root"
        return
    fi

    # 默认
    echo "auto"
}

# 检测类型和范围
COMMIT_TYPE=$(detect_type "$ALL_FILES")
SCOPE=$(detect_scope "$ALL_FILES")

# Agent 信息
AGENT_TASK_ID="${AGENT_TASK_ID:-scheduled-task}"
AGENT_MODEL="${AGENT_MODEL:-claude-code}"
AGENT_DECISION="${AGENT_DECISION:-Auto-detected commit type: $COMMIT_TYPE}"
AGENT_LIMITATION="${AGENT_LIMITATION:-None}"

# 生成 commit message
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
echo "   Type: $COMMIT_TYPE"
echo "   Scope: $SCOPE"
