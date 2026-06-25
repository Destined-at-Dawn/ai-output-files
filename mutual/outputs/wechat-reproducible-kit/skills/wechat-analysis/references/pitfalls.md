# 微信聊天分析踩坑铁律（22 条）

> 来源：实测 16 个 DB + 19 个导出文件 + 5 轮调试（2026-06-07~09）

---

## 一、密钥与解密（1-5）

### 1. 密钥只在内存中
微信运行时密钥存在进程内存里，必须用 wx_key 等工具从正在运行的微信进程中提取。
**不能**从文件/注册表/配置中读取密钥。

### 2. wx_key 需要管理员权限
提取密钥的工具（wx_key.exe）必须以管理员身份运行，否则无法读取微信进程内存。

### 3. 微信必须正在运行
密钥提取前不能关闭微信。提取完成后可以关闭。

### 4. Temp 目录清理风险
解密后的 DB 通常放在 `%TEMP%` 目录，Windows 磁盘清理可能删除。
**建议**：解密后立即复制到安全位置。

### 5. hex 匹配在新版失效
旧版微信密钥是固定长度的 hex 字符串，新版可能改变格式。
**应对**：用 wx_key 官方版本，不要自己写正则匹配。

---

## 二、数据库（6-10）

### 6. 表名会变
不同微信版本的表名可能不同。不要硬编码表名，先用 `sqlite_master` 查询。
```python
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
```

### 7. zstd 压缩必须处理
新版微信（8.0+）的 `CompressContent` 字段用 zstd 压缩。magic bytes：`28 B5 2F FD`。
不解压直接读 StrContent 可能为空或乱码。

### 8. sender_id 因聊天而异
同一个 sender_id 在不同聊天中代表不同的人。详见 `sender-resolution.md`。

### 9. CreateTime 是 Unix 时间戳
单位是秒（不是毫秒）。转北京时间：`datetime.fromtimestamp(ts, tz=timezone(timedelta(hours=8)))`

### 10. 部分消息内容为空
StrContent 和 CompressContent 可能都为空（系统消息、特殊类型）。需要检查并跳过。

---

## 三、编码与脚本（11-16）

### 11. Bash heredoc 含中文必炸
Windows MSYS2/Git Bash 下，heredoc 中的中文会被 locale 层破坏。
**铁律**：含中文的脚本一律用 Python 写文件再执行。

### 12. PowerShell 脚本需要 GBK
Windows PowerShell 默认编码是 GBK，不是 UTF-8。写 .ps1 文件时用 `encoding='gbk'`。
或用 `powershell -ExecutionPolicy Bypass -File script.ps1` 执行。

### 13. Python 脚本用 UTF-8
Python 脚本文件用 `encoding='utf-8'` 写入。Python 原生支持 Unicode 路径。

### 14. PowerShell $_ 在 bash 中失败
Bash 会在 PowerShell 看到 `$_` 之前展开它。必须用脚本文件模式，不能内联。

### 15. Read 工具对中文路径有假阴性
Read 工具可能对中文路径返回 "File does not exist" 但文件实际存在。
**验证层级**：Python > grep > Read。

### 16. 终端 GBK ≠ 文件内容
终端输出的中文可能是 GBK 编码，但文件内容是 UTF-8。不要用终端输出判断文件内容。

---

## 四、导出与分析（17-22）

### 17. 群聊需要 Name2Id 映射
群聊消息的 sender_id 需要查 Name2Id 表或 contact.db 才能转为昵称。

### 18. 拍一拍占 40%+ 噪音
系统消息（Type=10000）中，拍一拍消息占比极高。分析前必须过滤。

### 19. 信息密度 < 2%
群聊中真正有价值的信息（文件/链接/方法论）不到 2%。关键词匹配会产生 95%+ 噪音。
**正确做法**：先去噪（过滤拍一拍/表情/短文本），再做价值提取。

### 20. 关键词匹配对聊天记录无效
"工作"匹配到"工作群"、"分享"匹配到"分享日常"。需要更精细的信号检测。

### 21. attach/ 目录全部 AES 加密
`msg/attach/` 下的图片全部 AES 加密（magic bytes `07 08 56 32`），无法直接读取。
需要通过 `message_resource.db` + `hardlink.db` 映射到解密后的路径。

### 22. file/ 和 video/ 未加密
`msg/file/` 下的文档（PDF/DOCX/HTML）和 `msg/video/` 下的视频**未加密**，保留原始文件名。
可以直接读取和复制。
