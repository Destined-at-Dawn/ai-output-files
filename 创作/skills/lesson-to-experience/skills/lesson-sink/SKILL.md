---
name: lesson-sink
parent: lesson-to-experience
version: 1.0.0
description: 教训提取与归档——从对话上下文中自动识别踩坑事件，完成五步闭环
---

# A: lesson-sink（教训提取与归档）

> 对标 `.claude/rules/lesson-sink-checklist.md` 的自动化实现。

---

## 一、问题域

### 1.1 解决什么问题

对话中出现"用户纠正"、"方案失败"、"踩坑"时，需要：

1. 写入当日记忆（.newmax/memory/{日期}.md）
2. 写入负结果日志（negative-results.md）
3. 写入自我进化系统（self-evolution/）← 最容易遗漏
4. 检查是否需要回写 SOP
5. 双写到模块级经验库

当前 Step 3 经常被跳过，Step 5 经常被遗忘。

### 1.2 行家怎么做

真正的知识管理系统（如 Zettelkasten）：

- **即时捕获**：踩坑发生后 30 秒内记录，不等对话结束
- **标准化格式**：每条教训都有固定字段（触发、根因、正确做法、关联）
- **双向链接**：教训 ↔ SOP ↔ 规则 ↔ 案例，形成知识网络

### 1.3 新手/AI 常见问题

- 等到对话结束才记录，结果忘了细节
- 只记"发生了什么"，不记"为什么"和"怎么防"
- Step 3 和 Step 5 经常跳过
- 教训写完不检查是否真的落盘了

### 1.4 做错了什么样

- 教训只在 memory 里，self-evolution 空白 → 新对话读不到历史教训
- 同一个坑踩三次，每次都"记录了"但记录位置不对
- SOP 更新了但教训没关联，下次遇到同类问题找不到参考

---

## 二、使用方式

### 2.1 触发条件（自动识别）

以下信号出现时自动执行：

| 信号 | 示例 |
|------|------|
| 用户否定 | "不对"、"不是这个意思"、"你误解了" |
| 用户纠正 | "应该是..."、"我说的是..."、"你搞错了" |
| 方案失败 | 验证结果不如预期、被用户否决 |
| 流程违规 | 跳过了 F8 技能链、没读 SOP 就动笔 |
| 踩坑 | 报错、遗漏、工具调用失败 |

### 2.2 执行流程

```
触发信号识别
    │
    ▼
Step 1: 提取教训要素
  - 触发事件（用户原话）
  - 根因分析（AI 判断）
  - 正确做法（从用户纠正中提取）
  - 影响范围（涉及哪些模块/SOP/规则）
    │
    ▼
Step 2: 写入 .newmax/memory/{YYYY-MM-DD}.md
    │
    ▼
Step 3: 写入 negative-results.md
    │
    ▼
Step 4: 写入 self-evolution/教训+经验
  - self-evolution/INDEX.md 追加条目
  - self-evolution/lessons.md 追加教训
  - 如有成功经验：self-evolution/做得好的/ 创建文件
  - 如有失败教训：self-evolution/做得差的避免/ 创建文件
    │
    ▼
Step 5: 检查 SOP 回写需求
  - 查 F6 映射表
  - 同类教训 ≥3 次 → 升级为铁律
    │
    ▼
Step 6: 双写到模块级经验库（调用 case-generate）
    │
    ▼
Step 7: 运行双写验证脚本
```

### 2.3 输出

- memory 文件更新 ✅
- negative-results.md 更新 ✅
- self-evolution/ 更新 ✅
- SOP 迭代日志更新（如需要）✅
- 返回教训编号（如 E33）供后续引用

---

## 三、配置

### 3.1 可配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `自动识别` | `true` | 是否自动从对话上下文识别踩坑信号 |
| `即时记录` | `true` | 踩坑后立即记录，不等对话结束 |
| `SOP映射表` | 见 CLAUDE.md F6 | 教训→SOP 的映射关系 |

### 3.2 扩展点

- **自定义触发词**：在 CLAUDE 规则中添加新的触发信号
- **自定义教训格式**：修改负结果日志的模板
- **集成通知**：教训记录后推送提醒到飞书/微信

---

## 四、不可做清单

- ❌ 等对话结束才记录（必须即时）
- ❌ 只写 memory 不写 self-evolution
- ❌ 教训文件不关联 SOP/CLAUDE 规则
- ❌ 声称"已记录"但没有 Read 验证
- ❌ 用 PowerShell 操作中文路径

---

## 五、与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| `lesson-to-experience`（父） | 本 Skill 是父 Skill 的第一步 |
| `case-generate`（下游） | 教训归档完成后，调用 case-generate 生成经验库卡片 |
| `auto-assign`（下游） | 案例卡片生成后，调用 auto-assign 更新索引 |
| `li-improve-agent` | 本 Skill 的教训会反馈给 li-improve-agent 的进化系统 |
| `longmemory` | memory 层的归档由 longmemory 处理 |
