#!/usr/bin/env python3
"""飞书 Wiki 节点读取器 - 先通过 wiki API 获取实际文档 token，再读取内容"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SKILL_DIR, "reference", "feishu_config.json")
TOKEN_CACHE = os.path.join(SKILL_DIR, "reference", ".token_cache.json")

BASE_URL = "https://open.feishu.cn/open-apis"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"ERROR: 配置文件不存在: {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_tenant_access_token():
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


def api_get(path, params=None):
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
        return {"code": e.code, "msg": body}


def get_wiki_node(wiki_token):
    """通过 wiki token 获取节点信息（含实际文档 token）"""
    resp = api_get("/wiki/v2/spaces/get_node", {"token": wiki_token})
    return resp


def read_docx(doc_token):
    """读取 docx 文档内容"""
    meta = api_get(f"/docx/v1/documents/{doc_token}")
    if meta.get("code") != 0:
        return None, meta.get("msg", "unknown error")

    doc_info = meta.get("data", {}).get("document", {})

    blocks = []
    page_token = None
    while True:
        params = {"document_id": doc_token, "page_size": 500}
        if page_token:
            params["page_token"] = page_token
        resp = api_get(f"/docx/v1/documents/{doc_token}/blocks", params)
        if resp.get("code") != 0:
            break
        items = resp.get("data", {}).get("items", [])
        blocks.extend(items)
        if not resp.get("data", {}).get("has_more"):
            break
        page_token = resp["data"].get("page_token")

    return {"document": doc_info, "blocks": blocks, "block_count": len(blocks)}, None


def extract_text(blocks):
    """从 blocks 提取纯文本"""
    texts = []
    for block in blocks:
        block_type = block.get("block_type")
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


def process_url(url):
    """处理单个飞书 URL，返回 {url, type, token, title, text, error}"""
    result = {"url": url, "type": None, "token": None, "title": None, "text": None, "error": None}

    # 解析 URL
    if "/docx/" in url:
        result["type"] = "docx"
        result["token"] = url.split("/docx/")[-1].split("?")[0].split("/")[0]
    elif "/wiki/" in url:
        result["type"] = "wiki"
        result["token"] = url.split("/wiki/")[-1].split("?")[0].split("/")[0]
    elif "/doc/" in url:
        result["type"] = "doc"
        result["token"] = url.split("/doc/")[-1].split("?")[0].split("/")[0]
    elif "/sheets/" in url:
        result["type"] = "sheet"
        result["token"] = url.split("/sheets/")[-1].split("?")[0].split("/")[0]
    else:
        result["error"] = f"无法解析 URL 类型: {url}"
        return result

    print(f"  [{result['type']}] {result['token']}", file=sys.stderr)

    # Wiki: 先获取节点信息
    if result["type"] == "wiki":
        node_resp = get_wiki_node(result["token"])
        if node_resp.get("code") != 0:
            result["error"] = f"Wiki 节点获取失败: code={node_resp.get('code')}, msg={node_resp.get('msg', '')[:200]}"
            return result

        node = node_resp.get("data", {}).get("node", {})
        obj_type = node.get("obj_type", "")
        obj_token = node.get("obj_token", "")
        result["title"] = node.get("title", "")
        print(f"    → wiki 节点: type={obj_type}, obj_token={obj_token}, title={result['title']}", file=sys.stderr)

        if obj_type == "docx":
            result["type"] = "docx"
            result["token"] = obj_token
        elif obj_type == "doc":
            result["type"] = "doc"
            result["token"] = obj_token
        elif obj_type == "sheet":
            result["type"] = "sheet"
            result["token"] = obj_token
        else:
            result["error"] = f"不支持的 wiki 节点类型: {obj_type}"
            return result

    # 读取文档内容
    if result["type"] == "docx":
        doc_data, err = read_docx(result["token"])
        if err:
            result["error"] = err
            return result
        if not result["title"]:
            result["title"] = doc_data.get("document", {}).get("title", "")
        result["text"] = extract_text(doc_data.get("blocks", []))
    elif result["type"] == "doc":
        resp = api_get(f"/doc/v2/{result['token']}/raw_content")
        if resp.get("code") != 0:
            result["error"] = f"旧版文档读取失败: {resp.get('msg')}"
            return result
        result["text"] = resp.get("data", {}).get("content", "")
    elif result["type"] == "sheet":
        result["error"] = "电子表格暂不支持批量文本提取"
    else:
        result["error"] = f"不支持的类型: {result['type']}"

    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="飞书 Wiki/Docx 批量读取器")
    parser.add_argument("--urls-file", required=True, help="包含 URL 列表的文件（每行一个）")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    args = parser.parse_args()

    # 读取 URL 列表
    with open(args.urls_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    print(f"共 {len(urls)} 个文档待处理", file=sys.stderr)
    os.makedirs(args.output_dir, exist_ok=True)

    results = []
    success = 0
    fail = 0

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] 处理: {url}", file=sys.stderr)
        result = process_url(url)

        if result["error"]:
            print(f"  ❌ 失败: {result['error'][:100]}", file=sys.stderr)
            fail += 1
        else:
            print(f"  ✅ 成功: {result['title'] or '(无标题)'} ({len(result.get('text', ''))} 字)", file=sys.stderr)
            success += 1
            # 保存单个文档
            safe_name = (result["title"] or result["token"] or f"doc_{i}").replace("/", "_").replace("\\", "_")[:50]
            out_path = os.path.join(args.output_dir, f"{i:02d}_{safe_name}.txt")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(f"# {result['title'] or '(无标题)'}\n")
                f.write(f"# 来源: {result['url']}\n")
                f.write(f"# 类型: {result['type']}\n\n")
                f.write(result.get("text", ""))

        results.append({
            "index": i,
            "url": result["url"],
            "type": result["type"],
            "title": result["title"],
            "text_length": len(result.get("text", "")),
            "error": result["error"]
        })

        # 小延迟防限流
        if i < len(urls):
            time.sleep(0.5)

    # 写汇总报告
    report_path = os.path.join(args.output_dir, "_fetch_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "total": len(urls),
            "success": success,
            "fail": fail,
            "results": results
        }, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}", file=sys.stderr)
    print(f"完成: {success} 成功 / {fail} 失败 / {len(urls)} 总计", file=sys.stderr)
    print(f"报告: {report_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
