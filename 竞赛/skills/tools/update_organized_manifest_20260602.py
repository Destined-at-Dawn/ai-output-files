from __future__ import annotations

import csv
import datetime
import shutil
from pathlib import Path


ROOT = Path("D:/AMD/_整理版_20260602_143315")
AMD = Path("D:/AMD")
INDEX_DIR = ROOT / "00_整理说明与索引"
MANIFEST = INDEX_DIR / "整理清单.csv"
SNAPSHOT = INDEX_DIR / "原始D_AMD文件快照.csv"
README = INDEX_DIR / "README_整理说明.md"
AI_DIR = ROOT / "04_AI协作区_交接记录与经验" / "AI经验库同步"
FINAL_DOC_DIR = ROOT / "03_实验文档_DOCX_PDF_MD" / "20260602_最终实验指导书DOCX"


def main() -> None:
    rows = []
    if MANIFEST.exists():
        with MANIFEST.open("r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))

    source_map = {
        "rtl_code_lessons.md": "${WORKSPACE_ROOT}/memory/rtl_code_lessons.md",
        "rtl-one-pass-sop.md": "${WORKSPACE_ROOT}/self-evolution/rtl-one-pass-sop.md",
        "12_FPGA_RTL客户交付一把过SOP.md": "${WORKSPACE_ROOT}/SOPs/12_FPGA_RTL客户交付一把过SOP.md",
        "fpga_rtl_delivery_skill_chain.md": "${WORKSPACE_ROOT}/skill-calls/fpga_rtl_delivery_skill_chain.md",
        "vivado_rtl_lessons_global_skill.md": "C:/Users/13975/.agents/skills/rtl-fpga-lessons/references/vivado_rtl_lessons.md",
    }
    AI_DIR.mkdir(parents=True, exist_ok=True)
    for target_name, source in source_map.items():
        source_path = Path(source)
        if source_path.exists():
            shutil.copy2(source_path, AI_DIR / target_name)

    existing = {(r["source"], r["organized"]) for r in rows}

    final_doc_sources = [
        AMD / "project_output" / "实验文档" / "实验指导书_ADC1采样DAC1回放固定10Hz.docx",
        AMD / "project_output" / "实验文档" / "实验指导书_AT21CS01单总线EEPROM读写暖复位.docx",
    ]
    FINAL_DOC_DIR.mkdir(parents=True, exist_ok=True)
    for source_path in final_doc_sources:
        if not source_path.exists():
            continue
        target_path = FINAL_DOC_DIR / source_path.name
        shutil.copy2(source_path, target_path)
        key = (str(source_path), str(target_path))
        if key in existing:
            continue
        rows.append({
            "category": "实验文档_最终指导书",
            "kind": "file",
            "source": str(source_path),
            "organized": str(target_path),
            "size_bytes": str(target_path.stat().st_size),
            "mtime": datetime.datetime.fromtimestamp(target_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        })
        existing.add(key)

    for path in sorted(AI_DIR.glob("*")):
        if not path.is_file():
            continue
        source = source_map.get(path.name, str(path))
        key = (source, str(path))
        if key in existing:
            continue
        rows.append({
            "category": "AI协作区_经验库同步",
            "kind": "file",
            "source": source,
            "organized": str(path),
            "size_bytes": str(path.stat().st_size),
            "mtime": datetime.datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        })

    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["category", "kind", "source", "organized", "size_bytes", "mtime"])
        writer.writeheader()
        writer.writerows(rows)

    with SNAPSHOT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["path", "size_bytes", "mtime", "extension"])
        for path in AMD.rglob("*"):
            if not path.is_file():
                continue
            rel = str(path.relative_to(AMD)).replace("\\", "/")
            if rel.startswith("_整理版_"):
                continue
            st = path.stat()
            writer.writerow([
                str(path),
                st.st_size,
                datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                path.suffix,
            ])

    text = README.read_text(encoding="utf-8-sig" if README.exists() else "utf-8")
    import re
    text = re.sub(r"- 已复制/登记条目数：\d+", f"- 已复制/登记条目数：{len(rows)}", text)
    if "原始D_AMD文件快照.csv" not in text:
        text += "\n- 原始目录快照：`原始D_AMD文件快照.csv`\n"
    if "20260602_最终实验指导书DOCX" not in text:
        text += "- 最终实验指导书：`03_实验文档_DOCX_PDF_MD/20260602_最终实验指导书DOCX/`\n"
    README.write_text(text, encoding="utf-8-sig")

    print(len(rows))
    print(SNAPSHOT)


if __name__ == "__main__":
    main()
