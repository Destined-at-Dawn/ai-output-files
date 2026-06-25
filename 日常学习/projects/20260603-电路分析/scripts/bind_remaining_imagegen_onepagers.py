from __future__ import annotations

from pathlib import Path
import shutil

from PIL import Image, JpegImagePlugin
from pypdf import PdfReader


SRC_DIR = Path(r"C:\Users\13975\.codex\generated_images\019ee61c-6df7-7883-9608-86f90c9e0feb")
ROOT = Path(r"E:\ai产出文件\牛马\日常学习\projects\20260603-电路分析")
OUT_ROOT = ROOT / "outputs" / "imagegen_final"
PDF_OUT = ROOT / "outputs" / "PDF"

CHAPTERS = [
    ("01", "电路模型和电路定律"),
    ("02", "电阻电路的等效变换"),
    ("04", "电路定理"),
    ("06", "储能元件"),
    ("07", "一阶电路"),
    ("08", "相量法"),
    ("09", "正弦稳态电路分析"),
    ("10", "含有耦合电感的电路"),
    ("11", "电路的频率响应"),
    ("13", "非正弦周期电流电路"),
    ("16", "二端口网络"),
]


def main() -> None:
    PDF_OUT.mkdir(parents=True, exist_ok=True)
    images = sorted(SRC_DIR.glob("*.png"), key=lambda path: path.stat().st_mtime)
    if len(images) < 19:
        raise RuntimeError(f"Expected at least 19 image_gen images, got {len(images)}")

    onepagers = images[8:19]
    results: list[str] = []
    for source, (number, title) in zip(onepagers, CHAPTERS):
        chapter_dir = OUT_ROOT / f"第{number}章_{title}"
        pages_dir = chapter_dir / "pages"
        final_dir = chapter_dir / "final_pdf"
        preview_dir = chapter_dir / "preview"
        for directory in [pages_dir, final_dir, preview_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        page_path = pages_dir / f"ch{number}_p01_imagegen_onepage.png"
        shutil.copyfile(source, page_path)

        image = Image.open(page_path).convert("RGB")
        pdf_path = final_dir / f"第{number}章_{title}_imagegen直出版_1页.pdf"
        image.save(pdf_path, resolution=144.0)

        copied_pdf = PDF_OUT / pdf_path.name
        shutil.copyfile(pdf_path, copied_pdf)

        preview = preview_dir / f"第{number}章_{title}_imagegen直出版_preview.png"
        shutil.copyfile(page_path, preview)

        pages = len(PdfReader(str(copied_pdf)).pages)
        results.append(f"- 第{number}章 {title}：{copied_pdf}；页数：{pages}；原图：{source}")

    record = OUT_ROOT / "IMAGEGEN_CALL_RECORD.md"
    with record.open("a", encoding="utf-8") as file:
        file.write("\n## 其余章节一页 image_gen 冲刺版\n\n")
        file.write("\n".join(results))
        file.write("\n")

    print("\n".join(results))


if __name__ == "__main__":
    main()
