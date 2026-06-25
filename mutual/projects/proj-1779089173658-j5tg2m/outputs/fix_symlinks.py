"""Remove symlinked skills that can't be moved with shutil"""
import os, sys, subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

SKILLS_DIR = Path(r"C:\Users\13975\.newmax\skills")
SYMLINKS = ["copywriting-skills", "humanizer-zh", "image-editing",
            "jiaying-tool", "qiaomu-mondo-poster-design", "short-video-production"]

for name in SYMLINKS:
    p = SKILLS_DIR / name
    print(f"\n--- {name} ---")
    print(f"  exists: {p.exists()}")
    print(f"  is_symlink: {p.is_symlink()}")
    print(f"  is_dir: {p.is_dir()}")

    # Try os.unlink first
    try:
        os.unlink(str(p))
        print(f"  UNLINKED via os.unlink")
        continue
    except Exception as e:
        print(f"  os.unlink failed: {e}")

    # Try cmd rmdir (works on Windows symlinks/junctions)
    try:
        result = subprocess.run(["cmd", "/c", "rmdir", str(p)],
                                capture_output=True, text=True, timeout=10)
        print(f"  cmd rmdir: rc={result.returncode}, out={result.stdout.strip()}, err={result.stderr.strip()}")
        if result.returncode == 0:
            print(f"  REMOVED via cmd rmdir")
            continue
    except Exception as e:
        print(f"  cmd rmdir failed: {e}")

    # Try Python os.rmdir (works on empty dir symlinks)
    try:
        os.rmdir(str(p))
        print(f"  REMOVED via os.rmdir")
    except Exception as e:
        print(f"  os.rmdir failed: {e}")

# Final count
remaining = [d.name for d in SKILLS_DIR.iterdir() if d.is_dir() or d.is_symlink()]
print(f"\nRemaining: {len(remaining)}")
non_li = [s for s in remaining if not s.startswith('li-')]
print(f"Non li- ({len(non_li)}):")
for s in sorted(non_li):
    if s != 'skill-routing-table.json':
        print(f"  {s}")
