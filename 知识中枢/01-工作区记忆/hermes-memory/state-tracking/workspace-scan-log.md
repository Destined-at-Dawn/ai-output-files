# 工作区扫描记录

> 每次启动时扫描 6 个工作区的 artifact-registry.md / handoffs/ / project-context/
> 记录扫描时间和发现。

---

## 最近扫描

### 2026-06-21 周度深度巡检

**扫描时间**：2026-06-21 21:33 (cron)

| 工作区 | artifact-registry | handoffs/ | project-context/ | memories | long-term.md |
|--------|-------------------|-----------|-----------------|----------|-------------|
| mutual/mutual | 8 条 | 0 | 2 文件 | 35 | 310 行 (20K) ⚠️ |
| 个人/个人 | 0 条（模板） | 0 | 1 文件 | 24 | 79 行 (8K) |
| 创作/创作 | 4 条 | 0 | 1 文件 | 9 | 161 行 (12K) |
| 学习/学习 | 0 条（模板） | 0 | 1 文件 | 4 | 76 行 (4K) |
| 求职/求职 | 0 条（模板） | 0 | 1 文件 | 13 | 126 行 (12K) |
| 竞赛/竞赛 | 0 条（模板） | 0 | 1 文件 | 24 | 103 行 (8K) |

**自动修复**：
- 5 个今日记忆模板创建
- atomic-facts.md 压缩（178→107 行，-40%）
- 2026-06-20 Codex handoff 消费并归档

**发现**：
- mutual/mutual CLAUDE.md Hermes 规则缺 tool-ecosystem-scan.md（其他 5 区完整）
- 5/6 注册表为空模板（已知问题）
- mutual/long-term.md 310 行接近膨胀阈值
- 本周无新增教训，无需升级铁律

---

### 2026-06-20 周度深度巡检

**扫描时间**：2026-06-20 03:00 (cron)

| 工作区 | artifact-registry | handoffs/ | project-context/ |
|--------|-------------------|-----------|-----------------|
| mutual/mutual | 8 条（7 usable, 1 archived） | 空 | 2 文件（TEMPLATE + PROJ-生态优化） |
| 个人/个人 | 0 条（模板） | 空 | 1 文件（TEMPLATE） |
| 创作/创作 | 4 条（all usable） | 空 | 1 文件（TEMPLATE） |
| 学习/学习 | 0 条（模板） | 空 | 1 文件（TEMPLATE） |
| 求职/求职 | 0 条（模板） | 空 | 1 文件（TEMPLATE） |
| 竞赛/竞赛 | 0 条（模板） | 空 | 1 文件（TEMPLATE） |

**发现**：
- 创作区新增 4 条产出（科研日报+GSAP+SkVM品读+SkVM信息差），均已登记
- 所有 handoffs/ 目录仍为空
- PROJ-生态优化 项目卡已 Active 23 天（2026-05-28 创建），关闭条件未满足
- 5 区注册表仍为空模板，cross-tool-state.md 已有完整"应登记产出"清单待用户决策
- 05-每日记忆/ 有 5 个 Codex 交接文件已消费并提取事实（6/17-6/19）

**CLAUDE.md Hermes 规则一致性**：
- mutual：简短版（相对路径，缺 tool-ecosystem-scan.md）
- 个人/创作/学习/求职/竞赛：完整版（绝对路径，含 3 个文件）
- **日常学习：无 Hermes 规则**（独立工作区，不在 6 区列表中但有内容）

---

### 2026-06-11 初始扫描

**扫描时间**：2026-06-11

| 工作区 | artifact-registry | handoffs/ | project-context/ |
|--------|-------------------|-----------|-----------------|
| mutual/mutual | 7 条（6 usable, 1 archived） | 空 | 2 文件（TEMPLATE + PROJ-生态优化） |
| 个人/个人 | 0 条（模板） | 空 | 1 文件（TEMPLATE） |
| 创作/创作 | 0 条（模板） | 空 | 1 文件（TEMPLATE） |
| 学习/学习 | 0 条（模板） | 空 | 1 文件（TEMPLATE） |
| 求职/求职 | 0 条（模板） | 空 | 1 文件（TEMPLATE） |
| 竞赛/竞赛 | 0 条（模板） | 空 | 1 文件（TEMPLATE） |

**发现**：
- 仅 mutual 有实际产出登记，其余 5 区注册表为空模板
- 所有 handoffs/ 目录为空（无待消费交接）
- 仅 mutual 有项目卡（PROJ-生态优化），其余为空模板
- 已从 mutual 的 long-term.md 和 2026-06-11.md 提取 18 条原子事实

---

> 创建：2026-06-11 | Hermes v1.0 初始化
> 最后更新：2026-06-21
