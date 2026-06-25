# 生态索引 + 女娲蒸馏 + 文风DNA 自动注入系统

## 背景

小黎需要一个统一的"生态手册"，包含：
- 常用工作群状态（微信活跃群近30天统计）
- Skill 库完整索引（136+ skills）
- SOP 跨工作区索引（5个工作区共 89 SOPs）
- MCP 工具索引
- 女娲蒸馏结果（所有频繁联系人的心理画像 + 文风DNA）
- 小黎自蒸馏（文风DNA，自动更新）

**核心要求**：写作时自动注入文风DNA（除正式文体外），每周日晚自动刷新。

---

## 方案设计

### 组件1：生态手册（统一索引文件）

**位置**：`E:\ai产出文件\牛马\mutual\mutual\ecosystem-manual\`

```
ecosystem-manual/
├── README.md                    # 总索引入口（30秒版）
├── work-groups.md               # 常用工作群活跃度统计
├── skill-inventory.md           # Skill 完整清单（按类别）
├── sop-index.md                 # 跨工作区 SOP 索引
├── mcp-tools.md                 # MCP 工具清单 + 状态
├── distillations/
│   ├── self-voice-dna.md        # 小黎文风DNA（从创作区同步+自动更新）
│   └── contacts/
│       ├── {联系人名}.md        # 每个频繁联系人的蒸馏结果
│       └── ...
└── meta.json                    # 上次刷新时间、下次执行时间
```

### 组件2：每周定时任务（周日晚 22:00）

**自动化流程**：
1. 扫描微信 DB → 统计所有活跃群（近30天有消息的）
2. 扫描 5 个工作区 skills/ + SOPs/ + .mcp.json → 重建索引
3. 检查新的聊天导出 → 增量蒸馏频繁联系人
4. 从最新对话历史中提取小黎文风DNA → 更新自蒸馏
5. 写入 ecosysystem-manual/ 下所有文件

**执行方式**：通过 `create_tasks` 创建定时任务，execution_type=auto

### 组件3：文风DNA自动注入规则

**位置**：`.claude/rules/voice-dna-auto-inject.md`

**规则**：
- 用户要求写作时，自动读取 `ecosystem-manual/distillations/self.md`
- 正式文体（论文/报告/PRD）不注入，其他一律注入
- 注入时机：在生成内容前，先加载文风DNA到工作记忆

### 组件4：女娲蒸馏增量更新

**已有资源**：
- `wechat-distiller` skill（五步蒸馏法）
- `E:\ai产出文件\牛马\创作\创作\output\personality_profiles\`（已有 7 个蒸馏结果）
- `E:\ai产出文件\牛马\创作\创作\output\wechat_exports\`（已有聊天导出）

**增量逻辑**：
- 每周检查是否有新的聊天导出文件
- 对新导出执行蒸馏 → 输出到 `ecosystem-manual/distillations/{联系人名}.md`
- 已有蒸馏结果不重复执行（除非聊天新增 > 500 条）

---

## 实施步骤

### Step 1：创建 ecosysystem-manual/ 目录结构
### Step 2：生成当前快照（skill/SOP/MCP/工作群/蒸馏）
### Step 3：创建文风DNA自动注入规则（.claude/rules/）
### Step 4：创建周日晚定时任务（create_tasks）
### Step 5：更新 long-term.md 记录此决策
### Step 6：验证——模拟一次"小黎让我写文章"的场景

---

## 依赖

- 微信 DB 需要已解密（`E:\Data\WeChat_Export\`）
- wechat-distiller skill 可用
- niuma-voice-dna SKILL.md 存在
- 5 个工作区 SOPs 目录可访问
