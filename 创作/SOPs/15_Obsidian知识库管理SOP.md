# SOP-15：Obsidian 知识库管理 SOP（个性化版）

> **适用场景**：Obsidian Vault 搭建、AI 插件配置、笔记模板管理、知识图谱维护、**框架驱动AI研究**
> **版本**：v2.1 | 2026-06-09
> **前置依赖**：已完成 Obsidian 安装 + 基本配置

---

## 零、框架驱动AI研究（v2.0 新增 — 1小时了解陌生行业）

> **来源**：YouCore王世民「如何用 Obsidian 在 1 小时内快速了解陌生行业？」
> **核心公式**：专业分析框架 + AI自动搜索填充 + 人工检查 + 一键输出PDF = 1小时了解陌生行业

### 0.1 四步流程

| 步骤 | 操作 | 耗时 | 工具 |
|------|------|------|------|
| **① 框架提取** | 从思维导图/图片提取分析框架 → 生成MD文件 | 3min | AI读取图片 |
| **② AI填充** | AI按框架每个子项逐一搜索最新数据并填入 | 10min | Obsidian AI插件 |
| **③ 人工检查** | 逐页阅读检查，选择文字让AI调整 | 45min | 人工+AI |
| **④ 输出PDF** | 10个MD文件合并渲染为带封面目录的PDF | 1min | AI命令 |

### 0.2 关键设计原则

1. **框架驱动而非AI发挥**：不是"帮我分析XX行业"，而是给AI一个10维度×数十子指标的专业框架，让它按框架逐一搜索填充
2. **框架和数据分离**：框架来自人的判断（方法论），数据填充来自AI的执行（搜索能力）
3. **可复用可迭代**：分析框架存为Obsidian模板，下次换行业直接复用，3个月后让AI刷新数据覆盖旧文件

### 0.3 行业分析框架模板（10维度）

用户应将以下框架存入Obsidian `_Templates/` 目录：

```
Template - 行业分析/
├── 宏观环境分析.md     # PESTEL六维
├── 市场分析.md         # 市场总量+消费者行为
├── 行业分析.md         # 产业链+商业模式
├── 竞争分析.md         # 龙头企业+市场份额
├── 渠道分析.md         # 分销渠道+触达方式
├── 原材料供应分析.md    # 核心零部件+供应商
├── 技术分析.md         # 技术趋势+专利
├── 内部销售分析.md      # 营收+增长
├── 财务分析.md         # 成本+利润
└── 企业资源与能力分析.md # 团队+IP+壁垒
```

### 0.4 可直接复制的 Prompt 模板

**Step 1 — 从图片提取框架**（3min）：
```
@Assets/行业分析/行业分析框架.png 读取图片，将第一层的每个节点作为一页md文档保存在
@Assets/行业分析/标准分析框架 下，例如 宏观环境分析.md、市场分析.md
每个md文档，按第二层及以后层次的节点构建空白目录
```

**Step 2 — AI 搜索填充**（10min）：
```
对照这个标准分析框架，分析 {行业名} 行业。
分析结果，保存在 @Assets/行业分析/{行业名} 下
每个维度要求：① 引用最新数据（标注年份和来源）② 列出关键企业/产品名 ③ 给出具体数字
```

**Step 3 — 人工检查调整**（45min）：
```
选择具体文字 → 让AI调整：
"这段数据过时了，请搜索2026年最新数据替换"
"这个分析太泛，请补充 {具体企业名} 的案例"
"请用表格对比 {企业A} 和 {企业B} 的 {指标}"
```

**Step 4 — 输出PDF**（1min）：
```
将10个分析文件的内容合并输出为一份PDF文档
要求：封面+目录+蓝色主题+表格清晰+每维度自成一章
```

### 0.5 与现有SOP的集成

| 场景 | 触发词 | 行动 |
|------|-------|------|
| 快速了解陌生行业 | "帮我了解XX行业" / "XX行业分析" | 走本流程四步 |
| 竞品分析 | "分析一下XX公司的竞品" | 用竞争分析模板 |
| 投资分析 | "XX行业值不值得投" | 用完整10维度框架 |
| 论文选题调研 | "这个方向有多少人在做" | 用技术分析+竞争分析 |
| OPC 机会评估 | "XX值不值得做" | 走 SOP-22 + 本流程市场分析 |

---

## 一、Vault 结构设计（小黎专属）

### 1.1 核心理念

「结构为 AI 服务，AI 强化结构」——每个文件夹、每个模板、每个 frontmatter 字段都必须是**机器可读**的。

### 1.2 推荐目录结构

```
小黎的Vault/
├── _Templates/                    # 笔记模板（Obsidian 模板目录）
│   ├── Template - 论文.md
│   ├── Template - 术语.md
│   ├── Template - 实习日志.md
│   ├── Template - 课程笔记.md
│   ├── Template - 项目.md
│   ├── Template - MOC.md
│   └── Template - 人物.md
│
├── 00-Inbox/                      # 未处理的快速捕获
│
├── 01-Research/                   # 科研笔记（活跃项目）
│   ├── Papers/                    # 论文笔记（PDF自动解析产出）
│   ├── Terms/                     # 术语表（自动提取+人工修正）
│   ├── MOC/                       # Map of Content（知识地图）
│   └── Projects/                  # 科研项目（集创赛/ICAN/皮影戏）
│
├── 02-Internship/                 # 实习进展库
│   ├── Daily/                     # 每日实习记录
│   ├── Weekly/                    # 每周总结
│   ├── Skills/                    # 实习中学到的技能
│   └── Learnings/                 # 关键收获和复盘
│
├── 03-EE-AI/                      # 电气×AI 交叉领域
│   ├── PowerSystems/              # 电力系统 + AI
│   ├── FPGA/                      # FPGA + AI 加速
│   ├── EmbodiedAI/                # 具身智能
│   └── OPC/                       # 个人成长方法论
│
├── 04-Courses/                    # 课程笔记
│   ├── 大一/                      # 按学期分
│   └── 大二/
│
├── 05-Content/                    # 创作素材（公众号/小红书）
│   ├── Drafts/                    # 草稿
│   ├── Published/                 # 已发布
│   └── Ideas/                     # 选题灵感
│
├── 06-People/                     # 人脉关系
│
├── 07-Journal/                    # 日记/周记/月记
│   ├── Daily/
│   ├── Weekly/
│   └── Monthly/
│
├── 99-Archive/                    # 已完成/已归档
│
├── _Attachments/                  # 图片和文件附件
│
└── .obsidian/                     # Obsidian 配置（自动管理）
```

### 1.3 命名规则

| 类型 | 格式 | 示例 |
|------|------|------|
| 论文笔记 | `{作者}-{年份}-{关键词}.md` | `Vaswani-2017-Attention.md` |
| 术语 | `{术语名}.md` | `反向传播.md` |
| 实习日志 | `{YYYY-MM-DD}-实习.md` | `2026-07-01-实习.md` |
| 项目 | `{项目名}.md` | `ICAN小车.md` |
| MOC | `MOC-{领域}.md` | `MOC-FPGA.md` |
| 课程 | `{学期}-{课程名}.md` | `大一-电路原理.md` |

---

## 二、AI 插件配置（2026 最佳实践）

### 2.1 必装三件套

| 插件 | 安装方式 | 用途 | 模型 |
|------|---------|------|------|
| **Obsidian Copilot** | 社区插件搜索「Copilot」 | 主力 AI 对话 + Vault 问答 | DeepSeek V3（免费） |
| **Smart Connections** | 社区插件搜索「Smart Connections」 | 语义搜索 + 笔记关联发现 | 本地嵌入（免费） |
| **Smart Composer** | 社区插件搜索「Smart Composer」 | Cursor 式内联编辑 | DeepSeek V3 |

### 2.2 配置优先级

**第一步：Copilot 配置（5 分钟）**

```
Settings → Copilot → Model → Add Custom Model
  Model Name: DeepSeek V3
  Provider: OpenAI Compatible
  Base URL: https://api.deepseek.com/v1
  API Key: [你的 DeepSeek API Key]
  Model ID: deepseek-chat
```

**第二步：Smart Connections 本地嵌入（零成本）**

```
Settings → Smart Connections → Embedding Model
  选择: Built-in Local Embedding Model（不花钱，不发数据到云端）
  
等索引完成（首次可能需要 10-30 分钟，取决于笔记数量）
```

**第三步：Smart Composer（Cursor 式编辑）**

```
Settings → Smart Composer
  Model: DeepSeek V3（同 Copilot）
  Context: 开启 Vault 全局搜索
```

### 2.3 可选增强

| 插件 | 用途 | 优先级 |
|------|------|--------|
| **Nova** | 内联编辑（类似 Copilot 快捷键） | 有 Copilot 可跳过 |
| **LLM Wiki** | 知识库查询增强 | Smart Connections 够用可跳过 |
| **Obsidian Bases** | 内置数据库视图 | 高——自动汇总笔记 |
| **Dataview** | 高级查询和视图 | 高——和 Bases 配合 |
| **Templater** | 高级模板引擎 | 高——比原生模板强大 |
| **Calendar** | 日历视图 | 日记场景必装 |
| **Kanban** | 看板视图 | 项目管理用 |

---

## 三、笔记模板系统

### 3.1 论文笔记模板

```markdown
---
tags:
  - Paper
  - "{{领域}}"
authors:
  - "{{作者}}"
year: {{年份}}
venue: "{{会议/期刊}}"
rating: 0          # 1-5星，读完后填
status: unread     # unread / reading / done
last updated: "{{日期}}"
---

## 概述

> [!info] 一句话总结
> {{AI 自动生成的论文摘要，3句话以内}}

## 核心贡献

- 贡献1：...
- 贡献2：...

## 方法

{{AI 自动提取的方法部分，保留关键公式和图示}}

## 实验结果

| 指标 | 本文 | 基线 | 提升 |
|------|------|------|------|
| ... | ... | ... | ... |

## 与我的研究关系

> [!tip] 这篇论文对我的价值
> - 可以借鉴：...
> - 可以对比：...
> - 可以引用：...

## 术语提取

> [!note] 新术语（自动从文中提取）
> - [[术语1]]：定义...
> - [[术语2]]：定义...

## 参考笔记

```base
filters:
  and:
    - file.inFolder("01-Research/Terms")
    - file.hasLink(this.file)
views:
  - type: table
    order:
      - file.name
```
```

### 3.2 实习日志模板

```markdown
---
tags:
  - Internship
  - Daily
date: "{{日期}}"
day: {{第N天}}
mood: ""          # 😊😐😤💪
last updated: "{{日期}}"
---

## 今日任务

- [ ] 任务1
- [ ] 任务2
- [ ] 任务3

## 实际完成

### 任务1：{{任务名}}
- 做了什么：...
- 学到什么：...
- 遇到什么问题：...
- 怎么解决的：...

### 任务2：{{任务名}}
- 做了什么：...
- 学到什么：...

## 今日收获

> [!tip] 关键收获（3条以内）
> 1. ...
> 2. ...
> 3. ...

## 明日计划

- [ ] ...

## 技能成长

> [!note] 今天学到的新技能/工具
> - [[技能名]]：...

## 关键词索引

#实习第{{N}}天 #{{技术标签}}
```

### 3.3 术语模板

```markdown
---
tags:
  - Term
  - "{{领域}}"
aliases:
  - "{{英文名}}"
related:
  - "[[相关术语1]]"
  - "[[相关术语2]]"
last updated: "{{日期}}"
---

## 定义

{{简洁定义，2句话以内}}

## 详细解释

{{AI 辅助生成的详细解释，学生能懂的深度}}

## 公式（如果有）

$$
{{LaTeX 公式}}
$$

## 应用场景

- 场景1：...
- 场景2：...

## 出现在哪些论文中

```base
filters:
  and:
    - file.inFolder("01-Research/Papers")
    - file.hasLink(this.file)
views:
  - type: table
    order:
      - file.name
      - status
```

## 参考来源

- 来源1：...
- 来源2：...
```

---

## 四、AI 工作流（核心）

### 4.1 论文解析工作流

```
1. 把 PDF 放到 01-Research/Papers/ 文件夹
2. 打开 Copilot，输入：
   "请解析这篇论文，生成结构化笔记，填写论文笔记模板"
3. Copilot 自动生成：
   - 概述、核心贡献、方法、实验结果
   - 提取新术语并创建术语笔记
   - 建立论文↔术语的双向链接
4. 人工复核 → 修正 AI 的误判 → 打分
```

### 4.2 实习日志工作流

```
1. 每天下班前，打开 Copilot
2. 输入："帮我整理今天的实习记录，用实习日志模板"
3. Copilot 基于今天的零散笔记生成结构化日志
4. 补充：情绪、遇到的问题、解决方案
5. 自动生成技能成长笔记（如果学了新东西）
```

### 4.3 知识图谱维护工作流（每周一次）

```
1. 打开 Smart Connections 面板
2. 检查"孤立笔记"（没有任何链接的笔记）
3. 对每个孤立笔记：
   - 查看 Smart Connections 推荐的关联笔记
   - 建立 2-3 个双向链接
   - 更新对应 MOC
4. 更新 MOC 索引（Copilot 辅助）
```

### 4.4 课程笔记工作流

```
1. 上课录音 + 拍照（用手机）
2. 下课后，把录音转文字（Whisper/飞书妙记）
3. 把文字和照片放到 _Attachments/
4. 打开 Copilot："根据这些材料，用课程笔记模板整理"
5. AI 生成结构化笔记 + 提取公式 + 建立术语链接
```

---

## 五、Obsidian Bases 配置

### 5.1 论文库总览（放在 01-Research/Papers.base）

```yaml
filters:
  and:
    - file.inFolder("01-Research/Papers")
properties:
  file.name:
    displayName: 论文
  note.authors:
    displayName: 作者
  note.year:
    displayName: 年份
  note.rating:
    displayName: 评分
  note.status:
    displayName: 状态
  note.venue:
    displayName: 会议
views:
  - type: table
    name: 全部论文
    order:
      - file.name
      - year
      - authors
      - rating
      - status
      - venue
    sort:
      - property: year
        direction: DESC
      - property: rating
        direction: DESC
  - type: table
    name: 未读论文
    filters:
      and:
        - note.status = "unread"
    order:
      - file.name
      - year
      - venue
  - type: table
    name: 高分论文
    filters:
      and:
        - note.rating >= 4
    order:
      - file.name
      - rating
      - venue
```

### 5.2 实习进度总览（放在 02-Internship/Internship.base）

```yaml
filters:
  and:
    - file.inFolder("02-Internship")
properties:
  file.name:
    displayName: 记录
  note.date:
    displayName: 日期
  note.day:
    displayName: 第N天
  note.mood:
    displayName: 心情
views:
  - type: table
    name: 全部日志
    order:
      - date
      - file.name
      - mood
    sort:
      - property: date
        direction: DESC
  - type: table
    name: 本周
    filters:
      and:
        - note.date >= date(today, "-7d")
    order:
      - date
      - file.name
      - mood
```

---

## 六、与牛马 AI 的集成

### 6.1 Obsidian MCP Server（让 AI 直接读写 Vault）

```bash
# 安装
npm install -g obsidian-mcp-server

# 在 ~/.newmax/.mcp.json 中添加：
{
  "obsidian": {
    "command": "obsidian-mcp-server",
    "args": ["--vault", "E:\\path\\to\\your\\vault"]
  }
}
```

### 6.2 从牛马 AI 工作区直接操作 Vault

```
用户："帮我把这篇论文解析到 Obsidian"
→ AI 调用 MCP Server → 读取 PDF → 创建笔记 → 建立链接
→ 全自动，不需要手动复制粘贴
```

### 6.3 从 YouTube 视频学习

```bash
# 安装 yt-dlp
pip install yt-dlp

# 提取字幕
yt-dlp --write-auto-sub --sub-lang en --skip-download -o "%(title)s.%(ext)s" "https://youtube.com/watch?v=xxx"

# AI 处理字幕 → 生成结构化笔记 → 写入 Obsidian Vault
```

---

## 七、维护节奏

| 频率 | 动作 | 耗时 |
|------|------|------|
| **每天** | 实习日志 + 课程笔记 | 15 分钟 |
| **每周** | 知识图谱维护（检查孤立笔记） | 30 分钟 |
| **每月** | MOC 更新 + 归档已完成项目 | 1 小时 |
| **每学期** | Vault 结构优化 + 插件更新 | 2 小时 |

---

## 八、v3 增强功能（2026-05-28 新增）

> 以下内容来自公众号文章提取和分析的系统性信息差，已融入 Obsidian+AI 入门指南 v3。

### 8.1 微信→Obsidian 自动同步

**两种方案**（详见入门指南 v3 §8.3）：

| 方案 | 工具 | 适用场景 |
|------|------|---------|
| 轻量方案 | 笔记同步助手（notehelper 插件） | 偶尔有重要内容需保存，零技术门槛 |
| AI 方案 | AutoClaw（AI Agent） | 每天大量微信内容需自动分类整理 |

**集成到工作流**：微信转发 → 同步助手/Agent → Obsidian Inbox → AI 整理 → 对应文件夹。

### 8.2 Agent Skills 按需加载

**核心理念**：不要把所有规则堆在 CLAUDE.md 里。用「渐进式披露」三层策略（详见入门指南 v3 §6.4）：

- **常驻层**：核心身份+偏好（< 300 字）
- **按需层**：专项 Skill，关键词触发才加载
- **懒加载层**：参考资料，AI 判断需要时才读

**自我蒸馏**：每 2 周用提示词让 Claude Code 扫描工作记录，找出可自动化的重复工作流 → 打包成 Skill。

### 8.3 语音笔记工作流

微信语音 → 转文字 → 转发同步助手 → Obsidian → AI 整理为结构化笔记（详见入门指南 v3 §8.7）。

### 8.4 /goal 长任务自主执行

```bash
/goal 扫描 Vault 中所有无标签笔记，根据内容自动添加标签。每批 20 个汇报进度。
/goal 找出所有孤立笔记，用 Smart Connections 推荐链接，列出建议清单。
```

---

## 九、资源索引

### 已下载的仓库（github/ 目录下）

| 仓库 | 路径 | 用途 |
|------|------|------|
| Smart Connections | `github/smart-connections/` | 语义搜索 + 笔记关联（源码参考） |
| AI Second Brain | `github/ai-second-brain/` | CODE/PARA 模板 + AI Skills 范例 |
| Awesome Obsidian AI | 搜索获取 | 86 个 AI 插件清单 |

### 关键链接

- Obsidian 官网：https://obsidian.md
- Obsidian 帮助文档：https://help.obsidian.md
- Smart Connections：https://github.com/brianpetro/obsidian-smart-connections
- AI Second Brain 模板：https://github.com/jamesmcroft/obsidian-ai-second-brain
- Ollama（本地 AI）：https://ollama.com
- yt-dlp（YouTube 字幕提取）：https://github.com/yt-dlp/yt-dlp
- AutoClaw（AI Agent，微信→Obsidian）：https://github.com/affaan-m/ECC
- Whisper（语音转文字）：https://github.com/openai/whisper
- SkillOpt（微软，Skill 自动优化）：https://github.com/microsoft/SkillOpt

---

## 十、迭代日志

| 日期 | 变更 | 版本 |
|------|------|------|
| 2026-05-26 | 初版，基于 AI Second Brain 模板 + 小黎实际场景定制 | v1.0 |
| 2026-05-28 | 新增 §八 v3 增强功能（微信同步、Agent Skills按需加载、语音笔记、/goal命令）；更新资源索引；关联入门指南 v3 | v1.1 |
| 2026-06-09 | 新增 §〇 框架驱动AI研究（v2.0，10维度模板） | v2.0 |
| 2026-06-09 | §〇 新增 §0.4 可直接复制的 Prompt 模板（Step 1-4 具体指令）+ §0.5 OPC评估集成 + 来源确认王世民原文 | v2.1 |
