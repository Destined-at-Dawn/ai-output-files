# 跨盘文件夹迁移：Junction 打法与 4 个技术坑

> 来源：Claude Code（牛马/mutual）2026-06-16 · C盘清理迁移实战
> 跨工具价值：robocopy/PowerShell 自动化、任何工具的脚本编码、Claude 多进程环境

## 任务

C盘紧张（剩45G），把 Ollama/剪映/夸克 等大文件夹迁到 F盘（空1.8T），程序无感知。

## 正确打法（已封装为 li-script 库脚本 migrate-folder-to-drive.ps1）

`copy(robocopy) → 校验(退出码+文件数/字节数) → 原地改名 → 建Junction → 删旧副本`

- 用 **Junction（`mklink /J` / `New-Item -ItemType Junction`）不用 symlink**：迁本地盘无需管理员/开发者模式，对程序完全透明。
- **改名→建链→删旧** 的顺序：建链失败可把改名的源秒回滚，绝不出现"既删了又没链接"的窗口。

## 4 个真实坑

### 坑1：robocopy 退出码 1/3 是「成功」
robocopy 0-7 全是成功（1=复制了文件，3=复制+有额外文件），>=8 才是错误。脚本直接 `& script.ps1` 后，robocopy 的 `$LASTEXITCODE` 会成为整脚本退出码 → 被 harness/CI 误判 failed。**脚本末尾必须按真实业务结果 `exit 0/1`**。

### 坑2：PS 5.1 + 中文Windows 读 UTF-8(无BOM) 脚本会解析崩
中文注释的 UTF-8 字节被按 GBK 误读，字节奇偶错位会**吃掉行尾换行符**，把下一行代码吞进注释 → "Catch block must be last"/"Unexpected token" 等诡异报错。**铁律：自动化脚本一律 ASCII**（英文注释 + ASCII 路径/字符串）。关联已有教训 `20260531_PowerShell中文路径静默失败` `20260606_Python脚本4个技术坑_编码`。

### 坑3：app「主程序关了」≠ 文件夹解锁
剪映靠后台 `JianyingProTray`/`VEDetector` 占着缓存目录；夸克网盘开着 **13 个 `quark_cloud_drive` 进程**（进程名带下划线，不是 QuarkCloudDrive）。**停进程要按 `Get-Process | Where Path -match` 排查真实占用者，别只猜主 exe 名**。

### 坑4：绝不能 `Stop-Process -Name Claude`
Claude Desktop（D:\WindowsApps\Claude...）和 Claude Code（我自己，Roaming\Claude\claude-code 与 .newmax\bin）**共用 `claude.exe` 进程名**。按名杀进程 = 连自己当前会话一起杀。涉及 Claude 数据迁移（如 vm_bundles 11.5G）只能让用户手动退出桌面版后迁，脚本 Procs 留空、不自动 kill。

## 校验铁律（AI工程方法论 · 异常数字五连审计）
别信脚本自报数字，**直接量 C/F 盘 Free 增减 + `Get-Item` 确认 LinkType=Junction**。本次发现 F 涨了 104G 但只迁了 18.7G，审计查出多出的 85G 是别的进程并发往 F 搬的（migrated-from-D/study 等），与本脚本无关——验证才能下诚实结论，否则会误报"我搬出了104G"。

## 成果
C盘释放 17.9G（45→63 free），4 个 junction 生效，app 透链可读。
