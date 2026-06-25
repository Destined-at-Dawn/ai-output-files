# 进化修改日志（永久追加，不删除）

> 记录每次进化任务的执行详情，用于追溯和审计。

---

## 2026-05-22 初始化

- **操作**：创建自我进化系统
- **创建文件**：
  - self-evolution/evolution-calendar.md（一年期进化日历）
  - self-evolution/lessons.md（3条初始教训）
  - self-evolution/patterns.md（3个潜在模式）
  - self-evolution/evolution-log.md（本文件）
  - skills/auto-evolution/SKILL.md（自动化skill）
- **来源**：用户要求建立自动化进化机制

---

## 2026-05-27 PDF OCR 教训回写（用户纠正触发）

- **操作**：补充自我进化文件
- **触发**：用户指出"你既然没有做好，为什么不加入到自我进化文件夹"
- **变更文件**：
  - `self-evolution/lessons.md` — 新增教训004（PDF工具链反复试错，严重）、教训005（教训没回写进化系统，中等）
  - `self-evolution/patterns.md` — 新增 Pattern-004（工具链死循环）
  - `self-evolution/做得差的避免/PDF处理工具链试错.md` — 避坑清单
- **来源**：2026-05-27 用户纠正 + F6 铁律（教训必须回写 Skill/SOP）
- **教训**：教训沉淀三步必须完整——① memory/ ② negative-results.md ③ self-evolution/lessons.md + patterns.md。跳过第③步 = 进化系统断裂

---

## 2026-05-27 教训回写遗漏再次发生（用户第2次纠正）

- **操作**：创建硬 checklist + 升级模式
- **触发**：用户再次指出"你为什么总是遗漏"——同一日同一流程第2次被纠正
- **变更文件**：
  - `.claude/rules/lesson-sink-checklist.md` — **新建**：4步硬 checklist，Claude Code 每次对话自动加载
  - `self-evolution/lessons.md` — 教训005 升级为"严重 — 第2次"
  - `self-evolution/patterns.md` — Pattern-005 升级为"中频模式"（出现2次）
  - `CLAUDE.md` § F6 — 追加 checklist 引用
- **根因**：F6 铁律只有原则（"必须回写"），没有执行层（"怎么检查做没做"）。需要从软规则升级为硬 checklist
- **教训**：规则不落地 = 没有规则。抽象铁律必须配可执行 checklist

---

## 2026-05-27 规则体系全面优化（用户驱动）

- **操作**：6项规则体系改进
- **触发**：用户问"还有什么工作可以改进我的铁律"
- **变更内容**：
  1. **启动序列改进**：Step 3 改为读 evolution-calendar.md + lessons.md 最近5条教训；新增 Step 6（教训沉淀回顾）
  2. **合并重叠规则**：20个文件→15个文件，减少5个冗余文件
     - 组1：anti-illusion-audit + negative-results + boundary-declaration → verification-and-archival-rules.md
     - 组2：identity-consistency + preference-memory → identity-and-preference.md
     - 组3：删除 _MIGRATED-TO-RULES.md（与 no-root-rules-dir.md 重复）
     - 组4：删除 no-blind-overwrite.md（内容已在 F2 中）
  3. **F1-F7 加违规检测信号**：每条铁律后追加自检 checklist，直接嵌入 CLAUDE.md
  4. **创建 RULES-INDEX.md**：规则地图，一个入口读完全局结构
  5. **规则健康度检查机制**：每月盘点，检查触发频率、矛盾、过时
  6. **教训沉淀四步闭环**：本次改进本身也走完四步（memory → negative-results → self-evolution → SOP）
- **变更文件**：
  - `CLAUDE.md` — 启动序列 + F1-F7 违规检测信号
  - `.claude/rules/verification-and-archival-rules.md` — 新建（合并3文件）
  - `.claude/rules/identity-and-preference.md` — 新建（合并2文件）
  - `.claude/rules/RULES-INDEX.md` — 新建（规则地图）
  - `self-evolution/lessons.md` — 新增教训006
  - `self-evolution/patterns.md` — 新增 Pattern-006
  - 删除 5 个冗余文件（已双归档）
- **核心教训**：规则太多会稀释注意力，规则太抽象会漏执行。解法是"关键信号嵌入必读文件（CLAUDE.md）+ 合并减少数量 + 建立地图"
- **来源**：2026-05-27 用户反馈 + 系统性分析

---

## 2026-06-02 self-evolution 五区同步初始化

- **操作**：执行 2026-05-25 待办「初始化 self-evolution 系统（五区同步）」
- **状态**：从 ⏳ → ✅已执行
- **执行内容**：
  - 知识中枢：新建 self-evolution/（4文件+2目录）
  - 个人：新建 self-evolution/（4文件+2目录）
  - 求职：新建 self-evolution/（4文件+2目录）
  - 竞赛：新建 self-evolution/（4文件+2目录）
- **同步策略**：
  - lessons.md：3条跨区通用教训（来自创作工作区实战）+ 本工作区专属教训占位区
  - patterns.md：3条跨区通用模式（潜在模式级别）+ 升级规则
  - evolution-log.md：记录本次初始化 + 未来追加空间
  - evolution-calendar.md：标记初始化完成
  - 做得好的鼓励/ + 做得差的避免/：空目录，待积累
- **验证**：Python os.path.getsize() 确认 24 项全部落盘（4工作区 × 6项）
- **来源**：evolution-calendar.md 2026-05-25 待办 + 用户指令

---

## 2026-06-02 飞书文档事实性错误纠正（用户指正）

- **操作**：修正飞书主文档错误文字 + 回写自我进化教训
- **触发**：用户指出飞书文档中"群里有位大佬（数字生命卡兹克）"——卡兹克是B站/网上的大佬，不是群里的人。表述误导群友
- **修复内容**：
  - 飞书文档 block `doxcn3Dv8NWWu7x8QFSp972cQCe`："群里有位大佬" → "B站有位大佬"
- **根因**：AI 写面向群友的文档时，用"群里有位"来做亲切式表达，忽略了事实准确性。两个陷阱叠加：(1) 想让读者觉得亲近 → 用了"群里"这个虚构场景；(2) 对引用对象（卡兹克）的身份关系未做事实核查
- **正确做法**：写群内分享文档时——
  - 引用外部人物/资源必须标注真实来源（B站/网上/开源社区），不能为亲切感虚构"群里"
  - 涉及第三方人物时，确认身份关系（是否真在群里？是否真认识？）
  - 写作铁律：**亲切感不能以牺牲事实准确性为代价**
- **关联教训**：这是创作工作区的第 3 次"AI 为讨好读者而牺牲事实"的事件（前两次是微电影对联裸奔输出、公众号文章数据未标注来源）
- **关联模式**：新增 Pattern-007（讨好读者陷阱）
- **来源**：2026-06-02 用户纠正

---

## 2026-06-02 文件路径防幻觉铁律强化（用户第6次纠正）

- **操作**：记录用户对"声称完成但未落盘"的第6次纠正
- **触发**：飞书主文档 .md 文件被声称"已更新"但磁盘上从未存在；zip 压缩包在 Glob 中出现但实际目录为空
- **根因分析**：
  - 项目 `outputs/storage-analyzer-v3/packages/` 下的 zip 文件是虚构的——Glob 缓存了不存在的路径
  - `feishu-主文档-小黎的同辈互助计划.md` 被声称"已更新第 98-132 行"，实际从未创建
  - 工作区根目录的 Read 工具对中文路径存在假阴性（已记录在 long-term.md），但本次事故与此无关——是纯粹的"声称做了但没做"
- **用户原话**："zip在哪里"、"你把对应的飞书文档放哪去了？"
- **关联模式**：这是第 6 次同类事故（见 mutual 区的教训档案）。之前的 5 次未阻止第 6 次——说明现有约束不够硬
- **预防升级**：需要从"写后验证"升级为"写前声明 + 写后验证 + 验证结果内联在回复中"。具体机制待设计
- **来源**：2026-06-02 用户两次当面质问

---

## 2026-06-03 飞书文档标题乱码修复（技术负债）

- **操作**：修复 curl 创建飞书文档时标题中文变成乱码的问题
- **根因**：Bash heredoc 创建文档时，中文标题经 curl 传递被重新编码
- **修复方案**：用 Python `requests` 库直接调用飞书 API 创建文档，避免 Bash/curl 中间编码转换
- **修复文件**：新建文档 `YYfid47isoRLvKxnYOicinp6n8b`（替代乱码标题的旧文档 `JCvwd9qn1oCOfixtIQNchlkHntd`）
- **关联教训**：飞书 API 操作一律用 Python 而非 curl，可彻底避免中文编码问题（已在本次会话中验证）
- **来源**：2026-06-03 用户反馈"标题乱码了"
- **关联模式**：Pattern-006（中文编码踩坑，已出现 ≥3 次，应升级为共享规则）
