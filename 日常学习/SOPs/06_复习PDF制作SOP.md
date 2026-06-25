# SOP-06 复习PDF制作

> **工作区：** 日常学习
> **版本：** 1.0 | **最后更新：** 2026-06-18
> **触发条件：** 用户要求把课程章节、课件、教材、笔记、题型整理成“1小时吃透版 / 复习PDF / 考前速通讲义 / 自测题+答案区”

---

## 一、触发条件

| 触发信号 | 示例 | 优先级 |
|----------|------|--------|
| 明确要复习 PDF | “帮我做复习PDF”“做成可打印讲义” | P0 |
| 明确要 1 小时吃透 | “这章做个1小时吃透版”“考前速通” | P0 |
| 要自测和答案区 | “出题+答案”“给我自测题” | P1 |
| 课程章节复习 | “电路第X章复习”“大学物理这章速通” | P1 |

---

## 二、执行步骤

### Step 1: 确认材料和边界
- **操作**：确认课程、章节、考试范围、输入材料路径或粘贴文本。
- **调用 skill**：材料是 PDF/图片时先用 `pdf` 或 `ppocrv5` 抽取文字。
- **输出**：材料清单 + 章节边界 + 是否核心章节。

### Step 2: 生成复习稿
- **操作**：调用 `study-review-pdf`。普通章节按“直觉 / 核心概念 / 套路秒杀 / 自测题 / 答案区”生成 Markdown；期末复习包先走 source-first exam mode，建立资料索引和原题数据库，再生成复习稿。
- **调用 skill**：`study-review-pdf`
- **输出**：`outputs/{课程}-{章节}-1小时吃透版.md`

### Step 3: 质量检查
- **操作**：检查问题是否在答案前、核心概念是否有正反例、题型章节是否有“触发条件 -> 标准动作 -> 易错点”。
- **输出**：通过/需补强清单。

### Step 4: 渲染为可打印产物
- **操作**：调用 study-review-pdf skill 的渲染脚本。**各工具从自身 skills 目录加载**（`.codex` / `.newmax` / `.claude` 三者已同步），`{SKILLS_ROOT}` = 当前工具的 skills 根目录：
```powershell
python "{SKILLS_ROOT}\study-review-pdf\scripts\render_review_pdf.py" "{复习稿.md}" --outdir "{outputs目录}"
```
- **输出**：优先 PDF；若 Pandoc/LaTeX 环境失败，则输出 `.print.html` 并说明失败原因。

### Step 5: 回写学习状态
- **操作**：更新当日 memory；若章节状态变化，再更新课程 `project.md`。
- **输出**：完成记录 + 待回看薄弱点。

---

## 三、决策表

| 输入/场景 | 执行路径 | 使用的 Skill | 产出 |
|-----------|---------|-------------|------|
| 有教材 PDF | PDF 抽取 -> 复习稿 -> 渲染 | `pdf` + `study-review-pdf` | PDF/HTML |
| 有扫描件/图片 | OCR -> 复习稿 -> 渲染 | `ppocrv5` + `study-review-pdf` | PDF/HTML |
| 已有 Markdown/笔记 | 直接生成复习稿 -> 渲染 | `study-review-pdf` | PDF/HTML |
| 期末冲刺包 | 资料索引 -> 原题数据库 -> 题型模板 -> A4速查/模拟卷 | `study-review-pdf` source-first mode | 复习包 |
| 辅助章节 | 只做直觉+概念，说明跳过题型 | `study-review-pdf` | 短讲义 |
| 核心题型章节 | 四模块完整生成 | `study-review-pdf` | 完整讲义+自测 |

---

## 四、检查清单

- [ ] 输入材料来源明确，没有把不同课程混在一起。
- [ ] 复习稿不是单纯摘要，包含自测题。
- [ ] 答案区独立放在题目之后。
- [ ] 核心概念有“人话解释 + 专业定义 + 正例 + 反例/易混点”。
- [ ] 题型章节有“触发条件 + 关键词 + 标准动作 + 易错点”。
- [ ] 渲染结果路径已验证；PDF 失败时已给出 HTML 保底路径。
- [ ] 已写入 memory，必要时更新 `project.md`。

---

## 五、关联Pattern-Key

| Pattern-Key | 描述 | 本SOP中的防犯措施 |
|-------------|------|------------------|
| PK-STUDY-001 | 把复习材料做成被动摘要，学生看完仍不会做题 | Step 2 强制加入自测题和答案区 |
| PK-STUDY-002 | 只列公式，不告诉题目触发条件 | Step 3 检查“触发条件 -> 标准动作” |
| PK-STUDY-003 | PDF 生成失败却声称完成 | Step 4 要求披露失败并交付 HTML |
| PK-STUDY-004 | 多课程材料混用导致错误复习重点 | Step 1 先确认课程和章节边界 |

---

## 六、关联文件

| 文件 | 用途 | 读取时机 |
|------|------|---------|
| `{SKILLS_ROOT}\study-review-pdf\SKILL.md` | 复习 PDF 生成主流程（已同步 .codex/.newmax/.claude 三工具） | Step 2 |
| `{SKILLS_ROOT}\study-review-pdf\references\review-template.md` | 标准复习稿模板（skill 自含，**不依赖任何 proj 目录**） | Step 2 |
| `{SKILLS_ROOT}\study-review-pdf\scripts\render_review_pdf.py` | Markdown 渲染 HTML/PDF | Step 4 |
| `E:\ai产出文件\牛马\日常学习\memory\MEMORY.md` | 历史薄弱点和学习原则 | Step 1 |
| `E:\ai产出文件\牛马\日常学习\projects\{课程}\project.md` | 章节进度和状态 | Step 1/5 |

---

## 七、Skill链路

```
课程材料/PDF/笔记 ->
1. pdf 或 ppocrv5（抽取材料）
2. study-review-pdf（生成1小时吃透复习稿）
3. render_review_pdf.py（渲染 HTML/PDF）
4. memory/project.md（回写学习状态）
-> 可打印复习 PDF/HTML
```

---

## 变更记录

| 日期 | 版本 | 变更内容 |
|------|------|---------|
| 2026-06-18 | 1.0 | 从“电路分析-1小时吃透版模板”沉淀为 SOP |
| 2026-06-18 | 1.1 | Hermes 去孤岛：skill 同步 .codex/.newmax/.claude 三工具；渲染路径与关联文件改用 `{SKILLS_ROOT}` 工具无关占位；声明 skill 自含、不依赖 proj 目录 |
