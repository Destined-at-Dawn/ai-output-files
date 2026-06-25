# 技能自动激活硬协议（Skill Auto-Activation Protocol）

> **优先级**：最高（与 chinese-path-safety.md 同级）
> **创建日期**：2026-06-08
> **根因**：路由表存在但 AI 不调用——把 skill 当"可选参考"而非"必须执行的工作流引擎"
> **事故档案**：见 `自我进化/做得差的避免/20260608_skill-routing-dual-files.md`

---

## 核心铁律

**技能和 MCP 是自动的，不是手动的。用户说出来的是需求，不是技能名。**

以下三条违反任何一条 = 技能审计失败：

1. **扫描必做** — 每收到用户消息，必须扫描 `skill-routing-table.json` 匹配触发词
2. **匹配必调** — 匹配到 → 直接用 `mcp__skill-handler__Skill` 调用，**不问用户"要不要用"**
3. **调用必审** — 每轮对话结束前，必须输出技能审计日志（📋 格式）

## 强制流程（每轮对话）

```
收到用户消息
  │
  ├─ Step 1: 关键词扫描（15秒内完成）
  │   从 skill-routing-table.json 的 triggers[] 中匹配用户消息中的关键词
  │   规则：匹配任意一个触发词 → 该条路由激活
  │   多条匹配 → 按 priority 排序（1 最高）
  │
  ├─ Step 2: 自动调用
  │   matched_skills = [s for s in routes if any(trigger in user_msg for trigger in s.triggers)]
  │   for skill in sort_by_priority(matched_skills):
  │       mcp__skill-handler__Skill(skill=skill.name)
  │   注意：多个 skill 可能同时激活（如 hardware-design + karpathy-guidelines）
  │
  ├─ Step 3: 执行 skill 工作流
  │   skill 不是"参考文件"，是"工作流引擎"——强制执行其内部步骤和门禁
  │
  └─ Step 4: 技能审计（对话结束前强制）
      输出 📋 格式审计日志
```

## 路由失败处理

**路由失败 = AI 的问题，不是用户的问题。**

如果用户消息应该触发某个 skill 但没有触发：
1. 在技能审计中如实记录（"被忽视的"栏）
2. 检查路由表是否有对应的触发词 → 没有则添加
3. 分析为什么匹配失败 → 记录改进措施

## 反模式（绝对禁止）

| 反模式 | 为什么错 | 正确做法 |
|--------|---------|---------|
| 手动 Read skill 的 SKILL.md 替代调用 | SKILL.md 只是参考，不强制执行工作流 | 必须通过 `mcp__skill-handler__Skill` 调用 |
| 匹配到 skill 后问用户"要不要用" | 路由表设计就是自动的，问用户 = 把决策负担推回去 | 直接调用，完成后告知 |
| 说"我先看看能不能手动处理" | 绕过了 skill 的门禁和验证流程 | 先调 skill，skill 内部决定处理方法 |
| 手动实现 skill 的功能 | 重复造轮子，且缺少 skill 的经验积累 | 调用 skill，让经验累积在 skill 内部 |
| 读完路由表但不实际匹配 | 路由表是决策引擎，不是参考文档 | 必须执行匹配逻辑 |

## 已验证的失败模式（从真实事故提炼）

### 失败模式 1：路由表空白区
- **现象**：路由表存在但缺少某类 skill 的触发词（如 li-* 系列 0 条）
- **根因**：新 skill 创建后未同步注册到路由表
- **修复**：创建 skill 时必须同时更新路由表
- **检测**：技能审计中"被忽视的"栏出现同类 skill 多次 → 检查路由表

### 失败模式 2：双文件混乱
- **现象**：skill-routing-table.json 和 skill-rules.json 两个文件格式不同，AI 不知道该读哪个
- **根因**：历史遗留，未做废弃清理
- **修复**：skill-rules.json 已标记 deprecated，单一真相源 = skill-routing-table.json
- **检测**：Glob 搜索 `skill-rules*` 和 `skill-routing*` 确认只有 1 个活跃文件

### 失败模式 3：手动替代综合征
- **现象**：AI 读了路由表，但选择"手动处理"而不是调用 skill
- **根因**：AI 把 skill 当成"可选的参考"，而非"必须执行的工作流"
- **修复**：本协议的强制流程
- **检测**：技能审计中"本次调用"为空但用户消息有明确触发词 → 违规

### 失败模式 4：skill 生命周期操作未调用对应 skill（2026-06-13 新增）
- **现象**：执行 skill 创建/拆分/融合/弃用时，直接手动编辑 SKILL.md，未调用 li-skillfusion/li-skillcreate/li-skills-mgmt
- **根因**：AI 把 skill 拆分/融合当成"普通文件编辑"，而非"skill 生命周期操作"
- **修复**：
  - 收到"skill 分离/拆分/融合/创建/弃用"需求时，**必须先调用对应 skill**
  - li-skillfusion：技能拆分/融合/微技能创建
  - li-skillcreate：新 skill 创建
  - li-skills-mgmt：skill 审核/弃用
- **检测**：
  - AI 修改了 SKILL.md 但没有调用 skill → 违规
  - AI 说"我手动编辑一下" → 违规
  - AI 输出了 lifecycle-log.md 但没有调用 li-skillfusion → 违规

**铁律**：skill 是工作流引擎，不是参考文件。skill 生命周期操作必须通过 skill 自身完成。

## 与 CLAUDE.md 的关系

- CLAUDE.md Step 4.5 → 加载 `skill-routing-table.json`（数据）
- 本文件 → 定义如何使用这个数据（协议）
- CLAUDE.md §技能自动激活 → 原则声明（本文件是其可执行展开）

## 自检信号

以下任何一条出现 = 技能自动激活失败：

- [ ] 用户消息有关键词（如"FPGA""调研""代码"），但本轮没有调用对应 skill
- [ ] 技能审计日志中"本次调用"为空
- [ ] 技能审计日志中"被忽视的"非空
- [ ] AI 说"我先手动试试"而不是先调用 skill
- [ ] 路由表中有对应 skill 但 AI 没有匹配到
- [ ] **AI 修改了 SKILL.md 但没有调用 li-skillfusion/li-skillcreate/li-skills-mgmt**（2026-06-13 新增）

---

> 创建日期：2026-06-08
> 来源：11/11 技能调用失败事故（2026-06-08 对话）+ 双路由文件混乱
> 版本：v1.1（2026-06-13 新增失败模式 4：skill 生命周期操作）
> 关联规则：CLAUDE.md §F1（技能审计）、CLAUDE.md Step 4.5（路由表加载）、li-skillfusion、li-skillcreate、li-skills-mgmt
