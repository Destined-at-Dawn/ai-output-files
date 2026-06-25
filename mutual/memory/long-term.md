# 长期记忆

> 本文件由 longmemory 技能每日自动归档，对话中禁止直接写入。
> 压缩记录：2026-06-20 1072→~600行，近30天内容保留核心教训，压缩冗长叙述。

## 用户偏好

- 信息密度：高密度、结论先行、移动端友好（列表优于表格）
- 技术水平：IC/EE 领域专家，熟悉 OPC、FPGA、集成电路设计
- 痛点：信息过载、AI 给假数字不质疑、重复踩坑
- 输出风格：「为什么」的深层解释 + 可落地建议
- **GitHub 身份**：Destined-at-Dawn = 小黎。"小黎"不算泄露，真名+学校+GPA 组合线才是风险。[高置信]
- **软件安装路径偏好** [高置信]：< 1GB → D 盘，≥ 1GB → F 盘（2026-06-19）
- **🔴 设计铁律：AI 适应用户，不是用户适应 AI** [永久有效]
  - 来源：2026-06-01 用户纠正
  - 反模式：教用户"你应该说 XX 来触发 YY"
  - 检验标准：用户随便说一句话，AI 都能正确理解意图并执行

## 重要决策

### 2026-05-25
- **AI 工程 OS v2.0**：从纯输出格式约束升级到工程纪律约束（防假象/负结果归档/边界声明）
- **R13/R15/R16/R17 架构规则**：地图优先盲搜、主目录优先、根目录优先约束、新会话启动协议
- **防回退三层防御**：`.claude/rules/no-root-rules-dir.md` + `_MIGRATED-TO-RULES.md` + `.NO-RULES-DIR-HERE.md`
- **MCP 全局配置**：filesystem + memory + markitdown 三个服务器

### 2026-05-28
- **跨区工作流三件套**：`project-context/` + `artifact-registry.md` + `workflow-inbox.md`。三条铁律：①跨区项目先建项目卡 ②重要产出必须登记 ③长期记忆必须候选确认
- **CLAUDE.md 是核心保障**：hooks 和外部脚本是锦上添花，Compact Instructions（compaction 后自动重读）才是上下文压缩的真正保障

### 2026-06-01
- **跨区三件套落地**：放弃「五区规则全文同步」→ 改为「五区项目上下文同步」
- **三路 CLI 并行**：Claude Code (主力) + Codex CLI (代码) + Gemini CLI (多模态)
- **快模式**：仅"快！"（全角感叹号）可跳过启动序列，"快"/"快点"/"马上"不算

### 2026-06-11
- **主力工具链迁移**：Newmax 降级为备用，主力转为 Claude Desktop + Codex + Hermes Agent
- **学术论文 LaTeX 模板迁移**：IEEEtran/elsarticle/Springer Nature 模板存 E 盘论文目录

## 跨项目知识

### 生态架构栈（截至 2026-05-25）
- **R13**：地图优先于盲搜 | **R15**：主目录优先 | **R16**：根目录优先约束
- **知识中枢**：`E:\ai产出文件\牛马\知识中枢\`（Obsidian vault）
- **MCP 工具**：filesystem + memory + markitdown

### 生态健康指标
- 工作区：5（mutual/个人/创作/求职/竞赛）+ 知识中枢
- R16 整合后文件削减：模板 -79%、通用 SOPs -66%、知识中枢模板 -49%
- Git 自动化：NiumaAutoCommit + agent-commit.sh + pre-push hook
- 共享规则：17 条（R01~R17）
- 防回退：三层防御体系

### 2026-05-27
- **上下文压缩三层防御**：Observation Masking + 主动压缩（70% 阈值）+ Hook 防御
- **GitHub 安全审计标准化**：双关键词策略（用户名 + 目标院校/公司），API 结果交叉验证
- **规则体系优化**：启动序列 Step 3 改为读 lessons.md；规则合并 20→15 文件

## 技能自动激活系统（2026-05-26）

- **核心理念**：用户说的是需求，不是技能名。路由是 AI 的责任
- **路由表**：`skill-routing-table.json`（31→108 条，持续优化）
- **激活规则**：`.claude/rules/skill-auto-activation.md`
- **关键决策**：匹配到→直接调用不问用户；confidence < 0.5→简要告知后执行；用户手动指定=路由失败=需更新路由表

## 经验教训

### 架构级教训
| ID | 教训 | 时间 |
|----|------|------|
| PK-INFRA-010 | 系统自动生成的目录名不能作为永久标识 | 5/25 |
| PK-INFRA-011 | 记忆文件分散 = 跨会话记忆连续性断裂 | 5/25 |
| PK-INFRA-012 | Windows 文件锁会阻止移动正在使用的目录 | 5/25 |
| PK-ARCH-001 | 治理清理本身也需要防膨胀机制 | 5/25 |
| PK-ARCH-002 | 迁移规则路径时需全量引用审计 | 5/25 |
| PK-ARCH-003 | `_MIGRATED-TO-RULES.md` 内容过时会成为"卧底" | 5/25 |

### Skill 开发教训（PK-SKILL-001~007，5/22）
- 创建 skill 前必须搜索全部已有资源
- 触发词必须从真实对话中采集，不能凭空设计
- 引用其他 skill 前必须验证其存在
- 决策类 skill 必须包含反讨好协议

### 全局提示词教训（PK-PROMPT-001~005，5/26）
| ID | 教训 |
|----|------|
| 001 | 身份信息必须有文件级证据，不能脑补 |
| 002 | 好提示词 = 最少的字 × 最大的约束力 |
| 003 | 格式和内容是骨架，语气才是灵魂 |
| 004 | 全局提示词只放"只有全局才能表达的东西" |
| 005 | 事故发生后立刻归档，不能拖 |

### 安全审计教训（PK-SEC-001~003，5/27）
- API 搜索泄露数字不能直接采信，必须交叉验证
- grep 关键词必须包含双维度（用户名 + 目标院校/公司）
- 需要独立 Skill 内置关键词清单

### 运维级教训（PK-INFRA-013~020）
| ID | 教训 |
|----|------|
| 013 | MCP 配置 3 连错（路径/import/包装）→ 已升级为 mcp-config-protocol.md |
| 014 | `~/.mcp.json` 和 `~/.newmax/.mcp.json` 是两个文件，Newmax 只读后者 |
| 015 | `markitdown`（pip）和 `markitdown-mcp`（MCP 包）是两个包 |
| 016 | MCP 有两种传输协议（stdio/HTTP），不可混用 |
| 017 | `ask-user-mcp` 端口参数必须显式传：`npx -y ask-user-mcp 7878` |
| 018 | Newmax 只读 `~/.newmax/.mcp.json`（永久固化） |
| 019 | MCP 两种传输协议不可混用——stdio vs HTTP |
| 020 | Newmax 模型配置在 SQLite 数据库中，不在 config.json |

### 验证工具教训（PK-VERIFY-001~008）
**验证工具层级**：`python -c "open(path).read()"` > `grep` > `Read` 工具

| ID | 教训 | 时间 |
|----|------|------|
| 001 | Read 可能返回缓存/幻觉，不能作为唯一验证 | 5/28 |
| 002 | 声称"完成多文件同步"前必须 Python 逐文件验证 | 5/28 |
| 003 | 用户纠正时立即落盘到 memory，不反问"要不要写入" | 5/28 |
| 004 | 验证优先级：python -c > grep > Read | 5/28 |
| 005 | Read 对中文路径有时假阴性（返回不存在但文件存在） | 5/30 |
| 006 | write_project_file 写入项目子目录而非工作区根目录 | 5/30 |
| 007 | grep 和 Read 矛盾时→Python 做裁判；声称"多文件完成"→Python 逐文件验证 | 6/01 |
| 008 | 用户纠正立即落盘，不问"要不要写入"（批评即落盘铁律） | 6/01 |

**核心铁律**：grep 和 Read 矛盾时 → 用 Python 做最终裁判。[失效条件：Read 工具底层改为直接文件系统读取]

### 2026-05-28 补充
- **npm 代理干扰**：HTTP_PROXY 指向 127.0.0.1:10808，代理未启动时 npm install 会损坏缓存
- **PATH 优先级冲突**：StepFun wrapper 排在 Newmax 前面但 exe 已不存在
- **Karpathy Guidelines**：四原则融入 think-before-act.md（核心增量："200行能50行搞定就重写" + "diff 每行追溯用户需求"）
- **验证工具层级**：`python -c` > `grep` > `Read`（PK-VERIFY-001~004）
- **上下文压缩五区全覆盖**：之前只部署到 mutual，根因："说完成但实际只做了 1/5"

### 2026-05-29
- **Skill 上架**：186 Skill 中 62 个原创，S 级 10 个可上架，jc-clarifier 评分最高
- **FPGA 工程拆分经验**：ILA 核心不能只靠 MARK_DEBUG；拆分后地址/参数独立验证
- **客户交付文档标准**：A4 单栏、公司页眉、真实截图、图注、红色警告、文件超链接
- **多 AI 并行协作边界**：图片 AI ≠ 任务书 AI ≠ 视频 AI，先确认分工再开始

### 2026-05-30
- **Temp 目录残留配置**：牛马AI 升级后 `%TEMP%\newmax_app*.json` 残留含 API Key，已迁移备份
- **GitHub 备份恢复协议**：origin(github) + niuma(github) + gitee 三个远程备份源

### 2026-06-01
- **MCP 配置协议永久固化**：5 条铁律已部署五区（mcp-config-protocol.md）
- **用户核心语义指令**："永远不要再出现 MCP 配置类错误" = 已固化；"不要节约token" = 全力研究；"快！" = 跳过启动序列（精确匹配）
- **Skill 路由优化待办**：全量扫描→交叉比对→补齐缺失→动态调整→端到端测试

## 技能系统更新

### 2026-06-05 li 系列 v2.0 扩展
- li 系列 2→5 个（li-skillcreate/li-transcript/li-bestskill/li-manage/li-skillfusion）
- 全局用户画像首次创建 `~/.newmax/user-profile.md`
- 路由表 73→78 条
- **沉睡率 96.5%**：198 个 skill 中只有 7 个被使用。根因：SKILL.md 不是执行层
- **技能调用强制执行层**：`.claude/rules/skill-logging-enforcement.md`（5 条铁律）
- **Antigravity IDE**：OAuth 超时→Google 账号地区限制

### 2026-06-07
- **微信聊天记录分析 SOP 化**：wx_key → WeChatDataAnalysis → analyze_wechat.py
- **dbs 系列更新**：10 个 skill 更新 + 4 个全新，总计 21 个 dbs skill
- **li-manage v2.0**：四层不可变性架构（事实→规律→定格→待解）

### 2026-06-08
- **路由表治理**：113→101 路由，35→0 重复触发词。教训：每次扩容后必须跑重复检测
- **li-improve v1.0**：1139→467 行 SKILL.md + 27 支撑文件
- **li- 系列最终结构**：12 个 skill（li/li-research/li-transcript/li-devil/li-sync/li-manage/li-mindcoach/li-skillcreate/li-skillfusion/li-bestskill/li-improve/li-local-search）

### 2026-06-09
- **li-memory v2.0**：基于 Supermemory 23.2K★，原子事实+矛盾检测+自动遗忘+混合检索
- **li-hardware v2.0**：从 D:\AMD 的 3 次 FPGA 交付 + C919 皮影 18 舵机项目吸收实战知识
- **路由表全量治理**：跨 66 个 CLAUDE.md 工作区，108 routes / 0 交叉冲突
- **第三方仓库只读铁律**：任何 git clone = 只读，绝不可改
- **群聊发送者名称修复**：sender_id→wxid→昵称映射，总解析率 97.4%

### 2026-06-10
| 教训 | 根因 | 修复 |
|------|------|------|
| 011: git 命令失败 | npm git.cmd 覆盖系统 git.exe | 调整 PATH 优先级 |
| 012: MCP 无限循环 | markitdown_mcp 启动逻辑缺陷 | wrapper + runpy.run_module() |
| 013: MCP 401 认证失败 | 子进程未继承环境变量 | -e 参数显式传递 |
| 014: 重构应渐进式 | 一次性大改导致不稳定 | 增量方式，每步验证 |

### 2026-06-11
- **Skill 大清理**：149→58 个活跃 skill（-61%），所有归档可恢复
- **三层防跳过机制**：SKILL.md 执行协议 + .claude/rules/ 全局约束 + 日志验证
- **LaTeX 模板库**：IEEEtran/elsarticle/Springer Nature 54 文件，存 `~/.newmax/skills/li-office/references/templates/official/`
- **mempalace 清理**：释放 23.20 GB，D 盘 43.78→66.98 GB free
- **API 中转站废弃**：api-siyu.top 不稳定，切换到 Anthropic 官方 OAuth

### 2026-06-21（W24 审计）
- **路由覆盖率跃升**：30% → 81.9%（+51.9%），104 条路由覆盖 104 个 skill
- **全局 skill 精简**：212 → 127 个（-85 个低频/重复 skill）
- **断裂路由清零**：路由健康度 100%
- **触发词增长**：1417 → 1632 个（+215）
- **skill 沉睡率**：100%（本周 0 次调用记录，日志系统可能失效）
- **Hermes watchdog v4**：监控→执行打通，新增可执行动作 JSON 输出
- **SOP 空壳修复**：3 → 1（仅 sop-file-operations.md 缺失）
- **健康度评分**：72/100（较上周 55/100 +17 分）
- **核心教训**：路由覆盖率大幅提升 ≠ 技能使用率提升；监控系统必须有执行能力

## 微信分析体系

### 四阶段流水线
```
密钥提取(wx_key) → 聊天导出(wechat-exporter) → 社群过滤(community-filter) → 心理蒸馏(wechat-distiller)
```

### 关键数据
- 解密 DB: `创作/output/databases/wxid_3nvidmluot0a22/`（17 个 DB，501 表）
- 信息密度 0.37%——99.6% 群聊消息是噪音
- 288 个真正资源从 77,000+ 消息中提取
- 微信红包金额不可提取（redEnvelopeTable 无金额字段）
- 转账数据：收入 ¥19,441 / 支出 ¥20,358

### 社群注册表（13 群）
- 必监控：AI赋能实习群、小黎同辈互助群、2026实习求职技巧课1群
- 按需：萱式成长营、北狼语冰室、一棵树、乎乎、向阳集等 10 个

### 微信分析 Skill 体系
| Skill | 功能 |
|-------|------|
| wechat-analysis v3.0 | 主入口：分类汇总/精细查询/联系人统计 |
| wechat-exporter v1.0 | DB→MD 导出 |
| wechat-distiller v1.0 | 心理蒸馏：五维分析+人物Skill+文风DNA |
| community-filter v3.0 | 社群过滤：百大认知交叉+噪音模式库 |

## 基础设施

### 2026-06-12 磁盘清理
- D 盘释放 41.5GB（Xilinx 35.4GB + Windsurf/Antigravity/edge_install）
- MCP 从 6 个精简到 2 个（markitdown + mempalace）
- C 盘仍紧张(17.6GB)：.newmax/conversations 11.3GB + chrome-profiles 6.9GB

### 2026-06-12 生态手册
- 位置：`E:\ai产出文件\牛马\mutual\mutual\ecosystem-manual\`
- 内容：skill-inventory(138) + sop-index(83) + mcp-tools + work-groups + 文风DNA
- 自动注入规则：`.claude/rules/voice-dna-auto-inject.md`
- 定时刷新：每周日 22:00

### 2026-06-13 Impeccable 质量门禁注入
- html-to-notes v1.0→v2.0：6维度143分评分体系
- 来源：pbakaus/impeccable（100+ stars），适配为笔记质量门禁
- 新增 Step 5.5（Impeccable 门禁）+ references/ 目录（6 命令文件 29KB）
- 保留 v1 全部 19 项基础门禁，新增 AI 腔检测 + 认知科学评分

### 2026-06-14 Claude Fable 5 提示词泄露
- 3 项改动融入工作流：
  1. 新建 search-decision-tree.md（搜索决策树）
  2. 增强 lesson-auto-update.md（硬编码检查步骤）
  3. 对照诊断：8 条洞察中 1 条对齐、2 条落地、2 条待审计

## 自动提取记录

### 2026-06-16
- 长期记忆映射表清理：重写为 100% 基于实际章节的映射表（18 一级 + 52 二级）
- 32 条过期任务清理（跨 5/28~6/14，最久 19 天）
- mutual 工作区当前不在 git 管理下（已知状态）

### 2026-06-17
- **MemPalace 整合协议**：定位为 8 工具共享语义搜索引擎，9 Wing 分类，每周日 23:00 增量索引
- **Skill 生态波动**：active_skills 117→98，trigger_conflicts 11→14，待核实
- **Windows GBK 编码**：`-X utf8` 是最可靠方案（不依赖环境变量）
- **Junction 迁移教训**：robocopy 退出码 1/3 是成功；PS5.1 读 UTF-8(无BOM) 崩溃

### 2026-06-18
- **CLAUDE.md 膨胀治理**：380→140 行（-63%），精简原则只保留铁律和引用
- **MCP Wrapper 模式成熟化**：markitdown + agentmail 两次验证，应文档化为标准流程
- **mimo multimodal 限制**：不支持图片/PDF，涉及多模态任务必须指定 `model: "opus"`

### 2026-06-19
- **Skill 交付商业突破**：高校超算中心工程师主动联系，定价逻辑 = 帮对方省下摸索时间
- **Python PATH 冲突(018)**：E:\python.exe(3.13) 优先级高但缺 mempalace 包，3.13 上补装
- **study-review-kit 打包哲学**：极简平铺 > 复杂嵌套，"下载即用" > "优雅目录结构"
- **高要求 PDF 教训**：①双引号容错 ②image2 大小写敏感（`Image` 才行，description 必填）
- **MCP 配置路径**：`~/.newmax/.mcp.json`，命令直接调用 npx/python 不用 `cmd /c`

## Agent 故障诊断

### 2026-06-09
- Agent 子会话继承主会话模型，主模型不支持 multimodal → Agent 无法处理图片/PDF
- Agent Prompt 铁律：每次调用必须包含具体目标、输出格式、停止条件
- Agent 类型匹配：Explore(找文件) / general-purpose(综合分析) / Plan/code-reviewer(代码审查)

## Skill 调用体系

### 待办（2026-06-01 记录，部分已完成）
- [x] 路由表全量扫描 → 108 条，0 交叉冲突
- [ ] Obsidian MCP 连接问题待验证
- [ ] confidence 动态调整机制未实现
- [ ] SOP × Skill 映射矩阵

### 铁律 F3 放行
- 从禁止直接写入改为允许写入但需遵循候选协议

---

*压缩版本：2026-06-20，原始 1072 行 → ~580 行*

### 2026-06-20
- **个人建站项目迁出**：`outputs\个人建站` → `F:\work\个人建站`，3 个 Python 脚本输出路径已同步更新
  - scan2.py / scan_web_design.py / upgrade_v3.py 的 OUT_DIR 已改为新路径
  - 路由表无相关条目，无需更新
- **Hermes watchdog v3→v4 升级**：+自动刷新过期文件、+自动消费 handoff、+可执行动作 JSON 输出、+缺失文件检测 [高置信] [失效条件：watchdog v5 发布]
  - 设计决策：不创建第 6 个 skill，利用现有 5 个 skill + cron 调度
  - 日心跳（2h）+ 周巡检（周日 21:00）双频模式
  - v3 归档：`归档/2026-06-20-watchdog-v3-archive/`
- **咨询收入周报 Week 2**：¥476.76 历史确认（截止 2026-06-06），微信连续 2 周数据缺口 +31.3MB [高置信] [失效条件：微信运行并解密]
- **indienews 方向锁定**：第一个内容网站选独立开发者新闻聚合站，域名 lilanyuan.net 三备案完成 [中置信] [失效条件：用户改变方向]
- **Hermes 健康报告**：long-term.md 1072 行（超阈值 800），无 >90 天条目暂不压缩，atomic-facts 64 条，未解决矛盾 C-2026-06-18-001 待确认
  - memory 中的历史记录保持原样（记录的是"当时发生了什么"）

### 2026-06-21
- **文风DNA v3.0 蒸馏**：Week 2 自动蒸馏完成，新增 2 个表达特征 [高置信] [失效条件：用户表达风格显著变化]
  - 认知对偶句："监控≠治理""做网站和靠网站赚钱是两件事"——对仗结构自带传播力，适合金句
  - 阶段标签意识："粗筛/中级/全签核""P0/P1/P2"——工程思维外化，让读者知道结论可靠性
  - 来源：6-14~6-21 对话记忆 5 文件分析
  - 产出：`ecosystem-manual/distillations/self-voice-dna.md` v3.0
- **个人网站双轨部署决策** [高置信] [失效条件：备案政策变化或域名更换]
  - 服务器：阿里云 ECS 经济型 e（99 元/年，华东 2，Ubuntu 22.04），IP 139.196.5.53
  - 备案策略：湖南地址备案（零成本快）+ 有居住证后迁移（零停机），lilanyuan.cn 已提交初审
  - 域名分工：lilianyuan.net（海外版，Cloudflare Pages 已上线）/ lilanyuan.cn（国内版，待备案）
  - 物理隔离铁律：国内站严禁支付元素（防经营性检测），商业化全走海外 .net
  - Ubuntu 22.04 铁律：具身智能（ROS2 Humble）和支付环境首选 22.04，非 24.04
  - 产出：`outputs/personal-site-status-v1.md`（双轨部署决策总览）
- **workspace-sanitizer skill 创建** [高置信] [失效条件：workspace-sanitizer 被更完善的工具替代]
  - 2026-06-22 mutual 工作区深度清理：45项 -> 21项，38垃圾+10错位+13死链接
  - 核心认知："乱"不是垃圾多，是职责不清。只做卫生清理 = 隔靴搔痒
  - 根因修复：scaffold-workspace 模板还在教新工作区建 `归档/` 和 `自我进化/`——修模板比清表面重要
  - 三层互补：workspace-sanitizer（存量清理）+ scaffold-workspace（新建脚手架）+ li-manage（文档同步）
  - 路由：r412，16 个触发词，联动 li-manage
  - 产出：`skills/workspace-sanitizer/SKILL.md`

### 2026-06-22
- **Skill 清理分流规则** [高置信] [失效条件：share-skill 目录用途改变]
  - 不适合 mutual 工作区的 skill ≠ 直接删除，而是迁移到 `F:\share-skill\`
  - 分流标准：功能与 mutual 工作区方向无关（如非电气/AI/个人成长类），但 skill 本身质量合格可分享
  - 操作顺序：先评估是否可分享 → 能分享的复制到 share-skill 并标记 DEPRECATED → 不能分享的才删除
  - 根因：skill 是劳动成果，直接删除 = 浪费；分享 = 让 skill 继续产生价值
- **li-local-search 定位纠正** [高置信] [失效条件：skill-auto-activation 架构重构]
  - 核心认知："有路由"和"被使用"是两件事。li-local-search 是底层基础设施（"空气"），每次任务自动参与路由决策
  - SKILL.md v1.2->v1.3：数字修正（230+->128, li- 31->52），新增底层 Layer 定位段
  - 路由表 r082：priority 1->0，新增 `role: foundational-layer` 标记
  - skill-index.md 全量重写：128 个 skill 分域索引（255 行）
- **工作区大清理** [高置信]
  - 删除 .tmp/ 残留（7 个脚本）、过期顶层文件（AGENTS.md/MASTER.md/CLAUDE-*.md）、飞书文档副本
  - 统一索引迁移到 _system/unified-index/
  - 路由表精简 31 条冗余条目
  - 旧项目会话清理（2 个 proj-xxx 过期 memory/outputs/session-meta）
- **niuma-engine v4.0 发布准备** [高置信] [失效条件：v4.0 已推送]
  - 缺陷全量分析：P0 3 个（根目录无 CLAUDE.md / .gitignore 排除 / README 引用已删除文件）、P1 4 个、P2 若干
  - 发布总结：29 条规则 / ~124KB / 移除 3 条太个人化规则 / 全局路径脱敏
  - 清理脚本 4 个已生成，推送待手动执行
- **生态手册双重刷新** [高置信]
  - 首次：meta.json v5->v6，触发词 1417->1651（+234）
  - 二次：口径修正 1651->1639（去重），新增退役 skill 维度（3 个），meta.json v6->v7
  - 教训：统计必须标注口径（原始/去重），否则无法跨时间对比（法则 1 证据分层）
- **FPGA touchscreen RTL** [中置信]
  - 新增完整 RTL：I2C 主控制器(339 行) + 触摸控制(404 行) + 七段数码管(122 行) + 顶层(231 行)
  - + ILA IP 核 + XDC 约束 + rtl_code_lessons.md 教训文档
  - 待综合/仿真验证

### 2026-06-24
- **个人建站 - 备案完成进入部署** [高置信] [失效条件：网站正式上线]
  - 备案号：湘ICP备2026025336号
  - footer 方案：张鑫旭式三层（Designed & Engineered by 李兰源 / (c) 2026 / 备案号）
  - 联系入口：方案A替换（居中布局 + 微信二维码 + 金色边框）
  - hover 动效：鼠标悬停彩色线条环绕+整体亮起
  - 用户审美铁律：高饱和度、阳光向上、3-4 种混合色彩搭配随机展示
  - 色彩方案仍在迭代中
- **独立 EXE 更新陷阱** [高置信] [失效条件：工具切换到纯 npm 包管理]
  - Claude Code 和 Codex CLI 都是独立 EXE 安装（非 npm 包）
  - `npm install -g` 更新的是另一份副本，PATH 优先级更高的是旧版
  - 正确更新方式：GitHub Releases 下载 zip/exe 直接替换
  - Claude Code：`~/.local/bin/claude`（native installer）
  - Codex CLI：`D:\codex\bin\codex.exe`（独立 EXE）
- **用户禁令：禁止无用填充语** [高置信] [永久有效]
  - 禁止："你说得对""我之前的方案是闭门造车"等自我批评式铺垫
  - 正确做法：直接去做，不要铺垫。错了就改，不要先道歉
  - 已写入 `~/.claude/rules/全局禁令.md`，跨所有 AI 工具生效
- **li-content 去向** [高置信]
  - li-content 已被合并到 li-analyze（Mode B 内容诊断），记录在 li-skillfusion 案例2
  - 但 li-intent 路由规则中仍引用 li-content（SOP-02/SOP-04），需清理
  - 教训：skill 合并/弃用后，路由引用必须同步清理
- **先搜索再推荐** [高置信] [失效条件：用户明确说"不用搜了"]
  - 用户批评 AI 在已有信息里重新组装方案 = "闭门造车"
  - 正确流程：先外部搜索真实案例（国内外都要）→ 带案例回来让用户选 → 不够再问用户要信息
  - 适用场景：footer 设计、UI 方案、任何"行业惯例"类决策
