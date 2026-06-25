---
name: feishu-doc-writer
description: 将 Markdown 内容直接发布为飞书文档。支持创建新文档、追加到已有文档、创建到知识库。
metadata: {"moltbot":{"emoji":"✏️","requires":{"bins":["python3"]}}}
---

# Feishu Document Writer

将 Markdown 内容通过飞书 Open API 直接发布为飞书文档。

## 依赖

- **feishu-doc-reader skill**：共享飞书 App 凭证配置（`feishu-doc-reader/reference/feishu_config.json`）
- **Python 3.6+**：仅使用标准库（无第三方依赖）

## 前置条件（必读）

飞书 App 需要以下权限（在[飞书开放平台](https://open.feishu.cn)后台配置）：

| 权限 | 用途 |
|------|------|
| `docx:document` | 创建和写入新文档 |
| `docx:document:create` | 创建文档 |
| `wiki:wiki` | 在知识库中创建节点（可选） |

> ⚠️ 如果只有 `docx:document:readonly`，只能读不能写。需要在开放平台后台追加写入权限。

## 使用方式

### 1. 创建新文档（从 Markdown 文件）

```bash
python scripts/write_feishu_doc.py create \
  --title "行动手册 9 · AI 榨干每一节课" \
  --from-md outputs/tutorial.md
```

### 2. 创建到指定文件夹

```bash
python scripts/write_feishu_doc.py create \
  --title "教程" \
  --from-md content.md \
  --folder-token fldcnXXXXXX
```

### 3. 创建到知识库（wiki space）

```bash
python scripts/write_feishu_doc.py create \
  --title "新教程" \
  --from-md content.md \
  --wiki-space 7xxxxxxxxxxxxx
```

### 4. 向已有文档追加内容

```bash
python scripts/write_feishu_doc.py append \
  --doc-token docx_XXXXXXXX \
  --from-md extra_content.md
```

### 5. 纯 Markdown 转换（不调 API，只输出 JSON）

```bash
python scripts/md_to_feishu_blocks.py content.md -o blocks.json
```

## 完整发布流程（AI 调用指南）

当用户说"发布到飞书"或"写入飞书文档"时，按以下步骤执行：

```
Step 1: 按 SOP 生成 Markdown 内容 → 保存到 outputs/xxx.md
Step 2: 调用 write_feishu_doc.py create --title "xxx" --from-md outputs/xxx.md
Step 3: 返回文档 URL 给用户
Step 4: 如果失败，检查权限或网络，重试一次
```

## 输出格式

成功时返回 JSON：
```json
{
  "document_id": "docx_XXXXXXXX",
  "title": "文档标题",
  "url": "https://feishu.cn/docx/docx_XXXXXXXX",
  "blocks_written": 42,
  "blocks_total": 42,
  "location": "folder"
}
```

## Markdown → 飞书 Block 映射

| Markdown 语法 | 飞书 Block Type |
|---------------|----------------|
| `# H1` - `###### H6` | heading1 - heading6 |
| 普通段落 | text (type 2) |
| `- 项目` / `* 项目` | bullet (type 12) |
| `1. 项目` | ordered (type 13) |
| ` ```lang ``` ` | code (type 14) |
| `> 引用` | quote (type 15) |
| `- [x] 任务` | todo (type 17) |
| `---` | divider (type 22) |
| **加粗** | bold text_element_style |
| *斜体* | italic text_element_style |
| `行内代码` | inline_code text_element_style |
| [链接](url) | link text_element_style |
| ~~删除线~~ | strikethrough text_element_style |

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| HTTP 403 | App 没有写入权限 | 在飞书开放平台添加 `docx:document` 权限 |
| HTTP 404 | folder_token 或 doc_token 不存在 | 检查 token 是否正确 |
| code 99991663 | 无权限访问文档 | 确保文档已共享给 App |
| 网络超时 | 飞书 API 不可达 | 检查网络，重试 |

## 限速

- 飞书 API 限制：3 请求/秒/应用
- 每次写入最多 50 个 block，超过自动分批
- 脚本内置 0.35 秒间隔，无需手动控制

## 文件结构

```
feishu-doc-writer/
├── SKILL.md                    # 本文件
├── _meta.json                  # 元数据
└── scripts/
    ├── write_feishu_doc.py     # 主写入脚本（创建+追加）
    └── md_to_feishu_blocks.py  # Markdown → 飞书 Block 转换器
```

## 安全注意

- 凭证共享 feishu-doc-reader 的配置，不重复存储
- Token 缓存在 reader 目录，2 小时自动过期
- 写入操作不可撤销（飞书 API 无回滚），建议重要内容先在本地备份 Markdown
