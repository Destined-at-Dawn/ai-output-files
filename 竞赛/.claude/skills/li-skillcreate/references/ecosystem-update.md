# Phase 5 详细生态更新协议

> 本文件是 li-skillcreate SKILL.md Phase 5 的详细参考，包含一鱼多吃（生态副作用写入）的完整流程。

---

## 总则

技能创建并验证后，**必须**执行以下生态更新（至少 5 个）。

---

## ① 注册路由表

更新 `skill-routing-table.json`，添加新路由条目：

```json
{
  "id": "r0XX",
  "triggers": ["触发词1", "触发词2", "..."],
  "context": ["场景描述"],
  "skill": "skill-name",
  "mcp": null,
  "priority": N,
  "auto": true,
  "confidence": 0.8,
  "note": "路由说明"
}
```

**触发词设计原则**（来源：li-devil）：
- 初始触发词从用户真实对话中提取
- 不是猜用户会说什么，而是记录用户实际说了什么
- 路由创建后观察 1 周，无命中则调整触发词

---

## ② 更新今日记忆

Edit 追加到 `memory/{today}.md`：

```markdown
## [时间] 创建/迭代技能：[技能名]
- 类型：[新建/迭代]
- 参考技能：[N 个]
- 核心机制：[1-2 句]
- 文件路径：~/.newmax/skills/[name]/
- 文件大小：[N] 个文件 / [X] KB
- 路由：r0XX（[触发词数] 个触发词）
```

---

## ③ 更新 skill-catalog

如果工作区有 skill-catalog 文件，追加新条目。

---

## ④ 更新 artifact-registry.md

如果文件存在，追加新产出登记。

---

## ⑤ 更新调研画像

如果技能创建过程中调研了用户习惯，更新 `memory/research-profile.md`。

---

## ⑥ 记忆候选

如果创建过程中发现了值得沉淀的教训或偏好：

```
📋 记忆候选
- 类型：[教训/偏好/决策]
- 内容：[一句话]
- 建议写入：memory/long-term.md § [章节]
```
