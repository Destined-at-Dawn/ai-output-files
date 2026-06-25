from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


URLS = [
    "https://mp.weixin.qq.com/s/rEf-8brdDx3ryY9SEucQwQ",
    "https://mp.weixin.qq.com/s/XlssT9sxabS-n3ZcuyaEsA",
    "https://mp.weixin.qq.com/s/4DepUwNns5AuerHKS1voBg",
    "https://mp.weixin.qq.com/s/jU0HPIjU9dTiQJZn819Uuw",
    "https://mp.weixin.qq.com/s/4DepUwNns5AuerHKS1voBg",
    "https://mp.weixin.qq.com/s/U-0UWD7XvcOqWLfSXQ1FHQ",
    "https://mp.weixin.qq.com/s/OYxfr8uoPc8YkvqBq82aww",
    "https://mp.weixin.qq.com/s/AOBJ94eCbE7p2tBYgrUg9w",
    "https://mp.weixin.qq.com/s/HpYXoJ9bOwkWorsjF0c7mg",
    "https://mp.weixin.qq.com/s/olxDZGz0QXuOWobf4UioOg",
    "https://mp.weixin.qq.com/s/_h5hHQwJPyLJ5YGuT99Rlg",
    "https://mp.weixin.qq.com/s/oeRIbp0z9YoFEKEP90xTLg",
    "https://mp.weixin.qq.com/s/Mim-2yXSAK2NhYBfaHycNA",
    "https://mp.weixin.qq.com/s/ywo5b3twrlJAQ6Ngc68hsQ",
    "https://mp.weixin.qq.com/s/0v-Yn5p02nzMjw5Z8-Enlw",
    "https://mp.weixin.qq.com/s/gprIgBZnW-AOCE8EENbJIA",
    "https://mp.weixin.qq.com/s/VZUhUo-ppqpICzbbGgCpbA",
    "https://mp.weixin.qq.com/s/adiVbYo7EGe2WT2oCZOtYg",
    "https://mp.weixin.qq.com/s/tIhSfRIhIzz0iOzKIhI84A",
    "https://mp.weixin.qq.com/s/GK3i3Q7fpCriDPQYoYmzgw",
    "https://mp.weixin.qq.com/s/s1BOXDuiYH_7MUpypWSGpg",
]

FOCUS_ID = "ywo5b3twrlJAQ6Ngc68hsQ"


def safe_name(text: str) -> str:
    text = re.sub(r"[\\/:*?\"<>|\r\n]+", "_", text).strip()
    return text[:90] or "untitled"


def unique_urls(urls: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            result.append(url)
    return result


def text_or_empty(page, selector: str) -> str:
    loc = page.locator(selector)
    if loc.count() == 0:
        return ""
    return loc.first.inner_text(timeout=3000).strip()


def main() -> None:
    out_dir = Path("tmp_wechat_sources") / "playwright_extract"
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 390, "height": 1400},
            user_agent=(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
                "Mobile/15E148 Safari/604.1"
            ),
            locale="zh-CN",
        )
        page = context.new_page()

        for index, url in enumerate(unique_urls(URLS), start=1):
            article_id = url.rstrip("/").split("/")[-1]
            record = {
                "index": index,
                "id": article_id,
                "url": url,
                "status": "ok",
                "title": "",
                "author": "",
                "publish_time": "",
                "text_length": 0,
                "image_count": 0,
                "text_path": "",
                "html_path": "",
                "screenshot_path": "",
                "error": "",
            }

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                try:
                    page.wait_for_load_state("networkidle", timeout=12000)
                except PlaywrightTimeoutError:
                    pass
                page.wait_for_timeout(2500)

                title = text_or_empty(page, "#activity-name")
                author = text_or_empty(page, "#js_name")
                publish_time = text_or_empty(page, "#publish_time")
                content = text_or_empty(page, "#js_content")
                if not title:
                    title = page.title().strip()
                if not content:
                    content = page.locator("body").inner_text(timeout=5000).strip()

                image_count = page.locator("#js_content img").count()
                html = page.content()
                base = f"{index:02d}_{safe_name(title)}"
                text_path = out_dir / f"{base}.txt"
                html_path = out_dir / f"{base}.html"
                screenshot_path = ""
                text_path.write_text(content, encoding="utf-8")
                html_path.write_text(html, encoding="utf-8")

                if article_id == FOCUS_ID:
                    screenshot_file = out_dir / f"{base}.png"
                    page.screenshot(path=str(screenshot_file), full_page=True)
                    screenshot_path = str(screenshot_file)

                record.update(
                    {
                        "title": title,
                        "author": author,
                        "publish_time": publish_time,
                        "text_length": len(content),
                        "image_count": image_count,
                        "text_path": str(text_path),
                        "html_path": str(html_path),
                        "screenshot_path": screenshot_path,
                    }
                )
            except Exception as exc:  # noqa: BLE001
                record["status"] = "error"
                record["error"] = repr(exc)

            results.append(record)

        browser.close()

    (out_dir / "summary.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for item in results:
        print(
            f"{item['index']:02d} {item['status']} "
            f"{item['text_length']:>6} chars {item['image_count']:>3} imgs "
            f"{item['title']}"
        )
    print(f"Saved summary: {out_dir / 'summary.json'}")


if __name__ == "__main__":
    main()
