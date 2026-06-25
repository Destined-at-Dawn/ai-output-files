# Context Compression Skill

> 上下文压缩自动化 — 基于 Claude Code 原生 Hook 机制
> 触发词：压缩上下文、context compression、上下文管理、检查点、checkpoint

## 核心原理

Claude Code 原生提供三层压缩控制，本 skill 配置并协调它们：

```
用户对话进行中
  → context 渐满
  → PreCompact hook 触发 → 解析 transcript → 写检查点 → 返回 additionalContext
  → compaction 执行（summarizer 读取 CLAUDE.md Compact Instructions）
  → SessionStart(compact) hook 触发 → 读检查点 → 注入恢复上下文
  → Claude 继续工作（带压缩后的上下文 + 恢复信息）
```

---

## Hook 配置（.claude/settings.json）

### PreCompact Hook（压缩前）
- **脚本**：`.claude/hooks/pre-compact.py`
- **触发**：auto（自动压缩）+ manual（用户 /compact）
- **动作**：
  1. 从 stdin JSON 读取 `transcript_path`
  2. 解析 JSONL 对话记录（最后 200 行）
  3. 提取：用户消息、助手回复、工具调用、修改的文件
  4. 写检查点到 `.claude/session-checkpoint.md`
  5. 返回 `additionalContext`（存活压缩，指向检查点位置）
- **超时**：30 秒
- **输出限制**：10,000 字符

### SessionStart(compact) Hook（压缩后）
- **脚本**：`.claude/hooks/on-compact.py`
- **触发**：每次 compaction 完成后
- **动作**：
  1. 读取 `.claude/session-checkpoint.md`（PreCompact 写入的）
  2. 读取 `memory/{today}.md` 尾部
  3. 输出恢复指令到 stdout → Claude 自动注入上下文
- **超时**：15 秒

### PostCompact Hook（日志）
- **触发**：auto
- **动作**：记录压缩事件时间戳

---

## CLAUDE.md Compact Instructions

CLAUDE.md 末尾的 `# Compact Instructions` 段落指导 summarizer 保留什么：

**必须保留**：用户最新需求、修改的文件路径、关键决策及理由、错误状态、任务进度
**不保留**：完整工具输出、中间推理、逐字文件内容

---

## 主动压缩策略

### 何时主动 /compact
- 长任务（>15min）→ 每 30min 主动写检查点 + `/compact focus on [当前任务]`
- 感觉 Claude 开始"忘记"早期对话 → 主动压缩
- 不相关任务切换前 → `/clear`（比 /compact 更彻底）

### /compact 指令模板
```
/compact focus on [具体任务名]。保留所有修改的文件路径和关键决策。
```

### /rewind 部分压缩
- 双击 Esc → 选择检查点
- "Summarize from here" → 压缩后面部分，保留前面
- "Summarize up to here" → 压缩前面部分，保留最近

---

## 压缩后恢复清单

压缩后 Claude Code 自动执行：
1. ✅ CLAUDE.md（root）从磁盘重新加载（自动）
2. ✅ .claude/rules/ 重新加载（自动）
3. ✅ SessionStart(compact) hook 注入检查点（自动）
4. ⚠️ skill descriptions 不会重载（已加载的 body 保留，上限 5K/skill）
5. ⚠️ path-scoped rules 需要再次读取对应文件
6. ⚠️ 嵌套 CLAUDE.md（子目录）不会自动重载

---

## 与现有系统集成

| 系统 | 集成方式 |
|------|---------|
| memory/ 系统 | PreCompact 写检查点引用 memory/ 路径；on-compact.py 读取今日记忆 |
| auto-evolution | 压缩日志记录到 memory/compression-log.md，供进化分析 |
| CLAUDE.md 启动序列 | Step 6 检查 session-checkpoint.md，压缩后自动恢复 |
| project-tools MCP | 检查点中记录修改的文件列表，恢复后可继续操作 |
| skill-routing-table | 路由表在 CLAUDE.md 中，compaction 后自动重载 |

---

## 压缩日志

每次压缩事件记录到 `memory/compression-log.md`：
```markdown
## [日期 时间] 压缩事件
- 类型：auto/manual
- 检查点：.claude/session-checkpoint.md
- 恢复状态：成功/失败
```

---

## 研究来源

| 来源 | 关键发现 |
|------|---------|
| Claude Code 官方文档 | hooks 格式、SessionStart(compact) matcher、Compact Instructions |
| claude-code-brain-bootstrap (GitHub) | PreCompact transcript 解析 + SessionStart 双 matcher |
| claude-memory-engine (GitHub) | 三层保存点（mid-session + PreCompact + SessionEnd） |
| claude-memory-compiler (GitHub) | PreCompact 解析 JSONL + 后台 LLM 提取 |
| claude-diary (GitHub) | PreCompact 注入 /diary 指令触发日记生成 |
| Anthropic 工程博客 | Context Engineering 三大技术、Progressive Disclosure |
| Anthropic 官方最佳实践 | Sub-agent 隔离、path-scoped rules、/rewind 部分压缩 |
