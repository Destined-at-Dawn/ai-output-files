# Obsidian 知识库优化方案 · 五位一体 v1.0

> **目标**：让 64 本认知书籍 + 5 个工作区记忆 + 5 个 AI 工具，通过一个 Obsidian vault 互联互通。
> **日期**：2026-06-10
> **适用**：小黎（上海电力大学 · FPGA · 考研 · 内容创作）

---

## 一、现状诊断

### 1.1 你已有的资产

| 资产 | 位置 | 状态 |
|------|------|------|
| **知识中枢 vault** | `E:\ai产出文件\牛马\知识中枢\` | 骨架完整，15 个目录，有仪表盘 |
| **百大认知书籍** | `E:\ai产出文件\牛马\个人\个人\百大认知书籍\` | **64 本书笔记**，172KB 总索引，7 域色标，42 概念聚类，82 子问题映射 |
| **求职工作区记忆** | `求职\求职\memory\` | 最厚：39KB long-term + 16 个日期文件 |
| **创作工作区记忆** | `创作\创作\memory\` | 中等：8.7KB long-term + 8 个日期文件 |
| **个人工作区记忆** | `个人\个人\memory\` | 中等：7.7KB + 6 个专题文件 |
| **Mutual 工作区记忆** | `mutual\mutual\memory\` | 最长跨度：4月19日→6月8日，含聚合 MEMORY.md |
| **日常学习工作区** | `日常学习\日常学习\` | ⚠️ 无 memory 目录 |
| **B站拆解笔记** | `知识中枢\08-创作\B站分享拆解\` | 39 个文件（凯子巨人 33 篇 + AI工具 6 篇） |
| **创作 SOP** | `知识中枢\08-创作\SOP\` | **16 份 SOP**，全 vault 最密集 |
| **共享规则** | `知识中枢\02-共享规则\` | R00-R19 完整编号体系 |
| **工具协同协议** | `知识中枢\02-共享规则\工具协同协议\` | 四位一体总纲 + 4 工具职责规范 |

### 1.2 核心问题（3 个）

**问题 1：两座孤岛**

```
知识中枢 vault                    百大认知书籍
(15 目录, 仪表盘, CSS)            (64 本书, 172KB 索引, 7 域色标)
        ↕ 没有任何桥接 ↕
```

知识中枢的仪表盘导航指向 6 个 MOC，但**没有一个指向百大认知**。CLAUDE.md 里引用了百大认知的路径，但 Obsidian 里看不到。

**问题 2：Obsidian 是空壳**

| 组件 | 状态 | 影响 |
|------|------|------|
| Dataview 插件 | ❌ 未安装 | 无法动态查询笔记 |
| Templater 插件 | ❌ 未安装 | 新笔记没有标准模板 |
| Local REST API | ❌ 9字节占位文件 | AI 工具无法通过 API 访问 vault |
| Obsidian MCP Server | ❌ 未配置 | Claude Desktop 无法直连 vault |
| 书内 wiki-link | ❌ 无 | 64 本书之间无 Obsidian 双向链接 |

**问题 3：5 个 AI 工具各自为战**

- **Marvis**：无法访问知识中枢（没有本地 RAG）
- **Hermes**：记忆写在各工作区 memory/ 里，不流入 vault
- **Claude Desktop**：需要 MCP 才能读写 vault
- **Codex**：只管代码，不知道知识库存在
- **WorkBuddy**：浏览器采集的内容没有流入 vault 的管道

---

## 二、核心方案：四步打通

### Step 1：桥接——百大认知进入 vault（最关键一步）

**方法**：Windows Junction（目录联结）

```cmd
mklink /J "E:\ai产出文件\牛马\知识中枢\11-百大认知" "E:\ai产出文件\牛马\个人\个人\百大认知书籍"
```

**效果**：
- 百大认知的 64 本书 + 索引文件，**原地不动**，以 `11-百大认知/` 出现在 vault 里
- Obsidian 自动索引，双向链接、搜索、图谱全部可用
- 现有引用路径（`.claude/rules/` 里的 `百大认知书籍/010-xxx`）**不需改**
- 百大认知内部已有的 `.cross-domain-index.md`、`.format-standard.md` 等全部保留

**验证**：在 Obsidian 左侧文件树里应看到 `11-百大认知` 目录，展开后有 000-063 的笔记。

**安全**：Junction 不复制文件，删除 Junction 不会删除原文件。

---

### Step 2：插件配置（AI 可操作 vault 的基础设施）

#### 2.1 必装插件（3 个）

| 插件 | 用途 | 安装方式 |
|------|------|---------|
| **Dataview** | 动态查询笔记元数据（标签、字段、日期） | 社区插件搜索 "Dataview" |
| **Templater** | 新笔记自动套模板（书籍笔记、记忆、SOP） | 社区插件搜索 "Templater" |
| **Local REST API** | 让外部 AI 工具通过 HTTP 读写 vault | 社区插件搜索 "Local REST API"（删除现有 9 字节占位文件） |

#### 2.2 安装步骤

1. Obsidian → 设置 → 第三方插件 → 关闭安全模式
2. 浏览社区插件 → 搜索安装上述 3 个
3. 启用后配置：
   - **Dataview**：开启 JavaScript 查询（设置 → Dataview → Enable JavaScript Queries）
   - **Templater**：模板文件夹设为 `_templates/`（稍后创建）
   - **Local REST API**：默认端口 27124，记下 API Key

#### 2.3 可选但推荐

| 插件 | 用途 |
|------|------|
| **Obsidian MCP Server** | Claude Desktop 直连 vault（替代 REST API 方案） |
| **Tag Wrangler** | 批量管理标签 |
| **Calendar** | 日期文件日历视图 |

---

### Step 3：知识增强（让 64 本书真正"活"起来）

#### 3.1 添加 Obsidian frontmatter 到每本书

当前状态：64 本书有详细内容，但**没有 Obsidian frontmatter**（YAML 元数据头）。

需要为每本书添加：

```yaml
---
title: "多巴胺国度"
book_id: "001"
author: "Anna Lembke"
year: 2021
domain: ["D1-脑科学", "D3-习惯行为"]
quality: "A"  # A/B/C 来自 .format-standard.md
tags: [认知书籍, 神经科学, 成瘾医学, 行为设计]
个人耦合度: 5
---
```

**作用**：Dataview 可以按域、质量、耦合度动态查询。

#### 3.2 添加双向 wiki-link

当前：书内概念以纯文本引用（如"009-认知天性"）。
需要改为 Obsidian wiki-link：`[[009-认知天性-Make-It-Stick|认知天性]]`。

**影响范围**：64 本书 + `.cross-domain-index.md` + 总索引。

#### 3.3 创建模板目录

```
知识中枢/_templates/
├── tpl-书籍笔记.md     # 新书笔记模板
├── tpl-每日记忆.md     # 工作区每日记忆模板
├── tpl-SOP.md          # SOP 标准模板
└── tpl-网页采集.md     # WorkBuddy 采集模板
```

---

### Step 4：AI 工具对接（五位一体）

#### 4.1 工具职责矩阵（升级版）

| 工具 | 角色 | 对 Obsidian 做什么 | 接入方式 |
|------|------|-------------------|---------|
| **Marvis**（腾讯） | 🔧 系统+知识管家 | ① 构建本地 RAG（64 本书 + SOP）② 维护双向链接 ③ 自动标签 ④ 每日记忆同步 | 文件直读 + 本地知识库 |
| **Claude Desktop** | 🧠 深度分析+创作 | ① 读书笔记升级（Level B→A）② 概念交叉引用 ③ SOP 生成 | MCP Server 或 REST API |
| **Hermes** | 🗂️ 记忆+知识检索 | ① 记忆写入 vault ② 跨工作区知识搜索 ③ 过期记忆清理 | REST API |
| **Codex** | ⚙️ 代码+自动化 | ① Dataview 查询脚本 ② 批量 frontmatter 注入 ③ 同步脚本 | 文件读写 |
| **WorkBuddy** | 🌐 信息采集 | ① 网页→vault 笔记 ② B 站视频→拆解笔记 ③ 论文→知识卡片 | REST API |

#### 4.2 接入架构

```
                        ┌─────────────────────┐
                        │   Obsidian Vault     │
                        │  (知识中枢 + 11-百大) │
                        │  ┌───────────────┐   │
                        │  │ Local REST API │   │ ← HTTP :27124
                        │  │    插件        │   │
                        │  └───────┬───────┘   │
                        └──────────┼───────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
             ┌──────┴──────┐ ┌────┴────┐ ┌───────┴──────┐
             │ Claude      │ │ Hermes  │ │ WorkBuddy    │
             │ Desktop     │ │         │ │              │
             │ (MCP/REST)  │ │ (REST)  │ │ (REST)       │
             └─────────────┘ └─────────┘ └──────────────┘
                    │
        ┌───────────┼───────────┐
        │                       │
 ┌──────┴──────┐         ┌─────┴─────┐
 │ Marvis      │         │ Codex     │
 │ (文件直读   │         │ (文件读写  │
 │  + 本地RAG) │         │  + 脚本)  │
 └─────────────┘         └───────────┘
```

#### 4.3 Marvis 接入详情

Marvis 安装后第一件事：

1. **添加 vault 为本地知识库目录**
   - 路径：`E:\ai产出文件\牛马\知识中枢\`
   - 包含子目录：全部（含 Junction 进来的 11-百大认知）

2. **构建 RAG 索引**
   - 索引范围：64 本书笔记 + 16 份创作 SOP + 6 份求职 SOP + 共享规则
   - 索引粒度：每本书的 §二核心概念 + §四对现在的我 + §六速查索引

3. **日常使用场景**
   - "《深度工作》里的核心概念是什么" → RAG 检索 + 回答
   - "哪些书讲了多巴胺" → 跨书搜索
   - "帮我写一个新的 SOP" → 参考现有 SOP 模板 + 生成

---

## 三、仪表盘升级

当前仪表盘有 6 个 MOC 入口（求职/竞赛/创作/生态/个人/跨工作区），但**缺少百大认知**。

### 新增入口

```markdown
### 🧠 [[MOC-百大认知|百大认知]] — 64本书 · 7域 · 42概念
> 认知科学工具箱：脑科学、学习科学、习惯系统、专注力、系统思维、社会认知、人生哲学

- [[000-总索引-Index|总索引]] · [[.cross-domain-index|跨域索引]] · [[.format-standard|格式标准]]
```

### 新增 Dataview 动态区块

```markdown
## 📊 认知书籍统计

### 按质量分级
\```dataview
TABLE length AS "数量"
FROM "11-百大认知"
WHERE file.name != "000-总索引-Index"
GROUP BY quality
\```

### 最近更新
\```dataview
TABLE title, domain, quality
FROM "11-百大认知"
SORT file.mtime DESC
LIMIT 10
\```

### 高耦合度书籍（⭐⭐⭐⭐⭐）
\```dataview
TABLE title, domain
FROM "11-百大认知"
WHERE 个人耦合度 = 5
SORT file.name ASC
\```
```

---

## 四、Marvis 即时行动清单

安装 Marvis 后，按以下顺序执行（每步预计 5-15 分钟）：

### P0：桥接 + 知识库（今天做）

| # | 任务 | 命令/操作 | 预计耗时 |
|---|------|---------|---------|
| 1 | 创建 Junction | `mklink /J "知识中枢\11-百大认知" "个人\个人\百大认知书籍"` | 1 分钟 |
| 2 | 验证 Junction | 在 Obsidian 里打开 vault，确认 `11-百大认知` 可见 | 1 分钟 |
| 3 | 安装 Dataview | Obsidian → 社区插件 → 搜索安装 | 3 分钟 |
| 4 | 安装 Templater | 同上 | 3 分钟 |
| 5 | 安装 Local REST API | 同上（删除现有 9 字节占位文件） | 3 分钟 |
| 6 | 创建 vault 知识库 | Marvin → 添加本地目录 → `E:\ai产出文件\牛马\知识中枢\` | 5 分钟 |

### P1：知识增强（本周做）

| # | 任务 | 执行者 | 预计耗时 |
|---|------|--------|---------|
| 7 | 为 64 本书添加 frontmatter | Marvis/Codex | 30 分钟（批量脚本） |
| 8 | 创建 _templates/ 目录和 4 个模板 | Marvis | 15 分钟 |
| 9 | 更新仪表盘（新增百大认知入口） | Marvis | 10 分钟 |
| 10 | 测试 RAG 查询（问一个跨书问题） | Marvis | 5 分钟 |

### P2：工具对接（本月做）

| # | 任务 | 执行者 | 预计耗时 |
|---|------|--------|---------|
| 11 | Claude Desktop 配置 MCP Server | Marvis | 15 分钟 |
| 12 | Hermes 记忆同步脚本 | Codex | 30 分钟 |
| 13 | WorkBuddy 网页采集模板 | Marvis | 15 分钟 |
| 14 | Codex frontmatter 批量注入脚本 | Codex | 30 分钟 |

---

## 五、安全与风险

| 风险 | 概率 | 缓解 |
|------|------|------|
| Junction 导致 Obsidian 索引变慢 | 低 | 64 本书体量小（总计 <2MB），影响可忽略 |
| 多工具同时写 vault 导致冲突 | 中 | Local REST API 支持锁机制；写入走队列 |
| frontmatter 批量注入破坏现有内容 | 低 | 只在文件头追加 YAML，不动正文；先 backup |
| 百大认知原路径引用失效 | 极低 | Junction 保持原路径可用，不改任何已有引用 |

---

## 六、与前次方案的关系

本方案是「五位一体协同优化方案 v2.0」的**子模块深化**：
- v2.0 定义了 5 个工具的职责和进场协议
- **本方案**具体解决"知识库怎么建"的问题——把 Obsidian 从空壳变成五位一体的中枢

| v2.0 方案 | 本方案 |
|-----------|--------|
| Marvis 构建本地知识库 | **具体**：哪些目录入 RAG，索引粒度是什么 |
| Claude Desktop 替代 Newmax | **具体**：通过 MCP Server 还是 REST API 接入 vault |
| 五位一体进场协议 | **具体**：各工具对 vault 的读写权限和操作边界 |

---

## 附录 A：frontmatter 批量注入脚本

> 以下脚本由 Codex 或 Marvis 执行，为 64 本书添加 YAML 元数据头。

```python
import os, re, json

VAULT = r"E:\ai产出文件\牛马\个人\个人\百大认知书籍"
# 从 .format-standard.md 提取的分级
LEVEL_A = [29, 37, 41, 44, 45, 46, 47, 50, 51, 52, 57, 60, 62]
LEVEL_B = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 25, 26, 28]
LEVEL_C = [23, 24, 27, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40, 42, 43, 48, 49, 53, 54, 55, 56, 58, 59, 61]

DOMAIN_MAP = {
    "001": "D1", "002": "D7", "003": "D5", "004": "D6",
    "005": "D4", "006": "D3", "007": "D4", "008": "D2",
    # ... 需要从 .cross-domain-index.md 完整映射
}

def get_quality(book_num):
    if book_num in LEVEL_A: return "A"
    if book_num in LEVEL_B: return "B"
    return "C"

def inject_frontmatter(filepath, book_id, title):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 跳过已有 frontmatter
    if content.startswith('---'):
        print(f"SKIP (已有frontmatter): {filepath}")
        return

    book_num = int(book_id)
    quality = get_quality(book_num)

    frontmatter = f"""---
title: "{title}"
book_id: "{book_id}"
quality: "{quality}"
tags: [认知书籍]
---
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)

    print(f"OK: {book_id}-{title} (质量={quality})")

# 遍历所有书籍文件
for fname in sorted(os.listdir(VAULT)):
    if re.match(r'^\d{3}-.+\.md$', fname):
        book_id = fname[:3]
        title = fname[4:-3]  # 去掉编号前缀和 .md 后缀
        inject_frontmatter(os.path.join(VAULT, fname), book_id, title)
```

> ⚠️ 此脚本仅追加 YAML 头，不动正文。执行前先 `git commit` 检查点。
> ⚠️ DOMAIN_MAP 需要从 `.cross-domain-index.md` 完整提取后补充。

---

## 附录 B：Obsidian 模板文件

### tpl-书籍笔记.md

```markdown
---
title: "{{title}}"
book_id: "{{id}}"
author: ""
year: 
domain: []
quality: ""
tags: [认知书籍]
个人耦合度: 
created: <% tp.date.now("YYYY-MM-DD") %>
---

# {{title}}

## 一、著作科学定位


## 二、核心概念

### 概念 1：
**原句：**
**解读：**
**个人应用：**

## 三、核心金句

1. **""**

## 四、对现在的我

### 当前诊断
小黎，

### SOP 1：
**痛点：**
**机制：**
**行动：**

## 五、对未来的我

### 道（底层认知）

### 法（原则策略）

### 术（方法技巧）

| 领域 | 策略 | 具体执行 |
|------|------|---------|
|      |      |         |

### 器（工具资源）

### 成长四维评估

| 维度 | 短期影响（1-2年） | 长期影响（5-10年） |
|------|-------------------|-------------------|
| 钱 | | |
| 影响力 | | |
| 关系 | | |
| 技能 | | |

### 终极破局

## 六、速查索引

| 场景 | 对应概念 | 立即行动 |
|------|---------|---------|
|      |         |         |

## 七、与其他书籍的交叉耦合
```

### tpl-每日记忆.md

```markdown
---
created: <% tp.date.now("YYYY-MM-DD") %>
workspace: ""
tags: [每日记忆]
---

# <% tp.date.now("YYYY-MM-DD") %> · <% tp.date.now("dddd") %>

## 任务完成情况


## 关键决策


## 新增教训


## 待跟进事项

- [ ]
```

---

> 最后更新：2026-06-10
> 关联：五位一体协同优化方案 v2.0 · CLAUDE.md · 知识中枢 vault
