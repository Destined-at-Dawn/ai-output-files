#!/usr/bin/env python3
"""
Context Compression Kit — 一键安装脚本
======================================
用法：在你的 Claude Code 项目根目录下运行
    python install.py [--dir /path/to/your/project]

功能：
1. 创建 .claude/hooks/ 目录
2. 复制 hook 脚本
3. 合并 settings.json（不覆盖已有配置）
4. 复制 context-essentials.md
5. 提示手动添加 CLAUDE.md 片段
"""

import json
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime


# === 颜色输出 ===
def green(text):
    return f"\033[92m{text}\033[0m"

def yellow(text):
    return f"\033[93m{text}\033[0m"

def red(text):
    return f"\033[91m{text}\033[0m"

def bold(text):
    return f"\033[1m{text}\033[0m"


def find_project_dir():
    """查找 Claude Code 项目根目录（包含 CLAUDE.md 或 .claude/ 的目录）"""
    # 优先使用命令行参数
    if "--dir" in sys.argv:
        idx = sys.argv.index("--dir")
        if idx + 1 < len(sys.argv):
            return Path(sys.argv[idx + 1])

    # 从当前目录向上查找
    cwd = Path.cwd()
    for d in [cwd] + list(cwd.parents):
        if (d / "CLAUDE.md").exists() or (d / ".claude").is_dir():
            return d

    # 没找到就用当前目录
    return cwd


def merge_settings(settings_path, hooks_config):
    """合并 hooks 配置到 settings.json（不覆盖已有配置）"""
    existing = {}
    if settings_path.exists():
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, IOError):
            print(yellow(f"  Warning: {settings_path} 存在但无法解析，将创建新文件"))

    if "hooks" not in existing:
        existing["hooks"] = {}

    # 合并：只添加 compact 相关的 hook（不覆盖已有的）
    added = []
    skipped = []
    for event_name, event_config in hooks_config.items():
        if event_name in existing["hooks"]:
            skipped.append(event_name)
        else:
            existing["hooks"][event_name] = event_config
            added.append(event_name)

    return existing, added, skipped


def backup_file(filepath):
    """备份文件到同目录的 .bak 文件"""
    if filepath.exists():
        backup_path = filepath.with_suffix(filepath.suffix + ".bak")
        shutil.copy2(filepath, backup_path)
        return backup_path
    return None


def main():
    print(bold("=" * 60))
    print(bold("  Context Compression Kit — 安装程序"))
    print(bold("=" * 60))
    print()

    # 1. 定位项目目录
    project_dir = find_project_dir()
    claude_md = project_dir / "CLAUDE.md"
    claude_dir = project_dir / ".claude"
    hooks_dir = claude_dir / "hooks"
    settings_path = claude_dir / "settings.json"
    checkpoint_path = claude_dir / "session-checkpoint.md"
    essentials_path = claude_dir / "context-essentials.md"

    print(f"项目目录: {bold(str(project_dir))}")
    print(f"CLAUDE.md: {'存在' if claude_md.exists() else '不存在'}")
    print(f".claude/: {'存在' if claude_dir.exists() else '不存在'}")
    print()

    # 确认
    response = input("在此目录安装？(Y/n): ").strip().lower()
    if response and response != "y":
        print("已取消。用 --dir 参数指定其他目录。")
        return

    # 2. 创建目录
    print("\n[1/5] 创建 hooks 目录...")
    hooks_dir.mkdir(parents=True, exist_ok=True)
    print(green(f"  OK: {hooks_dir}"))

    # 3. 复制 hook 脚本
    print("\n[2/5] 复制 hook 脚本...")
    kit_dir = Path(__file__).parent
    scripts = [
        ("hooks/pre-compact.py", "PreCompact hook (压缩前检查点)"),
        ("hooks/on-compact.py", "SessionStart hook (压缩后恢复)"),
    ]
    for src_rel, desc in scripts:
        src = kit_dir / src_rel
        dst = hooks_dir / Path(src_rel).name
        if not src.exists():
            print(red(f"  MISSING: {src}"))
            continue
        shutil.copy2(src, dst)
        print(green(f"  OK: {dst.name} ({desc})"))

    # 4. 合并 settings.json
    print("\n[3/5] 合并 settings.json...")
    hooks_template = kit_dir / "templates" / "settings-hooks.json"
    if hooks_template.exists():
        with open(hooks_template, "r", encoding="utf-8") as f:
            hooks_config = json.load(f)

        # 备份已有 settings.json
        backup = backup_file(settings_path)
        if backup:
            print(yellow(f"  已备份: {backup}"))

        merged, added, skipped = merge_settings(settings_path, hooks_config)

        settings_path.parent.mkdir(parents=True, exist_ok=True)
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)

        for event in added:
            print(green(f"  + 已添加: {event}"))
        for event in skipped:
            print(yellow(f"  ~ 已存在（跳过）: {event}"))
    else:
        print(red(f"  MISSING: {hooks_template}"))

    # 5. 复制 context-essentials.md
    print("\n[4/5] 复制 context-essentials.md...")
    essentials_src = kit_dir / "templates" / "context-essentials.md"
    if essentials_src.exists():
        shutil.copy2(essentials_src, essentials_path)
        print(green(f"  OK: {essentials_path}"))
    else:
        print(red(f"  MISSING: {essentials_src}"))

    # 6. 创建空检查点文件
    if not checkpoint_path.exists():
        with open(checkpoint_path, "w", encoding="utf-8") as f:
            f.write("# Session Checkpoint\n\n> Created by Context Compression Kit installer\n")
        print(green(f"  OK: {checkpoint_path} (空模板)"))

    # 7. 提示 CLAUDE.md 修改
    print("\n[5/5] CLAUDE.md 修改（需手动）")
    snippet_path = kit_dir / "CLAUDE-compact-snippet.md"
    print(yellow(f"""
  需要手动将以下文件的内容追加到你的 CLAUDE.md 末尾：

    {snippet_path}

  内容包括：
    - Hook 防御链说明
    - 主动压缩策略
    - Compact Instructions（保护清单：压缩时保留什么、丢弃什么）
"""))

    # 完成
    print(bold("=" * 60))
    print(green(bold("  安装完成！")))
    print(bold("=" * 60))
    print(f"""
  已安装的文件：
    {hooks_dir / 'pre-compact.py'}
    {hooks_dir / 'on-compact.py'}
    {settings_path}
    {essentials_path}

  待手动完成：
    1. 将 CLAUDE-compact-snippet.md 追加到你的 CLAUDE.md
    2. 重启 Claude Code 会话（hooks 在下次会话生效）

  工作原理：
    压缩前 → PreCompact hook 自动写检查点到 session-checkpoint.md
    压缩后 → SessionStart(compact) hook 自动读检查点 + 注入恢复上下文
    CLAUDE.md 重新加载 → 铁律和保护清单存活

  测试：
    1. 在 Claude Code 中进行一段对话
    2. 输入 /compact 手动触发压缩
    3. 检查 .claude/session-checkpoint.md 是否被写入
    4. 压缩后 Claude 应自动引用检查点内容
""")


if __name__ == "__main__":
    main()
