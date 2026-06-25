from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter


ROOT = Path(r"E:\ai产出文件\牛马\日常学习\projects\20260603-电路分析")
PDF_DIR = ROOT / "outputs" / "PDF"
OUTPUT = PDF_DIR / "电路分析_期末冲刺全书版.pdf"

CHAPTER_FILES = [
    "第01章_电路模型和电路定律.pdf",
    "第02章_电阻电路的等效变换.pdf",
    "第03章_电阻电路的一般分析.pdf",
    "第04章_电路定理.pdf",
    "第06章_储能元件.pdf",
    "第07章_一阶电路.pdf",
    "第08章_相量法.pdf",
    "第09章_正弦稳态电路分析.pdf",
    "第10章_含有耦合电感的电路.pdf",
    "第11章_电路的频率响应.pdf",
    "第13章_非正弦周期电流电路.pdf",
    "第16章_二端口网络.pdf",
]


def main() -> None:
    writer = PdfWriter()
    page_start = 0
    manifest: list[str] = []

    for filename in CHAPTER_FILES:
        path = PDF_DIR / filename
        if not path.exists():
            raise FileNotFoundError(path)

        reader = PdfReader(str(path))
        chapter_title = path.stem
        writer.add_outline_item(chapter_title, page_start)
        for page in reader.pages:
            writer.add_page(page)

        manifest.append(f"- {filename}: {len(reader.pages)}页, 起始页 {page_start + 1}")
        page_start += len(reader.pages)

    with OUTPUT.open("wb") as file:
        writer.write(file)

    manifest_path = PDF_DIR / "电路分析_期末冲刺全书版_manifest.md"
    manifest_path.write_text(
        "\n".join(
            [
                "# 电路分析期末冲刺全书版 manifest",
                "",
                "## 结论",
                "",
                f"- 输出文件：{OUTPUT}",
                f"- 总页数：{len(PdfReader(str(OUTPUT)).pages)}",
                "- 已添加章节书签。",
                "",
                "## 章节顺序",
                "",
                *manifest,
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(OUTPUT)
    print(f"pages={len(PdfReader(str(OUTPUT)).pages)}")
    print(manifest_path)


if __name__ == "__main__":
    main()
