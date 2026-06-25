#!/usr/bin/env python3
"""Phase 1: Inject case studies + antipatterns + conditional next into 9 WARN skills."""
import os

SKILLS_DIR = r"C:\Users\13975\.newmax\skills"

# === UPGRADE CONTENT FOR EACH WARN SKILL ===

upgrades = {
    "li-data": {
        "cases": """
## Case Studies

### Case 1: 对话数据清洗管道
用户要求将 30 天的对话日志（12 万字）清洗为结构化知识库。执行流程：langdetect 语言检测 → 去重（SimHash）→ 分段（按主题切分）→ 格式统一（Markdown）→ 质量抽检。耗时 45 分钟，原始 12 万字 → 清洗后 4.8 万字（去重率 60%）。
- **教训**：去重阈值太激进（>0.85）会丢失有效信息，经测试 0.78 是最优阈值
- **Source**: conversation-journal/2026-06-01.md

### Case 2: 多源数据合并陷阱
竞赛区 3 个项目目录的 SOP 文件有 40% 内容重叠但格式不同（Markdown/纯文本/Word 转换残留）。用 Python 模糊匹配 + 人工确认合并，最终 188 个 SOP 去重为 142 个。
- **教训**：Word 转 Markdown 的残留格式（如 `<!-- -->` 注释和 `\t` 制表符）会导致字段解析错误
- **Source**: 竞赛/sop-indexes.txt

### Case 3: 路由表数据修复
113 条路由中有 35 个重复触发词、10 条同 skill 重复路由。用 Python 脚本检测重复 → 仲裁冲突（高优先级保留）→ 合并重复 → 全量同步 47 工作区。
- **教训**：JSON 路由表的 `triggers` 数组去重不能用简单的 `set()`——需要大小写归一化 + 空格标准化
- **Source**: skill-routing-table.json 治理记录""",
        "antipatterns": """
## Anti-Patterns

| ID | 反模式 | 理论锚点 | 后果 | 正确做法 |
|----|--------|----------|------|----------|
| AP-D1 | 存原始文本不提取结构 | 认知负荷理论 T4（Sweller） | 后续检索效率 O(n)，无法语义匹配 | 先结构化再存储，每条数据标注类型+来源+时间戳 |
| AP-D2 | 去重阈值凭直觉设定 | 实测优先于直觉 T3 | 阈值太严丢信息，太松留垃圾 | 用 3 组真实数据扫描测试，画精度-召回曲线 |
| AP-D3 | 数据清洗不验证残留 | 证据分层 T1 | 清洗后仍有隐藏格式残留 | 每批清洗后抽检 5%，检查格式/编码/空值 |
| AP-D4 | 多源合并不做冲突检测 | 跨边界先校验 T5 | 同名不同义字段被覆盖，数据语义丢失 | 合并前先对比 schema 差异，冲突字段人工确认 |
| AP-D5 | 一次加载全部数据到上下文 | 认知负荷理论 T4 | 超出窗口，信息被截断丢失 | 分批加载 + 摘要压缩，每批 ≤300 行 |""",
        "conditional": """
## Conditional Next Steps

| 条件 | 下一步 |
|------|--------|
| 数据量 >10MB | → li-research Phase 2 压缩策略 |
| 多源数据格式不一致 | → li-workspace Phase 1 格式统一 |
| 涉及敏感信息 | → Phase 3 隐私脱敏 |
| 需要持久化存储 | → li-memory Phase 1 事实提取 |
| 清洗结果需多人确认 | → li-sync Phase 3 审查协议 |"""
    },

    "li-voice": {
        "cases": """
## Case Studies

### Case 1: 会议录音转文字
1 小时 FPGA 技术讨论录音（中文），使用 Whisper 转文字后得到 8000 字逐字稿。问题：专业术语（"时钟域交叉""建立时间"）识别错误率 15%。解决方案：建立领域术语词典注入 Whisper prompt，错误率降至 3%。
- **教训**：通用 ASR 对专业术语的识别率极低，必须预注入领域词典
- **Source**: 竞赛/projects/FPGA-逆变器/documentation/

### Case 2: 逐字稿清洗流水线
小红书视频逐字稿（15 分钟），需要清洗为公众号文章素材。执行流程：ASR 转文字 → li-transcript 清洗（去口头禅/重复/语气词）→ li-analyze 道法术器拆解 → 格式化输出。
- **教训**：口头禅（"就是""然后""对吧"）删除后需要重读一遍确认语义连贯，自动删除会破坏句子结构
- **Source**: 创作/sops/sop-01-内容研究与选题.md

### Case 3: 多语言语音识别
英文技术讲座字幕提取。Whisper large-v3 英文识别率 >98%，但中英混杂（如"FPGA 的 timing constraint"）时切分错误。
- **教训**：中英混杂场景需要先做语言分段，再分别识别
- **Source**: li-transcript/references/case-studies.md""",
        "antipatterns": """
## Anti-Patterns

| ID | 反模式 | 理论锚点 | 后果 | 正确做法 |
|----|--------|----------|------|----------|
| AP-V1 | 直接用 ASR 原始输出不做清洗 | 认知负荷 T4 | 口头禅/重复/错误占 30%，后续分析质量差 | 必须经 li-transcript 清洗后才进入分析流程 |
| AP-V2 | 不注入领域术语词典 | 跨边界校验 T5 | 专业术语识别错误率 >15% | ASR 前先建领域术语表，注入 prompt/词典 |
| AP-V3 | 自动删除口头禅不验证 | 证据分层 T1 | 删掉口头禅后语义断裂，关键信息丢失 | 删除后必须重读验证语义连贯性 |
| AP-V4 | 音频格式不检查直接处理 | 跨边界校验 T5 | 编码不兼容导致静默失败 | 处理前确认格式/采样率/声道数 |
| AP-V5 | 长音频不分段直接转写 | 认知负荷 T4 | Whisper 内存溢出或结果质量下降 | >30 分钟音频先按静音分段再逐段转写 |""",
        "conditional": """
## Conditional Next Steps

| 条件 | 下一步 |
|------|--------|
| 需要内容创作 | → li-transcript 清洗 → li-analyze 分析 |
| 专业术语多 | → 先建领域术语词典再 ASR |
| 音频 >30 分钟 | → 分段处理，每段 ≤15 分钟 |
| 需要多语言 | → 先做语言检测再分语言处理 |
| 结果需发布 | → li-analyze Phase 3 质量评估 |"""
    },

    "li-platform": {
        "cases": """
## Case Studies

### Case 1: 小红书平台算法适配
用户要发电气专业科普帖。小红书的算法偏好：封面图 > 标题 > 正文前 2 行。根据平台特性调整策略：用 li-visual 生成封面 → li-prompt 优化标题（18 字以内 + emoji）→ 正文首段前置核心结论。
- **教训**：小红书的流量分配 80% 取决于封面和标题质量，正文质量只影响完读率
- **Source**: 创作/sops/sop-00-内容创作总索引.md

### Case 2: 公众号 vs 知乎内容复用
同一篇 FPGA 学习路线文章需要发公众号和知乎。两个平台格式差异巨大：公众号需要行间距 1.75 倍 + 图片居中 + 分割线；知乎支持 Markdown 但需要专栏标签。
- **教训**：不要用一份 Markdown 直接发两个平台——需要用 li-prompt 的平台母语模板分别适配
- **Source**: li-prompt/references/platform-templates.md

### Case 3: 微信读书笔记提取
用户在微信读书做了 200+ 条划线笔记，需要提取到 Obsidian 知识库。微信读书没有 API，只能通过网页版手动导出 → 格式清洗 → 按书籍分组 → 写入 Obsidian。
- **教训**：微信读书导出的 HTML 格式每本书都不同，需要用 BeautifulSoup 解析而不是正则匹配
- **Source**: 个人/sops/sop-01-知识管理SOP.md""",
        "antipatterns": """
## Anti-Patterns

| ID | 反模式 | 理论锚点 | 后果 | 正确做法 |
|----|--------|----------|------|----------|
| AP-P1 | 一份内容直接发所有平台 | 跨边界校验 T5 | 格式错乱，平台算法降权 | 每个平台用 li-prompt 母语模板分别适配 |
| AP-P2 | 不研究平台算法就发布 | 实测优先 T3 | 内容好但没有流量 | 发布前用 li-research 搜该平台的最新算法规则 |
| AP-P3 | 用浏览器 API 抓取平台数据 | 证据分层 T1 | API 变动导致脚本失效 | 优先用官方 API / MCP 工具，浏览器抓取作为 fallback |
| AP-P4 | 忽略平台的内容审核规则 | 安全第一 | 内容被限流或删除 | 发布前检查平台敏感词列表 |
| AP-P5 | 把平台当成存储而非分发渠道 | 工具定律 T6 | 内容锁死在一个平台 | 跨平台复用，本地留源文件 |""",
        "conditional": """
## Conditional Next Steps

| 条件 | 下一步 |
|------|--------|
| 需要跨平台发布 | → li-prompt 母语适配 |
| 需要优化算法曝光 | → li-research 平台算法研究 |
| 需要批量发布 | → li-workflow 自动化管道 |
| 需要数据回收 | → li-data 采集+分析 |
| 平台规则变化 | → li-sync 更新 SOP |"""
    },

    "li-session": {
        "cases": """
## Case Studies

### Case 1: 对话压缩后丢失上下文
对话进行 2 小时后触发 auto-compact，压缩后 AI 丢失了"正在修路由表"的上下文，开始重复已完成的工作。解决方案：session-checkpoint.md 记录当前任务状态 + 已完成步骤 + 下一步。
- **教训**：compact 是不可逆的——如果 checkpoint 没写，丢失的上下文无法恢复
- **Source**: .claude/session-checkpoint.md

### Case 2: 35 天对话日志断裂
conversation-journal 从 5/26 开始停止更新（35 天没记录）。根因：启动序列中的对话日志写入步骤被跳过——不是规则消失了，而是 AI 在后续会话中没有主动执行。
- **教训**：靠"AI 记得要做"不可靠——需要 hook 驱动或硬规则强制
- **Source**: conversation-journal/ 目录扫描

### Case 3: 多会话任务衔接
FPGA 项目分 3 次对话完成。第 2 次对话开始时 AI 不知道第 1 次做到哪里——因为 project.md 的状态标记没更新。解决方案：每次结束前更新 project.md + memory/{date}.md。
- **教训**：跨会话的任务衔接必须有持久化状态文件，不能靠 AI 的"记忆"
- **Source**: 竞赛/projects/LCD驱动开发-verilog修改/""",
        "antipatterns": """
## Anti-Patterns

| ID | 反模式 | 理论锚点 | 后果 | 正确做法 |
|----|--------|----------|------|----------|
| AP-S1 | 对话结束前不写 checkpoint | 记录即记忆 | compact 后丢失全部进行中任务 | 每次长对话结束前更新 session-checkpoint.md |
| AP-S2 | 对话日志断更 | 规则结晶 T10 | 历史经验无法被后续会话检索 | 每日对话必须写 conversation-journal/{date}.md |
| AP-S3 | project.md 状态不更新 | 负结果归档 T7 | 跨会话不知道做到哪里了 | 里程碑完成时更新状态标记 |
| AP-S4 | compact 时不保留关键路径 | 认知负荷 T4 | 压缩后 AI 重走老路 | compact 指令里写明"保留: 文件路径+决策+下一步" |
| AP-S5 | 不区分"讨论"和"执行"模式 | 认知灵活性 T9 | 讨论产生的草稿被当成最终输出 | 明确标注"草稿/讨论/最终"状态 |""",
        "conditional": """
## Conditional Next Steps

| 条件 | 下一步 |
|------|--------|
| 对话 >30 分钟 | → 写 checkpoint 到 session-checkpoint.md |
| 任务跨会话 | → 更新 project.md + memory/{date}.md |
| 对话即将结束 | → li-improve Phase 0 自审 |
| 上下文即将满 | → /compact focus on [当前任务] |
| 多个并行任务 | → li-triage 分流优先级 |"""
    },

    "li-search": {
        "cases": """
## Case Studies

### Case 1: 本地全文搜索定位失败
用户问"我之前做过 I2C 相关的 SOP 在哪里"。grep "I2C" 在 67 个工作区返回 200+ 结果，但真正相关的只有 3 个。问题：关键词太宽泛，没用路径过滤。
- **教训**：本地搜索必须先用 `list_project_files` 定位目录，再用 `read_project_file` 精确读取——R13 地图优先于盲搜
- **Source**: .claude/rules/13-map-before-search.md

### Case 2: 跨工作区知识检索
用户问"我之前做过哪些 FPGA 项目"。相关文件分散在 4 个工作区（竞赛/projects/、个人/outputs/、mutual/memory/、学习/），需要跨区搜索。
- **教训**：跨区搜索先查知识中枢注册表（工作区注册表.md），再逐区精确搜索
- **Source**: 知识中枢/00-注册表/工作区注册表.md

### Case 3: 路由表搜索定位 skill
用户说"帮我做思维导图"——需要在 105 条路由 / 1493 个触发词中找到匹配的 skill。实际命中 li-mindmap（r053, priority 8）。
- **教训**：触发词匹配是模糊匹配——"思维导图""mindmap""脑图"都能命中，但"结构化思考"不会——需要多维触发词覆盖
- **Source**: skill-routing-table.json""",
        "antipatterns": """
## Anti-Patterns

| ID | 反模式 | 理论锚点 | 后果 | 正确做法 |
|----|--------|----------|------|----------|
| AP-SS1 | 连续 grep 3 次还没找到不停下 | R13 地图优先 | 浪费 token，找不到还是找不到 | 连续 3 次未命中 → 停下查地图/注册表 |
| AP-SS2 | 搜索不指定范围 | 认知负荷 T4 | 全局搜索返回海量无关结果 | 先定位目录再搜索，范围逐步缩小 |
| AP-SS3 | 只搜文件名不搜内容 | 实测优先 T3 | 文件名不含关键词但内容相关的被遗漏 | 文件名+内容双搜索 |
| AP-SS4 | 不区分"搜什么"和"在哪搜" | 跨边界校验 T5 | 在错误的目录里搜半天 | 先查注册表/索引确定目标目录，再搜索 |
| AP-SS5 | 搜索结果不验证就使用 | 证据分层 T1 | 搜到的是旧版/废弃文件 | 搜索结果必须 Read 验证内容后再使用 |""",
        "conditional": """
## Conditional Next Steps

| 条件 | 下一步 |
|------|--------|
| 搜本地文件 | → li-local-search |
| 搜网上 skill | → li-bestskill 四阶段搜索 |
| 搜历史对话 | → li-memory 事实检索 |
| 搜知识中枢 | → 查注册表 → 精确路径 Read |
| 找不到 → | → 停下，用 R13 地图优先 |"""
    },

    "li-docs": {
        "cases": """
## Case Studies

### Case 1: SOP 文档丢失导致任务失败
竞赛区一个项目的 SOP-06（硬件设计铁律）在目录重组时被意外删除。两周后做类似项目时 AI 不知道这些铁律，重复犯了已知错误。
- **教训**：SOP 删除前必须 git checkpoint + 归档——git-recover.md 规则适用于所有文档
- **Source**: .claude/rules/git-recovery.md

### Case 2: 文档格式不统一导致解析失败
5 个工作区的 SOP 格式各异（有的有 YAML frontmatter，有的没有；有的用一级标题，有的用二级）。批量解析脚本因格式不一致输出错误结果。
- **教训**：文档管理的第一步是格式标准化——先统一格式，再做批量操作
- **Source**: mutual/SOPs/sop-indexes.txt

### Case 3: 知识中枢注册表过期
知识中枢的工作区注册表最后一次更新是 5/28，之后新增的 12 个 skill 和 3 个项目没有记录。导致 AI 查注册表时找不到新内容。
- **教训**：注册表更新必须是 skill 创建/修改流程的一部分——不能靠"AI 记得更新"
- **Source**: 知识中枢/00-注册表/工作区注册表.md""",
        "antipatterns": """
## Anti-Patterns

| ID | 反模式 | 理论锚点 | 后果 | 正确做法 |
|----|--------|----------|------|----------|
| AP-DC1 | 文档格式不统一就批量操作 | 跨边界校验 T5 | 解析错误，数据丢失 | 先标准化格式再操作 |
| AP-DC2 | SOP 创建后不更新索引 | 规则结晶 T10 | SOP 存在但 AI 找不到 | 每次 SOP 变更后更新 SOP 总索引 |
| AP-DC3 | 注册表不更新 | 规则结晶 T10 | 新 skill/项目对其他工作区不可见 | 每次结构变更后更新知识中枢注册表 |
| AP-DC4 | 文档只建不维护 | 认知灵活性 T9 | 文档过期误导后续 AI | 每月检查文档时效性，标记 [需刷新] |
| AP-DC5 | 删除文档不归档 | 负结果归档 T7 | 误删无法恢复 | 删前 git checkpoint + 归档目录备份 |""",
        "conditional": """
## Conditional Next Steps

| 条件 | 下一步 |
|------|--------|
| 新建 SOP | → 更新 SOP 总索引 + 知识中枢注册表 |
| 文档格式不一致 | → 先标准化再操作 |
| 删除文档 | → git checkpoint + 归档 |
| 文档过期 | → 标记 [需刷新] + 安排更新 |
| 跨区文档同步 | → li-sync Phase 3 |"""
    },

    "li-personal": {
        "cases": """
## Case Studies

### Case 1: 简历优化 16 版迭代
求职区的简历优化 SOP 经历 16 版迭代——从 v1 的"技能罗列"到 v16 的"STAR 法则 + 量化成果 + 5 维工程语言检查"。每版都有明确的改进点和验证标准。
- **教训**：个人文档的优化是长期过程——每次迭代必须有明确的改进方向和验证标准，不是"改了就好"
- **Source**: 求职/sops/sop-01-简历优化.md

### Case 2: 费曼检验发现知识盲区
用户声称理解了 FPGA 时序约束。用费曼检验要求用类比解释给高中生听——发现"建立时间"和"保持时间"的关系说不清楚。
- **教训**：费曼检验不是形式——真正的理解 = 能用简单类比解释清楚。说不清楚的就是盲区
- **Source**: 个人/sops/sop-01-知识管理SOP.md

### Case 3: 职业规划路径对比
考研（上交/东南电气）vs 就业（威泊机器人研发实习）的决策分析。用 li-devil 泼冷水 + 道法术器四层分析 + 百大认知（双系统理论/锚定效应/反脆弱），最终输出杠铃式方案。
- **教训**：重大决策不能只用一个框架——至少用 2 个正交框架独立分析，结论一致才可信
- **Source**: 个人/sops/sop-02-职业规划SOP.md""",
        "antipatterns": """
## Anti-Patterns

| ID | 反模式 | 理论锚点 | 后果 | 正确做法 |
|----|--------|----------|------|----------|
| AP-PR1 | 费曼检验只走形式 | 刻意练习 T7 | 自以为理解了但实际有盲区 | 解释不清楚的就是知识盲区，必须补 |
| AP-PR2 | 重大决策只用一个框架 | 证据分层 T1 | 框架偏见导致错误决策 | ≥2 个正交框架独立分析 |
| AP-PR3 | 简历/文档只改不验 | 实测优先 T3 | 改了但不知道改得好不好 | 每版迭代必须有验证标准 |
| AP-PR4 | 个人目标不定期复盘 | 认知灵活性 T9 | 目标偏离但不自知 | 每月复盘一次目标达成率 |
| AP-PR5 | 学习笔记只记不检索 | 认知负荷 T4 | 记了但用的时候找不到 | 笔记必须标注关键词+场景，便于后续检索 |""",
        "conditional": """
## Conditional Next Steps

| 条件 | 下一步 |
|------|--------|
| 需要深度学习 | → li-study 学习规划 |
| 需要做重大决策 | → li-devil 泼冷水 + li-analyze 道法术器 |
| 需要优化简历 | → li-analyze + 求职 SOP |
| 需要复盘 | → li-improve Phase 0 自审 |
| 需要规划未来 | → li-plan 长期规划 |"""
    },

    "li-frontend": {
        "cases": """
## Case Studies

### Case 1: HTML 报告自动生成
li-transcript 的 HTML 生成脚本（generate_html.py）将逐字稿清洗结果输出为带样式的 HTML 页面。CSS 样式从 references/style-guide.md 读取，支持 8 种风格切换。
- **教训**：HTML 生成必须内联 CSS（不依赖外部样式表），因为用户可能直接用浏览器打开本地文件
- **Source**: li-transcript/scripts/generate_html.py

### Case 2: Web App Testing 自动化
li-webtest 的 Playwright 脚本对 remotion 项目进行 E2E 测试。35 个测试用例覆盖：渲染正确性、交互响应、性能指标（LCP/FCP）。
- **教训**：E2E 测试不稳定时先检查是否是时序问题（元素未加载就操作），加 `waitForSelector` 解决 90% 的 flaky test
- **Source**: li-webtest/references/test-templates.md

### Case 3: Obsidian 知识库 UI 优化
知识中枢的 Obsidian vault 需要自定义 CSS 主题。直接修改 `.obsidian/snippets/` 下的 CSS 文件，通过 Obsidian 的实时预览即时验证效果。
- **教训**：Obsidian 的 CSS 选择器和标准 Web 不同（用 `.markdown-preview-view` 而不是 `.content`），需要查 Obsidian 开发者文档
- **Source**: 知识中枢/.obsidian/""",
        "antipatterns": """
## Anti-Patterns

| ID | 反模式 | 理论锚点 | 后果 | 正确做法 |
|----|--------|----------|------|----------|
| AP-FE1 | HTML 依赖外部 CSS 文件 | 跨边界校验 T5 | 本地打开时样式丢失 | 内联 CSS 或用 `<style>` 标签 |
| AP-FE2 | E2E 测试不处理时序 | 实测优先 T3 | Flaky test 导致误报 | 关键操作前加 waitForSelector |
| AP-FE3 | 不测试移动端适配 | 防假象审计 T2 | 桌面正常但手机错乱 | 用响应式设计 + 多设备测试 |
| AP-FE4 | 前端代码不压缩就部署 | 实测优先 T3 | 加载速度慢，用户体验差 | 生产环境必须压缩 CSS/JS |
| AP-FE5 | 不处理浏览器兼容性 | 跨边界校验 T5 | 某些浏览器下功能失效 | 测试至少 2 种浏览器引擎 |""",
        "conditional": """
## Conditional Next Steps

| 条件 | 下一步 |
|------|--------|
| 生成 HTML 报告 | → li-transcript HTML 生成 |
| 需要 E2E 测试 | → li-webtest Playwright |
| 需要 UI 优化 | → li-visual 视觉风格 |
| 需要 Web App | → li-scaffold 工作区搭建 |
| 需要部署 | → li-workflow 自动化 |"""
    },

    "li-writing": {
        "cases": """
## Case Studies

### Case 1: 公众号文章生产
用户口述 FPGA 学习路线 → li-transcript 清洗逐字稿 → li-analyze 道法术器拆解 → li-writing 排版输出 → baoyu-post-to-wechat 发布。全流程 30 分钟。
- **教训**：写作不是"写完再改"而是"按 SOP 生产"——流程化比灵感可靠
- **Source**: 创作/sops/sop-00-内容创作总索引.md

### Case 2: 小红书标题优化
电气专业科普帖标题"聊聊 FPGA 的时序约束"。用 li-prompt 的小红书母语模板优化后："⚡FPGA 时序约束 | 90% 的新手都会踩的 3 个坑"。点击率提升 3 倍。
- **教训**：标题优化不是"加 emoji"——需要有数字（具体性）+ 痛点（情感共鸣）+ 专业符号（圈层识别）
- **Source**: li-prompt/references/platform-templates.md

### Case 3: 学术论文润色
用户写的课程论文需要学术风格润色。li-writing 检测到 3 类问题：口语化表达（"我觉得"→"本研究认为"）、引用格式不统一（混用 APA/GB/T 7714）、逻辑连接词缺失。
- **教训**：学术写作和内容创作是完全不同的风格——不能用同一套模板
- **Source**: 学习/sops/""",
        "antipatterns": """
## Anti-Patterns

| ID | 反模式 | 理论锚点 | 后果 | 正确做法 |
|----|--------|----------|------|----------|
| AP-W1 | 写完不检查直接发布 | 证据分层 T1 | 错别字/格式错误/逻辑断裂 | 写完必须过质量检查清单 |
| AP-W2 | 所有平台用同一套文案 | 跨边界校验 T5 | 平台算法降权 + 用户体验差 | 每个平台用 li-prompt 母语模板分别适配 |
| AP-W3 | 追求"完美"反复修改 | 认知灵活性 T9 | 完美主义导致产出为零 | 80% 质量就发布，用数据反馈迭代 |
| AP-W4 | 不参考历史优秀作品 | 实测优先 T3 | 每次都从零开始，不积累 | 写之前先读同主题的历史优秀文章 |
| AP-W5 | 忽略读者的认知负荷 | 认知负荷 T4 | 文章太长/太密，读者放弃阅读 | 用金字塔结构：结论先行，层层展开 |""",
        "conditional": """
## Conditional Next Steps

| 条件 | 下一步 |
|------|--------|
| 需要写公众号 | → li-analyze + li-writing + baoyu-post-to-wechat |
| 需要写小红书 | → li-prompt 平台母语 + li-writing |
| 需要写学术论文 | → li-writing 学术模式 |
| 需要批量生产 | → li-workflow 内容管道 |
| 写作遇到瓶颈 | → li-mindcoach 心力教练 |"""
    },
}

# === INJECT INTO EACH SKILL ===
results = []
for skill_name, content in upgrades.items():
    skill_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    if not os.path.exists(skill_path):
        results.append(f"MISSING: {skill_name}")
        continue

    with open(skill_path, encoding="utf-8") as f:
        existing = f.read()

    # Check what's missing
    has_cases = "## Case Studies" in existing or "## Cases" in existing or "## 案例" in existing
    has_anti = "## Anti-Patterns" in existing or "## Anti" in existing or "## 反模式" in existing

    injection = ""

    if not has_cases:
        injection += content["cases"] + "\n"

    if not has_anti:
        injection += content["antipatterns"] + "\n"

    injection += content["conditional"] + "\n"

    if injection.strip():
        # Insert before the last section (usually metadata or version)
        # Find a good insertion point - before any "## Version" or "## Metadata" or end
        lines = existing.split("\n")
        insert_idx = len(lines)

        # Look for version/metadata section to insert before
        for i in range(len(lines)-1, -1, -1):
            if lines[i].startswith("## Version") or lines[i].startswith("## Metadata") or \
               lines[i].startswith("## 变更日志") or lines[i].startswith("## Changelog"):
                insert_idx = i
                break

        new_lines = lines[:insert_idx] + [""] + injection.strip().split("\n") + [""] + lines[insert_idx:]
        new_content = "\n".join(new_lines)

        with open(skill_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        line_count = len(new_content.split("\n"))
        results.append(f"UPGRADED: {skill_name} -> {line_count} lines")
    else:
        results.append(f"SKIPPED (already has cases+anti): {skill_name}")

print("\n".join(results))
