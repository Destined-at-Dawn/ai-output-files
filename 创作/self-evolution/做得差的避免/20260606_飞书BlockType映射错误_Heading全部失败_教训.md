# 飞书 Block Type 映射错误导致 Heading 全部失败

> **教训 E34** | 2026-06-06 | 来源：本轮对话——飞书 blocks 批量写入

---

## 踩坑过程

用 Python 脚本批量写入 64 个 blocks 到飞书文档。heading blocks 全部返回 `invalid param`，普通段落全部成功。

第一轮尝试的映射（错误）：
- heading1 → block_type: 1 ❌
- heading2 → block_type: 2 ❌
- heading3 → block_type: 3 ❌

修正后的映射（正确）：
- heading1 → block_type: 3 ✅
- heading2 → block_type: 4 ✅
- heading3 → block_type: 5 ✅

## 根因

飞书 block_type 编号从 2 开始（2=TEXT），heading 从 3 开始：
- 2 = TEXT（普通段落）
- 3 = H1（一级标题）
- 4 = H2（二级标题）
- 5 = H3（三级标题）
- 13 = Ordered List Item（T13，加粗标题+正文）
- 14 = Divider（⚠️ wiki 不支持）
- 27 = Image（⚠️ API 创建受限）

## 为什么看起来行其实不行

- 普通段落（block_type=2）写入成功，说明 API 本身正常
- 但 heading 用了错误的编号，所有标题全部静默失败
- 没有逐个 block 检查返回值，只看了最后的"成功"统计

## 正确做法

1. **首次写入前**必须测试 3 种核心 block type：TEXT(2) + H2(4) + T13(13)
2. **逐个检查**每个 block 的 API 返回值，不要只看汇总
3. **建立 block_type 映射表**（已在 feishu-api-protocol.md 铁律 7 中）

## 退出判据

- heading block 返回 `invalid param` → 立即检查 block_type 编号
- 连续 3 个同类 block 失败 → 停止批量发送，先排查映射

## 已沉淀到

- feishu-api-protocol.md 铁律 7（Block Type 选用规则）
- SOP-01 Step 7（飞书设计标准）
- SOP-16 §二-B（嘉宾笔记飞书文档设计标准）
