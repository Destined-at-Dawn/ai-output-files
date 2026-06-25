#!/usr/bin/env python3
"""飞书文档 Blocks 结构读取器 - 获取完整文档树"""

import json
import os
import sys
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from read_feishu_doc import api_get, get_tenant_access_token


def get_all_blocks(doc_token):
    """分页获取文档所有 blocks"""
    blocks = []
    page_token = None
    while True:
        params = {"document_id": doc_token, "page_size": 500}
        if page_token:
            params["page_token"] = page_token
        resp = api_get(f"/docx/v1/documents/{doc_token}/blocks", params)
        if resp.get("code") != 0:
            print(f"ERROR: {resp.get('msg')}", file=sys.stderr)
            break
        items = resp.get("data", {}).get("items", [])
        blocks.extend(items)
        if not resp.get("data", {}).get("has_more"):
            break
        page_token = resp["data"].get("page_token")
    return blocks


def get_block_children(doc_token, block_id):
    """获取指定 block 的子 block"""
    children = []
    page_token = None
    while True:
        params = {"document_id": doc_token, "page_size": 500}
        if page_token:
            params["page_token"] = page_token
        resp = api_get(f"/docx/v1/documents/{doc_token}/blocks/{block_id}/children", params)
        if resp.get("code") != 0:
            print(f"ERROR: {resp.get('msg')}", file=sys.stderr)
            break
        items = resp.get("data", {}).get("items", [])
        children.extend(items)
        if not resp.get("data", {}).get("has_more"):
            break
        page_token = resp["data"].get("page_token")
    return children


def build_block_tree(blocks):
    """将扁平 blocks 列表构建为树结构"""
    block_map = {}
    for b in blocks:
        block_map[b["block_id"]] = {**b, "children": []}

    root_blocks = []
    for b in blocks:
        parent_id = b.get("parent_id")
        if parent_id and parent_id in block_map:
            block_map[parent_id]["children"].append(block_map[b["block_id"]])
        else:
            root_blocks.append(block_map[b["block_id"]])

    return root_blocks


BLOCK_TYPE_NAMES = {
    1: "page", 2: "text", 3: "heading1", 4: "heading2", 5: "heading3",
    6: "heading4", 7: "heading5", 8: "heading6", 9: "heading7",
    10: "heading8", 11: "heading9", 12: "bullet", 13: "ordered",
    14: "code", 15: "quote", 16: "todo", 17: "bitable",
    18: "callout", 19: "chat_card", 20: "diagram", 21: "divider",
    22: "file", 23: "grid", 24: "grid_column", 25: "iframe",
    26: "image", 27: "isv", 28: "mindnote", 29: "sheet",
    30: "table", 31: "table_cell", 32: "view", 33: "quote_container",
    34: "task", 35: "okr", 36: "okr_objective", 37: "okr_key_result",
    38: "okr_progress", 39: "add_ons", 40: "jira_issue",
    41: "wiki_catalog", 42: "board", 43: "agenda", 44: "agenda_item",
    45: "agenda_item_title", 46: "link_preview"
}


def block_to_text(block, indent=0):
    """将单个 block 转为可读文本"""
    block_type = block.get("block_type", 0)
    type_name = BLOCK_TYPE_NAMES.get(block_type, f"type_{block_type}")
    prefix = "  " * indent

    text_content = ""
    text_data = block.get("text", {})
    elements = text_data.get("elements", [])
    parts = []
    for elem in elements:
        if "text_run" in elem:
            parts.append(elem["text_run"].get("content", ""))
        elif "mention_doc" in elem:
            parts.append(f"[doc:{elem['mention_doc'].get('token', '?')}]")
        elif "equation" in elem:
            parts.append(f"${elem['equation'].get('content', '')}$")
    text_content = "".join(parts)

    if type_name == "heading1":
        return f"{prefix}# {text_content}"
    elif type_name == "heading2":
        return f"{prefix}## {text_content}"
    elif type_name == "heading3":
        return f"{prefix}### {text_content}"
    elif type_name == "bullet":
        return f"{prefix}- {text_content}"
    elif type_name == "ordered":
        return f"{prefix}1. {text_content}"
    elif type_name == "code":
        lang = block.get("code", {}).get("language", "")
        return f"{prefix}```{lang}\n{prefix}{text_content}\n{prefix}```"
    elif type_name == "quote":
        return f"{prefix}> {text_content}"
    elif type_name == "divider":
        return f"{prefix}---"
    elif type_name == "todo":
        done = block.get("todo", {}).get("done", False)
        mark = "x" if done else " "
        return f"{prefix}- [{mark}] {text_content}"
    elif type_name == "image":
        token = block.get("image", {}).get("token", "")
        return f"{prefix}![image]({token})"
    elif type_name == "table":
        return f"{prefix}[TABLE {block.get('table', {}).get('property', {}).get('row_size', '?')}x{block.get('table', {}).get('property', {}).get('column_size', '?')}]"
    elif text_content:
        return f"{prefix}{text_content}"
    else:
        return f"{prefix}[{type_name}]"


def tree_to_markdown(blocks, indent=0):
    """将 block 树转为 Markdown"""
    lines = []
    for block in blocks:
        text = block_to_text(block, indent)
        if text.strip():
            lines.append(text)
        children = block.get("children", [])
        if children:
            child_lines = tree_to_markdown(children, indent + 1)
            lines.extend(child_lines)
    return lines


def main():
    parser = argparse.ArgumentParser(description="飞书文档 Blocks 结构读取器")
    parser.add_argument("--doc-token", required=True, help="文档 token")
    parser.add_argument("--block-id", help="获取指定 block 的子 block")
    parser.add_argument("--include-children", action="store_true", help="包含子 block")
    parser.add_argument("--as-markdown", action="store_true", help="输出 Markdown 格式")
    parser.add_argument("--output", "-o", help="输出文件路径")
    args = parser.parse_args()

    print(f"读取文档 blocks: {args.doc_token}", file=sys.stderr)
    get_tenant_access_token()  # 确保 token 有效

    if args.block_id:
        blocks = get_block_children(args.doc_token, args.block_id)
        result = {
            "parent_block_id": args.block_id,
            "children": blocks,
            "count": len(blocks)
        }
    else:
        blocks = get_all_blocks(args.doc_token)
        if args.include_children or args.as_markdown:
            tree = build_block_tree(blocks)
            if args.as_markdown:
                md_lines = tree_to_markdown(tree)
                output = "\n".join(md_lines)
                if args.output:
                    with open(args.output, "w", encoding="utf-8") as f:
                        f.write(output)
                    print(f"Markdown 已保存到: {args.output}", file=sys.stderr)
                else:
                    print(output)
                print(f"SUCCESS: {len(blocks)} blocks -> Markdown", file=sys.stderr)
                return
            result = {
                "document_id": args.doc_token,
                "blocks": tree,
                "block_count": len(blocks)
            }
        else:
            result = {
                "document_id": args.doc_token,
                "blocks": blocks,
                "block_count": len(blocks)
            }

    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"结果已保存到: {args.output}", file=sys.stderr)
    else:
        print(output)

    print(f"SUCCESS: {len(blocks)} blocks", file=sys.stderr)


if __name__ == "__main__":
    main()
