# 飞书 Tenant Token 无法管理文档协作者

> **教训 E37** | 2026-06-06 | 来源：本轮对话——批量设置文档权限

---

## 踩坑过程

用 tenant_access_token 批量给 9 个文档添加协作者：
- 尝试 `POST /drive/v1/permissions/{token}/members` → 全部 1063002（Permission denied）
- 尝试 `PATCH /drive/v1/permissions/{token}/public` → 全部 1063002
- 尝试 `POST /drive/v1/permissions/{token}/members/transfer_owner` → 400 Bad Request
- 尝试用 batch_update API → 1063002

## 根因

飞书的文档权限模型：
- **App 创建文档** → App 是「创建者」但不是「owner」
- **只有 owner 能管理协作者** → App 永远无法管理自己创建的文档的权限
- **tenant_access_token 不具备文档权限管理能力**——这是架构限制，不是 scope 问题

即使开通了 `docs:permission.member:create` scope，tenant_access_token 仍然返回 1063002。

## 为什么看起来行其实不行

- scope 列表里确实有 `docs:permission.member:create`（App 有这个权限）
- 但 App 创建的文档，App 自己不是 owner → 权限管理 API 永远返回 forbidden
- 飞书的「创建者 ≠ owner」设计是故意的（防止 App 滥用权限管理）

## 正确做法

1. **不要尝试用 tenant_access_token 管理协作者**——这是死路
2. **用户在飞书 UI 操作**（30 秒搞定）
3. **如果需要自动化**：走 OAuth 流程获取 user_access_token，用用户身份管理
4. **最终突破**：用户发现同一 App 用 user_access_token 可以管理协作者

## 退出判据

- `POST /drive/v1/permissions/{token}/members` 返回 1063002 → 立即停止，告知用户手动操作
- **最多探测 1 轮**，超过 1 轮 = 浪费

## 关联

- feishu-api-protocol.md 铁律 1/2/5
- 教训 E33（wiki 权限反复排查）
