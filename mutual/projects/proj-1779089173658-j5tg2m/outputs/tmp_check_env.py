#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查微信解密环境"""
import os
import datetime

checks = [
    r'C:\Users\13975\AppData\Local\Temp\wechat-db-copy-20260607\wx_key_keys_interactive.json',
    r'C:\Users\13975\AppData\Local\Temp\wechat-decrypted-wxid_3nvidmluot0a22\message_0.db',
    r'E:\ai产出文件\牛马\创作\创作\output\databases\wxid_3nvidmluot0a22\message_0.db',
    r'D:\data\wechat\xwechat_files\wxid_3nvidmluot0a22_72ff\db_storage\message\message_0.db',
    r'E:\ai产出文件\牛马\创作\创作\tools\wx_key\v2.1.8',
]

for p in checks:
    exists = os.path.exists(p)
    if exists and os.path.isfile(p):
        s = os.path.getsize(p)
        m = datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%Y-%m-%d %H:%M:%S')
        print(f'[OK] {m} | {s/1024/1024:.1f}MB | {p}')
    elif exists and os.path.isdir(p):
        print(f'[OK] DIR | {p}')
    else:
        print(f'[MISSING] {p}')

# 也检查一下是否有 contact.db 解密版
contact_candidates = [
    r'C:\Users\13975\AppData\Local\Temp\wechat-decrypted-wxid_3nvidmluot0a22\contact.db',
    r'E:\ai产出文件\牛马\创作\创作\output\databases\wxid_3nvidmluot0a22\contact.db',
]
print()
for p in contact_candidates:
    if os.path.exists(p):
        s = os.path.getsize(p)
        m = datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%Y-%m-%d %H:%M:%S')
        print(f'[OK] contact.db | {m} | {s/1024/1024:.1f}MB | {p}')
    else:
        print(f'[MISSING] contact.db | {p}')
