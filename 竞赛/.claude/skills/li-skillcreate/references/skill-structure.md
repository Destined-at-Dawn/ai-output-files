# Phase 3 详细技能结构规范

> 本文件是 li-skillcreate SKILL.md Phase 3 的详细参考，包含 SKILL.md 六层结构、references/ 规范、_meta.json 格式。

---

## SKILL.md 六层结构

**Layer 1：YAML Frontmatter**（必须）

```yaml
---
name: skill-name         # 小写+连字符，≤64字符
description: "..."       # ≤1024 字符，包含触发词和使用场景，双引号包裹
---
```

description 必须包含：
- 做什么（功能描述）
- 什么时候用（触发场景）
- 触发词列表（越多越好，从用户真实对话中采集）

**Layer 2：设计哲学**（推荐）

3-7 条核心原则，每条包含：
- 原则名称
- 来源（哪个参考 skill 或哪次教训）
- 为什么必须遵守

**Layer 3：Phase 工作流**（核心）

按阶段组织，每个 Phase 包含：
- 目标（一句话）
- 铁律（不可违反的约束）
- 步骤（可执行的指令，不是描述）
- 反模式（禁止什么 + 为什么）

**Layer 4：认知框架引用**（按需）

如果技能涉及分析/决策/学习，引用百大认知书籍：
```
| 场景 | 框架 | 书名编号 | 用法 |
```

**Layer 5：参考技能清单**（记录来源）

列出所有融合的参考 skill 和提取的核心机制：
```
| Skill | 融入的机制 |
```

**Layer 6：说话风格 + 禁止模式**

明确语气、格式、绝对禁止的行为。

---

## references/ 文件规范

- 每个 reference 文件 ≤ 200 行
- 超长内容用 Table of Contents
- 从 SKILL.md 直接链接（不嵌套引用）

---

## 目录结构

```
skill-name/
├── SKILL.md          (必须，< 500 行，Progressive Disclosure)
├── _meta.json        (可选，元数据：版本/参考技能/创建日期)
├── INTRODUCTION.md   (可选，面向用户的介绍)
├── references/       (可选，按需加载的详细参考)
│   ├── xxx.md
│   └── yyy.md
├── scripts/          (可选，可执行脚本)
└── assets/           (可选，模板/资源文件)
```

**禁止创建的文件**：README.md / INSTALLATION_GUIDE.md / QUICK_REFERENCE.md / CHANGELOG.md
（skill-creator 铁律：技能只需要 AI agent 做任务的信息）

---

## _meta.json 格式

```json
{
  "name": "skill-name",
  "version": "1.0",
  "created": "YYYY-MM-DD",
  "author": "小黎 & AI",
  "reference_skills": ["skill-1", "skill-2", "..."],
  "ecosystem_connections": {
    "routes": ["r0XX"],
    "memory_files": ["memory/research-profile.md", "..."],
    "related_skills": ["skill-a", "skill-b"]
  },
  "changelog": [
    {"version": "1.0", "date": "YYYY-MM-DD", "changes": "初始创建"}
  ]
}
```

---

## 质量门禁（15 项强制检查）

| # | 检查项 | 通过标准 | 不通过处理 |
|---|--------|---------|-----------|
| 1 | 主文件行数 | ≤ 300 行 | 拆到 references/ |
| 2 | 理论锚点 | ≥ 5 项，每项有来源编号 | 补理论表 |
| 3 | 设计哲学 | ≥ 3 条，每条有反例 | 补反例 |
| 4 | 反模式 | ≥ 5 条，每条有来源 | 补反模式 |
| 5 | 案例库 | ≥ 2 个真实案例（在 references/） | 补案例 |
| 6 | 条件下一步 | ≥ 3 条决策表 | 补决策表 |
| 7 | 联动技能 | ≥ 3 个实质联动（有触发条件+联动方式） | 补联动 |
| 8 | 外部研究 | ≥ 1 个项目（名称+Stars+学到什么） | 搜 GitHub |
| 9 | _meta.json | 存在且有 version/created/reference_skills | 创建 |
| 10 | eval.json | 存在且有 ≥ 5 项断言 | 创建 |
| 11 | golden_rules.md | 存在且有 ≥ 3 条规则 | 补规则 |
| 12 | references/ | 至少 3 个文件且非空 | 补文件 |
| 13 | YAML frontmatter | name + description 齐全 | 补写 |
| 14 | 触发词设计 | ≥ 10 个触发词（同义词+口语+英文） | 扩展 |
| 15 | 费曼检验 | description 一句话说清"做什么" | 重写 |

---

## 评审报告模板（必须输出）

```
## 质量评审报告

| 维度 | 评分(1-5) | 问题 |
|------|----------|------|
| 理论深度 | X | [如有] |
| 实用性 | X | [如有] |
| 生态连接 | X | [如有] |
| 渐进披露 | X | [如有] |
| 参考深度 | X | [如有] |
| 总分 | XX/25 | |

不合格项：[列出需要修复的编号]
处理：[修复后重检 / 直接通过]
```

**评分标准**：
- **25-30 分**：优秀，可以交付
- **20-24 分**：合格，建议迭代 1 轮
- **15-19 分**：不合格，需要迭代 2-3 轮
- **< 15 分**：推倒重来
