# agent-commit.ps1 - Agent 自动提交脚本（Windows/PowerShell 版本）
#
# 用法：
#   .\scripts\agent-commit.ps1 -Type feat -Scope memory -Summary "Add daily summary"
#
# 参数：
#   -Type        : Commit 类型（feat/fix/chore/docs/memory/sop/config/refactor/test）
#   -Scope       : 变更范围
#   -Summary     : 变更摘要
#   -TaskId      : 任务 ID（可选）
#   -Model       : 使用的模型（可选）
#   -Decision    : 关键设计决策（可选）
#   -Limitation  : 已知局限（可选）

param(
    [string]$Type = "chore",
    [string]$Scope = "auto",
    [string]$Summary = "Auto commit by agent",
    [string]$TaskId = "scheduled-task",
    [string]$Model = "claude-code",
    [string]$Decision = "Automated commit",
    [string]$Limitation = "None"
)

# 检查是否有更改
$status = git status --porcelain
if (-not $status) {
    Write-Host "No changes to commit."
    exit 0
}

# 生成 commit message（Agent Trailer 格式）
$commitMsg = @"
$Type($Scope): $Summary

Agent-Task: $TaskId
Agent-Model: $Model
Agent-Decision: $Decision
Agent-Limitation: $Limitation
"@

# 添加所有更改
git add -A

# 提交
git commit -m $commitMsg

Write-Host "✅ Committed: $Type($Scope): $Summary"
