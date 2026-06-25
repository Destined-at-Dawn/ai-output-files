# Script Safety Check（脚本安全检查 - 最高优先级）

## 铁律
**任何脚本在执行前，必须通过安全检查清单。没有例外。**

这条规则的诞生原因：2026-05-24 一个清理脚本差点删除 Windows 系统启动目录（C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup），被 UAC 拦截。根因是 Remove-Item 的路径指向了目录本身而非目录内的具体文件。

---

## 强制安全检查清单（每个脚本执行前必过）

### 1. 路径安全检查
- [ ] **禁止对以下路径执行删除/修改操作**：
  - `C:\Windows\*`
  - `C:\ProgramData\Microsoft\*`（除非精确到具体 .lnk/.exe 文件）
  - `C:\Program Files\*`、`C:\Program Files (x86)\*`
  - 任何系统环境变量目录（%SystemRoot%, %WinDir%）
  - 用户 AppData 中的系统级目录
- [ ] **删除操作必须精确到文件级别**，绝不能对目录级别执行 Remove-Item
- [ ] **路径必须以具体文件名结尾**（如 `xxx.lnk`），不能以目录结尾

### 2. 操作范围检查
- [ ] 脚本影响的文件数量是否合理？（>10 个文件必须先列出清单给用户确认）
- [ ] 是否有递归删除（`-Recurse`）？如果有，目标目录是否安全？
- [ ] 是否使用了通配符（`*`）？通配符 + 删除 = 极高风险，必须先 dry-run

### 3. Dry-Run 强制规则
**以下情况必须先 dry-run（只打印不执行）：**
- 删除超过 5 个文件
- 涉及系统目录
- 使用通配符
- 涉及注册表 HKLM 键
- 涉及防火墙/服务/驱动

Dry-run 方法：
```powershell
# PowerShell: 用 -WhatIf
Remove-Item $path -WhatIf

# 或者先只打印路径
Write-Output "WOULD DELETE: $path"
```

### 4. 不可逆操作确认
- [ ] 删除前是否已备份？（归档到 E:\ai产出文件\牛马\归档\）
- [ ] 注册表修改前是否已导出备份？
- [ ] 是否告知用户具体要删什么、为什么删？

### 5. 提权操作额外检查
当脚本需要管理员权限（UAC 弹窗）时：
- [ ] 为什么需要管理员权限？是否有非提权替代方案？
- [ ] 提权脚本的每一行都检查过安全性？
- [ ] 提权脚本是否最小化权限范围？（只做必须提权的那一步）

---

## 禁止模式（绝对不允许）

| 禁止操作 | 原因 |
|----------|------|
| `Remove-Item "C:\ProgramData\...\Startup"` | 删除系统启动目录 |
| `Remove-Item $dir` 其中 $dir 是目录路径 | 应该是 `$dir\具体文件.ext` |
| `Remove-Item * -Recurse` 在系统路径下 | 灾难性删除 |
| `reg delete HKLM\SOFTWARE\Microsoft` | 删除系统注册表根键 |
| 未经 dry-run 的批量删除 | 无法预知影响范围 |
| 拼接路径时不验证最终路径是否合理 | 路径拼接错误是最常见的事故源 |

---

## 正确模式

### 删除快捷方式的正确写法
```powershell
# ✅ 正确：精确到文件
$lnk = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\某应用.lnk"
if (Test-Path $lnk) {
    Remove-Item $lnk -Force
}

# ❌ 错误：指向目录
Remove-Item "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
```

### 批量清理的正确流程
```powershell
# Step 1: 收集目标（dry-run）
$targets = @()
Get-ChildItem "D:\某目录" -Filter "*.lnk" | ForEach-Object {
    # 验证是否失效
    $shell = New-Object -ComObject WScript.Shell
    $target = $shell.CreateShortcut($_.FullName).TargetPath
    if (-not (Test-Path $target)) {
        $targets += $_.FullName
        Write-Output "BROKEN: $($_.FullName) -> $target"
    }
}

# Step 2: 用户确认后才执行
# Step 3: 逐个删除并记录
```

---

## 事故响应
如果脚本已经造成损害：
1. 立即停止所有后续操作
2. 检查归档目录是否有备份
3. 检查 git history / 回收站
4. 坦诚告知用户发生了什么、影响范围、恢复方案
5. 记录到 memory/long-term.md 作为教训

---

## 执行顺序总结
```
写脚本 → 安全检查清单 → dry-run → 展示结果给用户 → 用户确认 → 执行 → 验证
```

**跳过任何一步 = 违规。没有"这次很简单不用检查"的例外。**
