# MCP 配置协议（硬约束 — 违反即事故）

> 来源：3 次真实配置事故（写错路径 / import 不存在的函数 / 多余 cmd 包装）
> 创建日期：2026-05-26
> 优先级：等同 script-safety-check.md

---

## 铁律 1：配置路径

**Newmax 读取的 MCP 配置文件是 `~/.newmax/.mcp.json`，不是 `~/.mcp.json`。**

| 环境 | 配置路径 | 备注 |
|------|---------|------|
| **Newmax（牛马AI）** | `C:\Users\13975\.newmax\.mcp.json` | ✅ 唯一正确路径 |
| Claude Code 原版 | `C:\Users\13975\.mcp.json` | ❌ Newmax 不读这个 |

- ❌ **禁止**往 `~/.mcp.json` 写 MCP 配置（写了也白写，Newmax 不会加载）
- ✅ **必须**写入 `~/.newmax/.mcp.json`
- 写入前必须 Read 该文件当前内容（No Blind Overwrite）

---

## 铁律 2：命令格式

**Newmax 直接调用可执行文件，不需要 `cmd /c` 包装。**

```json
// ✅ 正确
{ "command": "npx", "args": ["-y", "some-package"] }
{ "command": "python", "args": ["some_script.py"] }

// ❌ 错误（多余的 cmd 包装）
{ "command": "cmd", "args": ["/c", "npx", "-y", "some-package"] }
{ "command": "cmd", "args": ["/c", "python", "some_script.py"] }
```

**例外**：只有当命令本身是 Windows 内置命令（如 `dir`、`type`）时才需要 `cmd /c`。
npm/npx/pip/python/node 等一律直接调用。

---

## 铁律 3：markitdown MCP 启动方式

**`markitdown_mcp` 包没有顶层 `main` 函数，禁止用 `from markitdown_mcp import main`。**

正确启动方式（写在 wrapper 脚本中）：
```python
import runpy
runpy.run_module("markitdown_mcp", run_name="__main__")
```

Wrapper 脚本位置：`~/.newmax/scripts/markitdown_quiet.py`

---

## 铁律 4：写入后必须验证

**每次修改 `.newmax/.mcp.json` 后，必须执行以下验证：**

1. **JSON 语法检查**：用 python 解析确认无语法错误
   ```bash
   python -c "import json; json.load(open(r'path/to/.mcp.json'))"
   ```
2. **文件存在确认**：Read 文件确认内容正确
3. **启动测试**（新增 MCP 时必须）：用 `echo '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"0.1"}}}' | npx -y some-package` 测试能否正常启动
4. **告知用户重启**：新 MCP 在下次会话才会加载

---

## 铁律 5：不要残留旧配置

**修改 MCP 配置后，检查是否有旧位置的残留文件。**

- 修改 `~/.newmax/.mcp.json` 后，检查 `~/.mcp.json` 是否有冲突配置
- 如果有 → 清理或同步（避免两份配置不一致导致混乱）

---

## MCP 新增清单（每次新增 MCP 前逐项检查）

- [ ] 配置写入 `~/.newmax/.mcp.json`（不是 `~/.mcp.json`）
- [ ] 命令格式无 `cmd /c` 包装（除非是 Windows 内置命令）
- [ ] 依赖包已安装（`pip install` / `npm install`）
- [ ] 启动测试通过（stdin initialize 握手）
- [ ] JSON 语法验证通过
- [ ] 已告知用户需要重启会话
- [ ] 旧配置位置无冲突残留
