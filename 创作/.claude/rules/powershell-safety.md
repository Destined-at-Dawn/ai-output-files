# PowerShell Execution Rules (CRITICAL)

## Problem
Bash shell interprets `$_` and `$.Property` BEFORE PowerShell sees them:
- `$_` → replaced with empty string or bash's last-arg
- `$_.Property` → the `.` triggers bash glob expansion
- No amount of quoting/escaping reliably fixes this

## Rule: NEVER use `$_` in inline `powershell -Command "..."`
This is a hard error. It will ALWAYS fail. There is no workaround for inline mode.

## Correct Patterns

### Pattern 1: Script file (preferred for anything complex)
```bash
# Write script to temp file, then execute
cat > /tmp/task.ps1 << 'PSEOF'
Get-ChildItem C:\some\path -Directory | ForEach-Object {
    $s = (Get-ChildItem $_.FullName -Recurse | Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{Name=$_.Name; SizeGB=[math]::Round($s/1GB,2)}
} | Format-Table -AutoSize
PSEOF
powershell -ExecutionPolicy Bypass -File /tmp/task.ps1
```
Key: The `'PSEOF'` (single-quoted) prevents bash from expanding any variables inside the heredoc.

### Pattern 2: Inline with escaped variables (simple one-liners only)
For commands that do NOT use `$_`, use:
```bash
powershell -Command "& { Get-PSDrive C | Select-Object Free, Used }"
```
If you MUST pass bash variables into PowerShell, use `-Command` with param syntax:
```powershell
powershell -Command "& { param(\$x) Write-Output \$x }" -x "hello"
```

### Pattern 3: Avoid PowerShell entirely
For disk space checks, use `df` or `wmic`:
```bash
wmic logicaldisk where "DeviceID='C:'" get FreeSpace,Size /format:value
```

## ⚠️ 中文路径编码铁律（2026-05-31 · ≥3次踩坑升级）

**根因**：PowerShell 在 Bash Shell（Git Bash / Claude Code）中执行时，中文路径默认编码为 GBK/CP936，但 Bash 环境默认 UTF-8。编码不匹配导致：
- `Test-Path` 返回 False（路径存在但编码不对，匹配失败）
- `Copy-Item` 静默失败（不报错但文件没复制）
- `ls` / `Get-ChildItem` 返回空（目录存在但读不到内容）
- **假阳性**：工具返回"成功"但文件实际没落盘

**铁律**：

| 场景 | 正确做法 | 禁止做法 |
|------|---------|---------|
| 涉及中文路径的文件操作 | **用 Python**（`os.path.exists`/`shutil.copy`） | PowerShell `Test-Path` / `Copy-Item` |
| 验证中文路径文件是否落盘 | **Python `os.path.exists()`** 或 **Read 工具直接读** | Bash `ls`（可能返回假结果） |
| 批量复制中文路径文件 | **Python `shutil.copytree()`** | PowerShell `Copy-Item -Recurse` |
| 创建中文目录 | **Python `os.makedirs()`** | PowerShell `New-Item -ItemType Directory` |

**Python 模板**（任何涉及中文路径的操作直接套用）：
```python
import os, shutil
src = r"E:\ai产出文件\牛马\xxx"
dst = r"E:\ai产出文件\牛马\yyy"
if os.path.exists(src):
    shutil.copytree(src, dst, dirs_exist_ok=True)
    print(f"OK: {os.path.exists(dst)}")
else:
    print(f"MISSING: {src}")
```

**自检信号**（任一触发 → 立即改用 Python）：
- [ ] PowerShell 命令涉及 `E:\ai产出文件\` 路径
- [ ] `Test-Path` 返回 False 但你确信文件存在
- [ ] `Copy-Item` 没报错但目标目录为空
- [ ] 需要同步到多个含中文路径的工作区

---

## Checklist before writing any PowerShell command
1. Does it use `$_`? → MUST use script file (Pattern 1)
2. Does it use `$variable` of any kind? → Prefer script file
3. Is it a simple one-liner without `$`? → Inline OK (Pattern 2)
4. Can I do it in pure bash/cmd instead? → Prefer that (Pattern 3)
5. **Does it involve Chinese paths (中文路径)?** → **MUST use Python, not PowerShell**
