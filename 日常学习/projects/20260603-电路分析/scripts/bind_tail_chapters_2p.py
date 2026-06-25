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
    ("07", "一阶电路"),
    ("08", "相量法"),
    ("09", "正弦稳态电路分析"),
    ("10", "含有耦合电感的电路"),
    ("11", "电路的频率响应"),
    ("13", "非正弦周期电流电路"),
    ("16", "二端口网络"),
]


def bind_two_page(number: str, title: str, problem_page: Path) -> Path:
    chapter_dir = OUT_ROOT / f"第{number}章_{title}"
    pages_dir = chapter_dir / "pages"
    final_dir = chapter_dir / "final_pdf"
    preview_dir = chapter_dir / "preview"
    for directory in [pages_dir, final_dir, preview_dir, PDF_OUT]:
        directory.mkdir(parents=True, exist_ok=True)

    p01 = pages_dir / f"ch{number}_p01_imagegen_onepage.png"
    if not p01.exists():
        raise FileNotFoundError(p01)

    p02 = pages_dir / f"ch{number}_p02_imagegen_problem.png"
    shutil.copyfile(problem_page, p02)

    images = [Image.open(p01).convert("RGB"), Image.open(p02).convert("RGB")]
    built_pdf = final_dir / f"第{number}章_{title}.pdf"
    images[0].save(built_pdf, save_all=True, append_images=images[1:], resolution=144.0)
    final_pdf = PDF_OUT / f"第{number}章_{title}.pdf"
    shutil.copyfile(built_pdf, final_pdf)

    pages = len(PdfReader(str(final_pdf)).pages)
    if pages != 2:
        raise RuntimeError(f"{final_pdf} expected 2 pages, got {pages}")
    return final_pdf


def main() -> None:
    images = sorted(SRC_DIR.glob("*.png"), key=lambda path: path.stat().st_mtime)
    # Last 8 images are: one discarded wrong ch07 page, then 7 valid generic problem pages.
    valid_problem_pages = images[-7:]
    results = []
    for (number, title), problem_page in zip(CHAPTERS, valid_problem_pages):
        results.append(bind_two_page(number, title, problem_page))

    record = OUT_ROOT / "IMAGEGEN_CALL_RECORD.md"
    with record.open("a", encoding="utf-8") as file:
        file.write("\n## 第07章以后补充做题页\n\n")
        for result in results:
            file.write(f"- {result}：2页（知识点页 + 做题页）\n")
    print("\n".join(str(path) for path in results))


if __name__ == "__main__":
    main()
