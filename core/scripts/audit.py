#!/usr/bin/env python3
"""clean-ui audit: print a page's current scheme and list rule violations.

Usage: python core/scripts/audit.py page.html [--json] [--a11y] [--mobile] [--explain]
                                    [--mode strict|balanced|brand-first] [--config flawless.config.json]
                                    [--avoid 'phrase one|phrase two']
Errors (hard rules) set exit code 1. Warnings (judgment calls) do not.

--explain   add the design principle and a suggested fix under every finding.
--mode      strictness preset (default strict). See docs/configuration.md.
--config    project config file. Without the flag, flawless.config.json is looked up next to the
            page and in its parent folders. Config can set the mode, brand colors, accessibility
            target, and headline limit.

What this script can and cannot check is listed in docs/audit-coverage.md.
"""
import re, sys, json, colorsys

import os
def load_rules():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "tokens", "rules.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def _arg(flag):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv and sys.argv.index(flag) + 1 < len(sys.argv) else None

def find_config(page=None):
    explicit = _arg("--config")
    if explicit:
        return explicit
    start = os.path.dirname(os.path.abspath(page)) if page else os.getcwd()
    for _ in range(6):
        cand = os.path.join(start, "flawless.config.json")
        if os.path.isfile(cand):
            return cand
        parent = os.path.dirname(start)
        if parent == start:
            break
        start = parent
    return None

MODES = {
    # mode: (error prefixes demoted to warnings, rule overrides)
    "strict": ((), {}),
    "balanced": (("spacing off the scale", "pill/badge", "eyebrow"),
                 {"hero.max_headline_words": 10, "color.banned_min_saturation": 0.35, "eyebrow.allowed_per_page": 2}),
    "brand-first": (("color #", "hsl", "gradients", "spacing off the scale", "pill/badge", "eyebrow", "backdrop blur"),
                    {"hero.max_headline_words": 12, "eyebrow.allowed_per_page": 3}),
}

def apply_overrides(rules, overrides):
    for dotted, val in overrides.items():
        node = rules
        keys = dotted.split(".")
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = val

def load_config(page=None):
    """Returns (config dict, path or None). A broken config file is reported, not ignored."""
    path = find_config(page)
    if not path:
        return {}, None
    try:
        with open(path, encoding="utf-8") as f:
            cfg = json.load(f)
        if not isinstance(cfg, dict):
            raise ValueError("top level must be an object")
        return cfg, path
    except (OSError, ValueError) as e:
        sys.exit("config error in %s: %s" % (path, e))

R = load_rules()
_page_arg = next((a for a in sys.argv[1:] if a.endswith((".html", ".htm"))), None)
CONFIG, CONFIG_PATH = load_config(_page_arg)
MODE = _arg("--mode") or CONFIG.get("mode", "strict")
if MODE not in MODES:
    sys.exit("unknown mode '%s'; use one of: %s" % (MODE, ", ".join(MODES)))
DEMOTE, _mode_over = MODES[MODE]
apply_overrides(R, _mode_over)
if str(CONFIG.get("accessibility_target", "AA")).upper() == "AAA":
    R["contrast"]["text_min"] = max(R["contrast"]["text_min"], 7.0)
if "max_headline_words" in CONFIG:
    R["hero"]["max_headline_words"] = int(CONFIG["max_headline_words"])
BRAND = {c.lstrip("#").lower() for c in CONFIG.get("brand_colors", [])}
SCALE = set(R["spacing_scale_px"])
BANNED_WORDS = R["banned_words"]
FILLER = R["filler_text"]
HUE_LO, HUE_HI = R["color"]["banned_hue_min"], R["color"]["banned_hue_max"]
HUE_SAT = R["color"]["banned_min_saturation"]
MAX_WORDS = R["hero"]["max_headline_words"]
MAX_BTNS = R["hero"]["max_buttons"]
MAX_PARAS = R["hero"]["max_paragraphs"]
C_TEXT, C_MARK, C_BTN = R["contrast"]["text_min"], R["contrast"]["marker_min"], R["contrast"]["button_text_min"]
SYMBOLS = R["banned_symbols"]
WARN_SYMBOLS = R.get("warn_symbols", {})
EYEBROW = R["eyebrow"]
MOTION = R["motion"]

def rgb(hx):
    if len(hx) == 3:
        hx = "".join(c * 2 for c in hx)
    return tuple(int(hx[i:i + 2], 16) / 255 for i in (0, 2, 4))

def hls(hx):
    h, l, s = colorsys.rgb_to_hls(*rgb(hx))
    return round(h * 360), round(s, 2), round(l, 2)

def lum(c):
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = map(f, c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(c1, c2):
    a, b = sorted((lum(c1), lum(c2)), reverse=True)
    return (a + 0.05) / (b + 0.05)

def token(css, name):
    """Value of --name from the FIRST declaration (the default theme)."""
    m = re.search(r"--%s\s*:\s*([^;]+);" % name, css)
    return m.group(1).strip() if m else None

def to_rgb(val, over=None):
    if not val:
        return None
    m = re.match(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$", val)
    if m:
        return rgb(m.group(1))
    m = re.match(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\s*\)", val)
    if m:
        c = tuple(int(m.group(i)) / 255 for i in (1, 2, 3))
        a = float(m.group(4)) if m.group(4) else 1.0
        if over is not None and a < 1:
            return tuple(c[i] * a + over[i] * (1 - a) for i in range(3))
        return c
    return None

# (message prefix, principle, suggested fix). Used by --explain. Principles are defined in core/rules.md.
EXPLAIN = [
    ("gradients", "Flat color reads as deliberate; gradients are the most common sign of generated UI.", "Replace with a flat token color. For text over a photo, use a flat rgba overlay."),
    ("color #", "Blue-violet hues are the default output of generated UI, so the range is banned.", "Pick a palette with /palette, or allow a brand color in flawless.config.json (brand_colors)."),
    ("hsl", "Blue-violet hues are banned (see the color rule).", "Move the hue outside the banned range or register it as a brand color."),
    ("visible copy contains", "Slashes, middle dots, bullets and em dashes are decorative separators; plain sentences carry meaning better.", "Rewrite with a period or the word 'and'."),
    ("banned hero word", "Stock marketing phrases say nothing specific.", "Say what the thing is or does in plain words (/copy)."),
    ("emoji in visible copy", "Emoji act as decoration, not information.", "Remove them or use real iconography the user supplied."),
    ("filler/placeholder", "Placeholder text must never ship.", "Replace it with real copy or remove the element."),
    ("spacing off the scale", "A small fixed scale keeps rhythm consistent.", "Use a --s1 to --s8 token or a value from the scale in core/tokens/rules.json."),
    ("backdrop blur", "Glassmorphism is a banned effect.", "Use a flat, opaque surface."),
    ("looping animation", "Endless motion competes with the content and fails reduced-motion users.", "Animate once, on entrance, and respect prefers-reduced-motion."),
    ("pill/badge", "Filler tags add noise unless the user supplied them.", "Delete the element."),
    ("hero has", "A hero has one job: a headline, one sentence, at most two buttons.", "Remove the extra buttons or paragraphs."),
    ("headline has", "Short headlines are read; long ones are skimmed.", "Cut to the core claim (/copy headline)."),
    ("eyebrow", "Eyebrow labels usually repeat the headline.", "Remove it unless it carries new information."),
    ("motion present with no prefers-reduced-motion", "Some people get ill from motion; the OS setting must be honoured.", "Add @media (prefers-reduced-motion: reduce) { * { animation: none; transition: none; } }"),
    ("low contrast", "WCAG contrast keeps text readable.", "Darken or lighten the text or background (/palette or /a11y)."),
    ("a11y: <html> has no lang", "Screen readers pick pronunciation from the lang attribute.", "Add lang=\"en\" (or the right language) to <html>."),
    ("a11y: <img> without alt", "Images need a text alternative.", "Add alt text, or alt=\"\" for decorative images."),
    ("a11y: outline removed", "Keyboard users need a visible focus indicator.", "Add a :focus-visible style."),
    ("mobile: no viewport", "Without the viewport tag phones render a shrunken desktop page.", "Add <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">."),
    ("mobile: no max-width media query", "The layout will not adapt to small screens.", "Add a max-width media query for the phone layout (/mobile)."),
    ("mobile: font sizes", "Small text is hard to read on phones.", "Use 14px or larger."),
    ("mobile: button padding", "Tap targets under 44px are easy to miss.", "Increase button padding."),
    ("possible statistic", "Invented numbers destroy trust.", "Keep it only if the user supplied it."),
    ("possible trust claim", "Unverified trust claims are made up in most generated pages.", "Remove unless real and supplied."),
    ("possible second accent", "One accent color keeps the page focused.", "Reduce to a single accent hue."),
    ("no <h1>", "Every page needs one main heading.", "Add an <h1>."),
    ("transition: all", "Animating every property is wasteful and can cause layout jank.", "List opacity and transform."),
    ("animation/transition of", "Long motion feels slow.", "Keep durations at or under the limit in rules.json."),
    ("keyframes animate", "Layout and paint properties cause jank.", "Animate opacity, transform or clip-path only."),
]

def explain(msg):
    for prefix, why, fix in EXPLAIN:
        if msg.startswith(prefix) or prefix in msg:
            return {"principle": why, "fix": fix}
    return None

def show_explain(msg, out):
    if "explanations" in out and msg in out["explanations"]:
        e = out["explanations"][msg]
        print("      why:", e["principle"])
        print("      fix:", e["fix"])

def main(path):
    html = open(path, encoding="utf-8").read()
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))
    body_m = re.search(r"<body[^>]*>(.*)</body>", html, re.S)
    raw_body = re.sub(r"<!--.*?-->", "", body_m.group(1) if body_m else html, flags=re.S)
    body = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", raw_body, flags=re.S)
    text = " ".join(re.sub(r"<[^>]+>", " ", body).split())
    low = text.lower()

    scheme, errors, warnings = {}, [], []

    for name in ("base", "surface", "text", "accent"):
        v = token(css, name)
        if v:
            scheme[name] = v
    fonts = re.findall(r"--font-(?:display|body)\s*:\s*([^;]+);", css)
    if fonts:
        scheme["fonts"] = [f.strip() for f in fonts]
    gf = re.findall(r"family=([A-Za-z+]+)", html)
    if gf:
        scheme["google_fonts"] = sorted(set(g.replace("+", " ") for g in gf))
    r = token(css, "radius")
    if r:
        scheme["radius"] = r

    # ---- errors ----
    n = len(re.findall(r"gradient\s*\(", css + html, re.I))
    if n:
        errors.append(f"gradients: {n} found (all gradients are banned)")

    hexes = sorted(set(re.findall(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", css)))
    for hx in hexes:
        h, s, l = hls(hx)
        if hx.lower() in BRAND or (len(hx) == 3 and "".join(c * 2 for c in hx).lower() in BRAND):
            continue
        if s > HUE_SAT and HUE_LO <= h <= HUE_HI:
            errors.append(f"color #{hx}: hue {h} is in the banned %d-%d blue-violet range" % (HUE_LO, HUE_HI) + "")
    for fn, args in re.findall(r"(hsla?)\(\s*([^)]*)\)", css):
        hv = re.match(r"\s*(\d+)", args)
        sv = re.findall(r"(\d+)%", args)
        if hv and sv and HUE_LO <= int(hv.group(1)) <= HUE_HI and int(sv[0]) > HUE_SAT * 100:
            errors.append(f"{fn}({args.strip()}): hue in banned range")

    for sym, label in SYMBOLS.items():
        if sym in text:
            errors.append(f"visible copy contains {label} '{sym}'")
    for w in BANNED_WORDS:
        if w in low:
            errors.append(f"banned hero word/phrase: '{w}'")
    if re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", text):
        errors.append("emoji in visible copy")
    for w in FILLER:
        if w in low:
            errors.append(f"filler/placeholder text in visible copy: '{w}'")

    off = set()
    for decl in re.findall(r"(?:padding|margin|gap)[a-z-]*\s*:\s*([^;}]+)", css):
        if "var(" in decl or "clamp(" in decl:
            continue
        for v in re.findall(r"(-?\d+(?:\.\d+)?)px", decl):
            if int(float(v)) not in SCALE:
                off.add(v + "px")
    if off:
        errors.append("spacing off the scale (4,8,16,24,32,48,64,96): " + ", ".join(sorted(off)))

    if re.search(r"backdrop-filter\s*:\s*blur", css):
        errors.append("backdrop blur (glassmorphism) found")
    if re.search(r"box-shadow\s*:[^;]*(?:0 0 \d+px|\d+px \d+px \d{2,}px)", css):
        warnings.append("large or glow-style box-shadow found (shadows should be almost none)")
    if re.search(r"animation[^;]*infinite", css):
        errors.append("looping animation found")

    # ---- hero and structure checks ----
    pills = re.findall(r'class="[^"]*\b(badge|pill|chip|tag)\b[^"]*"', raw_body)
    if pills:
        errors.append("pill/badge/tag elements found (%d); remove unless the user supplied them" % len(pills))
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", raw_body, re.S)
    if h1:
        words = re.sub(r"<[^>]+>", " ", h1.group(1)).split()
        if len(words) > MAX_WORDS:
            warnings.append(f"headline has {len(words)} words (aim for %d or fewer)" % MAX_WORDS + "")
        if len(re.findall(r"<br\s*/?>", h1.group(1))) > 1:
            warnings.append("headline breaks across more than two lines")
    else:
        warnings.append("no <h1> found")
    first = re.search(r"<(?:section|main|header)\b.*?</(?:section|main|header)>", raw_body, re.S)
    if first:
        btns = re.findall(r'<a\b[^>]*class="[^"]*\bbtn\b', first.group(0)) + \
               re.findall(r"<button\b", first.group(0))
        if len(btns) > MAX_BTNS:
            errors.append(f"hero has {len(btns)} buttons (maximum %d)" % MAX_BTNS + "")
        paras = re.findall(r"<p\b", first.group(0))
        if len(paras) > MAX_PARAS:
            warnings.append("hero has %d paragraphs; keep brand line, one supporting sentence only" % len(paras))
    if re.search(r"\b\d{1,3}(?:[.,]\d+)?\s?(?:[kKmM]\+|\+|%)", text):
        warnings.append("possible statistic in copy; confirm the user supplied it")
    if re.search(r"(?i)trusted by|as seen (?:in|on)|\d+\s?(?:five[- ])?star", text):
        warnings.append("possible trust claim in copy; confirm it is real and supplied")


    # ---- eyebrow, ampersand, headline wrapping ----
    for sym, why in WARN_SYMBOLS.items():
        if sym in text:
            warnings.append(f"visible copy contains '{sym}': {why}")
    eb = re.findall(r'class="[^"]*\b(%s)\b[^"]*"' % "|".join(EYEBROW["class_names"]), raw_body)
    if len(eb) > EYEBROW["allowed_per_page"]:
        errors.append(f"{len(eb)} eyebrow/kicker labels (max {EYEBROW['allowed_per_page']})")
    elif eb:
        warnings.append("eyebrow label present: remove it unless it carries information the headline lacks")
    if re.search(r"<h1\b", raw_body) and "text-wrap" not in css:
        warnings.append("headline has no text-wrap: balance; the last line may be a single orphan word")

    # ---- motion ----
    durs = [float(v) * (1000 if u == "s" else 1) for v, u in re.findall(r"(?:animation|transition)[^;{}]*?(?<![\w.])(\d*\.\d+|\d+)(ms|s)\b", css)]
    for d in durs:
        if d > MOTION["duration_ms"]["max"]:
            warnings.append(f"animation/transition of {d:.0f}ms is longer than {MOTION['duration_ms']['max']}ms")
            break
    if re.search(r"transition\s*:\s*all\b", css):
        warnings.append("transition: all animates every property; list opacity and transform instead")
    for kf in re.findall(r"@keyframes\s+[\w-]+\s*\{(.*?)\}\s*\}", css, re.S) + re.findall(r"@keyframes\s+[\w-]+\s*\{(.*)", css):
        bad = [pn for pn in ("width", "height", "top", "left", "right", "bottom", "margin", "padding", "box-shadow", "filter", "background") if re.search(r"\b%s\s*:" % pn, kf)]
        if bad:
            warnings.append("keyframes animate layout or paint properties (%s); animate only opacity, transform, clip-path" % ", ".join(bad)); break
    if re.search(r"cubic-bezier\([^)]*-\d", css):
        warnings.append("overshoot easing (negative cubic-bezier value); avoid bounce and elastic")
    if (re.search(r"@keyframes|animation\s*:|transition\s*:", css)) and "prefers-reduced-motion" not in css:
        errors.append("motion present with no prefers-reduced-motion rule")
    if "--avoid" in sys.argv:
        for phrase in sys.argv[sys.argv.index("--avoid") + 1].split("|"):
            if phrase.strip() and phrase.strip().lower() in low:
                errors.append(f"reuses text from the reference: '{phrase.strip()}'")

    # layout variety
    grids = re.findall(r"grid-template-columns\s*:\s*repeat\(\s*(\d+)", css)
    if len(grids) >= 2 and len(set(grids)) == 1:
        warnings.append("every grid uses the same %s-column repeat; vary section layouts" % grids[0])

    # ---- accent discipline ----
    sat = []
    for hx in hexes:
        h, s, l = hls(hx)
        if hx.lower() in BRAND:
            continue
        if s >= 0.45 and 0.15 <= l <= 0.85:
            sat.append(h)
    clusters = []
    for h in sorted(sat):
        if not clusters or min(abs(h - c) if abs(h - c) <= 180 else 360 - abs(h - c) for c in clusters) > 25:
            clusters.append(h)
    if len(clusters) > 1:
        warnings.append("possible second accent: saturated hues near " + ", ".join(str(c) for c in clusters))

    # ---- contrast ----
    base = to_rgb(scheme.get("base"))
    pairs = []
    if base:
        t = to_rgb(scheme.get("text"))
        if t:
            pairs.append(("text on base", contrast(t, base), C_TEXT))
        tm = to_rgb(token(css, "text-muted"), over=base)
        if tm:
            pairs.append(("muted text on base", contrast(tm, base), C_TEXT))
        ac = to_rgb(scheme.get("accent"))
        if ac:
            pairs.append(("accent on base (marker)", contrast(ac, base), C_MARK))
        sf = to_rgb(scheme.get("surface"))
        if sf and t:
            pairs.append(("text on surface", contrast(t, sf), C_TEXT))
    ac = to_rgb(scheme.get("accent"))
    ink = to_rgb(token(css, "accent-ink"))
    if ac and ink:
        pairs.append(("button text on accent", contrast(ink, ac), C_BTN))
    scheme["contrast"] = {k: round(v, 2) for k, v, _ in pairs}
    for k, v, need in pairs:
        if v < need:
            (errors if "text" in k else warnings).append(f"low contrast: {k} is {v:.2f}:1 (needs {need}:1)")

    # ---- accessibility ----
    if "--a11y" in sys.argv or "--mobile" in sys.argv:
        if not re.search(r"<html[^>]*\blang=", html):
            errors.append("a11y: <html> has no lang attribute")
        if re.search(r"<img\b(?![^>]*\balt=)", raw_body):
            errors.append("a11y: <img> without alt")
        if re.search(r"<svg\b(?![^>]*(?:aria-hidden|role=|aria-label))", raw_body):
            warnings.append("a11y: <svg> without role or aria-label")
        if "outline: none" in css.replace("outline:none", "outline: none") and ":focus-visible" not in css:
            errors.append("a11y: outline removed with no :focus-visible replacement")
    if "--mobile" in sys.argv:
        if not re.search(r"<meta[^>]*name=[\"']viewport", html):
            errors.append("mobile: no viewport meta tag")
        if not re.search(r"@media[^{]*max-width", css):
            errors.append("mobile: no max-width media query; layout will not adapt")
        small = {v for v in re.findall(r"font-size\s*:\s*(\d+)px", css) if int(v) < 14}
        if small:
            warnings.append("mobile: font sizes under 14px: " + ", ".join(sorted(small, key=int)) + "px")
        pad = re.findall(r"\.btn\s*\{[^}]*padding\s*:\s*(\d+)px", css)
        if pad and int(pad[0]) < 12:
            warnings.append("mobile: button padding under 12px may fail the 44px tap target")
        if re.search(r"overflow-x\s*:\s*scroll", css) and "body" in css:
            warnings.append("mobile: check for horizontal scroll on body")

    # mode: some hard rules become warnings (never contrast, accessibility, or reduced-motion rules)
    if DEMOTE:
        kept = []
        for e in errors:
            (warnings if any(d in e for d in DEMOTE) else kept).append(e)
        errors = kept

    scheme["visible_copy"] = text[:300]
    scheme["mode"] = MODE
    if CONFIG_PATH:
        scheme["config"] = CONFIG_PATH
    out = {"scheme": scheme, "errors": errors, "warnings": warnings}
    if "--explain" in sys.argv:
        out["explanations"] = {m: explain(m) for m in errors + warnings if explain(m)}
    if "--json" in sys.argv:
        print(json.dumps(out, indent=2))
    else:
        print("CURRENT SCHEME")
        for k, v in scheme.items():
            print(f"  {k}: {v}")
        print("ERRORS" if errors else "NO ERRORS")
        for p in errors:
            print("  -", p)
            show_explain(p, out)
        if warnings:
            print("WARNINGS")
            for p in warnings:
                print("  -", p)
                show_explain(p, out)
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1])
