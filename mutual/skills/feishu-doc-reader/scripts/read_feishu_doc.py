#!/usr/bin/env python3
"""飞书文档读取器 - 通过飞书 Open API 读取文档内容"""

import json
import os
import sys
import time
import argparse
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SKILL_DIR, "reference", "feishu_config.json")
TOKEN_CACHE = os.path.join(SKILL_DIR, "reference", ".token_cache.json")

BASE_URL = "https://open.feishu.cn/open-apis"


def load_config():
    """加载飞书凭证配置"""
    if not os.path.exists(CONFIG_PATH):
        print(f"ERROR: 配置文件不存在: {CONFIG_PATH}", file=sys.stderr)
        print("请创建配置文件，包含 app_id 和 app_secret", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_tenant_access_token():
    """获取 tenant_access_token（带缓存）"""
    # 检查缓存
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

    # 缓存 token
    cache = {"token": token, "expire_time": time.time() + expire - 300}
    os.makedirs(os.path.dirname(TOKEN_CACHE), exist_ok=True)
    with open(TOKEN_CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f)

    return token


def api_get(path, params=None):
    """GET 请求飞书 API"""
    token = get_tenant_access_token()
    url = f"{BASE_URL}{path}"
    if params:
        from urllib.parse import urlencode
        url += "?" + urlencode(params)

    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"ERROR: HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def read_docx(doc_token):
    """读取新版飞书文档（docx）"""
    # 获取文档元信息
    meta = api_get(f"/docx/v1/documents/{doc_token}")
    if meta.get("code") != 0:
        print(f"ERROR: 获取文档失败: {meta.get('msg')}", file=sys.stderr)
        return None

    doc_info = meta.get("data", {}).get("document", {})

    # 获取所有 blocks
    blocks = []
    page_token = None
    while True:
        params = {"document_id": doc_token, "page_size": 500}
        if page_token:
            params["page_token"] = page_token
        resp = api_get(f"/docx/v1/documents/{doc_token}/blocks", params)
        if resp.get("code") != 0:
            print(f"ERROR: 获取 blocks 失败: {resp.get('msg')}", file=sys.stderr)
            break
        items = resp.get("data", {}).get("items", [])
        blocks.extend(items)
        if not resp.get("data", {}).get("has_more"):
            break
        page_token = resp["data"].get("page_token")

    return {
        "document": doc_info,
        "blocks": blocks,
        "block_count": len(blocks)
    }


def read_doc_legacy(doc_token):
    """读取旧版飞书文档（doc）"""
    resp = api_get(f"/doc/v2/{doc_token}/raw_content")
    if resp.get("code") != 0:
        print(f"ERROR: 获取旧版文档失败: {resp.get('msg')}", file=sys.stderr)
        return None
    return resp.get("data", {})


def read_sheet(doc_token):
    """读取飞书电子表格"""
    # 获取表格元信息
    meta = api_get(f"/sheets/v3/spreadsheets/{doc_token}")
    if meta.get("code") != 0:
        print(f"ERROR: 获取表格失败: {meta.get('msg')}", file=sys.stderr)
        return None

    # 获取所有 sheet
    sheets_resp = api_get(f"/sheets/v3/spreadsheets/{doc_token}/sheets/query")
    sheets = sheets_resp.get("data", {}).get("sheets", [])

    result = {
        "spreadsheet": meta.get("data", {}).get("spreadsheet", {}),
        "sheets": []
    }

    for sheet in sheets[:5]:  # 最多读5个sheet
        sheet_id = sheet.get("sheet_id")
        if not sheet_id:
            continue
        # 读取数据（前100行）
        range_str = f"{sheet_id}!A1:Z100"
        data_resp = api_get(f"/sheets/v2/spreadsheets/{doc_token}/values/{range_str}")
        result["sheets"].append({
            "sheet_info": sheet,
            "data": data_resp.get("data", {})
        })

    return result


def extract_text(blocks):
    """从 blocks 中提取纯文本"""
    texts = []
    for block in blocks:
        block_type = block.get("block_type")
        # 文本类 block
        if block_type in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12):
            text_run = block.get("text", {})
            elements = text_run.get("elements", [])
            line = ""
            for elem in elements:
                if "text_run" in elem:
                    line += elem["text_run"].get("content", "")
                elif "mention_user" in elem:
                    line += f"@{elem['mention_user'].get('user_id', 'unknown')}"
            if line.strip():
                texts.append(line)
    return "\n".join(texts)


def main():
    parser = argparse.ArgumentParser(description="飞书文档读取器")
    parser.add_argument("--doc-token", required=True, help="文档 token（从 URL 获取）")
    parser.add_argument("--type", choices=["docx", "doc", "sheet", "auto"], default="auto",
                        help="文档类型（auto=自动检测）")
    parser.add_argument("--extract-text-only", action="store_true", help="只提取纯文本")
    parser.add_argument("--output", "-o", help="输出文件路径（默认 stdout）")
    args = parser.parse_args()

    doc_token = args.doc_token
    doc_type = args.type

    # 自动检测类型
    if doc_type == "auto":
        if doc_token.startswith("docx_") or doc_token.startswith("shtc_"):
            doc_type = "docx"
        elif doc_token.startswith("doc_"):
            doc_type = "doc"
        elif doc_token.startswith("sheet_"):
            doc_type = "sheet"
        else:
            doc_type = "docx"  # 默认尝试 docx

    print(f"读取文档: {doc_token} (类型: {doc_type})", file=sys.stderr)

    if doc_type == "docx":
        result = read_docx(doc_token)
    elif doc_type == "doc":
        result = read_doc_legacy(doc_token)
    elif doc_type == "sheet":
        result = read_sheet(doc_token)
    else:
        print(f"ERROR: 不支持的文档类型: {doc_type}", file=sys.stderr)
        sys.exit(1)

    if result is None:
        print("ERROR: 文档读取失败", file=sys.stderr)
        sys.exit(1)

    if args.extract_text_only and doc_type == "docx":
        text = extract_text(result.get("blocks", []))
        output = json.dumps({"text": text, "block_count": result.get("block_count", 0)}, ensure_ascii=False, indent=2)
    else:
        output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"结果已保存到: {args.output}", file=sys.stderr)
    else:
        print(output)

    print("SUCCESS", file=sys.stderr)


if __name__ == "__main__":
    main()
