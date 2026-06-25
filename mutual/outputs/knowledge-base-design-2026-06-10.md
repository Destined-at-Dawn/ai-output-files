# 知识库三层结构设计

> 日期: 2026-06-10
> 方法论: 信息差6 — 知识库用三层结构设计
> 原则: Layer 0（碎片积累）→ Layer 1（知识卡沉淀）→ Layer 2（Skill/SOP执行）

---

## 当前知识分布问题

### 问题1: memory/long-term.md 混合了三种不同性质的内容

| 内容类型 | 举例 | 应属层级 |
|----------|------|----------|
| 用户偏好 | "偏好简洁输出" | Layer 1（持久决策卡） |
| 教训 | "429事故" | Layer 0（待提炼为规则） |
| 知识 | "Karpathy原则" | Layer 1（知识卡） |
| 临时发现 | "某skill路由漏了" | Layer 0（碎片，可过期） |

### 问题2: .claude/rules/ 混合了工程法则和认知科学

| 文件 | 性质 | 应属层级 |
|------|------|----------|
| think-before-act.md | 工程法则 | Layer 2（执行规则） |
| anti-illusion-audit.md | 工程法则+认知科学 | Layer 2 + Layer 1引用 |
| identity-consistency.md | 身份管理 | Layer 1（持久知识卡） |
| preference-memory.md | 偏好管理 | Layer 1（持久知识卡） |
| 10-engineering-laws.md | 工程法则 | Layer 2（执行规则） |

### 问题3: outputs/ 没有分类

| 内容类型 | 举例 | 应属层级 |
|----------|------|----------|
| 调研报告 | "Obsidian知识库优化方案" | Layer 1（知识卡） |
| 分析结果 | "workflow-gap-analysis" | Layer 0→1（待提炼） |
| 代码修复 | "fix-li-intent-visual.py" | Layer 2（执行产物） |

---

## 三层结构设计

```
E:i产出文件\牛马\mutual\mutual├── knowledge-base/              ← 新建
│   ├── layer0-fragments/        ← 碎片层：快速积累，可过期
│   │   ├── README.md            ← 碎片管理规则
│   │   └── {date}-{topic}.md   ← 按日期+主题命名
│   │
│   ├── layer1-cards/            ← 知识卡层：独立文档，可复用
│   │   ├── README.md            ← 知识卡管理规则
│   │   ├── decisions/           ← 持久决策
│   │   │   └── {topic}.md
│   │   ├── patterns/            ← 模式/方法论
│   │   │   └── {pattern}.md
│   │   ├── lessons/             ← 教训（从Layer 0沉淀）
│   │   │   └── {lesson-id}.md
│   │   └── references/          ← 外部知识引用
│   │       └── {source}.md
│   │
│   └── layer2-executable/       ← 可执行层：Skill/SOP/规则
│       ├── README.md            ← 管理规则
│       └── index.md             ← 索引（与SOP总索引合并）
│
├── skills/                      ← 现有（= Layer 2）
├── .claude/rules/               ← 现有（= Layer 2）
├── SOPs/                        ← 现有（= Layer 2）
├── memory/                      ← 现有 → 改造
│   ├── long-term.md             ← 精简为：用户偏好 + 持久决策索引
│   └── {date}.md               ← 保留：每日任务记录
│
└── outputs/                     ← 现有 → 分流
    ├── analyses/                ← 分析产出（可提升到Layer 1）
    └── deliverables/            ← 交付物
```

---

## 迁移计划

### Phase 1: 创建目录结构（立即执行）

1. 创建 `knowledge-base/` 及子目录
2. 创建各层 README.md
3. 创建索引文件

### Phase 2: 分流现有内容（本周内）

1. 读取 memory/long-term.md
2. 将"教训"类内容提取到 layer1-cards/lessons/
3. 将"知识"类内容提取到 layer1-cards/patterns/
4. memory/long-term.md 只保留用户偏好 + 持久决策索引

### Phase 3: 更新路由（下周）

1. li-intent 的 Phase 2（历史上下文注入）增加 knowledge-base/ 查找
2. SOP总索引 引用 layer2-executable/index.md

---

## 碎片管理规则（Layer 0）

- **生命周期**: 30天未被引用 → 标记为"待清理"；90天 → 归档
- **晋升条件**: 被引用 ≥3次 → 提升到 Layer 1
- **命名规则**: `{YYYY-MM-DD}-{3词主题}.md`
- **内容格式**: 碎片 + 来源 + 日期 + 置信度

## 知识卡管理规则（Layer 1）

- **生命周期**: 长期保留，定期审查
- **更新条件**: 发现新信息、用户纠正
- **命名规则**: `{category}-{topic}.md`
- **内容格式**: 结论 + 证据 + 来源 + 置信度 + 失效条件
- **分类**: decisions / patterns / lessons / references

## 可执行层管理规则（Layer 2）

- **生命周期**: 跟随skill/SOP生命周期
- **更新条件**: 路由表变更、skill合并/淘汰
- **管理**: 由li-manage负责
