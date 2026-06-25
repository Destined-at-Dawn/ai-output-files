#!/bin/bash
# ============================================================
# NiumaAutoCommit - Auto commit script
# Called every 2 hours by Windows Task Scheduler via Git Bash
# Follows AGENT.md Conventional Commits + Agent Trailer
# ============================================================

set -euo pipefail

GIT_ROOT="${LEGACY_ROOT}"
LOG_DIR="$GIT_ROOT/logs"
LOG_FILE="$LOG_DIR/auto-commit.log"

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo "$1"
}

cd "$GIT_ROOT" || { log "ERROR: Cannot cd to $GIT_ROOT"; exit 1; }

# Verify git repo
if ! git rev-parse --git-dir >/dev/null 2>&1; then
    log "ERROR: Not a git repo at $GIT_ROOT"
    exit 1
fi

# Check for changes
STATUS=$(git status --porcelain)
if [ -z "$STATUS" ]; then
    log "INFO: No changes to commit"
    exit 0
fi

TOTAL=$(echo "$STATUS" | wc -l | tr -d ' ')
log "INFO: Found $TOTAL changed files"

# Stage all
git add -A

# Auto-detect scope from changed files
SCOPE="auto"
TYPE="chore"

CHANGED=$(git diff --cached --name-only)

if echo "$CHANGED" | grep -qi "memory/"; then
    SCOPE="memory"
elif echo "$CHANGED" | grep -qi "sop"; then
    SCOPE="sop"
elif echo "$CHANGED" | grep -qiE "\.(json|yaml|yml)$|CLAUDE\.md"; then
    SCOPE="config"
fi

# Count change types
MODIFIED=$(echo "$STATUS" | grep -c "^ M\|^M " || true)
UNTRACKED=$(echo "$STATUS" | grep -c "^?? " || true)
DELETED=$(echo "$STATUS" | grep -c "^ D\|^D " || true)

if [ "$MODIFIED" -gt 0 ] && [ "$UNTRACKED" -eq 0 ] && [ "$DELETED" -eq 0 ]; then
    TYPE="fix"
    SCOPE="sync"
elif [ "$UNTRACKED" -gt "$MODIFIED" ]; then
    TYPE="feat"
fi

DATESTR=$(date '+%Y-%m-%d %H:%M')

# Commit with multi-line message
git commit -m "$TYPE($SCOPE): auto batch commit $DATESTR

Changes: $TOTAL files ($MODIFIED modified, $UNTRACKED new, $DELETED deleted)
Auto-committed by NiumaAutoCommit scheduled task

Agent-Task: auto-scheduled
Agent-Model: auto-commit.sh
Agent-Decision: batch commit $TOTAL changes
Agent-Limitation: no semantic review, auto-detected type=$TYPE scope=$SCOPE"

if [ $? -eq 0 ]; then
    log "OK: Committed $TYPE($SCOPE): $TOTAL files"

    # Push to remote
    if git remote | grep -q "origin"; then
        BRANCH=$(git branch --show-current)
        if git push origin "$BRANCH" 2>/dev/null; then
            log "OK: Pushed to origin/$BRANCH"
        else
            log "WARN: Push failed to origin/$BRANCH"
        fi
    fi
else
    log "WARN: Commit failed"
    git reset HEAD >/dev/null 2>&1 || true
fi

log "INFO: Script finished"
