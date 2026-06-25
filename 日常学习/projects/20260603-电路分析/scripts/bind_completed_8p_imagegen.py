from __future__ import annotations

from pathlib import Path
import shutil

from PIL import Image, JpegImagePlugin
from pypdf import PdfReader


SRC_DIR = Path(r"C:\Users\13975\.codex\generated_images\019ee61c-6df7-7883-9608-86f90c9e0feb")
ROOT = Path(r"E:\ai产出文件\牛马\日常学习\projects\20260603-电路分析")
OUT_ROOT = ROOT / "outputs" / "imagegen_final"
PDF_OUT = ROOT / "outputs" / "PDF"


def make_contact_sheet(page_paths: list[Path], output: Path) -> None:
    thumbs = []
    for path in page_paths:
        image = Image.open(path).convert("RGB")
        image.thumbnail((240, 340))
        canvas = Image.new("RGB", (260, 370), "white")
        canvas.paste(image, ((260 - image.width) // 2, 10))
        thumbs.append(canvas)
    sheet = Image.new("RGB", (4 * 260, 2 * 370), (246, 242, 250))
    for index, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((index % 4) * 260, (index // 4) * 370))
    sheet.save(output, quality=95)


def bind_chapter(number: str, title: str, source_images: list[Path]) -> Path:
    chapter_dir = OUT_ROOT / f"第{number}章_{title}"
    pages_dir = chapter_dir / "pages"
    final_dir = chapter_dir / "final_pdf"
    preview_dir = chapter_dir / "preview"
    for directory in [pages_dir, final_dir, preview_dir, PDF_OUT]:
        directory.mkdir(parents=True, exist_ok=True)

    page_paths = []
    for index, source in enumerate(source_images, 1):
        target = pages_dir / f"ch{number}_p{index:02d}_imagegen.png"
        shutil.copyfile(source, target)
        page_paths.append(target)

    images = [Image.open(path).convert("RGB") for path in page_paths]
    built_pdf = final_dir / f"第{number}章_{title}.pdf"
    images[0].save(built_pdf, save_all=True, append_images=images[1:], resolution=144.0)
    final_pdf = PDF_OUT / f"第{number}章_{title}.pdf"
    shutil.copyfile(built_pdf, final_pdf)

    contact = preview_dir / f"第{number}章_{title}_8p_contact_sheet.png"
    make_contact_sheet(page_paths, contact)

    pages = len(PdfReader(str(final_pdf)).pages)
    if pages != 8:
        raise RuntimeError(f"{final_pdf} expected 8 pages, got {pages}")
    return final_pdf


def main() -> None:
    images = sorted(SRC_DIR.glob("*.png"), key=lambda path: path.stat().st_mtime)
    # Generation chronology:
    # 0-7: ch03 full 8p
    # 8-18: one-page versions for ch01,ch02,ch04,ch06,ch07,ch08,ch09,ch10,ch11,ch13,ch16
    # 19-25: ch01 p02-p08
    # 26-32: ch02 p02-p08
    jobs = [
        ("01", "电路模型和电路定律", [images[8], *images[19:26]]),
        ("02", "电阻电路的等效变换", [images[9], *images[26:33]]),
        ("04", "电路定理", [images[10], images[34], images[35], images[37], images[38], images[39], images[40], images[41]]),
        ("06", "储能元件", [images[11], images[42], images[45], images[46], images[47], images[50], images[51], images[52]]),
    ]
    results = []
    for number, title, chapter_images in jobs:
        results.append(str(bind_chapter(number, title, chapter_images)))

    record = OUT_ROOT / "IMAGEGEN_CALL_RECORD.md"
    with record.open("a", encoding="utf-8") as file:
        file.write("\n## 已补齐8页章节\n\n")
        for result in results:
            file.write(f"- {result}\n")
    print("\n".join(results))


if __name__ == "__main__":
    main()
