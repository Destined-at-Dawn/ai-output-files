#!/bin/bash
# Agent-Aware Git Commit Script
# Based on AGENT.md Git workflow conventions
#
# Usage: ./agent-commit.sh <type> <scope> <summary> [agent-task] [agent-decision]
#
# Examples:
#   ./agent-commit.sh feat auth "add login endpoint"
#   ./agent-commit.sh fix memory "prevent overwrite on append" "proj-123-memory-fix" "use read-modify-write pattern"

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Validate arguments
if [ $# -lt 3 ]; then
    echo -e "${RED}Error: Missing required arguments${NC}"
    echo "Usage: $0 <type> <scope> <summary> [agent-task] [agent-decision]"
    echo ""
    echo "Types: feat, fix, refactor, docs, style, test, chore, sop, memory, config"
    echo ""
    echo "Examples:"
    echo "  $0 feat auth 'add login endpoint'"
    echo "  $0 fix memory 'prevent overwrite' 'proj-123-fix' 'use read-modify-write'"
    exit 1
fi

COMMIT_TYPE="$1"
COMMIT_SCOPE="$2"
COMMIT_SUMMARY="$3"
AGENT_TASK="${4:-unknown}"
AGENT_DECISION="${5:-standard commit}"

# Validate commit type
VALID_TYPES="feat fix refactor docs style test chore sop memory config perf ci build revert"
if ! echo "$VALID_TYPES" | grep -qw "$COMMIT_TYPE"; then
    echo -e "${RED}Error: Invalid commit type '$COMMIT_TYPE'${NC}"
    echo "Valid types: $VALID_TYPES"
    exit 1
fi

# Get agent model from environment or default
AGENT_MODEL="${AGENT_MODEL:-claude-3.5-sonnet}"

# Build commit message
COMMIT_MSG="${COMMIT_TYPE}(${COMMIT_SCOPE}): ${COMMIT_SUMMARY}

Agent-Task: ${AGENT_TASK}
Agent-Model: ${AGENT_MODEL}
Agent-Decision: ${AGENT_DECISION}
Agent-Limitation: none"

# Check if there are changes to commit
if git diff --cached --quiet && git diff --quiet; then
    echo -e "${YELLOW}Warning: No changes to commit${NC}"
    echo "Stage your changes first with: git add <files>"
    exit 0
fi

# Check if on main branch (with pre-push hook protection)
CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "detached")
if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
    echo -e "${YELLOW}Warning: You are on the '$CURRENT_BRANCH' branch${NC}"
    echo "Consider creating a feature branch: git checkout -b agent/<task-id>-<description>"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Stage all changes if nothing is staged
if git diff --cached --quiet; then
    echo -e "${YELLOW}No staged changes. Staging all modified files...${NC}"
    git add -A
fi

# Show what will be committed
echo -e "${GREEN}Committing:${NC}"
git diff --cached --stat
echo ""
echo -e "${GREEN}Message:${NC}"
echo "$COMMIT_MSG"
echo ""

# Commit
git commit -m "$COMMIT_MSG"
echo -e "${GREEN}✅ Committed successfully${NC}"

# Show commit hash
COMMIT_HASH=$(git rev-parse --short HEAD)
echo -e "Commit: ${GREEN}${COMMIT_HASH}${NC}"
