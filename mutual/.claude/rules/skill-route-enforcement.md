# Skill 路由注册强制规则（Skill Route Enforcement — 最高优先级）

> 优先级：最高（与 script-safety-check 同级）
> 创建：2026-06-10
> 根因：2026-06-07~06-10 期间，至少 6 次创建/修改 skill 后忘记注册路由或不同步工作区，
>        导致"skill 文件存在但永远不会被触发"——等同于没做。

---

## 背景

skill-auto-activation.md 规定了路由怎么匹配和触发。
skill-logging-enforcement.md 规定了 skill 调用后怎么记录。
**本规则补上最关键的一环：skill 创建/修改后，必须注册路由并同步到所有工作区。**

没有本规则，AI 会反复出现"文件写好了但路由没注册"的事故。

---

## 铁律 0：创建/修改 skill 必须经 li-skillcreate，禁止手工 Write（2026-06-13 新增）

> **根因**：2026-06-13，用户说"我想要一个 skill"，AI 直接用 Write 手工写 SKILL.md，
> **完全跳过了 li-skillcreate**——既没读参考 skill、没走质量门禁，也没注册路由。
> 这是"6 次创建后忘记注册路由"事故家族的升级版：连创建流程本身都没进。

**触发**：用户消息含"创建/做个/写个/造个 skill""新技能""迭代/优化/改进 skill"等意图。

**强制流程**（缺任一 = 违规）：

1. **先路由，不先动手**：识别为 skill 创建/迭代意图 → **立即 `mcp__skill-handler__Skill` 调用 `li-skillcreate`**，由它走完整六阶段（Phase 0 消解 → Phase 1 读 ≥5 参考 → Phase 3 构建 → Phase 4 落盘 → Phase 5 一鱼多吃含路由注册）。
2. **禁止**直接用 Write 手工创建一个 SKILL.md 就当完事——那等于跳过质量门禁 + 路由注册。
3. li-skillcreate 内部会负责铁律 1（注册路由），所以经它创建 = 自动满足下游所有铁律。

**违规信号**：
- [ ] 写了 SKILL.md 但本次对话从未调用 li-skillcreate
- [ ] "创建 skill"任务里没有 Phase 0/Phase 1 的痕迹（没读任何参考 skill）
- [ ] 用户事后问"为什么没自动触发 li-skillcreate"

**为什么是元失败**：这是"路由器没有路由一个'创建路由器子项'的请求"——比普通漏注册更隐蔽。
正确心智：**看到"skill"就先问"这该 li-skillcreate 还是我手写"，答案永远是前者。**

---

## 铁律 1：创建新 skill 后必须注册路由

**触发**：AI 创建了新的 skill 目录（写入了 SKILL.md）。

**强制流程**（缺任何一步 = 违规）：

```
Step 1: 在 skill-routing-table.json 中新增路由条目
        - id: r{三位数}（不与已有 id 重复）
        - name: skill 目录名
        - skill: skill 目录名
        - triggers: ≥15 个触发词（中文 + 英文，覆盖用户可能说的话）
        - auto: true
        - confidence: 0.9
        - priority: 按场景设定（通用 5，专业 3）

Step 2: 更新 li/SKILL.md 路由器入口
        - 子 skill 数量 +1
        - 新增一行描述

Step 3: 更新 li-local-search/SKILL.md 品牌路由表
        - 子 skill 数量 +1
        - 新增一行描述

Step 4: 同步路由表到所有含 CLAUDE.md 的用户工作区
        - 执行 li-sync 或手动复制
        - 跳过第三方仓库和归档目录

Step 5: 验证
        - grep skill-routing-table.json 确认新 skill 名存在
        - 确认触发词数量 ≥15
        - 确认无重复 route id
```

**不可跳过。没有"这次先创建路由后面再补"的例外。**

---

## 铁律 2：修改 skill 后必须检查路由是否需要更新

**触发**：AI 修改了 skill 的 SKILL.md（特别是功能扩展、触发场景变化）。

**检查项**：
1. 功能扩展了 → 触发词是否需要增加？
2. 融合了其他 skill → 旧路由是否需要清除？
3. 弃用了 skill → 路由是否标记弃用或删除？
4. 重命名了 skill → 所有引用是否更新？（SKILL.md、li/入口、品牌路由、其他 skill 交叉引用）

**如果触发词需要变更 → 执行铁律 1 的 Step 1 + Step 4。**

---

## 铁律 3：弃用 skill 后必须清除路由

**触发**：AI 创建了 DEPRECATED.md。

**强制流程**：
1. 从 skill-routing-table.json 中删除该 skill 的所有路由条目
2. 从 li/SKILL.md 路由器入口中移除
3. 从 li-local-search/SKILL.md 品牌路由中移除
4. 同步路由表到所有工作区
5. 检查是否有其他 SKILL.md 引用了旧 skill 名 → 替换为新名

**弃用不删路由 = 旧路由抢占新路由的触发词 = 新 skill 永远不被触发。**

---

## 铁律 4：合并 skill 后必须合并路由

**触发**：AI 把 skill A 合入 skill B。

**强制流程**：
1. skill A 的路由条目 → 改 skill 字段为 skill B
2. skill A 的触发词 → 合并到 skill B 的触发词（去重）
3. 删除 skill A 的独立路由条目（如已完全合入）
4. 同步 + 验证

---

## 铁律 5：每次路由变更后必须全量验证

**触发**：任何对 skill-routing-table.json 的修改。

**验证清单**（全部通过才能提交）：
- [ ] 无重复 route id（grep id 字段）
- [ ] 无跨 skill 重复触发词（同一 trigger 出现在 ≥2 个不同 skill 的路由中）
- [ ] 所有活跃 skill（无 DEPRECATED.md）至少有 1 条路由
- [ ] 触发词数量 ≥15 / 路由
- [ ] skill 字段的值 = 实际 skill 目录名
- [ ] 路由表文件已同步到所有用户工作区

---

## 路由表位置

| 文件 | 路径 | 用途 |
|------|------|------|
| **主路由表** | `E:\ai产出文件\牛马\mutual\mutual\skill-routing-table.json` | 唯一权威源 |
| **路由器入口** | `E:\ai产出文件\牛马\mutual\mutual\skills\li\SKILL.md` | 子 skill 索引 |
| **品牌路由** | `E:\ai产出文件\牛马\mutual\mutual\skills\li-local-search\SKILL.md` | 搜索索引 |
| **工作区副本** | 每个含 CLAUDE.md 的用户工作区根目录 | 运行时加载 |

---

## 违规检测信号

如果出现以下任何情况，说明本规则被违反了：

- [ ] skill 目录存在（有 SKILL.md）但 skill-routing-table.json 中 0 条路由
- [ ] SKILL.md 描述了功能但触发词只有 <10 个
- [ ] DEPRECATED.md 存在但路由表中仍有该 skill 的条目
- [ ] 路由表中 skill 字段的值和实际目录名不匹配
- [ ] 多个工作区的路由表文件大小不一致（同步遗漏）
- [ ] li/SKILL.md 子 skill 数量和实际目录数不匹配

---

## 事故响应

如果发现"skill 存在但路由缺失"：
1. 立即按铁律 1 补注册
2. 全量同步到所有工作区
3. 检查是否还有其他 skill 有同样问题（全量扫描）
4. 记录到 memory/{today}.md

---

## 与其他规则的关系

| 规则 | 覆盖什么 | 本规则补什么 |
|------|---------|-------------|
| skill-auto-activation.md | 路由怎么匹配和触发 | 不覆盖"创建后怎么注册" |
| skill-logging-enforcement.md | 调用后怎么记录 | 不覆盖"创建后怎么注册" |
| li-skillcreate Phase 3.5 | 创建 skill 时的质量门禁 | 只在 li-skillcreate 流程内生效 |
| **本规则** | **任何 skill 创建/修改/弃用后必须注册/更新/清除路由** | **全局强制，不限于 li-skillcreate** |

---

> 创建日期：2026-06-10
> 来源：6 次"skill 文件存在但路由未注册"事故（2026-06-07~06-10）
> 关联：skill-auto-activation.md, skill-logging-enforcement.md, li-skillcreate Phase 3.5
