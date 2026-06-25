# 生态系统每日健康报告 2026-06-17

> 自动化定时任务 · 数据采集时间 08:55 CST
> 对比基线：2026-06-15 审计报告 + 2026-06-16 long-term.md 更新

---

## 系统指标（对比上次审计 06-15）

| 指标 | 今日 (06-17) | 上次 (06-15) | 变化 | 状态 |
|------|-------------|-------------|------|------|
| active_skills | 98 | 117 | -19 | ⚠️ 大幅下降 |
| deprecated_skills | 19 | 23 | -4 | ✅ 清理中 |
| total_routes | 105 | 104 | +1 | ✅ |
| total_triggers | 1633 | 1628 | +5 | ✅ |
| unrouted_skills | 8 | 8 | 0 | ⚠️ 未改善 |
| trigger_conflicts | 14 | 11 | +3 | ❌ 恶化 |
| sop_count | 8 | 8 | 0 | ✅ |
| empty_sops | 0 | 0 | 0 | ✅ |
| thin_skills (<200B) | 0 | N/A | - | ✅ |
| orphan_skills | 2 | N/A | - | ⚠️ |
| shared_rules (mutual) | 30 | N/A | - | ✅ |
| 知识中枢教训总数 | 98 | N/A | - | ✅ |

---

## 关键变化分析

### 1. active_skills 大幅下降 117→98（-19）

**可能原因**：部分 skill 目录被删除或移入 deprecated，而非新增弃用标记（deprecated 从 23 降到 19，说明有些 skill 被彻底清理了）。需要确认这 19 个 skill 是有意删除还是误操作。

**风险**：如果有 skill 被删除但路由表仍保留条目，会造成幽灵路由。当前路由表 105 条，routed_skills 105 个唯一名——需核实是否有路由指向已删除的 skill。

### 2. trigger_conflicts 14→11→14（+3 新冲突）

新增冲突来自已知问题的扩散：
- "文风DNA" 冲突从 2 个 skill 扩散到 3 个（加入 wechat-consultant）
- "有没有现成的"/"自动化脚本"/"自动化流程" 冲突（li-bestskill vs li-script / li-workflow vs li-script）

**根因**：触发词设计时各 skill 独立添加，缺乏全局去重审查。

### 3. 8 个 unrouted skills 持平

| Skill | 类型 | 风险 |
|-------|------|------|
| baoyu-infographic | 内容 | 🟡 配图能力不可触发 |
| competition-yolo | 竞赛 | 🟡 竞赛场景不可触发 |
| dot-skill | 工具 | 🟢 内部工具，低优先 |
| li-embedded | 嵌入式 | 🔴 嵌入式开发场景不可触发 |
| li-zhongshu | 治理 | 🟡 知识中枢守护不可触发 |
| personal-info-discovery | 个人 | 🟢 低频场景 |
| session-audit | 审计 | 🟢 已有 hook 自动触发 |
| workflow-automator | 工程 | 🟢 与 li-workflow 重叠 |

---

## 4 个工作区同步状态

| 工作区 | long-term | 近期记忆 | 最新文件日期 | 待同步教训 |
|--------|-----------|---------|-------------|-----------|
| 个人 | ✅ 5.5KB | 4 | 06-12 | ⚠️ 无 06-13~17 记录 |
| 创作 | ✅ 10.4KB | 5 | 06-09 | ⚠️ 无 06-10~17 记录 |
| 竞赛 | ✅ 7.5KB | 9 | 06-15 | ✅ 最新 |
| 求职 | ✅ 9.6KB | 4 | 06-15 | ✅ 最新 |

### 需要同步的新教训

1. **2026-06-16 Junction 迁移 + 4 个技术坑**（知识中枢已有）
   - robocopy 退出码 1/3 是成功
   - PS5.1 + 中文 Windows 读 UTF-8(无BOM) 崩溃
   - app 关了 ≠ 文件夹解锁
   - 不能 Stop-Process -Name Claude
   - **同步方向**：→ mutual memory + competition memory（竞赛区常用脚本）

2. **2026-06-15 HTML 个人站经验孤岛化治理**（知识中枢已有）
   - **同步方向**：→ creation memory（创作区涉及个人网站）

---

## 共享规则一致性

| 工作区 | 规则数 | 状态 |
|--------|--------|------|
| mutual | 30 | ✅ 基准 |
| personal | 21 | ⚠️ 差 9 条 |
| creation | 24 | ⚠️ 差 6 条 |
| competition | 26 | ⚠️ 差 4 条 |
| job | 21 | ⚠️ 差 9 条 |

> 注：差异部分包含工作区特有规则，不一定需要同步。但共享规则（如 no-blind-overwrite、script-safety-check 等）应确保全覆盖。

---

## Git 健康

- 最近提交：2026-06-17 08:51（auto batch commit）
- NiumaAutoCommit 正常运行 ✅
- 最近 5 次提交间隔：~2-8 小时，节奏正常

---

## 待处理问题（按优先级）

### 🔴 高优先

1. **active_skills 骤降 19 个** — 需确认是有意清理还是误删。如果是有意的，更新 runtime-snapshot 和 long-term.md 中的数字。
2. **trigger_conflicts +3 新冲突** — 文风DNA 相关触发词已扩散到 3 个 skill，必须做一次去重审查。

### 🟡 中优先

3. **8 个 unrouted skills 持平未改善** — li-embedded（嵌入式开发）和 competition-yolo（竞赛训练）对用户日常价值较高，建议优先补注册。
4. **个人区/创作区记忆断档** — 个人区 06-12 后无记录、创作区 06-09 后无记录，说明这两个区近 5 天无活跃对话或记忆未落盘。
5. **Junction 教训未同步到 mutual/competition** — 知识中枢已记录但本地 memory 未更新。

### 🟢 低优先

6. **共享规则数量差异** — personal/job 各 21 条 vs mutual 30 条，需确认哪些是遗漏的共享规则。
7. **ChatGPT Plus 续费提醒** — 2026-06-27 到期，还剩 10 天。

---

## 今日建议行动

1. **核实 skill 清理记录** — 查看 06-15 到 06-17 期间的 git log，确认 19 个 skill 的去向
2. **触发词去重** — 对 14 个冲突触发词做优先级裁决，更新路由表
3. **补注册 2 个高价值 unrouted skill** — li-embedded + competition-yolo
4. **同步 Junction 教训** — 写入 mutual memory/2026-06-17.md
5. **更新 runtime-snapshot.md** — 数字已过时（仍写着 92 routes/140 skills）

---

## 教训同步状态

| 来源 | 教训 | 同步目标 | 状态 |
|------|------|---------|------|
| 知识中枢 06-16 | Junction + 4 技术坑 | mutual + competition | ⚠️ 待同步 |
| 知识中枢 06-15 | HTML 孤岛化治理 | creation | ⚠️ 待同步 |
| 知识中枢 06-14 | 动手前检查门禁 | 已全局部署 | ✅ 已同步 |

---

*报告生成：自动定时任务 · 下次审计：2026-06-18*
