# Claude Code 认证问题修复指南

## 问题描述

每次启动 Claude Code 都需要重新登录，即使本地有有效的认证凭据。

## 根本原因

1. **启动时网络抖动**：Windows 开机时网络未就绪，导致 token 验证失败
2. **UI 状态不更新**：后台刷新成功后，UI 不知道，仍然显示登录页
3. **settings.json BOM 问题**：UTF-8 BOM 导致配置解析失败

## 已完成的修复

### 1. 移除 settings.json 的 BOM（已完成）

```bash
# 备份已创建：~/.claude/settings.json.bak.bom
# BOM 已移除，配置文件现在可以正常解析
```

### 2. 认证保活脚本（需要安装）

脚本位置：
```
E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs\auth-keepalive.py
```

**功能**：
- 每 30 分钟检查 token 状态
- token 即将过期时自动刷新
- 记录所有认证事件到日志文件
- 支持 Windows 任务计划程序定时运行

**安装步骤**：

#### 方式一：手动运行（测试用）

```bash
# 查看当前状态
python auth-keepalive.py --status

# 单次检查
python auth-keepalive.py

# 后台持续运行（Ctrl+C 退出）
python auth-keepalive.py --daemon
```

#### 方式二：安装到任务计划程序（推荐）

1. 以管理员身份打开 PowerShell 或 CMD

2. 运行安装命令：
```bash
python "E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs\auth-keepalive.py" --install
```

3. 这会生成两个文件：
   - `~/.newmax/auth-logs/claude-auth-keepalive.xml` - 任务定义
   - `~/.newmax/auth-logs/install-task.bat` - 安装脚本

4. 右键点击 `install-task.bat` -> **以管理员身份运行**

5. 安装成功后，任务会在：
   - 每次登录 Windows 时启动
   - 每 30 分钟检查一次 token 状态

#### 方式三：手动创建任务计划程序任务

如果自动安装失败，可以手动创建：

1. 打开"任务计划程序"（Win+R -> `taskschd.msc`）

2. 点击"创建基本任务"

3. 设置：
   - **名称**: `Claude-Auth-KeepAlive`
   - **描述**: `Claude Code 认证保活 - 定期刷新 token 防止登录失效`
   - **触发器**: 
     - "当我登录时"
     - "每天"，重复任务间隔 30 分钟
   - **操作**: "启动程序"
     - **程序**: `python`
     - **参数**: `"E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs\auth-keepalive.py"`
   - **完成**

4. 右键任务 -> 属性 -> 勾选"如果任务失败，按以下频率重新启动"

---

## 日志文件

所有认证事件都会记录到日志文件：

**位置**: `~/.newmax/auth-logs/`

**文件名格式**: `auth-YYYY-MM-DD.log`

**查看日志**:
```bash
# 查看今日日志
cat ~/.newmax/auth-logs/auth-$(date +%Y-%m-%d).log

# 实时监控日志
tail -f ~/.newmax/auth-logs/auth-$(date +%Y-%m-%d).log
```

**日志示例**:
```
2026-06-11 22:11:28,676 [INFO] [AUTH_EVENT] CHECK_START: 开始认证检查
2026-06-11 22:11:28,677 [INFO] [AUTH_EVENT] TOKEN_STATUS: 过期时间: 2026-06-12 04:10:12.359000, 剩余: 21524秒
2026-06-11 22:11:28,677 [INFO] [AUTH_EVENT] TOKEN_VALID: Token 仍然有效
```

---

## 验证修复

### 1. 验证 BOM 已移除

```bash
# 检查前 3 个字节（应该是 7b 0a 22，不是 ef bb bf）
xxd ~/.claude/settings.json | head -1
```

输出应该是：
```
00000000: 7b0a 2020 ...
```

不是：
```
00000000: efbb bf7b ...
```

### 2. 验证保活脚本运行

```bash
# 运行单次检查
python auth-keepalive.py

# 应该看到类似输出：
# 2026-06-11 22:11:28,676 [INFO] [AUTH_EVENT] CHECK_START: 开始认证检查
# 2026-06-11 22:11:28,677 [INFO] [AUTH_EVENT] TOKEN_STATUS: 过期时间: 2026-06-12 04:10:12.359000, 剩余: 21524秒
# 2026-06-11 22:11:28,677 [INFO] [AUTH_EVENT] TOKEN_VALID: Token 仍然有效
```

### 3. 验证任务计划程序任务（如果已安装）

```bash
# 查看任务状态
schtasks /query /tn "Claude-Auth-KeepAlive" /v

# 应该看到：
# - 状态: 就绪
# - 下次运行时间: [下次计划时间]
# - 触发器: 登录时; 每天 [时间] 重复每 30 分钟
```

---

## 故障排除

### 问题 1: 脚本运行失败

**错误**: `ModuleNotFoundError: No module named 'xxx'`

**解决**: 脚本只使用 Python 标准库，不需要安装任何依赖。如果仍然报错，请检查 Python 版本：
```bash
python --version
# 应该是 Python 3.6+
```

### 问题 2: 任务计划程序任务不运行

**检查**:
1. 任务计划程序中任务是否存在
2. 任务是否启用
3. 任务历史记录中是否有错误

**手动触发**:
```bash
schtasks /run /tn "Claude-Auth-KeepAlive"
```

### 问题 3: 日志文件没有生成

**检查**:
```bash
# 检查日志目录是否存在
ls -la ~/.newmax/auth-logs/

# 如果不存在，手动创建
mkdir -p ~/.newmax/auth-logs
```

### 问题 4: Token 刷新失败

**可能原因**:
- 网络问题
- Claude 服务端问题
- Refresh token 已失效

**检查**:
```bash
# 查看网络连接
ping api.anthropic.com

# 检查认证状态
claude auth status

# 如果需要重新登录
claude auth login
```

---

## 提交 Bug Report

我已经准备了详细的 bug report，可以提交给 Anthropic：

**文件位置**: `bug-report-auth-persistence.md`

**提交方式**:
1. GitHub Issues: https://github.com/anthropics/claude-code/issues
2. Anthropic Support: support@anthropic.com
3. Discord: Claude Code Discord server

**提交内容**:
- 问题描述
- 根本原因分析
- 复现步骤
- 修复建议
- 日志证据

---

## 技术细节

### 认证流程（正常情况）

```
1. Claude Code 启动
2. 读取 ~/.newmax/.credentials.json
3. 检查 accessToken 是否过期
4. 如果过期，使用 refreshToken 刷新
5. 刷新成功，更新 .credentials.json
6. 通知 UI 认证成功
7. 显示正常界面
```

### 问题流程（当前情况）

```
1. Claude Code 启动
2. 读取 ~/.newmax/.credentials.json
3. 检查 accessToken 是否过期
4. 如果过期，使用 refreshToken 刷新
5. 网络抖动或服务端问题，刷新失败
6. initialize() 返回 null
7. UI 显示登录页（错误！）
8. 后台重试刷新（成功）
9. 但不通知 UI（BUG！）
10. UI 永远停在登录页
```

### 修复后的流程（预期）

```
1. Claude Code 启动
2. 读取 ~/.newmax/.credentials.json
3. 检查 accessToken 是否过期
4. 如果过期，使用 refreshToken 刷新
5. 网络抖动或服务端问题，刷新失败
6. 返回缓存的 user（而不是 null）
7. UI 显示正常界面（带"刷新中"状态）
8. 后台重试刷新（成功）
9. 通知 UI 刷新成功
10. UI 更新为完全登录状态
```

---

## 相关文件

- **保活脚本**: `auth-keepalive.py`
- **Bug Report**: `bug-report-auth-persistence.md`
- **本指南**: `auth-fix-guide.md`
- **凭据文件**: `~/.newmax/.credentials.json`
- **配置文件**: `~/.claude/settings.json`
- **日志目录**: `~/.newmax/auth-logs/`

---

## 更新历史

- **2026-06-11**: 初始版本
  - 移除 settings.json BOM
  - 创建认证保活脚本
  - 编写 bug report
  - 编写本指南

---

## 反馈

如果问题仍未解决，请提供以下信息：

1. **Claude Code 版本**:
   ```bash
   claude --version
   ```

2. **认证状态**:
   ```bash
   claude auth status
   ```

3. **保活脚本状态**:
   ```bash
   python auth-keepalive.py --status
   ```

4. **日志文件**:
   ```bash
   cat ~/.newmax/auth-logs/auth-$(date +%Y-%m-%d).log
   ```

5. **配置文件前几行**:
   ```bash
   xxd ~/.claude/settings.json | head -3
   ```

---

*最后更新: 2026-06-11*
