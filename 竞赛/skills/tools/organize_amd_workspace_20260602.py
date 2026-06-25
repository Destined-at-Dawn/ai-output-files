from __future__ import annotations

import csv
import os
import shutil
from datetime import datetime
from pathlib import Path


SRC = Path("D:/AMD")
EXTERNAL_EEPROM_PROJECT = Path("D:/xillin")


def unique_target_root() -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return SRC / f"_整理版_{stamp}"


def ensure_dirs(root: Path) -> dict[str, Path]:
    dirs = {
        "index": root / "00_整理说明与索引",
        "final": root / "01_最终交付物_老板可直接发送",
        "projects": root / "02_工程文件_可继续开发",
        "docs": root / "03_实验文档_DOCX_PDF_MD",
        "ai": root / "04_AI协作区_交接记录与经验",
        "intermediate": root / "05_中间产物与历史版本",
        "refs": root / "06_资料数据手册与原理图",
        "tools": root / "07_工具脚本",
    }
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    return dirs


def rel_to_src(path: Path) -> str:
    try:
        return str(path.relative_to(SRC)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def copy_file(src: Path, dst_dir: Path, manifest: list[dict[str, str]], category: str) -> None:
    if not src.exists() or not src.is_file():
        return
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    if dst.exists():
        base = dst.stem
        suffix = dst.suffix
        dst = dst_dir / f"{base}__dup{suffix}"
    shutil.copy2(src, dst)
    manifest.append({
        "category": category,
        "kind": "file",
        "source": str(src),
        "organized": str(dst),
        "size_bytes": str(src.stat().st_size),
        "mtime": datetime.fromtimestamp(src.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
    })


def ignore_generated(dir_path: str, names: list[str]) -> set[str]:
    # Keep Vivado projects intact for current deliverables, but avoid copying
    # transient cache folders when organizing older non-final projects.
    ignored = set()
    for name in names:
        if name in {".Xil", ".git", "__pycache__"}:
            ignored.add(name)
    return ignored


def copy_dir(src: Path, dst_dir: Path, manifest: list[dict[str, str]], category: str, full: bool = True) -> None:
    if not src.exists() or not src.is_dir():
        return
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    if dst.exists():
        dst = dst_dir / f"{src.name}__dup"
    shutil.copytree(src, dst, ignore=None if full else ignore_generated)
    size = sum(p.stat().st_size for p in src.rglob("*") if p.is_file())
    manifest.append({
        "category": category,
        "kind": "directory",
        "source": str(src),
        "organized": str(dst),
        "size_bytes": str(size),
        "mtime": datetime.fromtimestamp(src.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
    })


def top_files(pattern: str) -> list[Path]:
    return sorted(SRC.glob(pattern), key=lambda p: p.name)


def write_manifest(root: Path, manifest: list[dict[str, str]]) -> None:
    manifest_path = root / "00_整理说明与索引" / "整理清单.csv"
    with manifest_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["category", "kind", "source", "organized", "size_bytes", "mtime"])
        writer.writeheader()
        writer.writerows(manifest)


def write_readme(root: Path, manifest: list[dict[str, str]]) -> None:
    readme = root / "00_整理说明与索引" / "README_整理说明.md"
    lines = [
        "# D:/AMD 非破坏式整理说明",
        "",
        f"整理时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 安全策略",
        "",
        "- 未删除任何原文件。",
        "- 未移动任何原文件。",
        "- 本目录是新建整理版本，所有内容来自复制或索引。",
        "- 原始工作区仍保留在 `D:/AMD`，EEPROM 当前工程额外来自 `D:/xillin`。",
        "",
        "## 分类结构",
        "",
        "- `01_最终交付物_老板可直接发送`：最终 ZIP、bit/ltx 配套包。",
        "- `02_工程文件_可继续开发`：当前可继续开发的 Vivado 工程。",
        "- `03_实验文档_DOCX_PDF_MD`：实验指导书、客户文档、PDF/MD。",
        "- `04_AI协作区_交接记录与经验`：交接、经验、归档、AI 生成过程材料。",
        "- `05_中间产物与历史版本`：旧版 ZIP、早期工程、恢复点、历史压缩包。",
        "- `06_资料数据手册与原理图`：datasheet、公司手册、原理图图片。",
        "- `07_工具脚本`：脚本、工具、COE/HEX 生成相关文件。",
        "",
        "## 下次使用建议",
        "",
        "1. 给老板发文件时，优先使用 `01_最终交付物_老板可直接发送`。",
        "2. 继续改代码时，优先从 `02_工程文件_可继续开发` 找当前工程。",
        "3. 写文档时，从 `03_实验文档_DOCX_PDF_MD` 找最终 DOCX。",
        "4. 查旧问题和 AI 经验时，看 `04_AI协作区_交接记录与经验`。",
        "5. 旧 ZIP 和实验过程版本不要直接发老板，除非明确需要回溯。",
        "",
        "## 本次整理统计",
        "",
        f"- 已复制/登记条目数：{len(manifest)}",
        "- 详细清单：`整理清单.csv`",
    ]
    readme.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    root = unique_target_root()
    dirs = ensure_dirs(root)
    manifest: list[dict[str, str]] = []

    # 01 final deliverables
    final_names = [
        "ADC1采样_DAC1固定10Hz回放实验_含实验文档_20260602.zip",
        "AT21CS01单总线EEPROM读写暖复位实验_含实验文档_20260602.zip",
        "EEPROM单总线读写_AT21CS01暖复位修正版_D0成功D1失败_20260602.zip",
    ]
    for name in final_names:
        copy_file(SRC / name, dirs["final"] / "20260602_最终确认版本", manifest, "最终交付物")

    # 02 current projects
    copy_dir(SRC / "dac_adc1_loopback_10hz", dirs["projects"] / "当前可用工程", manifest, "工程文件")
    copy_dir(EXTERNAL_EEPROM_PROJECT, dirs["projects"] / "当前可用工程", manifest, "工程文件_外部来源D_xillin")
    for name in ["dac1_triangle_1khz", "eeprom_rw", "05_eeprom_rw"]:
        copy_dir(SRC / name, dirs["projects"] / "历史可参考工程", manifest, "工程文件_历史参考", full=False)

    # 03 documents
    doc_root = SRC / "project_output" / "实验文档"
    if doc_root.exists():
        copy_dir(doc_root, dirs["docs"] / "实验文档集中归档", manifest, "实验文档")
    for path in top_files("*.docx"):
        copy_file(path, dirs["docs"] / "根目录散落DOCX", manifest, "实验文档_散落")

    # 04 AI collaboration and archives
    for name in ["ADC_archives", "zip", "_restore_dac_adc1_loopback_before_highspeed_20260530"]:
        copy_dir(SRC / name, dirs["ai"] / "归档与恢复点", manifest, "AI协作区_归档", full=False)
    for path in (SRC / "ADC").glob("*.md") if (SRC / "ADC").exists() else []:
        copy_file(path, dirs["ai"] / "ADC交接记录", manifest, "AI协作区_交接")
    for path in top_files("*.txt"):
        copy_file(path, dirs["ai"] / "日志与记录", manifest, "AI协作区_日志")

    # 05 intermediate and historical packages
    final_set = set(final_names)
    for path in top_files("*.zip"):
        if path.name not in final_set:
            copy_file(path, dirs["intermediate"] / "历史ZIP包", manifest, "中间产物_历史ZIP")
    for pattern in ["*.rar", "*.7z"]:
        for path in top_files(pattern):
            copy_file(path, dirs["intermediate"] / "历史压缩包", manifest, "中间产物_压缩包")
    for name in [
        "ADC",
        "current",
        "ctp",
        "screen_4bit",
        "touch_4bit",
        "touchscreen",
        "touchscreen1",
        "touchsreeen",
        "rubbish",
    ]:
        copy_dir(SRC / name, dirs["intermediate"] / "历史工程与过程目录", manifest, "中间产物_历史目录", full=False)

    # 06 references
    for name in ["datasheets", "material"]:
        copy_dir(SRC / name, dirs["refs"] / "资料手册", manifest, "资料数据手册")
    if (SRC / "ADC").exists():
        img_dir = dirs["refs"] / "ADC_DAC_EEPROM原理图图片"
        for ext in ("*.png", "*.jpg", "*.jpeg"):
            for path in (SRC / "ADC").glob(ext):
                copy_file(path, img_dir, manifest, "资料原理图")

    # 07 tools and standalone scripts/assets
    for name in ["tools", "image_to_coe_toolkit", "general"]:
        copy_dir(SRC / name, dirs["tools"] / "工具目录", manifest, "工具脚本", full=False)
    for ext in ("*.py", "*.tcl", "*.v", "*.xdc", "*.coe", "*.hex", "*.png"):
        for path in top_files(ext):
            copy_file(path, dirs["tools"] / "根目录散落脚本与资源", manifest, "工具脚本_散落")

    write_manifest(root, manifest)
    write_readme(root, manifest)
    print(root)
    print(len(manifest))


if __name__ == "__main__":
    main()
