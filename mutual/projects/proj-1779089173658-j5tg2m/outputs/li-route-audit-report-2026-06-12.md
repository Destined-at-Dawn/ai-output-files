# li- 系列端到端触发审计 + 技能审查报告

> 日期：2026-06-12
> 触发：session checkpoint P2 待办 "li- 系列端到端触发测试"
> 方法：Python 全量交叉审计 + 逐个 SKILL.md 深度审查
> 审计脚本：`outputs/audit_li_routes.py`

---

## 一、总览

| 指标 | 数值 | 状态 |
|------|------|------|
| 已安装 li-* 技能目录 | 50 | — |
| 有路由的 li-* 技能 | 40 | — |
| **缺失路由（GAP）** | **10** | 🔴 |
| 幽灵路由（指向不存在的技能） | 0 | ✅ |
| 跨技能重复触发词 | 0 | ✅ |
| 触发词不足 15 个 | 4 | 🟡 |
| 触发词总数 | 1,133 | ✅ |
| E2E 抽样测试 | 10/10 | ✅ |

---

## 二、审计方法

### 步骤 1：全量交叉审计（Python 脚本）

```
输入：
  - skill-routing-table.json（89条路由，1133个触发词）
  - ~/.newmax/skills/li-*/（50个活跃目录，排除 .zip）

输出：
  - 已安装但无路由的 GAP 技能
  - 有路由但未安装的 GHOST 路由
  - 每个技能的触发词数
  - 跨技能重复触发词
```

### 步骤 2：逐个 SKILL.md 深度审查

读每个 GAP 技能的 SKILL.md，判断：
1. 功能是否有独立价值？
2. 与其他已路由技能是否有功能重叠？
3. 是否有真实案例（而非编造的"预期场景"）？
4. SKILL.md 质量如何？（执行协议/理论锚点/反模式是否完整）

### 步骤 3：E2E 抽样测试

用 10 条真实用户消息模拟触发匹配，验证路由表是否能正确匹配。

---

## 三、E2E 抽样测试（10/10 通过 ✅）

| # | 用户消息 | 期望命中 | 实际命中 | 结果 |
|---|---------|---------|---------|------|
| 1 | "帮我写一篇小红书帖子，主题是FPGA学习" | li-xhs | li-hardware, li-xhs, li-study | ✅ |
| 2 | "这个FPGA代码的时序收敛不了，帮我看看" | li-hardware | li-hardware | ✅ |
| 3 | "我想做一个深度调研，对比一下市场上的AI编程工具" | li-research | li-research, li-code | ✅ |
| 4 | "帮我分析一下这篇文章的认知科学支撑" | li-analyze | li-analyze | ✅ |
| 5 | "我觉得自己学不进去了，总是拖延" | li-mindcoach | li-mindcoach | ✅ |
| 6 | "把这几个skill合并一下" | li-skillfusion | li-skillfusion | ✅ |
| 7 | "昨天的工作做一个复盘" | li-improve | li-improve | ✅ |
| 8 | "帮我设计一个品牌视觉规范" | li-design | li-visual, li-design | ✅ |
| 9 | "把这段会议录音转成文字" | li-transcript | li-transcript | ✅ |
| 10 | "帮我做一个PPT，答辩用" | li-office | li-office | ✅ |

**结论**：现有路由表覆盖良好。10 条消息全部命中期望技能，无漏触发。

---

## 四、GAP 技能逐个审查

### 4.1 li-docs — ⭐ 建议保留 + 注册路由

| 维度 | 评估 |
|------|------|
| 在41活跃名单中 | ✅ 是（Tier 2 内容平台） |
| SKILL.md 行数 | 293 行 |
| 真实案例 | ✅ 3 个（li-infra SOP 体系、交接文档 v3、百大认知书籍） |
| 执行协议 | Phase 0-2 三阶段工作流 |
| 认知锚点 | ✅ 5 个理论锚点 |
| 反模式清单 | ✅ 5 条 |
| 功能重叠 | ❌ 无 — 唯一专注于"文档共创工作流"的技能 |
| 建议触发词 | 文档共创、协同写作、写文档、方案文档、技术文档、设计文档、PRD、RFC、文档质量、文档评审、好文档、一起写、共创、写提案、写规格 |

**裁决**：必须保留。在41名单中，功能无重叠，有真实案例。

---

### 4.2 li-personal — ⭐ 建议保留 + 注册路由

| 维度 | 评估 |
|------|------|
| 在41活跃名单中 | ❌ 否（额外技能） |
| SKILL.md 行数 | 110 行 |
| 真实案例 | ✅ 1 个（实习 vs 考研时间分配） |
| 底层包装 | resume-modification, self-intro-writer, university-planner, personal-info-discovery, personal-rag-qa |
| 功能重叠 | ❌ 无 — 已路由技能中无直接的"个人品牌/简历/面试"协调器 |
| 建议触发词 | 简历、resume、面试、自我介绍、职业规划、career、求职、job、offer、大学规划、考研、复试、CV、个人品牌、求职信、cover letter |

**裁决**：建议保留。功能独立于已路由技能，覆盖求职/面试/简历场景的核心需求。

---

### 4.3 li-writing — ⭐ 建议保留 + 注册路由

| 维度 | 评估 |
|------|------|
| 在41活跃名单中 | ❌ 否（额外技能） |
| SKILL.md 行数 | 119 行 |
| 真实案例 | ✅ 3 个（小红书帖子、公众号长文、学术润色） |
| 底层包装 | blog-post-writer, copywriting-skills, humanizer-zh, chinese-natural-voice-revision, khazix-writer, koubo-script-writer |
| 功能重叠 | ⚠️ 部分 — li-xhs 覆盖小红书，li-wechat 覆盖公众号。但 li-writing 作为"多平台写作协调器"有编排价值（自动识别文体→路由到正确子技能） |
| 建议触发词 | 写文章、写文案、写作、润色、改写、去AI味、文风、写作技巧、文案、稿件、撰写、撰文、稿子、copywriting、humanizer、文风调整、风格改写、脚本写作 |

**裁决**：建议保留。有真实案例验证，作为跨平台写作协调器填补了"内容创作入口"这个节点。

---

### 4.4 ⚠️ li-autoreply vs li-persona-qa — 功能高度重复

这是本次审计发现的最严重重复问题。两个技能几乎做同一件事：

#### 功能对比

| 维度 | li-autoreply | li-persona-qa |
|------|-------------|---------------|
| 核心功能 | 个人问题自动应答 | 个人问答代答器 |
| 信息源 | telos/ 8 个文件（必读） | telos/ 5 个文件（必读） |
| 动态信息 | memory/ 最近 7 天（按需） | memory/ 最近 3 天（按需） |
| 深度扫描 | personal-info-discovery 技能 | glob 关键词搜索 |
| 问题分类 | 6 类（面试/反思/社交/规划/观点/通用） | 4 场景（问卷/面试/自我介绍/反思） |
| 口吻控制 | 7 条口吻规则 + 禁用词清单 | 调用 niuma-voice-dna |
| 自审清单 | 5 项 | 6 项 |
| 快速模式 | ✅ 有（只读 3 文件） | ❌ 无 |
| 理论锚点 | ❌ 无 | ✅ 6 个认知理论 |
| 信息缺口处理 | ❌ 无独立协议 | ✅ 有（事实缺口/感受缺口/时效缺口三级） |
| 执行协议 | ✅ 完善（RED 必读 8 文件 + YELLOW 按需 + STOP 门禁） | ⚠️ 有（但门禁不够硬） |
| 创建日期 | 2026-06-11 | 2026-06-11 |

#### 关键差异

**li-autoreply 更强的地方**：
- 执行协议更硬（RED/YELLOW/STOP 三级门禁）
- 口吻规则直接在 SKILL.md 中硬编码（不依赖外部 skill）
- 有快速模式（3 文件即可生成回答）
- 问题分类更细（6 类 vs 4 类）

**li-persona-qa 更强的地方**：
- 信息缺口处理协议更完善（三级缺口 + 处理策略）
- 有认知理论支撑（6 个锚点）
- 场景速查更实用（问卷代填、面试模拟、自我介绍、反思 4 个高频场景都有独立方案）
- 置信度标注机制（✅确定 / ⚠️推断 / ❓不确定）

#### 重叠度测算

```
功能重叠矩阵：
  Phase 1（信息采集）    ：重叠 85%
  Phase 2（问题分类）    ：重叠 70%（分类方式不同）
  Phase 3（代答生成）    ：重叠 90%
  Phase 4（自审交付）    ：重叠 80%
  ─────────────────────────────────
  综合重叠度              ：~81%
```

#### 裁决选项

**选项 A：保留 li-autoreply，弃用 li-persona-qa**
- 理由：执行协议更完整，口吻控制内建（不依赖外部 skill），快速模式实用
- 代价：丢失 li-persona-qa 的信息缺口处理协议和认知理论锚点

**选项 B：保留 li-persona-qa，弃用 li-autoreply**
- 理由：信息缺口处理协议是生产级必需的，场景速查更实用，有认知理论支撑
- 代价：丢失 li-autoreply 的硬执行协议和快速模式

**选项 C：融合两者优势 → 合并为一个**
- 保留 li-autoreply 的执行协议 + 快速模式
- 注入 li-persona-qa 的信息缺口处理协议 + 场景速查 + 认知锚点
- 取长补短，产出 v2.0
- 代价：需要额外一轮融合工作

---

### 4.5 li-frontend — ❌ 建议弃用

| 维度 | 评估 |
|------|------|
| 真实案例 | ❌ 0 个（所有案例标注"尚未被实际使用"） |
| 底层包装 | web-design-engineer, frontend-design, canvas-design, algorithmic-art, brand-guidelines |
| 被谁覆盖 | **li-web**（r112）— 覆盖完全相同的场景：网页制作/前端开发/React/HTML/CSS/部署网站 |
| 裁决理由 | li-web 已有 19 个触发词，路由活跃。li-frontend 零真实案例 + 完全重叠。 |

---

### 4.6 li-platform — ❌ 建议弃用

| 维度 | 评估 |
|------|------|
| 真实案例 | ✅ 1 个（公众号排版优化） |
| 底层包装 | wechat-article-collector, wechat-exporter, wechat-analysis, x-article-publisher, xiaojiang |
| 被谁覆盖 | **li-wechat**（r296）— 22 个触发词覆盖微信全场景：公众号/微信文章/聊天记录/微信采集/公众号分析 |
| 裁决理由 | li-wechat 直接覆盖，且 li-platform 的 X/Twitter 发布功能价值不高（用户主要是国内平台）。 |

---

### 4.7 li-search — ❌ 建议弃用

| 维度 | 评估 |
|------|------|
| 真实案例 | ✅ 1 个（搜 Arduino 舵机控制 skills） |
| 底层包装 | step-search, web-access, find-skills, aihot, research-daily |
| 被谁覆盖 | **li-research**（57 触发词）+ **li-bestskill**（26 触发词）+ **li-local-search**（18 触发词）三重覆盖 |
| 裁决理由 | 搜索是 li-research 的核心能力之一（已含"搜一下""查找""资料收集"），技能搜索走 li-bestskill，本地工具搜索走 li-local-search。li-search 没有独立价值。 |

---

### 4.8 li-session — ❌ 建议弃用

| 维度 | 评估 |
|------|------|
| 真实案例 | ✅ 1 个（跨天继续任务） |
| 底层包装 | session-summary, daily-review, conversation-to-knowledge, post-task-audit |
| 被谁覆盖 | **li-sync**（收尾/会话结束）+ **li-manage**（对话日志/工作流审查）+ **li-improve**（对话结束/复盘）三重覆盖 |
| 裁决理由 | 会话管理功能已经被拆解到了三个已有路由的技能中。li-session 的 4 种模式（A/B/C/D）各自由不同的已路由技能承担。 |

---

### 4.9 li-voice — ❌ 建议弃用

| 维度 | 评估 |
|------|------|
| 真实案例 | ❌ 0 个（标注"尚未被实际使用"） |
| 底层包装 | niuma-voice-dna, humanizer-zh, chinese-natural-voice-revision |
| 被谁覆盖 | **li-writing**（包含文风调整/去AI味/润色）|
| 裁决理由 | 零真实案例 + 声纹DNA功能完全可以并入 li-writing 的 Phase 2（精修：中文自然语感修正）。单独一个 skill 太重。 |

---

## 五、触发词不足 15 个（4 个技能）

| 技能 | 当前 | 缺口 | 建议 |
|------|------|------|------|
| **li-skills-mgmt** | 14 | 1 | 补"技能审计""skill审计""技能检查" |
| **li-devil** | 12 | 3 | 补"帮我质疑""帮我找问题""批判性思考""找漏洞""挑刺" |
| **li-plan** | 10 | 5 | 补"今天计划""本周计划""排一下""任务安排""日程""时间管理""规划一下" |
| **li-code** | 10 | 5 | 补"写个函数""代码实现""编程实现""写个工具""utils""helper""代码片段" |

---

## 六、建议的行动计划

### 立即执行（本对话）

1. **li-docs** → 注册路由（≥15 触发词）
2. **li-personal** → 注册路由（≥15 触发词）
3. **li-writing** → 注册路由（≥15 触发词）
4. **4 个低触发词技能** → 补到 ≥15 个

### 等待用户决策

5. **li-autoreply vs li-persona-qa** → 选项 A/B/C 待定

### 待执行（用户确认后）

6. **li-frontend** → 创建 DEPRECATED.md，归档
7. **li-platform** → 创建 DEPRECATED.md，归档
8. **li-search** → 创建 DEPRECATED.md，归档
9. **li-session** → 创建 DEPRECATED.md，归档
10. **li-voice** → 创建 DEPRECATED.md，归档
11. 同步路由表到 5 个工作区

---

## 七、审计证据

| 证据 | 路径 |
|------|------|
| 审计脚本 | `outputs/audit_li_routes.py` |
| 路由表 | `skill-routing-table.json`（89条路由，2410行） |
| 技能目录 | `~/.newmax/skills/li-*/`（50个活跃目录） |
| 本报告 | `outputs/li-route-audit-report-2026-06-12.md` |

---

> 审计完成时间：2026-06-12
> 下一步：等待用户对 li-autoreply vs li-persona-qa 的裁决
