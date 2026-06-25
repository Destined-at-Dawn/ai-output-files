# 失败教训：Python 飞书上传脚本 4 个技术坑——函数冲突 / 中文路径 / Emoji / JSON 转义

## 日期
2026-06-06

## 场景
写 Python 脚本批量上传 Markdown 内容到飞书文档。脚本运行在 Git Bash（Windows）环境，涉及中文路径、emoji 字符、JSON 编码等场景。连续踩了 4 个技术坑，每个都导致脚本中断或输出异常。

## 踩坑清单

### 坑1：函数名与变量名冲突
**表现**：`TypeError: 'int' object is not callable`
**根因**：脚本中定义了函数 `B()` 同时有变量 `B = 10`，Python 解释器把 `B()` 解释为对整数的调用。后续又出现 `H()` 函数和 `H` 变量冲突。
**正确做法**：函数名用 `snake_case`（如 `build_blocks`），变量名用小写或有意义的名称。永远不要用单个大写字母同时做函数名和变量名。Python 不会报命名冲突，只会静默覆盖。

### 坑2：中文路径文件输出为空
**表现**：`python upload.py` 执行后输出文件为空（0 bytes），但脚本逻辑看起来没问题
**根因**：Bash Shell（Git Bash）执行 Python 脚本时，涉及中文路径的文件读写可能因编码问题静默失败。`open()` 不报错但写入 0 字节。
**正确做法**：用 Write 工具写入脚本文件（确保 UTF-8 BOM），用绝对路径执行。验证时用 Read 工具读文件内容，不要依赖终端输出。

### 坑3：Python print emoji 在 Windows GBK 终端崩溃
**表现**：`UnicodeEncodeError: 'gbk' codec can't encode character`
**根因**：Windows 终端默认编码是 GBK，Python print 输出 emoji（如 ✅❌）时 GBK 无法编码。
**正确做法**：
```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```
或者干脆不在 print 中用 emoji，用 `[OK]` `[FAIL]` 等纯 ASCII 标记代替。

### 坑4：飞书 blocks JSON 特殊字符未转义
**表现**：`json.JSONDecodeError` 或 API 返回 `invalid json`
**根因**：Markdown 内容中的引号 `"`、反斜杠 `\`、换行符等特殊字符直接拼进 JSON 字符串，没有转义。
**正确做法**：用 `json.dumps()` 生成 JSON，不要手动拼接字符串。`json.dumps` 会自动处理所有特殊字符转义。
```python
# ❌ 错误：手动拼接
payload = '{"title": "' + title + '"}'

# ✅ 正确：用 json.dumps
payload = json.dumps({"title": title}, ensure_ascii=False)
```

### 坑5：飞书引用块（quote block）格式不兼容
**表现**：108 个 blocks 中有 14 个写入失败，全是引用块（Markdown `>` 格式）
**根因**：飞书 Docx API 的 quote block（block_type 14）格式与普通 text block 不同，不能用相同的 body 结构。
**正确做法**：遇到 `>` 引用格式时，降级为普通文本块（加 `「引用」` 前缀），不尝试写 quote block。或者研究飞书 quote block 的正确 API 格式。

## 用户纠正原话

本轮用户没有直接纠正这些技术问题（用户看不到脚本报错），但这些坑导致：
- 4 个文档创建失败需重建
- 权限问题叠加技术问题，总返工 5+ 轮

## 根因分析

**最深层根因：没有先做小规模测试再批量执行。**

正确流程应该是：
1. 先创建 1 个文档 + 写入 1 个 block → 验证全链路
2. 再批量创建 + 批量写入
3. 最后浏览器验证

实际执行：直接批量创建 4 个文档 → 多处报错 → 返工重建

## 正确流程（飞书上传脚本开发检查清单）

```
1. 单块测试 → 创建文档 + 写入 1 个 block → 验证可访问
2. 格式兼容 → 测试所有 block 类型（text/list/code/quote/table）
3. 中文路径 → 用 Write 工具写脚本，Read 工具验证输出
4. Emoji → sys.stdout.reconfigure 或用 ASCII 标记替代
5. JSON → 绝不手动拼接，用 json.dumps
6. 批量执行 → 确认单块通过后再批量
```

## 关联已有教训
- powershell-safety.md（中文路径编码铁律）：本教训在 Python 维度印证了同一问题
- mcp-config-protocol.md（写入后必须验证）：脚本写入后必须验证输出

## 关联工程法则
- 法则3（实测优先）：先测 1 个再批量，不要假设格式正确
- 法则5（跨边界校验）：Markdown → 飞书 JSON，两种格式的边界处最容易出错
- 法则8（门禁文化）：脚本执行前缺少"单块测试门禁"
