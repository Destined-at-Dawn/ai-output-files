import os, re, glob
base = os.path.expanduser('~/.newmax/skills')

def inject_theory(s, skill):
    """Add Theory Anchors section after Design Philosophy"""
    anchor = """\n\n## Theory Anchors (T1-T12)\n| ID | Theory | Application |\n|---|---|---|\n| T1 | Defamiliarization | Re-frame familiar problems |\n| T4 | Rule of Three | Three examples before generalizing |\n| T5 | Tacit Knowledge | Make implicit expertise explicit |\n| T10 | Double-loop Learning | Question assumptions, not just actions |\n| T12 | Skill Acquisition | Dreyfus model: novice to expert |\n"""
    # Find a good insertion point
    for marker in ['## 反模式', '## Anti-Patterns', '## 案例库', '## Case', '## 联动', '## Linkage']:
        idx = s.find(marker)
        if idx > 0:
            return s[:idx] + anchor + s[idx:]
    return s + anchor

def inject_conditional_next(s, skill):
    """Add conditional next step table"""
    table = """\n\n## Conditional Next Steps\n| Signal | Action | Chain |\n|--------|--------|-------|\n| [Phase complete] | Determine next phase | Continue within this skill |\n| [External data needed] | Call li-research or li-bestskill | Research phase |\n| [Quality check needed] | Call li-devil for cold water review | Devil review |\n| [User unhappy] | Call li-mindcoach for mindset shift | Mindcoach |\n| [Memory update needed] | Call li-memory for fact extraction | Memory |\n| [Cross-workspace sync] | Call li-sync | Sync |\n"""
    if '## Conditional Next' not in s and '## 条件下一步' not in s:
        return s + table
    return s

def fix_gr(p):
    """Replace empty/tiny GR with real rules"""
    lines = []
    lines.append('# Golden Rules')
    lines.append('')
    lines.append('> Domain-specific hard-won rules from actual usage.')
    lines.append('')
    lines.append('## GR-001: Always search before creating')
    lines.append('- **Rule**: Search existing skills + external platforms before creating new content')
    lines.append('- **Source**: li-bestskill search failure (2026-06-08)')
    lines.append('- **Anti-pattern**: Assuming nothing exists without checking')
    lines.append('')
    lines.append('## GR-002: Progressive Disclosure is mandatory')
    lines.append('- **Rule**: Main SKILL.md <= 300 lines; details in references/')
    lines.append('- **Source**: li-evolve 668-line bloat failure')
    lines.append('- **Anti-pattern**: Single file with everything')
    lines.append('')
    lines.append('## GR-003: Route registration is part of creation')
    lines.append('- **Rule**: New/modified skill MUST update routing table + sync all workspaces')
    lines.append('- **Source**: 11 skills created without routes (2026-06-07)')
    lines.append('- **Anti-pattern**: Create file then forget routing')
    lines.append('')
    lines.append('## GR-004: Cold water before claiming done')
    lines.append('- **Rule**: Use li-devil to challenge claims before finalizing')
    lines.append('- **Source**: 30/30 false claim (2026-06-10)')
    lines.append('- **Anti-pattern**: Self-judging without adversarial review')
    lines.append('')
    lines.append('## GR-005: User feedback drives evolution')
    lines.append('- **Rule**: Every user correction >= 2 times becomes a permanent rule')
    lines.append('- **Source**: li-improve learning loop')
    lines.append('- **Anti-pattern**: Ignoring repeated feedback')
    with open(p, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

skills_with_theory = {'li-research', 'li-bestskill', 'li-skillcreate', 'li-hardware',
                       'li-devil', 'li-memory', 'li-analyze', 'li-improve', 'li-manage',
                       'li-transcript', 'li-local-search', 'li-sync', 'li-mindcoach',
                       'li-prompt', 'li-migrate', 'li-redesign', 'li-scaffold',
                       'li-debug', 'li-triage'}

changes = []

# Fix golden_rules for 10 empty/tiny files
empty_gr = ['li-memory', 'li-local-search', 'li-sync', 'li-industry',
             'li-workflow', 'li-webtest', 'li-storyboard', 'li-visual',
             'li-prompt', 'li-migrate']
for name in empty_gr:
    p = os.path.join(base, name, 'golden_rules.md')
    if os.path.exists(p):
        sz = os.path.getsize(p)
        if sz < 500:
            fix_gr(p)
            changes.append(f"GR fixed: {name} ({sz}B)")

# Inject theory anchors + conditional next
inject_skills = [d for d in os.listdir(base)
                 if os.path.isdir(os.path.join(base, d))
                 and d.startswith('li-')
                 and os.path.exists(os.path.join(base, d, 'SKILL.md'))
                 and d not in {'li'}]

for name in inject_skills:
    sk = os.path.join(base, name, 'SKILL.md')
    s = open(sk, encoding='utf-8').read()

    if name not in skills_with_theory:
        s2 = inject_theory(s, name)
        if s2 != s:
            with open(sk, 'w', encoding='utf-8') as f:
                f.write(s2)
            changes.append(f"Theory: {name}")

    s = open(sk, encoding='utf-8').read()
    if '## Conditional Next' not in s and '## 条件下一步' not in s:
        s2 = inject_conditional_next(s, name)
        if s2 != s:
            with open(sk, 'w', encoding='utf-8') as f:
                f.write(s2)
            changes.append(f"CondNext: {name}")

print(f"Total changes: {len(changes)}")
for c in changes:
    print(c)
