from __future__ import annotations

from pathlib import Path
import shutil

from PIL import Image, JpegImagePlugin
from pypdf import PdfReader


SRC_DIR = Path(r"C:\Users\13975\.codex\generated_images\019ee61c-6df7-7883-9608-86f90c9e0feb")
ROOT = Path(r"E:\ai产出文件\牛马\日常学习\projects\20260603-电路分析")
OUT = ROOT / "outputs" / "imagegen_final" / "第03章_电阻电路的一般分析"
PAGES_DIR = OUT / "pages"
PREVIEW_DIR = OUT / "preview"
FINAL_DIR = OUT / "final_pdf"
PDF_OUT = ROOT / "outputs" / "PDF"


def make_contact_sheet(page_paths: list[Path], output: Path) -> None:
    thumbs: list[Image.Image] = []
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


def main() -> None:
    for directory in [PAGES_DIR, PREVIEW_DIR, FINAL_DIR, PDF_OUT]:
        directory.mkdir(parents=True, exist_ok=True)

    source_images = sorted(SRC_DIR.glob("*.png"), key=lambda path: path.stat().st_mtime)
    if len(source_images) < 8:
        raise RuntimeError(f"Expected 8 image_gen pages, got {len(source_images)} from {SRC_DIR}")

    page_paths: list[Path] = []
    for index, source in enumerate(source_images[:8], 1):
        target = PAGES_DIR / f"ch03_p{index:02d}_imagegen.png"
        shutil.copyfile(source, target)
        page_paths.append(target)

    images = [Image.open(path).convert("RGB") for path in page_paths]
    pdf_path = FINAL_DIR / "第03章_电阻电路的一般分析_imagegen直出版_8页.pdf"
    images[0].save(pdf_path, save_all=True, append_images=images[1:], resolution=144.0)

    copied_pdf = PDF_OUT / pdf_path.name
    shutil.copyfile(pdf_path, copied_pdf)

    contact = PREVIEW_DIR / "第03章_电阻电路的一般分析_imagegen直出版_8p_contact_sheet.png"
    make_contact_sheet(page_paths, contact)

    record = ROOT / "outputs" / "imagegen_final" / "IMAGEGEN_CALL_RECORD.md"
    with record.open("a", encoding="utf-8") as file:
        file.write("\n## 第03章完整8页\n\n")
        file.write(f"- 原始 image_gen 目录：{SRC_DIR}\n")
        file.write(f"- 页图目录：{PAGES_DIR}\n")
        file.write(f"- 最终PDF：{copied_pdf}\n")
        file.write(f"- 总览图：{contact}\n")
        file.write(f"- PDF页数：{len(PdfReader(str(copied_pdf)).pages)}\n")

    print(copied_pdf)
    print(contact)
    print(f"pages={len(PdfReader(str(copied_pdf)).pages)}")


if __name__ == "__main__":
    main()
