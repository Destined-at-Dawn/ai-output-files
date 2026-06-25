#!/bin/bash
# Smart Auto-Commit Script for AI Agent Workflows
# Automatically detects change type and creates appropriate commit
#
# Usage: ./smart-commit.sh [agent-task] [agent-decision]
#
# This script analyzes staged changes and determines:
# - Commit type (feat/fix/docs/sop/memory/config)
# - Scope (based on file paths)
# - Summary (based on file names and change patterns)

set -e

AGENT_TASK="${1:-auto-detect}"
AGENT_DECISION="${2:-smart commit auto-detection}"
AGENT_MODEL="${AGENT_MODEL:-claude-3.5-sonnet}"

# Get list of changed files
CHANGED_FILES=$(git diff --cached --name-only 2>/dev/null || git diff --name-only 2>/dev/null || echo "")

if [ -z "$CHANGED_FILES" ]; then
    echo "No changes detected. Stage files first: git add <files>"
    exit 0
fi

# Auto-detect commit type based on file patterns
detect_type() {
    local files="$1"

    # Memory files
    if echo "$files" | grep -q "memory/"; then
        echo "memory"
        return
    fi

    # SOP files
    if echo "$files" | grep -q "SOP\|sop"; then
        echo "sop"
        return
    fi

    # Documentation
    if echo "$files" | grep -q "\.md$\|README\|CHANGELOG"; then
        echo "docs"
        return
    fi

    # Configuration
    if echo "$files" | grep -q "\.json$\|\.yaml$\|\.yml$\|\.toml$\|config"; then
        echo "config"
        return
    fi

    # Tests
    if echo "$files" | grep -q "test\|spec\|__tests__"; then
        echo "test"
        return
    fi

    # Scripts
    if echo "$files" | grep -q "\.sh$\|\.ps1$\|scripts/"; then
        echo "chore"
        return
    fi

    # Default
    echo "feat"
}

# Auto-detect scope based on file paths
detect_scope() {
    local files="$1"

    if echo "$files" | grep -q "memory/"; then
        echo "memory"
        return
    fi

    if echo "$files" | grep -q "SOP\|sop"; then
        echo "sop"
        return
    fi

    if echo "$files" | grep -q "projects/"; then
        # Extract project name
        local project=$(echo "$files" | grep "projects/" | head -1 | sed 's|projects/||' | cut -d'/' -f1)
        echo "$project"
        return
    fi

    if echo "$files" | grep -q "\.claude/"; then
        echo "config"
        return
    fi

    if echo "$files" | grep -q "scripts/"; then
        echo "scripts"
        return
    fi

    # Default: use first changed file's directory
    local dir=$(echo "$files" | head -1 | xargs dirname | head -1)
    echo "${dir:-root}"
}

# Generate summary from file changes
generate_summary() {
    local files="$1"
    local type="$2"

    local count=$(echo "$files" | wc -l | tr -d ' ')
    local file_list=$(echo "$files" | head -3 | tr '\n' ', ' | sed 's/,$//')

    case "$type" in
        memory)
            echo "update daily memory ($count files)"
            ;;
        sop)
            echo "update SOP ($count files: $file_list)"
            ;;
        docs)
            echo "update documentation ($count files: $file_list)"
            ;;
        config)
            echo "update configuration ($count files: $file_list)"
            *)
            echo "update files ($count: $file_list)"
            ;;
    esac
}

# Detect components
COMMIT_TYPE=$(detect_type "$CHANGED_FILES")
COMMIT_SCOPE=$(detect_scope "$CHANGED_FILES")
COMMIT_SUMMARY=$(generate_summary "$CHANGED_FILES" "$COMMIT_TYPE")

# Check if on main branch
CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "detached")
if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
    echo "⚠️  Warning: On '$CURRENT_BRANCH' branch"
    echo "Consider: git checkout -b agent/<task-id>-<description>"
    read -p "Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Stage all if nothing staged
if git diff --cached --quiet; then
    echo "Staging all changes..."
    git add -A
fi

# Build commit message
COMMIT_MSG="${COMMIT_TYPE}(${COMMIT_SCOPE}): ${COMMIT_SUMMARY}

Agent-Task: ${AGENT_TASK}
Agent-Model: ${AGENT_MODEL}
Agent-Decision: ${AGENT_DECISION}
Agent-Limitation: auto-detected type and scope"

# Show preview
echo "📋 Detected: type=${COMMIT_TYPE} scope=${COMMIT_SCOPE}"
echo ""
echo "Files:"
git diff --cached --stat
echo ""
echo "Message:"
echo "$COMMIT_MSG"
echo ""

# Commit
git commit -m "$COMMIT_MSG"
echo "✅ Committed: $(git rev-parse --short HEAD)"
