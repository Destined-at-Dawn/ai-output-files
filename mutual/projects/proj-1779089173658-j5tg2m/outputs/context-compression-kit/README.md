# Context Compression Kit

> Claude Code 上下文压缩/恢复自动化 — 一键安装包
> 让你的 Claude Code 在上下文压缩后不会"失忆"。

## 这是什么？

Claude Code 对话进行到一定长度后会自动压缩上下文（compaction）。压缩后，Claude 可能忘记：
- 刚才改了哪些文件
- 当前任务是什么
- 关键决策的理由

这个工具包通过 Claude Code 原生的 **Hook 机制**，在压缩前自动写检查点、压缩后自动恢复上下文。

## 工作原理

```
对话进行中 → 上下文渐满 → 触发压缩
                              ↓
              PreCompact hook 解析对话记录
              → 提取：用户消息、修改的文件、关键决策、错误状态
              → 写入检查点到 .claude/session-checkpoint.md
              → 返回 additionalContext（存活压缩）
                              ↓
                    Claude Code 执行压缩
                              ↓
              SessionStart(compact) hook 触发
              → 读取检查点
              → 注入恢复上下文
                              ↓
              Claude 继续工作（知道刚才做了什么）
```

## 安装

### 前提条件
- Python 3.8+
- Claude Code 已安装

### 一键安装

```bash
# 1. 解压到任意位置
# 2. 在你的 Claude Code 项目根目录下运行：

python /path/to/context-compression-kit/install.py

# 或者指定项目目录：
python install.py --dir /path/to/your/project
```

安装脚本会：
1. 创建 `.claude/hooks/` 目录
2. 复制 hook 脚本
3. 合并 `.claude/settings.json`（不覆盖你已有的配置）
4. 复制 `context-essentials.md`
5. 提示你手动修改 CLAUDE.md

### 手动步骤

安装脚本会提示你将 `CLAUDE-compact-snippet.md` 的内容追加到你的 `CLAUDE.md` 末尾。

这一步是必须的，因为：
- CLAUDE.md 的 `Compact Instructions` 段指导压缩器保留什么
- 没有这个段，压缩器会按默认策略丢弃信息

## 包含的文件

```
context-compression-kit/
├── README.md                       # 本文件
├── install.py                      # 一键安装脚本
├── CLAUDE-compact-snippet.md       # 需要追加到 CLAUDE.md 的内容
├── hooks/
│   ├── pre-compact.py              # PreCompact hook（压缩前检查点）
│   └── on-compact.py               # SessionStart hook（压缩后恢复）
└── templates/
    ├── settings-hooks.json         # hooks 配置模板
    └── context-essentials.md       # 压缩后注入的铁律
```

## 测试

安装后，在 Claude Code 中：

1. 进行一段正常对话（让它读写几个文件）
2. 输入 `/compact` 手动触发压缩
3. 检查 `.claude/session-checkpoint.md` 是否被自动写入
4. 压缩后，Claude 应该能继续刚才的任务（而不是一脸懵）

## 自定义

### 修改保护清单

编辑 `CLAUDE-compact-snippet.md` 中的 Compact Instructions 段，告诉压缩器什么该保留、什么该丢弃。

### 修改检查点格式

编辑 `hooks/pre-compact.py` 中的 `build_checkpoint()` 函数。

### 修改恢复行为

编辑 `hooks/on-compact.py` 中的 `main()` 函数。

## 原理细节

### 三层防御

| 层级 | 机制 | 作用 |
|------|------|------|
| L1 | CLAUDE.md Compact Instructions | 告诉 summarizer 保留什么 |
| L2 | PreCompact hook | 自动写检查点到磁盘 |
| L3 | SessionStart(compact) hook | 压缩后自动注入恢复上下文 |

### 九段式检查点

PreCompact hook 生成的检查点包含 9 个段落：

1. 当前任务（最新用户请求）
2. 最近用户消息（最后 3 条）
3. 最近助手回复摘要
4. 修改的文件（保护清单 — 压缩后必须重读）
5. 读取的文件
6. 关键决策
7. 错误状态
8. 文件:行号引用
9. 工具使用统计

### additionalContext

PreCompact hook 除了写磁盘文件，还返回 `additionalContext`（< 10K 字符），这段内容**直接存活压缩**，不会被 summarizer 丢弃。它指向检查点文件的位置，确保压缩后能找到完整信息。

## 已知限制

- **检查点质量取决于对话长度**：如果对话太短（< 5 轮），检查点信息可能不完整
- **memory/ 目录需要存在**：on-compact.py 会尝试读取 `memory/` 下的文件，如果你的项目没有 memory 目录，这部分会被跳过（不影响其他功能）
- **Windows 路径**：脚本使用 Python 原生路径处理，兼容 Windows/macOS/Linux
- **不支持嵌套项目**：只在项目根目录的 `.claude/` 下生效

## 来源

基于以下研究迭代（28 轮）：
- Claude Code 官方文档：hooks 格式、SessionStart(compact) matcher
- Anthropic Context Compaction Cookbook
- claude-code-brain-bootstrap (GitHub)
- claude-memory-engine (GitHub)
- Forge Code 模式匹配压缩算法
