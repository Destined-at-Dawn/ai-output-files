"""Copy .claude/rules/ from mutual to all 4 other workspaces."""
import shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')

source = r"E:\ai产出文件\牛马\mutual\mutual\.claude\rules"
targets = [
    r"E:\ai产出文件\牛马\个人\个人\.claude\rules",
    r"E:\ai产出文件\牛马\创作\创作\.claude\rules",
    r"E:\ai产出文件\牛马\求职\求职\.claude\rules",
    r"E:\ai产出文件\牛马\竞赛\竞赛\.claude\rules",
]

for t in targets:
    os.makedirs(t, exist_ok=True)
    print(f"[DIR] {t}")
    count = 0
    for f in os.listdir(source):
        if f.endswith('.md'):
            src_file = os.path.join(source, f)
            dst_file = os.path.join(t, f)
            shutil.copy2(src_file, dst_file)
            size = os.path.getsize(dst_file)
            print(f"  OK {f} ({size} bytes)")
            count += 1
    print(f"  TOTAL: {count} files copied")

print("\n=== VERIFICATION ===")
for t in targets:
    files = [f for f in os.listdir(t) if f.endswith('.md')]
    print(f"{t}: {len(files)} .md files")
    for f in sorted(files):
        print(f"  - {f}")
