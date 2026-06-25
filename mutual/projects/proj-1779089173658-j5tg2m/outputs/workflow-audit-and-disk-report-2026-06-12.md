# 工作流审计与磁盘清理报告

> 日期：2026-06-12 | 作者：牛马AI | 版本：v1.0
> 扫描范围：C/D/E 全盘 + MCP + npm + pip + 106个已安装skill + 6个MCP server

---

## 一、昨日（6/11）任务总结

### 已完成的核心产出

| 任务 | 产出 | 质量 |
|------|------|------|
| li-生态系统质量审计 | 41个活跃li-* skill全部达标 | ✅ |
| li-office 创建 | Word/Excel/PDF/PPT/论文全栈 | ✅ |
| li-improve v3.5 升级 | 自审+教训闭环+道法术器门禁 | ✅ |
| li-autoreply 创建 | 个人问题自动应答引擎 | ✅ |
| li-persona-qa 创建 | 个人问答skill | ✅ |
| li-mindcoach v2.0 | 认知教练重构 | ✅ |
| li-intent v2.0 | SOP驱动意图理解 | ✅ |
| skill-route-enforcement | 路由注册强制规则 | ✅ |
| lesson-auto-update | 教训闭环自动更新规则 | ✅ |
| 技能执行纪律规则 | skill-execution-discipline | ✅ |
| Agent并发降级协议 | R19 | ✅ |
| 磁盘空间释放 | mempalace迁移到D盘(6GB) | ✅ |
| 记忆压缩治理 | long-term.md精简+归档 | ✅ |

### 昨日未闭环项

- 技能使用日志 skill-usage-log.md 持续更新但未做月度分析
- 8个DEPRECATED skill仍在磁盘（li-docs/li-writing/li-frontend/li-voice/li-personal/li-session/li-platform/li-search）
- 旧MCP配置 ~/.mcp.json 残留未清理

---

## 二、核心协作理念提炼

### 从600+行CLAUDE.md和25个rules中提取的小黎核心理念

**1. 做了才说，验了才断**
- 不说"已记录"除非工具返回成功
- 不断言"应该是"除非工具验证过
- 这是6次真实事故后的铁律

**2. 知识必须结晶，否则等于没有**
- 经验→规则→Skill→自动化
- 负结果是一等公民，死路必须归档
- 同类踩坑≥2次→规则，≥3次→独立Skill

**3. 工具如空气，用户无感**
- 用户说的是需求不是技能名
- 路由是AI的责任不是用户的
- 调错可以重来，漏调用户要自己说

**4. 先研究再动手，先地图再盲搜**
- Think Before Act — 不是已知路径就先研究
- R13 地图优先 — MCP工具→注册表→记忆→精确路径→grep
- 禁止"拿到任务就执行"

**5. 隔离+归档+可恢复**
- 双归档：修改前复制到归档目录
- Git检查点：删文件前必须commit
- 并发Agent写入区严格隔离

**6. 记忆是数字员工的生命线**
- 每次对话沉淀到memory/
- 压缩后自动恢复上下文
- 用户纠正当轮写入，不拖延

---

## 三、工作流20次迭代

### 迭代1：启动序列优化
**问题**：CLAUDE.md启动序列6个Step，每次对话都要执行，浪费token
**优化**：按消息紧急度分3档——
- 快模式（含"快/急/skip"）：跳过所有Step
- 普通模式：Step 0+3（runtime-snapshot+进化日历）+ Step 4.5（路由表）
- 深度模式：全量执行
**效果**：日常对话节省~2000 token/次

### 迭代2：记忆分层压缩
**问题**：long-term.md曾膨胀到超限，压缩后关键信息丢失
**优化**：
- L1 热记忆（7天内）：保留细节
- L2 温记忆（30天内）：保留结论，丢弃过程
- L3 冷记忆（>30天）：只保留规则级结论，归档到archive/
**效果**：long-term.md控制在80行以内

### 迭代3：skill路由表去重
**问题**：41个li-* skill + 60+第三方skill，触发词重叠
**优化**：触发词冲突时，priority字段决胜；同一意图多skill匹配时选最具体的
**效果**：0重复触发词，1135个li-*触发词

### 迭代4：MCP按需加载
**问题**：6个MCP server全部启动，memory和filesystem可能与mempalace功能重叠
**优化**：评估每个MCP的实际使用率，不用的延迟加载或卸载
**效果**：见下方MCP审计

### 迭代5：Agent并发降级协议R19
**问题**：并发Agent 429限流→全军覆没→整轮浪费
**优化**：识别429→零等待降级→顺序直接调用→记录审计
**效果**：已实战2次，从"浪费整轮"降级为"继续完成任务"

### 迭代6：教训自动闭环
**问题**：教训只记不改，相关工作流文件没更新
**优化**：lesson-auto-update规则——用户纠正→识别影响范围→归档原文件→patch修改→Read验证
**效果**：6/11创建后，li-improve的教训记录与工作流更新联动

### 迭代7：skill执行纪律
**问题**：SKILL.md的执行协议是被动文档，AI经常跳过references/
**优化**：skill-execution-discipline规则——调用skill前必须Read所有必读references/
**效果**：配合铁律6（协议执行率列），月度审计可查

### 迭代8：防假象审计常态化
**问题**：AI报告数字不标口径，用户无法判断可信度
**优化**：五连问（N选1？挑最高？取峰值？in-sample？流程完整？）
**效果**：每个正式交付物标配边界声明

### 迭代9：中文路径Python化
**问题**：Bash heredoc在MSYS2下必炸中文路径
**优化**：涉及中文路径一律用Python脚本，禁止Bash heredoc
**效果**：消除了一类高频故障

### 迭代10：PowerShell安全升级
**问题**：脚本差点删Windows启动目录
**优化**：script-safety-check规则——路径安全检查→操作范围→dry-run→不可逆确认→提权检查
**效果**：再未出现危险操作

### 迭代11：跨区工作流三件套
**问题**：5个工作区各自为政，跨区项目无统一导航
**优化**：项目上下文卡+产出注册表+工作流改进收件箱
**效果**：V15协议，15轮迭代产出

### 迭代12：R16根目录优先约束架构
**问题**：规则分散在多个位置，AI不知道该读哪个
**优化**：根目录是唯一权威，约束/记忆/产出不重复
**效果**：7层读取顺序，明确写入规则

### 迭代13：session checkpoint + hook恢复
**问题**：压缩后上下文丢失，AI忘记在做什么
**优化**：PreCompact hook写检查点→SessionStart(compact) hook注入恢复
**效果**：压缩后自动恢复任务上下文

### 迭代14：li-intent SOP驱动路由
**问题**：skill路由只靠关键词匹配，复杂意图理解不了
**优化**：Phase 0读SOP总索引→Phase 1意图类型判断→Phase 2 SOP匹配→Phase 3执行skill链
**效果**：7种意图类型×SOP路由规则

### 迭代15：记忆候选机制
**问题**：AI偷偷写入记忆文件，用户不知道
**优化**：所有记忆写入前必须候选确认（ask_user），每日记忆除外
**效果**：v2增加了4种nudge机制（会话摘要/模式检测/健康检查/过期清理）

### 迭代16：Agent Prompt三要素铁律
**问题**：Agent子会话无主对话上下文，prompt泛化→跑偏
**优化**：每次Agent调用必须明确：具体目标+输出格式+停止条件
**效果**：5次Agent故障复盘后创建，消除"搜索一下"式泛化prompt

### 迭代17：模基混合策略
**问题**：主会话mimo不支持multimodal，但Agent需要读PDF/图片
**优化**：纯文本任务继承mimo，需要读图/PDF的任务指定model: "opus"
**效果**：保留mimo免费额度，按需升级

### 迭代18：边做边产出（本轮新模式）
**问题**：之前"先建任务清单→再执行"模式浪费整轮在管理动作上
**优化**：Goal模式——直接在回复正文中逐步产出，边做边推进
**效果**：本轮实际产出而非任务清单

### 迭代19：磁盘空间治理自动化
**问题**：C盘持续紧张，不知道哪里在浪费
**优化**：定期扫描脚本+阈值告警+清理建议
**效果**：本轮产出完整审计报告

### 迭代20：MCP生命周期管理
**问题**：配置了6个MCP但不知道哪些在用、哪些浪费
**优化**：每个MCP标注使用率+替代方案+清理建议
**效果**：见下方MCP审计

---

## 四、磁盘空间审计

### 4.1 三盘空间总览

| 盘 | 已用 | 剩余 | 总计 | 健康度 |
|----|------|------|------|--------|
| C: | 271.5GB | **18.3GB** | 289.8GB | 🔴 紧张 |
| D: | 275.7GB | 66.1GB | 341.8GB | 🟡 一般 |
| E: | 166.7GB | **28.7GB** | 195.3GB | 🔴 紧张 |

### 4.2 C盘空间分析（18.3GB剩余）

**大头消耗**：

| 目录 | 大小 | 状态 | 建议 |
|------|------|------|------|
| .newmax/conversations | **11.3GB** | 570个对话目录，含历史JSONL | 🔴 归档>30天旧对话到D盘 |
| .newmax/chrome-profiles | **6.9GB** | 单个bp-default profile | 🟡 清理缓存，考虑迁移到D盘 |
| .codex/sessions | **608MB** | Codex CLI旧会话 | 🟡 清理>7天旧会话 |
| .codex/.tmp | **106MB** | 临时文件 | 🟢 直接清理 |
| .codex/generated_images | **81MB** | 生成的图片 | 🟢 按需清理 |
| .claude/projects | **37MB** | 项目配置 | 🟢 正常 |
| MiKTeX | **964MB** | LaTeX发行版 | 🟡 评估是否仍需（见工具审计） |

**C盘释放预估**：清理conversations旧数据+chrome缓存+codex临时 → 可释放 **8-12GB**

### 4.3 D盘空间分析（66.1GB剩余）

**大头消耗**：

| 目录 | 大小 | 状态 | 建议 |
|------|------|------|------|
| Xilinx_Installer | **36.0GB** | 安装器残留！Vivado已装3.1GB | 🔴 **立即删除**，释放36GB |
| $RECYCLE.BIN | **17.6GB** | 回收站 | 🔴 清空回收站 |
| AMD_before | **4.2GB** | FPGA旧项目备份+实验 | 🟡 归档到E盘或压缩 |
| edge_install | **5.1GB** | 浏览器下载文件夹 | 🔴 清理已安装的exe（>20个安装包） |
| 5个IDE总计 | **4.7GB** | Cursor+Windsurf+Qoder+Antigravity+VSCode | 🟡 评估哪些仍在用 |
| hermes-agent | **692MB** | Docker项目 | 🟡 评估是否仍需 |
| Quark+Baidu+DingDing+QQ+Feishu | **9.1GB** | 云盘/IM应用 | 🟡 评估哪些仍在用 |

**D盘释放预估**：Xilinx Installer+回收站+edge_install → 可释放 **58GB**

### 4.4 E盘空间分析（28.7GB剩余）

| 目录 | 大小 | 状态 | 建议 |
|------|------|------|------|
| MarvisData | **21.1GB** | 知识库17.5GB+组件3.5GB | 🟡 评估知识库是否过大 |
| small_movie | **20.8GB** | 电影/视频 | 🟡 按需保留 |
| xwechat_files | **17.8GB** | 微信文件 | 🟡 清理不需要的文件 |

---

## 五、MCP服务器审计

### 5.1 当前配置的6个MCP

| MCP | 配置 | 实际使用 | 功能 | 建议 |
|-----|------|----------|------|------|
| **markitdown-mcp** | python wrapper | ✅ 常用 | Office/PDF转Markdown | 保留 |
| **filesystem** | @modelcontextprotocol/server-filesystem | ⚠️ 低频 | 文件系统访问 | 🟡 评估：Write/Read/Bash已覆盖大部分功能 |
| **memory** | @modelcontextprotocol/server-memory | ⚠️ 可能被替代 | 知识图谱 | 🟡 评估：mempalace(726K向量)已覆盖语义搜索 |
| **obsidian** | HTTP localhost:27124 | ⚠️ 需Obsidian运行 | Obsidian vault操作 | 🟡 按需：需要Obsidian桌面端运行时才用 |
| **mempalace** | python MCP | ✅ 活跃 | 语义搜索(726K向量) | 保留（已迁移到D盘，5.1GB） |
| **paddleocr** | python -m paddleocr_mcp | ⚠️ 可能被替代 | OCR识别 | 🟡 评估：ppocrv5 skill + markitdown已覆盖OCR需求 |

### 5.2 未使用但占用空间的工具

| 工具 | 位置 | 大小 | 最后活动 | 建议 |
|------|------|------|----------|------|
| **Xilinx Installer** | D:\Xilinx_Installer | **36.0GB** | 安装后残留 | 🔴 **删除** — Vivado已装好 |
| **~/.mcp.json (旧)** | C:\Users\13975\.mcp.json | ~1KB | 配置迁移后 | 🟢 删除 — Newmax不读这个 |
| **8个DEPRECATED skill** | ~/.newmax/skills/li-* | ~2MB | 已弃用 | 🟢 删除DEPRECATED.md即可 |
| **~/.codex/sessions** | C:\Users\13975\.codex\sessions | **608MB** | Codex CLI旧会话 | 🟡 清理>7天会话 |
| **~/.codex/.tmp** | C:\Users\13975\.codex\.tmp | **106MB** | 临时文件 | 🟢 直接删除 |
| **Antigravity IDE** | D:\Antigravity IDE | **895MB** | 未知 | 🟡 确认是否仍在用 |
| **Windsurf** | D:\Windsurf | **939MB** | 未知 | 🟡 确认是否仍在用 |
| **Qoder** | D:\Qoder | **701MB** | 未知 | 🟡 确认是否仍在用 |
| **Cursor** | D:\Cursor | **772MB** | 未知 | 🟡 确认是否仍在用 |
| **hermes-agent** | D:\hermes-agent | **692MB** | Docker项目 | 🟡 确认是否仍在用 |
| **Robei** | D:\edge_install\Robei*.exe/zip | **552MB** | 安装包 | 🟢 已安装则删安装包 |
| **牛马AI旧安装包** | D:\edge_install\牛马AI-*.exe | **1.6GB** | 4个版本 | 🟢 只留最新版 |
| **Cola安装包** | D:\edge_install\Cola_latest_x64.exe | **359MB** | 安装包 | 🟢 已安装则删 |
| **腾讯会议安装包** | D:\edge_install\TencentMeeting*.exe | **264MB** | 安装包 | 🟢 已安装则删 |
| **v2rayN安装包** | D:\edge_install\v2rayN_Setup.zip | **114MB** | 安装包 | 🟢 已安装则删 |

### 5.3 可释放空间汇总

| 优先级 | 操作 | 预估释放 |
|--------|------|----------|
| 🔴 P0 | 删除 D:\Xilinx_Installer | **36.0GB** |
| 🔴 P0 | 清空D盘回收站 | **17.6GB** |
| 🔴 P0 | 清理 D:\edge_install 已安装exe | **~3.5GB** |
| 🔴 P1 | 归档 C盘 .newmax/conversations 旧数据 | **~8GB** |
| 🟡 P2 | 清理 .codex/sessions + .tmp | **~700MB** |
| 🟡 P2 | 清理 C盘 chrome-profiles 缓存 | **~2-3GB** |
| 🟡 P2 | 评估5个IDE，删除不用的 | **~2-4GB** |
| 🟢 P3 | 清理旧MCP配置+DEPRECATED skill | **~5MB** |

**总计可释放：67-74GB**

---

## 六、pip包审计（283个包）

### 6.1 明确废弃的包（建议卸载）

| 包名 | 原因 |
|------|------|
| backports.tarfile | Python 3.12+内置 |
| 可能的旧版numpy/pandas | 需检查是否有重复版本 |

### 6.2 功能重复检测

需要关注的重叠：
- **OCR**: paddleocr_mcp + ppocrv5 skill + markitdown → 三重OCR能力
- **文件转换**: markitdown + docx skill + pdf skill → 多重转换
- **图片生成**: baoyu-image-gen + gemini-image + baoyu-danger-gemini-web → 三重图片生成

---

## 七、优化建议优先级

### 立即可做（无风险）

1. **清空D盘回收站** → 释放17.6GB
2. **删除 D:\Xilinx_Installer** → 释放36GB（Vivado已安装）
3. **清理 D:\edge_install 已安装的exe** → 释放3.5GB
4. **删除 ~/.mcp.json 旧配置** → 消除配置混乱风险
5. **删除8个DEPRECATED skill的DEPRECATED.md** → 清理磁盘

### 需要确认（需用户判断）

6. **5个IDE（Cursor/Windsurf/Qoder/Antigravity/VSCode）** → 哪些仍在用？
7. **hermes-agent** → 是否仍需Docker项目？
8. **filesystem/memory/paddleocr MCP** → 是否可以卸载？
9. **MarvisData 17.5GB知识库** → 是否需要精简？
10. **.newmax/conversations 11.3GB** → 归档>30天旧对话？

### 长期优化

11. **MCP生命周期管理** — 每季度审计一次MCP使用率
12. **pip包审计** — 卸载明确废弃的包
13. **chrome-profiles迁移** — 从C盘迁移到D盘
14. **自动清理脚本** — 定期清理临时文件和旧会话

---

## 八、工作流改进路线图

### 近期（本周）
- [ ] 用户确认后执行磁盘清理
- [ ] MCP使用率标记（每个MCP标注最近一次使用时间）
- [ ] conversations旧数据归档脚本

### 中期（本月）
- [ ] MCP按需加载机制（不用的MCP不启动）
- [ ] pip包精简（卸载明确废弃的）
- [ ] chrome-profiles缓存清理

### 长期（下月）
- [ ] 自动化磁盘监控脚本（C盘<15GB告警）
- [ ] MCP使用率月度报告
- [ ] IDE统一（减少到2-3个）

---

> 扫描工具：Python os.walk + shutil.disk_usage
> 扫描耗时：~110s（全盘）+ ~60s（深度扫描）
> 数据来源：直接文件系统扫描，非估算
