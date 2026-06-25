# R16 根目录优先约束架构 - 落地报告

> 日期：2026-05-25
> 执行者：mutual 工作区
> 影响范围：五大工作区（mutual、个人、创作、竞赛、求职）

## 背景

小黎要求统一治理五大工作区，解决：
1. proj-ID 碎片化问题
2. 约束、记忆、产出重复问题
3. 缺乏统一读取顺序问题

## 执行内容

### 第1轮：归档式清理
- 5个工作区共 178 个治理文件已归档删除
- 归档位置：`E:\ai产出文件\牛马\归档\2026-05-25-governance-cleanup\`

### 第2轮：R16规则注入
- 5个工作区 CLAUDE.md 全部升级到 R16
- 读取顺序、写入规则、禁止规则已固化

### 第3轮：目录结构创建
- 5个工作区 × 4个核心目录 = 20个目录创建
- .claude/rules/、SOPs/、memory/、outputs/

### 第4轮：骨架文件创建
- 5个工作区 × 6个骨架文件 = 30个文件创建
- read-order.md、write-rules.md、project-directory-rules.md
- session-lifecycle.md、long-term.md、.gitkeep

### 第5轮：规范文件创建
- 5个工作区 × 11个规范文件 = 55个文件创建
- naming-convention.md、archive-rules.md、index-rules.md
- memory-rules.md、output-rules.md、skill-routing-rules.md
- memory-spec.md、output-spec.md、session-checklist.md
- workspace-manifest.json、cross-workspace-ref.md、rules-list.md
- sop-list.md、rules-count.md、session-meta-template.json

## R16 核心规则

### 读取顺序（每次对话必须执行，Step 1-4 不可跳过）
1. 根目录 `CLAUDE.md` ← 全局约束
2. 根目录 `memory/long-term.md` ← 长期记忆
3. 根目录 `memory/{今天日期}.md` ← 今日记忆
4. `.claude/rules/` ← 工程法则（Claude Code 自动加载）
5. 根目录 `SOPs/` ← SOP 入口（按需）
6. 根目录 `index.md` ← 统一索引（按需）
7. ~~项目目录 `rules/`~~ ← 已删除，所有规则在 `.claude/rules/`
8. 项目目录 `outputs/` ← 中间产物（按需）

### 写入规则
- 记忆 → 只写根目录 `memory/`
- 最终产出 → 只写根目录 `outputs/`
- 项目约束 → 只写与根目录不重复的差异项
- 中间产物 → 可写项目目录，会话结束后提升到根目录

### 项目文件夹禁止放什么
- ❌ 不放全局约束（已在根目录）
- ❌ 不放 SOP（已在根目录）
- ❌ 不放记忆文件（已在根目录）
- ❌ 不放技能调用规则（已在根目录）
- ❌ 不放统一索引（已在根目录）

## 验证结果

| 工作区 | R16状态 | .claude/rules/ | SOPs/ | memory/ | outputs/ |
|--------|---------|--------|-------|---------|----------|
| mutual | ✅ | ✅ | ✅ | ✅ | ✅ |
| 个人 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 创作 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 竞赛 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 求职 | ✅ | ✅ | ✅ | ✅ | ✅ |

## 后续工作

1. 验证读取顺序是否生效
2. 清理残留的proj-ID目录
3. 建立定期审计机制

---

*报告生成时间：2026-05-25 22:30*
