#!/usr/bin/env python3
"""技能版本自动同步脚本 — 改 SKILL.md 后一键同步所有引用方的版本号

用法：
  python skill-version-sync.py self-improving          # 报告模式：列出所有不一致
  python skill-version-sync.py self-improving --fix     # 修复模式：自动更新配置文件
  python skill-version-sync.py --all                    # 扫描所有已注册技能
  python skill-version-sync.py --all --fix              # 修复所有不一致

设计原则：
  - 权威版本源 = SKILL.md 文件头部的 version 字段
  - 只更新「配置文件」（路由表/引用表/注册表），不改「历史记录」（教训/记忆/变更日志）
  - 用 Python os + re，不用 PowerShell（中文路径安全）
  - 遵循 SOP-18 Phase 5（配置同步）+ Phase 7（验证）

来源：2026-06-07 用户指出"技能注册表 §一 v3.1 vs §二 v3.2 vs CLAUDE.md v3.0"版本不一致
"""

import os
import re
import sys
from pathlib import Path

# === UTF-8 输出 ===
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# === 路径配置 ===
ROOT_WORKSPACE = r"E:\ai产出文件\牛马\创作\创作"
NEWMAX_SKILLS = r"C:\Users\13975\.newmax\skills"
LOCAL_SKILLS = os.path.join(ROOT_WORKSPACE, "skills")

# === 技能注册表（技能名 → SKILL.md 所在位置） ===
SKILL_LOCATIONS = {
    "self-improving": os.path.join(NEWMAX_SKILLS, "self-improving", "SKILL.md"),
    "post-task-audit": os.path.join(NEWMAX_SKILLS, "post-task-audit", "SKILL.md"),
    "li-manage": os.path.join(NEWMAX_SKILLS, "li-manage", "SKILL.md"),
    "li-bestskill": os.path.join(NEWMAX_SKILLS, "li-bestskill", "SKILL.md"),
    "li-skillfusion": os.path.join(NEWMAX_SKILLS, "li-skillfusion", "SKILL.md"),
    "experience-sync": os.path.join(LOCAL_SKILLS, "experience-sync", "SKILL.md"),
}

# === 历史文件黑名单（这些文件记录的是"当时发生了什么"，版本号不该被自动更新） ===
HISTORY_PATTERNS = [
    r"memory\\",
    r"memory/",
    r"教训",
    r"negative-results",
    r"lessons\.md",
    r"经验库\\做得",
    r"变更记录",
    r"迭代日志",
    r"归档",
    r"outputs\\CASE-",
    r"outputs/OPC",
    r"evolution-calendar",
    r"自我进化\\",
]

# === 配置文件白名单（这些文件必须反映当前版本） ===
CONFIG_PATTERNS = [
    r"CLAUDE\.md$",
    r"CLAUDE-",
    r"技能注册表",
    r"技能PK机制",
    r"Skill路由系统",
    r"Skill链式调用",
    r"技能库",
    r"SOP总索引",
    r"06_系统管理",
    r"经验库\\INDEX",
    r"经验库/INDEX",
    r"RULES-INDEX",
    r"SKILL\.md$",
]


def extract_version_from_skill(skill_path: str) -> str | None:
    """从 SKILL.md 文件头部提取权威版本号

    支持的格式：
    - YAML frontmatter: version: 3.3.0 / version: "3.2"
    - Markdown: > **版本：** v3.2
    - Markdown: **version**: v1.0
    - Semver 三段: 3.3.0 → v3.3（只取前两段，保持和其他引用一致）
    """
    if not os.path.exists(skill_path):
        return None

    with open(skill_path, "r", encoding="utf-8") as f:
        # 只读前50行（YAML frontmatter 可能在 20+ 行）
        head = []
        for i, line in enumerate(f):
            head.append(line)
            if i >= 50:
                break

    head_text = "".join(head)

    # 匹配多种版本格式（优先级从高到低）
    patterns = [
        # YAML frontmatter: version: 3.3.0 / version: "3.2" / version: 3.2.0
        r'(?m)^version[：:\s]+["\']?[Vv]?(\d+\.\d+(?:\.\d+)?)["\']?\s*$',
        # Markdown 行内: > **版本：** v3.2 / 版本: v3.2
        r'[Vv]ersion[：:]\s*[Vv]?(\d+\.\d+(?:\.\d+)?)',
        # 简写: V：3.2 / v: 1.0
        r'[Vv][：:]\s*[Vv]?(\d+\.\d+(?:\.\d+)?)',
    ]

    for pat in patterns:
        m = re.search(pat, head_text)
        if m:
            raw_ver = m.group(1)
            # Semver 三段 → 两段（3.3.0 → v3.3），保持和引用方一致
            parts = raw_ver.split('.')
            if len(parts) >= 3:
                return f"v{parts[0]}.{parts[1]}"
            return f"v{raw_ver}"

    return None


def is_history_file(filepath: str) -> bool:
    """判断是否为历史记录文件（不应被自动修改）"""
    normalized = filepath.replace("/", "\\")
    for pat in HISTORY_PATTERNS:
        if re.search(pat, normalized, re.IGNORECASE):
            return True
    return False


def is_config_file(filepath: str) -> bool:
    """判断是否为配置文件（应该反映当前版本）"""
    normalized = filepath.replace("/", "\\")
    for pat in CONFIG_PATTERNS:
        if re.search(pat, normalized, re.IGNORECASE):
            return True
    return False


def grep_version_refs(skill_name: str, search_root: str) -> list[dict]:
    """搜索所有引用该 skill 版本的文件

    匹配模式：{skill_name} v{X.Y}
    返回：[{file, line_no, line_text, matched_version}]
    """
    results = []
    # 匹配 skill名 vX.Y 的模式
    pattern = re.compile(
        re.escape(skill_name) + r'\s+v(\d+\.\d+)',
        re.IGNORECASE
    )

    for root, dirs, files in os.walk(search_root):
        # 跳过 .git 和 __pycache__
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules', '.Codex')]

        for fname in files:
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    for line_no, line in enumerate(f, 1):
                        m = pattern.search(line)
                        if m:
                            results.append({
                                'file': fpath,
                                'line_no': line_no,
                                'line_text': line.rstrip(),
                                'matched_version': f"v{m.group(1)}",
                            })
            except (UnicodeDecodeError, PermissionError):
                continue

    return results


def update_version_in_file(filepath: str, skill_name: str, old_version: str,
                           new_version: str, dry_run: bool = True) -> bool:
    """更新文件中的版本号

    Args:
        filepath: 文件路径
        skill_name: 技能名
        old_version: 旧版本号（如 v3.0）
        new_version: 新版本号（如 v3.2）
        dry_run: True=只打印不修改，False=实际修改

    Returns:
        True if changes were made (or would be made in dry_run)
    """
    pattern = re.compile(
        re.escape(skill_name) + r'\s+' + re.escape(old_version),
        re.IGNORECASE
    )

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError, FileNotFoundError):
        return False

    new_content = pattern.sub(f"{skill_name} {new_version}", content)

    if new_content == content:
        return False

    if not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return True


def scan_skill(skill_name: str, fix: bool = False) -> dict:
    """扫描单个技能的版本一致性

    Returns:
        {
            'skill': str,
            'authoritative_version': str | None,
            'skill_path': str,
            'total_refs': int,
            'consistent': int,
            'inconsistent': [{'file', 'line_no', 'current_ver', 'expected_ver', 'is_history'}],
            'fixed': int (only in fix mode),
        }
    """
    result = {
        'skill': skill_name,
        'authoritative_version': None,
        'skill_path': '',
        'total_refs': 0,
        'consistent': 0,
        'inconsistent': [],
        'fixed': 0,
    }

    # 1. 找到 SKILL.md 并提取权威版本
    skill_path = SKILL_LOCATIONS.get(skill_name)
    if not skill_path or not os.path.exists(skill_path):
        # 尝试在 local skills 目录找
        alt_path = os.path.join(LOCAL_SKILLS, skill_name, "SKILL.md")
        if os.path.exists(alt_path):
            skill_path = alt_path
        else:
            result['skill_path'] = f"NOT FOUND: {skill_path or alt_path}"
            return result

    result['skill_path'] = skill_path
    ver = extract_version_from_skill(skill_path)
    result['authoritative_version'] = ver

    if not ver:
        return result

    # 2. 搜索所有引用
    refs = grep_version_refs(skill_name, ROOT_WORKSPACE)
    # 也搜 .newmax/skills
    if os.path.exists(NEWMAX_SKILLS):
        refs += grep_version_refs(skill_name, NEWMAX_SKILLS)

    result['total_refs'] = len(refs)

    # 3. 检查一致性
    seen_files = set()
    for ref in refs:
        fpath = ref['file']
        if fpath in seen_files:
            continue  # 同一文件只检查一次
        seen_files.add(fpath)

        matched_ver = ref['matched_version']
        if matched_ver.lower() == ver.lower():
            result['consistent'] += 1
        else:
            is_hist = is_history_file(fpath)
            entry = {
                'file': fpath,
                'line_no': ref['line_no'],
                'current_ver': matched_ver,
                'expected_ver': ver,
                'is_history': is_hist,
            }
            result['inconsistent'].append(entry)

            # 修复模式：只修配置文件，不修历史文件
            if fix and not is_hist:
                success = update_version_in_file(
                    fpath, skill_name, matched_ver, ver, dry_run=False
                )
                if success:
                    result['fixed'] += 1

    return result


def scan_all_skills(fix: bool = False) -> list[dict]:
    """扫描所有已注册技能"""
    results = []
    for skill_name in SKILL_LOCATIONS:
        r = scan_skill(skill_name, fix=fix)
        if r['authoritative_version']:  # 只报告能找到版本号的
            results.append(r)
    return results


def print_report(results: list[dict]):
    """打印扫描报告"""
    print("=" * 70)
    print("  技能版本同步报告")
    print("=" * 70)

    total_inconsistent = 0
    total_fixed = 0

    for r in results:
        skill = r['skill']
        ver = r['authoritative_version'] or 'UNKNOWN'
        total = r['total_refs']
        consistent = r['consistent']
        inconsistent = len(r['inconsistent'])
        total_inconsistent += inconsistent
        total_fixed += r.get('fixed', 0)

        status = "✅" if inconsistent == 0 else "🔴"
        print(f"\n{status} {skill}（权威版本：{ver}）")
        print(f"   SKILL.md: {r['skill_path']}")
        print(f"   引用总数: {total} | 一致: {consistent} | 不一致: {inconsistent}")

        if r['inconsistent']:
            for entry in r['inconsistent']:
                fpath = entry['file']
                # 显示相对路径
                display_path = fpath.replace(ROOT_WORKSPACE, ".").replace(NEWMAX_SKILLS, "~/.newmax/skills")
                hist_mark = " [历史文件-跳过]" if entry['is_history'] else ""
                fix_mark = " [已修复]" if r.get('fixed', 0) > 0 and not entry['is_history'] else ""
                print(f"   🔴 {display_path}#{entry['line_no']}")
                print(f"      当前: {entry['current_ver']} → 应为: {entry['expected_ver']}{hist_mark}{fix_mark}")

    print("\n" + "=" * 70)
    print(f"  总计: {len(results)} 个技能 | 不一致引用: {total_inconsistent} | 已修复: {total_fixed}")
    print("=" * 70)

    if total_inconsistent > 0 and total_fixed == 0:
        print("\n💡 运行 --fix 自动修复配置文件中的版本不一致")
        print("   注意：历史文件（memory/教训/归档）不会被自动修改")
    elif total_inconsistent > total_fixed:
        remaining = total_inconsistent - total_fixed
        print(f"\n⚠️  {remaining} 处不一致来自历史文件（已跳过），这些不应被自动修改")


def main():
    args = sys.argv[1:]

    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        return

    fix = '--fix' in args
    args = [a for a in args if a != '--fix']

    if args[0] == '--all':
        results = scan_all_skills(fix=fix)
        print_report(results)
    else:
        skill_name = args[0]
        if skill_name not in SKILL_LOCATIONS:
            # 尝试模糊匹配
            matches = [s for s in SKILL_LOCATIONS if skill_name.lower() in s.lower()]
            if matches:
                print(f"未精确匹配 '{skill_name}'，找到近似: {', '.join(matches)}")
                print(f"使用: python {sys.argv[0]} {matches[0]}")
            else:
                print(f"未知技能: {skill_name}")
                print(f"已注册: {', '.join(SKILL_LOCATIONS.keys())}")
            return

        result = scan_skill(skill_name, fix=fix)
        print_report([result])


if __name__ == '__main__':
    main()
