# R15 主目录优先架构

> proj-ID 是暂存区，中文主目录是权威源。
> 来源：2026-05-25 proj-ID 碎片化治理方案。

---

## 问题背景

newmax 平台每次新建对话会生成 `proj-{timestamp}-{random}` 目录。这些目录：
- 名称无意义，用户无法凭名称识别内容
- 每个目录各自生成 memory/、outputs/，导致记忆和产出碎片化
- SOP/规则文件在每个目录各存一份，修改一处不能同步

## 核心规则

**每个 proj-ID 目录必须关联一个中文主目录（`YYYYMMDD-任务名` 格式）。主目录是唯一权威数据源。**

### 目录命名
- 主目录：`{YYYYMMDD}-{中文任务名}`（如 `20260525-公众号运营`）
- proj-ID：`proj-{timestamp}-{random}`（newmax 平台自动分配，仅作暂存区）

### 数据流向

| 数据类型 | 写入位置 | 读取位置 | 会话结束后 |
|---------|---------|---------|-----------|
| long-term.md | 主目录/memory/ | 主目录/memory/ | 不动 |
| 每日记忆 YYYY-MM-DD.md | 主目录/memory/ | 主目录/memory/ | 不动 |
| CLAUDE.md | 主目录/ | 主目录/ | 不动 |
| .claude/rules/ | 主目录/.claude/rules/ | 主目录/.claude/rules/（Claude Code 自动加载） | 不动 |
| SOPs/ | 主目录/SOPs/ | 主目录/SOPs/ | 不动 |
| 永久产出 | 主目录/outputs/ | 主目录/outputs/ | 不动 |
| 临时草稿 | proj-ID/outputs/ | proj-ID/outputs/ | 有价值的复制到主目录，然后归档 proj-ID |

### 会话启动协议
1. 检查 proj-ID 目录下是否有 `.session-meta.json`
2. 如有 → 读取 `mainDirectory` 字段，从主目录加载记忆/规则/SOP
3. 如无 → 这是新项目，需要先创建主目录（用 scaffold-workspace skill）

### 会话结束协议
1. proj-ID 暂存区有价值产出 → 复制到主目录 outputs/
2. proj-ID 目录 → 备份后移到归档/
3. 每日记忆 → 确认已在主目录中（不需额外合并）

---

## 适用范围

所有 5 个工作区（mutual、创作、个人、求职、竞赛）均适用。

## 关联规则
- R13 地图优先于盲搜
- No Blind Overwrite（修改前必须先读）
- 双归档铁律（删除/移动前必须备份）
