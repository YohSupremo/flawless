#!/usr/bin/env python3
"""Session state shared by all commands.

Usage:
  state.py init [--scheme-from page.html]   create state (or rebuild the scheme from a page)
  state.py show                             print the whole state
  state.py set KEY VALUE                    set a scheme key (base, text, accent, font_display, font_body, radius)
  state.py page PATH [audit=clean|errors]   register a page and its last audit result
  state.py flag active on|off               turn session mode on or off

State lives at $CLEAN_UI_STATE, or ~/.clean-ui-state.json. It is best effort: if the file is
missing, rebuild it from the newest page with `init --scheme-from`.
"""
import sys, os, json, subprocess

PATH = os.environ.get("CLEAN_UI_STATE", os.path.expanduser("~/.clean-ui-state.json"))
SCHEME_KEYS = {"base", "surface", "text", "accent", "font_display", "font_body", "radius"}

def load():
    if os.path.exists(PATH):
        return json.load(open(PATH))
    return {"active": False, "scheme": {}, "pages": {}}

def save(st):
    json.dump(st, open(PATH, "w"), indent=2)

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
    st, cmd = load(), a[0]
    if cmd == "init":
        if "--scheme-from" in a:
            st["scheme"] = scheme_from(a[a.index("--scheme-from") + 1])
        save(st); print("state ready:", PATH)
    elif cmd == "show":
        print(json.dumps(st, indent=2))
    elif cmd == "set":
        if a[1] not in SCHEME_KEYS:
            sys.exit("unknown key; use one of: " + ", ".join(sorted(SCHEME_KEYS)))
        st["scheme"][a[1]] = a[2]; save(st); print("set", a[1], "=", a[2])
    elif cmd == "page":
        status = "unknown"
        for x in a[2:]:
            if x.startswith("audit="):
                status = x.split("=", 1)[1]
        st["pages"][a[1]] = {"audit": status}; save(st); print("page recorded:", a[1], status)
    elif cmd == "flag":
        st[a[1]] = (a[2] == "on"); save(st); print(a[1], "=", st[a[1]])
    else:
        sys.exit(__doc__)

if __name__ == "__main__":
    main(sys.argv[1:])
