#!/bin/bash
# git-recover.sh - Git 文件恢复脚本（30秒内恢复任何被删文件）
#
# 用法：
#   bash scripts/git-recover.sh --list [目录]    列出最近删除的文件
#   bash scripts/git-recover.sh --diff <文件>    查看文件修改历史
#   bash scripts/git-recover.sh --all            恢复最近一次提交中所有被删文件
#   bash scripts/git-recover.sh <文件路径>        恢复指定文件
#
# 创建日期：2026-05-26
# 来源：AI 误删文件风险 → 必须有秒级恢复能力

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否在 git 仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ 错误：当前目录不是 Git 仓库${NC}"
    echo "请先 cd 到有 .git 的目录再执行"
    exit 1
fi

# 模式 1：列出最近删除的文件
if [ "$1" = "--list" ]; then
    DIR="${2:-.}"
    echo -e "${YELLOW}📋 最近一次提交中删除的文件：${NC}"
    DELETED=$(git diff --name-status HEAD~1 HEAD 2>/dev/null | grep "^D" | awk '{print $2}')
    if [ -z "$DELETED" ]; then
        echo -e "${GREEN}✅ 没有发现被删除的文件${NC}"
    else
        echo "$DELETED" | while read -r file; do
            echo -e "  ${RED}🗑 $file${NC}"
        done
        echo ""
        echo -e "${YELLOW}恢复单个文件：bash scripts/git-recover.sh <文件路径>${NC}"
        echo -e "${YELLOW}恢复所有文件：bash scripts/git-recover.sh --all${NC}"
    fi
    exit 0
fi

# 模式 2：查看文件修改历史
if [ "$1" = "--diff" ]; then
    FILE="$2"
    if [ -z "$FILE" ]; then
        echo -e "${RED}❌ 用法：bash scripts/git-recover.sh --diff <文件路径>${NC}"
        exit 1
    fi
    echo -e "${YELLOW}📜 文件修改历史：$FILE${NC}"
    git log --oneline --follow -- "$FILE" 2>/dev/null || echo "未找到该文件的历史记录"
    exit 0
fi

# 模式 3：恢复所有被删文件
if [ "$1" = "--all" ]; then
    echo -e "${YELLOW}🔄 恢复最近一次提交中所有被删文件...${NC}"
    DELETED=$(git diff --name-status HEAD~1 HEAD 2>/dev/null | grep "^D" | awk '{print $2}')
    if [ -z "$DELETED" ]; then
        echo -e "${GREEN}✅ 没有发现被删除的文件${NC}"
        exit 0
    fi
    COUNT=0
    echo "$DELETED" | while read -r file; do
        git checkout HEAD~1 -- "$file" 2>/dev/null && {
            echo -e "  ${GREEN}✅ 已恢复：$file${NC}"
            COUNT=$((COUNT + 1))
        } || {
            echo -e "  ${RED}❌ 恢复失败：$file${NC}"
        }
    done
    echo ""
    echo -e "${GREEN}恢复完成。请用 'git status' 确认，然后 'git add + git commit' 保存恢复。${NC}"
    exit 0
fi

# 模式 4：恢复单个文件
if [ -n "$1" ] && [ "$1" != "--help" ] && [ "$1" != "-h" ]; then
    FILE="$1"
    echo -e "${YELLOW}🔄 恢复文件：$FILE${NC}"

    # 尝试从最近一次提交恢复
    if git checkout HEAD -- "$FILE" 2>/dev/null; then
        echo -e "${GREEN}✅ 已从 HEAD 恢复：$FILE${NC}"
        exit 0
    fi

    # 尝试从上一次提交恢复（文件在最近一次被删）
    if git checkout HEAD~1 -- "$FILE" 2>/dev/null; then
        echo -e "${GREEN}✅ 已从 HEAD~1 恢复：$FILE${NC}"
        exit 0
    fi

    # 尝试从更早的历史恢复
    LAST_COMMIT=$(git log --all --pretty=format:"%H" -- "$FILE" 2>/dev/null | head -1)
    if [ -n "$LAST_COMMIT" ]; then
        if git checkout "$LAST_COMMIT" -- "$FILE" 2>/dev/null; then
            echo -e "${GREEN}✅ 已从历史提交 $LAST_COMMIT 恢复：$FILE${NC}"
            exit 0
        fi
    fi

    echo -e "${RED}❌ 无法恢复：$FILE${NC}"
    echo "可能原因："
    echo "  1. 文件从未被 commit 过"
    echo "  2. 文件路径不正确"
    echo "  3. 文件在 git 历史中不存在"
    echo ""
    echo "尝试：bash scripts/git-recover.sh --list 查看可恢复的文件"
    exit 1
fi

# 帮助信息
echo "用法："
echo "  bash scripts/git-recover.sh --list [目录]    列出最近删除的文件"
echo "  bash scripts/git-recover.sh --diff <文件>    查看文件修改历史"
echo "  bash scripts/git-recover.sh --all            恢复所有被删文件"
echo "  bash scripts/git-recover.sh <文件路径>        恢复指定文件"
echo ""
echo "创建日期：2026-05-26"
