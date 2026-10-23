#!/usr/bin/env python3
"""Session state shared by all commands.

Usage:
  state.py init [--scheme-from page.html]   create state (or rebuild the scheme from a page)
  state.py show                             print the whole state
  state.py set KEY VALUE                    set a scheme key (base, surface, text, accent, font_display, font_body, radius)
  state.py page PATH [audit=clean|errors]   register a page and its last audit result
  state.py flag active on|off               turn session mode on or off
  state.py path                             print the state file in use

Where the state file lives (first match wins):
  1. $FLAWLESS_STATE                        explicit file path
  2. $CLEAN_UI_STATE                        legacy name, still honoured
  3. $FLAWLESS_PROJECT_ROOT/.flawless-state.json   project-scoped state
  4. ~/.clean-ui-state.json                 user-level default (legacy location)

Page paths are stored relative to $FLAWLESS_PROJECT_ROOT when it is set.

Robustness: writes are atomic (temp file + rename) and serialised with a lock file, a corrupt
state file is moved aside to <file>.corrupt and a fresh state is started, and every file carries a
"version" field so future formats can be migrated. State is best effort: if it is missing, rebuild
the scheme from the newest page with `init --scheme-from`.
"""
import sys, os, json, subprocess, tempfile, time
from contextlib import contextmanager

STATE_VERSION = 1
SCHEME_KEYS = {"base", "surface", "text", "accent", "font_display", "font_body", "radius"}


def project_root():
    r = os.environ.get("FLAWLESS_PROJECT_ROOT")
    return os.path.abspath(r) if r else None


def state_path():
    for var in ("FLAWLESS_STATE", "CLEAN_UI_STATE"):
        if os.environ.get(var):
            return os.path.abspath(os.path.expanduser(os.environ[var]))
    root = project_root()
    if root:
        return os.path.join(root, ".flawless-state.json")
    return os.path.expanduser("~/.clean-ui-state.json")


def fresh():
    return {"version": STATE_VERSION, "active": False, "scheme": {}, "pages": {}}


def migrate(st):
    """Bring an older state dict up to STATE_VERSION. Version 0 = files written before versioning."""
    if not isinstance(st, dict):
        raise ValueError("state root is not an object")
    v = st.get("version", 0)
    if v > STATE_VERSION:
        raise ValueError("state file is from a newer version (%s)" % v)
    if v < 1:
        st.setdefault("active", False)
        st.setdefault("scheme", {})
        st.setdefault("pages", {})
        st["version"] = 1
    return st


@contextmanager
def locked(path, timeout=5.0):
    """Advisory lock via an exclusive lock file. Falls through after the timeout so a stale lock never blocks work."""
    lock = path + ".lock"
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fd, deadline = None, time.time() + timeout
    while fd is None:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            try:  # a lock older than the timeout is stale
                if time.time() - os.path.getmtime(lock) > timeout:
                    os.remove(lock)
                    continue
            except OSError:
                pass
            if time.time() > deadline:
                break
            time.sleep(0.05)
    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
            try:
                os.remove(lock)
            except OSError:
                pass


def load(path=None):
    path = path or state_path()
    if not os.path.exists(path):
        return fresh()
    try:
        with open(path, encoding="utf-8") as f:
            return migrate(json.load(f))
    except (ValueError, OSError) as e:  # json.JSONDecodeError is a ValueError
        aside = path + ".corrupt"
        try:
            os.replace(path, aside)
        except OSError:
            aside = "(could not move aside)"
        print("warning: state file unreadable (%s); moved to %s and started fresh" % (e, aside), file=sys.stderr)
        return fresh()


def save(st, path=None):
    path = path or state_path()
    st["version"] = STATE_VERSION
    d = os.path.dirname(path) or "."
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".flawless-state.", suffix=".tmp", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(st, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def rel_page(p):
    root = project_root()
    if root:
        ap = os.path.abspath(p)
        if ap == root or ap.startswith(root + os.sep):
            return os.path.relpath(ap, root)
    return p


def scheme_from(page):
    here = os.path.dirname(os.path.abspath(__file__))
    out = subprocess.run([sys.executable, os.path.join(here, "audit.py"), page, "--json"],
                         capture_output=True, text=True).stdout
    sc = json.loads(out)["scheme"]
    fonts = sc.get("google_fonts", [])
    return {k: v for k, v in {
        "base": sc.get("base"), "surface": sc.get("surface"), "text": sc.get("text"),
        "accent": sc.get("accent"), "radius": sc.get("radius"),
        "font_display": fonts[0] if fonts else None,
        "font_body": fonts[1] if len(fonts) > 1 else None}.items() if v}


def main(a):
    if not a:
        sys.exit(__doc__)
    path, cmd = state_path(), a[0]
    if cmd == "path":
        print(path); return
    if cmd not in ("init", "show", "set", "page", "flag"):
        sys.exit(__doc__)
    with locked(path):
        st = load(path)
        if cmd == "init":
            if "--scheme-from" in a:
                st["scheme"] = scheme_from(a[a.index("--scheme-from") + 1])
            save(st, path); print("state ready:", path)
        elif cmd == "show":
            print(json.dumps(st, indent=2))
        elif cmd == "set":
            if len(a) < 3 or a[1] not in SCHEME_KEYS:
                sys.exit("unknown key; use one of: " + ", ".join(sorted(SCHEME_KEYS)))
            st["scheme"][a[1]] = a[2]; save(st, path); print("set", a[1], "=", a[2])
        elif cmd == "page":
            if len(a) < 2:
                sys.exit(__doc__)
            status = "unknown"
            for x in a[2:]:
                if x.startswith("audit="):
                    status = x.split("=", 1)[1]
            st["pages"][rel_page(a[1])] = {"audit": status}; save(st, path); print("page recorded:", rel_page(a[1]), status)
        elif cmd == "flag":
            if len(a) < 3:
                sys.exit(__doc__)
            st[a[1]] = (a[2] == "on"); save(st, path); print(a[1], "=", st[a[1]])


if __name__ == "__main__":
    main(sys.argv[1:])
