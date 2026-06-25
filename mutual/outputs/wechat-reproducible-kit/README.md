# 微信聊天分析可复刻工具包 v1.2

> 拿到这个包，你就能：解密微信数据库 → 导出聊天记录 → 过滤有价值信息 → 分析人格画像。

---

## 四步执行路线

### Step 1：环境准备（5分钟）

```bash
pip install zstandard
```

### Step 2：提取密钥（需要微信运行 + 管理员权限）

1. 确保微信已登录且正在运行
2. 以管理员身份打开终端
3. 运行 `tools/wx_key/wx_key.exe`（如果包含在包中）
4. 复制显示的密钥（hex 字符串）

### Step 3：解密数据库

1. 关闭微信
2. 找到微信数据目录（通常在 `D:\data\wechat\xwechat_files\wxid_xxx\`）
3. 用 WeChatDataAnalysis 工具解密 `db_storage/message/` 下的数据库
4. 输出到指定目录

### Step 4：运行分析

```bash
# 分类汇总报告
python scripts/analyze_wechat.py --db-dir 解密DB目录

# 导出特定聊天
python scripts/export_chat.py --db-dir 解密DB目录 --name "联系人名"
```

---

## 包结构

```
wechat-reproducible-kit/
├── README.md                          ← 你在读的这个文件
├── requirements.txt                   ← 依赖包
├── scripts/
│   └── analyze_wechat.py              ← 分类汇总脚本（已验证 33.9 万条）
├── skills/
│   ├── wechat-analysis/               ← 主入口 skill（v3.0）
│   ├── wechat-exporter/               ← 导出 skill（v1.0）
│   ├── wechat-distiller/              ← 蒸馏 skill（v1.0）
│   ├── community-filter/              ← 社群过滤 skill（v2.0）
│   └── wechat-db-update/              ← DB更新触发器（v1.0）
├── sop/
│   └── wechat-analysis-sop.md         ← 四阶段完整流水线
└── lessons/
    ├── pitfalls.md                    ← 22 条踩坑铁律
    ├── db-structure.md                ← 数据库结构速查
    └── tool-selection.md              ← 工具选型理由
```

---

## Skill 体系

| Skill | 触发词 | 功能 |
|-------|--------|------|
| wechat-analysis | 微信/聊天记录/聊天统计 | 主入口：分类汇总/精细查询 |
| wechat-exporter | 导出聊天/转成MD | DB→MD 转换 |
| wechat-distiller | 蒸馏/心理画像 | 五维心理分析 + 人格 Skill |
| community-filter | 社群过滤/资源清单 | 噪音过滤 + 百大认知交叉 |
| wechat-db-update | 更新微信/刷新聊天 | DB更新后自动触发全套 |

---

## 已知限制

1. **wx_key 工具未包含在 v1.1 包中**（体积 18MB），需要单独获取
2. **图片文件路径映射未完成**：34,959 张图片全部 AES 加密，需要从 DB 中提取密钥
3. **群聊发送者名称**：部分群聊有 2.6% 的消息无法解析发送者（纯图片/表情消息）

---

## 更新日志

### v1.2 (2026-06-11)
- 重新打包（旧 zip 归档至 `E:\ai产出文件\牛马\归档\`）
- 确认 v1.0 无法重建（wx_key 58MB 字体工具已丢失）
- v1.2 为当前活跃版本，仅含精简内容（无 wx_key 等大文件）

### v1.1 (2026-06-09)
- 新增 wechat-db-update skill（DB更新触发器）
- 新增 lessons/ 目录（22条铁律 + DB结构 + 工具选型）
- 更新 community-filter 到 v2.0（噪音模式库 + 百大认知交叉）

### v1.0 (2026-06-07)
- 初始版本
- 包含 analyze_wechat.py + export_chat.py + wx_key 工具
