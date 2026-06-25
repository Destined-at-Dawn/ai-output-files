# SOP 总索引

## 结论

本学习区 SOP 采用“意图 -> SOP -> 输出文件”的路由方式。复习 PDF、章节图片、A4 速查、模拟卷统一走 `06_复习PDF制作SOP.md`，并强制启用 `source-first exam mode`。

Source: ..\CLAUDE.md#li-intent 意图理解层（SOP驱动智能路由）
Source: ..\AGENT.md#七、Skill 使用

---

## SOP 列表

### 01 内容分析

- 文件：`sop-content-analysis.md`
- 触发：读/分析/解读/总结文章或链接。
- 输出：结论先行、原因、行动建议。
Source: sop-content-analysis.md#Trigger Intent

### 02 内容创作

- 文件：`sop-content-creation.md`
- 触发：写/做/创建内容。
- 输出：平台适配格式、CTA、反馈记录。
Source: sop-content-creation.md#Trigger Intent

### 03 深度调研

- 文件：`sop-research.md`
- 触发：调研/研究/搜/查找/了解/对比。
- 输出：30秒版、2分钟版、完整版。
Source: sop-research.md#Trigger Intent

### 04 Skill 生命周期

- 文件：`sop-skill-lifecycle.md`
- 触发：创建、优化、审核、拆分、融合 skill。
- 输出：skill 方案、质量门禁、迭代记录。
Source: sop-skill-lifecycle.md#SOP

### 06 复习 PDF 制作

- 文件：`06_复习PDF制作SOP.md`
- 路由：`skill-routing-table.json#r403`
- 触发：复习PDF、章节复习稿、期末冲刺包、A4速查表、模拟卷、原题数据库、题型模板。
- 强制链路：资料索引 -> 原题数据库 -> 题型模板/陷阱表 -> A4速查/模拟卷/章节图片 -> 复习 PDF。
- 关键规则：旧图和旧 PDF 只作为版式参考，事实来源必须回到当前教材、PPT、习题、答案和最终复习题。
Source: 06_复习PDF制作SOP.md#Source-First Exam Mode

---

## r403 路由说明

命中 `r403` 时，不允许直接生成 PDF 或图片。必须先检查以下文件是否存在且与当前目标章节匹配：

- `outputs/00_资料索引.md`
- `outputs/chapter_resource_index.md`
- `outputs/05_教材原题与习题原题索引.md`
- 对应章节 `习题/exercise_index.md`

若缺失，先补 P0/P1；若已存在但目标章节未覆盖，先更新对应章节记录。

Source: 06_复习PDF制作SOP.md#PDF / 图片制作流程
