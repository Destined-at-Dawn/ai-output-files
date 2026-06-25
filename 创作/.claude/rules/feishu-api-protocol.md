# 飞书 API 使用协议（Feishu API Protocol）

> **优先级**：最高（违反即事故）
> **创建日期**：2026-06-06
> **来源**：反复出现 "你无权调整链接分享范围，如有需要可联系文档所有者@workbuddy" 弹窗，用户明确要求"永远不想要看到这个"

---

## 铁律 1：禁止调用链接分享权限 API

**绝对禁止**在任何飞书上传脚本中调用以下 API：

```
PUT /drive/v1/permissions/{token}/public
PATCH /drive/v1/permissions/{token}/public
```

**根因**：App（workbuddy）创建的文档，App 自己不是 owner。飞书的权限模型是「创建者 ≠ owner」——App 有 `docx:document` scope 能创建和写入文档，但 **没有文档级权限管理能力**。调用这个 API 会：
1. 返回错误码 99992402 或 1063002
2. **在飞书 UI 弹出恶心的错误提示**："你无权调整链接分享范围，如有需要可联系文档所有者@workbuddy"
3. 这个提示用户**永远不想看到**

**正确做法**：
- 脚本只做：创建文档 → 写入内容 → 完成
- **权限/分享设置完全交给用户在飞书 UI 手动操作**
- 不要"好心"帮用户设权限

---

## 铁律 2：禁止调用协作者管理 API

**禁止**在脚本中调用以下 API（除非已确认 App 有 `docs:permission.member:create` scope 且文档 owner 授权）：

```
POST /drive/v1/permissions/{token}/members
```

**根因**：App 的 tenant_access_token 不是文档 owner，调用此 API 返回 1063002（Permission denied）。

**正确做法**：用户需要协作者管理时，在飞书 UI 手动操作。

---

## 铁律 3：飞书 API 脚本的安全边界

飞书 App（tenant_access_token）**能做**的事：

| 操作 | API | 状态 |
|------|-----|------|
| 创建独立文档 | POST /docx/v1/documents | ✅ 可用 |
| 读取文档 blocks | GET /docx/v1/documents/{id}/blocks | ✅ 可用 |
| 写入内容 blocks | POST /docx/v1/documents/{id}/blocks/batch_create | ✅ 可用 |
| 更新 block 内容 | PATCH /docx/v1/documents/{id}/blocks/{block_id} | ✅ 可用 |
| 删除 block | DELETE /docx/v1/documents/{id}/blocks/{block_id} | ✅ 可用 |
| 上传图片获取 file_token | POST /drive/v1/medias/upload_all | ✅ 可用 |

飞书 App（tenant_access_token）**不能做**的事：

| 操作 | API | 状态 |
|------|-----|------|
| 修改链接分享范围 | PUT /drive/v1/permissions/{token}/public | ❌ 禁止调用 |
| 添加协作者 | POST /drive/v1/permissions/{token}/members | ❌ 禁止调用 |
| 写入 wiki 节点 | POST /wiki/v2/spaces/{id}/nodes | ❌ 需要 wiki space 级授权 |
| 转让文档所有权 | PATCH /drive/v1/permissions/{token}/public/owner | ❌ 禁止调用 |

---

## 铁律 4：Wiki 文档写入的正确路径

Wiki 文档写入需要**双重授权**：
1. **App scope**（开放平台配置）：`wiki:wiki` scope 已开通 ✅
2. **Wiki space 级权限**（飞书 UI 操作）：App 机器人需被添加为 wiki 空间成员

**当前状态**：App 能读 wiki blocks，但写入返回 403（131006: wiki space permission denied）。

**解决方案**：用户在飞书 UI 中将 App 机器人添加为 wiki 空间的编辑者。

**在此之前**：Wiki 内容更新只能由用户手动操作，脚本只负责创建独立文档。

---

## 铁律 5：用户身份 vs App 身份

| 身份 | Token 类型 | 能力 |
|------|-----------|------|
| App 身份 | tenant_access_token | 创建文档、写入内容、上传图片 |
| 用户身份 | user_access_token | 上述全部 + 权限管理 + wiki 写入 |

**用户发现的突破**：用 user_access_token 可以绕过 wiki 权限限制。但获取 user_access_token 需要 OAuth 授权流程（用户点击授权链接）。

**当前可用方案**：
- 创建/写入独立文档 → tenant_access_token ✅
- Wiki 写入 → 需要用户操作或 user_access_token
- 权限管理 → 用户在飞书 UI 手动操作

---

## 铁律 6：创建文档后必须浏览器验证

**每次**用 API 创建文档后，必须用 `browser_open` 打开文档 URL，在浏览器中验证管理员可访问。API 返回成功 ≠ 用户能访问。

**验证清单**：
- [ ] 文档 URL 在浏览器中可打开（无"没有权限"错误）
- [ ] 文档在用户的云盘/知识库中有入口（不是"孤岛文档"）
- [ ] 如需添加成员，用 email 而非 open_id（open_id 跨 app 不通用）

---

## 铁律 7：飞书文档设计标准（写入前必读）

> **来源**：2026-06-06 用户严厉批评——"格式太烂了，wiki 里的笔记不管是内容、结构、颜色、视觉效果都比你现在的好一万倍"。
> **适用范围**：所有通过 API 写入飞书文档的内容（嘉宾笔记、分享记录、教程、知识库文档）。

### 7.1 Block Type 选用规则

| Block Type | block_type 值 | 用途 | 何时用 |
|---|---|---|---|
| **T13（Ordered List Item）** | 13 | **加粗标题 + 破折号 + 正文** | 每个核心观点/要点——这是飞书文档看起来专业的关键 |
| H2 | 4 | 二级标题 | 章节分隔（道/法/术/器/行动清单） |
| H3 | 5 | 三级标题 | 子章节 |
| TEXT | 2 | 普通段落 | 补充说明、背景信息 |
| QTCONT | 34 | 引用容器 | 资源导航卡片、核心金句 |
| CTNR | — | 容器 | 视觉分组（每个观点包一层） |
| GRID | — | 网格 | 多列并排展示（工具对比、方案对比） |

### 7.2 结构模板（嘉宾笔记标准格式）

```
H2: 道 — 核心认知
  T13: 核心判断 — 一句话提炼 + 数据/案例支撑
  T13: 第二个判断 — 同上
  （每个 T13 = 一个独立可传播的认知点）

H2: 法 — 方法论
  T13: 方法名 — 具体步骤（1-2-3 或 if-then 逻辑）
  T13: 关键公式 — 用数据说话

H2: 术 — 具体操作
  T13: 操作步骤1 — 怎么做（动词开头）
  T13: 操作步骤2 — 怎么做
  T13: 操作步骤3 — 怎么做

H2: 器 — 工具与资源
  T13: 工具名 — 能做什么 + 一句话评价
  （或用 GRID 做工具对比卡片）

H2: 认知武器
  T13: 金句1 — 出处/背景
  T13: 金句2 — 出处/背景

H2: 行动清单
  T13: 今天做 — 具体动作
  T13: 本周做 — 具体动作
```

### 7.3 视觉规范

| 规则 | 说明 |
|---|---|
| **禁止多余 emoji** | emoji 降低信息密度，让人感觉累。只在标题层偶尔使用，正文一律不用 |
| **用 T13 而非 TEXT 做要点** | T13 自带有序列表格式 + 加粗标题，视觉层次远优于普通段落 |
| **每个观点独立 T13** | 不要把 3 个观点塞进一个 TEXT block——一个 T13 = 一个可独立传播的认知点 |
| **H2 分隔大板块** | 道/法/术/器/行动清单，每个板块用 H2 开头 |
| **QTCONT 做资源卡片** | 工具链接、参考资源用引用容器包裹，视觉上和正文区分开 |
| **GRID 做对比** | 两个方案/工具并排对比时用 GRID，不用长表格 |

### 7.4 内容质量标准

| 标准 | 说明 |
|---|---|
| **每个 T13 必须有"深挖一层"** | 不是罗列嘉宾原话，而是解释为什么成立、数据支撑是什么 |
| **道法术器每层至少 2 个 T13** | 信息密度不够 = 不及格 |
| **行动清单必须具体到动作** | "今天做XX"而非"建议了解一下XX" |
| **认知武器必须有出处** | 金句 + 来源（书籍/理论/嘉宾原话） |
| **Markdown 格式不进飞书** | 飞书不渲染 `**bold**`，用 API 的 style 字段实现加粗 |

### 7.5 Wiki 写入注意事项

- Wiki 文档不支持 divider（block_type=14），用 heading 替代
- Wiki 文档不支持 callout（block_type=19），用 QTCONT 或 TEXT 替代
- Wiki children API 可能不支持 CTNR/GRID，需要逐个测试

---

## 违规检测信号

以下任何一条出现 = 本协议被违反：

- [ ] 飞书脚本中出现 `permissions/public` API 调用
- [ ] 飞书脚本中出现 `permissions/members` API 调用
- [ ] 用户在飞书 UI 看到 "你无权调整链接分享范围" 提示
- [ ] 脚本试图设置 `link_share_entity` 或 `external_access_entity`
- [ ] 脚本试图添加协作者到文档
- [ ] 创建文档后没有用浏览器验证可访问性（铁律6）
- [ ] 添加成员时用了 open_id 而非 email（open_id 跨 app 不通用）

---

## 脚本模板（安全版）

```python
def create_and_write_doc(title, blocks, token):
    """安全的飞书文档创建流程——只创建+写入，不碰权限"""
    # 1. 创建文档
    resp = requests.post(
        "https://open.feishu.cn/open-apis/docx/v1/documents",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": title}
    )
    doc_id = resp.json()["data"]["document"]["document_id"]

    # 2. 写入内容
    # ... batch_create blocks ...

    # 3. 返回链接，让用户自己管权限
    link = f"https://vcnogbywj044.feishu.cn/docx/{doc_id}"
    return link

    # ❌ 绝对不要：
    # requests.put(f".../permissions/{doc_id}/public", ...)  # 禁止
    # requests.post(f".../permissions/{doc_id}/members", ...)  # 禁止
```

---

## 迭代日志

| 日期 | 变更 | 版本 |
|------|------|------|
| 2026-06-06 | 初版。来源：飞书链接分享 API 导致 UI 弹出权限错误提示，用户明确要求"永远不想要看到这个"。16 个历史脚本需清理 | v1.0 |
| 2026-06-06 | v1.1 **🔴 铁律1追加实战验证**：用 tenant_access_token 创建文档后设 `link_share_entity: closed`，管理员完全无法访问（4个文档100%失败）。**新增铁律6**：创建文档后必须浏览器验证可访问性。**新增认知**：① 不传权限参数 = 默认 tenant_readable = 最安全默认值 ② open_id 跨 app 不通用，添加成员用 email ③ API 独立文档是"孤岛"，不挂云盘无入口。来源：用户严厉批评"管理员看不到自己组织的文档" | v1.1 |
| 2026-06-07 | v1.2 **🆕 迭代日志引用系统性教训**：本协议的所有坑已合并为可执行检查清单——`社群运营/经验库/做得差的/20260606_飞书文档全流程永不再犯检查清单_系统性教训.md`（8个坑→4阶段清单+退出判据）。同步更新：① CLAUDE.md 路由表+1行（飞书文档创建/上传/权限）② 反复试探不切换方案教训（35轮浪费70%根因+方案切换决策树）③ 私域认知「技术信任链路与工具选型」。来源：用户要求"再也不会犯错" | v1.2 |
| 2026-06-07 | v1.3 **🆕 引用 SOP-21**：飞书文档创建的完整流程（§〇 GATE + §一 6步闭环 + §二 Wiki流程 + §三 退出判据 + §四 2轮规则 + §五 权限架构 + §六 陷阱速查）已标准化为 `SOPs/21_飞书文档创建标准流程.md`。本协议作为 API 层铁律被 SOP-21 引用。社群运营 Workflow J 同步更新引用 SOP-21。 | v1.3 |
