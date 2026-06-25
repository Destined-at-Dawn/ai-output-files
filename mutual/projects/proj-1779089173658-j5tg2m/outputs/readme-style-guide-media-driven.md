# README 写作风格指南：「媒体驱动型」

> 来源：read2017/learn-anything-with-AI (123 stars) + read2017/business-html-ppt-skill
> 适用：面向中文用户的开源 Skill/工具类仓库
> 与「教训驱动型」（github-publisher 风格）并列，作为可选风格

---

## 风格特征

### 1. 密集徽章行

```markdown
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Skill](https://img.shields.io/badge/type-skill-green.svg)
![Language](https://img.shields.io/badge/language-Markdown-orange.svg)
![Method](https://img.shields.io/badge/method-...-9cf)
![GitHub Stars](https://img.shields.io/github/stars/{user}/{repo}.svg)
```

徽章是"入口信号"——读者不用往下翻就能判断这个仓库是什么、用什么方法、有多受欢迎。

### 2. 双语指针

```markdown
> 🇨🇳 中文版本 | [📖 English Version](./README-en.md)
```

英文版单独放 README-en.md，主页只留一行指针。不搞中英混排。

### 3. 一句话电梯演讲

徽章行下面紧跟一句话核心价值声明。不超过 20 字。

```markdown
> 让 AI 从"问一答一"升级为结构化学习伙伴
```

### 4. 媒体区（可选但强效）

```markdown
<p align="center">
  <img src="https://.../封面.png" width="600" alt="封面"/>
</p>

> 📺 视频教程：[B站](https://...) | 📝 图文教程：[小红书](https://...)
```

图片/视频托管在小红书、B站等平台，README 只放链接和预览。降低仓库体积。

### 5. 快速导航

```markdown
## 快速导航

- [快速开始](#快速开始) | [技能特性](#特性) | [详细文档](./references/) | [自定义指南](./自定义指南)
```

锚点链接，读者跳转不用滚动。

### 6. 30秒快速开始

```markdown
## 30秒快速开始

1. 下载 `skills/learn-anything-skill/` 整个目录
2. 放到 AI 工具的 skills 目录
3. 对 AI 说：**"我要学习神经网络基础"**

就这么简单。
```

极简步骤 + 示例提示词。用户复制粘贴就能用。

### 7. 代理兼容性表格

```markdown
| 代理/工具 | 兼容性 |
|-----------|--------|
| Claude Code | ✅ 已测试 |
| Cursor | ✅ 兼容 |
| Windsurf | ✅ 兼容 |
| GitHub Copilot | ✅ 兼容 |
| Codex CLI | ✅ 已测试 |
| NewMax AI | ✅ 已测试 |
```

### 8. 使用示例（用户可复制的提示词）

```markdown
## 使用示例

直接对 AI 说：

- **"我要系统学习深度学习，每天2小时"** → 自动生成结构化学习计划
- **"用费曼技巧帮我理解反向传播"** → 交互式费曼讲解
- **"读一下这本书"**（上传书籍PDF）→ 三分法精读引导
```

这是最有效的"文档"——用户不需要读说明书，复制一句话就行。

### 9. 目录树

```markdown
## 目录结构

```
skills/learn-anything-skill/
├── SKILL.md                    # 主技能文件
├── agents/
│   └── universal-learning-tutor.md  # 模板加载器
├── assets/                     # 学习模板
│   ├── learning-plan-template.md
│   ├── study-notes-template.md
│   └── ...
└── references/                 # 参考文档
    ├── mastery-rubric.md       # 掌握度评估
    ├── source-strategy.md      # 来源策略
    └── ...
```
```

### 10. 设计原则清单

```markdown
## 设计原则

- ✅ 四层拆解（道法术器）：概念本质 → 原理机制 → 实操步骤 → 工具公式
- ✅ 掌握度检验：不问"你懂了吗"，用任务验证
- ✅ 项目驱动：每阶段都有可交付产出物
- ✅ 来源透明：区分事实依据与建议判断
```

---

## 与「教训驱动型」的对比

| 维度 | 媒体型（read2017） | 教训驱动型（github-publisher） |
|------|-------------------|------------------------------|
| **入口** | 徽章+媒体 | 铁律+事故记录 |
| **信任建立** | 视觉+兼容性+示例 | 安全检查+教训编号 |
| **适用场景** | 面向普通用户、学习类工具 | 面向开发者、安全敏感工具 |
| **首次印象** | "好看、好用、兼容" | "安全、靠谱、不踩坑" |
| **可复用元素** | 徽章行/快速导航/30秒启动/使用示例 | 铁律表/教训编号/Phase流程 |

---

## 使用方式

写 README 时，先判断目标受众：
- **普通用户/学习工具** → 用媒体型
- **开发者/安全工具** → 用教训驱动型
- **两者都适用** → 混合使用（徽章行+铁律表）

---

> 创建日期：2026-06-23
> 来源：read2017 两个仓库分析
