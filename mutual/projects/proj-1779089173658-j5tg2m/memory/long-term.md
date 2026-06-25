## 2026-06-20 自动提取
- 用户要求自动化解决群成员信息提取问题，用于社交网络分析
- 用户需要助手优化其文风DNA和私域运营心法，并创建对应的咨询agent
- 用户确认当前已知咨询收入为 ¥476.76，但怀疑存在更多未记录的收入，要求彻底查找
- 用户的微信数据库中存在群聊成员列表（chatroom_member 表），之前分析因未读取 contact.db 而错过
- 用户的微信转账和红包记录位于 general.db，包含 68 笔转账和 710 条红包记录，是收入分析的重要数据源

## 2026-06-12 微信数据库全量自动化工程

### 数据库定位
- **最新加密DB路径**：`D:\data\wechat\xwechat_files\wxid_3nvidmluot0a22_72ff\db_storage\message\message_0.db`（342.8MB，6/12 19:37更新）
- **旧解密DB路径**：`E:\ai产出文件\牛马\创作\创作\output\databases\wxid_3nvidmluot0a22\message_0.db`（330.8MB，6/7 数据）
- **wx_key工具**：v2.1.8 已安装（`pip install wx_key`），需微信进程运行才能提取密钥

### Phase 1 现状：需用户打开微信
- wx_key 通过 DLL Hook 注入提取密钥，无法离线解密
- 已复制最新加密DB到 outputs/databases/latest/
- 备选：sqlcipher3 已安装可用，需正确密钥

### Phase 2 产出（extract_full_data.py v2.0）
- **WCDB Schema**：列名是 create_time（不是 CreateTime）、real_sender_id、message_content
- **sender_id=2 永远是用户**（已验证3个私聊会话）
- **群聊消息前缀为 sender_wxid:\n 格式**
- **产出目录**：`E:\ai产出文件\牛马\创作\创作\output\wechat_analysis\`
  - all_sessions.json（492会话）
  - top_private.json（Top 20 私聊）
  - top_groups.json（Top 20 群聊）
  - transfers.json（30收入+38支出+710红包）
  - group_members.json（140个群，15225成员）
  - corpus.json（33431条消息）
  - data_summary.md（Markdown报告）

### Phase 3 产出（文风DNA v2.0）
- **源文件**：`ecosystem-manual/distillations/self-voice-dna.md`
- **关键发现**：
  - 私聊中位数 8字，55.7%不到10字（碎话模式）
  - 群聊感叹号率13.9%，是私聊的5倍（主持人模式）
  - 私聊"我"28.1% vs 群聊"我"17.4%
  - 禁用词实际出现率<0.01%（天生反AI腔调）

### Phase 4 产出（私域运营心法）
- **文件**：`outputs/private-domain-ops-methodology.md`
- **5条心法**：价值前置→信任积累→自然付费、一人撑群要有退出机制、群聊是舞台私聊是收银台、短句更能建立信任、收入是顺带的不是目标
- **同辈互助群参与率43%**，远超行业均值（15-20%）
- **收入来源**：30笔转账来自15+人，轩式成长营5笔最高频

### Phase 5 产出（li-consultant Agent）
- **Skill目录**：`~/.newmax/skills/li-consultant/`
- **References**：consulting-cases.md / pricing-guide.md / auto-reply-templates.md
- **路由**：r401，16个触发词
- **已同步**：所有5个工作区 + skill-routing-table.json

### Phase 6 产出（定时任务）
- 每周六22:00：微信数据自动更新（解密+提取+分析）
- 每周日22:00：文风DNA自动蒸馏
- 每周日22:30：咨询收入每周汇总
- 已创建未来4周的任务链


## 2026-06-13 自动提取
- 快模式触发词严格限定为精确匹配"快！"（中文"快"+全角感叹号），不接受"快""！""快点""马上"等其他任何变体
- 将用户指令"马上"自行解释为可以跳过完整流程，是执行者自身的纪律问题，不是用户的触发词模糊
- 已更新的记忆文件：`memory/long-term.md` 快模式启动序列及用户核心语义指令，明确"快！"的精确匹配要求并标注非触发词


## 2026-06-14 自动提取
- 提取公众号内容时应使用专门的 SOP（标准操作流程）


## 2026-06-18 自动提取
- 用户偏好：执行任务要快、省 token，避免太慢太卡
- 用户偏好：文档要精简提炼，删除冗余解释，保留铁律/禁止条目和"详见"链接
- 决策：精简文档前先归档原文件再写入
- 归档路径约定：`E:\ai产出文件\牛马\归档\` 下按日期建子目录


## 2026-06-19 自动提取
- 用户不喜欢带连字符的域名（例如 lilian-yuan.com），认为输入麻烦、口头介绍别扭、显得不专业

## 2026-06-19 个人网站建设与域名（新增）
- **域名 `lilanyuan.cn` 已通过阿里云万网成功注册**（¥38/首年），实名认证已完成。
- **一内一外双轨部署策略**已确立：
  - 国内版（lilanyuan.cn）：体制内成就、电气工程硬核、皮赛/蓓伟企业身份、预留 ICP 备案号
  - 海外版（待建）：自媒体人设、AI 信息差、私域变现、商业闭环
- **产出文件**（`outputs/`）：
  - `lilanyuan-cn-v2.html`（65KB）：国内版个人网站，融合电气+具身智能身份、GPA 3.9、飞书知识库链接
  - `皮赛仪器AI采购申请清单20260619.md`（6KB）：Claude Team 双席位薅羊毛方案 + 投入产出分析
  - `双轨部署策略-一内一外.md`（5KB）：海外版定位 + 部署方案

## 2026-06-19 职业路径与备案策略纠正（高优先级）
- **备案策略纠正**：从"挂皮赛企业备案"改为"个人 ICP 备案"。原因：小黎职业路径是大厂轮转，域名备案必须跟着人走，不能绑在任何一家企业营业执照上。
- **职业时间线已确认**：
  - 皮赛仪器/蓓伟机器人 = 大学阶段跳板，不是长期锚点
  - 大二暑假起：特斯拉/蔚来/宁德时代/宇树科技（正式暑期实习）
  - 考研后 2029.2-9：一家很厉害的大厂实习
- **部署策略**：阿里云 OSS + CDN（国内秒开），个人备案 7-15 天，临时方案 Cloudflare Pages 或 Lisa 主机
- **飞书知识库**为用户个人知识中枢（非 Notion 1345）。
- **皮赛仪器 AI 采购方案**：Claude Team 活动价 ¥160/月 双席位，需 `@programsys.com.cn` 企业邮箱绑定。


## 2026-06-19 自动提取
- 用户的目标是让中国大陆用户通过微信顺利访问 lilanyuan.cn 上的单文件静态 HTML 页面
- 最终确定使用阿里云 OSS + CDN 作为最优部署方案，待皮赛备案完成后即可正式上线
- 域名已在阿里云管理，备案主体为"皮赛仪器"，备案后需将备案号写入页面
- 备案前阶段可用 Lisa 美国主机或 Cloudflare Pages 作为临时过渡方案
- 用户需要一份手把手的阿里云 OSS + CDN 部署操作教程


## 2026-06-19 自动提取
- 从大二暑假开始，简历投递目标为大厂，如特斯拉、蔚来、宁德时代、宇树科技等
- 考研后（2029年2月到9月）计划去一家很厉害的大厂实习


## 2026-06-20 Hermes 深度优化 [高置信]

### Hermes 真实状态（纠正了"零运行"的误判）
- **运行实例存在**：hermes-memory-watchdog.py（v3→v4）每 120 分钟跑一次，今天 17:46/19:46 正常运行
- **定时任务存在**：3 个 cron job（watchdog 每2h + work-auto-commit 每2h + weekly-patrol 周日21:00）
- **数据完整**：hermes-memory/ 有 atomic-facts(47条)、contradiction-log(1条未解决)、cross-tool-state(含42个memory文件+handoff追踪)
- **真正问题不是"零"，是"浅"**：watchdog v3 只做浅层扫描（mtime检测+行数阈值），不做内容分析、不自动修复、不调度 skill

### 已执行操作（watchdog v3→v4 + weekly-patrol 补全）
1. **watchdog v3→v4**：`C:\Users\13975\AppData\Local\hermes\profiles\selfevolve\scripts\hermes-memory-watchdog.py`
   - +维度6：过期文件自动刷新（runtime-snapshot/checkpoint >3天 → 标记修复）
   - +维度7：过期 handoff 自动消费（提取摘要→atomic-facts→标记consumed）
   - +可执行动作 JSON（供 cron agent 调用 li-memory/li-sync 等 skill）
   - +缺失 memory 检测（6 工作区每日检查）
   - v3 已归档：`E:\ai产出文件\牛马\归档\2026-06-20-watchdog-v3-archive\`
2. **hermes-weekly-patrol prompt 补全**：串联 4 个 skill（li-sync→li-improve→li-manage + li-memory 按需）
3. **path bug**（scripts/scripts/）已确认修复
4. **v4 首次运行成功**：发现 runtime-snapshot 过期 8 天、session-checkpoint 过期 7 天、atomic-facts 接近膨胀

### 设计决策
- **不创建第 6 个 skill**（li-hermes）——利用现有基础设施（watchdog v4 + 5 个 skill 的 cron 调度）
- 日心跳（每 2h）+ 周巡检（周日 21:00）双频模式
- "可执行动作 JSON"是关键接口：watchdog 输出 → cron agent 消费 → 调用对应 skill
- **教训**：先验证再断言——"看起来零"不等于"真的零"（违反铁律"验了才断"）

### 定时任务布局（最终）
```
watchdog (每120m) → 7维扫描 + 可执行动作JSON
weekly-patrol (周日21:00) → Phase1看watchdog → Phase2自动修复 → Phase3串联3个skill → Phase4周报
work-auto-commit (每120m) → Git自动提交
```

### 待跟进
- hermes-workspace-governance SKILL.md 在 cron 中被引用但文件系统未找到
- hermes-tasks.db 表结构完整但数据为空（0条任务/0条日志）
- atomic-facts.md 接近膨胀阈值（178行），下次周巡检应触发 li-memory 压缩


## 2026-06-20 自动提取
- 用户的内容平台矩阵：公众号 + 小红书 + 朋友圈 + 视频号（不用知识星球和知乎）
- 用户已有 skill：li-xhs、li-wechat、baoyu-post-to-wechat、li-video、voice-dna-auto-inject、li-analyze（道法术器）
- 用户方向：OPC 超级个体 + 商业闭环
- 用户当前缺少：固定的每日素材采集节奏、统一的"一份素材→多平台版本"调度器、outputs/ 结构化归档体系
- 用户对朋友的"数字资产工作台"Skill 感兴趣，决定不直接安装原版，而是融入现有工具链（建 li-asset/li-daily + outputs/digital-assets/ 归档）


## 2026-06-21 技能联动架构升级 [高置信]

### 架构决策：skill-auto-activation v1.0 → v2.0
- **联动优先 > 单打独斗**：一个任务能调2个skill就不只调1个
- **三层路由优先级链**：技能路由(Layer 0) > SOP(Layer 1) > 触发词(Layer 2) > 原生能力(Layer 3)
- **探索性任务强制用技能**：用户方向不明确时禁止原生裸跑，必须走 li-analyze/li-research/li-devil
- **自我学习闭环**：用户不满 → 5步学习 → 当轮修正 → 路由表更新 → 下次同类自动用新链
- **路由表 v2.1**：新增 linkage 字段，11 个核心 skill 已配置联动链
- 归档位置：`E:\ai产出文件\牛马\归档\2026-06-21-skill-activation-upgrade\`

### 联动链设计原则
- 辅助 skill 不超过 2-3 个（防拖慢超50%）
- li-devil 是最高频的辅助 skill（质疑型联动）
- 动态联动兜底：增强/质疑/归档三类至少选1

## 2026-06-21 自动提取
- 用户的个人建站项目路径为 `F:\work\个人建站\02-代码实现\`，部署平台是 Cloudflare Pages
- 用户的个人素材（如海报）存放在 `E:\personal_information\海报\`
- AI 产出文件的归档路径为 `E:\ai产出文件\牛马\归档\`，归档命名格式含日期和描述
- 技能联动调用优先：一个任务应触发多技能协作链

## 2026-06-22 niuma-engine v4.0 发布  [高置信]
- GitHub 仓库 Destined-at-Dawn/niuma-engine 从 v1.0（10条规则/~20KB）升级到 v4.0（29条规则/~124KB）
- 核心范式升级：从"单体AI工程师纪律"到"多Agent协作生态纪律"
- 根因修复：v1.0 .gitignore 的 `.claude/` 整目录排除导致规则从未分发
- 全量隐私脱敏：名称移除 + 路径占位符替换，零个人信息残留
- 待用户手动 push

## 2026-06-22 技能联动失败教训 [高置信] [关键教训]
- **事故**：调用 li 只拿到路由结果，未实际执行 li-research/li-analyze/li-devil 子技能，用原生工具替代了全链——被用户纠正"你让我很失望"
- **根因**：把 li 当成了一个"问一个答案"的单一工具，没有理解 li 是路由器、子技能才是执行体
- **铁律固化**：调用 li 后必须至少完成 li-research（信息补全）+ li-analyze（深度分析）两步链，不能只拿路由就自己干了
- **同类踩坑**：这是第 2 次"调了技能但没真正用技能内容"（首次见 2026-06-11 skill-execution-discipline.md 创建）

## 2026-06-22 开源配置包自检清单 [高置信]
- 开源给陌生人用的 AI 配置包必须过：CLAUDE.md 入口文件存在 / 所有引用文件实际存在 / 零视觉 emoji / 零个人隐私 / 安装文档可执行 / adapter 引用不超实际规则数
- 每次删除仓库中的规则后，必须 grep 全量扫描 README/docs/adapters 是否有死引用

## 2026-06-22 自动提取
- 使用 li 技能时必须严格执行完整链（li-research → li-analyze → li-devil → github-publisher 等），不可仅调用一次 li 路由后跳过后续环节
- 违反 skill-auto-activation v2.0 铁律“联动优先”会导致任务失败


## 2026-06-22 自动提取
- 修复了11处配置文件真死链接。
- 保留了20处workspace-sanitizer迁移规则


## 2026-06-25 自动提取
- 用户要求助手在调整方案时必须读取所有文件，有问题就向用户汇报，一起解决。
- 用户强调前提是助手真的解决不了问题时才汇报和一起解决。
