#!/usr/bin/env python3
"""Regenerate everything derived from manifest.json.

Usage: python core/scripts/build.py

Writes:
  - the wiring block inside every commands/<name>/COMMAND.md (between the wiring markers)
  - commands/flawless-c/tokens/command-table.md
  - commands/palette/references/palettes.md (from tokens/palettes.json)
  - core/graph.md (who calls and hands off to whom)
Run this after editing manifest.json. validate.py fails if anything is stale.
"""
import json, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
M = json.load(open(os.path.join(ROOT, "manifest.json"), encoding="utf-8"))
CMDS = M["commands"]

def called_by(name):
    return sorted(k for k, v in CMDS.items() if name in v["calls"])

def handed_from(name):
    return sorted(k for k, v in CMDS.items() if name in v["hands_off_to"])

def fmt(items, code=True):
    if not items:
        return "none"
    return ", ".join(("`%s`" % i) if code else i for i in items)

def cmdref(names):
    return fmt(["/" + n for n in names])

def wiring(name):
    c = CMDS[name]
    lines = [
        "## Wiring",
        "",
        "_Generated from `manifest.json` by `core/scripts/build.py`. Edit the manifest, not this block._",
        "",
        "| | |",
        "|---|---|",
        "| Modifies files | %s |" % ("yes" if c["modifies_files"] else "no (read-only)"),
        "| Pre-hooks | %s |" % fmt(c["pre_hooks"]),
        "| Post-hooks | %s |" % fmt(c["post_hooks"]),
        "| Reads | %s |" % fmt(c["reads"]),
        "| Scripts | %s |" % fmt(c["scripts"]),
        "| Calls | %s |" % cmdref(c["calls"]),
        "| Called by | %s |" % cmdref(called_by(name)),
        "| Hands off to | %s |" % cmdref(c["hands_off_to"]),
        "| Handed off from | %s |" % cmdref(handed_from(name)),
        "| Requires | %s |" % cmdref(c["requires"]),
        "| State read | %s |" % fmt(c["state_reads"]),
        "| State written | %s |" % fmt(c["state_writes"]),
    ]
    return "\n".join(lines)

def write_wiring():
    for name, c in CMDS.items():
        p = os.path.join(ROOT, c["folder"], "COMMAND.md")
        s = open(p, encoding="utf-8").read()
        block = "<!-- wiring:start -->\n" + wiring(name) + "\n<!-- wiring:end -->"
        s2 = re.sub(r"<!-- wiring:start -->.*?<!-- wiring:end -->", lambda m: block, s, flags=re.S)
        if s2 != s:
            open(p, "w", encoding="utf-8").write(s2)

GENERATED = "<!-- GENERATED FILE. Do not edit by hand: edit manifest.json (or the token file named below), then run python core/scripts/build.py. CI fails if this file is out of date. -->\n"

def yn(b):
    return "yes" if b else "no"

def command_table():
    rows = [GENERATED.rstrip("\n"), "", "| Command | What it does | Example |", "|---|---|---|"]
    order = ["flawless", "flawless-c"] + [k for k in CMDS if k not in ("flawless", "flawless-c", "help")]
    for n in order:
        c = CMDS[n]
        rows.append("| `/%s` | %s | %s |" % (n, c["description"], c["example"]))
        for a in c.get("aliases", []):
            rows.append("| `/%s` | Same as `/%s` | `/%s` |" % (a, n, a))
    rows += ["", "## Command details", "",
             "| Command | Changes files | Needs a page | Asks to confirm | Preview mode | Related | Typical output |",
             "|---|---|---|---|---|---|---|"]
    for n in order:
        c = CMDS[n]
        rows.append("| `/%s` | %s | %s | %s | %s | %s | %s |" % (n, yn(c["modifies_files"]), yn(c["needs_target"]), yn(c["confirms"]),
                    yn(c["supports_preview"]), cmdref(c["related"]), c["output"]))
    rows += ["", "## Common failure cases", ""]
    for n in order:
        rows.append("- `/%s`: %s" % (n, "; ".join(CMDS[n]["common_failures"])))
    return "\n".join(rows) + "\n"

def palettes_md():
    P = json.load(open(os.path.join(ROOT, "commands/palette/tokens/palettes.json"), encoding="utf-8"))["palettes"]
    R = json.load(open(os.path.join(ROOT, "core/tokens/rules.json"), encoding="utf-8"))
    out = [GENERATED.rstrip("\n"), "", "# Palettes", "",
           "Generated from `commands/palette/tokens/palettes.json`. Every palette passes `core/scripts/palette.py`: no hue in %d to %d, text contrast at least %s:1, accent marker at least %s:1, button text at least %s:1. Every base is a flat color."
           % (R["color"]["banned_hue_min"], R["color"]["banned_hue_max"], R["contrast"]["text_min"], R["contrast"]["marker_min"], R["contrast"]["button_text_min"]),
           "", "| Name | Base | Text | Accent | Button text | Suits | Text on base | Accent on base | Button on accent |",
           "|---|---|---|---|---|---|---|---|---|"]
    for p in P:
        c = p["contrast"]
        out.append("| %s | `%s` | `%s` | `%s` | `%s` | %s | %s | %s | %s |" % (
            p["name"], p["base"], p["text"], p["accent"], p["accent_ink"], ", ".join(p["suits"]),
            c["text_on_base"], c["accent_on_base"], c["button_text_on_accent"]))
    out += ["", "Brand colors, light and dark variants, and failing-color fixes: `commands/palette/references/palette-rules.md`."]
    return "\n".join(out) + "\n"

def graph_md():
    L = [GENERATED.rstrip("\n"), "", "# Command graph", "",
         "Generated from `manifest.json`. Solid arrows are calls (one command runs another). Dashed arrows are hand-offs (control passes after the user decides). `requires` means the other command's data must exist.", "",
         "```mermaid", "flowchart LR"]
    for n, c in CMDS.items():
        for t in c["calls"]:
            L.append("  %s --> %s" % (n.replace("-", "_"), t.replace("-", "_")))
        for t in c["hands_off_to"]:
            L.append("  %s -.-> %s" % (n.replace("-", "_"), t.replace("-", "_")))
        for t in c["requires"]:
            L.append("  %s == requires ==> %s" % (n.replace("-", "_"), t.replace("-", "_")))
    L += ["```", "", "## Calls (text form)", ""]
    for n, c in CMDS.items():
        L.append("- `/%s` calls %s; hands off to %s." % (n, cmdref(c["calls"]), cmdref(c["hands_off_to"])))
    L += ["", "## Shared layers", "",
          "- **Rules:** `core/rules.md` and thresholds in `core/tokens/rules.json`. Read by every command that builds or checks UI.",
          "- **Hooks:** `core/hooks.md`. Snapshot before changes; audit, state, and report after.",
          "- **State:** `core/state.md`, managed by `core/scripts/state.py`. One session scheme shared by all commands.",
          "- **Scripts:** `core/scripts/` (audit, palette, snapshot, state, extract_palette, analyze_layout, build, validate)."]
    return "\n".join(L) + "\n"

def main():
    write_wiring()
    open(os.path.join(ROOT, "commands/flawless-c/tokens/command-table.md"), "w", encoding="utf-8").write(command_table())
    open(os.path.join(ROOT, "commands/palette/references/palettes.md"), "w", encoding="utf-8").write(palettes_md())
    open(os.path.join(ROOT, "core/graph.md"), "w", encoding="utf-8").write(graph_md())
    print("built: wiring for %d commands, command table, palettes.md, graph.md" % len(CMDS))

if __name__ == "__main__":
    main()
