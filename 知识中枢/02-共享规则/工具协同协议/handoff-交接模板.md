# Handoff 交接模板

> 使用：工具 A 完成任务后，下一步该工具 B 接手时，复制此模板填写。
> 位置：`{工作区}/handoffs/{项目名}-{from}-{to}-{任务简称}.md`

---

## 模板

```markdown
# Handoff: {任务名}

> 从：{工具A} → 到：{工具B}
> 日期：{YYYY-MM-DD}
> 关联项目卡：project-context/PROJECT-{项目名}.md

---

## {工具A} 已完成

| 产出 | 路径 | 一句话描述 |
|------|------|-----------|
| {产出1} | {绝对路径} | {描述} |
| {产出2} | {绝对路径} | {描述} |

### 核心结论（{工具B} 必须知道）
- {关键结论 1}
- {关键结论 2}
- {关键结论 3}

---

## {工具B} 需要做

- [ ] {任务 1}
- [ ] {任务 2}
- [ ] {任务 3}

---

## 约束 & 注意事项

### 技术约束
- {限制 1}
- {限制 2}

### 设计/内容偏好
- {偏好 1}
- {偏好 2}

### 文件位置
- 源文件目录：{路径}
- 产出目标目录：{路径}

---

## 参考

- [{参考名称}]({路径或链接})
```

---

## 使用示例

### Newmax → Codex

```markdown
# Handoff: FPGA 项目展示站 → 从 Newmax 到 Codex

> 从：Newmax → 到：Codex
> 日期：2026-06-09
> 关联项目卡：project-context/PROJECT-fpga-showcase.md

## Newmax 已完成

| 产出 | 路径 | 一句话描述 |
|------|------|-----------|
| 需求分析 | E:\...\竞赛\outputs\需求分析-fpga展示站.md | 确定展示站目标、受众、内容范围 |
| 内容大纲 | E:\...\竞赛\outputs\展示站大纲.md | 5 个页面的大纲和内容要点 |

### 核心结论（Codex 必须知道）
- 目标受众：招聘方 + 竞赛评委，技术深度要求高
- 需要展示 5 个 FPGA 项目，每个项目独立页面
- 用户偏好：简洁专业风格，不要花哨动画

## Codex 需要做

- [ ] 整理 5 个项目的技术文档（README + 架构说明）
- [ ] 写 API 参考文档（如果有可展示的接口）
- [ ] 输出每个项目的核心技术亮点列表（方便后续 WorkBuddy 做展示页）

## 约束 & 注意事项

### 技术约束
- 项目源文件在 D:\AMD\，不要移动
- 文档用 Markdown，后续 WorkBuddy 会转 HTML

### 设计/内容偏好
- 技术深度：面向内行人，不解释基础概念
- 格式：结论先行 + 边界声明

### 文件位置
- 源文件目录：D:\AMD\
- 产出目标目录：E:\ai产出文件\牛马\竞赛\outputs\
```

### Codex → WorkBuddy

```markdown
# Handoff: FPGA 项目展示站 → 从 Codex 到 WorkBuddy

> 从：Codex → 到：WorkBuddy
> 日期：2026-06-09
> 关联项目卡：project-context/PROJECT-fpga-showcase.md

## Codex 已完成

| 产出 | 路径 | 一句话描述 |
|------|------|-----------|
| 技术文档 | E:\...\竞赛\outputs\project-docs.md | 5 个项目的完整技术文档 |
| API 参考 | E:\...\竞赛\outputs\api-reference.md | 如有接口的说明 |
| 技术亮点 | E:\...\竞赛\outputs\tech-highlights.md | 每个项目 5 个技术亮点 |

### 核心结论（WorkBuddy 必须知道）
- 5 个项目：ADC 采集 / DAC 输出 / EEPROM 读写 / UART 通信 / 综合控制
- 每个项目页需要：项目简介 + 架构图 + 关键技术指标 + 实物照片位
- 首页做导航：项目卡片网格布局

## WorkBuddy 需要做

- [ ] 根据 project-docs.md 做 5 个项目展示页 + 1 个首页
- [ ] 配色：深蓝主色调（技术感），参考 references/design-spec.png
- [ ] 飞书内嵌适配：宽度 ≤ 800px

## 约束 & 注意事项

### 技术约束
- 页面纯静态 HTML，零依赖
- 飞书不支持 WebGL/Canvas
- 架构图用 Mermaid 内嵌渲染

### 设计/内容偏好
- 风格：简洁专业，面向招聘方
- 色调：深蓝 + 白 + 灰

### 文件位置
- 文档源：E:\ai产出文件\牛马\竞赛\outputs\project-docs.md
- 设计参考：E:\ai产出文件\牛马\竞赛\references\design-spec.png
- HTML 产出：E:\ai产出文件\牛马\竞赛\outputs\showcase\
```

### WorkBuddy → Newmax

```markdown
# Handoff: FPGA 项目展示站 → 从 WorkBuddy 到 Newmax

> 从：WorkBuddy → 到：Newmax
> 日期：2026-06-09
> 关联项目卡：project-context/PROJECT-fpga-showcase.md

## WorkBuddy 已完成

| 产出 | 路径 | 一句话描述 |
|------|------|-----------|
| 展示站首页 | E:\...\竞赛\outputs\showcase\index.html | 5 项目卡片导航 |
| 项目页 ×5 | E:\...\竞赛\outputs\showcase\project-*.html | 每个项目独立展示页 |
| 飞书文档 | https://xxx.feishu.cn/docx/xxx | 飞书版展示文档 |
| 截图 | E:\...\竞赛\outputs\screenshots\ | 6 张页面截图 |

### 核心结论（Newmax 必须知道）
- 页面已部署，可直接双击 index.html 打开
- 视觉亮点：深蓝科技风、架构图渲染清晰、数据指标突出

## Newmax 需要做

- [ ] 基于展示站写 3 篇 XHS 帖子（不同角度：项目 / 技术 / 成长）
- [ ] 写 1 篇公众号文章（深度技术复盘）
- [ ] 飞书文档分享到相关群

## 约束 & 注意事项

### 内容可用的亮点
- ADC 项目：12-bit 精度，采样率 1MSPS
- 整体：5 项目从零到交付，覆盖 ADC/DAC/EEPROM/UART/综合
- 成长线：从学校课程项目 → 公司级文档标准

### 文件位置
- 截图：E:\ai产出文件\牛马\竞赛\outputs\screenshots\
- 展示站：E:\ai产出文件\牛马\竞赛\outputs\showcase\index.html
```

---

> 创建：2026-06-09 | 四位一体协同协议
> 每个工作区应在根目录创建 `handoffs/` 目录存放交接文件
