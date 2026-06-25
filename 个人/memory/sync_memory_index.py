#!/usr/bin/env python3
"""
MEMORY.md 自动同步脚本
扫描所有memory目录 → 提取可索引内容 → 对比MEMORY.md → 输出差异报告 → 可选自动修复

用法:
  python sync_memory_index.py              # dry-run: 只输出报告
  python sync_memory_index.py --apply      # 实际修复MEMORY.md
  python sync_memory_index.py --workspace E:\\ai产出文件\\牛马\\个人\\个人  # 指定工作区根目录
"""

import argparse
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional


# ─── 配置 ───────────────────────────────────────────────────────

DEFAULT_WORKSPACE = Path(r"E:\ai产出文件\牛马\个人\个人")
ARCHIVE_DIR = Path(r"E:\ai产出文件\归档\memory")
DATE_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")
SKIP_FILES = {"MEMORY.md", "long-term.md", "sync_memory_index.py"}

# ─── 数据结构 ────────────────────────────────────────────────────

class DailyFile:
    """解析后的每日memory文件"""
    def __init__(self, path: Path, date: str):
        self.path = path
        self.date = date
        self.is_session = False  # 是否为会话记录（vs 自动报告）
        self.title_summary = ""  # 从H2标题提取的摘要
        self.completed_tasks: list[str] = []  # ✅标记的任务
        self.lessons: list[tuple[str, str]] = []  # (emoji_type, text)
        self.pattern_keys: list[tuple[str, str]] = []  # (key, meaning)
        self.relative_path = ""  # 相对于memory/目录的路径
        self.source_type = "workspace"  # workspace / project / career-breakthrough


def parse_daily_file(path: Path, date: str) -> DailyFile:
    """解析单个daily memory文件，提取可索引内容"""
    df = DailyFile(path, date)
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return df

    lines = content.split("\n")

    # 检测是否为会话记录
    for line in lines[:5]:
        if line.startswith("# ") and "会话记录" in line:
            df.is_session = True
            break

    # 提取H2标题作为摘要候选
    h2_titles = []
    for line in lines:
        if line.startswith("## ") and not line.startswith("### "):
            title = line[3:].strip()
            # 跳过通用标题
            if title not in ("任务执行", "完成事项", "待办", "用户反馈", "教训与改进"):
                h2_titles.append(title)

    # 提取第一个有意义的H3标题或✅任务作为摘要
    for line in lines:
        # H3标题（如 "### 1. 安装 Kami skill ✅"）
        m = re.match(r"^###\s+\d+\.\s+(.+?)\s*[✅⬜⚠️]", line)
        if m:
            df.title_summary = m.group(1).strip()
            break
        # ✅行
        m2 = re.match(r"^[-*]\s+✅\s*(.+)", line)
        if m2:
            df.title_summary = m2.group(1).strip()[:60]
            break

    # 如果没有好的摘要，用第一个非通用H2
    if not df.title_summary and h2_titles:
        df.title_summary = h2_titles[0][:60]

    # 提取已完成任务
    for line in lines:
        if "✅" in line and line.strip().startswith(("-", "*", "###")):
            task = re.sub(r"^[-*]\s*✅\s*", "", line.strip())
            task = re.sub(r"^###\s*\d+\.\s*", "", task)
            task = task.replace("✅", "").strip()
            if task and len(task) > 3:
                df.completed_tasks.append(task[:80])

    # 提取教训/经验/里程碑（emoji标记行）
    for line in lines:
        for emoji, ltype in [("🔴", "教训"), ("🟡", "经验"), ("🟢", "里程碑")]:
            if emoji in line:
                text = line.strip().lstrip("-* ").strip()
                text = re.sub(r"^\*\*.*?\*\*[:\s]*", "", text)  # 去掉粗体前缀
                if len(text) > 5:
                    df.lessons.append((ltype, text[:120]))

    # 提取Pattern-Key
    in_pk_section = False
    for line in lines:
        if "Pattern-Key" in line and "速查" in line:
            in_pk_section = True
            continue
        if in_pk_section and line.startswith("## "):
            break
        if in_pk_section and "|" in line and "`" in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                key = parts[0].strip("`")
                meaning = parts[1].strip()
                if "." in key:
                    df.pattern_keys.append((key, meaning))

    return df


def discover_memory_files(workspace: Path) -> list[DailyFile]:
    """扫描所有memory目录，发现并解析daily files"""
    results = []

    # 1. workspace-level memory/
    memory_dir = workspace / "memory"
    if memory_dir.is_dir():
        for f in memory_dir.iterdir():
            if f.is_file() and f.suffix == ".md" and f.name not in SKIP_FILES:
                m = DATE_PATTERN.match(f.name)
                if m:
                    df = parse_daily_file(f, m.group(1))
                    df.relative_path = f.name
                    df.source_type = "workspace"
                    results.append(df)

    # 2. projects/*/memory/
    projects_dir = workspace / "projects"
    if projects_dir.is_dir():
        for proj in projects_dir.iterdir():
            if not proj.is_dir():
                continue
            mem = proj / "memory"
            if not mem.is_dir():
                continue
            for f in mem.iterdir():
                if f.is_file() and f.suffix == ".md" and f.name not in SKIP_FILES:
                    m = DATE_PATTERN.match(f.name)
                    if m:
                        df = parse_daily_file(f, m.group(1))
                        proj_name = proj.name
                        df.relative_path = f"../projects/{proj_name}/memory/{f.name}"
                        df.source_type = "project"
                        results.append(df)

    # 3. career-breakthrough/memory/
    cb_mem = workspace / "career-breakthrough" / "memory"
    if cb_mem.is_dir():
        for f in cb_mem.iterdir():
            if f.is_file() and f.suffix == ".md" and f.name not in SKIP_FILES:
                m = DATE_PATTERN.match(f.name)
                if m:
                    df = parse_daily_file(f, m.group(1))
                    df.relative_path = f"../career-breakthrough/memory/{f.name}"
                    df.source_type = "career-breakthrough"
                    results.append(df)

    return sorted(results, key=lambda x: x.date)


# ─── MEMORY.md 解析 ──────────────────────────────────────────────

def parse_memory_md(memory_path: Path) -> dict:
    """解析MEMORY.md，提取已有的索引信息"""
    result = {
        "exists": memory_path.exists(),
        "date_sections": set(),  # 已有的日期段
        "file_listing": set(),  # 记忆文件列表中的文件名
        "lessons_dates": set(),  # 跨项目教训表中的日期
        "pattern_keys": set(),  # 已有的Pattern-Key
        "raw_content": "",
    }

    if not memory_path.exists():
        return result

    content = memory_path.read_text(encoding="utf-8")
    result["raw_content"] = content

    # 提取日期段标题
    for m in re.finditer(r"^## (\d{4}-\d{2}-\d{2})（", content, re.MULTILINE):
        result["date_sections"].add(m.group(1))

    # 提取记忆文件列表
    for m in re.finditer(r"\|\s*`(\d{4}-\d{2}-\d{2}\.md)`\s*\|", content):
        result["file_listing"].add(m.group(1))

    # 提取跨项目教训日期
    for m in re.finditer(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|", content):
        result["lessons_dates"].add(m.group(1))

    # 提取Pattern-Key
    for m in re.finditer(r"\|\s*`([^`]+\.[^`]+)`\s*\|\s*([^|]+)\|", content):
        key = m.group(1).strip()
        if "." in key and not key.startswith("memory/"):
            result["pattern_keys"].add(key)

    return result


# ─── 差异对比 ────────────────────────────────────────────────────

class DiffReport:
    """同步差异报告"""
    def __init__(self):
        self.missing_file_list: list[DailyFile] = []
        self.missing_date_sections: list[DailyFile] = []
        self.missing_lessons: list[tuple[str, str, str]] = []  # (date, type, text)
        self.missing_pattern_keys: list[tuple[str, str]] = []
        self.skipped_auto_reports: list[DailyFile] = []

    @property
    def total_fixes(self) -> int:
        real_file_missing = len([df for df in self.missing_file_list
                                 if df not in self.skipped_auto_reports])
        return (real_file_missing + len(self.missing_date_sections)
                + len(self.missing_lessons) + len(self.missing_pattern_keys))

    def print_report(self):
        print("\n" + "=" * 50)
        print("  MEMORY.md 同步报告")
        print("=" * 50)

        # A. 记忆文件列表
        real_missing = [df for df in self.missing_file_list if df not in self.skipped_auto_reports]
        print(f"\n[A] 记忆文件列表: {len(real_missing)}个缺失")
        for df in self.missing_file_list:
            if df in self.skipped_auto_reports:
                print(f"  ~ {df.date}.md  (自动报告，已跳过)")
            else:
                print(f"  + {df.date}.md  ({df.source_type}: {df.title_summary[:40]})")

        # B. 日期索引段
        print(f"\n[B] 日期索引段: {len(self.missing_date_sections)}个缺失")
        for df in self.missing_date_sections:
            print(f"  + ## {df.date}（{df.title_summary[:50]}）")
            print(f"    → 来源: {df.relative_path}")

        # C. 跨项目教训
        print(f"\n[C] 跨项目教训: {len(self.missing_lessons)}个缺失")
        for date, ltype, text in self.missing_lessons:
            emoji = {"教训": "🔴", "经验": "🟡", "里程碑": "🟢"}.get(ltype, "⚪")
            print(f"  + {emoji} {date} | {ltype} | {text[:60]}...")

        # D. Pattern-Key
        print(f"\n[D] Pattern-Key: {len(self.missing_pattern_keys)}个缺失")
        for key, meaning in self.missing_pattern_keys:
            print(f"  + `{key}` | {meaning[:50]}")

        print(f"\n{'=' * 50}")
        if self.total_fixes > 0:
            print(f"  共 {self.total_fixes} 项需要修复")
            print(f"  运行 --apply 自动修复")
        else:
            print("  ✅ MEMORY.md 与实际文件完全同步，无需修复")
        print("=" * 50 + "\n")


def compute_diff(daily_files: list[DailyFile], memory_info: dict) -> DiffReport:
    """对比实际文件与MEMORY.md，计算差异"""
    report = DiffReport()

    # 同一天多个来源时，workspace优先；同类型保留第一个
    seen_dates = set()
    deduplicated = []
    for df in daily_files:
        if df.date not in seen_dates or df.source_type == "workspace":
            deduplicated.append(df)
            seen_dates.add(df.date)

    for df in deduplicated:
        # A. 记忆文件列表检查（只检查workspace级文件，项目级不进文件列表）
        if df.source_type == "workspace" and df.date + ".md" not in memory_info["file_listing"]:
            report.missing_file_list.append(df)
            if not df.is_session:
                report.skipped_auto_reports.append(df)

        # B. 日期索引段检查（只索引会话记录，跳过自动报告）
        if df.date not in memory_info["date_sections"]:
            if df.is_session:  # 只有会话记录才生成索引段
                report.missing_date_sections.append(df)

        # C. 跨项目教训检查（项目级文件中的emoji教训）
        if df.source_type == "project" and df.lessons:
            for ltype, text in df.lessons:
                # 去掉emoji前缀后检查文本是否已在MEMORY.md中出现
                clean_text = re.sub(r"^[🔴🟡🟢⚪]\s*", "", text).strip()
                text_snippet = clean_text[:30]
                if text_snippet and text_snippet not in memory_info["raw_content"]:
                    report.missing_lessons.append((df.date, ltype, clean_text))

        # D. Pattern-Key检查
        for pk_key, pk_meaning in df.pattern_keys:
            if pk_key not in memory_info["pattern_keys"]:
                report.missing_pattern_keys.append((pk_key, pk_meaning))

    return report


# ─── 修复逻辑 ────────────────────────────────────────────────────

def backup_memory(memory_path: Path):
    """备份MEMORY.md到归档目录"""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = ARCHIVE_DIR / f"MEMORY.md.{timestamp}.bak"
    shutil.copy2(memory_path, backup_path)
    print(f"  📦 备份: {backup_path}")
    return backup_path


def apply_fixes(memory_path: Path, report: DiffReport, daily_files: list[DailyFile]):
    """实际修复MEMORY.md"""
    if not memory_path.exists():
        print("  ❌ MEMORY.md 不存在，无法修复")
        return

    # 备份
    backup_memory(memory_path)

    content = memory_path.read_text(encoding="utf-8")
    original_content = content
    insertions = []

    # ── A. 修复记忆文件列表 ──
    # 找到记忆文件列表表格的末尾，在最后一行后插入
    file_list_insert = []
    real_missing = [df for df in report.missing_file_list
                    if df not in report.skipped_auto_reports]
    for df in real_missing:
        # 生成描述
        desc = df.title_summary[:50] if df.title_summary else "待索引"
        row = f"| `{df.date}.md` | {df.date} {desc} |"
        file_list_insert.append(row)

    if file_list_insert:
        # 找到记忆文件列表表格的最后一行（紧跟表格行，不跳过空行）
        lines = content.split("\n")
        insert_idx = None
        in_file_list = False
        last_table_row = None
        for i, line in enumerate(lines):
            if "## 记忆文件列表" in line:
                in_file_list = True
                continue
            if in_file_list and line.startswith("## "):
                break
            if in_file_list and line.startswith("| `") and ".md`" in line:
                last_table_row = i
        if last_table_row is not None:
            insert_idx = last_table_row + 1

        if insert_idx is not None:
            for j, row in enumerate(file_list_insert):
                lines.insert(insert_idx + j, row)
            content = "\n".join(lines)

    # ── B. 修复日期索引段 ──
    # 在"## 关键 Pattern-Key 速查"之前插入新的日期段
    date_insert_lines = []
    for df in report.missing_date_sections:
        summary = df.title_summary[:50] if df.title_summary else "会话记录"
        section = f"\n## {df.date}（{summary}）\n\n"

        # 从daily file提取关键内容作为索引
        if df.completed_tasks:
            for task in df.completed_tasks[:3]:
                section += f"- {task}\n"
        elif df.lessons:
            for ltype, text in df.lessons[:2]:
                emoji = {"教训": "🔴", "经验": "🟡", "里程碑": "🟢"}.get(ltype, "⚪")
                section += f"- {emoji} {text[:80]}\n"
        else:
            section += f"- [{df.date} 完整记录]({df.relative_path})\n"

        date_insert_lines.append(section)

    if date_insert_lines:
        # 在 "## 关键 Pattern-Key" 或 "## 跨项目" 之前插入
        anchor = "## 关键 Pattern-Key 速查"
        if anchor not in content:
            anchor = "## 跨项目 Memory 索引"
        if anchor not in content:
            anchor = "## 记忆架构的认知科学原理"

        if anchor in content:
            insert_text = "\n".join(date_insert_lines)
            content = content.replace(anchor, insert_text + "\n" + anchor)

    # ── C. 修复跨项目教训 ──
    if report.missing_lessons:
        # 找到跨项目教训汇总表的最后一行
        lessons_insert = []
        for date, ltype, text in report.missing_lessons:
            emoji = {"教训": "🔴", "经验": "🟡", "里程碑": "🟢"}.get(ltype, "⚪")
            row = f"| {date} | {emoji} {ltype} | 跨项目 | {text[:80]} | 待补充 |"
            lessons_insert.append(row)

        lines = content.split("\n")
        insert_idx = None
        in_lessons_table = False
        for i, line in enumerate(lines):
            if "跨项目教训汇总" in line:
                in_lessons_table = True
                continue
            if in_lessons_table and line.startswith("## "):
                insert_idx = i
                break
            if in_lessons_table and line.startswith("| 20") and "|" in line:
                insert_idx = i + 1

        if insert_idx is not None:
            for j, row in enumerate(lessons_insert):
                lines.insert(insert_idx + j, row)
            content = "\n".join(lines)

    # ── D. 修复Pattern-Key ──
    if report.missing_pattern_keys:
        pk_insert = []
        for key, meaning in report.missing_pattern_keys:
            row = f"| `{key}` | {meaning[:50]} | 自动同步 |"
            pk_insert.append(row)

        lines = content.split("\n")
        insert_idx = None
        in_pk_table = False
        for i, line in enumerate(lines):
            if "关键 Pattern-Key 速查" in line:
                in_pk_table = True
                continue
            if in_pk_table and line.startswith("## "):
                insert_idx = i
                break
            if in_pk_table and line.startswith("| `") and "." in line:
                insert_idx = i + 1

        if insert_idx is not None:
            for j, row in enumerate(pk_insert):
                lines.insert(insert_idx + j, row)
            content = "\n".join(lines)

    # ── 写入 ──
    if content != original_content:
        memory_path.write_text(content, encoding="utf-8")
        print(f"  ✅ MEMORY.md 已更新 ({len(original_content)} → {len(content)} bytes)")
    else:
        print("  ℹ️  无变更（所有内容已同步）")


# ─── 主流程 ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="MEMORY.md 自动同步脚本")
    parser.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE,
                        help="工作区根目录")
    parser.add_argument("--apply", action="store_true",
                        help="实际修复MEMORY.md（默认只输出报告）")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    memory_path = workspace / "memory" / "MEMORY.md"

    print(f"\n🔍 扫描工作区: {workspace}")
    print(f"📄 目标文件: {memory_path}")

    # Step 1: 发现
    daily_files = discover_memory_files(workspace)
    print(f"\n📁 发现 {len(daily_files)} 个daily memory文件:")
    for df in daily_files:
        tag = "📋会话" if df.is_session else "📊报告"
        print(f"  {tag} {df.date}.md ({df.source_type}: {df.path.parent.name}/)")

    # Step 2: 解析MEMORY.md
    memory_info = parse_memory_md(memory_path)
    print(f"\n📊 MEMORY.md 状态:")
    print(f"  日期段: {len(memory_info['date_sections'])}个")
    print(f"  文件列表: {len(memory_info['file_listing'])}个")
    print(f"  Pattern-Key: {len(memory_info['pattern_keys'])}个")

    # Step 3: 对比
    report = compute_diff(daily_files, memory_info)
    report.print_report()

    # Step 4: 修复
    if args.apply and report.total_fixes > 0:
        print("\n🔧 执行修复...")
        apply_fixes(memory_path, report, daily_files)
    elif args.apply and report.total_fixes == 0:
        print("\n✅ 无需修复")
    else:
        if report.total_fixes > 0:
            print("💡 提示: 运行 `python sync_memory_index.py --apply` 执行修复")


if __name__ == "__main__":
    main()
