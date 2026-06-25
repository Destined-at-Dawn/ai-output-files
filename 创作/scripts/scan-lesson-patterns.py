#!/usr/bin/env python3
"""教训模式自动扫描器（v3.3 新增——v1组件→v2连接→v3硬约束→v3.3闭环）

扫描所有经验库教训文件，自动检测：
  1. 重复模式（同一关键词出现在≥2篇教训中 → 标记为"应升级"）
  2. C级预防占比（无"系统加固动作"章节的教训 → 仅为记录 = C级 = 无效）
  3. 升级建议（同类≥3次 → 建议升级为铁律；≥5次 → 建议新建独立SOP）
  4. INDEX覆盖率

用法：
  python scripts/scan-lesson-patterns.py                # 完整报告
  python scripts/scan-lesson-patterns.py --brief        # 仅摘要
  python scripts/scan-lesson-patterns.py --promotions   # 仅升级建议

设计原则：
  - 纯 Python，避免中文路径编码问题
  - 输出可直接作为 self-improving Phase 0.5 的输入
  - 纳入 F1 审计的"被忽视的"自动检测链

v3.3 来源：v1(组件)→v2(连接)→v3(硬约束)演进后，发现"谁监督监督者"的自举问题——
        F1/F6的硬约束本身也需要被监督，本脚本是自举机制的执行层。
"""

import os, re, sys, json
from collections import Counter, defaultdict
from datetime import datetime

# ─── 配置 ───
ROOT = r'E:\ai产出文件\牛马\创作\创作'
EXP_BAD = os.path.join(ROOT, 'projects', '20260425-内容创作系统', '社群运营', '经验库', '做得差的')
EXP_GOOD = os.path.join(ROOT, 'projects', '20260425-内容创作系统', '社群运营', '经验库', '做得好的')
SELF_EVO_BAD = os.path.join(ROOT, '自我进化', '做得差的避免')
SELF_EVO_GOOD = os.path.join(ROOT, '自我进化', '做得好的')
INDEX_PATH = os.path.join(ROOT, '自我进化', 'INDEX.md')

# ─── 关键词→模式映射（正则）───
PATTERNS = {
    'SOP流程遗漏': r'SOP|流程|步骤遗漏|检查清单|checklist',
    '文件操作违规': r'Write|Edit|文件操作|Write后Read|先Read|落盘|文件路径|覆盖',
    '双写同步断裂': r'双写|dual.write|同步率|验证脚本|模块级.*经验库',
    'F8路由跳过': r'F8|路由|技能链|dbs-content|内容创作.*路由|品牌档案|约束文件',
    '飞书API/权限': r'飞书|feishu|API.*权限|文档创建|wiki|tenant|权限失败',
    '中文编码陷阱': r'编码|中文路径|PowerShell.*中文|Bash.*中文|heredoc|GBK|UTF-8',
    '归档遗漏': r'归档|备份|git.*commit|checkpoint|恢复|删除.*归档',
    'INDEX失修': r'INDEX|索引|注册表|技能注册|SOP总索引',
    '格式转换伪装': r'HTML|MD|txt|格式转换|格式伪装|HTML.*转|转.*MD',
    '对话输出当交付': r'对话输出|没落盘|没写文件|只输出|只说了|没有Write|没执行',
    '跨人物污染': r'嘉宾|归属|人名|见名即停|映射|谁说的|作者',
    '高压崩塌': r'高压|半小时|马上|就要|跳过.*步骤|省略',
}

# ─── 升级规则（来自 CLAUDE.md §五 升级规则）───
PROMOTION_RULES = {
    1: '记录到自我进化 + SOP迭代日志',
    2: 'SOP对应步骤旁加 高频坑标记',
    3: '升级为铁律，更新 CLAUDE.md',
    5: '评估是否需要新建独立 SOP/Skill',
}

# ─── 核心函数 ───

def scan_directory(directory):
    """扫描单个目录，返回 (文件列表, 内容dict)"""
    files = {}
    if not os.path.exists(directory):
        return files
    for f in sorted(os.listdir(directory)):
        if f.endswith('.md'):
            path = os.path.join(directory, f)
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                files[f] = {'path': path, 'content': content, 'size': len(content)}
            except Exception as e:
                print(f'  [WARN] Cannot read {f}: {e}')
    return files


def detect_patterns(files_dict):
    """对所有文件做关键词模式匹配"""
    results = defaultdict(list)
    for fname, info in files_dict.items():
        content = info['content']
        for pattern_name, regex in PATTERNS.items():
            if re.search(regex, content, re.IGNORECASE):
                results[pattern_name].append(fname)
    return dict(results)


def detect_c_level_prevention(files_dict):
    """检测C级预防占比——缺少"系统加固动作"章节的教训"""
    c_level = []
    a_level = []
    for fname, info in files_dict.items():
        content = info['content']
        has_system_fix = bool(re.search(
            r'系统加固|硬约束.*注入|CLAUDE\.md.*修改|修改了.*文件|规则.*注入|铁律.*新增|路由表.*新增',
            content, re.IGNORECASE))
        if has_system_fix:
            a_level.append(fname)
        else:
            c_level.append(fname)
    return c_level, a_level


def generate_promotions(pattern_hits):
    """根据出现次数生成升级建议"""
    promotions = {}
    for pattern_name, files in sorted(pattern_hits.items(), key=lambda x: -len(x[1])):
        count = len(files)
        if count >= 5:
            promotions[pattern_name] = {
                'count': count,
                'action': PROMOTION_RULES[5],
                'severity': 'critical',
                'files': files,
            }
        elif count >= 3:
            promotions[pattern_name] = {
                'count': count,
                'action': PROMOTION_RULES[3],
                'severity': 'high',
                'files': files,
            }
        elif count >= 2:
            promotions[pattern_name] = {
                'count': count,
                'action': PROMOTION_RULES[2],
                'severity': 'medium',
                'files': files,
            }
    return promotions


def check_index_coverage():
    """检查 INDEX.md 覆盖率"""
    if not os.path.exists(INDEX_PATH):
        return {'status': 'MISSING', 'gaps': [], 'total': 0, 'covered': 0}

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        idx_content = f.read()

    all_files = {}
    for d in [SELF_EVO_BAD, SELF_EVO_GOOD]:
        if os.path.exists(d):
            for f in os.listdir(d):
                if f.endswith('.md'):
                    all_files[f] = f in idx_content

    total = len(all_files)
    covered = sum(1 for v in all_files.values() if v)
    gaps = [f for f, covered_flag in all_files.items() if not covered_flag]
    return {
        'status': 'OK' if not gaps else 'GAPS',
        'total': total, 'covered': covered, 'gaps': gaps,
        'coverage_pct': round(covered / total * 100, 1) if total > 0 else 100,
    }


def check_dual_write():
    """快速双写同步检查（不跑完整 verify，只做文件存在性检查）"""
    module_bad = set()
    root_bad = set()

    if os.path.exists(EXP_BAD):
        module_bad = {f for f in os.listdir(EXP_BAD) if f.endswith('.md')}
    if os.path.exists(SELF_EVO_BAD):
        root_bad = {f for f in os.listdir(SELF_EVO_BAD) if f.endswith('.md')}

    only_module = module_bad - root_bad
    only_root = root_bad - module_bad
    both = module_bad & root_bad

    return {
        'status': 'OK' if not only_module and not only_root else 'GAPS',
        'module_only': list(only_module),
        'root_only': list(only_root),
        'synced': len(both),
        'total_module': len(module_bad),
        'total_root': len(root_bad),
    }


# ─── 主报告 ───

def main():
    brief = '--brief' in sys.argv
    promotions_only = '--promotions' in sys.argv

    # 1. 扫描
    bad_files = scan_directory(EXP_BAD)
    good_files = scan_directory(EXP_GOOD)

    # 2. 模式检测
    bad_patterns = detect_patterns(bad_files)

    # 3. C级预防检测
    c_level, a_level = detect_c_level_prevention(bad_files)
    c_pct = round(len(c_level) / len(bad_files) * 100, 1) if bad_files else 0

    # 4. 升级建议
    promotions = generate_promotions(bad_patterns)

    # 5. INDEX检查
    idx_status = check_index_coverage()

    # 6. 双写检查
    dw_status = check_dual_write()

    if promotions_only:
        print('\n升级建议（按严重程度排序）')
        print('=' * 60)
        for pname, pinfo in sorted(promotions.items(), key=lambda x: -x[1]['count']):
            sev_icon = {'critical': '5+', 'high': '3+', 'medium': '2'}[pinfo['severity']]
            print(f'\n[{sev_icon}] {pname}: {pinfo["count"]}篇 → {pinfo["action"]}')
            if not brief:
                for f in pinfo['files'][:5]:
                    print(f'    - {f}')
                if len(pinfo['files']) > 5:
                    print(f'    ... 还有 {len(pinfo["files"]) - 5} 篇')
        return 0

    # 完整报告
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f'\n{"=" * 60}')
    print(f'教训模式自动扫描报告 — {now}')
    print(f'{"=" * 60}')

    print(f'\n一、数据总览')
    print(f'  失败教训: {len(bad_files)} 篇')
    print(f'  成功经验: {len(good_files)} 篇')

    print(f'\n二、预防级别分布')
    print(f'  A级（有系统加固）: {len(a_level)} 篇 ({round(len(a_level)/max(len(bad_files),1)*100,1)}%)')
    print(f'  C级（仅记录）    : {len(c_level)} 篇 ({c_pct}%)')
    if c_pct > 30:
        print(f'  WARNING: C级预防>30%——系统仍在退化，教训为白记')
    elif c_pct > 15:
        print(f'  CAUTION: C级预防>15%——需加速A级转换')

    print(f'\n三、模式分布（Top 10）')
    for pname, files in sorted(bad_patterns.items(), key=lambda x: -len(x[1]))[:10]:
        pct = round(len(files) / len(bad_files) * 100, 1)
        bar = '█' * int(pct / 5)
        print(f'  {pname:20s} {len(files):3d}篇 ({pct:5.1f}%) {bar}')

    print(f'\n四、INDEX覆盖率')
    print(f'  {idx_status["covered"]}/{idx_status["total"]} ({idx_status["coverage_pct"]}%)')
    if idx_status['gaps']:
        print(f'  GAPS: {len(idx_status["gaps"])} 个文件不在INDEX中')

    print(f'\n五、双写同步')
    print(f'  同步: {dw_status["synced"]} 篇')
    if dw_status['module_only']:
        print(f'  仅模块级: {len(dw_status["module_only"])} 篇 ← 需同步到根级')
    if dw_status['root_only']:
        print(f'  仅根级: {len(dw_status["root_only"])} 篇 ← 需同步到模块级')

    print(f'\n六、升级建议')
    if promotions:
        for pname, pinfo in sorted(promotions.items(), key=lambda x: -x[1]['count']):
            sev = pinfo['severity']
            icon = {'critical': '!!', 'high': '!', 'medium': '~'}[sev]
            print(f'  [{icon}] {pname}: {pinfo["count"]}篇 → {pinfo["action"]}')
    else:
        print(f'  无需要升级的模式')

    # 健康分
    health = 100
    if c_pct > 30: health -= 20
    elif c_pct > 15: health -= 10
    if idx_status['coverage_pct'] < 95: health -= 10
    if idx_status['coverage_pct'] < 80: health -= 15
    if dw_status['module_only']: health -= 10
    if dw_status['root_only']: health -= 10
    print(f'\n七、系统健康分: {health}/100')
    if health < 60:
        print(f'  STATUS: CRITICAL — 系统存在严重退化风险')
    elif health < 80:
        print(f'  STATUS: WARNING — 需要立即关注')
    else:
        print(f'  STATUS: OK')

    return 0 if health >= 60 else 1


if __name__ == '__main__':
    sys.exit(main())
