#!/bin/bash
# privacy-scan.sh - 隐私扫描脚本（每次公开推送前必执行）
#
# 用法：
#   bash scripts/privacy-scan.sh [目录]
#
# 扫描内容：
#   1. 姓名/学号/GPA/学校等个人信息
#   2. 本地路径泄露
#   3. 文件级黑名单（memory/CLAUDE.md 等）
#
# 创建日期：2026-05-26

set -e

SCAN_DIR="${1:-.}"
FAIL=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=== 隐私扫描开始 ==="
echo "扫描目录：$SCAN_DIR"
echo ""

# 第一梯队：致命级
echo "--- 第一梯队：致命级关键词 ---"
KEYWORDS=(
    "小黎"
    "李兰源"
    "兰源"
    "13975"
    "3.896"
    "上海电力大学"
    "上电"
    "SUEP"
    "威泊"
)

for keyword in "${KEYWORDS[@]}"; do
    result=$(grep -ril "$keyword" "$SCAN_DIR" 2>/dev/null | grep -v "\.git/" | head -5)
    if [ -n "$result" ]; then
        echo -e "  ${RED}🔴 发现：$keyword${NC}"
        echo "$result" | while read -r f; do
            echo "     文件：$f"
        done
        FAIL=1
    fi
done

# 路径泄露扫描
echo ""
echo "--- 路径泄露扫描 ---"
PATH_KEYWORDS=(
    "C:\\\\Users\\\\13975"
    "C:/Users/13975"
    "E:\\\\ai产出"
    "E:/ai产出"
    ".newmax"
)

for keyword in "${PATH_KEYWORDS[@]}"; do
    result=$(grep -ril "$keyword" "$SCAN_DIR" 2>/dev/null | grep -v "\.git/" | head -5)
    if [ -n "$result" ]; then
        echo -e "  ${RED}🔴 路径泄露：$keyword${NC}"
        echo "$result" | while read -r f; do
            echo "     文件：$f"
        done
        FAIL=1
    fi
done

# 文件级黑名单
echo ""
echo "--- 文件级黑名单检查 ---"
BLOCKED_FILES=(
    "memory"
    "outputs"
    "CLAUDE.md"
    ".newmax"
    ".telos"
    ".env"
)

for blocked in "${BLOCKED_FILES[@]}"; do
    if [ -e "$SCAN_DIR/$blocked" ]; then
        echo -e "  ${RED}🔴 黑名单文件存在：$blocked${NC}"
        FAIL=1
    fi
done

# 敏感文件扫描
echo ""
echo "--- 敏感文件扫描 ---"
SENSITIVE_PATTERNS=("*.env" "*.pem" "*.key" "*.p12" "credentials*" "secrets*")
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    found=$(find "$SCAN_DIR" -name "$pattern" -not -path "*/.git/*" 2>/dev/null)
    if [ -n "$found" ]; then
        echo -e "  ${RED}🔴 敏感文件：$found${NC}"
        FAIL=1
    fi
done

# 结果
echo ""
echo "=== 扫描结果 ==="
if [ $FAIL -eq 1 ]; then
    echo -e "${RED}❌ 扫描失败：发现隐私泄露风险，禁止推送${NC}"
    echo "请修复上述问题后重新扫描"
    exit 1
else
    echo -e "${GREEN}✅ 扫描通过：未发现隐私泄露${NC}"
    exit 0
fi
