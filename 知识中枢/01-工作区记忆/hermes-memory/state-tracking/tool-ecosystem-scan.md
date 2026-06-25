# 工具生态全景扫描

> Hermes 首次对 6 个 AI 工具配置目录的完整扫描。

---

## 工具清单

| 工具 | 配置路径 | 角色 | 状态 |
|------|---------|------|------|
| Newmax (牛马AI) | `.newmax/` | 内容创作中枢 | 活跃，104 skills，6 MCP servers |
| Claude Code/Desktop | `.claude/` | 主力编码+全局规则 | 活跃，6 条 CRITICAL RULE，telos 系统 |
| Codex | `.codex/` | 代码引擎 | 活跃，AGENTS.md 已配置，4 个 li- skill（li-skillcreate/li-skills-mgmt/li-infra/li-sync） |
| Hermes | `.hermes/` | 记忆中枢（我） | 刚搭建 |
| WorkBuddy | `.workbuddy/` | UI+飞书 | 活跃，connector-proxy MCP |
| Gemini | `.gemini/` | Google AI | 配置中，antigravity 框架 |
| Marvis | `E:\Marvis\` | 桌面AI助手（应用宝） | 活跃，22 skill（文档处理/桌面操作/浏览器/知识库），2 MCP server |

---

## 用户画像（综合 telos + long-term + work-style）

- **身份**：小黎（李兰源），2007.12.25，上海电力大学大一，电气工程（2026-06 转专业成功）
- **GPA**：3.896（目标 3.9+）
- **终极目标**：常州市局电网（考研上交/东南为手段）
- **当前竞赛**：ICAN小车（9月）+ 皮影戏（6.15 交初稿）
- **副业**：公众号+微信朋友圈（小红书已放弃）
- **工作风格**：直接、结论先行、信息密度高、一次对话搞定、能自动化绝不手动

---

## 关键架构发现

### 1. Telos 系统（`.claude/telos/`）
- 8 个文件覆盖：identity/goals/interests/skills/beliefs/learned/soul/work-style
- 所有工作区共享，是个人信息的单一真相源
- **Hermes 需要尊重**：读取个人信息优先用 telos，不硬编码

### 2. 6 条 CRITICAL RULE（`.claude/CLAUDE.md`）
- No Blind Overwrite（禁止盲目覆写）
- Think Before Act（动手前必先思考）
- 竞赛项目记忆路径覆盖（竞赛区特殊路径规则）
- Telos 个人信息跨工作区同步
- AI 工程方法论——行为触发器（8 条触发器）
- 小黎语言DNA 全局风格触发

### 3. Newmax Skill 生态
- 48 个 li- 系列 skill（小黎专属工作流）
- 56 个非 li- skill（通用工具）
- 3 层防跳过机制已落地
- 路由表 264 routes，38 active li- routes
- **2026-06-15 审计**：Skill 111 个（90 活跃/19 弃用），路由 97 条（-15），触发词 1530（+142）
- **断裂路由**：wechat-consultant（r400）本地无 SKILL.md
- **孤儿 Skill 7 个**：li-embedded + competition-yolo 应注册路由
- **技能使用日志停滞 10 天**（最后 06-05），Stop hook 疑似异常

### 4. MCP 服务器矩阵
- Newmax: filesystem + memory + obsidian + mempalace + paddleocr + markitdown
- WorkBuddy: connector-proxy (飞书 + tmeet)

---

## Hermes 配合策略

### 给 Newmax
- 注入：项目上下文、历史决策、用户偏好（从 telos 读取）
- 接收：产出注册更新、skill 使用日志

### 给 Codex
- 注入：技术决策历史、已知 bug 列表、代码规范偏好
- 接收：技术产出注册、架构决策记录

### 给 Marvis
- 注入：文档处理上下文、桌面操作历史、用户偏好
- 接收：文档处理结果、桌面操作产出、知识库更新

### 给 WorkBuddy
- 注入：设计偏好、飞书适配约束、展示内容来源
- 接收：UI 产出注册、飞书文档链接

### 给所有工具
- 上下文注入 ≤500 字
- 矛盾检测（新事实 vs 已有记忆）
- 跨工具状态追踪（handoffs 监控）

### 统一协作规则（2026-06-13）
- 所有工具可**读** hermes-memory（atomic-facts / cross-tool-state / tool-ecosystem-scan）
- 所有工具**不写** hermes-memory（Hermes 专属写入区）
- 需要交接给 Hermes 的内容写到 `05-每日记忆/`
- Hermes 每次新会话自动扫描 `05-每日记忆/` 未处理文件并给修改意见
- 交接文件命名规范：`YYYY-MM-DD-{来源工具}-{主题}.md`

---

> 扫描时间：2026-06-11（初始化）
> 最后更新：2026-06-15（+生态审计数据更新）
