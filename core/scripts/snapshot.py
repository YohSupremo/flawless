#!/usr/bin/env python3
"""Version history for /edit and /revert.

Usage:
  python scripts/snapshot.py save page.html     copy current file to page.history/vN.html
  python scripts/snapshot.py list page.html     list saved versions
  python scripts/snapshot.py restore page.html [N]   restore version N (default: latest)
Restoring first saves the current file, so a restore can itself be undone.
"""
import sys, os, re, shutil

def hist_dir(p):
    root, _ = os.path.splitext(p)
    return root + ".history"

def versions(p):
    d = hist_dir(p)
    if not os.path.isdir(d):
        return []
    return sorted(int(m.group(1)) for f in os.listdir(d) if (m := re.fullmatch(r"v(\d+)\.html", f)))

def save(p):
    d = hist_dir(p)
    os.makedirs(d, exist_ok=True)
    v = (versions(p) or [0])[-1] + 1
    shutil.copy2(p, os.path.join(d, f"v{v}.html"))
    return v


def restore_file(p, n):
    """Copy version n over the page through a temp file, so an interrupted restore never leaves half a page."""
    tmp = p + ".restore.tmp"
    shutil.copy2(os.path.join(hist_dir(p), f"v{n}.html"), tmp)
    os.replace(tmp, p)

def main(a):
    if len(a) < 2:
        sys.exit(__doc__)
    cmd, p = a[0], a[1]
    if cmd in ("save", "restore") and not os.path.isfile(p):
        sys.exit(f"page not found: {p}")
    if cmd == "save":
        print(f"saved v{save(p)}")
    elif cmd == "list":
        vs = versions(p)
        print("versions:", ", ".join(f"v{v}" for v in vs) if vs else "none")
    elif cmd == "restore":
        vs = versions(p)
        if not vs:
            sys.exit("no versions saved")
        n = int(a[2]) if len(a) > 2 else vs[-1]
        if n not in vs:
            sys.exit(f"v{n} not found")
        save(p)
        restore_file(p, n)
        print(f"restored v{n}")
    else:
        sys.exit(__doc__)

if __name__ == "__main__":
    main(sys.argv[1:])
