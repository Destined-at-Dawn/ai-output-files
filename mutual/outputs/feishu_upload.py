#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发布飞书主文档：小黎的同辈互助计划"""

import requests
import json
import re
import time
import sys
import os

# Windows GBK 兼容
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# ======== 配置 ========
APP_ID = "cli_a95f68fe27389bd3"
APP_SECRET = "ATWmHpI8KePLpMoSmAxhBeX561ZHXyOt"
MD_FILE = r"E:\ai产出文件\牛马\mutual\mutual\feishu-主文档-小黎的同辈互助计划.md"
TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
CREATE_DOC_URL = "https://open.feishu.cn/open-apis/docx/v1/documents"

# ======== 辅助函数 ========

def t(elements):
    """创建文本块"""
    return {"block_type": 2, "text": {"elements": elements}}

def h(level, elements):
    """创建标题块 level 1-9"""
    key = f"heading{level}"
    return {"block_type": 2 + level, key: {"elements": elements}}

def b(elements):
    """创建无序列表"""
    return {"block_type": 12, "bullet": {"elements": elements}}

def o(elements):
    """创建有序列表"""
    return {"block_type": 13, "ordered": {"elements": elements}}

def code(lines):
    """创建代码块"""
    return {"block_type": 14, "code": {
        "elements": [{"text_run": {"content": "\n".join(lines)}}],
        "style": {"language": 1, "wrap": True}
    }}

def sep():
    """分隔线（用文本替，飞书 children API 不支持 divider 块类型）"""
    return t([{"text_run": {"content": "─" * 50}}])

def quote_block(elements):
    """引用块"""
    return {"block_type": 15, "quote": {"elements": elements}}

def bold_text(content, extra_styles=None):
    """创建加粗文本元素"""
    style = {"bold": True}
    if extra_styles:
        style.update(extra_styles)
    return {"text_run": {"content": content, "text_element_style": style}}

def normal(content):
    """普通文本"""
    return {"text_run": {"content": content}}

def italic(content):
    """斜体文本"""
    return {"text_run": {"content": content, "text_element_style": {"italic": True}}}

def code_text(content):
    """行内代码"""
    return {"text_run": {"content": content, "text_element_style": {"inline_code": True}}}

def link_text(text, url):
    """链接文本"""
    return {"text_run": {"content": text, "text_element_style": {"link": {"url": url}}}}

def parse_inline(text):
    """解析行内 Markdown 为 text_run 元素列表"""
    elements = []
    i = 0
    while i < len(text):
        # **粗体**
        if text[i:i+2] == "**" and i+2 < len(text):
            end = text.find("**", i+2)
            if end != -1:
                elements.append(bold_text(text[i+2:end]))
                i = end + 2
                continue
        # ~~删除线~~
        if text[i:i+2] == "~~" and i+2 < len(text):
            end = text.find("~~", i+2)
            if end != -1:
                elements.append({"text_run": {"content": text[i+2:end], "text_element_style": {"strikethrough": True}}})
                i = end + 2
                continue
        # *斜体*（单星号）
        if text[i] == "*" and (i == 0 or text[i-1] != "*"):
            end = text.find("*", i+1)
            if end != -1 and end > i+1:
                elements.append(italic(text[i+1:end]))
                i = end + 1
                continue
        # `行内代码`
        if text[i] == "`":
            end = text.find("`", i+1)
            if end != -1:
                elements.append(code_text(text[i+1:end]))
                i = end + 1
                continue
        # [链接](url)
        if text[i] == "[":
            end_b = text.find("](", i)
            if end_b != -1:
                end_p = text.find(")", end_b + 2)
                if end_p != -1:
                    elements.append(link_text(text[i+1:end_b], text[end_b+2:end_p]))
                    i = end_p + 1
                    continue
        elements.append(normal(text[i]))
        i += 1
    return elements

def strip_emoji_prefix(text):
    """提取行首 emoji 后的文本"""
    m = re.match(r"^([\U0001F300-\U0001F9FF☀-➿✀-➿︀-️‍⃣㊗㊙\U0001F000-\U0001F02F\U0001F0A0-\U0001F0FF\U0001F100-\U0001F64F\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF]+)\s+(.+)", text)
    if m:
        return m.group(1), m.group(2)
    return None, text

# ======== Markdown → Blocks ========

def md_to_blocks(md_text):
    lines = md_text.split("\n")
    blocks = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        # --- 分隔线 → 细线文本
        if line.strip() in ("---", "***"):
            blocks.append(sep())
            i += 1
            continue

        # 代码块 ```...```
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip() or "plain"
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1  # skip ```
            blocks.append(code(code_lines))
            continue

        # 标题 # - ######
        heading_match = re.match(r"^(#{1,6})\s+(.+)", line)
        if heading_match:
            level = min(len(heading_match.group(1)), 5)  # cap at h5
            text = heading_match.group(2)
            elements = parse_inline(text)
            blocks.append(h(level, elements))
            i += 1
            continue

        # 无序列表 - * +
        bullet_match = re.match(r"^(\s*)[-*+]\s+(.+)", line)
        if bullet_match:
            text = bullet_match.group(2)
            indent = len(bullet_match.group(1))
            elements = parse_inline(text)
            items = [elements]
            i += 1
            while i < len(lines):
                sub = re.match(r"^(\s*)[-*+]\s+(.+)", lines[i])
                if sub and len(sub.group(1)) == indent:
                    items.append(parse_inline(sub.group(2)))
                    i += 1
                else:
                    break
            for item in items:
                blocks.append(b(item))
            continue

        # 有序列表 1. 1)
        ordered_match = re.match(r"^(\s*)\d+[.)]\s+(.+)", line)
        if ordered_match:
            text = ordered_match.group(2)
            indent = len(ordered_match.group(1))
            elements = parse_inline(text)
            blocks.append(o(elements))
            i += 1
            while i < len(lines):
                sub = re.match(r"^(\s*)\d+[.)]\s+(.+)", lines[i])
                if sub and len(sub.group(1)) == indent:
                    blocks.append(o(parse_inline(sub.group(2))))
                    i += 1
                else:
                    break
            continue

        # 引用块 >
        quote_match = re.match(r"^>\s+(.+)", line)
        if quote_match:
            text = quote_match.group(1)
            quote_lines = [text]
            i += 1
            while i < len(lines) and re.match(r"^>\s+(.+)", lines[i]):
                quote_lines.append(re.match(r"^>\s+(.+)", lines[i]).group(1))
                i += 1
            elements = parse_inline(" ".join(quote_lines))
            blocks.append(quote_block(elements))
            continue

        # 表格 → 检测下一个非空行是否含 | 和 ---
        if "|" in line:
            next_non_empty = i + 1
            while next_non_empty < len(lines) and not lines[next_non_empty].strip():
                next_non_empty += 1
            if next_non_empty < len(lines) and "---" in lines[next_non_empty]:
                # 是表格
                header_row = line
                sep_row = lines[next_non_empty]
                data_rows = []
                j = next_non_empty + 1
                while j < len(lines) and "|" in lines[j] and lines[j].strip():
                    data_rows.append(lines[j])
                    j += 1
                # 格式化为代码块样式
                headers = [c.strip() for c in header_row.split("|") if c.strip()]
                result_lines = []
                result_lines.append(" | ".join(headers))
                result_lines.append(" | ".join("─" * max(len(h), 3) for h in headers))
                for row in data_rows:
                    cells = [c.strip() for c in row.split("|") if c.strip()]
                    result_lines.append(" | ".join(cells))
                blocks.append(code(result_lines))
                i = j
                continue

        # 普通文本
        elements = parse_inline(line)
        blocks.append(t(elements))
        i += 1

    return blocks

# ======== 发送块（带自动重试） ========

def send_blocks(blocks, batch_size=40):
    """分批发送块到飞书文档，自动处理限流"""
    total = 0
    retries = 0

    for start in range(0, len(blocks), batch_size):
        batch = blocks[start:start + batch_size]
        end = min(start + batch_size, len(blocks))

        for attempt in range(3):
            resp = requests.post(BLOCK_URL, headers=HEADERS,
                json={"children": batch}, timeout=30)

            if resp.status_code == 429:
                wait = 2 ** (attempt + 1)
                print(f"  ⏳ 限流，等待 {wait}s...")
                time.sleep(wait)
                continue

            result = resp.json()
            if result.get("code") == 0:
                total += len(batch)
                print(f"  ✅ 块 {start+1}-{end} 发送成功")
                break
            elif result.get("code") == 99991400:  # rate limit
                time.sleep(3)
                continue
            else:
                # 逐个发送找出问题块
                print(f"  ⚠️  批发送失败，逐个重试...")
                for idx, block in enumerate(batch):
                    for a2 in range(2):
                        r2 = requests.post(BLOCK_URL, headers=HEADERS,
                            json={"children": [block]}, timeout=15)
                        if r2.status_code == 429:
                            time.sleep(1)
                            continue
                        rj = r2.json()
                        if rj.get("code") == 0:
                            total += 1
                            break
                        else:
                            print(f"    块 {start+idx+1} 失败: {rj.get('msg','?')}")
                            print(f"    内容前200字: {json.dumps(block, ensure_ascii=False)[:200]}")
                            break
                    else:
                        print(f"    块 {start+idx+1} 最终失败")
                break
        else:
            print(f"  ❌ 块 {start+1}-{end} 重试3次后仍失败")

    return total

# ======== 主流程 ========

print("[1/4] 获取 Token...")
resp = requests.post(TOKEN_URL, json={"app_id": APP_ID, "app_secret": APP_SECRET})
token_data = resp.json()
if token_data.get("code") != 0:
    print(f"Token 失败: {token_data}")
    sys.exit(1)
TOKEN = token_data["tenant_access_token"]
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json; charset=utf-8"}
print("Token OK")

print("[2/4] 读取文档...")
with open(MD_FILE, "r", encoding="utf-8") as f:
    md_content = f.read()
print(f"读取完成 ({len(md_content)} 字符)")

print("[3/4] 创建飞书文档...")
resp = requests.post(CREATE_DOC_URL, headers=HEADERS,
    json={"title": "必须知道的信息差 - 小黎的同辈互助计划"})
doc_data = resp.json()
if doc_data.get("code") != 0:
    print(f"创建失败: {doc_data}")
    sys.exit(1)
DOC_ID = doc_data["data"]["document"]["document_id"]
DOC_URL = f"https://niumaai.feishu.cn/docx/{DOC_ID}"
print(f"文档已创建: {DOC_URL}")

BLOCK_URL = f"https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_ID}/blocks/{DOC_ID}/children"

print("[4/4] 转换并发送内容...")
blocks = md_to_blocks(md_content)
print(f"转换了 {len(blocks)} 个块")

sent = send_blocks(blocks)

print(f"\n======== 完成 ========")
print(f"已发送: {sent}/{len(blocks)} 个块")
print(f"文档链接: {DOC_URL}")
print(f"分享链接: https://niumaai.feishu.cn/docx/{DOC_ID}")

# 保存 ID
with open(r"E:\ai产出文件\牛马\mutual\mutual\outputs\feishu_doc_id.txt", "w", encoding="utf-8") as f:
    f.write(f"document_id: {DOC_ID}\nurl: {DOC_URL}\n")
