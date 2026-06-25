# 依赖分析详细流程

> 来源：li-skillfusion Phase 1
> 用途：每次技能操作前必做，评估影响范围

---

## 完整分析步骤

```
1. 读取目标 skill 的 SKILL.md（理解功能边界）
2. 扫描 skill-routing-table.json：哪些路由指向这个 skill？
3. 扫描其他 skill 的 SKILL.md：哪些引用了这个 skill？
4. 扫描记忆文件：用户对这个 skill 的历史评价
5. 读取 skill-usage-log.md：调用频率和成功率
6. 输出依赖图 + 风险评估
```

---

## 依赖图格式

```
target-skill
├── 被引用 by：[skill-A, skill-B]
├── 路由表：[r001, r015]
├── 使用频率：[高/中/低/未使用]
└── 风险等级：[低/中/高]
```

---

## 风险等级判定

| 条件 | 风险 |
|------|------|
| 无其他 skill 引用 + 路由表无条目 + 使用频率低 | 低 |
| 有 1-2 个引用 或 路由表有条目 | 中 |
| 多个 skill 引用 + 高使用频率 + 路由表多条目 | 高 |

**高风险操作**必须先告知用户影响范围，获得确认后才执行。

---

## 扫描命令参考

```bash
# 扫描路由表中指向某 skill 的条目
grep -i "skill-name" skill-routing-table.json

# 扫描其他 skill 的引用
grep -r "skill-name" ~/.newmax/skills/*/SKILL.md

# 检查使用频率
grep -c "skill-name" ~/.newmax/skill-usage-log.md
```
