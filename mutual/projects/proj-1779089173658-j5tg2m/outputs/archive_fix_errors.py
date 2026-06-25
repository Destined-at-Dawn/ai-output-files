"""Fix remaining archive errors: symlinks + git-locked dirs"""
import os, shutil, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

SKILLS_DIR = Path(r"C:\Users\13975\.newmax\skills")
ARCHIVE_DIR = Path(r"E:\ai产出文件\归档\deprecated-skills-phase2-20260611")

# 1. Symlinks - just unlink them (they point somewhere else)
SYMLINKS = ["copywriting-skills", "humanizer-zh", "image-editing",
            "jiaying-tool", "qiaomu-mondo-poster-design", "short-video-production"]

for name in SYMLINKS:
    p = SKILLS_DIR / name
    if p.exists() or p.is_symlink():
        try:
            if p.is_symlink():
                os.unlink(str(p))
                print(f"  UNLINK symlink: {name}")
            else:
                # Not a symlink, try regular move
                shutil.move(str(p), str(ARCHIVE_DIR / name))
                print(f"  MOVED: {name}")
        except Exception as e:
            print(f"  SKIP {name}: {e}")
    else:
        print(f"  NOT FOUND: {name}")

# 2. Git-locked dirs - remove .git first then move
GIT_LOCKED = ["ex-skill", "follow-builders", "guizang-ppt-skill", "nuwa-skill"]

for name in GIT_LOCKED:
    src = SKILLS_DIR / name
    if not src.exists():
        print(f"  NOT FOUND: {name}")
        continue

    git_dir = src / ".git"
    if git_dir.exists():
        try:
            # Make .git files writable first
            for root, dirs, files in os.walk(str(git_dir)):
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        os.chmod(fp, 0o777)
                    except:
                        pass
            shutil.rmtree(str(git_dir))
            print(f"  Removed .git from: {name}")
        except Exception as e:
            print(f"  Cannot remove .git from {name}: {e}")
            # Try to move without .git
            try:
                dst = ARCHIVE_DIR / name
                # Copy non-git files, then remove source
                shutil.copytree(str(src), str(dst), ignore=shutil.ignore_patterns('.git'))
                shutil.rmtree(str(src))
                print(f"  COVED (without .git): {name}")
                continue
            except Exception as e2:
                print(f"  FAILED {name}: {e2}")
                continue

    try:
        shutil.move(str(src), str(ARCHIVE_DIR / name))
        print(f"  MOVED: {name}")
    except Exception as e:
        print(f"  FAILED {name}: {e}")

# Final count
remaining = [d.name for d in SKILLS_DIR.iterdir() if d.is_dir()]
li_count = len([s for s in remaining if s.startswith('li-')])
non_li = sorted([s for s in remaining if not s.startswith('li-')])

print(f"\n=== Final State ===")
print(f"Total: {len(remaining)}")
print(f"li- series: {li_count}")
print(f"Non li-: {len(non_li)}")
print(f"\nNon li- list:")
for s in non_li:
    print(f"  {s}")
