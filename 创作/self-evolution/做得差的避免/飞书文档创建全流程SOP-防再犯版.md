# 飞书文档创建全流程 SOP——防再犯版

> **教训等级：铁律级** | 2026-06-06
> **用法**：每次飞书操作前逐条过

---

## 前置决策

- 独立文档 → tenant token ✅
- Wiki → user token（没有则创建独立文档替代）

## 10 步流程

| 步骤 | 操作 | 教训 |
|------|------|------|
| 1 | 获取 Token | E31 |
| 2 | 创建文档（只传 title） | E32 |
| 3 | 浏览器验证可访问 | E32 |
| 4 | heading=3/4/5，T13 为主 | E34 |
| 5 | 纯文本清洗 | E29/E30 |
| 6 | 批量写入 <=50 blocks | E34 |
| 7 | 验证 block 数量 | — |
| 8 | 禁止调 permissions API | E37 |
| 9 | 返回链接给用户 | — |
| 10 | 写入当日记忆 | — |

## 禁用 Block（Wiki 不支持）

- Divider(14) → heading 替代
- Image(27) → 用户手动插入
- Callout(19) → TEXT 替代

## 检查清单

- [ ] Token 类型正确
- [ ] heading = 3/4/5
- [ ] 无 Markdown 语法
- [ ] 不调 permissions API
- [ ] 验证 block 数量

---

> 来源：教训 E29-E37
