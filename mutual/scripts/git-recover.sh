#!/bin/bash
# git-recover.sh - 从 Git 历史恢复被删除/被覆盖的文件
# 用法: bash git-recover.sh [文件相对路径]
#       bash git-recover.sh --list [目录路径]  (列出该目录下已删除的文件)
#       bash git-recover.sh --diff [文件路径]  (查看文件最近修改)
#       bash git-recover.sh --all              (恢复最近一次提交中所有被删文件)

set -e
cd "${LEGACY_ROOT}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# 功能1: 列出被删除的文件
if [ "$1" = "--list" ]; then
    DIR="${2:-.}"
    echo -e "${CYAN}=== 最近删除的文件 (${DIR}) ===${NC}"
    # 在最近20个commit中查找被删除的文件
    DELETED=$(git log --oneline --diff-filter=D --name-only -20 -- "$DIR" 2>/dev/null | grep -v "^[a-f0-9]" | grep -v "^$" | sort -u)
    if [ -z "$DELETED" ]; then
        echo -e "${GREEN}没有发现被删除的文件${NC}"
    else
        echo "$DELETED" | while read -r f; do
            LAST=$(git log -1 --format="%h %ai %s" -- "$f" 2>/dev/null)
            echo -e "${RED}  DELETED${NC} $f  ${YELLOW}(${LAST})${NC}"
        done
    fi
    exit 0
fi

# 功能2: 查看文件修改历史
if [ "$1" = "--diff" ]; then
    FILE="$2"
    if [ -z "$FILE" ]; then
        echo "用法: bash git-recover.sh --diff <文件路径>"
        exit 1
    fi
    echo -e "${CYAN}=== 文件修改历史: ${FILE} ===${NC}"
    git log --oneline -10 -- "$FILE" 2>/dev/null
    echo ""
    echo -e "${CYAN}=== 最近一次修改内容 ===${NC}"
    git log -1 -p -- "$FILE" 2>/dev/null | head -60
    exit 0
fi

# 功能3: 恢复最近一次提交中所有被删文件
if [ "$1" = "--all" ]; then
    echo -e "${CYAN}=== 恢复最近一次提交中被删除的文件 ===${NC}"
    COMMIT=$(git log -1 --format="%H" 2>/dev/null)
    if [ -z "$COMMIT" ]; then
        echo -e "${RED}Git 仓库为空${NC}"
        exit 1
    fi
    DELETED_FILES=$(git diff-tree --no-commit-id --diff-filter=D -r "$COMMIT" | awk '{print $NF}')
    if [ -z "$DELETED_FILES" ]; then
        echo -e "${GREEN}最近一次提交没有删除文件${NC}"
        exit 0
    fi
    echo "$DELETED_FILES" | while read -r f; do
        echo -e "${GREEN}  恢复:${NC} $f"
        git checkout "${COMMIT}^" -- "$f" 2>/dev/null || echo -e "${RED}  失败: $f${NC}"
    done
    echo ""
    echo -e "${GREEN}恢复完成！文件已放回原位（已暂存状态）${NC}"
    echo "  执行 'git status' 查看，然后 'git commit' 保存恢复"
    exit 0
fi

# 功能4: 恢复指定文件（默认模式）
FILE="$1"
if [ -z "$FILE" ]; then
    echo -e "${CYAN}Git 文件恢复工具${NC}"
    echo ""
    echo "用法:"
    echo "  bash git-recover.sh <文件路径>           恢复单个文件"
    echo "  bash git-recover.sh --list [目录]        列出已删除的文件"
    echo "  bash git-recover.sh --diff <文件>        查看文件修改历史"
    echo "  bash git-recover.sh --all                恢复最近提交中所有被删文件"
    echo ""
    echo "示例:"
    echo "  bash git-recover.sh mutual/skills/某skill/SKILL.md"
    echo "  bash git-recover.sh --list mutual/skills/"
    exit 0
fi

echo -e "${CYAN}=== 恢复文件: ${FILE} ===${NC}"

# 检查文件是否已存在
if [ -f "$FILE" ]; then
    echo -e "${YELLOW}文件当前存在，将从 Git 历史恢复上一个版本${NC}"
fi

# 查找文件最后存在的 commit
LAST_COMMIT=$(git log -1 --format="%H" -- "$FILE" 2>/dev/null)
if [ -z "$LAST_COMMIT" ]; then
    echo -e "${RED}在 Git 历史中找不到: ${FILE}${NC}"
    echo "  可能是文件从未被提交，或者路径不正确"
    echo "  尝试: bash git-recover.sh --list $(dirname "$FILE")"
    exit 1
fi

# 判断文件是被删除了还是被修改了
STATUS=$(git cat-file -t "${LAST_COMMIT}:${FILE}" 2>/dev/null && echo "exists" || echo "deleted")

echo -e "最后修改: ${YELLOW}$(git log -1 --format='%h %ai %s' -- "$FILE")${NC}"
echo ""

if [ -f "$FILE" ]; then
    echo "文件存在，显示与上次版本的差异:"
    git diff "$LAST_COMMIT" -- "$FILE" | head -40
    echo ""
    read -p "是否用上次版本覆盖当前文件? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git checkout "$LAST_COMMIT" -- "$FILE"
        echo -e "${GREEN}已恢复到版本 ${LAST_COMMIT:0:7}${NC}"
    else
        echo "取消恢复"
    fi
else
    echo -e "${GREEN}文件已被删除，正在恢复...${NC}"
    git checkout "$LAST_COMMIT" -- "$FILE"
    echo -e "${GREEN}✅ 已恢复: ${FILE}${NC}"
    echo "  恢复自版本: ${LAST_COMMIT:0:7}"
    echo "  文件已暂存，执行 'git commit' 保存恢复"
fi
