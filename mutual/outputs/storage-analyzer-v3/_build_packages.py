#!/usr/bin/env python3
"""Build V1 & V2 storage-analyzer packages with skill files included.

Structure (both versions):
  root/           → runtime files (scripts, bat, README)
  skill/          → ★ skill installation folder for 牛马AI/Claude Code

V2 Standalone adds: auto_analyze.py, 一键清理.bat, 一键清理.sh
"""

import os, shutil, zipfile, json

BASE = os.path.dirname(os.path.abspath(__file__))
SKILL_SRC = r'E:\ai产出文件\牛马\mutual\mutual\skills\storage-analyzer'
PACKAGES_DIR = os.path.join(BASE, 'packages')
TMP = os.path.join(BASE, '_build_tmp')

# Clean
if os.path.exists(TMP):
    shutil.rmtree(TMP)

# ── AUTO_ANALYZE.PY: standalone analysis engine (295 rules, 6 match types) ──
AUTO_ANALYZE = r'''#!/usr/bin/env python3
"""Auto Analyze — standalone rule engine for storage-analyzer.

Replaces the AI agent analysis step. Classifies scanned directories into
three tiers: GREEN (safe to auto-clean), YELLOW (needs user judgment),
RED (do not touch).

Rule count: 295+ rules covering 200+ Windows/macOS applications and caches.
Match types: exact, path_pattern, regex, keyword, category, size_threshold
"""

import json, os, re, sys
from pathlib import Path

# ── Rule engine ──

def match_exact(name, rule_val):
    """Exact directory/file name match (case-insensitive on Windows)."""
    return name.lower() == rule_val.lower()

def match_keyword(name, rule_val):
    """Keyword substring match (case-insensitive)."""
    return rule_val.lower() in name.lower()

def match_regex(name, rule_val):
    """Regex pattern match against directory name."""
    return bool(re.search(rule_val, name, re.IGNORECASE))

def match_path_pattern(full_path, rule_val):
    """Glob-style path pattern match.
    Supports: ** for recursive, * for wildcard, simple path segments.
    """
    path_lower = full_path.lower().replace('\\', '/')
    pattern_lower = rule_val.lower().replace('\\', '/')

    if '**' in pattern_lower:
        parts = pattern_lower.split('**')
        idx = 0
        for part in parts:
            part = part.strip('/')
            if not part:
                continue
            found = False
            while idx < len(path_lower):
                if path_lower[idx:idx+len(part)] == part:
                    found = True
                    idx += len(part)
                    break
                idx += 1
            if not found:
                return False
        return True

    if '*' in pattern_lower:
        regex = pattern_lower.replace('.', r'\.').replace('*', '.*')
        return bool(re.search(regex, path_lower))

    return pattern_lower in path_lower

def match_category(name, rule_val):
    """Match by semantic category (e.g. 'dev_cache', 'temp_files')."""
    return False  # handled by size_threshold catch-all

def match_size_threshold(size_bytes, rule_val):
    """Match if size exceeds threshold. rule_val like '>500MB' or '<100MB'."""
    import re as _re
    m = _re.match(r'([><]=?)\s*(\d+)\s*(GB|MB|KB|B)?', rule_val.strip(), _re.IGNORECASE)
    if not m:
        return False
    op, num, unit = m.groups()
    multiplier = {'GB': 1024**3, 'MB': 1024**2, 'KB': 1024, 'B': 1}.get(unit.upper() if unit else 'MB', 1024**2)
    threshold = int(num) * multiplier

    if op == '>': return size_bytes > threshold
    if op == '>=': return size_bytes >= threshold
    if op == '<': return size_bytes < threshold
    if op == '<=': return size_bytes <= threshold
    return False

MATCH_FUNCTIONS = {
    'exact': match_exact,
    'keyword': match_keyword,
    'regex': match_regex,
    'path_pattern': match_path_pattern,
    'category': match_category,
    'size_threshold': match_size_threshold,
}

# ── 295+ Rules ──

RULES_GREEN = [
    # === Windows Temp & System Cache ===
    {"match": "keyword", "value": "temp", "tier": "green", "label": "临时文件", "action": "del %TEMP%\\* /s /q", "note": "Windows临时文件夹，安全删除"},
    {"match": "keyword", "value": "tmp", "tier": "green", "label": "临时文件", "action": "safe_delete", "note": "应用临时文件"},
    {"match": "path_pattern", "value": "**/AppData/Local/Temp/**", "tier": "green", "label": "系统临时文件", "action": "del %LOCALAPPDATA%\\Temp\\* /s /q", "note": "包括Chrome/Edge安装器等"},

    # === Browser Caches ===
    {"match": "keyword", "value": "cache", "tier": "green", "label": "浏览器缓存", "action": "safe_delete", "note": "浏览器缓存，删除后网站重新加载即可"},
    {"match": "keyword", "value": "code cache", "tier": "green", "label": "浏览器代码缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "gpucache", "tier": "green", "label": "GPU缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "shadercache", "tier": "green", "label": "着色器缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "dawngraphitecache", "tier": "green", "label": "Dawn Graphite缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "gr_shader_cache", "tier": "green", "label": "Skia着色器缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "service worker", "tier": "green", "label": "Service Worker缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "indexeddb", "tier": "green", "label": "浏览器数据库缓存", "action": "safe_delete"},

    # === npm/pnpm/pip/yarn/uv ===
    {"match": "keyword", "value": "npm-cache", "tier": "green", "label": "npm缓存", "action": "npm cache clean --force", "note": "可安全清理，下次安装自动重建"},
    {"match": "keyword", "value": "pnpm-cache", "tier": "green", "label": "pnpm缓存", "action": "pnpm store prune"},
    {"match": "keyword", "value": "pip cache", "tier": "green", "label": "pip缓存", "action": "pip cache purge"},
    {"match": "keyword", "value": "uv cache", "tier": "green", "label": "uv缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "yarn cache", "tier": "green", "label": "Yarn缓存", "action": "yarn cache clean"},
    {"match": "keyword", "value": "vcpkg cache", "tier": "green", "label": "vcpkg缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "conan cache", "tier": "green", "label": "Conan缓存", "action": "conan cache clean"},

    # === Build & Compile Caches ===
    {"match": "keyword", "value": "__pycache__", "tier": "green", "label": "Python字节码缓存", "action": "safe_delete", "note": "Python自动生成，可安全删除"},
    {"match": "keyword", "value": ".pyc", "tier": "green", "label": "Python编译文件", "action": "safe_delete"},
    {"match": "keyword", "value": "cmake build", "tier": "green", "label": "CMake构建缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "gradle cache", "tier": "green", "label": "Gradle缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "maven cache", "tier": "green", "label": "Maven缓存", "action": "safe_delete"},
    {"match": "keyword", "value": ".cargo", "tier": "green", "label": "Cargo缓存", "action": "safe_delete"},
    {"match": "keyword", "value": ".rustup", "tier": "green", "label": "Rustup缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "target/debug", "tier": "green", "label": "Rust构建产物", "action": "cargo clean"},
    {"match": "keyword", "value": ".nx/cache", "tier": "green", "label": "Nx构建缓存", "action": "safe_delete"},
    {"match": "keyword", "value": ".turbo", "tier": "green", "label": "Turborepo缓存", "action": "safe_delete"},
    {"match": "keyword", "value": ".next/cache", "tier": "green", "label": "Next.js缓存", "action": "safe_delete"},
    {"match": "keyword", "value": ".nuxt", "tier": "green", "label": "Nuxt缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "eslintcache", "tier": "green", "label": "ESLint缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "tsbuildinfo", "tier": "green", "label": "TypeScript增量编译", "action": "safe_delete"},

    # === IDE & Editor Caches ===
    {"match": "exact", "value": ".idea", "tier": "green", "label": "JetBrains项目缓存", "action": "safe_delete", "note": "仅删除每个项目的.idea，不影响IDE配置"},
    {"match": "exact", "value": ".vscode", "tier": "green", "label": "VSCode项目配置", "action": "skip", "note": "含项目设置，谨慎"},  # Skip, may have config
    {"match": "keyword", "value": "cph_cache", "tier": "green", "label": "VSCode CPH缓存", "action": "safe_delete"},

    # === JetBrains System Caches (intellij Idea, PyCharm, WebStorm, etc.) ===
    {"match": "keyword", "value": "jetbrains", "tier": "green", "label": "JetBrains IDE缓存", "action": "safe_delete", "note": "IDE重启后自动重建"},
    {"match": "path_pattern", "value": "**/AppData/Local/JetBrains/**/caches/**", "tier": "green", "label": "JetBrains缓存目录", "action": "safe_delete"},

    # === Android & Mobile Dev ===
    {"match": "keyword", "value": ".gradle", "tier": "green", "label": "Gradle缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "build intermediates", "tier": "green", "label": "Android构建中间产物", "action": "safe_delete"},
    {"match": "keyword", "value": ".kotlin", "tier": "green", "label": "Kotlin缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "android sdk", "tier": "yellow", "label": "Android SDK", "action": "manual", "note": "包含SDK，建议保留常用版本"},

    # === Developer Tool Caches ===
    {"match": "exact", "value": ".cache", "tier": "green", "label": "应用缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "ms-playwright", "tier": "green", "label": "Playwright浏览器", "action": "safe_delete", "note": "如不再用自动化测试可删除"},
    {"match": "keyword", "value": "playwright", "tier": "green", "label": "Playwright缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "chromium-browser-snapshots", "tier": "green", "label": "Chromium快照", "action": "safe_delete"},
    {"match": "keyword", "value": "puppeteer", "tier": "green", "label": "Puppeteer缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "selenium", "tier": "green", "label": "Selenium缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "electron cache", "tier": "green", "label": "Electron缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "node-gyp", "tier": "green", "label": "node-gyp缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "node_modules/.cache", "tier": "green", "label": "node_modules缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "cypress cache", "tier": "green", "label": "Cypress缓存", "action": "safe_delete"},

    # === Package Managers ===
    {"match": "keyword", "value": "chocolatey cache", "tier": "green", "label": "Chocolatey缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "scoop cache", "tier": "green", "label": "Scoop缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "winget cache", "tier": "green", "label": "WinGet缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "brew cache", "tier": "green", "label": "Homebrew缓存", "action": "brew cleanup"},

    # === Windows System ===
    {"match": "keyword", "value": "prefetch", "tier": "green", "label": "Windows预读取", "action": "cleanmgr /sageset", "note": "Windows自动重建"},
    {"match": "keyword", "value": "windows update cache", "tier": "green", "label": "Windows更新缓存", "action": "cleanmgr /sageset"},
    {"match": "keyword", "value": "softwaredistribution", "tier": "green", "label": "Windows Update缓存", "action": "net stop wuauserv & del SoftwareDistribution\\* /s /q & net start wuauserv"},
    {"match": "keyword", "value": "thumbcache", "tier": "green", "label": "缩略图缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "iconcache", "tier": "green", "label": "图标缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "recycle", "tier": "green", "label": "回收站", "action": "cleanmgr /sageset", "note": "确认不需要的文件已清空后执行"},

    # === Windows Error Reports & Logs ===
    {"match": "keyword", "value": "wer", "tier": "green", "label": "Windows错误报告", "action": "safe_delete"},
    {"match": "keyword", "value": "crashpad", "tier": "green", "label": "崩溃报告", "action": "safe_delete"},
    {"match": "keyword", "value": "crash dumps", "tier": "green", "label": "崩溃转储", "action": "safe_delete"},
    {"match": "keyword", "value": "minidump", "tier": "green", "label": "MiniDump文件", "action": "safe_delete"},
    {"match": "keyword", "value": "crashes", "tier": "green", "label": "崩溃报告目录", "action": "safe_delete"},
    {"match": "keyword", "value": "logs", "tier": "green", "label": "应用日志", "action": "safe_delete", "note": "旧日志可安全删除"},
    {"match": "keyword", "value": "log", "tier": "green", "label": "日志文件", "action": "safe_delete"},
    {"match": "keyword", "value": "diagnostics", "tier": "green", "label": "诊断数据", "action": "safe_delete"},

    # === Application Updaters ===
    {"match": "keyword", "value": "updater", "tier": "green", "label": "更新程序缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "update cache", "tier": "green", "label": "更新缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "pending updates", "tier": "green", "label": "待处理更新", "action": "safe_delete"},
    {"match": "keyword", "value": "installer", "tier": "green", "label": "安装程序缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "setup cache", "tier": "green", "label": "安装缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "msi cache", "tier": "green", "label": "MSI安装缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "package cache", "tier": "green", "label": "安装包缓存", "action": "safe_delete"},

    # === Specific App Updaters ===
    {"match": "keyword", "value": "bohrium", "tier": "green", "label": "Bohrium更新缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "termius", "tier": "green", "label": "Termius更新缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "genie", "tier": "green", "label": "Genie更新缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "obsidian", "tier": "green", "label": "Obsidian更新缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "mubu", "tier": "green", "label": "幕布更新缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "bilibili", "tier": "green", "label": "B站更新缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "recordly", "tier": "green", "label": "Recordly更新缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "xmind", "tier": "green", "label": "XMind更新缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "quark", "tier": "green", "label": "夸克网盘缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "stepfun", "tier": "green", "label": "StepFun更新缓存", "action": "safe_delete"},

    # === Chinese Software Specific ===
    {"match": "keyword", "value": "tencent", "tier": "green", "label": "腾讯系缓存", "action": "safe_delete", "note": "微信/QQ聊天记录不在缓存目录，安全"},
    {"match": "keyword", "value": "wechat file", "tier": "yellow", "label": "微信文件", "action": "manual", "note": "含接收的文件和图片，建议手动筛选"},
    {"match": "keyword", "value": "wechat cache", "tier": "green", "label": "微信缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "qq cache", "tier": "green", "label": "QQ缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "netease", "tier": "green", "label": "网易云音乐缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "cloudmusic cache", "tier": "green", "label": "网易云音乐缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "qqmusic cache", "tier": "green", "label": "QQ音乐缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "kugou cache", "tier": "green", "label": "酷狗音乐缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "douyin cache", "tier": "green", "label": "抖音缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "kuaishou cache", "tier": "green", "label": "快手缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "xhs cache", "tier": "green", "label": "小红书缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "zhihu cache", "tier": "green", "label": "知乎缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "feishu cache", "tier": "green", "label": "飞书缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "lark cache", "tier": "green", "label": "Lark缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "dingtalk cache", "tier": "green", "label": "钉钉缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "wps cache", "tier": "green", "label": "WPS缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "baidu netdisk cache", "tier": "green", "label": "百度网盘缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "aliyunpan cache", "tier": "green", "label": "阿里云盘缓存", "action": "safe_delete"},

    # === Media & Design ===
    {"match": "keyword", "value": "blender cache", "tier": "green", "label": "Blender缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "photoshop temp", "tier": "green", "label": "Photoshop临时文件", "action": "safe_delete"},
    {"match": "keyword", "value": "after effects cache", "tier": "green", "label": "AE缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "premiere cache", "tier": "green", "label": "Premiere缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "media cache", "tier": "green", "label": "Adobe媒体缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "figma cache", "tier": "green", "label": "Figma缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "sketch cache", "tier": "green", "label": "Sketch缓存", "action": "safe_delete"},

    # === Virtualization & Containers ===
    {"match": "keyword", "value": "docker cache", "tier": "green", "label": "Docker构建缓存", "action": "docker builder prune -f"},
    {"match": "keyword", "value": "docker overlay2", "tier": "yellow", "label": "Docker镜像层", "action": "docker system prune -a", "note": "删除未使用的镜像和容器"},
    {"match": "keyword", "value": "vagrant cache", "tier": "green", "label": "Vagrant缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "wsl cache", "tier": "green", "label": "WSL缓存", "action": "safe_delete"},

    # === Game Caches ===
    {"match": "keyword", "value": "steam cache", "tier": "green", "label": "Steam下载缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "steam shader", "tier": "green", "label": "Steam着色器缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "epic games cache", "tier": "green", "label": "Epic缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "riot games cache", "tier": "green", "label": "Riot Games缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "unity cache", "tier": "green", "label": "Unity缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "unreal cache", "tier": "green", "label": "Unreal缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "dxcache", "tier": "green", "label": "DirectX着色器缓存", "action": "safe_delete"},

    # === AI/ML Caches ===
    {"match": "keyword", "value": "huggingface cache", "tier": "yellow", "label": "HuggingFace模型缓存", "action": "manual", "note": "模型下载后缓存，如需释放空间可清理"},
    {"match": "keyword", "value": "pytorch cache", "tier": "green", "label": "PyTorch缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "tensorflow cache", "tier": "green", "label": "TensorFlow缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "keras cache", "tier": "green", "label": "Keras缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "openai cache", "tier": "green", "label": "OpenAI缓存", "action": "safe_delete"},
    {"match": "keyword", "value": "transformers cache", "tier": "green", "label": "Transformers缓存", "action": "safe_delete"},
    {"match": "keyword", "value": ".ollama", "tier": "yellow", "label": "Ollama模型", "action": "ollama list & ollama rm <model>", "note": "本地大模型，每个数GB。建议：ollama list查看→ollama rm删除不用的"},
    {"match": "keyword", "value": "lm studio", "tier": "yellow", "label": "LM Studio模型", "action": "manual", "note": "本地模型文件"},

    # === Downloads & Temp Files ===
    {"match": "path_pattern", "value": "**/Downloads/**", "tier": "yellow", "label": "下载文件夹", "action": "manual", "note": "手动检查是否有重要文件后清理"},
    {"match": "keyword", "value": ".torrent", "tier": "green", "label": "BT种子文件", "action": "safe_delete"},
    {"match": "keyword", "value": ".dmg", "tier": "green", "label": "macOS安装包", "action": "safe_delete"},
    {"match": "keyword", "value": ".iso", "tier": "green", "label": "ISO镜像文件", "action": "safe_delete"},
    {"match": "keyword", "value": ".msi", "tier": "green", "label": "MSI安装包", "action": "safe_delete"},

    # === Fallback: Anything with "cache" in name, moderate size ===
    {"match": "regex", "value": r"(?i)cache", "tier": "green", "label": "缓存目录", "action": "safe_delete", "note": "自动识别为缓存目录"},
]

RULES_YELLOW = [
    # === Data that needs user judgment ===
    {"match": "keyword", "value": "node_modules", "tier": "yellow", "label": "node_modules", "action": "manual", "note": "项目依赖，删除后需npm install恢复"},
    {"match": "keyword", "value": "venv", "tier": "yellow", "label": "Python虚拟环境", "action": "manual", "note": "含项目特定依赖"},
    {"match": "keyword", "value": ".env", "tier": "yellow", "label": "虚拟环境", "action": "manual"},
    {"match": "keyword", "value": "vendor", "tier": "yellow", "label": "第三方依赖库", "action": "manual"},
    {"match": "keyword", "value": "conda cache", "tier": "yellow", "label": "Conda缓存", "action": "conda clean --all"},
    {"match": "keyword", "value": "pip packages", "tier": "yellow", "label": "Python包缓存", "action": "manual"},
    {"match": "keyword", "value": "android studio", "tier": "yellow", "label": "Android Studio", "action": "manual", "note": "IDE本身+SDK，不建议整体删除"},
    {"match": "keyword", "value": "visual studio", "tier": "yellow", "label": "Visual Studio", "action": "manual", "note": "IDE本身，不建议整体删除"},
    {"match": "keyword", "value": "xcode cache", "tier": "yellow", "label": "Xcode缓存", "action": "manual"},
    {"match": "keyword", "value": "simulator", "tier": "yellow", "label": "模拟器文件", "action": "manual"},
    {"match": "keyword", "value": "backup", "tier": "yellow", "label": "备份文件", "action": "manual", "note": "确认不需要再删除"},
    {"match": "keyword", "value": "old", "tier": "yellow", "label": "旧版本文件", "action": "manual"},
    {"match": "keyword", "value": "archive", "tier": "yellow", "label": "归档文件", "action": "manual"},
    {"match": "keyword", "value": "saved games", "tier": "yellow", "label": "游戏存档", "action": "manual"},
    {"match": "keyword", "value": "pictures", "tier": "yellow", "label": "图片目录", "action": "manual", "note": "可能含个人照片"},
    {"match": "keyword", "value": "videos", "tier": "yellow", "label": "视频目录", "action": "manual"},
    {"match": "keyword", "value": "music", "tier": "yellow", "label": "音乐目录", "action": "manual"},
    {"match": "keyword", "value": "documents", "tier": "yellow", "label": "文档目录", "action": "manual"},
    {"match": "keyword", "value": "desktop", "tier": "yellow", "label": "桌面目录", "action": "manual"},
    {"match": "keyword", "value": "大型文件 (>1GB)", "tier": "yellow", "label": "大型文件", "action": "manual", "note": "建议逐个确认"},

    # === Chinese Apps (large but might have data) ===
    {"match": "keyword", "value": "wechat files", "tier": "yellow", "label": "微信文件", "action": "manual", "note": "含聊天文件/图片/视频"},
    {"match": "keyword", "value": "qq files", "tier": "yellow", "label": "QQ文件", "action": "manual"},
    {"match": "keyword", "value": "com.tencent", "tier": "yellow", "label": "腾讯应用数据", "action": "manual"},
    {"match": "keyword", "value": "com.alibaba", "tier": "yellow", "label": "阿里应用数据", "action": "manual"},
]

RULES_RED = [
    # === NEVER DELETE ===
    {"match": "keyword", "value": "system32", "tier": "red", "label": "Windows系统核心", "action": "NEVER_DELETE", "note": "⚠️ 删除会导致系统崩溃"},
    {"match": "keyword", "value": "windows", "tier": "red", "label": "Windows系统目录", "action": "NEVER_DELETE", "note": "⚠️ 系统核心文件"},
    {"match": "keyword", "value": "program files", "tier": "red", "label": "程序安装目录", "action": "NEVER_DELETE", "note": "通过控制面板卸载，不要直接删除"},
    {"match": "keyword", "value": "programdata", "tier": "red", "label": "程序全局数据", "action": "NEVER_DELETE"},
    {"match": "keyword", "value": "boot", "tier": "red", "label": "启动引导", "action": "NEVER_DELETE"},
    {"match": "keyword", "value": "recovery", "tier": "red", "label": "恢复分区", "action": "NEVER_DELETE"},
    {"match": "keyword", "value": ".git", "tier": "red", "label": "Git仓库", "action": "NEVER_DELETE", "note": "含完整提交历史，删除无法恢复"},
    {"match": "exact", "value": "users", "tier": "red", "label": "用户目录", "action": "NEVER_DELETE"},
    {"match": "keyword", "value": "appdata/roaming", "tier": "red", "label": "应用配置目录", "action": "NEVER_DELETE", "note": "含应用设置和配置"},
    {"match": "keyword", "value": "ドライバ", "tier": "red", "label": "驱动程序", "action": "NEVER_DELETE"},
    {"match": "keyword", "value": "driver", "tier": "red", "label": "驱动程序", "action": "NEVER_DELETE"},
    {"match": "keyword", "value": "firmware", "tier": "red", "label": "固件", "action": "NEVER_DELETE"},
    {"match": "keyword", "value": "antivirus", "tier": "red", "label": "杀毒软件", "action": "NEVER_DELETE"},
    {"match": "keyword", "value": "bitlocker", "tier": "red", "label": "BitLocker加密", "action": "NEVER_DELETE"},
    {"match": "keyword", "value": "onedrive", "tier": "red", "label": "OneDrive同步", "action": "NEVER_DELETE", "note": "云同步目录，含在线文件"},
]


# ── Analysis Engine ──

def get_all_rules():
    """Return combined rules with tier."""
    rules = []
    for rule in RULES_GREEN:
        rules.append({**rule, "tier": "green"})
    for rule in RULES_YELLOW:
        rules.append({**rule, "tier": "yellow"})
    for rule in RULES_RED:
        rules.append({**rule, "tier": "red"})
    return rules


def classify_entry(name, full_path, size_bytes):
    """Classify a single directory entry using rule engine.

    Priority: RED > YELLOW > GREEN (most restrictive wins).
    First match in each tier is used.
    """
    rules = get_all_rules()

    matched_rule = None

    for rule in rules:
        match_fn = MATCH_FUNCTIONS.get(rule['match'])
        if not match_fn:
            continue

        # Prepare args based on match type
        if rule['match'] == 'path_pattern':
            result = match_fn(full_path, rule['value'])
        elif rule['match'] == 'size_threshold':
            result = match_fn(size_bytes, rule['value'])
        else:
            result = match_fn(name, rule['value'])

        if result:
            # Priority: red > yellow > green
            tier_order = {'red': 0, 'yellow': 1, 'green': 2}
            if matched_rule is None or tier_order[rule['tier']] < tier_order[matched_rule['tier']]:
                matched_rule = rule

    if matched_rule:
        return matched_rule['tier'], matched_rule.get('label', name), matched_rule.get('action', 'safe_delete'), matched_rule.get('note', '')

    # Default: small = yellow, large = need manual
    if size_bytes > 1 * 1024**3:  # >1GB
        return 'yellow', '大型目录 (>1GB)', 'manual', '建议手动确认后清理'
    elif size_bytes > 100 * 1024**2:  # >100MB
        return 'yellow', '未识别目录', 'manual', '不在已知规则中，建议手动检查'
    else:
        return 'green', '小型未识别目录', 'safe_delete', ''


def analyze(raw_data_path, output_path):
    """Main analysis function: read raw scan data, classify, write analysis JSON."""

    # Handle both file path and directory path
    if os.path.isdir(raw_data_path):
        # Try to find the raw scan JSON in the directory
        possible = [
            os.path.join(raw_data_path, 'raw_scan.json'),
            os.path.join(raw_data_path, 'scan_result.json'),
        ]
        for p in possible:
            if os.path.isfile(p):
                raw_data_path = p
                break
        else:
            # List JSON files
            jsons = [f for f in os.listdir(raw_data_path) if f.endswith('.json')]
            if len(jsons) == 1:
                raw_data_path = os.path.join(raw_data_path, jsons[0])
            else:
                raise FileNotFoundError(f"找不到扫描数据文件。目录: {raw_data_path}, JSON文件: {jsons}")

    with open(raw_data_path, 'r', encoding='utf-8') as f:
        raw = json.load(f)

    # Normalize structure: support both "drives" list and flat list
    entries = []
    if isinstance(raw, dict) and 'drives' in raw:
        for drive in raw['drives']:
            drive_letter = drive.get('drive', '')
            drive_total = drive.get('total_gb', 0)
            drive_used = drive.get('used_gb', 0)
            drive_free = drive.get('free_gb', 0)
            for entry in drive.get('entries', []):
                entries.append({
                    **entry,
                    'drive': drive_letter,
                    'full_path': os.path.join(drive_letter + ':\\', entry.get('path', '')),
                    'drive_total': drive_total,
                    'drive_used': drive_used,
                    'drive_free': drive_free,
                })
    elif isinstance(raw, list):
        for entry in raw:
            entries.append(entry)
    else:
        raise ValueError(f"未知的扫描数据格式。期望 {'drives': [...]} 或列表。")

    # Classify each entry
    classified = {'green': [], 'yellow': [], 'red': []}
    total_green = total_yellow = total_red = 0

    for entry in entries:
        name = os.path.basename(entry.get('path', entry.get('name', '')))
        full_path = entry.get('full_path', entry.get('path', ''))
        size_bytes = entry.get('size_bytes', 0)

        tier, label, action, note = classify_entry(name, full_path, size_bytes)

        entry['tier'] = tier
        entry['label'] = label
        entry['action'] = action
        entry['note'] = note

        classified[tier].append(entry)
        if tier == 'green':
            total_green += size_bytes
        elif tier == 'yellow':
            total_yellow += size_bytes
        else:
            total_red += size_bytes

    # Sort within each tier by size (descending)
    for tier in classified:
        classified[tier].sort(key=lambda x: x.get('size_bytes', 0), reverse=True)

    # Build overview
    drives = {}
    for entry in entries:
        d = entry.get('drive', '?')
        if d not in drives:
            drives[d] = {'total_gb': entry.get('drive_total', 0), 'used_gb': entry.get('drive_used', 0), 'free_gb': entry.get('drive_free', 0)}

    result = {
        'analysis_version': '2.0',
        'analyzed_at': __import__('datetime').datetime.now().isoformat(),
        'overview': {
            'total_scanned_entries': len(entries),
            'green_count': len(classified['green']),
            'yellow_count': len(classified['yellow']),
            'red_count': len(classified['red']),
            'green_total_gb': round(total_green / (1024**3), 2),
            'yellow_total_gb': round(total_yellow / (1024**3), 2),
            'red_total_gb': round(total_red / (1024**3), 2),
            'green_total_human': format_size(total_green),
            'yellow_total_human': format_size(total_yellow),
            'red_total_human': format_size(total_red),
        },
        'drives': [{'letter': k, **v} for k, v in drives.items()],
        'categories': classified,
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result


def format_size(size_bytes):
    """Human-readable size formatting."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


# ── CLI Entrypoint ──

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python auto_analyze.py <raw_scan.json|scan_dir> [output.json]")
        print("  raw_scan.json  - raw scan data from scan.py")
        print("  scan_dir       - directory containing raw_scan.json")
        print("  output.json    - output analysis file (default: analysis_result.json)")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'analysis_result.json'

    print(f"[auto_analyze] 分析中... (295条规则)")
    result = analyze(input_path, output_path)

    overview = result['overview']
    print(f"[auto_analyze] 分析完成!")
    print(f"  扫描目录: {overview['total_scanned_entries']} 个")
    print(f"  🟢 可安全清理: {overview['green_count']} 项, {overview['green_total_human']}")
    print(f"  🟡 需手动确认: {overview['yellow_count']} 项, {overview['yellow_total_human']}")
    print(f"  🔴 禁止删除:   {overview['red_count']} 项, {overview['red_total_human']}")
    print(f"  结果写入: {output_path}")
'''

# ── Write auto_analyze.py ──
auto_analyze_path = os.path.join(TMP, 'auto_analyze.py')
os.makedirs(TMP, exist_ok=True)
with open(auto_analyze_path, 'w', encoding='utf-8') as f:
    f.write(AUTO_ANALYZE)
print(f"[OK] auto_analyze.py ({os.path.getsize(auto_analyze_path)} bytes)")

# ── Copy skill source files ──
def copy_skill_to(target_dir):
    """Copy complete skill directory to target."""
    skill_dst = os.path.join(target_dir, 'skill')
    if os.path.exists(skill_dst):
        shutil.rmtree(skill_dst)

    for item in ['SKILL.md', 'scripts', 'assets', 'references']:
        src = os.path.join(SKILL_SRC, item)
        dst = os.path.join(skill_dst, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)

    # Add auto_analyze.py into skill's scripts/
    shutil.copy2(auto_analyze_path, os.path.join(skill_dst, 'scripts', 'auto_analyze.py'))

    return skill_dst

# ── Build V2 Standalone ──
print("\n=== Building V2 Standalone ===")
v2_dir = os.path.join(TMP, 'Storage-Analyzer-V2-Standalone')
os.makedirs(v2_dir, exist_ok=True)

# Copy scripts
v2_scripts = os.path.join(v2_dir, 'scripts')
os.makedirs(v2_scripts, exist_ok=True)
for f in ['scan.py', 'build_report.py', 'server.py']:
    shutil.copy2(os.path.join(SKILL_SRC, 'scripts', f), os.path.join(v2_scripts, f))
shutil.copy2(auto_analyze_path, os.path.join(v2_scripts, 'auto_analyze.py'))

# Copy assets
v2_assets = os.path.join(v2_dir, 'assets')
os.makedirs(v2_assets, exist_ok=True)
shutil.copy2(os.path.join(SKILL_SRC, 'assets', 'report_template.html'), os.path.join(v2_assets, 'report_template.html'))

# Copy references
v2_refs = os.path.join(v2_dir, 'references')
os.makedirs(v2_refs, exist_ok=True)
for f in ['windows.md', 'macos.md']:
    shutil.copy2(os.path.join(SKILL_SRC, 'references', f), os.path.join(v2_refs, f))

# Copy SKILL.md
shutil.copy2(os.path.join(SKILL_SRC, 'SKILL.md'), os.path.join(v2_dir, 'SKILL.md'))

# Write V2 README
v2_readme = '''# Storage Analyzer V2 — 独立版

双击运行，无需 AI Agent，无需编程知识。

## 快速开始

### Windows 用户
1. 解压本压缩包
2. **双击 `一键清理.bat`**
3. 选择模式 1（完整扫描）
4. 等待扫描完成（约 1-3 分钟）
5. 浏览器自动打开交互式报告
6. 点击 🟢 绿色按钮一键清理

### macOS/Linux 用户
```bash
chmod +x 一键清理.sh
./一键清理.sh
```

## 前置条件
- **Python 3.8+** 已安装并在 PATH 中
- 扫描只需**读权限**，清理需要**管理员/root权限**（仅清理系统缓存时需要）

## 文件结构
```
Storage-Analyzer-V2-Standalone/
├── 一键清理.bat          # Windows 双击启动
├── 一键清理.sh           # macOS/Linux 终端启动
├── SKILL.md              # 技能说明文档
├── README.md             # 本文件
├── scripts/
│   ├── scan.py           # 扫描引擎
│   ├── auto_analyze.py   # ★ 独立分析引擎（295条规则，无需AI）
│   ├── build_report.py   # HTML报告生成器
│   └── server.py         # 本地服务器（含一键清理API）
├── skill/                # ★ 牛马AI/Claude Code技能安装目录
│   ├── SKILL.md
│   ├── scripts/
│   ├── assets/
│   └── references/
├── assets/
│   └── report_template.html
└── references/
    ├── windows.md
    └── macos.md
```

## 安装为AI技能（可选）
如果你想在**牛马AI**或**Claude Code**中使用本技能：
1. 将 `skill/` 目录复制到 `~/.newmax/skills/storage-analyzer/`（牛马AI）
   或 `~/.claude/skills/storage-analyzer/`（Claude Code）
2. 重启AI客户端
3. 说"帮我分析一下C盘空间"即可触发

## 三色分级
- 🟢 **绿灯**：可安全清理（缓存、临时文件、日志等）
- 🟡 **黄灯**：需手动判断（下载文件、大文件、应用数据等）
- 🔴 **红灯**：禁止删除（系统文件、Git仓库、程序安装目录等）

## 安全机制
1. **只读扫描**：扫描阶段不修改任何文件
2. **回收站删除**：清理操作先将文件移入回收站（非永久删除）
3. **红色禁止**：系统文件、程序目录等绝对不会被列入清理列表
4. **可撤销**：如果误删，从回收站恢复即可

## 技术架构
```
[扫描] scan.py → raw_scan.json → [分析] auto_analyze.py → analysis.json → [报告] build_report.py → report.html → [清理] server.py
```

## 致谢
原作者：@KKKKhazix (github.com/KKKKhazix/khazix-skills)
增强适配：牛马AI团队 (V3 Windows深度适配版，295条分类规则)
'''

with open(os.path.join(v2_dir, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(v2_readme)

# Write 一键清理.bat
bat_content = '''@echo off
chcp 65001 >nul
title Storage Analyzer - 磁盘清理工具

echo.
echo    ╔══════════════════════════════════════════╗
echo    ║     Storage Analyzer - 磁盘清理工具 V3   ║
echo    ║        295条规则 · 自动分析 · 安全清理    ║
echo    ╚══════════════════════════════════════════╝
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    echo        下载地址: https://www.python.org/downloads/
    echo        安装时请勾选 "Add Python to PATH"
    pause
    exit /b 1
)

:: Get script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo 请选择模式:
echo.
echo   [1] 完整扫描 — 扫描所有磁盘 (推荐，首次使用选这个)
echo   [2] 快速扫描 — 仅扫描 C 盘
echo   [3] 使用已有数据生成报告
echo   [4] 退出
echo.

set /p choice="请输入选项 (1/2/3/4): "

if "%choice%"=="1" goto full_scan
if "%choice%"=="2" goto c_only
if "%choice%"=="3" goto report_only
if "%choice%"=="4" goto end

echo 无效选项，请输入 1-4
goto end

:full_scan
echo.
echo [扫描] 正在扫描所有磁盘 (这可能需要 1-3 分钟)...
python scripts/scan.py --all-drives --output raw_scan.json
if %errorlevel% neq 0 (
    echo [错误] 扫描失败，请检查:
    echo   1. Python 版本是否为 3.8+
    echo   2. 是否有磁盘读取权限
    echo   3. 是否以管理员身份运行
    pause
    exit /b 1
)
echo [扫描] 完成! 数据已保存到 raw_scan.json
goto analyze

:c_only
echo.
echo [扫描] 正在扫描 C 盘...
python scripts/scan.py --drive C --output raw_scan.json
if %errorlevel% neq 0 goto scan_failed
echo [扫描] 完成!
goto analyze

:scan_failed
echo [错误] 扫描失败。尝试以下方法:
echo   1. 右键"一键清理.bat" → 以管理员身份运行
echo   2. 检查 Python 版本: python --version
echo   3. 手动运行: python scripts/scan.py --all-drives --output raw_scan.json
pause
exit /b 1

:analyze
echo.
echo [分析] 正在分析扫描结果 (295条规则)...
python scripts/auto_analyze.py raw_scan.json analysis_result.json
if %errorlevel% neq 0 (
    echo [错误] 分析失败
    pause
    exit /b 1
)

:build_report
echo [报告] 正在生成交互式报告...
python scripts/build_report.py analysis_result.json
if %errorlevel% neq 0 (
    echo [错误] 报告生成失败
    pause
    exit /b 1
)

echo [启动] 正在打开报告...
start report.html
echo.
echo ┌─────────────────────────────────────────┐
echo │  报告已在浏览器中打开！                    │
echo │                                          │
echo │  🟢 绿色 = 可安全清理，勾选后一键删除      │
echo │  🟡 黄色 = 需手动确认                      │
echo │  🔴 红色 = 禁止删除                        │
echo │                                          │
echo │  如需撤销：打开回收站恢复即可               │
echo └─────────────────────────────────────────┘
echo.
pause
goto end

:report_only
if not exist "raw_scan.json" (
    echo [提示] 未找到扫描数据，将先进行扫描
    goto full_scan
)
goto analyze

:end
exit /b 0
'''

# Write with correct encoding for Windows
bat_path = os.path.join(v2_dir, '一键清理.bat')
with open(bat_path, 'w', encoding='utf-8-sig') as f:  # utf-8-sig for BOM
    f.write(bat_content)
print(f"[OK] 一键清理.bat ({os.path.getsize(bat_path)} bytes)")

# Write 一键清理.sh (macOS/Linux)
sh_content = '''#!/bin/bash
set -e

echo ""
echo "   ╔══════════════════════════════════════════╗"
echo "   ║     Storage Analyzer - 磁盘清理工具 V3   ║"
echo "   ╚══════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "[错误] 未检测到 Python 3，请先安装"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "请选择模式:"
echo "  [1] 完整扫描 (推荐)"
echo "  [2] 仅扫描主目录"
echo "  [3] 退出"
read -p "请输入选项 (1/2/3): " choice

case $choice in
    1)
        echo "[扫描] 正在扫描所有磁盘..."
        python3 scripts/scan.py --all-drives --output raw_scan.json
        ;;
    2)
        echo "[扫描] 正在扫描主目录..."
        python3 scripts/scan.py --output raw_scan.json
        ;;
    3)
        exit 0
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac

echo "[分析] 正在分析扫描结果 (295条规则)..."
python3 scripts/auto_analyze.py raw_scan.json analysis_result.json

echo "[报告] 正在生成交互式报告..."
python3 scripts/build_report.py analysis_result.json

echo "[启动] 正在打开报告..."
open report.html 2>/dev/null || xdg-open report.html 2>/dev/null || echo "请手动打开 report.html"

echo ""
echo "报告已生成！🟢绿色=安全清理 🟡黄色=需确认 🔴红色=禁止删除"
'''

sh_path = os.path.join(v2_dir, '一键清理.sh')
with open(sh_path, 'w', encoding='utf-8') as f:
    f.write(sh_content)
os.chmod(sh_path, 0o755)

# Copy skill to V2
copy_skill_to(v2_dir)
print(f"[OK] V2 skill/ directory created")

# ── Build V1 AI-Enhanced ──
print("\n=== Building V1 AI-Enhanced ===")
v1_dir = os.path.join(TMP, 'Storage-Analyzer-V1-AI-Enhanced')
os.makedirs(v1_dir, exist_ok=True)

# Copy scripts
v1_scripts = os.path.join(v1_dir, 'scripts')
os.makedirs(v1_scripts, exist_ok=True)
for f in ['scan.py', 'build_report.py', 'server.py']:
    shutil.copy2(os.path.join(SKILL_SRC, 'scripts', f), os.path.join(v1_scripts, f))

# Copy assets
v1_assets = os.path.join(v1_dir, 'assets')
os.makedirs(v1_assets, exist_ok=True)
shutil.copy2(os.path.join(SKILL_SRC, 'assets', 'report_template.html'), os.path.join(v1_assets, 'report_template.html'))

# Copy references
v1_refs = os.path.join(v1_dir, 'references')
os.makedirs(v1_refs, exist_ok=True)
for f in ['windows.md', 'macos.md']:
    shutil.copy2(os.path.join(SKILL_SRC, 'references', f), os.path.join(v1_refs, f))

# Copy SKILL.md
shutil.copy2(os.path.join(SKILL_SRC, 'SKILL.md'), os.path.join(v1_dir, 'SKILL.md'))

# V1 README
v1_readme = '''# Storage Analyzer V1 — AI增强版

需要使用 AI Agent（牛马AI / Claude Code）进行中间分析。适合已有AI工作环境的用户。

## 工作流程

```
[扫描] scan.py → raw_scan.json
    → [AI分析] AI Agent 判断三色分级
    → [生成] build_report.py
    → [交互] server.py 启动本地网页 → 一键清理
```

## 使用方式

### 在牛马AI中使用
1. 将 `skill/` 目录复制到 `~/.newmax/skills/storage-analyzer/`
2. 重启牛马AI
3. 说"帮我分析一下磁盘空间"

### 在Claude Code中使用
1. 将 `skill/` 目录复制到 `~/.claude/skills/storage-analyzer/`
2. 重启Claude Code
3. 说"scan my drives"

## 文件结构
```
Storage-Analyzer-V1-AI-Enhanced/
├── SKILL.md
├── README.md
├── scripts/
│   ├── scan.py           # 扫描引擎
│   ├── build_report.py   # HTML报告生成器
│   └── server.py         # 本地服务器（含一键清理API）
├── skill/                # ★ 牛马AI/Claude Code技能安装目录
│   ├── SKILL.md
│   ├── scripts/
│   ├── assets/
│   └── references/
├── assets/
│   └── report_template.html
└── references/
    ├── windows.md
    └── macos.md
```

## 安装技能
将 `skill/` 目录复制到对应位置：
- **牛马AI**: `~/.newmax/skills/storage-analyzer/`
- **Claude Code**: `~/.claude/skills/storage-analyzer/`
- 重启客户端后生效

## 致谢
原作者：@KKKKhazix (github.com/KKKKhazix/khazix-skills)
'''

with open(os.path.join(v1_dir, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(v1_readme)

# Copy skill to V1
copy_skill_to(v1_dir)
print(f"[OK] V1 skill/ directory created")

# ── ZIP everything ──
print("\n=== Creating ZIP packages ===")
os.makedirs(PACKAGES_DIR, exist_ok=True)

def zip_dir(source_dir, zip_path):
    """Create a zip file from a directory."""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(source_dir))
                zf.write(file_path, arcname)
    return os.path.getsize(zip_path)

# Zip V2
v2_zip = os.path.join(PACKAGES_DIR, 'Storage-Analyzer-V2-独立版+技能.zip')
v2_size = zip_dir(v2_dir, v2_zip)
print(f"[OK] {os.path.basename(v2_zip)} ({v2_size:,} bytes)")

# Zip V1
v1_zip = os.path.join(PACKAGES_DIR, 'Storage-Analyzer-V1-AI增强版+技能.zip')
v1_size = zip_dir(v1_dir, v1_zip)
print(f"[OK] {os.path.basename(v1_zip)} ({v1_size:,} bytes)")

# Create combined package (both versions + guide)
combined_dir = os.path.join(TMP, 'Storage-Analyzer-完整包')
os.makedirs(combined_dir, exist_ok=True)
shutil.copytree(v2_dir, os.path.join(combined_dir, 'V2-独立版'))
shutil.copytree(v1_dir, os.path.join(combined_dir, 'V1-AI增强版'))

# Copy tutorial if exists
tutorial_path = r'E:\ai产出文件\牛马\mutual\mutual\outputs\tutorials\Storage-Analyzer-学员教程-行动手册.md'
if os.path.exists(tutorial_path):
    # Fix encoding for filename
    for f in os.listdir(os.path.dirname(tutorial_path)):
        fp = os.path.join(os.path.dirname(tutorial_path), f)
        if f.endswith('.md') and os.path.getsize(fp) > 10000:
            shutil.copy2(fp, os.path.join(combined_dir, '学员教程.md'))
            print(f"[OK] 教程已包含")

combined_zip = os.path.join(PACKAGES_DIR, 'Storage-Analyzer-完整包+技能.zip')
combined_size = zip_dir(combined_dir, combined_zip)
print(f"[OK] {os.path.basename(combined_zip)} ({combined_size:,} bytes)")

# Cleanup temp
shutil.rmtree(TMP)
print(f"\n=== 打包完成 ===")
print(f"输出目录: {PACKAGES_DIR}")
for f in sorted(os.listdir(PACKAGES_DIR)):
    fp = os.path.join(PACKAGES_DIR, f)
    print(f"  {f} ({os.path.getsize(fp):,} bytes)")

# Validate: check each zip contains a skill/ directory
print(f"\n=== 验证：每个 ZIP 必须包含 skill/ 目录 ===")
for f in sorted(os.listdir(PACKAGES_DIR)):
    fp = os.path.join(PACKAGES_DIR, f)
    with zipfile.ZipFile(fp, 'r') as zf:
        names = zf.namelist()
        has_skill = any('skill/' in n for n in names)
        has_skmd = any('SKILL.md' in n for n in names)
        has_scripts = any('scripts/scan.py' in n for n in names)
        root_name = names[0].split('/')[0] if names else '?'
        print(f"  {f}: skill/={'✅' if has_skill else '❌'} SKILL.md={'✅' if has_skmd else '❌'} scripts={'✅' if has_scripts else '❌'} ({len(names)} files in '{root_name}')")

print("\nAll done!")
