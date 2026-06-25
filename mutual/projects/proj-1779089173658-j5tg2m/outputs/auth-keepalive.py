#!/usr/bin/env python3
"""
Claude Code 认证保活脚本
解决"每次启动都要登录"的问题

功能：
1. 定期检查 token 过期时间
2. token 即将过期时自动刷新
3. 记录所有认证事件到日志文件
4. 支持 Windows 任务计划程序定时运行

用法：
  python auth-keepalive.py              # 单次检查
  python auth-keepalive.py --daemon     # 后台持续运行
  python auth-keepalive.py --install    # 安装到任务计划程序
  python auth-keepalive.py --status     # 查看当前状态
"""

import json
import os
import sys
import time
import logging
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# 配置
CREDENTIALS_PATH = Path.home() / ".newmax" / ".credentials.json"
LOG_DIR = Path.home() / ".newmax" / "auth-logs"
LOG_FILE = LOG_DIR / f"auth-{datetime.now().strftime('%Y-%m-%d')}.log"

# Token 刷新阈值（秒）
REFRESH_THRESHOLD = 3600  # 1 小时内过期则刷新
CHECK_INTERVAL = 1800     # 每 30 分钟检查一次

# 设置日志
def setup_logging():
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def load_credentials():
    """加载凭据文件"""
    try:
        if not CREDENTIALS_PATH.exists():
            logging.error(f"凭据文件不存在: {CREDENTIALS_PATH}")
            return None

        with open(CREDENTIALS_PATH, 'r', encoding='utf-8') as f:
            creds = json.load(f)

        return creds
    except json.JSONDecodeError as e:
        logging.error(f"凭据文件 JSON 解析失败: {e}")
        return None
    except Exception as e:
        logging.error(f"读取凭据文件失败: {e}")
        return None

def get_token_expiry(creds):
    """获取 token 过期时间"""
    try:
        if 'claudeAiOauth' in creds:
            expires_at = creds['claudeAiOauth'].get('expiresAt')
            if expires_at:
                # 转换毫秒时间戳为秒
                return datetime.fromtimestamp(expires_at / 1000)
        return None
    except Exception as e:
        logging.error(f"解析 token 过期时间失败: {e}")
        return None

def is_token_expiring_soon(expires_at, threshold=REFRESH_THRESHOLD):
    """检查 token 是否即将过期"""
    if expires_at is None:
        return True

    now = datetime.now()
    time_left = (expires_at - now).total_seconds()

    return time_left < threshold

def refresh_token():
    """刷新 token"""
    try:
        logging.info("尝试刷新 token...")

        # 使用 claude auth status 触发刷新
        result = subprocess.run(
            ['claude', 'auth', 'status'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            logging.info("Token 刷新成功")
            return True
        else:
            logging.warning(f"Token 刷新可能失败: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logging.error("Token 刷新超时")
        return False
    except Exception as e:
        logging.error(f"Token 刷新异常: {e}")
        return False

def log_auth_event(event_type, details):
    """记录认证事件"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"[AUTH_EVENT] {event_type}: {details}")

def check_auth_status():
    """检查认证状态"""
    try:
        result = subprocess.run(
            ['claude', 'auth', 'status'],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            status = json.loads(result.stdout)
            return status
        else:
            logging.warning(f"获取认证状态失败: {result.stderr}")
            return None
    except Exception as e:
        logging.error(f"检查认证状态异常: {e}")
        return None

def run_once():
    """单次检查"""
    setup_logging()

    log_auth_event("CHECK_START", "开始认证检查")

    # 加载凭据
    creds = load_credentials()
    if creds is None:
        log_auth_event("CHECK_FAILED", "无法加载凭据")
        return False

    # 获取过期时间
    expires_at = get_token_expiry(creds)
    if expires_at:
        time_left = (expires_at - datetime.now()).total_seconds()
        log_auth_event("TOKEN_STATUS", f"过期时间: {expires_at}, 剩余: {time_left:.0f}秒")

        # 检查是否需要刷新
        if is_token_expiring_soon(expires_at):
            log_auth_event("REFRESH_NEEDED", "Token 即将过期")

            if refresh_token():
                log_auth_event("REFRESH_SUCCESS", "Token 刷新成功")
                return True
            else:
                log_auth_event("REFRESH_FAILED", "Token 刷新失败")
                return False
        else:
            log_auth_event("TOKEN_VALID", "Token 仍然有效")
            return True
    else:
        log_auth_event("NO_EXPIRY", "无法获取过期时间，尝试刷新")
        return refresh_token()

def run_daemon():
    """后台持续运行"""
    setup_logging()

    log_auth_event("DAEMON_START", f"保活守护进程启动，检查间隔: {CHECK_INTERVAL}秒")

    while True:
        try:
            run_once()
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            log_auth_event("DAEMON_STOP", "守护进程被用户中断")
            break
        except Exception as e:
            log_auth_event("DAEMON_ERROR", f"守护进程异常: {e}")
            time.sleep(60)  # 出错后等 1 分钟再试

def install_task():
    """安装到 Windows 任务计划程序"""
    setup_logging()

    script_path = Path(__file__).absolute()

    # 创建 XML 任务定义
    task_xml = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Claude Code 认证保活 - 定期刷新 token 防止登录失效</Description>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
    <CalendarTrigger>
      <Repetition>
        <Interval>PT30M</Interval>
        <Duration>P1D</Duration>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
      <StartBoundary>2026-01-01T00:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>python</Command>
      <Arguments>"{script_path}"</Arguments>
    </Exec>
  </Actions>
</Task>"""

    # 写入 XML 文件
    xml_path = LOG_DIR / "claude-auth-keepalive.xml"
    xml_path.parent.mkdir(exist_ok=True)

    with open(xml_path, 'w', encoding='utf-16') as f:
        f.write(task_xml)

    # 创建批处理脚本
    bat_path = LOG_DIR / "install-task.bat"
    with open(bat_path, 'w', encoding='utf-8') as f:
        f.write(f"""@echo off
echo 正在安装 Claude Code 认证保活任务...
schtasks /create /tn "Claude-Auth-KeepAlive" /xml "{xml_path}" /f
if errorlevel 1 (
    echo 安装失败！请以管理员身份运行此脚本。
    pause
    exit /b 1
)
echo 安装成功！任务将在每次登录时启动，并每 30 分钟检查一次。
echo.
echo 任务详情：
schtasks /query /tn "Claude-Auth-KeepAlive" /v
pause
""")

    log_auth_event("INSTALL_READY", f"任务定义已生成: {xml_path}")
    print(f"\n任务定义已生成: {xml_path}")
    print(f"安装脚本已生成: {bat_path}")
    print("\n请右键点击 install-task.bat -> 以管理员身份运行")

    return True

def show_status():
    """显示当前状态"""
    setup_logging()

    print("=" * 60)
    print("Claude Code 认证状态")
    print("=" * 60)

    # 加载凭据
    creds = load_credentials()
    if creds is None:
        print("[ERROR] 无法加载凭据文件")
        return

    # 显示 token 信息
    if 'claudeAiOauth' in creds:
        oauth = creds['claudeAiOauth']
        expires_at = get_token_expiry(creds)

        print(f"\n[OAuth] OAuth 信息:")
        print(f"   订阅类型: {oauth.get('subscriptionType', 'N/A')}")
        print(f"   限制层级: {oauth.get('rateLimitTier', 'N/A')}")

        if expires_at:
            now = datetime.now()
            time_left = (expires_at - now).total_seconds()

            print(f"\n[Token] Token 状态:")
            print(f"   过期时间: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   剩余时间: {time_left / 3600:.1f} 小时")

            if time_left < 0:
                print(f"   状态: [EXPIRED] 已过期")
            elif time_left < REFRESH_THRESHOLD:
                print(f"   状态: [WARNING] 即将过期")
            else:
                print(f"   状态: [OK] 有效")

    # 检查认证状态
    print(f"\n[Auth] 认证状态:")
    status = check_auth_status()
    if status:
        print(f"   登录状态: {'[OK] 已登录' if status.get('loggedIn') else '[ERROR] 未登录'}")
        print(f"   认证方式: {status.get('authMethod', 'N/A')}")
        print(f"   API 提供商: {status.get('apiProvider', 'N/A')}")
    else:
        print(f"   [ERROR] 无法获取认证状态")

    # 显示日志文件
    print(f"\n[Log] 日志文件:")
    print(f"   目录: {LOG_DIR}")
    print(f"   今日日志: {LOG_FILE}")

    # 显示最近的日志
    if LOG_FILE.exists():
        print(f"\n[Recent] 最近日志 (最后 10 行):")
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[-10:]:
                print(f"   {line.rstrip()}")

    print("\n" + "=" * 60)

def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == '--daemon':
            run_daemon()
        elif cmd == '--install':
            install_task()
        elif cmd == '--status':
            show_status()
        elif cmd == '--help':
            print(__doc__)
        else:
            print(f"未知命令: {cmd}")
            print("使用 --help 查看帮助")
            sys.exit(1)
    else:
        # 默认单次检查
        success = run_once()
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
