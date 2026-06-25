# Obsidian Vault 文件分类系统 · 优化方案 v2.1

> **创建日期**：2026-06-01
> **来源**：模仿 `创作区/outputs/b站分享拆解` 的 5 组颜色+大小+索引系统，进一步多维度优化
> **适用 Vault**：百大认知书籍（62本书 + 索引 + 映射表）
> **设计原则**：「多维度正交分类」——每一维独立变化，组合产生丰富的信息层次

---

## 零、源系统分析（b站分享拆解 · v1 系统）

### 源系统的三层架构

```
┌─────────────────────────────────────────────┐
│  1. 文件夹编号（大小/优先级）                    │
│  00-Inbox → 01-Research → ... → 99-Archive   │
│  数字越小 = 越活跃/越重要                       │
├─────────────────────────────────────────────┤
│  2. 图谱颜色分组（5 组）                        │
│  path:凯子巨人 → 橙红 | tag:#索引 → 金色       │
│  path:AI与工具 → 蓝色 | tag:#数学方法论 → 暖橙  │
├─────────────────────────────────────────────┤
│  3. 索引文件（00-总索引.md）                    │
│  YAML frontmatter + Wiki-link + ASCII 树      │
└─────────────────────────────────────────────┘
```

### 源系统的局限（v1 → v2 的优化点）

| 局限 | v1 表现 | v2 改进 |
|------|---------|---------|
| 颜色维度单一 | 只有 path + tag 两组查询 | 增加**认知领域、加工深度、引用频率**三维 |
| 节点大小无区分 | nodeSizeMultiplier=1.2 全局统一 | 用 **tag 权重**模拟节点大小差异 |
| 无文件浏览器着色 | 仅图谱有颜色，文件列表无视觉提示 | **CSS snippet** 按领域着色文件浏览器 |
| 索引无颜色图例 | 总索引纯文字，无视觉导航 | 索引嵌入**颜色图例 + 视觉导航** |
| 颜色无语义体系 | 橙红/蓝/金/暖橙/青蓝 随机搭配 | **语义化调色板**：红=认知、蓝=生产力、绿=习惯... |
| 无连边粗细分层 | lineSizeMultiplier=2.2 全局统一 | **按关系类型**分层（同领域粗线、跨领域细线） |

---

## 一、优化系统总览（v2 四层架构）

```
┌──────────────────────────────────────────────────┐
│  Layer 1: 文件夹编号（大小/活跃度）                   │
│  沿用 v1 编号体系，适用于「小黎 Obsidian Vault 模板」   │
├──────────────────────────────────────────────────┤
│  Layer 2: 图谱颜色分组（多维度）                      │
│  维度A: 认知领域（7色）→ 主色                        │
│  维度B: 引用频率（3级饱和度）→ 节点深浅                │
│  维度C: 加工状态（3种边框）→ 节点描边                  │
├──────────────────────────────────────────────────┤
│  Layer 3: 节点大小与连线（信息权重）                   │
│  引用次数 → 节点半径 | 关系类型 → 连线粗细             │
├──────────────────────────────────────────────────┤
│  Layer 4: 索引系统（视觉导航）                        │
│  颜色图例 + 领域MOC + 阅读路线 + 交叉引用热力图         │
└──────────────────────────────────────────────────┘
```

---

## 二、Layer 1：文件夹编号体系（大小/优先级）

> 与 v1 系统一致，用于「小黎的 Obsidian Vault 模板」。百大认知书籍为扁平结构，不需要此层。

| 编号 | 文件夹 | 含义 | 节点大小隐喻 |
|------|--------|------|-------------|
| `00-` | Inbox | 临时入口，待分类 | 最小节点 |
| `01-` | Research | 核心研究（知识生产） | 最大节点 |
| `02-` | Internship | 实习（经验积累） | 大节点 |
| `03-` | EE-AI | 专业领域（硬技能） | 大节点 |
| `04-` | Courses | 课程（系统学习） | 中节点 |
| `05-` | Content | 内容创作（输出） | 中节点 |
| `06-` | People | 人脉（关系网络） | 小节点 |
| `07-` | Journal | 日志（时间流） | 小节点 |
| `99-` | Archive | 归档（沉寂） | 最小节点 |

**原理**：编号 = 信息活跃度的降序排列。`00` = 信息刚进入系统，`01` = 正在被活跃加工，`99` = 已完成生命周期。

---

## 三、Layer 2：图谱颜色分组（多维度正交）

### 3.1 维度A：认知领域（7 色语义调色板）

> 62 本书 → 7 大领域。颜色选择遵循**语义隐喻**：红色 = 认知（热思考）、蓝色 = 生产力（冷静效率）、绿色 = 习惯（生长）、紫色 = 神经科学（神秘）、金色 = 哲学（智慧）、橙色 = 社会（人间烟火）、青色 = 经济决策（理性计算）

| # | 领域 | 色名 | Hex | RGB | 隐喻 | 书籍数 |
|---|------|------|-----|-----|------|--------|
| 1 | 🧠 认知科学与学习 | 暖红 | `#E74C3C` | `15152624` | 热思考·知识燃烧 | ~12本 |
| 2 | ⚡ 生产力与效能 | 电蓝 | `#2980B9` | `2724025` | 冷静效率·工程化 | ~10本 |
| 3 | 🌱 习惯与行为改变 | 森林绿 | `#27AE60` | `2596448` | 生长·重塑 | ~8本 |
| 4 | 🔬 神经科学与脑科学 | 星空紫 | `#8E44AD` | `9323693` | 神秘·硬件层 | ~8本 |
| 5 | 💭 哲学与思维 | 智慧金 | `#F39C12` | `15957522` | 智慧·框架层 | ~8本 |
| 6 | 🌐 社会与关系 | 人间橙 | `#E67E22` | `15105570` | 人间烟火·关系网 | ~10本 |
| 7 | 📊 经济与决策 | 理性青 | `#1ABC9C` | `1751724` | 理性计算·博弈 | ~6本 |
| 8 | ⭐ 索引/元数据 | 索引金 | `#FFD700` | `16766720` | 导航·枢纽 | 3个文件 |

### 3.2 维度B：引用频率（饱和度三级）

> 同一领域内，用**饱和度**区分引用热度。高引用 = 高饱和（鲜艳），低引用 = 低饱和（灰淡）。
> 实现方式：在高/中频书籍的 frontmatter 加 `citation_level: high|mid|low` 标签。

| 层级 | 标签 | 饱和度 | 效果 | 书籍数 |
|------|------|--------|------|--------|
| 高频引用 | `tag:#citation/high` | 100% | 鲜艳突出 | ~15本 |
| 中频引用 | `tag:#citation/mid` | 65% | 正常可见 | ~20本 |
| 低频/未引用 | `tag:#citation/low` | 35% | 背景淡化 | ~27本 |

**颜色值计算**（以认知科学暖红 `#E74C3C` 为例）：

| 层级 | Hex | RGB | 效果 |
|------|-----|-----|------|
| High | `#E74C3C` | `15152624` | 🔴 鲜艳红 |
| Mid | `#C0392B` | `12605995` | 🔴 暗红 |
| Low | `#996666` | `10053222` | 🔴 灰红 |

### 3.3 维度C：加工状态（3 种视觉标记）

| 状态 | Frontmatter 标签 | 建议视觉处理 |
|------|-----------------|-------------|
| 🌱 种子（待读） | `status: seedling` | 小节点 + 低饱和度 |
| 🌿 萌芽（已读+有笔记） | `status: budding` | 中节点 + 中饱和度 |
| 🌳 常青（深度加工+多引用） | `status: evergreen` | 大节点 + 高饱和度 |

---

## 四、Layer 3：节点大小与连线系统

### 4.1 节点大小策略

> graph.json 的 `nodeSizeMultiplier` 是全局参数。真正的差异化节点大小需要通过**标签权重**来模拟。

**推荐配置**：
```json
{
  "nodeSizeMultiplier": 1.5,
  "lineSizeMultiplier": 2.5,
  "linkDistance": 280,
  "repelStrength": 12,
  "centerStrength": 0.45,
  "linkStrength": 0.8
}
```

**原理说明**：
- `nodeSizeMultiplier: 1.5`（v1 是 1.2）→ 整体更大，层次更分明
- `lineSizeMultiplier: 2.5`（v1 是 2.2）→ 连线更粗，关系更明显
- `linkDistance: 280`（v1 是 250）→ 节点间距更大，减少重叠
- `repelStrength: 12`（v1 是 10）→ 更强的排斥力，图谱更展开
- `centerStrength: 0.45`（v1 是 0.52）→ 核心节点更居中但仍保留展开

### 4.2 全局图谱参数对比

| 参数 | v1 (b站拆解) | v2 (百大认知) | 变化 | 效果 |
|------|-------------|--------------|------|------|
| nodeSizeMultiplier | 1.2 | 1.5 | +25% | 节点更大，区分度更高 |
| lineSizeMultiplier | 2.2 | 2.5 | +14% | 连线更清晰 |
| linkDistance | 250 | 280 | +12% | 62本书不拥挤 |
| repelStrength | 10 | 12 | +20% | 图谱更展开 |
| centerStrength | 0.52 | 0.45 | -13% | 枢纽节点居中但不紧 |
| linkStrength | 1.0 | 0.8 | -20% | 连线更自然舒展 |

### 4.3 连线颜色与粗细

| 连线类型 | 粗细 | 颜色逻辑 |
|---------|------|---------|
| 同领域内引用 | 粗 | 该领域的主题色 |
| 跨领域引用 | 中 | 两种领域色的中间色 |
| 索引→书籍 | 细 | 灰色 `#999999` |
| 双向强关联 | 最粗 | 暖色高亮 |

---

## 五、Layer 4：索引系统增强

### 5.1 颜色图例嵌入索引

在 `000-总索引-Index.md` 头部新增可视化导航区：

```markdown
## 🗺️ 视觉导航

| 颜色 | 领域 | 核心书籍 |
|------|------|---------|
| 🔴 暖红 | 认知科学与学习 | 009-认知天性、010-思考快与慢、017-刻意练习 |
| 🔵 电蓝 | 生产力与效能 | 005-深度工作、007-搞定、013-精要主义 |
| 🟢 森林绿 | 习惯与行为改变 | 006-原子习惯、016-习惯的力量、014-心态 |
| 🟣 星空紫 | 神经科学与脑科学 | 001-多巴胺国度、022-认知神经科学、031-活体连线 |
| 🟡 智慧金 | 哲学与思维 | 003-框架的胜利、012-心流、024-心智探奇 |
| 🟠 人间橙 | 社会与关系 | 004-金榜题名之后、029-沧浪之水、035-权力 |
| 🔷 理性青 | 经济与决策 | 027-以日为鉴、034-现在做还是以后做 |
| ⭐ 索引金 | 导航/元数据 | 000-总索引、问题拆解映射表 |
```

### 5.2 推荐阅读路线（彩色标注）

```markdown
## 🧭 阅读路线（按颜色导航）

### 路线 1：学习效率革命 🔴→🔵→🟣
009-认知天性 → 017-刻意练习 → 025-认知负荷理论 → 028-我们如何学习

### 路线 2：习惯重塑 🟢→🔴→🟣
006-原子习惯 → 016-习惯的力量 → 001-多巴胺国度 → 021-执行功能

### 路线 3：社会认知升级 🟠→🟡→🟠
004-金榜题名之后 → 030-不平等的童年 → 035-权力 → 029-沧浪之水

### 路线 4：生产力系统 🔵→🔵→🔵
007-搞定 → 005-深度工作 → 013-精要主义 → 019-敏捷革命

### 路线 5：认知底层 🟣→🟣→🔴
022-认知神经科学 → 031-活体连线 → 026-笛卡尔的错误 → 010-思考快与慢
```

### 5.3 交叉引用热力图（Mermaid）

在总索引中加入领域交叉热力矩阵，一眼看出哪些书跨领域最多（= 信息枢纽）：

|  | 🔴认知 | 🔵效能 | 🟢习惯 | 🟣神经 | 🟡哲学 | 🟠社会 | 🔷决策 |
|--|--------|--------|--------|--------|--------|--------|--------|
| 🔴认知 | - | 多 | 中 | 多 | 中 | 少 | 少 |
| 🔵效能 | 多 | - | 中 | 少 | 少 | 少 | 中 |
| 🟢习惯 | 中 | 中 | - | 多 | 少 | 少 | 少 |
| 🟣神经 | 多 | 少 | 多 | - | 中 | 少 | 少 |
| 🟡哲学 | 中 | 少 | 少 | 中 | - | 中 | 少 |
| 🟠社会 | 少 | 少 | 少 | 少 | 中 | - | 中 |
| 🔷决策 | 少 | 中 | 少 | 少 | 少 | 中 | - |

---

## 六、CSS Snippet：文件浏览器着色

### 6.1 文件夹颜色

建议最终放入 Obsidian 的 snippets 目录中使用；当前仓库内已导出模板文件 `file-colors.css`，为 7 大领域的书籍文件添加颜色标记。

**原理**：Obsidian 的 CSS 可以通过 `data-path` 属性匹配文件名模式。对于 `001-009` 等编号范围，用 CSS 属性选择器批量着色。

```css
/* ===== 百大认知书籍 · 文件浏览器着色 ===== */

/* 认知科学与学习 — 暖红左边框 */
.nav-file-title[data-path*="009-认知天性"],
.nav-file-title[data-path*="010-思考快与慢"],
.nav-file-title[data-path*="017-刻意练习"],
.nav-file-title[data-path*="021-执行功能"],
.nav-file-title[data-path*="025-认知负荷理论"],
.nav-file-title[data-path*="028-我们如何学习"] {
  border-left: 3px solid #E74C3C;
}

/* 生产力与效能 — 电蓝左边框 */
.nav-file-title[data-path*="005-深度工作"],
.nav-file-title[data-path*="007-搞定"],
.nav-file-title[data-path*="013-精要主义"],
.nav-file-title[data-path*="019-敏捷革命"],
.nav-file-title[data-path*="018-算法之美"] {
  border-left: 3px solid #2980B9;
}

/* 习惯与行为改变 — 森林绿左边框 */
.nav-file-title[data-path*="006-原子习惯"],
.nav-file-title[data-path*="014-心态"],
.nav-file-title[data-path*="015-吃掉那只青蛙"],
.nav-file-title[data-path*="016-习惯的力量"],
.nav-file-title[data-path*="020-专注力管理"] {
  border-left: 3px solid #27AE60;
}

/* 神经科学与脑科学 — 星空紫左边框 */
.nav-file-title[data-path*="001-多巴胺国度"],
.nav-file-title[data-path*="022-认知神经科学"],
.nav-file-title[data-path*="026-笛卡尔的错误"],
.nav-file-title[data-path*="031-活体连线"],
.nav-file-title[data-path*="032-白板"] {
  border-left: 3px solid #8E44AD;
}

/* 哲学与思维 — 智慧金左边框 */
.nav-file-title[data-path*="003-框架的胜利"],
.nav-file-title[data-path*="012-心流"],
.nav-file-title[data-path*="024-心智探奇"] {
  border-left: 3px solid #F39C12;
}

/* 社会与关系 — 人间橙左边框 */
.nav-file-title[data-path*="004-金榜题名之后"],
.nav-file-title[data-path*="029-沧浪之水"],
.nav-file-title[data-path*="030-不平等的童年"],
.nav-file-title[data-path*="033-中国社会的个体化"],
.nav-file-title[data-path*="035-权力"],
.nav-file-title[data-path*="036-私人生活的变革"] {
  border-left: 3px solid #E67E22;
}

/* 经济与决策 — 理性青左边框 */
.nav-file-title[data-path*="027-以日为鉴"],
.nav-file-title[data-path*="034-现在做还是以后做"] {
  border-left: 3px solid #1ABC9C;
}

/* 索引/元数据 — 金色左边框 */
.nav-file-title[data-path*="000-总索引"],
.nav-file-title[data-path*="问题拆解-书籍映射"] {
  border-left: 3px solid #FFD700;
}

/* ===== 节点状态标记 ===== */

/* 高频引用 — 加粗文件名 */
.nav-file-title[data-tag*="citation/high"] .nav-file-title-content {
  font-weight: 700;
}

/* 种子状态 — 斜体 */
.nav-file-title[data-tag*="status/seedling"] .nav-file-title-content {
  font-style: italic;
  opacity: 0.6;
}

/* 常青状态 — 加粗 + 高亮 */
.nav-file-title[data-tag*="status/evergreen"] .nav-file-title-content {
  font-weight: 700;
  background: linear-gradient(90deg, transparent, rgba(255,215,0,0.15));
}
```

### 6.2 启用 CSS Snippet

1. 将上面的 CSS 保存到 `file-colors.css`
2. 将其手动放入 Obsidian 的 snippets 目录后启用；当前仓库内已导出模板文件 `file-colors.css`

---

## 七、graph.json 优化配置

### 7.1 完整配置（15 个颜色分组）

```json
{
  "collapse-filter": true,
  "search": "",
  "showTags": true,
  "showAttachments": false,
  "hideUnresolved": false,
  "showOrphans": true,
  "collapse-color-groups": false,
  "colorGroups": [
    {
      "query": "tag:#domain/认知科学",
      "color": {"a": 1, "rgb": 15152624}
    },
    {
      "query": "tag:#domain/生产力效能",
      "color": {"a": 1, "rgb": 2724025}
    },
    {
      "query": "tag:#domain/习惯行为",
      "color": {"a": 1, "rgb": 2596448}
    },
    {
      "query": "tag:#domain/神经科学",
      "color": {"a": 1, "rgb": 9323693}
    },
    {
      "query": "tag:#domain/哲学思维",
      "color": {"a": 1, "rgb": 15957522}
    },
    {
      "query": "tag:#domain/社会关系",
      "color": {"a": 1, "rgb": 15105570}
    },
    {
      "query": "tag:#domain/经济决策",
      "color": {"a": 1, "rgb": 1751724}
    },
    {
      "query": "tag:#索引",
      "color": {"a": 1, "rgb": 16766720}
    },
    {
      "query": "tag:#citation/high",
      "color": {"a": 1, "rgb": 16737894}
    },
    {
      "query": "tag:#citation/mid",
      "color": {"a": 1, "rgb": 16764006}
    },
    {
      "query": "tag:#citation/low",
      "color": {"a": 1, "rgb": 12895428}
    },
    {
      "query": "tag:#status/evergreen",
      "color": {"a": 1, "rgb": 39168}
    },
    {
      "query": "tag:#status/budding",
      "color": {"a": 1, "rgb": 10079232}
    },
    {
      "query": "tag:#status/seedling",
      "color": {"a": 1, "rgb": 12632256}
    },
    {
      "query": "tag:#小黎场景",
      "color": {"a": 1, "rgb": 16753152}
    }
  ],
  "collapse-display": false,
  "showArrow": true,
  "textFadeMultiplier": -0.5,
  "nodeSizeMultiplier": 1.5,
  "lineSizeMultiplier": 2.5,
  "collapse-forces": false,
  "centerStrength": 0.45,
  "repelStrength": 12,
  "linkStrength": 0.8,
  "linkDistance": 280,
  "scale": 0.85,
  "close": true
}
```

### 7.2 颜色分组完整对照表

| # | 查询 | 色名 | Hex | RGB | 对应内容 |
|---|------|------|-----|-----|---------|
| 1 | `tag:#domain/认知科学` | 暖红 | `#E74C3C` | `15152624` | 12本：009,010,017,021,025,028... |
| 2 | `tag:#domain/生产力效能` | 电蓝 | `#2980B9` | `2724025` | 10本：005,007,013,018,019... |
| 3 | `tag:#domain/习惯行为` | 森林绿 | `#27AE60` | `2596448` | 8本：006,014,015,016,020... |
| 4 | `tag:#domain/神经科学` | 星空紫 | `#8E44AD` | `9323693` | 8本：001,022,026,031,032... |
| 5 | `tag:#domain/哲学思维` | 智慧金 | `#F39C12` | `15957522` | 8本：003,012,024... |
| 6 | `tag:#domain/社会关系` | 人间橙 | `#E67E22` | `15105570` | 10本：004,029,030,033,035,036... |
| 7 | `tag:#domain/经济决策` | 理性青 | `#1ABC9C` | `1751724` | 6本：027,034... |
| 8 | `tag:#索引` | 索引金 | `#FFD700` | `16766720` | 3个：000, 问题拆解, cross-ref |
| 9 | `tag:#citation/high` | 高频红 | `#FF6600` | `16737894` | 高引用标记 |
| 10 | `tag:#citation/mid` | 中频橙 | `#FFB826` | `16764006` | 中引用标记 |
| 11 | `tag:#citation/low` | 低频灰 | `#C4C4C4` | `12895428` | 低引用标记 |
| 12 | `tag:#status/evergreen` | 常青绿 | `#009900` | `39168` | 深度加工 |
| 13 | `tag:#status/budding` | 萌芽黄绿 | `#99CC00` | `10079232` | 已有笔记 |
| 14 | `tag:#status/seedling` | 种子灰绿 | `#C0C0C0` | `12632256` | 待阅读 |
| 15 | `tag:#小黎场景` | 场景粉 | `#FFA500` | `16753152` | 40个小黎场景标记 |

### 7.3 v1 → v2 变更对照

| 参数 | v1 (b站拆解) | v2 (百大认知) | 优化原因 |
|------|-------------|--------------|---------|
| colorGroups | 5 组 | 15 组 | 三维正交（领域×引用×状态） |
| collapse-color-groups | false | false | 保持展开，所有颜色可见 |
| showTags | false | true | 图谱节点上显示标签 |
| showArrow | true | true | 保留方向箭头 |
| textFadeMultiplier | 0 | -0.5 | 非焦点文字淡出，突出核心 |
| nodeSizeMultiplier | 1.2 | 1.5 | 62本书需要更大区分度 |
| lineSizeMultiplier | 2.2 | 2.5 | 连线更清晰 |
| linkDistance | 250 | 280 | 62本书需要更大间距 |
| repelStrength | 10 | 12 | 更展开 |
| centerStrength | 0.52 | 0.45 | 枢纽居中但不过紧 |
| linkStrength | 1.0 | 0.8 | 连线自然舒展 |
| collapse-forces | true | false | 保持力导向持续运算 |

---

## 八、Frontmatter 标准化规范

### 8.1 每本书的 YAML 前置属性

```yaml
---
tags:
  - 百大认知书籍
  - domain/{认知科学|生产力效能|习惯行为|神经科学|哲学思维|社会关系|经济决策}
  - citation/{high|mid|low}
  - status/{evergreen|budding|seedling}
author: 作者名
year: 出版年份
domain: 认知科学
citation_count: 12
status: evergreen
personal_relevance: ⭐⭐⭐⭐⭐
---
```

### 8.2 批量打标签脚本（Python）

```python
"""为 62 本书批量添加领域 frontmatter 标签"""
import os
import re

VAULT = r"E:\ai产出文件\牛马\个人\个人\projects\20260504-数字先知升级\outputs\百大认知书籍"

# 领域映射表（书籍编号 → 领域标签）
DOMAIN_MAP = {
    # 神经科学与脑科学
    "001": "domain/神经科学", "022": "domain/神经科学",
    "026": "domain/神经科学", "031": "domain/神经科学",
    "032": "domain/神经科学",
    # 认知科学与学习
    "009": "domain/认知科学", "010": "domain/认知科学",
    "017": "domain/认知科学", "021": "domain/认知科学",
    "025": "domain/认知科学", "028": "domain/认知科学",
    # 习惯与行为改变
    "006": "domain/习惯行为", "014": "domain/习惯行为",
    "015": "domain/习惯行为", "016": "domain/习惯行为",
    "020": "domain/习惯行为", "034": "domain/习惯行为",
    # 生产力与效能
    "005": "domain/生产力效能", "007": "domain/生产力效能",
    "013": "domain/生产力效能", "018": "domain/生产力效能",
    "019": "domain/生产力效能",
    # 哲学与思维
    "003": "domain/哲学思维", "012": "domain/哲学思维",
    "024": "domain/哲学思维",
    # 社会与关系
    "002": "domain/社会关系", "004": "domain/社会关系",
    "008": "domain/社会关系", "029": "domain/社会关系",
    "030": "domain/社会关系", "033": "domain/社会关系",
    "035": "domain/社会关系", "036": "domain/社会关系",
    # 经济与决策
    "027": "domain/经济决策",
}

def add_domain_tag(filepath, domain_tag):
    """在已有 tags 列表末尾追加领域标签"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 在 tags 列表末尾追加（YAML frontmatter 内）
    pattern = r'(tags:\n(?:  - .+\n)*)'
    replacement = rf'\1  - {domain_tag}\n'
    new_content = re.sub(pattern, replacement, content, count=1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

# 批量执行
for fname in os.listdir(VAULT):
    match = re.match(r'^(\d{3})-', fname)
    if match and match.group(1) in DOMAIN_MAP:
        filepath = os.path.join(VAULT, fname)
        domain = DOMAIN_MAP[match.group(1)]
        add_domain_tag(filepath, domain)
        print(f"✅ {fname} → {domain}")
```

---

## 九、v1 与 v2 系统对比总结

| 维度 | v1 (b站拆解) | v2 (百大认知·优化) | 提升 |
|------|-------------|-------------------|------|
| 颜色分组数 | 5 组 | 15 组 | **3×** |
| 颜色维度 | 1 维（路径+标签） | 3 维（领域+引用+状态） | **正交化** |
| 语义调色板 | 无体系 | 7 色语义隐喻 | **认知友好** |
| 节点大小 | 全局统一 1.2 | 1.5 + 标签权重 | **有层次** |
| 连线粗细 | 全局统一 2.2 | 2.5 + 关系分级 | **有方向** |
| 文件浏览器着色 | 无 | CSS snippet 左边框 | **新增** |
| 索引视觉导航 | 纯文字 | 颜色图例+阅读路线+Mermaid | **可视化** |
| Frontmatter | 3 个字段 | 6+ 个字段（含领域/引用/状态） | **可查询** |
| 图谱参数 | 基础配置 | 精细调优 10+ 参数 | **更清晰** |

---

## 十、实施路线图

### Phase 1：立即可做（~30 分钟）
- [x] 已导出 `graph.json` 配置模板
- [x] 已导出 `file-colors.css` 模板
- [ ] 手动放入 Obsidian 对应目录并在外观设置中启用 CSS snippet

### Phase 2：核心优化（~2 小时）
- [ ] 为 62 本书批量添加领域 frontmatter 标签（用第八节的 Python 脚本）
- [ ] 手动标注 citation/high 书籍（基于 CITATION_TRACKING.md 数据）
- [x] 已在 `000-总索引-Index.md` 头部添加系统导航与命名说明

### Phase 3：深度优化（按需）
- [ ] 为每本书标注 status（evergreen/budding/seedling）
- [ ] 在 `cross-reference-map.md` 中生成交叉引用热力图
- [ ] 创建领域级别的 MOC（Map of Content）文件
- [ ] 添加 Dataview 查询面板（按领域/状态/引用频率筛选）

---

## 十一、边界声明

### ✅ 可写入材料
- 5 组 → 15 组颜色分组的优化方案（7 领域 × 3 引用频率 + 3 状态 + 1 索引 + 1 场景）
- 语义化调色板（7 色 + 隐喻映射）
- CSS snippet 文件浏览器着色方案
- graph.json 完整优化配置

### ⚠️ 不可写入材料（仅供参考）
- 具体的引用频率数据（需要从 CITATION_TRACKING.md 提取，口径待确认）
- 每本书的领域归属（部分书籍跨越多个领域，需要人工判断）
- CSS 的实际渲染效果（取决于 Obsidian 主题和版本）

### ❓ 尚不能声称
- 颜色选择对认知效率的量化提升（需要 A/B 测试）
- 节点大小差异在图谱中的可感知度（取决于显示器分辨率和图谱缩放级别）

---

> **创建日期**：2026-06-01
> **版本**：v2.1
> **基于**：创作区 b站分享拆解 v1 系统（5 组颜色 + 单维度分类）
> **关联文件**：`graph.json`、`file-colors.css`、`cross-reference-map.md`、`000-总索引-Index.md`
> **相关规则**：百大认知书籍优先 + 均衡引用（R12）
