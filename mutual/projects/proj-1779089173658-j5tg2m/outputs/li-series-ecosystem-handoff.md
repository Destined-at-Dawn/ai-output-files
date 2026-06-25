# li- 系列生态系统交接文档 v4.0

> 最后更新：2026-06-11 | 本文档是给下一个 AI 的可执行指南，不是项目介绍

---

## 1. 快速开始（10 件事）

1. Read  — 48 个 li-* 目录（39 活跃 + 8 弃用 + 1 路由器）
2. Read  — 88 条路由，li-* 占 39 条
3. Read  — 4 个全局 SOP（编排层）
4. Read 5 个工作区 SOP总索引 — 意图路由规则（创作区 14.4KB 最完备）
5. Scan  下 51 个非 li- 活跃 skill — 多数是第三方工具，不改
6. Check  — 创建 skill 后必须注册路由的铁律
7. Check  — 调用 li-* 必须读 references/
8. Verify routing sync:  扫描所有含 CLAUDE.md 的目录
9. Read  — 用户偏好和历史决策
10. Read  — 本文件

---

## 2. 架构

### Progressive Disclosure（硬约束）



### 三层 Tier 架构



---

## 3. 质量标准

### 必备 section（SKILL.md 内）

| Section | 作用 | 检测关键词 |
|---------|------|-----------|
| 设计哲学 | 核心原则 | 设计哲学 |
| 理论锚点 | 认知科学支撑 | 理论锚点 |
| 案例库 | 真实使用案例（禁止编造） | 案例库 |
| 反模式 | 做错的后果 | 反模式 |
| 联动技能 | 与其他 li-* 的协作 | 联动技能 |
| 条件下一步 | 决策表 | 条件下一步 |
| 注意事项 | 边界和限制 | 注意事项 |

### 行数铁律

- SKILL.md <= 300 行（硬限，超出 = 拆到 references/）
- 详细内容全在 references/，主文件只放骨架 + 摘要
- 主文件读完就能工作，references 按需加载

### 案例真实性铁律

- **有真实使用记录** → 写具体案例（日期/场景/结果）
- **没有真实使用** → 写骨架就绪，案例待首次使用后注入
- **编造案例 = 比没有更差** → 已删除 9 个空壳 skill 作为教训

---

## 4. 当前状态（2026-06-11 验证）

### li- 系列（48 个目录）

| 状态 | 数量 | 详情 |
|------|------|------|
| **OK** | 39 | 全部 <=300 行、eval.json、golden_rules >=500B、references >=1 |
| **WARN** | 1 | li（路由器，201 行，无 references — 预期行为） |
| **DEPRECATED** | 8 | li-docs/li-frontend/li-personal/li-platform/li-search/li-session/li-voice/li-writing |

### 路由表

| 指标 | 值 |
|------|-----|
| 总路由 | 88 |
| li-* 路由 | 39 |
| 总触发词 | ~1200 |
| 重复触发词 | 0 |
| 幽灵路由 | 0 |

### 工作区同步

- 42 个工作区已同步（递归 os.walk() 扫描）
- 所有含 CLAUDE.md 的目录都有路由表 + 加载指令
- 第三方仓库（4 个 GitHub 项目）标记只读

### li-intent（SOP 编排引擎）

- 171 行主文件 + 2 个 references
- 从 5 个工作区 SOP总索引提取真实意图模式
- 15 个意图类别 + IF/ELSE 路由规则 + 链式调用 + 自学习框架

---

## 5. 路由系统

### 注册铁律（.claude/rules/skill-route-enforcement.md）



### 同步脚本



### 第三方仓库（只读）



---

## 6. SOP 编排层

### 全局 SOP（mutual/SOPs/）

| SOP | 触发意图 | Skill 调用链 |
|-----|---------|-------------|
| content-analysis | 分析/读/看内容 | baoyu-url → li-analyze → li-memory → li-improve |
| content-creation | 写/创建内容 | li-analyze → li-transcript → li-mindcoach → li-sync |
| skill-lifecycle | 创建/融合/优化 skill | li-bestskill → li-skillcreate → li-skillfusion → li-manage |
| research | 调研/搜索 | li-research → li-devil → li-memory → li-improve |

### 工作区 SOP总索引（意图路由规则）

| 工作区 | 路径 | 大小 | 核心能力 |
|--------|------|------|---------|
| 创作区 |  | 14.4KB | 14 类意图 + 15 条优先级链 |
| 竞赛区 |  | 4.7KB | 13 SOP + 消息路由 |
| 求职区 |  | 3.1KB | 5 SOP + 链式调用 |
| 个人区 |  | 2.6KB | 复盘分析 + 决策 |
| 学习区 |  | 1.9KB | 费曼检验 + 考试准备 |

---

## 7. 工程法则（.claude/rules/ 中的硬约束）

| 规则 | 文件 | 核心 |
|------|------|------|
| **skill-route-enforcement** | skill-route-enforcement.md | 创建 skill 后必须注册路由 |
| **skill-execution-discipline** | skill-execution-discipline.md | 调用 li-* 必须先读 references/ |
| **skill-auto-activation** | skill-auto-activation.md | 触发词匹配 → 自动调用 |
| **skill-logging-enforcement** | skill-logging-enforcement.md | 调用后必须记录日志 |
| **no-blind-overwrite** | no-blind-overwrite.md | 写文件前必须先读 |
| **script-safety-check** | script-safety-check.md | 脚本执行前安全检查 |
| **chinese-path-safety** | chinese-path-safety.md | 中文路径用 Python 不用 Bash heredoc |
| **agent-prompt-ironclad** | agent-prompt-ironclad.md | Agent prompt 必须有三要素 |

---

## 8. 禁区（11 条，违反 = 事故）

| # | 禁区 | 违规后果 | 历史次数 |
|---|------|---------|---------|
| 1 | 编造案例 | 删除整个 skill（已删 9 个） | 2 |
| 2 | 创建 skill 不注册路由 | skill 永远不会触发 | 5+ |
| 3 | 改第三方仓库 | 数据损坏（已回滚 4 次） | 1 |
| 4 | 批量创建 = 低质量壳 | 浪费时间，必须返工 | 3 |
| 5 | 用行数当弃用理由 | li-workflow 110 行有独立价值 | 1 |
| 6 | 搜关键词太窄 | 只找 13★ 漏 23.2K★ | 1 |
| 7 | 不扫深层目录 | 漏掉 32 个嵌套工作区 | 1 |
| 8 | 不读 SOP 就设计 | 凭空设计而 188 个 SOP 已存在 | 2 |
| 9 | 覆写前不 Read | 数据丢失 | 1 |
| 10 | golden_rules 写占位符 | 质量门禁形同虚设 | 2 |
| 11 | 声称已做未验证 | 路由表 0 bytes 无人发现 | 1 |

---

## 9. 未完成任务（按优先级）

### P0（核心缺失）

| 任务 | 详情 | 操作 |
|------|------|------|
| li-intent references 充实 | 只有 2 个 ref 文件 | 从 SOP总索引 提取更多意图模式 |
| li-data 质量升级 | 136 行薄壳 | 读取本地数据分析经验注入 |

### P1（质量提升）

| 任务 | 详情 | 操作 |
|------|------|------|
| Tier 架构文档化 | 1/2/3 层的调用关系 | 写 SOP 编排层文档 |
| conversation-journal 恢复 | 只有 3 个文件 | 每日自动创建 |
| li-* 案例真实验证 | 部分案例是从对话推理的 | 标注待验证 |

### P2（长期优化）

| 任务 | 详情 | 操作 |
|------|------|------|
| 51 个非 li- skill 分类 | 第三方 vs 用户自建 | 逐个决策 |
| SOP 总索引统一格式 | 5 个工作区格式不一 | 制定标准格式 |
| 自进化闭环验证 | li-improve 的 hook 未实测 | 跑一轮完整流程 |

---

## 10. 工作区清单（42 个已同步）

**用户自有**（需同步路由表）：
- mutual / 个人 / 创作 / 学习 / 求职 / 竞赛 / 日常学习
- 各自下的 projects/*/ 子目录（深层嵌套，os.walk() 扫描）

**第三方只读**（不改）：
- mempalace / skills / ppt-master / remotion

**归档**（不改）：
- 归档/ 目录下所有

---

## 11. 决策记录

| # | 决策 | 日期 | 理由 |
|---|------|------|------|
| 1 | Progressive Disclosure 为标准架构 | 06-08 | li-improve 从 668→251 行验证有效 |
| 2 | 删除 9 个空壳 skill | 06-10 | 编造案例比没有更差 |
| 3 | li-workflow 恢复独立 | 06-10 | 110 行不是弃用理由 |
| 4 | SOP总索引 为意图模式库 | 06-11 | 188 个真实 SOP 比任何 JSON 都强 |
| 5 | li-intent 读 SOP 而非静态映射 | 06-11 | SOP 会更新，静态映射不会 |
| 6 | 第三方仓库只读 | 06-09 | 误改 4 个 GitHub 仓库后教训 |
| 7 | os.walk() 全递归扫描 | 06-09 | 漏掉 32 个深层嵌套工作区 |
| 8 | 搜索宽泛优先 + stars 排序 | 06-08 | 13★ vs 23.2K★ 教训 |

---

## 12. 验证清单（新 AI 上手后检查）

- [ ] 60 >= 39
- [ ]  中 li-* 路由数 >= 39
- [ ] 每个 li-* 的 SKILL.md <= 300 行
- [ ] 每个 li-* 有 eval.json + golden_rules.md（>=500B）
- [ ] 0 个跨 skill 重复触发词
- [ ] 42+ 工作区有 skill-routing-table.json
- [ ] 4 个第三方仓库未被修改
- [ ] .claude/rules/skill-route-enforcement.md 存在
