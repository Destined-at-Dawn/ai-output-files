# AI 工作流全面审计与迭代优化报告

> 执行者：Hermes（记忆中枢）
> 日期：2026-06-12
> 触发：小黎要求"总结昨天+反思工作流+扫描未使用资源+迭代20次"

---

## 一、昨天（6/11）任务总结

### 核心产出
1. **li- 系列生态清理**：149 → 58 活跃 skill（-61%），40 活跃 + 8 弃用
2. **skill 执行协议注入**：38 个 li- skill 全部注入三层防跳过机制
3. **文档修正**：6 个来源的统计口径统一（li-series-status-definitions.md 为权威源）
4. **li-lesson 机制创建**：教训 → 自动闭环 → 系统性修复
5. **Hermes 工作区切换**：从 C 盘切到 ${LEGACY_ROOT}
6. **行为约束固化**：三条死线 + 写入约束 + 响应结构

### 问题
- 昨天的工作高度集中在 **skill 体系治理**，但没有触碰 **磁盘空间** 和 **工具利用率** 问题
- 6/11 的 memory 记录了 4 弃用 → 实际 8 弃用（已修正），说明状态跟踪仍有滞后

---

## 二、你的 AI 协作核心理念（逆向推导）

从你的 CLAUDE.md、行为约束、telos、runtime-snapshot 综合分析：

### 你的核心理念是：**工具即器官，不是装饰**

你对 AI 协作的要求：
1. **自动化优先**：能自动的绝不手动（skill 自动激活、路由表、hook 链）
2. **做了才说**：不允许空话，工具调用返回成功才能确认
3. **每轮有质变**：迭代不是复制粘贴，每次必须有实质差异
4. **系统性思维**：不修单点，修系统（li-lesson 的教训 → 影响范围分析 → 全量更新）
5. **数据驱动**：量化指标、使用日志、沉睡率统计
6. **分层治理**：四位一体各司其职（Hermes 记忆、Newmax 创作、Codex 代码、WorkBuddy UI）

### 你最厌恶的模式
- AI 说"已记录"但没执行
- AI 用"我觉得"代替验证
- 表面审计（扫表面不扫深层）
- 装了不用的工具占空间

---

## 三、磁盘与工具全景扫描

### 3.1 磁盘空间危机

| 分区 | 总量 | 已用 | 可用 | 使用率 |
|------|------|------|------|--------|
| C: | 290G | 272G | **18G** | **94%** |
| D: | 342G | 276G | 67G | 81% |
| E: | 196G | 167G | 29G | 86% |

**C 盘 94% 是红色警报。** 主要元凶：

| 路径 | 大小 | 说明 |
|------|------|------|
| `.newmax/conversations/` | **12GB** | 570 个对话记录 |
| `.newmax/chrome-profiles/` | **7GB** | MCP 浏览器配置 |
| `.newmax/newmax.db` + `.bak` | **1.5GB** | 主数据库 + 备份 |
| `.newmax/projects/` | **816MB** | 项目缓存 |
| `.newmax/skills.zip` | **208MB** | 旧备份 |
| `.newmax/` 总计 | **22GB** | C 盘最大单体消耗 |
| `WorkBuddy/` | **198MB** | 295 个快照目录 |
| `tool-WeChatMsg/` | **71MB** | 微信消息工具 |
| `Obsidian/` | **350MB** | Obsidian 应用本体 |

### 3.2 MCP 服务器配置（Newmax 6 个）

| MCP | 功能 | 实际使用频率 | 状态 |
|-----|------|------------|------|
| `markitdown-mcp` | 文档转 Markdown | 低 | 保留 |
| `filesystem` | 文件系统访问 | 中 | 保留 |
| `memory` | 知识图谱记忆 | 低（Hermes 已接管） | **可考虑移除** |
| `obsidian` | Obsidian 笔记 | **未验证** | **待确认** |
| `mempalace` | 记忆宫殿 | **未知** | **待调研** |
| `paddleocr` | OCR 识别 | 低 | 保留（偶尔用） |

### 3.3 已安装但疑似停用的工具/目录

| 路径 | 大小 | 最后活跃 | 说明 |
|------|------|---------|------|
| `/d/Windsurf/` | **958MB** | 未知 | AI IDE，已被 Claude Code + Codex 替代 |
| `/d/Cursor/` | **809MB** | 未知 | AI IDE，已被 Claude Code + Codex 替代 |
| `/d/Antigravity IDE/` | 未知 | 2026-06 排障中 | AI IDE，OAuth 代理问题未完全解决 |
| `/e/Marvis/` | **2.7GB** | 未知 | Marvis AI 助手，**疑似早期 AI 工具** |
| `/e/MarvisData/` | 未知 | 未知 | Marvis 数据目录 |
| `/e/AI_software/` | **1.1GB** | 未知 | 包含 Antigravity IDE 安装包 |
| `/d/Vivado/` | 大（超时） | 未知 | Xilinx FPGA 工具（已从集成电路转专业） |
| `/d/Xilinx_Installer/` | 大（超时） | 未知 | Xilinx 安装器 |
| `/d/xillin/` | 未知 | 未知 | 疑似 Xilinx 相关 |
| `/d/51singlechip/` | 未知 | 未知 | 51 单片机（大一课程？） |
| `/c/Users/13975/Xilinx/` | 8KB | 未知 | Xilinx 配置残留 |
| `/c/Users/13975/tool-WeChatMsg/` | **71MB** | 未知 | 微信消息导出工具 |
| `/c/Users/13975/新建文件夹/` | 0 | 未知 | 空文件夹 |
| `/c/Users/13975/cola/` | 0 | 未知 | 空文件夹 |
| `/c/Users/13975/source/` | 0 | 未知 | 空文件夹 |
| `/e/niuma_ai/` | 未知 | 2026-04 | **旧版牛马 AI 工作区**（已被 /e/ai产出文件/牛马/ 替代） |
| `/e/codex_tmp_wenchuang_v2/` | 64KB | 未知 | Codex 临时文件 |
| `/d/codex/` | **474MB** | 未知 | Codex 安装目录（可能已通过 npm 全局安装替代） |
| `/e/Shandianshuo/` | 未知 | 未知 | 闪小说音频文件 |

### 3.4 Hermes 生态状态

| 组件 | 数量/大小 | 说明 |
|------|----------|------|
| 默认 profile skills | 30 个 | 不被 selfevolve 使用 |
| selfevolve profile skills | 20 个 | 当前活跃 |
| Newmax skills | 121 个 | 含 li- 系列 40 活跃 |
| Skill 使用日志 | 18 条记录 | 沉睡率可能仍很高 |
| Cron jobs | 未知 | 需要检查 |
| 工作区 | 6 个 | mutual/个人/创作/学习/求职/竞赛 |

### 3.5 WorkBuddy 状态

- 295 个快照目录（2026-03-24 到 2026-06-06）
- 最后活跃：2026-06-06
- **6 天未使用**，但占 198MB
- 每次运行都创建新快照目录，无清理机制

---

## 四、工作流迭代优化（20 轮）

### 迭代 1：清理 .newmax/conversations/ 旧对话
- **问题**：570 个对话 = 12GB
- **方案**：保留最近 30 天，归档其余到 E 盘
- **预期释放**：~10GB
- **风险**：低（Newmax 可重建索引）

### 迭代 2：清理 .newmax/chrome-profiles/
- **问题**：7GB 浏览器配置
- **方案**：检查是否仍在使用，不使用则清理
- **预期释放**：~7GB
- **风险**：中（MCP 可能依赖）

### 迭代 3：压缩 newmax.db + 删除旧备份
- **问题**：758MB 主库 + 748MB 备份 = 1.5GB
- **方案**：VACUUM 压缩主库，删除 6/11 备份
- **预期释放**：~500MB
- **风险**：低

### 迭代 4：清理 skills.zip
- **问题**：208MB 旧备份
- **方案**：删除（skills 目录本身只有 32MB）
- **预期释放**：208MB

### 迭代 5：WorkBuddy 快照清理
- **问题**：295 个快照 = 198MB
- **方案**：保留最近 10 个，其余删除
- **预期释放**：~180MB

### 迭代 6：Xilinx/Vivado 全家桶清理
- **问题**：已从集成电路转专业到电气工程，FPGA 工具不再需要
- **方案**：确认不需要后，删除 /d/Vivado/ + /d/Xilinx_Installer/ + /d/xillin/ + ~/Xilinx/
- **预期释放**：可能 10GB+
- **风险**：需要用户确认

### 迭代 7：Marvis AI 清理
- **问题**：/e/Marvis/ = 2.7GB，疑似早期 AI 工具
- **方案**：确认不再使用后删除
- **预期释放**：2.7GB

### 迭代 8：Windsurf + Cursor 清理
- **问题**：两个 AI IDE 各 ~900MB，已被 Claude Code + Codex 替代
- **方案**：确认不再使用后删除
- **预期释放**：1.7GB

### 迭代 9：旧版 niuma_ai 目录清理
- **问题**：/e/niuma_ai/ 是旧版工作区，已被 /e/ai产出文件/牛马/ 替代
- **方案**：归档后删除
- **风险**：低

### 迭代 10：Newmax memory MCP 精简
- **问题**：memory MCP 和 Hermes 记忆系统功能重叠
- **方案**：评估是否移除 memory MCP（减少启动开销）
- **风险**：中（需确认 Newmax 是否依赖）

### 迭代 11：Obsidian MCP 验证
- **问题**：配置已写入但 runtime-snapshot 标记"待验证"
- **方案**：在下次 Newmax 对话中验证是否加载成功
- **风险**：低

### 迭代 12：mempalace MCP 调研
- **问题**：mempalace_mcp.py 配置存在但使用情况未知
- **方案**：读取脚本内容，评估是否仍有价值
- **风险**：低

### 迭代 13：Hermes 默认 profile 清理
- **问题**：默认 profile 有 30 个 skill，selfevolve 不使用
- **方案**：评估是否需要保留（可能是其他 Hermes 会话使用）
- **风险**：低

### 迭代 14：建立自动清理 cron
- **问题**：WorkBuddy 快照、对话记录持续增长，无自动清理
- **方案**：创建 cron job，每周清理 30 天前的对话和快照
- **风险**：低

### 迭代 15：Skill 沉睡率审计
- **问题**：121 个 Newmax skill，使用日志只有 18 条
- **方案**：全量扫描 skill-usage-log.md + .claude.json skillUsage，标记沉睡 >30 天的 skill
- **风险**：低

### 迭代 16：C 盘空间告警机制
- **问题**：C 盘 94% 无告警
- **方案**：创建 cron job，每天检查磁盘空间，>90% 时告警
- **风险**：低

### 迭代 17：四位一体工具利用率仪表盘
- **问题**：无法一眼看到各工具使用频率
- **方案**：在 runtime-snapshot.md 增加工具使用频率追踪
- **风险**：低

### 迭代 18：统一 MCP 配置管理
- **问题**：MCP 配置分散在 .mcp.json（废弃）、.newmax/.mcp.json、Hermes config
- **方案**：创建单一 MCP 配置源文档
- **风险**：低

### 迭代 19：handoff 断链告警
- **问题**：6 个工作区的 handoffs/ 目录可能有超期未消费的交接
- **方案**：扫描所有 handoffs/，标记 >7 天的
- **风险**：低

### 迭代 20：工作流核心理念文档化
- **问题**：你的协作理念散落在 telos/CLAUDE.md/行为约束中
- **方案**：创建 `知识中枢/02-共享规则/协作核心理念.md`，统一文档化
- **风险**：低

---

## 五、立即可执行的高优先级行动

### P0（今天做）
1. **清理 .newmax/conversations/ 旧对话**（释放 ~10GB，C 盘从 94% 降到 ~90%）
2. **删除 skills.zip**（208MB，无风险）
3. **删除 newmax.db.bak**（748MB，已有最新备份策略）

### P1（本周做）
4. **Xilinx/Vivado 全家桶确认清理**（潜在 10GB+）
5. **Marvis + Windsurf + Cursor 确认清理**（5.3GB）
6. **Obsidian MCP 验证**

### P2（持续优化）
7. 自动清理 cron 建立
8. 磁盘告警 cron 建立
9. Skill 沉睡率审计

---

## 六、可回收空间估算

| 来源 | 可释放 | 优先级 |
|------|--------|--------|
| .newmax/conversations/ 旧对话 | ~10GB | P0 |
| .newmax/chrome-profiles/ | ~7GB | P0 |
| Xilinx/Vivado 全家桶 | ~10GB+ | P1 |
| Marvis | 2.7GB | P1 |
| Windsurf + Cursor | 1.7GB | P1 |
| newmax.db 备份 + skills.zip | ~950MB | P0 |
| WorkBuddy 旧快照 | ~180MB | P2 |
| **合计** | **~32GB+** | |

**如果全部执行，C 盘可从 18GB 可用恢复到 ~40GB+，E 盘也有显著改善。**
