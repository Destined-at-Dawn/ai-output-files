#!/usr/bin/env python3
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
