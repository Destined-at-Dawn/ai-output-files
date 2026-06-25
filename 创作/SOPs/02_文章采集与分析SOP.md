# 02_文章采集与分析SOP

> **工作区**：创作区
> **版本**：v3.0 | **最后更新**：2026-06-09
> **触发条件**：用户发公众号链接 / 说"分析文章/提取全文/品读" / 说"发现热文/搜文章/跑一下公众号"

---

## 〇、全链路概览（v3.0 新增）

```
Step 0: 发现(Discover)  →  Step 1: 提取(Extract)  →  Step 2: 分析(Analyze)  →  Step 3: 融入(Integrate)
    dajiala.com              down.mptext.top          SOP-02 四层读取               SOPs/技能/知识库
```

**这不是可选步骤，是强制管线。** 缺任何一个 Step = 流程未完成。

---

## 一、触发条件

| 触发信号 | 示例 | 优先级 |
|----------|------|--------|
| 公众号文章链接 | 发送 `mp.weixin.qq.com/s/` 链接 | P0 |
| 文章分析需求 | "分析这篇文章/拆解一下/品读" | P0 |
| 文风分析 | "分析文风/文风DNA/风格提取" | P0 |
| **搜索公众号热文（v3.0 新增）** | "搜一下AI相关文章/找热文/跑一下公众号/The Signal/发现好文" | **P0** |
| 批量采集 | "批量抓取/收集一批文章" | P1 |
| 提取全文 | "提取/抓取这篇文章" | P0 |

---

## 二、Step 0：文章发现（dajiala.com）—— v3.0 新增

> **核心原则：发现不是"等用户发链接"，是主动搜索。** 用户说"搜一下/跑一下/找热文"时，先执行发现再提取。

### 2.1 发现工具

**工具**：`outputs/wechat-hot-discovery.py`（v1.0）

```bash
# 使用配置文件搜索
python outputs/wechat-hot-discovery.py --config config.yaml --days 7

# 仅搜索不生成 HTML 报告
python outputs/wechat-hot-discovery.py --config config.yaml --days 7 --no-report
```

**API 来源**：dajiala.com（付费，¥0.40/组关键词）
**评分算法**：Wilson Score + 三维度加权（流量40% + 信任50% + 内容信号10%）
**等级**：S（≥55）/ A（≥35）/ B（≥20）/ 过滤（<20）

### 2.2 配置文件

参考模板：`outputs/wechat-extract-tool/jc-zhuagongzhonghao/assets/config-template.yaml`

```yaml
api:
  key: "你的API_KEY（从dajiala.com获取）"
  url: "https://www.dajiala.com/fbmain/monitor/v3/kw_search"

search:
  sort_type: 1
  mode: 3        # 标题+正文
  period: 7

search_groups:
  - name: "AI工作流"
    kw: "AI工作流"
    ex_kw: "招聘 论文 股票 课程推荐"
```

### 2.3 发现流程

```
用户说"找热文/搜文章"
    ↓
1. 确认关键词 + 费用（mcp__ask-user__ask_user）
2. 运行 wechat-hot-discovery.py
3. 得到评分排序的文章列表 + urls.txt
4. 自动进入 Step 1（提取）
```

### 2.4 费用确认（必须问）

每次发现前，告知用户：
- 搜索几组关键词？（每组 ¥0.40）
- 搜索几天内的？（默认 7 天）
- 有没有排除词？

用户说"可以"或"跑吧"后才能执行。

---

## 三、Step 1：API 提取全文（公众号文章专用）

### 3.1 提取工具

**工具**：`outputs/fetch-wechat-article.py`（v3.0）

```bash
# 单篇提取（JSON + TXT）
python outputs/fetch-wechat-article.py "https://mp.weixin.qq.com/s/xxxxx"

# 仅提取 Markdown
python outputs/fetch-wechat-article.py "https://mp.weixin.qq.com/s/xxxxx" --format md

# 提取 + 自动生成拆解模板
python outputs/fetch-wechat-article.py "https://mp.weixin.qq.com/s/xxxxx" --analyze

# 🔴 v3.0 批量提取（从 urls.txt 读取）
python outputs/fetch-wechat-article.py --batch urls.txt

# 批量提取 + 自动归档到公众号/别人/
python outputs/fetch-wechat-article.py --batch urls.txt --archive
```

**API 端点**：`https://down.mptext.top/api/public/v1/download?url={encoded_url}&format={json|md|html|text}`

**特点**：
- 无需登录 / API Key
- 支持 JSON（含完整元数据）/ Markdown / HTML / Text
- 返回标题、作者、公众号、发布时间、所有图片 CDN 链接
- **v3.0 新增**：批量提取 + 自动归档 + 增量去重

### 3.2 批量提取时的强制规则（v3.0）

| 文章数量 | 策略 | 产出 |
|---------|------|------|
| 1-5 篇 | 全部提取 + 全部走四层 | JSON + TXT + 四层分析 |
| 6-20 篇 | 全部提取，S/A 级走四层，B 级走第一层 | JSON + TXT + 选择性分析 |
| 20+ 篇 | 全部提取，S 级走四层，其余走第一层+第四层 | JSON + TXT + 选择性分析 |

### 3.3 产出文件

| 模式 | 产出 | 位置 |
|------|------|------|
| 基础模式 | `{标题}.json` + `{标题}.txt` | `outputs/wechat-articles/{日期}/` |
| --archive 模式 | 同上 + 归档到作者目录 | `公众号/别人/{作者名}/` |
| --analyze 模式 | 同上 + 道法术器模板 | `outputs/wechat-articles/{日期}/` |

### 3.4 降级方案

当 API 不可用时，降级到 browser_use 方案。降级触发条件：
- API 返回 403/500 且重试 3 次后仍失败
- 不是 `mp.weixin.qq.com` 域名
- API 返回数据不含 `content_noencode` 字段

---

## 四、Step 2：品读闭环

> 提取完成后，执行 F7 四步闭环。

| 步骤 | 操作 | 验证标准 |
|------|------|----------|
| ① 提取全文 | API 提取 → 保存到工作区 + 归档到作者目录 | Write 后 Read 验证 ≥5000 字符 |
| ② 下载资源 | 文中提到的 GitHub 仓库克隆；论文 PDF 下载 | 文件落盘到 outputs/downloads/ |
| ③ 融入 SOP | 更新对应 SOP + Skill 路由表 | Write 后 Read 验证 + 迭代日志 |
| ④ 生成学习指引 | `{作者}_学习指引与总结.md` | 含段落索引 + 信息差 + 深度思考题 |

---

## 五、Step 3：道法术器拆解

提取完成后，按以下框架拆解：

- **道（底层认知与范式转移）**：认知跃迁、范式转变
- **法（方法论与架构设计）**：核心方法、可迁移架构
- **术（技术实现细节）**：具体数字、关键技术、实现路径
- **器（工具与产品）**：提到的工具/产品/框架/模型

---

## 六、Step 4：文风DNA分析（可选）

调用 `mcp__skill-handler__Skill skill: "niuma-voice-dna"` 做量化文风对比。

---

## 七、Step 5：内容结构分析

- 文章大纲 + 论点-论据结构
- 关键金句 + 信息密度评估
- 防套路自检（意象/结构/角色/开头黑名单）

---

## 八、Step 6：内容复用方案

- **选题角度**：3-5 个可写选题
- **可复用素材**：金句、数据、类比
- **目标平台**：公众号 / 小红书 / 朋友圈 / 群分享

---

## 九、决策表（v3.0 扩展）

| 场景 | 发现方式 | 提取方式 | 分析深度 | 关键动作 |
|------|---------|---------|---------|---------|
| **搜索热文**（v3.0） | dajiala.com → 批量提取 | API 批量 | S/A 级四层 | 发现→提取→分析三连 |
| 单发链接（无标注词） | 跳过 | API 提取 | 基本信息速览 | 保存原文即可 |
| "品读/参考/融入" | 跳过 | API 提取 + 四步闭环 | 道法术器 + 融入 | F7 全闭环 |
| "分析文风" | 跳过 | API 提取 + 文风DNA | 风格特征 + 可复用 | 文风DNA逆向 |
| "批量抓取" | 可选 | API 批量模式 | 分类归档 | 按作者/主题整理 |
| 非公众号链接 | 跳过 | browser_use | 按需 | 降级方案 |

---

## 十、四层读取分析（🔴 提取完必须走，缺一不可）

> ⚠️ **提取原文只是开始。以下四层缺一不可。**
> **历史教训**：教训028 + 教训009 —— 两次只做提取不做四层。

### 强制流程

```
提取完成后
    ↓
必须继续 ↓

第一层：完整原文保存到 `公众号/别人/{作者名}/文章_{标题}.md`
第二层：文风DNA分析 → `公众号/别人/{作者名}/文风DNA分析.md`
第三层：视觉风格分析 → `公众号/别人/{作者名}/视觉风格分析.md`
第四层：信息差提取 + 工作改善映射 → `公众号/别人/{作者名}/信息差提取与工作改善.md`
```

### 批量时的执行规则

| 文章数量 | 策略 |
|---------|------|
| 1-3 篇 | 每篇完整走四层 |
| 4-10 篇 | 重点标注的文章走完整四层，其余走第一层+第四层 |
| 10+ 篇 | 全部走第一层，S/A 级走完整四层，其余走第四层 |

---

## 十一、高故障处理

### API 返回 403
- 确认链接能在浏览器打开
- 检查链接格式
- 降级到 browser_use

### 中文文件名乱码
- 使用 Python 的 `safe_filename()` 清洗
- 脚本使用 UTF-8 编码

### dajiala.com API 余额不足
- 脚本会显示余额
- 引导用户充值

---

## 十二、禁止

- ❌ 只做提取不做四层
- ❌ **只做发现不做提取（v3.0 — 发现后必须接提取）**
- ❌ 只做道法术器拆解就停
- ❌ 批量提取后只写总览文档
- ❌ **发现前不问用户确认费用（v3.0）**
- ❌ **提取后不归档到 `公众号/别人/{作者名}/`**

---

## 十三、Skill 链路（v3.0）

```
用户说"找热文/搜文章"
    ↓
Step 0: wechat-hot-discovery.py (dajiala.com)
    ├── 确认关键词+费用
    ├── 搜索 → 评分 → 排序
    └── 输出 urls.txt + summary.md
    ↓ (自动)
Step 1: fetch-wechat-article.py --batch urls.txt --archive (down.mptext.top)
    ├── 批量提取全文
    └── 自动归档到 公众号/别人/{作者名}/
    ↓
Step 2-6: SOP-02 四层读取
    ├── 文风DNA → 视觉 → 信息差 → 复用
    └── 融入 SOP/技能

用户直接发链接（跳过 Step 0）
    ↓
Step 1 → Step 2-6（同上）
```

---

## 十四、jc-zhuagongzhonghao Skill 集成（v3.1 新增）

> **来源**：用户提供的 ZIP 包（`D:\data\wechat\xwechat_files\...\公众号抓取zip.zip`）
> **安装位置**：`outputs/jc-zhuagongzhonghao/jc-zhuagongzhonghao/`
> **GitHub 源**：用户收藏的公众号热文抓取 Skill

### 14.1 组件清单

| 文件 | 用途 |
|------|------|
| `SKILL.md` | Skill 定义（触发词 + 工作流 + 评分算法 + 配置说明） |
| `scripts/公众号热文抓取.py` | 主脚本（dajiala.com API + Wilson Score 评分） |
| `assets/config-template.yaml` | 配置模板（API Key + 关键词组 + 评分权重） |
| `assets/report-template.html` | 杂志风格 HTML 报告模板（The Signal） |

### 14.2 工作流（每次调用必走）

1. **确认搜索需求**：关键词？几组？排除词？搜索范围？
2. **确认费用**：告知 `关键词组数 × ¥0.40`
3. **执行抓取**：更新 config.yaml → 运行脚本
4. **展示结果**：抓了多少篇、花了多少钱、S/A/B 各多少篇

### 14.3 与现有工具的关系

| 工具 | 定位 | 何时用 |
|------|------|--------|
| `wechat-hot-discovery.py` | 轻量发现（只搜+输出urls.txt） | 作为Step 0的快速入口 |
| `jc-zhuagongzhonghao` Skill | 完整发现+报告（搜+评分+HTML报告+Cloudflare部署） | 需要The Signal风格报告时 |
| `fetch-wechat-article.py` | 提取全文（Step 1） | 配合发现结果做批量提取 |

### 14.4 评分算法

```
总分 = 流量分 × 40% + 信任分 × 50% + 内容信号 × 10%
流量分 = log10(阅读量) 归一化到 0-100
信任分 = Wilson Score 下界(互动数, 阅读量) 归一化到 0-100
内容信号 = 原创(+30) + 关键词 + 内容长度
等级：S(≥55) / A(≥35) / B(20-34) / 过滤(<20)
```

### 14.5 部署（Cloudflare Pages）

```bash
# 首次
npx wrangler login
npx wrangler pages project create 项目名 --production-branch=main

# 之后自动（deploy.auto_deploy: true）
```

---

## 变更记录

| 日期 | 版本 | 变更内容 |
|------|------|---------|
| 2026-05-09 | v1.0 | 初始创建 |
| 2026-05-22 | v1.1 | Step 3 新增防套路自检框架 |
| 2026-06-03 | v2.0 | API 优先替代浏览器方案 |
| 2026-06-05 | v2.1 | 新增四层读取分析 |
| **2026-06-09** | **v3.0** | **全链路优化：+Step 0 文章发现（dajiala.com）+ 批量提取 + 自动归档。来源：7篇技能/Agent文章品读 + jc-zhuagongzhonghao 工具集成。全局目标：发现→提取→分析→融入 全链路自动化。** |
| **2026-06-09** | **v3.1** | **🆕 §十四 jc-zhuagongzhonghao Skill 集成：ZIP包解压到 outputs/，SKILL.md工作流+评分算法+部署方案正式写入SOP。与现有wechat-hot-discovery.py的关系：轻量发现 vs 完整发现+HTML报告。** |
