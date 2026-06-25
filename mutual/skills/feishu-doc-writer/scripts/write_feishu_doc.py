#!/usr/bin/env python3
"""
飞书文档写入器 - 通过飞书 Open API 创建文档并写入内容

功能：
  1. 创建新的飞书文档
  2. 向已有文档追加 block 内容
  3. 支持从 Markdown 文件直接发布为飞书文档
  4. 支持在指定知识库(wiki)节点下创建文档

用法：
  # 创建新文档（从 Markdown）
  python write_feishu_doc.py create --title "我的文档" --from-md content.md

  # 创建新文档到指定文件夹
  python write_feishu_doc.py create --title "测试" --from-md content.md --folder-token xxxxx

  # 向已有文档追加内容
  python write_feishu_doc.py append --doc-token docx_xxx --from-md content.md

  # 创建到知识库（wiki space）
  python write_feishu_doc.py create --title "教程" --from-md content.md --wiki-space xxxxx
"""

import json
import os
import sys
import time
import argparse
import urllib.request
import urllib.error
from urllib.parse import quote

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
READER_SKILL_DIR = os.path.join(os.path.dirname(SKILL_DIR), "feishu-doc-reader")
CONFIG_PATH = os.path.join(READER_SKILL_DIR, "reference", "feishu_config.json")
TOKEN_CACHE = os.path.join(READER_SKILL_DIR, "reference", ".token_cache.json")

# 如果 reader 的配置不存在，尝试 writer 自己的
if not os.path.exists(CONFIG_PATH):
    CONFIG_PATH = os.path.join(SKILL_DIR, "reference", "feishu_config.json")
    TOKEN_CACHE = os.path.join(SKILL_DIR, "reference", ".token_cache.json")

BASE_URL = "https://open.feishu.cn/open-apis"

# ============================================================
# Auth（复用 reader 的 token 缓存机制）
# ============================================================

def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"ERROR: 配置文件不存在: {CONFIG_PATH}", file=sys.stderr)
        print("请在 feishu-doc-reader 或 feishu-doc-writer 的 reference/ 下创建 feishu_config.json", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_tenant_access_token():
    """获取 tenant_access_token（带缓存，兼容 reader 的缓存文件）"""
    if os.path.exists(TOKEN_CACHE):
        with open(TOKEN_CACHE, "r", encoding="utf-8") as f:
            cache = json.load(f)
        if cache.get("expire_time", 0) > time.time():
            return cache["token"]

    config = load_config()
    url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
    payload = json.dumps({
        "app_id": config["app_id"],
        "app_secret": config["app_secret"]
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"ERROR: 网络请求失败: {e}", file=sys.stderr)
        sys.exit(1)

    if data.get("code") != 0:
        print(f"ERROR: 获取 token 失败: {data.get('msg', 'unknown')}", file=sys.stderr)
        sys.exit(1)

    token = data["tenant_access_token"]
    expire = data.get("expire", 7200)
    cache = {"token": token, "expire_time": time.time() + expire - 300}
    os.makedirs(os.path.dirname(TOKEN_CACHE), exist_ok=True)
    with open(TOKEN_CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f)
    return token


# ============================================================
# API 请求
# ============================================================

def api_request(method, path, body=None, params=None):
    """通用飞书 API 请求"""
    token = get_tenant_access_token()
    url = f"{BASE_URL}{path}"
    if params:
        from urllib.parse import urlencode
        url += "?" + urlencode(params)

    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"ERROR: HTTP {e.code}: {err_body}", file=sys.stderr)
        return {"code": e.code, "msg": err_body}


def api_post(path, body, params=None):
    return api_request("POST", path, body, params)


def api_patch(path, body):
    return api_request("PATCH", path, body)


# ============================================================
# 飞书文档操作
# ============================================================

def create_document(title, folder_token=None):
    """
    创建新的飞书文档
    返回 {"document_id": "docx_xxx", "title": "...", "url": "..."}
    """
    body = {"title": title}
    if folder_token:
        body["folder_token"] = folder_token

    resp = api_post("/docx/v1/documents", body)
    if resp.get("code") != 0:
        print(f"ERROR: 创建文档失败: {resp.get('msg')}", file=sys.stderr)
        return None

    doc = resp.get("data", {}).get("document", {})
    doc_id = doc.get("document_id")

    # 生成文档 URL
    url = f"https://feishu.cn/docx/{doc_id}" if doc_id else None

    return {
        "document_id": doc_id,
        "title": doc.get("title", title),
        "url": url,
        "revision_id": doc.get("revision_id")
    }


def write_blocks(doc_id, blocks, parent_block_id=None):
    """
    向文档写入 block 列表。
    parent_block_id: 父 block ID，默认为 document_id（根级别）。
    飞书限制每次最多 50 个 block，超过自动分批。
    """
    if parent_block_id is None:
        parent_block_id = doc_id

    total = len(blocks)
    written = 0
    batch_size = 50  # 飞书 API 限制

    for batch_start in range(0, total, batch_size):
        batch = blocks[batch_start:batch_start + batch_size]
        body = {
            "children": batch,
            "index": -1  # -1 = 追加到末尾
        }

        resp = api_post(
            f"/docx/v1/documents/{doc_id}/blocks/{parent_block_id}/children",
            body
        )

        if resp.get("code") != 0:
            print(f"ERROR: 写入 block 失败 (batch {batch_start}): {resp.get('msg')}", file=sys.stderr)
            return written

        written += len(batch)

        # 限速：3 请求/秒
        if batch_start + batch_size < total:
            time.sleep(0.35)

    return written


def create_wiki_node(space_id, title, doc_type="docx"):
    """
    在知识库中创建节点（页面）
    返回 {"node_token": "...", "obj_token": "...", "obj_type": "docx"}
    """
    body = {
        "space_id": space_id,
        "node_type": "origin",
        "obj_type": doc_type,
        "title": title,
    }

    resp = api_post(f"/wiki/v2/spaces/{space_id}/nodes", body)
    if resp.get("code") != 0:
        print(f"ERROR: 创建 wiki 节点失败: {resp.get('msg')}", file=sys.stderr)
        return None

    node = resp.get("data", {}).get("node", {})
    return {
        "node_token": node.get("node_token"),
        "obj_token": node.get("obj_token"),  # 这就是 document_id
        "obj_type": node.get("obj_type"),
        "title": title,
        "url": f"https://feishu.cn/wiki/{node.get('node_token')}"
    }


# ============================================================
# 主流程：从 Markdown 创建飞书文档
# ============================================================

def publish_from_markdown(md_path, title=None, folder_token=None, wiki_space=None):
    """
    完整流程：Markdown → 飞书文档
    返回文档信息 dict
    """
    # 1. 导入转换器
    sys.path.insert(0, SCRIPT_DIR)
    from md_to_feishu_blocks import convert_md_to_blocks

    # 2. 读取并转换 Markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    result = convert_md_to_blocks(md_text)
    blocks = result["blocks"]
    doc_title = title or result.get("title") or os.path.splitext(os.path.basename(md_path))[0]

    print(f"转换完成: {len(blocks)} 个 block, 标题: {doc_title}", file=sys.stderr)

    if not blocks:
        print("ERROR: 没有可写入的内容", file=sys.stderr)
        return None

    # 3. 创建文档
    doc_info = None

    if wiki_space:
        # 创建到知识库
        print(f"创建 wiki 节点: space={wiki_space}", file=sys.stderr)
        node_info = create_wiki_node(wiki_space, doc_title)
        if node_info:
            doc_id = node_info["obj_token"]
            doc_info = {
                "document_id": doc_id,
                "title": doc_title,
                "url": node_info["url"],
                "node_token": node_info["node_token"],
                "location": "wiki"
            }
        else:
            return None
    else:
        # 创建到普通文件夹
        print(f"创建文档: title={doc_title}, folder={folder_token or 'root'}", file=sys.stderr)
        doc_info = create_document(doc_title, folder_token)
        if not doc_info:
            return None
        doc_info["location"] = "folder"

    doc_id = doc_info["document_id"]

    # 4. 写入 blocks
    written = write_blocks(doc_id, blocks)
    doc_info["blocks_written"] = written
    doc_info["blocks_total"] = len(blocks)

    if written == len(blocks):
        print(f"SUCCESS: {written}/{len(blocks)} blocks 已写入", file=sys.stderr)
    else:
        print(f"PARTIAL: {written}/{len(blocks)} blocks 已写入", file=sys.stderr)

    return doc_info


def append_to_document(doc_id, md_path):
    """向已有文档追加 Markdown 内容"""
    sys.path.insert(0, SCRIPT_DIR)
    from md_to_feishu_blocks import convert_md_to_blocks

    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    result = convert_md_to_blocks(md_text)
    blocks = result["blocks"]

    print(f"追加: {len(blocks)} 个 block → {doc_id}", file=sys.stderr)
    written = write_blocks(doc_id, blocks)

    return {
        "document_id": doc_id,
        "blocks_written": written,
        "blocks_total": len(blocks)
    }


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="飞书文档写入器")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # create 子命令
    create_p = subparsers.add_parser("create", help="创建新文档")
    create_p.add_argument("--title", required=True, help="文档标题")
    create_p.add_argument("--from-md", required=True, help="Markdown 文件路径")
    create_p.add_argument("--folder-token", help="目标文件夹 token")
    create_p.add_argument("--wiki-space", help="知识库 space ID（创建到知识库）")
    create_p.add_argument("-o", "--output", help="输出结果到 JSON 文件")

    # append 子命令
    append_p = subparsers.add_parser("append", help="向已有文档追加内容")
    append_p.add_argument("--doc-token", required=True, help="目标文档 ID")
    append_p.add_argument("--from-md", required=True, help="Markdown 文件路径")
    append_p.add_argument("-o", "--output", help="输出结果到 JSON 文件")

    args = parser.parse_args()

    if args.command == "create":
        result = publish_from_markdown(
            args.from_md,
            title=args.title,
            folder_token=args.folder_token,
            wiki_space=args.wiki_space
        )
    elif args.command == "append":
        result = append_to_document(args.doc_token, args.from_md)
    else:
        parser.print_help()
        sys.exit(1)

    if result is None:
        print("FAILED", file=sys.stderr)
        sys.exit(1)

    # 输出结果
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if hasattr(args, 'output') and args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"结果已保存: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
