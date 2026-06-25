# 飞书 Image Block 和 Divider 在 Wiki 中不支持

> **教训 E36** | 2026-06-06 | 来源：本轮对话——飞书 blocks 批量写入

---

## 踩坑过程

### Divider（block_type=14）
- 独立文档：✅ 可用
- Wiki 文档：❌ 返回 `invalid param`
- 解决方案：用 heading 或空段落代替分隔线

### Image（block_type=27）
- 独立文档：❌ API 创建始终返回 `invalid param`
- Wiki 文档：❌ 同上
- 根因：飞书 image block 通过 API 创建有平台限制（需要先上传图片获取 file_token，再用 file_token 创建 image block，但即使 file_token 有效也可能失败）

## 根因

飞书 wiki 文档的 children API 支持的 block 类型比独立文档少：
- ✅ TEXT(2)、H1(3)、H2(4)、H3(5)、Ordered(13)、Quote Container(34)
- ❌ Divider(14)、Image(27)、Table(?)、Callout(?)

## 正确做法

1. **写入 wiki 前**先做类型可用性探测——发一个最小化测试 block
2. **Divider 替代方案**：用 H2 标题做板块分隔（视觉效果类似）
3. **Image 替代方案**：用户在飞书 UI 手动插入图片
4. **建立 wiki 可用 block 白名单**，不在白名单内的不要尝试

## 退出判据

- wiki children API 返回 `invalid param` → 检查 block_type 是否在白名单内
- 连续 2 个同类 block 失败 → 标记为 wiki 不支持，切换替代方案

## 关联

- feishu-api-protocol.md 铁律 7（Wiki 注意事项）
- 教训 E34（Block Type 映射错误）
