# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import shutil

import pdfplumber
import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


ROOT = Path(r"E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理")
OUT = ROOT / "outputs" / "ch06_static_review_v3_imagegen"
PAGE_DIR = OUT / "source_pages"
PAGE_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class Source:
    key: str
    kind: str
    path: Path
    priority: int


SOURCES = [
    Source("final_review", "老师总复习/划重点", ROOT / "outputs" / "大物B1总复习.pdf", 1),
    Source("spring_2024_b1", "最新真题", ROOT / "真题库" / "24春大学物理B1 (A卷）(1)(1).pdf", 2),
    Source("class_practice_06", "课堂练习PDF", ROOT / "第06章-静电场" / "原来" / "课堂练习06.pdf", 3),
    Source("textbook_up_5th", "教材", ROOT / "shared" / "教材" / "大学物理学_上_第5版.pdf", 4),
    Source("workbook_5th", "配套教辅", ROOT / "shared" / "教辅" / "大学物理学学习指导和能力训练_第5版.pdf", 5),
]

for idx, pdf in enumerate(sorted((ROOT / "真题库").glob("*.pdf")), start=1):
    if pdf.name == "24春大学物理B1 (A卷）(1)(1).pdf":
        continue
    SOURCES.append(Source(f"past_{idx:02d}", "往届真题", pdf, 10 + idx))


TERMS = {
    "静电": 6,
    "电场": 5,
    "电荷": 4,
    "高斯": 6,
    "电势": 6,
    "电通量": 7,
    "库仑": 5,
    "导体": 4,
    "电介质": 3,
    "电容": 2,
    "等势": 5,
    "场强": 5,
    "真空中": 2,
}

FORCED_PAGES = {
    "final_review": set(range(47, 58)),
    "textbook_up_5th": {121, 131, 141, 161, *range(171, 177)},
    "workbook_5th": set(range(91, 111)),
}


def clean_text(txt: str) -> str:
    return re.sub(r"\s+", " ", txt or "").strip()


def page_score(text: str) -> tuple[int, list[str]]:
    hits = []
    score = 0
    for term, weight in TERMS.items():
        n = text.count(term)
        if n:
            score += n * weight
            hits.append(f"{term}×{n}")
    return score, hits


def safe_name(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_\-]+", "_", text)


def render_page(src: Source, page_num: int, scale: float = 2.2) -> Path:
    doc = pdfium.PdfDocument(str(src.path))
    try:
        page = doc[page_num - 1]
        bitmap = page.render(scale=scale)
        img = bitmap.to_pil().convert("RGB")
        out = PAGE_DIR / f"{src.key}_p{page_num:03d}.png"
        img.save(out, quality=95)
        return out
    finally:
        doc.close()


def make_contact_sheet(rendered: list[tuple[Source, int, int, Path]]) -> Path | None:
    if not rendered:
        return None
    font_path = Path(r"C:\Windows\Fonts\msyh.ttc")
    font = ImageFont.truetype(str(font_path), 18) if font_path.exists() else ImageFont.load_default()
    thumb_w, thumb_h = 420, 300
    cols = 2
    rows = (len(rendered) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * thumb_h), (245, 248, 250))
    draw = ImageDraw.Draw(sheet)
    for i, (src, page, score, path) in enumerate(rendered):
        img = Image.open(path).convert("RGB")
        img.thumbnail((thumb_w - 28, thumb_h - 58), Image.Resampling.LANCZOS)
        x = (i % cols) * thumb_w
        y = (i // cols) * thumb_h
        sheet.paste(img, (x + (thumb_w - img.width) // 2, y + 12))
        label = f"{src.kind} | {src.path.name[:22]} | p{page} | score {score}"
        draw.text((x + 14, y + thumb_h - 36), label, fill=(20, 35, 50), font=font)
    out = OUT / "CH06_静电场候选题图_contact_sheet.png"
    sheet.save(out, quality=95)
    return out


def make_reference_pdf(rendered: list[tuple[Source, int, int, Path]]) -> Path | None:
    if not rendered:
        return None
    page_w, page_h = A4
    out = OUT / "CH06_静电场候选题图参考包.pdf"
    c = canvas.Canvas(str(out), pagesize=A4)
    for src, page_num, score, path in rendered:
        with Image.open(path) as opened:
            iw, ih = opened.size
        max_w, max_h = page_w, page_h
        scale = min(max_w / iw, max_h / ih)
        draw_w, draw_h = iw * scale, ih * scale
        x = (page_w - draw_w) / 2
        y = (page_h - draw_h) / 2
        c.drawImage(str(path), x, y, width=draw_w, height=draw_h, preserveAspectRatio=True, mask="auto")
        c.showPage()
    c.save()
    return out


def make_selected_problem_pdf(rendered: list[tuple[Source, int, int, Path]]) -> Path | None:
    if not rendered:
        return None
    selected_rules = {
        "spring_2024_b1": None,
        "final_review": {48, 49, 50, 51, 52, 53, 54, 55, 56, 57},
        "class_practice_06": None,
        "textbook_up_5th": set(range(171, 177)),
        "workbook_5th": set(range(91, 111)),
    }
    ordered_keys = [
        "spring_2024_b1",
        "final_review",
        "class_practice_06",
        "textbook_up_5th",
        "workbook_5th",
    ]
    key_rank = {key: i for i, key in enumerate(ordered_keys)}
    selected = []
    for item in rendered:
        src, page_num, _score, _path = item
        allowed = selected_rules.get(src.key)
        if src.key.startswith("past_"):
            selected.append(item)
        elif src.key in selected_rules and (allowed is None or page_num in allowed):
            selected.append(item)
    selected.sort(key=lambda item: (key_rank.get(item[0].key, 99), item[0].key, item[1]))

    page_w, page_h = A4
    out = OUT / "CH06_静电场精选题图包.pdf"
    c = canvas.Canvas(str(out), pagesize=A4)
    for _src, _page_num, _score, path in selected:
        with Image.open(path) as opened:
            iw, ih = opened.size
        scale = min(page_w / iw, page_h / ih)
        draw_w, draw_h = iw * scale, ih * scale
        x = (page_w - draw_w) / 2
        y = (page_h - draw_h) / 2
        c.drawImage(str(path), x, y, width=draw_w, height=draw_h, preserveAspectRatio=True, mask="auto")
        c.showPage()
    c.save()
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    rendered: list[tuple[Source, int, int, Path]] = []

    for src in SOURCES:
        if not src.path.exists():
            rows.append((src, 0, 0, 0, [], "文件不存在", ""))
            continue
        try:
            with pdfplumber.open(str(src.path)) as pdf:
                total = len(pdf.pages)
                candidate_pages = []
                for i, page in enumerate(pdf.pages, start=1):
                    text = clean_text(page.extract_text() or "")
                    score, hits = page_score(text)
                    forced = i in FORCED_PAGES.get(src.key, set())
                    # 教材/教辅比较长，阈值稍高；真题较短，阈值稍低。
                    threshold = 14 if src.kind in {"教材", "配套教辅"} else 8
                    if forced or score >= threshold:
                        snippet = text[:180]
                        candidate_pages.append((i, score, hits, snippet))
                # 对每个来源限制渲染数量，避免候选包过大；总复习和第六章课堂练习保留更多。
                if src.key == "final_review":
                    selected = candidate_pages[:14]
                elif src.key == "class_practice_06":
                    selected = candidate_pages[:18]
                elif src.key in {"textbook_up_5th", "workbook_5th"}:
                    selected = sorted(candidate_pages, key=lambda x: x[1], reverse=True)[:24]
                    selected = sorted(selected, key=lambda x: x[0])
                else:
                    selected = sorted(candidate_pages, key=lambda x: x[1], reverse=True)[:6]
                    selected = sorted(selected, key=lambda x: x[0])

                for page_num, score, hits, snippet in selected:
                    try:
                        img_path = render_page(src, page_num)
                        rendered.append((src, page_num, score, img_path))
                    except Exception as exc:
                        img_path = Path(f"渲染失败：{exc}")
                    rows.append((src, total, page_num, score, hits, "保留候选", snippet))
        except Exception as exc:
            rows.append((src, 0, 0, 0, [], f"扫描失败：{exc}", ""))

    contact = make_contact_sheet(rendered)
    ref_pdf = make_reference_pdf(rendered)
    selected_pdf = make_selected_problem_pdf(rendered)

    md = OUT / "00_CH06_静电场资料扫描与候选题图索引.md"
    lines = [
        "# 第06章静电场资料扫描与候选题图索引",
        "",
        "## 结论",
        "",
        "已按关键词筛选教材、教辅、总复习 PDF、课堂练习 PDF 与真题库中的静电场相关页，并渲染为候选题图。该文件是后续 image_gen 自然融合题图的素材索引，不是最终复习 PDF。",
        "",
        "## 输出",
        "",
        f"- 候选题图目录：`{PAGE_DIR}`",
        f"- 候选题图总览：`{contact}`" if contact else "- 候选题图总览：无",
        f"- 候选题图参考包：`{ref_pdf}`" if ref_pdf else "- 候选题图参考包：无",
        f"- 精选题图包：`{selected_pdf}`" if selected_pdf else "- 精选题图包：无",
        "",
        "## 候选页",
        "",
    ]
    current = None
    for src, total, page_num, score, hits, status, snippet in rows:
        if current != src.key:
            current = src.key
            lines += [
                "",
                f"### {src.kind}：{src.path.name}",
                "",
                f"- 文件：`{src.path}`",
                f"- 总页数：{total if total else '未知'}",
                "",
            ]
        if page_num:
            img = PAGE_DIR / f"{src.key}_p{page_num:03d}.png"
            lines += [
                f"#### p{page_num} | score {score} | {status}",
                "",
                f"- 命中：{', '.join(hits) if hits else '强制保留/待人工判断'}",
                f"- 截图：`{img}`",
                f"- 摘要：{snippet}",
                "",
            ]
        else:
            lines += [f"- {status}", ""]

    md.write_text("\n".join(lines), encoding="utf-8")
    print(md)
    if contact:
        print(contact)
    if ref_pdf:
        print(ref_pdf)
    if selected_pdf:
        print(selected_pdf)
    print(f"rendered={len(rendered)}")


if __name__ == "__main__":
    main()
