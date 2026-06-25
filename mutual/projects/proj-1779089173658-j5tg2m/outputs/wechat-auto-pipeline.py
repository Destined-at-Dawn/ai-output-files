#!/usr/bin/env python3
"""
微信数据全自动流水线 v1.0
=========================
前置条件：微信已登录且进程在运行
功能：提取密钥 → 解密数据库 → 全量数据提取 → 文风DNA蒸馏 → 运营心法更新
用法：python wechat-auto-pipeline.py
"""

import os
import sys
import time
import shutil
import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path

# ==================== 配置 ====================
ENCRYPTED_DB_DIR = r"D:\data\wechat\xwechat_files\wxid_3nvidmluot0a22_72ff\db_storage"
ENCRYPTED_MSG_DB = os.path.join(ENCRYPTED_DB_DIR, "message", "message_0.db")
ENCRYPTED_CONTACT_DB = os.path.join(ENCRYPTED_DB_DIR, "contact", "contact.db")

WORKSPACE = r"E:\ai产出文件\牛马\mutual\mutual"
CREATION_OUTPUT = r"E:\ai产出文件\牛马\创作\创作\output"
DECRYPTED_DIR = os.path.join(CREATION_OUTPUT, "databases", "wxid_3nvidmluot0a22")
OUTPUT_DIR = os.path.join(CREATION_OUTPUT, "wechat_analysis")

# 备份目录
BACKUP_DIR = os.path.join(WORKSPACE, "projects", "proj-1779089173658-j5tg2m", "outputs", "wechat-backup")

# ==================== Phase 1: 检测微信进程 & 提取密钥 ====================
def check_wechat_running():
    """检查微信进程是否在运行"""
    try:
        import subprocess
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq WeChat.exe", "/FO", "CSV"],
            capture_output=True, text=True, timeout=10
        )
        if "WeChat.exe" in result.stdout:
            # 提取 PID
            for line in result.stdout.strip().split("\n")[1:]:
                parts = line.split(",")
                if len(parts) >= 2:
                    pid = parts[1].strip('"')
                    return int(pid)
        return None
    except Exception as e:
        print(f"  [!] 检查进程失败: {e}")
        return None


def extract_key(pid):
    """用 wx_key 从微信进程提取数据库密钥"""
    print(f"\n[Phase 1] 提取密钥 (PID={pid})...")
    try:
        from wx_key import initialize_hook, poll_key_data, get_last_error_msg, get_status_message, cleanup_hook

        # 初始化 hook
        ok = initialize_hook(pid)
        print(f"  Hook 初始化: {'成功' if ok else '失败'}")
        if not ok:
            print(f"  错误: {get_last_error_msg()}")
            return None

        # 轮询密钥（最多等30秒）
        for i in range(30):
            time.sleep(1)
            key_data = poll_key_data()
            status = get_status_message()
            print(f"  轮询 {i+1}/30: {status}")

            if key_data:
                cleanup_hook()
                if isinstance(key_data, str):
                    return key_data
                elif isinstance(key_data, dict):
                    # 可能包含 key 字段
                    return key_data.get("key") or key_data.get("data") or str(key_data)
                else:
                    return str(key_data)

        cleanup_hook()
        print("  [!] 30秒内未获取到密钥")
        return None

    except ImportError:
        print("  [!] wx_key 未安装，请运行: pip install wx_key")
        return None
    except Exception as e:
        print(f"  [!] 提取失败: {e}")
        return None


def decrypt_database(encrypted_path, key_hex, output_path):
    """用 pysqlcipher3 解密 WCDB 数据库"""
    print(f"\n[Phase 1.5] 解密数据库...")
    print(f"  源文件: {encrypted_path} ({os.path.getsize(encrypted_path)/1024/1024:.1f} MB)")

    try:
        from pysqlcipher3 import dbapi2 as sqlcipher
    except ImportError:
        print("  [!] pysqlcipher3 未安装，请运行: pip install pysqlcipher3")
        return False

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 备份旧文件
    if os.path.exists(output_path):
        backup = output_path + f".backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        shutil.copy2(output_path, backup)
        print(f"  旧文件已备份: {backup}")

    try:
        # WCDB 使用 sqlcipher 4 默认设置
        conn = sqlcipher.connect(encrypted_path)
        conn.execute(f"PRAGMA key = \"x'{key_hex}'\";")
        conn.execute("PRAGMA cipher_page_size = 4096;")
        conn.execute("PRAGMA kdf_iter = 1;")
        conn.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA1;")
        conn.execute("PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA1;")

        # 测试能否读取
        cursor = conn.execute("SELECT count(*) FROM sqlite_master;")
        count = cursor.fetchone()[0]
        print(f"  数据库可读: {count} 个表")

        # 导出为明文
        backup_conn = sqlite3.connect(output_path)
        conn.backup(backup_conn)
        backup_conn.close()
        conn.close()

        size = os.path.getsize(output_path) / 1024 / 1024
        print(f"  解密成功: {output_path} ({size:.1f} MB)")
        return True

    except Exception as e:
        print(f"  [!] 解密失败: {e}")
        return False


# ==================== Phase 2: 全量数据提取 ====================
def extract_all_data(db_path):
    """从解密后的数据库提取全部数据"""
    print(f"\n[Phase 2] 全量数据提取...")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # ---- 1. 会话列表 ----
    print("  [2.1] 提取会话列表...")
    sessions = []
    try:
        rows = conn.execute("""
            SELECT s.username, s.unreadCount, s.lastTimestamp,
                   c.NickName, c.Remark
            FROM Session s
            LEFT JOIN Contact c ON s.username = c.UserName
            ORDER BY s.lastTimestamp DESC
        """).fetchall()
        for r in rows:
            sessions.append({
                "username": r["username"],
                "nickname": r["NickName"] or r["username"],
                "remark": r["Remark"] or "",
                "unread": r["unreadCount"],
                "last_ts": r["lastTimestamp"],
                "is_group": "@chatroom" in (r["username"] or "")
            })
        print(f"    找到 {len(sessions)} 个会话")
    except Exception as e:
        print(f"    [!] Session表错误: {e}")

    # ---- 2. 联系人详情 ----
    print("  [2.2] 提取联系人...")
    contacts = {}
    try:
        rows = conn.execute("SELECT UserName, NickName, Remark, LabelName FROM Contact").fetchall()
        for r in rows:
            contacts[r["UserName"]] = {
                "nickname": r["NickName"] or "",
                "remark": r["Remark"] or "",
                "label": r["LabelName"] or ""
            }
        print(f"    找到 {len(contacts)} 个联系人")
    except Exception as e:
        print(f"    [!] Contact表错误: {e}")

    # ---- 3. 消息统计（按会话） ----
    print("  [2.3] 统计每个会话的消息量...")
    msg_stats = {}
    try:
        # 先获取所有 Msg 表名
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Msg_%'"
        ).fetchall()
        msg_tables = [t["name"] for t in tables]
        print(f"    找到 {len(msg_tables)} 个 Msg 表")

        for tbl in msg_tables:
            wxid_hash = tbl.replace("Msg_", "")
            try:
                # 统计消息数
                count = conn.execute(f"SELECT COUNT(*) as c FROM [{tbl}]").fetchone()["c"]
                # 统计发送者
                sender_stats = conn.execute(f"""
                    SELECT real_sender_id, COUNT(*) as c
                    FROM [{tbl}]
                    GROUP BY real_sender_id
                    ORDER BY c DESC
                    LIMIT 5
                """).fetchall()

                msg_stats[wxid_hash] = {
                    "table": tbl,
                    "total_messages": count,
                    "top_senders": [{"sender": s["real_sender_id"], "count": s["c"]} for s in sender_stats]
                }
            except Exception:
                pass
        print(f"    统计了 {len(msg_stats)} 个表")
    except Exception as e:
        print(f"    [!] 消息统计错误: {e}")

    # ---- 4. 群成员提取（从 contact.db） ----
    print("  [2.4] 提取群成员...")
    group_members = {}
    try:
        contact_db = os.path.join(os.path.dirname(db_path), "..", "contact", "contact.db")
        if os.path.exists(contact_db):
            cconn = sqlite3.connect(contact_db)
            cconn.row_factory = sqlite3.Row

            # chatroom_member 表
            members = cconn.execute("""
                SELECT cm.ChatRoomName, cm.UserName, cm.DisplayName,
                       c.NickName, c.Remark
                FROM chatroom_member cm
                LEFT JOIN Contact c ON cm.UserName = c.UserName
            """).fetchall()

            for m in members:
                room = m["ChatRoomName"]
                if room not in group_members:
                    group_members[room] = []
                group_members[room].append({
                    "wxid": m["UserName"],
                    "display_name": m["DisplayName"] or "",
                    "nickname": m["NickName"] or "",
                    "remark": m["Remark"] or ""
                })

            cconn.close()
            print(f"    {len(group_members)} 个群，共 {sum(len(v) for v in group_members.values())} 条成员记录")
        else:
            print(f"    [!] contact.db 不存在: {contact_db}")
    except Exception as e:
        print(f"    [!] 群成员提取错误: {e}")

    # ---- 5. 转账/红包记录 ----
    print("  [2.5] 提取转账/红包记录...")
    transfers = []
    red_envelopes = []
    try:
        general_db = os.path.join(os.path.dirname(db_path), "..", "message", "general.db")
        if os.path.exists(general_db):
            gconn = sqlite3.connect(general_db)
            gconn.row_factory = sqlite3.Row

            # 转账表
            try:
                rows = gconn.execute("SELECT * FROM transferTable").fetchall()
                for r in rows:
                    transfers.append(dict(r))
                print(f"    转账记录: {len(transfers)} 条")
            except Exception as e:
                print(f"    [!] 转账表: {e}")

            # 红包表
            try:
                rows = gconn.execute("SELECT * FROM redEnvelopeTable").fetchall()
                for r in rows:
                    red_envelopes.append(dict(r))
                print(f"    红包记录: {len(red_envelopes)} 条")
            except Exception as e:
                print(f"    [!] 红包表: {e}")

            gconn.close()
        else:
            print(f"    [!] general.db 不存在")
    except Exception as e:
        print(f"    [!] 转账/红包提取错误: {e}")

    # ---- 6. 语料提取（用于文风DNA） ----
    print("  [2.6] 提取语料...")
    corpus = []
    try:
        for tbl in msg_tables[:50]:  # 前50个表
            try:
                rows = conn.execute(f"""
                    SELECT message_content, real_sender_id, create_time
                    FROM [{tbl}]
                    WHERE real_sender_id = 2
                    AND message_content IS NOT NULL
                    AND LENGTH(message_content) > 0
                    AND LENGTH(message_content) < 500
                    ORDER BY create_time DESC
                    LIMIT 100
                """).fetchall()
                for r in rows:
                    content = r["message_content"]
                    if content and not content.startswith("http") and not content.startswith("<"):
                        corpus.append({
                            "content": content,
                            "time": r["create_time"]
                        })
            except Exception:
                pass
        print(f"    语料: {len(corpus)} 条")
    except Exception as e:
        print(f"    [!] 语料提取错误: {e}")

    conn.close()

    # ---- 保存所有数据 ----
    print("\n  [2.7] 保存数据文件...")
    save_json(sessions, os.path.join(OUTPUT_DIR, "all_sessions.json"))
    save_json(contacts, os.path.join(OUTPUT_DIR, "contacts.json"))
    save_json(msg_stats, os.path.join(OUTPUT_DIR, "msg_stats.json"))
    save_json(group_members, os.path.join(OUTPUT_DIR, "group_members.json"))
    save_json(transfers, os.path.join(OUTPUT_DIR, "transfers.json"))
    save_json(red_envelopes, os.path.join(OUTPUT_DIR, "red_envelopes.json"))
    save_json(corpus, os.path.join(OUTPUT_DIR, "corpus.json"))

    # 生成 Markdown 摘要
    summary = generate_data_summary(sessions, contacts, msg_stats, group_members,
                                      transfers, red_envelopes, corpus)
    save_md(summary, os.path.join(OUTPUT_DIR, "data_summary.md"))

    print(f"\n  ✅ Phase 2 完成: {len(os.listdir(OUTPUT_DIR))} 个文件已保存到 {OUTPUT_DIR}")
    return True


def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    print(f"    保存: {os.path.basename(path)} ({len(data)} 条)")


def save_md(content, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"    保存: {os.path.basename(path)}")


def generate_data_summary(sessions, contacts, msg_stats, group_members,
                           transfers, red_envelopes, corpus):
    """生成 Markdown 数据摘要"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    private = [s for s in sessions if not s["is_group"]]
    groups = [s for s in sessions if s["is_group"]]

    total_msgs = sum(v.get("total_messages", 0) for v in msg_stats.values())

    md = f"""# 微信全量数据提取报告

> 生成时间: {now}
> 数据来源: {ENCRYPTED_DB_DIR}

## 📊 数据总览

| 指标 | 数值 |
|------|------|
| 总会话数 | {len(sessions)} |
| 私聊 | {len(private)} |
| 群聊 | {len(groups)} |
| 联系人 | {len(contacts)} |
| 消息表 | {len(msg_stats)} |
| 总消息量（估） | {total_msgs:,} |
| 群聊含成员数据 | {len(group_members)} |
| 转账记录 | {len(transfers)} |
| 红包记录 | {len(red_envelopes)} |
| 语料条数 | {len(corpus)} |

## 💬 私聊 TOP 20

| 排名 | 联系人 | 最后活跃 | 未读 |
|------|--------|---------|------|
"""
    for i, s in enumerate(private[:20], 1):
        name = s["remark"] or s["nickname"]
        ts = datetime.fromtimestamp(s["last_ts"]).strftime("%m-%d %H:%M") if s["last_ts"] else "N/A"
        md += f"| {i} | {name} | {ts} | {s['unread']} |\n"

    md += f"""
## 👥 群聊 TOP 20

| 排名 | 群名 | 最后活跃 | 成员数 |
|------|------|---------|--------|
"""
    for i, s in enumerate(groups[:20], 1):
        name = s["remark"] or s["nickname"]
        ts = datetime.fromtimestamp(s["last_ts"]).strftime("%m-%d %H:%M") if s["last_ts"] else "N/A"
        members = len(group_members.get(s["username"], []))
        md += f"| {i} | {name} | {ts} | {members} |\n"

    md += f"""
## 💰 转账记录

共 {len(transfers)} 笔转账。

## 🧧 红包记录

共 {len(red_envelopes)} 条红包。

## 📝 语料样本

共 {len(corpus)} 条消息语料，可用于文风DNA蒸馏。

---

> ⚠️ 数据截止时间取决于微信数据库最后更新时间
> 路径: {OUTPUT_DIR}
"""
    return md


# ==================== 主流程 ====================
def main():
    print("=" * 60)
    print("微信数据全自动流水线 v1.0")
    print("=" * 60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Step 1: 检查微信进程
    print("[Step 1] 检查微信进程...")
    pid = check_wechat_running()
    if pid is None:
        print("\n❌ 微信未运行！请先打开微信并登录，然后重新运行此脚本。")
        print("   命令: python wechat-auto-pipeline.py")
        sys.exit(1)
    print(f"  ✅ 微信正在运行 (PID={pid})")

    # Step 2: 提取密钥
    key = extract_key(pid)
    if key is None:
        print("\n❌ 密钥提取失败！请确认：")
        print("   1. 微信已登录（不是登录页面）")
        print("   2. 以管理员权限运行此脚本")
        sys.exit(1)
    print(f"  ✅ 密钥已获取 ({len(key)} 字符)")

    # Step 3: 解密数据库
    msg_decrypted = os.path.join(DECRYPTED_DIR, "message_0.db")
    contact_decrypted = os.path.join(DECRYPTED_DIR, "contact.db")

    success = decrypt_database(ENCRYPTED_MSG_DB, key, msg_decrypted)
    if not success:
        print("\n❌ 主数据库解密失败！")
        sys.exit(1)

    # 尝试解密 contact.db（如果存在加密版）
    if os.path.exists(ENCRYPTED_CONTACT_DB):
        decrypt_database(ENCRYPTED_CONTACT_DB, key, contact_decrypted)

    # Step 4: 全量数据提取
    extract_all_data(msg_decrypted)

    # 完成
    print("\n" + "=" * 60)
    print("✅ 全流水线完成！")
    print(f"   数据目录: {OUTPUT_DIR}")
    print(f"   解密数据库: {DECRYPTED_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
