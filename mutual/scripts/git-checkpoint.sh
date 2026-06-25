#!/bin/bash
cd "${LEGACY_ROOT}"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
MSG="${1:-checkpoint: ${TIMESTAMP}}"
git add -A
if git diff --cached --quiet 2>/dev/null; then
    echo "[checkpoint] no changes to commit"
    exit 0
fi
git commit -m "$MSG"
echo "[checkpoint] committed: $MSG"
