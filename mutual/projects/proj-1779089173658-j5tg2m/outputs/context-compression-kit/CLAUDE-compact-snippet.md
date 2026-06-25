# 以下内容追加到你的 CLAUDE.md 末尾

# Context Compression（上下文压缩自动化）

## Hook 防御链
1. **PreCompact hook**（auto+manual）→ `pre-compact.py`：解析对话 transcript，写检查点到 `.claude/session-checkpoint.md`，返回 `additionalContext`（存活压缩）
2. **SessionStart(compact) hook** → `on-compact.py`：压缩后自动触发，读取检查点，注入恢复上下文
3. **PostCompact hook**（auto）→ 日志记录压缩事件

## 主动压缩策略
- 长任务（>15min）→ 每 30min 主动写检查点
- `/compact focus on [任务]` → 指导 summarizer 保留什么
- `/rewind` → 部分压缩（只压缩历史，保留最近上下文）
- `/clear` → 不相关任务切换时清空上下文

## 压缩后自动恢复
压缩后 Claude Code 自动执行：CLAUDE.md 重新加载 + SessionStart(compact) hook 注入检查点。

## Compact Instructions（保护清单）

When compacting this conversation, ALWAYS preserve:
1. **用户最新需求**：用户最近一条请求原文
2. **修改的文件路径**：所有 write_project_file / Write / Edit 操作的 file_path
3. **文件:行号引用**：所有 Source: path#line 格式的引用
4. **关键决策及理由**：特别是架构级决策
5. **错误状态**：保留根因和修复方案
6. **任务进度**：当前任务的完成百分比和下一步

Do NOT preserve:
- 完整工具输出（只保留摘要和文件路径）
- 中间推理链（只保留结论）
- 逐字读取的文件内容（只保留路径和关键摘录）
- 重复的错误消息（只保留根因和修复方案）
