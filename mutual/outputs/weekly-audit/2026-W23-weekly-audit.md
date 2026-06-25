# 生态系统周报 2026-W23（06-01 ~ 06-07）

## 本周摘要

**li 系列架构定型为 7 子 skill + 212 个全局 skill，沉睡率 96.5% 未改善，路由覆盖 30%，SOP 索引有 3 个空壳条目。NiumaAutoCommit 稳定运行 43 次自动提交。**

---

## 系统健康度趋势（7 天）

| 维度 | 06-01（上周） | 06-07（本周） | 趋势 | 口径 |
|------|-------------|-------------|------|------|
| 已安装 skill（全局） | 198 | 212 | +14 | 粗筛 @ ls ~/.newmax/skills |
| 已安装 skill（mutual 本地） | 31 | 31 | → | 粗筛 @ ls skills/ |
| 路由表条目 | 82 | 78 | -4 | 粗筛 @ skill-routing-table.json |
| 路由覆盖技能数 | ~78 | 63 | -15 | 粗筛 @ unique skill in routes |
| 路由覆盖率 | 39% | 30% | ↓ | 63/212 |
| skill 沉睡率 | 96.5% | ~96.7% | → | 16/212 活跃 |
| SOP 数量 | 3 | 3 | → | SOPs/*.md |
| SOP 空壳条目 | 未检 | 3 | 新发现 | SOP总索引引用但文件不存在 |
| 自动提交 | 正常 | 43 次/7 天 | ✅ | git log --since |
| 手动提交 | — | 3 次/7 天 | — | git log --since |
| .claude/rules 数量 | 15 | 15 | → | 全部有效 |
| 工作区数量 | 5 | 5+1学习 | → | 注册表 |

### 健康度评分：**55/100**（较上周 50/100 微升）

| 子维度 | 分数 | 说明 |
|--------|------|------|
| 路由覆盖 | 15/25 | 30% 覆盖率，120+ skill 无路由 |
| skill 活跃度 | 10/25 | 96.7% 沉睡，本周仅 session-summary 自动调用 |
| SOP 完整性 | 10/20 | 3 个 SOP 有效但总索引引用 3 个不存在的文件 |
| 自动化稳定性 | 15/20 | NiumaAutoCommit 43 次无故障 |
| 记忆系统 | 5/10 | long-term.md 最后更新 06-01，滞后 6 天 |

---

## 技能利用率排行

### 本周被调用的 skill（06-01 ~ 06-07）

| 排名 | Skill | 调用次数 | 场景 |
|------|-------|---------|------|
| 1 | session-summary | 2 | 每日定时任务（06-05, 06-06） |
| 2 | li-skillcreate | 1 | li 系列架构定型（06-06） |
| 3 | li-research | 1 | 纳入 li 系列（06-06） |
| 4 | li-transcript | 1 | DEPRECATED 标记（06-06） |
| 5 | li-local-search | 1 | 路由修复（06-06） |

**本周调用总量：~6 次**（较 06-05 当天 16 次大幅下降）

### 从未被调用（安装 >7 天，0 次调用）

高优先级（与小黎核心需求强相关）：
- **humanizer-zh**（25.7K 安装）— 社群内容去 AI 味
- **learning-boost** — 学习提效（GPA 3.9 的学生从没用过学习工具）
- **blog-post-writer** — 公众号写作
- **interactive-learning** — 交互式学习
- **deep-research**（已被 li-research 取代）— 需确认是否保留

低优先级（场景偏窄）：
- dbs 系列 17 个（商业诊断，当前无商业场景）
- 图片/视频/音频类 12 个（无近期创作需求）

---

## 本周修复记录

| 日期 | 修复项 | 状态 |
|------|--------|------|
| 06-06 | li 系列架构定型（6→7 个子 skill） | ✅ |
| 06-06 | transcript-cleaner → DEPRECATED（li-transcript 超集） | ✅ |
| 06-06 | find-skills → DEPRECATED（li-local-search + li-bestskill 替代） | ✅ |
| 06-06 | 简历修改业务模块 V2（18 文件 + ATS/STAR/去 AI 味） | ✅ |
| 06-07 | Antigravity OAuth 临时用户级代理方案 | ⏳ 待 GUI 验证 |

---

## 本周新增问题

| 问题 | 严重度 | 说明 |
|------|--------|------|
| SOP 总索引空壳 | ⚠️ 中 | `sop-file-operations.md`/`sop-session-lifecycle.md`/`sop-memory-management.md` 不存在 |
| ecosystem-monitoring SOP 过薄 | ⚠️ 中 | 仅 4 步骤，无具体命令/阈值/检查清单 |
| 路由表编码异常 | ⚠️ 低 | `投流帖改写` 路由 skill 名出现乱码（UTF-8 vs GBK） |
| long-term.md 6 天未更新 | ⚠️ 中 | 最后更新 06-01，本周大量决策/教训未沉淀 |
| improvement-cycle-tracker.md 不存在 | ⚠️ 低 | 需创建 |

---

## 下周优先行动（不超过 5 项）

1. **🔴 补齐 SOP 空壳**：创建 `sop-file-operations.md`/`sop-session-lifecycle.md`/`sop-memory-management.md`，或从 SOP 总索引中移除引用
2. **🔴 触发第一次真实 skill 链调用**：用 `humanizer-zh` + `copywriting-skills` 产出一篇社群内容，打破 96.7% 沉睡率
3. **🟡 更新 long-term.md**：06-02 ~ 06-07 的重要决策和教训需归档
4. **🟡 创建 improvement-cycle-tracker.md**：记录改进周期状态
5. **🟢 修复路由表编码**：检查 `投流帖改写` 路由条目的 Unicode 编码

---

## 教训沉淀（本周新增）

| 教训 | 载体 | 状态 |
|------|------|------|
| SOP 总索引引用的文件必须存在，否则索引本身就是空壳 | SOPs/SOP总索引.md（需更新） | 待修复 |
| skill 创建当天 ≠ skill 持续使用，沉睡率不会自动下降 | long-term.md（待写入） | 待归档 |
| Antigravity 代理问题的验收标准：不带 `-x` 的 curl 能访问 Google | memory/2026-06-07.md（已记录） | ✅ |
| li 系列架构定型后 DEPRECATED 标记必须同步到路由表 | long-term.md（待写入） | 待归档 |

---

## 数据完整性声明

### 可写入材料
- ✅ git log 统计（46 commits，43 auto + 3 manual）— 口径：中级 @ git log --since
- ✅ skill 数量（212 全局，31 本地）— 口径：粗筛 @ ls 命令
- ✅ 路由表分析（78 条，63 unique skill）— 口径：中级 @ JSON 解析
- ✅ SOP 文件清单（3 个有效，3 个索引引用不存在）— 口径：粗筛 @ ls + Read

### 不可写入材料
- ⚠️ 沉睡率 96.7% — 口径不足（skill-usage-log.md 只记录了 06-05/06-06 两天数据，其他工作区的调用未统计）
- ⚠️ 健康度评分 55/100 — 无历史基准，首次评分无对比

### 尚不能声称
- ❓ "路由覆盖率下降" — 路由表从 82→78 可能是去重而非丢失，需要逐条对比才能确认
- ❓ "本周无 skill 链调用" — 仅统计了 mutual 工作区的 skill-usage-log，其他 4 区未统计

---

*生成时间：2026-06-07 10:30*
*下次审计：2026-06-14（W24）*
*审计范围：mutual 工作区 + ~/.newmax/skills/ + skill-usage-log.md*
