# 中文路径安全规则（CRITICAL — Windows 编码铁律）

> 优先级：最高（与 script-safety-check 同级）
> 创建：2026-06-07
> 根因：Bash heredoc 在 Windows MSYS2/Git Bash 下必炸中文，已反复踩坑

---

## 核心铁律

**涉及中文路径的脚本，一律用 Python 写文件再执行。禁止用 Bash heredoc。**

没有例外。没有"这次试试 heredoc"。没有"单引号 EOF 应该没问题"。

---

## 根因

Windows 下的 Bash（MSYS2/Git Bash）即使使用单引号 heredoc（`<< 'EOF'`），中文字符仍会被 locale 层破坏：
- UTF-8 中文 → 乱码 / 路径不存在 / 静默失败
- 单引号只阻止变量展开（`$var`），不阻止字符编码转换
- 这是 MSYS2 底层问题，无法通过引号、转义、`chcp` 修复

## 正确模式：Python 优先

```python
# 写 Python 脚本到临时文件，然后执行
import os, shutil, json, glob

# Python 原生支持 Unicode 路径，零编码问题
target = r"E:\ai产出文件\some目录"
for f in os.listdir(target):
    print(f)
```

```bash
# 执行方式
python /tmp/task.py
```

**关键**：Python 的 `open()`、`os.listdir()`、`shutil` 全部原生支持 Unicode 路径，无需任何编码处理。

## 禁止模式

| 禁止操作 | 原因 |
|----------|------|
| `cat > /tmp/task.ps1 << 'EOF'` 含中文路径 | heredoc 中文必炸 |
| `powershell -Command "..."` 含中文路径 | bash 先处理字符串，中文被破坏 |
| `echo "中文内容" > file` | echo 的编码取决于 bash locale |
| 任何 bash 内联含中文路径字符串 | bash 解析阶段就可能破坏编码 |

## 场景决策树

```
需要处理中文路径？
  ├── 是 → 用 Python 脚本（写 .py 文件 → python 执行）
  └── 否 → 按 powershell-safety.md 正常流程
```

### 细化决策

| 场景 | 工具 | 理由 |
|------|------|------|
| 文件操作（删/移/复制/列出）含中文路径 | Python | `os`/`shutil` 原生 Unicode |
| 文件内容处理含中文 | Python | `open(encoding='utf-8')` 可靠 |
| 简单系统命令（磁盘空间等）无中文 | Bash/wmic | 无编码风险 |
| PowerShell 脚本含中文路径 | Python（不用 PS） | PS 通过 bash 启动时仍受编码影响 |

## 反模式警告

- ❌ "单引号 heredoc 应该能保护中文" → 不能，locale 层在引号处理之后
- ❌ "chcp 65001 切到 UTF-8 就行" → 不行，MSYS2 bash 不认 Windows code page
- ❌ "上次 heredoc 中文成功了" → 可能是路径恰好全是 ASCII 或纯巧合
- ❌ "Python 太重了，用 PowerShell 吧" → PS 通过 bash 启动时一样炸

---

## 与 powershell-safety.md 的关系

- `powershell-safety.md`：处理 PowerShell 的 `$_` 和变量展开问题（无中文时）
- **本规则**：处理 Windows 下的中文编码问题（跨所有脚本语言）

当两条规则冲突时（既涉及 `$_` 又涉及中文路径）：**用 Python**，两条规则的问题都绕过。
