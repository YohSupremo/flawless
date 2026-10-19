#!/usr/bin/env python3
"""Check a palette against clean-ui color rules.

Usage: python scripts/palette.py BASE TEXT ACCENT [ACCENT_INK]
Colors are hex like #1b1410. Prints hue/saturation flags and contrast ratios.
"""
import sys, colorsys, json, os

_R = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tokens", "rules.json"), encoding="utf-8"))
HUE_LO, HUE_HI = _R["color"]["banned_hue_min"], _R["color"]["banned_hue_max"]
HUE_SAT = _R["color"]["banned_min_saturation"]
C_TEXT, C_MARK, C_BTN = _R["contrast"]["text_min"], _R["contrast"]["marker_min"], _R["contrast"]["button_text_min"]

def rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

def lum(c):
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = map(f, c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def cr(a, b):
    x, y = sorted((lum(rgb(a)), lum(rgb(b))), reverse=True)
    return (x + 0.05) / (y + 0.05)

def hue(h):
    hh, l, s = colorsys.rgb_to_hls(*rgb(h))
    return round(hh * 360), round(s, 2)

def main(args):
    if len(args) < 3:
        sys.exit(__doc__)
    base, text, accent = args[:3]
    ink = args[3] if len(args) > 3 else None
    ok = True
    for name, c in (("base", base), ("text", text), ("accent", accent), *((("accent-ink", ink),) if ink else ())):
        h, s = hue(c)
        bad = s > HUE_SAT and HUE_LO <= h <= HUE_HI
        ok &= not bad
        print(f"{name:11} {c}  hue {h:3}  sat {s:.2f}  {'BANNED blue-violet' if bad else 'ok'}")
    rows = [("text on base", cr(text, base), C_TEXT), ("accent on base", cr(accent, base), C_MARK)]
    if ink:
        rows.append(("button text on accent", cr(ink, accent), C_BTN))
    for k, v, need in rows:
        good = v >= need
        ok &= good
        print(f"{k:22} {v:5.2f}:1  needs {need}  {'pass' if good else 'FAIL'}")
    print("RESULT:", "pass" if ok else "fail")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main(sys.argv[1:])
