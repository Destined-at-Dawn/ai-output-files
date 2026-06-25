import os

skills_dir = os.path.expanduser('~/.newmax/skills')

def move_to_refs(skill_name, section_markers, ref_filename, ref_header):
    """Move sections from main SKILL.md to references/"""
    skill_path = os.path.join(skills_dir, skill_name, 'SKILL.md')
    refs_dir = os.path.join(skills_dir, skill_name, 'references')
    os.makedirs(refs_dir, exist_ok=True)

    with open(skill_path, 'r', encoding='utf-8') as f:
        text = f.read()
    lines = text.split('\n')

    # Find section boundaries
    moved_content = []
    kept_lines = []
    in_section = False
    section_start = -1

    for i, line in enumerate(lines):
        is_section = False
        for marker in section_markers:
            if line.strip().startswith(marker):
                is_section = True
                break

        if is_section and not in_section:
            in_section = True
            section_start = i
            # Replace with summary line
            kept_lines.append(f"## {section_markers[0].replace('## ', '')} → 详见 `references/{ref_filename}`")
            kept_lines.append("")
            continue

        if in_section:
            # Check if next section starts
            if line.startswith('## ') and not any(line.strip().startswith(m) for m in section_markers):
                in_section = False
                kept_lines.append(line)
            else:
                moved_content.append(line)
            continue

        kept_lines.append(line)

    if not moved_content:
        print(f"  {skill_name}: no sections found to move")
        return

    # Write moved content to references
    ref_path = os.path.join(refs_dir, ref_filename)
    with open(ref_path, 'w', encoding='utf-8') as f:
        f.write(f"# {ref_header}\n\n")
        f.write('\n'.join(moved_content).strip() + '\n')

    # Write trimmed main file
    new_text = '\n'.join(kept_lines)
    # Remove double blank lines
    while '\n\n\n' in new_text:
        new_text = new_text.replace('\n\n\n', '\n\n')

    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(new_text)

    new_lines = len(new_text.split('\n'))
    print(f"  {skill_name}: moved {len(moved_content)} lines -> references/{ref_filename}, now {new_lines}L")

# Fix each over-limit skill by moving added content to references/

# li-research: move anti-patterns to references
move_to_refs('li-research', ['## 反模式'], 'anti-patterns-summary.md', '反模式速查（主文件摘要）')

# li-improve: move linked skills to references
move_to_refs('li-improve', ['## 联动技能'], 'linked-skills.md', '联动技能详解')

# li-industry: move cases + linked to references
move_to_refs('li-industry', ['## 案例库', '## 联动技能'], 'cases-and-linked.md', '案例库与联动技能')

# li-storyboard: move cases to references
move_to_refs('li-storyboard', ['## 案例库'], 'case-studies.md', '案例库详解')

# li-sync: move cases to references
move_to_refs('li-sync', ['## 案例库'], 'case-studies.md', '案例库详解')

# li-skillcreate: move anti-patterns to references
move_to_refs('li-skillcreate', ['## 反模式'], 'anti-patterns-summary.md', '反模式速查')

# Final verification
print("\n=== FINAL VERIFICATION ===")
import re
for d in sorted(os.listdir(skills_dir)):
    if not d.startswith('li-') or not os.path.isdir(os.path.join(skills_dir, d)):
        continue
    if os.path.exists(os.path.join(skills_dir, d, 'DEPRECATED.md')):
        continue
    skill_path = os.path.join(skills_dir, d, 'SKILL.md')
    if not os.path.exists(skill_path):
        continue
    with open(skill_path, 'r', encoding='utf-8') as f:
        text = f.read()
    lines = len(text.split('\n'))
    has_cases = bool(re.search(r'## (案例|Case Stud)', text))
    has_anti = bool(re.search(r'## (反模式|Anti)', text))
    has_linked = bool(re.search(r'## (联动|Linked)', text))
    has_ref_cases = os.path.exists(os.path.join(skills_dir, d, 'references', 'case-studies.md'))
    has_ref_anti = os.path.exists(os.path.join(skills_dir, d, 'references', 'anti-patterns-summary.md'))

    status = 'OK'
    if lines > 300:
        status = f'FAIL({lines}L)'
    elif not (has_cases or has_ref_cases):
        status = 'WARN(no-cases)'
    elif not (has_anti or has_ref_anti):
        status = 'WARN(no-anti)'

    print(f"{status} {d}: {lines}L")
