# PowerShell Execution Rules (CRITICAL)

## Problem
Bash shell interprets `$_` and `$.Property` BEFORE PowerShell sees them:
- `$_` → replaced with empty string or bash's last-arg
- `$_.Property` → the `.` triggers bash glob expansion
- No amount of quoting/escaping reliably fixes this

## Rule: NEVER use `$_` in inline `powershell -Command "..."`
This is a hard error. It will ALWAYS fail. There is no workaround for inline mode.

## Correct Patterns

### Pattern 1: Script file (preferred for anything complex — BUT see Chinese path warning)
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

> ⚠️ **中文路径警告**：如果路径或内容包含中文字符，**禁止使用 heredoc**（单引号也不行，MSYS2 locale 层会破坏编码）。中文场景一律改用 Python 脚本。详见 `chinese-path-safety.md`。

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

## Checklist before writing any PowerShell command
1. Does it use `$_`? → MUST use script file (Pattern 1)
2. Does it use `$variable` of any kind? → Prefer script file
3. Is it a simple one-liner without `$`? → Inline OK (Pattern 2)
4. Can I do it in pure bash/cmd instead? → Prefer that (Pattern 3)
