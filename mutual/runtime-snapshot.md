# 运行时快照 — mutual（管理/优化）

> 新对话启动时读取本文件，30 秒内了解用户当前状态。

## 当前主线
- **🔴 核心任务**：skill 调用体系优化（92路由/141触发词/6+无路由skill）+ skill-SOP 整合优化
- **✅ MCP 精简完成**：6→2 server（markitdown + mempalace），卸载 filesystem/memory/paddleocr/obsidian，无能力缺口
- **✅ 磁盘清理累计释放 ~12GB**：pip缓存5.5GB + db备份748MB + skills.zip207MB + Qoder待删701MB
- **深度迭代完成**：150+ 轮工作流优化（重量化·全自动化适配）
- **三路 CLI 就绪**：Claude (Opus) + Codex (Plus) + Gemini (Pro)
- **跨区三件套已落地**：项目卡 + 产出注册表 + 工作流改进收件箱
- **快模式已部署**：五区 CLAUDE.md 启动序列支持"快/快速/急/skip"跳过
- **Hook 防御链 3→6 个**：PreToolUse + PostToolUse + Stop 新增
- **量化指标系统已部署**：5 个核心维度 + 每日汇总

## CLI 工具状态
| CLI | 模型 | 后端 | 状态 |
|-----|------|------|------|
| Claude Code (Newmax) | Opus 4.8 (1M context) | Anthropic 官方 (firstParty OAuth) | ✅ OAuth 已登录 2026-06-11 |
| Codex CLI | gpt-5.5 | 官方 OpenAI (ChatGPT Plus) | ✅ 在线 |
| Gemini CLI | gemini-2.5-pro | Google OAuth | ✅ 在线 |

## 快速切换命令
```bash
# 已切换到 Anthropic 官方 OAuth，不再使用中转站
claude auth login    # 登录官方订阅
claude auth status   # 查看认证状态
```

## 磁盘状态（2026-06-12 更新）
| 盘 | 剩余 | 关键占用 |
|---|---|---|
| C: | 40.9GB (14.1%) | .newmax 6.7GB（conversations 4.2GB + .git 611MB + db 764MB） |
| D: | 55.1GB (16.1%) | data 46GB + AI学习资料集 40GB + AICompData 40GB + Vivado 28GB + study 26GB + $RECYCLE.BIN 18GB |
| E: | 24.3GB (12.4%) | MarvisData 25.4GB |

**待手动处理**：D:\Qoder（701MB，被占用需关闭后删） + D盘回收站（18GB） + D:\AI学习资料集与AICompData是否重复（各40GB）

## MCP 配置（2 server）
- **markitdown**：Office/PDF→Markdown ✅
- **mempalace**：726K向量语义搜索 ✅
- 已卸载：filesystem（原生工具覆盖）/ memory（从未使用）/ paddleocr（skill覆盖）/ obsidian（插件未装）

## 本周优先级
1. 🔴 **skill 调用体系优化**：6+无路由skill补注册 + "文风DNA"触发词冲突修复 + li-autoreply/li-persona-qa合并
2. 🔴 **skill-SOP 整合优化**：映射矩阵→优先级消除→场景打通→路由表升级
3. 🟡 **D盘大目录审计**：AI学习资料集 vs AICompData（各40GB）是否重复
4. 🟡 **深度调研 + 迭代**：deep-research v4.0 实战迭代
5. Codex 以"外部工程师"视角评审工作流
6. 落地 workflow-inbox.md 中待验证想法
7. Skill 上架：jc-clarifier 优先

## 最近完成
- 2026-06-09：li-memory v2.0（Supermemory 23.2K★ 集成，原子事实+矛盾检测+三层过期）、li-diagnose v1.0（熵增诊断，170行+3 references）、li-debug v1.0（mattpocock 反馈循环，182行）、li-triage v1.0（5状态机分流，171行）、微信分析全链路重建（4 skill + 1 SOP + wechat-db-update）、路由冲突治理（184→31 子串冲突，-83%）、群聊发送者名称修复（97.4% 解析率）、可复刻工具包 v1.0+v1.1、微信深度心理蒸馏（Camellia+米蛋糕）。li- 系列 20→23 个子 skill，路由 101→112 条，43 工作区同步
- 2026-06-08：路由表治理（113→101 路由，35→0 重复，7/7 工作区同步）、li-improve 全量重构（v1.0→v4.0，Progressive Disclosure 架构）、li-bestskill 搜索策略 v1.2（宽泛优先+10平台指南）、11 skill→li- 系列批量转换（最终 20 个子 skill）、li- 系列架构标准化 Phase A+B（20/20 达标≤300行）、私域 skill 体系 v2.0、竞赛/皮影场景赶制+求职/简历V19+创作/社群商业分析
- 2026-06-06：li 系列架构定型（6→7 个子 skill，li-research 正式纳入 + transcript-cleaner/find-skills 废弃标记 + 8 文件变更）、简历修改业务模块 V2（career-breakthrough 仓库整合 + 18 文件 + ATS/STAR/去AI味四层 + 5 条铁律）、Antigravity OAuth 代理排障（代理注入路径修复 + 双套环境变量 + Chromium --proxy-server）、百大认知书籍 Obsidian 数据同步、NiumaAutoCommit 正常运行（9 次提交）
- 2026-06-05：li 系列 v2.0 扩展（2→6 个技能，li-bestskill/li-manage/li-skillfusion 新建 + li-local-search Layer 3 升级）、skill 调用强制执行层（.claude/rules/skill-logging-enforcement.md 5 条铁律）、社群运营技能体系（42+ 技能扫描 + 8 场景 SOP + 5 个技能安装）、telos 接管+全局用户画像创建、Antigravity IDE 排查（代理→账号地区限制）、技能使用日志系统启动（15 条真实调用记录 + Flow E 首次分析：沉睡率 96.5%）
- 2026-06-03：个人成长方案 v1→v2（创始人大学经历深度对比 + 杠铃策略 + 五路径概率分析）、第六工作区「学习」初始化（5 门课 + 4 SOP + 注册表更新）、飞书知识库上传（94/108 blocks）
- 2026-06-02：li-skillcreate 技能锻造器 v1.0 创建（5 文件 / 36KB）、卡兹克开源 Skills 安装（storage-analyzer/li-manage/aihot/hv-analysis 4 个 + 路由 r069-r072）、Storage Analyzer v3.0 Windows 深度适配（295 条规则 + Unicode/GBK/中文路径修复）、v4.0 "一键清理"模式（direct_clean.py + 3 种删除回退）、学员行动手册教程（409 行 / 15/15 质量自检）、3 个可分发 zip 包打包（V1 59K / V2 86K / 完整包 135K）
- 2026-06-01：深度迭代 150+（Hook 链扩展 + 量化指标 + 自进化闭环 + 记忆 Nudge + 九段式压缩 + CLAUDE.md 优化）、三路 CLI 配置（Claude/Codex/Gemini）、Codex 账号切换（Plus）、快模式五区部署、跨区三件套落地、工作流全景地图 v1.0、15 轮迭代产出归档、MCP 配置协议五区固化
- 2026-05-29：jc-clarifier v2 升级 + chinese-natural-voice-revision 安装、竞赛区 ADC/DAC/EEPROM 工程拆分与交付、个人区 Skill 盘点（186 个）、市场信号扫描
- 2026-05-28：三路 CLI 初始配置、工作流深度优化（70+ 迭代）、Hook 链 3→6、量化指标系统、Karpathy Guidelines 同步、工作流全景地图 v1.0、跨区三件套
- 2026-05-27：GitHub 安全审计、上下文压缩系统、规则体系优化
- 2026-05-26：comemo 整合、MCP 配置协议、技能自动激活
- 2026-05-25：R16 三层防御部署、572 冗余文件归档清理

## 用户当前状态
- **第六工作区「学习」已初始化**：5 门课程（高数/英语/CET-4/6/物理/电路）+ 4 个 SOP
- 三路 CLI 工具就绪，可按场景分工使用
- Claude Code 已切换到 Anthropic 官方 OAuth（不再用中转站）
- Codex 已登录 ChatGPT Plus（lanyuan2007@gmail.com）
- 六大工作区治理进入稳定期
- 工作流进入「重量化·全自动化」新阶段
- 技能系统 92 条路由，1417 个触发词，140 个 Skill 目录（117 活跃 / 23 弃用），li- 系列 30+ 个子 skill
- MCP 精简为 2 server（markitdown + mempalace），无能力缺口

## 需要关注的风险
- ChatGPT Plus 有效期至 2026-06-27，届时需续费
- D盘 $RECYCLE.BIN 18GB 待清空
- D:\AI学习资料集(40GB) vs D:\AICompData(40GB) 可能重复，需审计
- D:\Qoder 701MB 被占用，需手动关闭后删除
- Skill 沉睡率高（96.5%），路由覆盖率待提升
- "文风DNA"触发词冲突（li-xhs vs li-wechat-distiller）
- li-autoreply + li-persona-qa 待合并

---
最后更新：2026-06-20
> ⚠️ 本文件由 Hermes cron 自动刷新时间戳（2026-06-20）。磁盘状态/CLI状态等数据仍为 2026-06-12 快照，需下次活跃会话时手动核实更新。
