from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def find_ch13_output() -> Path:
    outputs = ROOT / "outputs"
    for child in outputs.iterdir():
        if child.is_dir() and "13" in child.name and "PDF" in child.name:
            return child
    raise FileNotFoundError("Chapter 13 PDF output directory not found.")


def write_tex(build_dir: Path, page_count: int) -> Path:
    lines = [
        r"\documentclass[a4paper]{article}",
        r"\usepackage[margin=0pt]{geometry}",
        r"\usepackage{graphicx}",
        r"\usepackage{pdfpages}",
        r"\pagestyle{empty}",
        r"\begin{document}",
    ]
    for i in range(1, page_count + 1):
        lines.append(
            rf"\noindent\includegraphics[width=\paperwidth,height=\paperheight,keepaspectratio]{{page_{i:02d}.png}}"
        )
        if i != page_count:
            lines.append(r"\clearpage")
    lines.append(r"\end{document}")
    tex = build_dir / "ch13_review_v3_latex.tex"
    tex.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return tex


def main() -> None:
    out = find_ch13_output()
    source_pages = out / "pages_v2"
    pages = sorted(source_pages.glob("*.png"))
    if not pages:
        raise FileNotFoundError(f"No PNG pages found in {source_pages}")

    build_dir = out / "latex_build_v3"
    build_dir.mkdir(parents=True, exist_ok=True)

    for old in build_dir.glob("page_*.png"):
        old.unlink()
    for index, page in enumerate(pages, 1):
        shutil.copyfile(page, build_dir / f"page_{index:02d}.png")

    tex = write_tex(build_dir, len(pages))
    cmd = ["xelatex", "-interaction=nonstopmode", "-halt-on-error", tex.name]
    subprocess.run(cmd, cwd=build_dir, check=True)

    built_pdf = build_dir / "ch13_review_v3_latex.pdf"
    generated_pdf = tex.with_suffix(".pdf")
    if generated_pdf != built_pdf:
        shutil.copyfile(generated_pdf, built_pdf)

    final_pdf = out / "第13章_非正弦周期电流电路_复习PDF_v3_LaTeX合成.pdf"
    shutil.copyfile(built_pdf, final_pdf)

    note = out / "latex_build_v3.md"
    note.write_text(
        "\n".join(
            [
                "# 第13章复习PDF v3 LaTeX 构建记录",
                "",
                "## 结论",
                "",
                "v3 使用 SOP 要求的“逐页图片 -> LaTeX 合成 PDF”链路生成。",
                "",
                "## 输入",
                "",
                f"- 页面图片目录：{source_pages}",
                f"- 页面数量：{len(pages)}",
                "- 页面尺寸：1055 x 1491 px",
                "",
                "## 输出",
                "",
                f"- LaTeX 源文件：{tex}",
                f"- 构建目录 PDF：{built_pdf}",
                f"- 最终 PDF：{final_pdf}",
                "",
                "## Source",
                "",
                "- SOPs/06_复习PDF制作SOP.md#PDF / 图片制作流程",
                "- outputs/第13章_非正弦周期电流电路_复习PDF/source_pack_v2.md#结论",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(final_pdf)
    print(note)


if __name__ == "__main__":
    main()
