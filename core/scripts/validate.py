#!/usr/bin/env python3
"""Check that the skill's structure and interconnections are sound.

Usage: python core/scripts/validate.py
Exit code 0 = valid, 1 = problems found.
"""
import json, os, re, sys, subprocess, tempfile, shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
errors, warns = [], []

def err(m): errors.append(m)
def warn(m): warns.append(m)

def exists(rel): return os.path.exists(os.path.join(ROOT, rel))

M = json.load(open(os.path.join(ROOT, "manifest.json"), encoding="utf-8"))
CMDS = M["commands"]
names = set(CMDS)

# 1. structure: folder, COMMAND.md, references, tokens
for n, c in CMDS.items():
    folder = c["folder"]
    for sub in ("", "/references", "/tokens"):
        if not os.path.isdir(os.path.join(ROOT, folder + sub)):
            err(f"{n}: missing folder {folder}{sub}")
    cm = os.path.join(ROOT, folder, "COMMAND.md")
    if not os.path.exists(cm):
        err(f"{n}: missing COMMAND.md"); continue
    text = open(cm, encoding="utf-8").read()
    m = re.match(r"---\nname: ([\w-]+)\ndescription: (.+)\n---", text)
    if not m: err(f"{n}: COMMAND.md frontmatter missing or malformed")
    elif m.group(1) != n: err(f"{n}: frontmatter name is '{m.group(1)}'")
    if "<!-- wiring:start -->" not in text: err(f"{n}: COMMAND.md has no wiring block")
    if len(text.split("\n")) < 25: warn(f"{n}: COMMAND.md is short ({len(text.splitlines())} lines)")
    for sec in ("## Steps", "## Failure cases"):
        if sec not in text and not any(sec in l for l in text.split("\n")):
            if sec == "## Steps" and "## Steps:" in text: continue
            err(f"{n}: COMMAND.md has no '{sec}' section")

# 2. every referenced file exists
for n, c in CMDS.items():
    for rel in c["reads"] + c["scripts"]:
        if not exists(rel): err(f"{n}: references missing file {rel}")
    own = set()
    for sub in ("references", "tokens"):
        d = os.path.join(ROOT, c["folder"], sub)
        if os.path.isdir(d):
            for f in os.listdir(d):
                own.add(f"{c['folder']}/{sub}/{f}")
    for f in sorted(own - set(c["reads"])):
        err(f"{n}: file not listed in reads (orphan): {f}")

# 3. calls, hand-offs, requires point at real commands
for n, c in CMDS.items():
    for key in ("calls", "hands_off_to", "requires"):
        for t in c[key]:
            if t not in names: err(f"{n}: {key} unknown command '{t}'")

# 4. no cycles among calls
def has_cycle():
    state = {}
    def dfs(u, path):
        state[u] = 1
        for v in CMDS[u]["calls"]:
            if v not in CMDS:
                continue
            if state.get(v) == 1: err("call cycle: " + " -> ".join(path + [u, v])); return True
            if v not in state and dfs(v, path + [u]): return True
        state[u] = 2
        return False
    return any(dfs(u, []) for u in CMDS if u not in state)
has_cycle()

# 5. modifying commands use the hooks; read-only ones do not
for n, c in CMDS.items():
    if c["modifies_files"] and ("snapshot" not in c["pre_hooks"] or "audit" not in c["post_hooks"]):
        err(f"{n}: modifies files but is missing snapshot or audit hook")
    if not c["modifies_files"] and c["pre_hooks"]:
        err(f"{n}: read-only command has a snapshot hook")

# 6. state fields written by exactly the commands core/state.md allows
allowed_scheme_writers = {"flawless", "palette", "match", "edit", "new", "revert"}
for n, c in CMDS.items():
    if "scheme" in c["state_writes"] and n not in allowed_scheme_writers:
        err(f"{n}: writes the session scheme but is not an allowed writer")

# 7. generated files are current
tmp = tempfile.mkdtemp()
try:
    dst = os.path.join(tmp, "s")
    shutil.copytree(ROOT, dst)
    subprocess.run([sys.executable, os.path.join(dst, "core", "scripts", "build.py")], capture_output=True)
    for rel in ["core/graph.md", "commands/flawless-c/tokens/command-table.md", "commands/palette/references/palettes.md"] + \
               [c["folder"] + "/COMMAND.md" for c in CMDS.values()]:
        a = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        b = open(os.path.join(dst, rel), encoding="utf-8").read()
        if a != b: err(f"stale generated content: {rel} (run core/scripts/build.py)")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# 8. router lists every command; rules.json parses; palettes pass
router = open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8").read()
for n in names:
    if f"commands/{n}/COMMAND.md" not in router: err(f"router SKILL.md does not point to commands/{n}/COMMAND.md")
try:
    json.load(open(os.path.join(ROOT, "core/tokens/rules.json"), encoding="utf-8"))
except Exception as e:
    err(f"rules.json invalid: {e}")
pal_path = os.path.join(ROOT, "commands/palette/tokens/palettes.json")
try:
    P = json.load(open(pal_path, encoding="utf-8"))["palettes"]
except Exception as e:
    err(f"palettes.json unreadable: {e}")
    P = []
for p in P:
    r = subprocess.run([sys.executable, os.path.join(ROOT, "core/scripts/palette.py"), p["base"], p["text"], p["accent"], p["accent_ink"]], capture_output=True, text=True)
    if r.returncode != 0: err(f"palette {p['id']} fails palette.py")

# 9. stale path mentions in markdown (paths in backticks that do not exist)
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith(".md"):
            t = open(os.path.join(dp, f), encoding="utf-8").read()
            for ref in set(re.findall(r"`((?:core|commands)/[\w./-]+\.(?:md|json|css|html|py))`", t)):
                if not exists(ref): err(f"{os.path.relpath(os.path.join(dp, f), ROOT)} mentions missing path {ref}")

for w in warns: print("WARN ", w)
for e in errors: print("ERROR", e)
print(f"\n{len(CMDS)} commands checked: {len(errors)} errors, {len(warns)} warnings")
sys.exit(1 if errors else 0)
