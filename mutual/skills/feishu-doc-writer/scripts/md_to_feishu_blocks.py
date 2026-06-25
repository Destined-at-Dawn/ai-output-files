#!/usr/bin/env python3
"""
Markdown → 飞书 Block 转换器

将标准 Markdown 文本转换为飞书 Open API 的 block JSON 结构。
支持：标题(H1-H9)、段落、有序/无序列表、代码块、引用、分割线、表格、任务列表。

用法：
    python md_to_feishu_blocks.py input.md              # 输出到 stdout
    python md_to_feishu_blocks.py input.md -o blocks.json  # 输出到文件
    echo "# Hello" | python md_to_feishu_blocks.py -    # 从 stdin 读取
"""

import re
import json
import sys
import argparse
from urllib.parse import quote

# ============================================================
# 飞书 Block Type 常量
# ============================================================
TYPE_TEXT = 2
TYPE_H1 = 3
TYPE_H2 = 4
TYPE_H3 = 5
TYPE_H4 = 6
TYPE_H5 = 7
TYPE_H6 = 8
TYPE_H7 = 9
TYPE_H8 = 10
TYPE_H9 = 11
TYPE_BULLET = 12
TYPE_ORDERED = 13
TYPE_CODE = 14
TYPE_QUOTE = 15
TYPE_TABLE = 31
TYPE_TABLE_CELL = 32
TYPE_DIVIDER = 22

# 代码语言映射（飞书 language ID）
CODE_LANG_MAP = {
    "plaintext": 1, "text": 1, "plain": 1,
    "python": 49, "py": 49,
    "javascript": 41, "js": 41,
    "typescript": 65, "ts": 65,
    "java": 40,
    "c": 31, "cpp": 32, "c++": 32,
    "go": 36, "golang": 36,
    "rust": 54,
    "ruby": 53, "rb": 53,
    "php": 47,
    "swift": 58,
    "kotlin": 42,
    "shell": 56, "bash": 28, "sh": 56, "zsh": 56,
    "powershell": 48, "ps1": 48,
    "sql": 57,
    "json": 42,  # fallback
    "html": 38,
    "css": 33,
    "xml": 68,
    "yaml": 69, "yml": 69,
    "markdown": 44, "md": 44,
    "lua": 43,
    "r": 51,
    "scala": 55,
    "dart": 34,
    "elixir": 35,
    "haskell": 37,
    "perl": 46,
    "java": 40,
}

# ============================================================
# Inline 解析器
# ============================================================

def _style(**overrides):
    """
    构造完整的 text_element_style。
    飞书 API 要求所有 5 个布尔字段必须存在，缺失会导致 schema mismatch。
    """
    base = {
        "bold": False,
        "italic": False,
        "underline": False,
        "strikethrough": False,
        "inline_code": False,
    }
    base.update(overrides)
    return base


def _text_run(content, **style_overrides):
    """构造标准 text_run 元素"""
    return {"text_run": {"content": content, "text_element_style": _style(**style_overrides)}}


def _link_run(content, url):
    """构造带链接的 text_run 元素"""
    encoded_url = quote(url, safe='')
    s = _style()
    s["link"] = {"url": encoded_url}
    return {"text_run": {"content": content, "text_element_style": s}}


# 内联格式正则（按优先级排列）
INLINE_PATTERNS = [
    # 1. 转义字符
    (r'\\(.)', lambda m: _text_run(m.group(1))),
    # 2. 链接 [text](url) — 特殊处理
    (r'\[([^\]]+)\]\(([^)]+)\)', None),
    # 3. 加粗+斜体 ***text*** 或 ___text___
    (r'\*\*\*(.+?)\*\*\*', lambda m: _text_run(m.group(1), bold=True, italic=True)),
    (r'___(.+?)___', lambda m: _text_run(m.group(1), bold=True, italic=True)),
    # 4. 加粗 **text** 或 __text__
    (r'\*\*(.+?)\*\*', lambda m: _text_run(m.group(1), bold=True)),
    (r'__(.+?)__', lambda m: _text_run(m.group(1), bold=True)),
    # 5. 斜体 *text* 或 _text_
    (r'\*(.+?)\*', lambda m: _text_run(m.group(1), italic=True)),
    (r'(?<!\w)_(.+?)_(?!\w)', lambda m: _text_run(m.group(1), italic=True)),
    # 6. 删除线 ~~text~~
    (r'~~(.+?)~~', lambda m: _text_run(m.group(1), strikethrough=True)),
    # 7. 行内代码 `code`
    (r'`([^`]+)`', lambda m: _text_run(m.group(1), inline_code=True)),
    # 8. emoji 短码 :emoji:
    (r':([a-z_]+):', lambda m: _text_run(m.group(0))),
]


def parse_inline(text):
    """解析内联格式，返回飞书 text elements 列表"""
    if not text:
        return [_text_run("")]

    elements = []
    remaining = text

    while remaining:
        # 找最早匹配的内联格式
        earliest_pos = len(remaining)
        earliest_match = None
        earliest_type = None

        # 链接特殊处理
        link_pat = re.search(r'\[([^\]]+)\]\(([^)]+)\)', remaining)
        if link_pat and link_pat.start() < earliest_pos:
            earliest_pos = link_pat.start()
            earliest_match = link_pat
            earliest_type = "link"

        # 其他内联格式
        for pattern, handler in INLINE_PATTERNS:
            if handler is None:
                continue
            m = re.search(pattern, remaining)
            if m and m.start() < earliest_pos:
                earliest_pos = m.start()
                earliest_match = m
                earliest_type = "normal"

        if earliest_match is None:
            if remaining:
                elements.append(_text_run(remaining))
            break

        # 添加匹配前的纯文本
        if earliest_pos > 0:
            elements.append(_text_run(remaining[:earliest_pos]))

        if earliest_type == "link":
            link_text = earliest_match.group(1)
            link_url = earliest_match.group(2)
            elements.append(_link_run(link_text, link_url))
            remaining = remaining[earliest_match.end():]
        else:
            for pattern, handler in INLINE_PATTERNS:
                if handler is None:
                    continue
                m = re.match(pattern, remaining[earliest_pos:])
                if m:
                    elements.append(handler(m))
                    remaining = remaining[earliest_pos + m.end():]
                    break
            else:
                elements.append(_text_run(remaining[earliest_pos]))
                remaining = remaining[earliest_pos + 1:]

    return elements if elements else [_text_run("")]


# ============================================================
# Block 构造器
# ============================================================

def make_text_block(block_type, text, style=None):
    """构造文本类 block（段落/标题/列表/引用）"""
    key_map = {
        TYPE_TEXT: "text",
        TYPE_H1: "heading1", TYPE_H2: "heading2", TYPE_H3: "heading3",
        TYPE_H4: "heading4", TYPE_H5: "heading5", TYPE_H6: "heading6",
        TYPE_H7: "heading7", TYPE_H8: "heading8", TYPE_H9: "heading9",
        TYPE_BULLET: "bullet",
        TYPE_ORDERED: "ordered",
        TYPE_QUOTE: "quote",
    }
    key = key_map.get(block_type, "text")
    block_style = {"align": 1, "folded": False}
    if style:
        block_style.update(style)
    block = {
        "block_type": block_type,
        key: {
            "elements": parse_inline(text),
            "style": block_style,
        }
    }
    return block


def make_divider_block():
    return {"block_type": TYPE_DIVIDER, "divider": {}}


def make_code_block(code, language="plaintext"):
    """构造代码块"""
    lang_id = CODE_LANG_MAP.get(language.lower(), 1)
    return {
        "block_type": TYPE_CODE,
        "code": {
            "elements": [_text_run(code)],
            "style": {
                "language": lang_id,
                "wrap": False
            }
        }
    }


def make_table_block(headers, rows):
    """
    构造表格 block。
    注意：飞书表格需要先创建 table block，再通过子 block 填充单元格。
    这里只返回 table 结构定义，单元格内容通过后续 batch_update 写入。
    为简化，这里将表格转为文本 block 格式（markdown 表格转文本）。
    """
    # 飞书 table block 只定义行列数，单元格是子 block
    # 为兼容性，先输出为文本形式
    lines = []
    if headers:
        lines.append(" | ".join(headers))
        lines.append(" | ".join(["---"] * len(headers)))
    for row in rows:
        lines.append(" | ".join(row))
    text = "\n".join(lines)
    return make_text_block(TYPE_TEXT, text)


def make_table_block_native(headers, rows):
    """构造原生飞书表格 block（需要后续填充单元格）"""
    col_count = len(headers) if headers else 0
    row_count = 1 + len(rows) if headers else len(rows)
    return {
        "block_type": TYPE_TABLE,
        "table": {
            "property": {
                "row_size": row_count,
                "column_size": col_count,
            },
            "cells": []  # 需要后续填充
        }
    }


# ============================================================
# Markdown 解析器
# ============================================================

def parse_markdown(md_text):
    """
    将 Markdown 文本解析为飞书 block 列表。
    返回 (blocks, metadata)。
    """
    lines = md_text.split('\n')
    blocks = []
    i = 0
    metadata = {"title": None}

    while i < len(lines):
        line = lines[i]

        # ---- 空行 ----
        if not line.strip():
            i += 1
            continue

        # ---- YAML front matter ----
        if i == 0 and line.strip() == '---':
            i += 1
            while i < len(lines) and lines[i].strip() != '---':
                if lines[i].startswith('title:'):
                    metadata["title"] = lines[i].split(':', 1)[1].strip().strip('"\'')
                i += 1
            i += 1
            continue

        # ---- 分割线 ----
        if re.match(r'^(\s*[-*_]\s*){3,}\s*$', line):
            blocks.append(make_divider_block())
            i += 1
            continue

        # ---- 标题 ----
        heading_match = re.match(r'^(#{1,9})\s+(.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            heading_type = TYPE_H1 + level - 1  # H1=3, H2=4, ...
            blocks.append(make_text_block(heading_type, text))
            if level == 1 and metadata["title"] is None:
                metadata["title"] = text
            i += 1
            continue

        # ---- 代码块 ----
        if line.strip().startswith('```'):
            lang_match = re.match(r'^```(\w*)', line.strip())
            lang = lang_match.group(1) if lang_match and lang_match.group(1) else "plaintext"
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # 跳过结束 ```
            code_text = '\n'.join(code_lines)
            blocks.append(make_code_block(code_text, lang))
            continue

        # ---- 任务列表（转为 bullet + checkbox emoji）----
        todo_match = re.match(r'^(\s*)[-*]\s+\[([ xX])\]\s+(.+)$', line)
        if todo_match:
            done = todo_match.group(2).lower() == 'x'
            text = todo_match.group(3)
            checkbox = "[v]" if done else "[ ]"
            blocks.append(make_text_block(TYPE_BULLET, f"{checkbox} {text}"))
            i += 1
            continue

        # ---- 无序列表 ----
        bullet_match = re.match(r'^(\s*)[-*+]\s+(.+)$', line)
        if bullet_match:
            indent = len(bullet_match.group(1))
            text = bullet_match.group(2)
            blocks.append(make_text_block(TYPE_BULLET, text))
            i += 1
            continue

        # ---- 有序列表 ----
        ordered_match = re.match(r'^(\s*)\d+\.\s+(.+)$', line)
        if ordered_match:
            text = ordered_match.group(2)
            blocks.append(make_text_block(TYPE_ORDERED, text))
            i += 1
            continue

        # ---- 引用块 ----
        if line.strip().startswith('>'):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_text = re.sub(r'^\s*>+\s?', '', lines[i])
                quote_lines.append(quote_text)
                i += 1
            full_quote = '\n'.join(quote_lines)
            blocks.append(make_text_block(TYPE_QUOTE, full_quote))
            continue

        # ---- 表格 ----
        if '|' in line and i + 1 < len(lines) and re.match(r'^\s*\|?\s*[-:]+[-| :]*$', lines[i + 1]):
            # 解析表头
            headers = [cell.strip() for cell in line.strip().strip('|').split('|')]
            i += 2  # 跳过表头和分隔行
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                row = [cell.strip() for cell in lines[i].strip().strip('|').split('|')]
                rows.append(row)
                i += 1
            blocks.append(make_table_block(headers, rows))
            continue

        # ---- 普通段落 ----
        # 收集连续非空行作为一个段落
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not _is_block_start(lines[i]):
            para_lines.append(lines[i])
            i += 1
        para_text = ' '.join(para_lines)
        blocks.append(make_text_block(TYPE_TEXT, para_text))

    return blocks, metadata


def _is_block_start(line):
    """判断是否是新 block 的开始"""
    line = line.strip()
    if not line:
        return True
    if re.match(r'^#{1,9}\s', line):
        return True
    if line.startswith('```'):
        return True
    if re.match(r'^[-*+]\s', line):
        return True
    if re.match(r'^\d+\.\s', line):
        return True
    if line.startswith('>'):
        return True
    if re.match(r'^(\s*[-*_]\s*){3,}\s*$', line):
        return True
    if '|' in line:
        return True
    return False


# ============================================================
# 主入口
# ============================================================

def convert_md_to_blocks(md_text):
    """
    将 Markdown 转换为飞书 blocks。
    返回 {"blocks": [...], "title": "...", "block_count": N}
    """
    blocks, metadata = parse_markdown(md_text)
    return {
        "blocks": blocks,
        "title": metadata.get("title"),
        "block_count": len(blocks)
    }


def main():
    parser = argparse.ArgumentParser(description="Markdown → 飞书 Block 转换器")
    parser.add_argument("input", help="Markdown 文件路径，用 - 表示 stdin")
    parser.add_argument("-o", "--output", help="输出 JSON 文件路径（默认 stdout）")
    parser.add_argument("--title", help="覆盖文档标题")
    parser.add_argument("--compact", action="store_true", help="紧凑输出（不格式化 JSON）")
    args = parser.parse_args()

    # 读取输入
    if args.input == '-':
        md_text = sys.stdin.read()
    else:
        with open(args.input, 'r', encoding='utf-8') as f:
            md_text = f.read()

    # 转换
    result = convert_md_to_blocks(md_text)

    if args.title:
        result["title"] = args.title

    # 输出（确保 Windows 终端兼容 UTF-8）
    indent = None if args.compact else 2
    output = json.dumps(result, ensure_ascii=False, indent=indent)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"已转换 {result['block_count']} 个 block → {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
