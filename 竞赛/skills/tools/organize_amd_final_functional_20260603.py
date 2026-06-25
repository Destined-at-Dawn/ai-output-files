from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path("D:/AMD")
BEFORE = Path("D:/AMD_before")
OLD_ARCHIVE = ROOT / "历史归档" / "旧版编号整理目录_20260602"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def copy_file(src: Path, dst: Path, rows: list[dict[str, str]], category: str, function: str) -> None:
    if not src.exists():
        rows.append({
            "功能": function,
            "类别": category,
            "文件": "",
            "位置": "",
            "来源": str(src),
            "状态": "来源不存在",
        })
        return
    ensure_dir(dst.parent)
    shutil.copy2(src, dst)
    rows.append({
        "功能": function,
        "类别": category,
        "文件": dst.name,
        "位置": str(dst),
        "来源": str(src),
        "状态": "已复制",
    })


def copy_selected_tree(src_root: Path, dst_root: Path, rows: list[dict[str, str]], function: str) -> None:
    if not src_root.exists():
        rows.append({
            "功能": function,
            "类别": "源码工程",
            "文件": "",
            "位置": str(dst_root),
            "来源": str(src_root),
            "状态": "源码目录不存在",
        })
        return

    keep_suffix = {".v", ".xdc", ".tcl", ".md", ".docx", ".csv"}
    keep_dirs = {"rtl", "xdc", "scripts", "sim", "docs", "references", "boss_ready_eeprom_package_20260601"}
    skip_parts = {".Xil", "vivado_project", "vivado_project_old", "vivado_project_backup"}

    for path in src_root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(src_root)
        parts = set(rel.parts)
        if parts & skip_parts:
            continue
        if path.suffix.lower() not in keep_suffix and not (parts & keep_dirs):
            continue
        target = dst_root / rel
        copy_file(path, target, rows, "源码工程", function)


def move_old_numbered_dirs() -> None:
    ensure_dir(OLD_ARCHIVE)
    for path in ROOT.iterdir():
        if not path.is_dir():
            continue
        name = path.name
        if len(name) >= 3 and name[:2].isdigit() and name[2] == "_":
            target = OLD_ARCHIVE / name
            if target.exists():
                continue
            shutil.move(str(path), str(target))


def write_readme(rows: list[dict[str, str]]) -> None:
    lines = [
        "# D:/AMD 快速查找索引",
        "",
        "## 使用方式",
        "",
        "- 给老板发最终文件：看 `老板可直接发送的最终压缩包/`。",
        "- 找某个功能对应的文档和代码：看 `最终交付包/<功能名>/`。",
        "- 找历史旧包：看 `历史参考包/`。",
        "- 找数据手册和原理图：看 `公共资料/`。",
        "- 上一次编号式整理目录已归档到 `历史归档/旧版编号整理目录_20260602/`，没有删除。",
        "",
        "## 最终交付功能",
        "",
    ]

    functions = []
    for row in rows:
        if row["功能"] and row["功能"] not in functions and row["类别"] == "最终压缩包":
            functions.append(row["功能"])

    for function in functions:
        lines.append(f"### {function}")
        for row in rows:
            if row["功能"] != function:
                continue
            if row["类别"] in {"最终压缩包", "实验文档", "顶层代码", "控制代码", "I2C代码", "约束文件", "说明文件"}:
                rel = Path(row["位置"]).relative_to(ROOT) if row["位置"] else ""
                lines.append(f"- {row['类别']}：`{rel}`")
        lines.append("")

    lines.extend([
        "## 目录说明",
        "",
        "- `最终交付包/`：按功能聚合，ZIP、DOCX、RTL、XDC、Tcl在同一个功能目录下。",
        "- `老板可直接发送的最终压缩包/`：只放可以直接发送的最终ZIP。",
        "- `公共资料/`：原理图图片、datasheet、学习板资料。",
        "- `AI协作记录/`：交接记录、理论分析、经验说明。",
        "- `历史参考包/`：旧版但仍可能用于回溯的功能包。",
        "- `工具脚本/`：COE/图片转换/Vivado辅助脚本。",
    ])
    (ROOT / "快速查找索引.md").write_text("\n".join(lines) + "\n", encoding="utf-8-sig")


def main() -> None:
    if not BEFORE.exists():
        raise SystemExit(f"Missing source folder: {BEFORE}")
    ensure_dir(ROOT)
    move_old_numbered_dirs()

    rows: list[dict[str, str]] = []

    base_dirs = [
        "最终交付包",
        "老板可直接发送的最终压缩包",
        "公共资料/原理图图片",
        "公共资料/数据手册",
        "AI协作记录",
        "历史参考包",
        "工具脚本",
        "历史归档",
    ]
    for d in base_dirs:
        ensure_dir(ROOT / d)

    final_items = [
        {
            "function": "ADC1采样_DAC1可调采样率回放_默认4kSPS",
            "zip": BEFORE / "ADC1采样_DAC1可调采样率回放_默认4kSPS_含实验文档_20260603.zip",
            "doc": BEFORE / "project_output" / "实验文档" / "实验指导书_ADC1采样DAC1可调采样率回放_默认4kSPS.docx",
            "source": BEFORE / "老板交付_ADC1采样DAC1可调采样率回放_默认4kSPS_20260602",
            "top": "源码工程/rtl/dac_adc1_loopback_top.v",
            "ctrl": "源码工程/rtl/dac_adc1_loopback_ctrl.v",
            "i2c": "源码工程/rtl/i2c_byte_master.v",
            "xdc": "源码工程/xdc/dac_adc1_loopback_top.xdc",
            "readme": "源码工程/00_老板先看这个.md",
        },
        {
            "function": "ADC1采样_DAC1固定10Hz回放",
            "zip": BEFORE / "zip" / "ADC1采样_DAC1固定10Hz回放实验_含实验文档_20260602.zip",
            "doc": BEFORE / "project_output" / "实验文档" / "实验指导书_ADC1采样DAC1回放固定10Hz.docx",
            "source": BEFORE / "dac_adc1_loopback_10hz",
            "top": "源码工程/rtl/dac_adc1_loopback_top.v",
            "ctrl": "源码工程/rtl/dac_adc1_loopback_ctrl.v",
            "i2c": "源码工程/rtl/i2c_byte_master.v",
            "xdc": "源码工程/xdc/dac_adc1_loopback_top.xdc",
            "readme": "源码工程/README.md",
        },
        {
            "function": "AT21CS01单总线EEPROM暖复位读写",
            "zip": BEFORE / "zip" / "AT21CS01单总线EEPROM读写暖复位实验_含实验文档_20260602.zip",
            "doc": BEFORE / "project_output" / "实验文档" / "实验指导书_AT21CS01单总线EEPROM读写暖复位.docx",
            "source": OLD_ARCHIVE / "02_工程文件_可继续开发" / "当前可用工程" / "xillin",
            "fallback_source": BEFORE / "eeprom_rw",
            "top": "源码工程/rtl/eeprom_rw_top.v",
            "ctrl": "源码工程/rtl/at21cs01_master.v",
            "i2c": "",
            "xdc": "源码工程/xdc/eeprom_rw_top.xdc",
            "readme": "源码工程/README.md",
        },
    ]

    for item in final_items:
        function = item["function"]
        folder = ROOT / "最终交付包" / function
        send_dir = ROOT / "老板可直接发送的最终压缩包"
        zip_dst = folder / "最终压缩包" / item["zip"].name
        doc_dst = folder / "实验文档" / item["doc"].name
        copy_file(item["zip"], zip_dst, rows, "最终压缩包", function)
        copy_file(item["zip"], send_dir / item["zip"].name, rows, "老板可直接发送", function)
        copy_file(item["doc"], doc_dst, rows, "实验文档", function)

        src = item["source"]
        if not src.exists() and item.get("fallback_source"):
            src = item["fallback_source"]
        copy_selected_tree(src, folder / "源码工程", rows, function)

        for category, key in [
            ("顶层代码", "top"),
            ("控制代码", "ctrl"),
            ("I2C代码", "i2c"),
            ("约束文件", "xdc"),
            ("说明文件", "readme"),
        ]:
            rel = item.get(key, "")
            if not rel:
                continue
            p = folder / rel
            rows.append({
                "功能": function,
                "类别": category,
                "文件": p.name,
                "位置": str(p),
                "来源": "功能目录内快速入口",
                "状态": "存在" if p.exists() else "缺失",
            })

    # Shared references.
    for src in [
        BEFORE / "ADC" / "0178A2918E7353AF817F6876A456B20F.png",
        BEFORE / "ADC" / "FB27DA63CCC6BA9C819BC4ADEA17B9AC.png",
        BEFORE / "ADC" / "3C3A72DA4461A004095EE239D0A91E30.png",
    ]:
        copy_file(src, ROOT / "公共资料" / "原理图图片" / src.name, rows, "公共资料", "原理图")

    for src in [
        BEFORE / "datasheets" / "AT21CS01_AT21CS11_DS20005857.pdf",
        BEFORE / "material" / "ETL4-7A35T XILINX ARTIX-7 FPGA入门级学习板实验指导手册.pdf",
    ]:
        copy_file(src, ROOT / "公共资料" / "数据手册" / src.name, rows, "公共资料", "数据手册")

    # AI and handoff records.
    ai_sources = [
        BEFORE / "I2C_ADC采样率理论分析_20260602.md",
        BEFORE / "ADC" / "ADC_handoff_20260529.md",
        BEFORE / "ADC" / "ADC工程拆分交接记录_20260529.md",
        BEFORE / "project_output" / "实验文档" / "实验教学文档重写SOP_20260529.md",
    ]
    for src in ai_sources:
        copy_file(src, ROOT / "AI协作记录" / src.name, rows, "AI协作记录", "交接经验")

    # Historical useful functional packages without numeric prefixes.
    history_zips = [
        "DAC1_10Hz正弦波输出工程_20260529.zip",
        "DAC1_10Hz三角波输出_ADC1采样ILA观察工程_20260529.zip",
        "ADC1采样_DAC1稳定回放_10Hz示波器对比工程_20260530.zip",
        "EEPROM单总线读写_AT21CS01协议修正版_D0成功D1失败_20260601.zip",
        "EEPROM单总线读写_AT21CS01暖复位修正版_D0成功D1失败_20260602.zip",
    ]
    for name in history_zips:
        src = BEFORE / "zip" / name
        copy_file(src, ROOT / "历史参考包" / name, rows, "历史参考包", "历史版本")

    # Tools.
    tool_sources = [
        BEFORE / "hex_to_coe.py",
        BEFORE / "logo_to_rom.py",
        BEFORE / "vivado_tcl_cheatsheet.txt",
    ]
    for src in tool_sources:
        copy_file(src, ROOT / "工具脚本" / src.name, rows, "工具脚本", "工具")

    manifest = ROOT / "交付物对应关系.csv"
    with manifest.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["功能", "类别", "文件", "位置", "来源", "状态"])
        writer.writeheader()
        writer.writerows(rows)

    write_readme(rows)
    print(ROOT / "快速查找索引.md")
    print(manifest)


if __name__ == "__main__":
    main()
