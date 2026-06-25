# 原子事实库（Atomic Facts）

> 由 Hermes 从各工作区 artifact-registry.md 提取。
> 格式：`[事实] [来源: path#line] [置信度] [时间]`
> 每次写入前必须与已有事实做矛盾对比。

---

## 架构与治理
- [事实] 牛马AI 生态治理核心要义总纲已存在，含 10 条根本原则 + R16 架构全景 + 28 轮迭代方法论 [来源: mutual/artifact-registry.md#ART-20260525-001] [置信度: 高] [时间: 2026-05-25]
- [事实] 牛马AI 工作流全景地图 v1.0 已完成，覆盖五区+知识中枢+MCP+Hook+CLI+181 Skill，24000 字 [来源: mutual/artifact-registry.md#ART-20260528-002] [置信度: 高] [时间: 2026-05-28]
- [事实] 15 轮迭代产出已归档至 E:\ai产出文件\牛马\归档\2026-05-28-workflow-15-iteration\，状态 archived [来源: mutual/artifact-registry.md#ART-20260528-003] [置信度: 高] [时间: 2026-05-28]
- [事实] 跨区工作流三件套已落地：project-context/ + artifact-registry.md + workflow-inbox.md [来源: mutual/memory/long-term.md#2026-05-28] [置信度: 高] [时间: 2026-05-28]
- [事实] PROJ-20260528-001（生态优化）状态 Active，五区中仅 mutual 进行中，其余四区待启动 [来源: mutual/project-context/PROJ-生态优化.md] [置信度: 高] [时间: 2026-05-28]

## CLI 工具
- [事实] 三路 CLI 配置已总结：Claude Code + Codex CLI + Gemini CLI [来源: mutual/artifact-registry.md#ART-20260528-004] [置信度: 高] [时间: 2026-05-28]
- [事实] 三路模型切换配置已记录：mimo/opus/gpt/deepseek [来源: mutual/artifact-registry.md#ART-20260528-005] [置信度: 高] [时间: 2026-05-28]

## 研究
- [事实] 上下文压缩研究报告已完成，28 轮迭代的方案设计 [来源: mutual/artifact-registry.md#ART-20260527-001] [置信度: 高] [时间: 2026-05-27]
- [事实] 工作流优化研究报告已完成，GitHub/YouTube/X 三平台研究，30+ 发现 [来源: mutual/artifact-registry.md#ART-20260528-006] [置信度: 高] [时间: 2026-05-28]

## 安全
- [事实] comemo 安全审计报告已完成 [来源: mutual/artifact-registry.md#ART-20260528-007] [置信度: 高] [时间: 2026-05-28]

## 用户身份与偏好
- [事实] 小黎 = Destined-at-Dawn (GitHub)，上海电力大学电气工程专业 [来源: mutual/memory/long-term.md] [置信度: 高] [时间: 2026-05-25]
- [事实] 用户偏好：信息密度高、结论先行、移动端友好、列表优于表格 [来源: mutual/memory/long-term.md] [置信度: 高] [时间: 2026-05-25]
- [事实] 设计铁律：AI 适应用户，不是用户适应 AI [来源: mutual/memory/long-term.md#2026-06-01] [置信度: 高] [时间: 2026-06-01] [失效条件: 用户明确推翻]

## Skill 生态（2026-06-11 最新）
- [事实] 活跃 skill 58 个（38 li- + 20 非 li-），从 149 个精简 61% [来源: mutual/memory/2026-06-11.md] [置信度: 高] [时间: 2026-06-11]
- [事实] 8 个 mutual 全局 SOP 已验证，37 个工作区路由表已同步 [来源: mutual/memory/2026-06-11.md] [置信度: 高] [时间: 2026-06-11]
- [事实] li- skill 执行协议三层防跳过机制已落地：SKILL.md 执行协议 + .claude/rules/ 全局约束 + 日志验证 [来源: mutual/memory/2026-06-11.md] [置信度: 高] [时间: 2026-06-11]

## API 与基础设施
- [事实] api-siyu.top 中转代理已废弃，切换到 Anthropic 官方 firstParty OAuth [来源: mutual/memory/2026-06-11.md] [置信度: 高] [时间: 2026-06-11]
- [事实] dan-koe-insights-premium npm 包已删除（1.7GB），C 盘释放到 20.6GB [来源: mutual/memory/2026-06-11.md] [置信度: 高] [时间: 2026-06-11]
- [事实] 可复刻包 v1.2 已产出（26 files, 51KB） [来源: mutual/memory/2026-06-11.md] [置信度: 高] [时间: 2026-06-11]

## 四位一体架构
- [事实] 四位一体架构 v1.0 于 2026-06-09 创建：Hermes + Newmax + Codex + WorkBuddy [来源: 知识中枢/02-共享规则/工具协同协议/00-四位一体协同总纲.md] [置信度: 高] [时间: 2026-06-09]
- [事实] Hermes Agent 职责规范 v1.0 定义五大核心职责：事实提取/矛盾检测/上下文注入/自动遗忘/跨工具状态追踪 [来源: 知识中枢/02-共享规则/工具协同协议/hermes-agent-职责规范.md] [置信度: 高] [时间: 2026-06-09]
- [事实] Hermes 记忆存储位于 知识中枢/01-工作区记忆/hermes-memory/ [来源: hermes-memory/README.md] [置信度: 高] [时间: 2026-06-11]

---

## 工具生态（2026-06-11 扫描）
- [事实] 小黎使用 6 个 AI 工具：Newmax + Claude Code + Codex + Hermes + WorkBuddy + Gemini [来源: .claude/CLAUDE.md + .newmax/ + .codex/ + .workbuddy/ + .gemini/] [置信度: 高] [时间: 2026-06-11]
- [事实] Newmax 拥有 104 个 skill，其中 48 个 li- 系列（小黎专属），56 个通用工具 [来源: .newmax/skills/] [置信度: 高] [时间: 2026-06-11]
- [事实] Newmax MCP 服务器：filesystem + memory + obsidian + mempalace + paddleocr + markitdown（共 6 个） [来源: .newmax/.mcp.json] [置信度: 高] [时间: 2026-06-11]
- [事实] WorkBuddy MCP：connector-proxy（飞书 + tmeet） [来源: .workbuddy/.mcp.json] [置信度: 高] [时间: 2026-06-11]
- [事实] Telos 系统（.claude/telos/）包含 8 个文件，是小黎个人信息的单一真相源 [来源: .claude/CLAUDE.md#Telos] [置信度: 高] [时间: 2026-06-11]
- [事实] .claude/CLAUDE.md 定义 6 条 CRITICAL RULE，优先级高于系统提示词 [来源: .claude/CLAUDE.md] [置信度: 高] [时间: 2026-06-11]
- [事实] Codex 拥有 4 个 li- skill：li-skillcreate/li-skills-mgmt/li-infra/li-sync [来源: 05-每日记忆/2026-06-13-Codex-skill-sop-hermes-handoff.md] [置信度: 高] [时间: 2026-06-13]
- [事实] Codex 与 Hermes 协作规则：读 hermes-memory 三文件但不写入，交接写到 05-每日记忆/ [来源: 05-每日记忆/2026-06-13-Codex-skill-sop-hermes-handoff.md] [置信度: 高] [时间: 2026-06-13]
- [事实] Marvis（应用宝桌面AI助手）E:\Marvis\，22 skill + 2 MCP server（win_use_mcp/yyb_alg_mcp） [来源: E:\Marvis\MarvisAgent\1.0.1000.104\skills\] [置信度: 高] [时间: 2026-06-13]
- [事实] 统一协作规则：所有工具可读 hermes-memory 但不写入，交接写到 05-每日记忆/ [来源: tool-ecosystem-scan.md#统一协作规则] [置信度: 高] [时间: 2026-06-13]
- [事实] 小黎已转专业成功：集成电路设计与集成系统 → 电气工程及其自动化（2026-06） [来源: .claude/telos/identity.md] [置信度: 高] [时间: 2026-06-07]
- [事实] 小黎双重企业身份：上海皮赛仪器 AI 流程工程师 + 蓓伟机器人具身智能实习生 [来源: 用户直接确认] [置信度: 高] [时间: 2026-06-19]
- [事实] 小黎核心职业目标：常州电网市局（保底）+ 具身智能/电气化（长期） [来源: 用户直接确认] [置信度: 高] [时间: 2026-06-19]
- [事实] 小黎个人知识库：飞书文档 https://vcnogbywj044.feishu.cn/wiki/G49awLm91i2ZObkWXBmcLnmFncf [来源: 用户直接确认] [置信度: 高] [时间: 2026-06-19]
- [事实] 小黎暑期将去注册资本 2 千万的具身智能企业做 AI 化迭代工作流 [来源: .claude/telos/identity.md] [置信度: 高] [时间: 2026-05-28]
- [事实] 小黎小红书已放弃，副业聚焦公众号+微信朋友圈 [来源: .claude/telos/identity.md] [置信度: 高] [时间: 2026-06-07]

## 微信数据分析（2026-06-15）
- [事实] 微信红包金额无法从本地数据库提取（redEnvelopeTable 710条无金额字段），转账已完整提取：收入30笔¥19,441.02/支出38笔¥20,358.72；咨询周报定时任务因数据不足已取消 [来源: mutual/projects/proj-1779089173658-j5tg2m/memory/2026-06-15.md] [置信度: 高] [时间: 2026-06-15]
- [事实] 微信分析产出：transfers_summary.json（68笔）、red_envelopes_full.json（710条元数据）、consulting-weekly-2026-06-14.md（首期周报） [来源: mutual/projects/proj-1779089173658-j5tg2m/memory/2026-06-15.md] [置信度: 高] [时间: 2026-06-15]

## 行业动态（2026-06-15）
- [事实] VLA成为具身智能核心范式（自动化学报/arXiv/CCF综述），Figure AI估值390亿美元，具身智能2025市场192亿元预计2035年万亿（CAGR 73%），已上升为国家战略 [来源: 求职/memory/2026-06-15.md] [置信度: 高] [时间: 2026-06-15]
- [事实] 科研日报-无人机自动巡检 2026-06-15 已产出：15 篇论文（4 S级/8 A级/3 B级），核心趋势 = YOLO26 成事实标准 + 安全约束形式化 + 注意力机制架构化 + LLM/Agent 嵌入视觉任务 [来源: 创作/科研日报/产出/科研日报-无人机自动巡检-2026-06-15.md] [置信度: 高] [时间: 2026-06-15]

## 生态健康（2026-06-15）
- [事实] 生态健康度 7.5/10：Skill 111个（90活跃/19弃用），路由97条，断裂路由1个（wechat-consultant r400），孤儿Skill 7个，技能使用日志停滞10天（最后06-05） [来源: mutual/outputs/daily-audit/2026-06-15-ecosystem-audit.md] [置信度: 高] [时间: 2026-06-15]
- [事实] C919 模板填充教训已闭环：模板填充只能"打开模板→填内容→局部修正→校验结构未变"，禁止"重做文档" [来源: 创作/自我进化/做得差的避免/20260614_C919任务书模板填充失败教训.md] [置信度: 高] [时间: 2026-06-14]

## 技术研究（2026-06-15）
- [事实] SkVM论文品读完成：上海交大Skill虚拟机，AOT+JIT双层编译，成功率+15.3%/Token-40%/加速3.2倍；信息差三件内容已产出（社群稿+公众号+小红书） [来源: 创作/projects/proj-1777084456942-plvse9/outputs/] [置信度: 高] [时间: 2026-06-15]
- [事实] ljg-skills融合分析完成：21个skill精读，与li-*重叠<10%，高价值融合4个（ljg-think/ljg-rank/ljg-book/ljg-plain） [来源: mutual/projects/proj-1779089173658-j5tg2m/outputs/ljg-skills-融合分析v2.md] [置信度: 高] [时间: 2026-06-15]
- [事实] 教训闭环执行看板创建，13 个操作全部完成（含 6 区 CLAUDE.md Hermes 协作规则同步 + 创作 SOP 更新 + 路由表修复） [来源: 知识中枢/05-每日记忆/教训闭环执行看板.md] [置信度: 高] [时间: 2026-06-15]
- [事实] li-cicc-robei-fpga Skill 由 Codex 创建，用于 FPGA 竞赛 Robei 项目（代码风格迁移/报告措辞视觉/提交包证据结构） [来源: 05-每日记忆/2026-06-17-Codex-Robei集创赛Skill优化.md] [置信度: 高] [时间: 2026-06-17]
- [事实] Robei 往届优秀作品对标分析已完成：代码文档视觉对标、风格迁移建议、报告/PPT 措辞迁移清单、提交包证据结构优化 [来源: 05-每日记忆/2026-06-17-Codex-Robei集创赛Skill优化.md] [置信度: 高] [时间: 2026-06-17]
- [事实] 用户纠偏：电路分析高要求复习 PDF 主证据必须是原资料截图或 AI 视觉融合展示，Source 路径仅作辅助追溯 [来源: 05-每日记忆/2026-06-18-Codex-电路PDF证据逻辑纠偏.md] [置信度: 高] [时间: 2026-06-18]
- [事实] li-webstyle Skill 由 Codex 创建：网页风格学习与多样化 HTML 生成，已三工具同步，路由 r319/r243/r327 [来源: 05-每日记忆/2026-06-19-Codex-li-webstyle.md] [置信度: 高] [时间: 2026-06-19]
- [事实] study-review-kit 出图链路更新：默认 Codex 内置 image_gen，image2/baoyu-image-gen 仅非 Codex fallback [来源: 05-每日记忆/2026-06-19-Codex-study-review-kit-imagegen.md] [置信度: 高] [时间: 2026-06-19]
- [事实] study-review-kit 介绍页审计完成：新增 PyTorch 26 题学习矩阵，baoyu-image-gen 随包交付确认 [来源: 05-每日记忆/2026-06-19-Codex-study-review-kit审计.md] [置信度: 高] [时间: 2026-06-19]

## 协作规则部署（2026-06-14，2026-06-21 auto-consumed）
- [事实] 2026-06-14 教训闭环：4 条教训共同根因 = "动手前检查"门禁缺失，已部署 pre-action-check.md 到 7 个工作区（mutual/个人/创作/学习/求职/竞赛/日常学习） [来源: 05-每日记忆/2026-06-14-Hermes-教训闭环-执行清单.md] [置信度: 高] [时间: 2026-06-14]
- [事实] Hermes 记忆中枢协作规则已部署到 4 个工具：.claude/CLAUDE.md + .codex/AGENTS.md + .newmax/CLAUDE.md + .workbuddy/CLAUDE.md [来源: 05-每日记忆/给{ClaudeCode,Codex,Newmax,WorkBuddy}-追加Hermes协作规则.md] [置信度: 高] [时间: 2026-06-14]
- [事实] Marvis rules.md 追加 Hermes 协作规则待确认（文件路径 E:\Marvis\MarvisAgent\1.0.1000.104\prompts\core\rules.md） [来源: 05-每日记忆/给Marvis-追加Hermes协作规则.md] [置信度: 中] [时间: 2026-06-14]
- [事实] 教训闭环要求：写脚本→li-script 自动路由（skill-routing-table.json），但该文件不存在，任务可能已过时 [来源: 05-每日记忆/给ClaudeCode-教训闭环-路由表和检查规则.md] [置信度: 中] [时间: 2026-06-14]

## SOP 维护（2026-06-18）
- [事实] SOP-13重构时删除，内容迁至templates/FPGA-RTL类/案例-AMD_FPGA.md，竞赛区2文件旧引用已修复 [来源: 05-每日记忆/2026-06-18-Hermes-SOP13残留引用修复建议.md] [置信度: 高] [时间: 2026-06-18]

## 实习与职业（2026-06-18）
- [事实] 威泊机器人实习已落地：闵行租房已定，6.18-26考试周后30号正式开始；首项目=7A35T FPGA实验箱文档；待遇=ChatGPT PRO报销+津贴阶梯1k/3k/5k/10k+下学期远程 [来源: 个人/个人/memory/2026-06-18.md] [置信度: 高] [时间: 2026-06-18]
- [事实] telos四文件已同步更新（威泊实习/考试安排/嵌入式软件+AI流程智能化+商业认知技能/创业者心态）；小黎微创业野心：学全链路，AI+制造业是风口 [来源: 个人/个人/memory/2026-06-18.md] [置信度: 高] [时间: 2026-06-18]

## 学习与竞赛（2026-06-18）
- [事实] 电路分析source-first exam mode SOP落地：先建资料索引+原题库再做复习PDF；study-review-pdf skill三工具同步，跨工具skill创建铁律确立（三同步+三路由） [来源: 日常学习/memory/2026-06-18.md] [置信度: 高] [时间: 2026-06-18]
- [事实] 电路分析第13章复习PDF v2已生成（8页），全量资料核验131个文件；FPGA安全通信项目Robei资料提取完成（8文件+16工程文件） [来源: 日常学习+竞赛/memory/2026-06-18.md] [置信度: 高] [时间: 2026-06-18]

## 复习PDF方法论（2026-06-20 新增）
- [事实] 高要求复习PDF必须用Codex内置image_gen直出完整成品图，禁止用Markdown/HTML/PIL/Matplotlib/ReportLab/LaTeX排版冒充；本地工具仅允许源材料整理+图片装订PDF+页数验证；每章至少1-2页拔高综合页 [来源: 05-每日记忆/2026-06-20-Codex-study-review-pdf-imagegen-sop-skill.md] [置信度: 高] [时间: 2026-06-20]

---

> 最后更新：2026-06-21
> 事实总数：59（新增 +4，来源：8 个过期 handoff auto-consumed）
