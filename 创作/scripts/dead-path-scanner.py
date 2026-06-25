#!/usr/bin/env python3
"""
死路径扫描器 v3.1 — SOP/规则/CLAUDE 文件中的断链检测 + 定期体检
用法：
  python scripts/dead-path-scanner.py                  # 终端输出（默认 extended）
  python scripts/dead-path-scanner.py --report         # 保存报告到 outputs/
  python scripts/dead-path-scanner.py --severity all   # 含 low 严重度
  python scripts/dead-path-scanner.py --quick          # 只扫核心文件（<5秒）
  python scripts/dead-path-scanner.py --fix            # 自动修复模式（生成修复脚本）

v3.1 改进（v3.0 误报太多：3175 条中 60%+ 是误报）：
- 上下文感知：相对路径先从源文件目录找 → 再工作区 → 再 projects/ 下找
- 路由表过滤：表格中多段中文关键词（如「公众号/小红书/视频」）不是路径
- .claude/rules/ 隐式引用自动补全
- 建议修复：自动查找正确路径
"""

import os
import re
import sys
import io
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Windows GBK 编码修复
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# === 路径配置 ===
WORKSPACE = Path(r"E:\ai产出文件\牛马\创作\创作")
SKILLS_DIR = Path(r"C:\Users\13975\.newmax\skills")
NEWMAX_DIR = Path(r"C:\Users\13975\.newmax")

# === 扫描目标 ===

# Tier 1: 核心文件（每次必扫，<5秒）
CORE_FILES = [
    "CLAUDE.md", "AGENT.md", "runtime-snapshot.md",
    "SOPs/SOP总索引.md",
    "SOPs/00_提示词优化SOP.md",
    "SOPs/01_内容创作SOP.md",
    "SOPs/02_文章采集与分析SOP.md",
    "SOPs/03_视觉素材生成SOP.md",
    "SOPs/06_系统管理SOP.md",
    "SOPs/14_GitHub项目生命周期管理SOP.md",
    "SOPs/15_Obsidian知识库管理SOP.md",
    "SOPs/16_社群分享SOP.md",
]

# Tier 2: 扩展目录（默认扫描，~15秒）
EXTENDED_DIRS = [
    "SOPs", "_system/rules", ".claude/rules",
    "projects/20260425-内容创作系统/社群运营",
    "公众号", "微信朋友圈",
]

# Tier 3: 全量目录（--full 模式，~30秒）
FULL_DIRS = EXTENDED_DIRS + [
    "科研日报", "自我进化", "科研认知", "IDEAS",
    "评论", "认知之书", "每日完成记录", "ppt", "视频提示词",
]

# 跳过的目录
SKIP_DIRS = {
    'github', 'node_modules', '.git', '__pycache__', '.mypy_cache',
    '归档', 'archive', 'downloads', 'temp', 'tmp',
    'html', '素材', '.venv', 'venv',
}

# 输出目录也跳过（里面是生成物不是源文件）
SKIP_DIRS.add('outputs')

# 根目录文件
ROOT_FILES = ["CLAUDE.md", "AGENT.md", "runtime-snapshot.md"]

# === 路径提取正则（v3.0 精准版）===

# 已知的相对路径前缀（只匹配这些开头的字符串）
KNOWN_PREFIXES = [
    'SOPs/', '_system/', 'projects/', '公众号/', '微信朋友圈/',
    '科研日报/', '自我进化/', 'skills/', '评论/', '认知之书/',
    'outputs/', 'scripts/', 'memory/', '.claude/', '.newmax/',
    'github/', 'ppt/', '视频提示词/', '科研认知/', 'IDEAS/',
    '每日完成记录/', '约束文件/', '经验库/', 'references/',
    'templates/', '知识中枢/',
]

# 不检查的模式（v3.0 大幅扩展，消灭误报）
SKIP_PATTERNS = [
    # 模板占位符
    re.compile(r'\{[^}]*\}'),
    # 通配符
    re.compile(r'[\*\?]'),
    # 方括号占位符 [xxx]
    re.compile(r'^\[.*\]$'),
    # URL
    re.compile(r'^https?://', re.I),
    re.compile(r'^ftp://', re.I),
    # CLI 命令
    re.compile(r'^(python|pip|npm|npx|node|git|gh|bash|sh|powershell|cmd|cd|ls|cat|echo|curl|wget|chmod|rm|cp|mv|dir|type|mkdir|rd|del)\s', re.I),
    # MCP 工具调用
    re.compile(r'^mcp__'),
    # 函数/代码
    re.compile(r'^(param|function|import|from|def |class |if |for |while |return )'),
    # 斜杠命令
    re.compile(r'^/(compact|rewind|clear|loop|tasks|help)'),
    # PowerShell 变量
    re.compile(r'^\$[\(\{_]'),
    # 纯中文（非路径）
    re.compile(r'^[一-鿿\s，。；：！？、""''（）]+$'),
    # 变量赋值
    re.compile(r'[=;|&<>]'),
    # 非路径的标识符
    re.compile(r'^(your-|xxx|example|sample|demo|test|placeholder|具体|对应|某)'),
    # 社群运营 skill 里的 workflow 名
    re.compile(r'^(WF[-_]|Mode[-_]|模式[一二三四五]?)'),
    # 书名号引用
    re.compile(r'^《.*》$'),
    # 引号包裹的纯文本
    re.compile(r'^["“].*["”]$'),
]

# 二次过滤：路径中含这些 → 不是路径
SKIP_CONTAINS = ['（', '）', '「', '」', '——', '……', '：', '；']

MAX_FILE_SIZE = 500_000  # 跳过 >500KB 的文件


class DeadPathScanner:
    def __init__(self, workspace=WORKSPACE, verbose=False):
        self.workspace = workspace
        self.verbose = verbose
        self.dead_paths = []
        self.stats = defaultdict(int)
        self.files_scanned = 0
        self.file_index = None  # 懒构建

    def _build_file_index(self):
        """预构建文件索引（一次遍历，之后用 set 查找，O(1)）"""
        if self.file_index is not None:
            return
        self.file_index = set()
        # 工作区
        for root, dirs, files in os.walk(self.workspace):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            for f in files:
                self.file_index.add(os.path.join(root, f))
                # 也登记无扩展名的（可能是目录引用）
                base = os.path.join(root, f)
                self.file_index.add(base.rstrip('/\\'))
        # .claude 目录（被上面的 . 开头跳过了）
        claude_dir = self.workspace / '.claude'
        if claude_dir.exists():
            for root, dirs, files in os.walk(claude_dir):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for f in files:
                    self.file_index.add(os.path.join(root, f))
        # skills 目录（只索引 SKILL.md 和 _meta.json）
        if SKILLS_DIR.exists():
            for root, dirs, files in os.walk(SKILLS_DIR):
                for f in files:
                    if f in ('SKILL.md', '_meta.json'):
                        self.file_index.add(os.path.join(root, f))
        if self.verbose:
            print(f"   File index: {len(self.file_index)} entries")

    def should_skip_path(self, path_str):
        """v3.1 综合过滤（+路由表+占位符+纯中文路径段过滤）"""
        if not path_str or len(path_str.strip()) < 4:
            return True
        path_str = path_str.strip()
        # 正则模式匹配
        for pattern in SKIP_PATTERNS:
            if pattern.search(path_str):
                return True
        # 含中文标点
        for ch in SKIP_CONTAINS:
            if ch in path_str:
                return True
        # 扩展名黑名单
        ext = Path(path_str).suffix.lower()
        if ext in ('.exe', '.dll', '.png', '.jpg', '.jpeg', '.gif', '.svg',
                    '.mp4', '.mp3', '.wav', '.pdf', '.docx', '.xlsx', '.pptx',
                    '.zip', '.tar', '.gz', '.woff', '.ttf', '.eot', '.ico'):
            return True
        # 绝对路径中含特殊字符（不是路径）
        if re.match(r'^[A-Za-z]:\\', path_str):
            if any(c in path_str for c in ['(', ')', '=', ';', '|', '&', '<', '>']):
                return True
        # v3.1 占位符检查：路径的任何部分含 xxx/example/placeholder → 跳过
        parts = re.split(r'[/\\]', path_str)
        placeholder_words = {'xxx', 'example', 'sample', 'demo', 'placeholder',
                             'your-name', 'your-university', 'your-gpa'}
        if any(p.lower() in placeholder_words for p in parts):
            return True
        # v3.1 路由表过滤：
        # 规则 1：3+ 段全是纯中文 → 关键词组合（如 公众号/小红书/视频/海报）
        if '/' in path_str:
            segments = path_str.split('/')
            if len(segments) >= 3 and all(re.match(r'^[一-鿿]{2,8}$', s) for s in segments):
                return True
            # 规则 2：3+ 段，大部分是中文关键词（>60%），且无文件扩展名
            if len(segments) >= 3:
                cn_count = sum(1 for s in segments if re.match(r'^[一-鿿]+$', s))
                has_ext = any('.' in s for s in segments)
                if cn_count / len(segments) > 0.6 and not has_ext:
                    return True
        # v3.1 纯英文/数字短标识符（不是路径）
        if re.match(r'^[a-zA-Z0-9_\-]+$', path_str) and len(path_str) < 20:
            return True
        return False

    def _build_projects_index(self):
        """构建 projects/ 下已知路径索引（用于上下文感知查找）"""
        if hasattr(self, '_proj_index'):
            return self._proj_index
        self._proj_index = {}
        proj_dir = self.workspace / 'projects'
        if proj_dir.exists():
            for root, dirs, files in os.walk(proj_dir):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for f in files:
                    full = os.path.join(root, f)
                    try:
                        rel = os.path.relpath(full, proj_dir)
                        parts = Path(rel).parts
                        # 处理两种项目命名格式：
                        # 1. proj-xxx/子目录/文件  → 去掉 proj-xxx 层
                        # 2. 20260425-名称/子目录/文件 → 去掉日期-名称层
                        # 3. _shared/文件 → 保留
                        if len(parts) > 1:
                            top = parts[0]
                            if top.startswith('proj-') or re.match(r'^\d{8}-', top):
                                # 去掉顶层项目目录
                                if len(parts) > 2:
                                    short = str(Path(*parts[1:]))
                                else:
                                    short = parts[-1]
                            elif top in ('_shared', 'PPT', '归档'):
                                short = str(Path(*parts))
                            else:
                                short = str(Path(*parts))
                            # 统一用 / 作为 key（与 CLAUDE.md 中的路径格式一致）
                            key = short.replace('\\', '/').lower()
                            self._proj_index[key] = full
                    except ValueError:
                        pass
        return self._proj_index

    def normalize_and_resolve(self, path_str, source_file):
        """
        v3.1 上下文感知：返回 (resolved_path, exists, suggestion)
        尝试顺序：
        1. 绝对路径 → 直接检查
        2. 源文件同目录 / 源文件的父目录链
        3. 工作区根目录
        4. .claude/rules/（隐式引用）
        5. projects/ 下搜索
        """
        path_str = path_str.strip().strip('"\'`')
        while path_str and path_str[-1] in '）)。，,；;、':
            path_str = path_str[:-1]
        if '#' in path_str:
            path_str = path_str.split('#')[0]
        if len(path_str) < 4:
            return None, False, None

        # 绝对路径
        if re.match(r'^[A-Za-z]:\\', path_str):
            p = Path(path_str)
            return p, p.exists(), None
        # ~/ 路径
        if path_str.startswith('~'):
            p = Path(path_str.replace('~', str(Path.home()), 1))
            return p, p.exists(), None

        # 相对路径：多上下文查找
        source_dir = Path(source_file).parent if source_file else self.workspace

        candidates = [
            source_dir / path_str,           # 源文件同目录
            self.workspace / path_str,        # 工作区根目录
        ]
        # 源文件向上 3 层目录
        parent = source_dir
        for _ in range(3):
            parent = parent.parent
            if parent == self.workspace or parent == parent.parent:
                break
            candidates.append(parent / path_str)

        # .claude/rules/ 隐式引用（短文件名如 script-safety-check.md）
        if '/' not in path_str and '\\' not in path_str and path_str.endswith('.md'):
            candidates.append(self.workspace / '.claude' / 'rules' / path_str)

        # 检查所有候选
        for c in candidates:
            if c.exists():
                return c, True, None

        # 都不存在 → 找建议
        suggestion = self._find_in_projects(path_str)
        return candidates[0], False, suggestion

    def _find_in_projects(self, path_str):
        """在 projects/ 下查找匹配路径"""
        proj_index = self._build_projects_index()
        # 统一用 / 作为 key
        key = path_str.lower().replace('\\', '/')
        # 精确匹配
        if key in proj_index:
            return proj_index[key]
        # 文件名匹配
        name = Path(path_str).name.lower()
        for k, v in proj_index.items():
            if k.endswith('/' + name) or k == name:
                return v
        return None

    def path_exists(self, path):
        """检查路径是否存在"""
        if path.exists():
            return True
        p = str(path)
        if p.endswith('/') or p.endswith('\\'):
            if Path(p.rstrip('/\\')).exists():
                return True
        return False

    def classify_severity(self, path_str, source_file):
        """严重度分级"""
        src = str(source_file).lower()
        # HIGH: 核心文件 / SOP / 规则中的 .md/.yaml
        if any(kw in src for kw in ['claude.md', 'agent.md', 'runtime-snapshot']):
            return 'high'
        if ('sop' in src or 'rules' in src) and path_str.endswith(('.md', '.yaml', '.yml')):
            return 'high'
        if 'skill' in src and path_str.endswith(('.md', '.yaml')):
            return 'high'
        # MEDIUM: 目录引用或 .md
        if '.' not in Path(path_str).name or path_str.endswith('.md'):
            return 'medium'
        return 'low'

    def extract_paths_from_file(self, filepath):
        """提取路径引用"""
        paths = []
        try:
            if os.path.getsize(filepath) > MAX_FILE_SIZE:
                return paths
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, OSError):
            return paths

        for line_no, line in enumerate(content.splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            # 1. 反引号中的路径
            for match in re.finditer(r'`([^`]{4,})`', line):
                val = match.group(1)
                if self._looks_like_path(val):
                    paths.append((line_no, val))

            # 2. 绝对路径
            for match in re.finditer(r'[A-Za-z]:\\[^\s"\'|`，。；）“”]+', line):
                paths.append((line_no, match.group(0)))

            # 3. 相对路径（已知前缀开头）
            for prefix in KNOWN_PREFIXES:
                escaped = re.escape(prefix)
                for match in re.finditer(rf'({escaped}[^\s`"\'|，。；）“”]+)', line):
                    val = match.group(1)
                    # 去尾部标点
                    val = val.rstrip('。，,；;、）)')
                    if len(val) > len(prefix) + 1:
                        paths.append((line_no, val))

        return paths

    def _looks_like_path(self, val):
        """判断是否像路径"""
        if len(val) < 4:
            return False
        if is_cli_command(val):
            return False
        if '/' in val or '\\' in val:
            return True
        if re.search(r'\.(md|yaml|yml|json|py|sh|txt|html|css|js|ps1|bat)$', val, re.I):
            return True
        return False

    def scan_file(self, filepath):
        """扫描单个文件（v3.1：上下文感知解析）"""
        self.files_scanned += 1
        if self.verbose and self.files_scanned % 50 == 0:
            print(f"   ... {self.files_scanned} files scanned")

        for line_no, path_str in self.extract_paths_from_file(filepath):
            self.stats['total_paths'] += 1

            if self.should_skip_path(path_str):
                self.stats['filtered'] += 1
                continue

            resolved, exists, suggestion = self.normalize_and_resolve(path_str, filepath)
            if resolved is None:
                self.stats['filtered'] += 1
                continue

            if exists:
                self.stats['alive'] += 1
            else:
                severity = self.classify_severity(path_str, filepath)
                # 格式化建议路径
                sugg_str = None
                if suggestion:
                    try:
                        sugg_str = str(Path(suggestion).relative_to(self.workspace))
                    except ValueError:
                        sugg_str = str(Path(suggestion).name)
                self.dead_paths.append({
                    'source': str(filepath),
                    'line': line_no,
                    'path': path_str,
                    'abs_path': str(resolved),
                    'severity': severity,
                    'suggestion': sugg_str,
                })
                self.stats['dead'] += 1
                self.stats[f'dead_{severity}'] += 1

    def scan_targets(self, targets, max_depth=6):
        """扫描目标列表（文件或目录）"""
        for target in targets:
            p = self.workspace / target if not Path(target).is_absolute() else Path(target)
            if p.is_file() and p.exists():
                self.scan_file(p)
            elif p.is_dir() and p.exists():
                self._scan_dir(p, 0, max_depth)

    def _scan_dir(self, dir_path, depth, max_depth):
        if depth > max_depth:
            return
        try:
            entries = sorted(dir_path.iterdir())
        except (PermissionError, OSError):
            return
        for entry in entries:
            if entry.is_dir():
                if entry.name in SKIP_DIRS:
                    continue
                if entry.name.startswith('.') and entry.name != '.claude':
                    continue
                self._scan_dir(entry, depth + 1, max_depth)
            elif entry.is_file() and entry.suffix in ('.md', '.yaml', '.yml', '.json'):
                self.scan_file(entry)

    def find_suggestions(self, dead_path_str):
        """在文件索引中查找同名文件作为修复建议"""
        if self.file_index is None:
            self._build_file_index()
        name = Path(dead_path_str).name
        if not name:
            return []
        suggestions = []
        for indexed in self.file_index:
            if indexed.endswith(name) or indexed.endswith(name + '\\') or indexed.endswith(name + '/'):
                try:
                    rel = str(Path(indexed).relative_to(self.workspace))
                except ValueError:
                    rel = str(Path(indexed).name)
                if rel not in suggestions:
                    suggestions.append(rel)
        return suggestions[:3]

    def run(self, mode='extended'):
        """执行扫描 mode: quick/extended/full"""
        print(f"Dead Path Scanner v3.1 [{mode}]")
        print(f"   Workspace: {self.workspace}")
        print(f"   Time:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        if mode == 'quick':
            # 只扫核心文件
            for fname in CORE_FILES:
                fpath = self.workspace / fname
                if fpath.exists():
                    self.scan_file(fpath)
        else:
            # 扫描根目录文件
            for fname in ROOT_FILES:
                fpath = self.workspace / fname
                if fpath.exists():
                    self.scan_file(fpath)
            # 扫描目录
            dirs = FULL_DIRS if mode == 'full' else EXTENDED_DIRS
            for d in dirs:
                p = self.workspace / d
                if p.exists():
                    self._scan_dir(p, 0, 6)
                    self.stats['scanned_dirs'] += 1
            # skills 目录：只扫描用户自建的 skill（含 workspace 引用的）
            # （第三方 SKILL.md 中大多是教学示例，会产生大量误报）
            user_skills = ['siyuliebian', 'opc-private-domain', 'koubo-script-writer']
            if SKILLS_DIR.exists():
                for skill_name in user_skills:
                    skill_dir = SKILLS_DIR / skill_name
                    if skill_dir.exists():
                        for f in skill_dir.iterdir():
                            if f.is_file() and f.suffix in ('.md', '.json'):
                                self.scan_file(f)
            # --full 模式扫描全部 skills
            if mode == 'full' and SKILLS_DIR.exists():
                for root, _, files in os.walk(SKILLS_DIR):
                    for f in files:
                        if f in ('SKILL.md', '_meta.json'):
                            fp = os.path.join(root, f)
                            if fp not in {str(SKILLS_DIR / s / 'SKILL.md') for s in user_skills}:
                                self.scan_file(fp)

        print(f"\nResult: {self.files_scanned} files | "
              f"{self.stats['total_paths']} paths | "
              f"{self.stats['alive']} valid | "
              f"{self.stats['filtered']} filtered | "
              f"{self.stats['dead']} dead")

        return self.generate_report()

    def generate_report(self):
        """生成 Markdown 报告"""
        lines = []
        lines.append("# Dead Path Scan Report")
        lines.append(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # 摘要
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- Files scanned: **{self.files_scanned}**")
        lines.append(f"- Paths found: {self.stats['total_paths']}")
        lines.append(f"- Valid: {self.stats['alive']}")
        lines.append(f"- Filtered: {self.stats['filtered']}")
        lines.append(f"- **Dead: {self.stats['dead']}**")
        lines.append(f"  - 🔴 HIGH: {self.stats.get('dead_high', 0)}")
        lines.append(f"  - 🟡 MEDIUM: {self.stats.get('dead_medium', 0)}")
        lines.append(f"  - 🟢 LOW: {self.stats.get('dead_low', 0)}")
        lines.append("")

        if not self.dead_paths:
            lines.append("**No dead paths found. All references are valid.**")
            return '\n'.join(lines)

        # 按严重度分组
        by_severity = defaultdict(list)
        for entry in self.dead_paths:
            by_severity[entry['severity']].append(entry)

        for severity in ['high', 'medium', 'low']:
            entries = by_severity.get(severity, [])
            if not entries:
                continue
            label = {'high': '🔴 HIGH', 'medium': '🟡 MEDIUM', 'low': '🟢 LOW'}[severity]
            lines.append(f"## {label} ({len(entries)})")
            lines.append("")

            # 按源文件分组
            by_file = defaultdict(list)
            for e in entries:
                try:
                    rel = str(Path(e['source']).relative_to(self.workspace))
                except ValueError:
                    rel = Path(e['source']).name
                by_file[rel].append(e)

            for source in sorted(by_file.keys()):
                file_entries = by_file[source]
                lines.append(f"### `{source}` ({len(file_entries)} dead)")
                lines.append("")
                lines.append("| Line | Dead Path | Suggestion |")
                lines.append("|------|-----------|------------|")
                for e in sorted(file_entries, key=lambda x: x['line']):
                    sugg = e.get('suggestion')
                    if sugg:
                        sugg = f"→ `{sugg}`"
                    else:
                        sugg = "—"
                    lines.append(f"| {e['line']} | `{e['path']}` | {sugg} |")
                lines.append("")

        # 热点统计
        dead_dirs = defaultdict(int)
        for e in self.dead_paths:
            parent = Path(e['abs_path']).parent.name
            if parent:
                dead_dirs[parent] += 1
        if dead_dirs:
            lines.append("## Dead Path Hotspots")
            lines.append("")
            for dir_name, count in sorted(dead_dirs.items(), key=lambda x: -x[1])[:10]:
                lines.append(f"- `{dir_name}/` — {count} references")
            lines.append("")

        return '\n'.join(lines)

    def generate_fix_script(self):
        """生成修复建议（JSON 格式，方便后续自动化）"""
        fixes = []
        for e in self.dead_paths:
            if e['severity'] in ('high', 'medium'):
                suggestions = self.find_suggestions(e['path'])
                fixes.append({
                    'file': e['source'],
                    'line': e['line'],
                    'old_path': e['path'],
                    'severity': e['severity'],
                    'suggestions': suggestions,
                })
        return fixes


def is_cli_command(val):
    """CLI 命令检测"""
    stripped = val.strip().lower()
    cli_prefixes = [
        'python ', 'pip ', 'npm ', 'npx ', 'node ', 'git ', 'gh ',
        'bash ', 'sh ', 'powershell ', 'cmd ', 'cd ', 'ls ', 'cat ',
        'echo ', 'curl ', 'wget ', 'chmod ', 'rm ', 'cp ', 'mv ',
    ]
    return any(stripped.startswith(p) for p in cli_prefixes)


def main():
    parser = argparse.ArgumentParser(
        description='Dead Path Scanner v3.0 — SOP/规则文件断链检测')
    parser.add_argument('--report', action='store_true',
                        help='Save report to outputs/dead-path-report.md')
    parser.add_argument('--fix', action='store_true',
                        help='Generate fix suggestions as JSON')
    parser.add_argument('--severity', choices=['high', 'medium', 'low', 'all'],
                        default='all', help='Filter severity (default: all)')
    parser.add_argument('--quick', action='store_true',
                        help='Quick mode: only scan core files (<5s)')
    parser.add_argument('--full', action='store_true',
                        help='Full mode: scan all directories')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    mode = 'quick' if args.quick else ('full' if args.full else 'extended')
    scanner = DeadPathScanner(verbose=args.verbose)
    report = scanner.run(mode)

    # 严重度过滤
    if args.severity != 'all':
        sev_map = {'high': 'HIGH', 'medium': 'MEDIUM', 'low': 'LOW'}
        target = sev_map[args.severity]
        filtered_lines = []
        keep = True
        for line in report.split('\n'):
            if line.startswith('## '):
                if 'HIGH' in line or 'MEDIUM' in line or 'LOW' in line:
                    keep = target in line
                elif 'Summary' in line or 'Hotspot' in line:
                    keep = True
            if keep:
                filtered_lines.append(line)
        report = '\n'.join(filtered_lines)

    # 输出
    if args.fix:
        fixes = scanner.generate_fix_script()
        fix_path = WORKSPACE / 'outputs' / 'dead-path-fixes.json'
        fix_path.parent.mkdir(parents=True, exist_ok=True)
        with open(fix_path, 'w', encoding='utf-8') as f:
            json.dump(fixes, f, ensure_ascii=False, indent=2)
        print(f"\nFix suggestions: {fix_path} ({len(fixes)} items)")
    elif args.report:
        report_path = WORKSPACE / 'outputs' / 'dead-path-report.md'
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nReport saved: {report_path}")
    else:
        print()
        print(report)

    sys.exit(1 if scanner.stats['dead'] > 0 else 0)


if __name__ == '__main__':
    main()
