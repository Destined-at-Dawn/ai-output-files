# E:\ai产出文件 全面审计报告

> 审计日期：2026-06-25
> 审计范围：E:\ai产出文件\ 全目录 + C盘 .newmax/.claude/.codex 配置 + F:\work 工作文件
> 审计方式：逐目录 ls + 逐文件 Read CLAUDE.md + grep 硬编码路径统计

---

## 一、E:\ai产出文件 根目录结构

```
E:\ai产出文件\
├── 牛马\                    (主生态, 7 个工作区)
│   ├── 竞赛\竞赛\           (竞赛区, 双重嵌套)
│   ├── 创作\创作\           (创作区, 双重嵌套)
│   ├── 个人\个人\           (个人区, 双重嵌套)
│   ├── 求职\求职\           (求职区, 双重嵌套)
│   ├── 日常学习\            (日常学习区, 单层)
│   ├── mutual\mutual\       (管理优化区, 双重嵌套)
│   ├── 归档\                (全局归档, 30+ 归档记录)
│   └── 知识中枢\            (Obsidian Vault, 9 个子目录)
├── 论文\                    (独立工作区, 不属于牛马体系)
├── 归档\                    (根级归档)
├── scripts\                 (根级脚本)
├── conversations\           (对话记录)
└── projects\                (根级项目)
```

---

## 二、7 个工作区逐一审计

### 2.1 竞赛区 (E:\ai产出文件\牛马\竞赛\竞赛\)

| 维度 | 状态 |
|------|------|
| CLAUDE.md | 855 行, **25 处硬编码路径** |
| .claude/rules/ | **23 个文件** (与 mutual 标准版高度重复, 额外 1 个 rtl-fpga-lessons.md) |
| skills/ | 1 个 (competition-yolo, 有 SKILL.md + references/) |
| memory/ | 22 个日志文件 + MEMORY.md + long-term.md + rtl_code_lessons.md |
| outputs/ | 8 个子目录 (列表/地图/模型/论文/报告/提交/相机/yolov8), 混乱 |
| projects/ | 15+ 个 proj 目录 |
| scripts/ | 9 个脚本 (adc_rules_skill_converter.py 等) |
| self-evolution/ | 有内容 (做得好的/做得差的/lessons/patterns) |
| skill-routing-table.json | **41 条路由** (少于 mutual 的 264 条) |
| workspace-manifest.md | 有 |

**问题**:
- 路由表只有 41 条, 与 mutual 的 264 条严重不同步
- outputs/ 下有 YOLO 训练结果和 FPGA 综合产物, 混在一起
- .claude/rules/ 与 mutual 完全重复的有 22 个文件

---

### 2.2 创作区 (E:\ai产出文件\牛马\创作\创作\)

| 维度 | 状态 |
|------|------|
| CLAUDE.md | 796 行, **19 处硬编码路径** |
| .claude/rules/ | **24 个文件** (含 3 个特供: content-creation-rules.md, knowledge-base-maintenance.md, li联盟特供版.md) |
| skills/ | 2 个 (platform-writer-unified, show-notes-cli) |
| memory/ | 7 个日志文件 + MEMORY.md + long-term.md + IDEAS/ |
| outputs/ | **按平台分类** (公众号运营/短视频/社群运营/小红书/脚本/子技能合集/素材/模板/媒体运营手册) |
| scripts/ | 多个脚本 (build_link_tree.py, dual-write-verify.py 等) |
| SOPs/ | **21 个 SOP** (含带编号的迭代版本 v1-v6) |
| self-evolution/ | 有内容 |

**问题**:
- SOPs 有 21 个, 但很多是迭代版本 (v1-v6), 需要清理旧版本
- outputs/ 分类较好 (按平台), 但与 .claude/rules 的 lesson-sink-checklist.md 路径硬编码冲突
- 有联盟特供版规则, 需要确认是否仍然需要

---

### 2.3 个人区 (E:\ai产出文件\牛马\个人\个人\)

| 维度 | 状态 |
|------|------|
| CLAUDE.md | 677 行, **17 处硬编码路径** |
| .claude/rules/ | **21 个文件** (含 1 个特供: li联盟特供版.md) |
| skills/ | 2 个 (blog-post-writer, niuma-voice-dna) |
| memory/ | 20 个日志文件 + MEMORY.md + MEMORY_dup.md + long-term.md + 考研规划-上交东南-常州电网.md |
| outputs/ | 知识库索引/实践手册/决策记录/全域增长手册/小红书头像/目标/提示词库/复盘/选择比努力更重要/页面 |
| projects/ | **24 个 proj 目录** (最多) |
| 百大认知书籍/ | **62 本认知科学书籍** (重要资产) |
| self-evolution/ | 有内容 |

**问题**:
- 有 MEMORY_dup.md 重复文件, 需要清理
- 百大认知书籍 (62 本) 是重要资产, 迁移时必须完整保留
- projects/ 有 24 个 proj, 很多可能已过期

---

### 2.4 求职区 (E:\ai产出文件\牛马\求职\求职\)

| 维度 | 状态 |
|------|------|
| CLAUDE.md | 706 行, **16 处硬编码路径** |
| .claude/rules/ | **21 个文件** (标准版) |
| skills/ | 1 个 (resume-skill, 有 SKILL.md) |
| memory/ | 12 个日志文件 + MEMORY.md + long-term.md |
| outputs/ | 竞赛+实习+WPS表格 |
| projects/ | 4 个 proj 目录 |
| scripts/ | 5 个脚本 |
| self-evolution/ | 有内容 |

**问题**:
- outputs/ 较少, 结构简单
- 硬编码路径最少 (16 处), 但仍需清理

---

### 2.5 日常学习区 (E:\ai产出文件\牛马\日常学习\)

| 维度 | 状态 |
|------|------|
| CLAUDE.md | 455 行, **17 处硬编码路径** |
| .claude/rules/ | **无** (唯一没有 .claude/rules/ 的工作区) |
| skills/ | **无** (无本地 skill) |
| memory/ | 9 个日志文件 + MEMORY.md + long-term.md |
| outputs/ | **无** |
| projects/ | 5 个课程目录 (高数/大英/四六级/大物/电路分析) |
| SOPs/ | 4 个 SOP (物理电路解题/任务收尾/课程学习/SOP总索引) |
| self-evolution/ | 有内容 (含 Course-Inside/) |

**问题**:
- 缺少 .claude/rules/, 不符合统一结构
- evolution-calendar.md 在根目录而非 self-evolution/
- 无 outputs/ 目录

---

### 2.6 mutual 管理优化区 (E:\ai产出文件\牛马\mutual\mutual\)

| 维度 | 状态 |
|------|------|
| CLAUDE.md | 650 行, **3 处硬编码路径** (最精简) |
| .claude/rules/ | **23 个文件** (标准版, 被其他 5 个区复制) |
| skills/ | 无本地 skill (使用 C:\Users\13975\.newmax\skills\) |
| memory/ | 31 个日志文件 + long-term.md + hermes 相关 + 记忆优化 |
| outputs/ | **31 个文件** (大量一次性脚本和分析报告) |
| projects/ | 当前活跃 proj |
| self-evolution/ | 有内容 |
| ecosystem-manual/ | 生态手册 (distillations/) |
| skill-routing-table.json | **264 条路由** (最完整) |
| workspace-manifest.md | 有 |

**问题**:
- outputs/ 堆积了 31 个文件, 大多是一次性脚本和分析报告
- 是 .claude/rules/ 的"源头", 其他 5 个区从这里复制
- 路由表 264 条是最完整的, 但其他区只有 41 条或更少

---

### 2.7 论文区 (E:\ai产出文件\论文\) -- 独立工作区

| 维度 | 状态 |
|------|------|
| CLAUDE.md | 404 行, **最精简最专业**, 独立于牛马体系 |
| .claude/rules/ | 1 个文件 (script-safety-check.md) |
| skills/ | 1 个 (academic-writing-pro, 有 SKILL.md) |
| memory/ | 2 个日志文件 + long-term.md |
| outputs/ | 论文相关产出 |
| papers/ | 6 个论文项目 (FPGA/竞赛/电力/高压/高增益) |
| scripts/ | 1 个脚本 (new_paper.py) |
| templates/ | 3 个期刊模板 (IEEE/Elsevier/Springer-Nature) |
| academic-skill-routing.md | 学术 Skill 路由表 |

**问题**:
- 独立于牛马体系, 无跨区 skill 系统
- 结构最规范, 是最佳参考模板

---

## 三、知识中枢 (E:\ai产出文件\牛马\知识中枢\)

| 目录 | 内容 | 文件数 |
|------|------|--------|
| 00-注册表/ | 工作区注册表, 路由配置, skill 分类决策树 | 3 |
| 01-工作区记忆/ | hermes 记忆中枢 (atomic-facts, cross-tool-state) | 2+ |
| 02-共享规则/ | 19 个共享规则文件 (已迁移) | 19 |
| 03-Hermes/ | hermes 相关 | 1+ |
| 04-SOP/ | 6 个 SOP 文件 | 6 |
| 05-每日记忆/ | 跨区每日记忆 | 多 |
| 06-百大认知知识库/ | 62 本认知书籍 Obsidian vault | 62+ |
| 07-方法论输出/ | 副教授相关 | 1+ |
| 08-跨区项目记录/ | 跨区项目文档 | 1+ |
| 09-领域知识库/ | 领域知识 | 0 (空) |

---

## 四、C 盘配置审计

### 4.1 .newmax/ (Newmax 主配置)

| 文件 | 用途 | 硬编码路径 |
|------|------|-----------|
| CLAUDE.md | 全局入口 | 5 处 |
| .mcp.json | 3 个 MCP 服务器 (markitdown/mempalace/agentmail) | 0 处 (用相对路径) |
| scripts/ | 2 个 MCP 脚本 (markitdown_quiet.py, mempalace_mcp.py) | 0 处 |
| skills/ | 28+ 个 skill 目录 | 3 处 (wechat-decrypt 2, wechat-analysis 1, study-review-pdf 1) |

### 4.2 .claude/ (原版 Claude Code)

| 文件 | 用途 | 硬编码路径 |
|------|------|-----------|
| rules/ | 16 个全局规则文件 | **0 处** |
| telos/ | 用户个人信息 (单一真相源) | 0 处 |

### 4.3 .codex/ (Codex 配置)

| 文件 | 用途 | 硬编码路径 |
|------|------|-----------|
| AGENTS.md | Codex 专用指令 | 未统计 |

---

## 五、F:\work 工作文件审计

| 目录 | 内容 | AI 关联度 |
|------|------|----------|
| 接单/ | 接单工作 (AGENTS.md, CLAUDE.md, clients/, configs/, docs/) | **高** (有 CLAUDE.md) |
| 定时任务+自动化流程包/ | outputs/ | 中 |
| 竞赛工作流包/ | outputs/ | 中 |
| 网页设计/ | 网页设计项目 | 高 (有 CLAUDE.md 引用) |
| 个人建站/ | lilanyuan.cn 建站项目 (src/, scripts/) | 高 (有 CLAUDE.md 引用) |
| 机械制图/ | 2 个图片文件 | 低 |
| BY1 控制器配套设计说明文档/ | AI 协作记录, 交付包, 脚本 | **高** (有 AI 协作记录) |

---

## 六、核心问题汇总

### 问题 1: 路径硬编码 (最高优先级)

**总计: ~122 处硬编码绝对路径**

| 位置 | 硬编码数 | 示例 |
|------|---------|------|
| 7 个 CLAUDE.md | 102 处 | `E:\ai产出文件\牛马\竞赛\竞赛\memory\long-term.md` |
| .claude/rules/ 文件 | 10+ 处 | `E:\ai产出文件\牛马\创作\创作\scripts\dual-write-verify.py` |
| 知识中枢/02-共享规则/ | 6 处 | `E:\ai产出文件\牛马\mutual\mutual\` |
| .newmax/skills/ | 3 处 | `E:\ai产出文件\牛马\` |
| **合计** | **~122 处** | |

### 问题 2: .claude/rules/ 大规模重复

**23 个规则文件被完整复制到 5 个工作区 = 115 个文件, 大量重复**

| 工作区 | 规则文件数 | 额外文件 |
|--------|-----------|---------|
| mutual (源头) | 23 | 无 |
| 竞赛 | 23 | + rtl-fpga-lessons.md |
| 创作 | 24 | + content-creation-rules.md, knowledge-base-maintenance.md, li联盟特供版.md |
| 求职 | 21 | 无 |
| 个人 | 21 | + li联盟特供版.md |
| 日常学习 | **0** | 无 (缺失) |
| 论文 | 1 | 仅 script-safety-check.md |

**每个规则文件平均 200-800 行, 重复内容约 20,000+ 行**

### 问题 3: 路由表碎片化

| 工作区 | 路由条数 | 状态 |
|--------|---------|------|
| mutual | 264 条 | 最完整 (权威源) |
| 竞赛 | 41 条 | 严重不同步 |
| 创作 | 存在 | 未统计 |
| 求职 | 存在 | 未统计 |
| 个人 | 存在 | 未统计 |
| 日常学习 | 存在 | 未统计 |

### 问题 4: 命名不一致 (双重嵌套)

| 工作区 | 当前路径 | 问题 |
|--------|---------|------|
| 竞赛 | `竞赛\竞赛\` | 双重嵌套 |
| 创作 | `创作\创作\` | 双重嵌套 |
| 个人 | `个人\个人\` | 双重嵌套 |
| 求职 | `求职\求职\` | 双重嵌套 |
| mutual | `mutual\mutual\` | 双重嵌套 |
| 日常学习 | `日常学习\` | 正常 |
| 论文 | `论文\` | 正常 |

### 问题 5: outputs/ 堆积

| 工作区 | outputs/ 状态 | 问题 |
|--------|-------------|------|
| mutual | 31 个文件 | 大量一次性脚本和报告 |
| 竞赛 | 8 个子目录 | YOLO 训练结果和 FPGA 产物混在一起 |
| 创作 | 按平台分类 | 结构较好 |
| 求职 | 较少 | 结构简单 |
| 个人 | 多个内容 | 需要整理 |
| 日常学习 | **无** | 缺失 |
| 论文 | 论文相关 | 正常 |

### 问题 6: 缺乏统一 skill 管理

| 位置 | skill 数量 | 说明 |
|------|-----------|------|
| C:\Users\13975\.newmax\skills\ | 28+ | 全局可用 |
| 竞赛/skills/ | 1 | 本地 |
| 创作/skills/ | 2 | 本地 |
| 求职/skills/ | 1 | 本地 |
| 个人/skills/ | 2 | 本地 |
| 日常学习/skills/ | 0 | 缺失 |
| 论文/skills/ | 1 | 本地 |

---

## 七、迁移计划

### Phase 0: 准备工作

**创建 F:\ai产出文件\ 目录骨架:**

```
F:\ai产出文件\
├── mutual\              (从 mutual\mutual\ 迁移, 去掉一层)
├── 个人\
├── 创作\
├── 求职\
├── 竞赛\
├── 日常学习\
├── 论文\
├── 知识中枢\            (Obsidian Vault + 共享规则中心)
├── 归档\                (全局归档)
├── _shared\             (跨工作区共享资源, 新增)
│   ├── rules\           (19 个共享规则源, 从知识中枢/02-共享规则/ 迁移)
│   ├── templates\       (工作区模板)
│   └── skill-registry\  (路由表 + skill 索引)
└── _work-bridge\        (F:\work 整合桥接层, 新增)
    ├── CLAUDE-bridge.md (桥接配置)
    ├── 网页设计\         (AI 相关文件同步)
    └── 个人建站\         (AI 相关文件同步)
```

**每个工作区统一内部结构:**

```
{工作区}\
├── CLAUDE.md            (变量占位符版本)
├── .claude\rules\       (仅工作区特定规则, 共享规则引用 _shared/)
├── memory\              (长期 + 每日记忆)
├── outputs\             (清理后)
├── SOPs\                (标准操作流程)
├── skills\              (工作区特定 skill)
├── self-evolution\      (自我进化)
└── projects\            (临时项目)
```

### Phase 1: 逐工作区迁移 (7 个, 按优先级)

**迁移顺序**: mutual -> 竞赛 -> 创作 -> 求职 -> 个人 -> 日常学习 -> 论文

每个工作区:
1. Read 原 CLAUDE.md, 识别硬编码路径
2. 生成变量占位符版本
3. 复制 memory/, SOPs/, .claude/rules/
4. 整理 outputs/ (可复用脚本保留, 一次性脚本移入 `_archived-scripts/`)
5. 验证

### Phase 2: 共享资源整合

- 知识中枢/02-共享规则/ 的 19 个规则 -> `_shared/rules/`
- skill-routing-table.json -> `_shared/skill-registry/`
- 创建 CLAUDE.md 标准模板 -> `_shared/templates/`

### Phase 3: F:\work 桥接

- 创建 `CLAUDE-bridge.md`: 定义 AI 在 F:\work 下工作时如何加载经验/skill
- 同步网页设计/个人建站的 CLAUDE.md 和 SOP 到桥接层

### Phase 4: 变量占位符系统

| 变量 | 含义 |
|------|------|
| `${WORKSPACE_ROOT}` | 当前工作区根目录 |
| `${AI_ROOT}` | F:\ai产出文件\ |
| `${SHARED_RULES}` | _shared\rules\ |
| `${SKILL_REGISTRY}` | _shared\skill-registry\ |
| `${KNOWLEDGE_HUB}` | 知识中枢\ |
| `${NEWMAX_HOME}` | ~/.newmax/ |

### Phase 5: C 盘配置更新

- 扫描 .newmax/skills/ 的硬编码路径 -> 替换变量
- 更新 ~/.newmax/.mcp.json
- 清理 ~/.codex/ 冗余

### Phase 6: 验证与文档

- grep 扫描确认无残留硬编码
- skill 路由测试
- 创建迁移日志和变量参考手册

---

## 八、需要用户确认的问题

1. **F 盘读写权限**: F:\ 根目录 ls 返回"Permission denied", 需要确认 F:\ai产出文件\ 是否已存在, 以及是否有写入权限
2. **联盟特供版规则**: 创作区和个人区有"li联盟特供版.md", 是否仍然需要?
3. **MEMORY_dup.md**: 个人区有 MEMORY_dup.md 重复文件, 是否直接丢弃?
4. **F:\work 接单/ 目录**: 有 AGENTS.md 和 CLAUDE.md, 是否需要纳入迁移范围?
5. **百大认知书籍 (62 本)**: 这些书籍文件很大, 是否需要完整复制到 F 盘?
6. **论文区**: 是否保持独立, 还是纳入牛马体系?
