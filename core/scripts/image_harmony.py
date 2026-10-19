#!/usr/bin/env python3
"""Check (and suggest) whether a palette fits the photo used on the page.

Usage:
  image_harmony.py PHOTO [--base #hex] [--accent #hex]    measure the photo, check the palette
  image_harmony.py PHOTO --suggest                        rank palettes from the library for this photo

Why: a palette picked without looking at the photo (green accent on a warm brown photo) looks pasted on.
The photo is the boss: its shadow color sets the base, and the accent sits in or near its hue family.
Thresholds: core/tokens/rules.json -> imagery. Needs Pillow.
"""
import sys, os, json, math, colorsys, warnings
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
R = json.load(open(os.path.join(HERE, "..", "tokens", "rules.json"), encoding="utf-8"))["imagery"]

def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

def hls(rgb):
    h, l, s = colorsys.rgb_to_hls(*rgb)
    return h * 360, l, s

def hdist(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)

def temperature(h):
    if h < 70 or h >= 330: return "warm"
    if h < 170: return "green"
    if h < 260: return "cool"
    return "violet"

def measure(path):
    from PIL import Image
    im = Image.open(path).convert("RGB"); im.thumbnail((300, 300))
    px = list(im.getdata())
    # dominant hue: saturation-weighted circular mean over usable pixels
    x = y = wsum = 0.0; sats = []
    for p in px:
        r = tuple(v / 255 for v in p); h, l, s = hls(r)
        sats.append(s)
        lo, hi = R["hue_sample_saturation_band"]
        if lo <= s <= hi and 0.06 < l < 0.9:
            w = 1.0  # area weighted; the saturation cap keeps small saturated UI (buttons, markers) out
            x += w * math.cos(math.radians(h)); y += w * math.sin(math.radians(h)); wsum += w
    mean_sat = sum(sats) / len(sats)
    hue = (math.degrees(math.atan2(y, x)) % 360) if wsum else None
    # shadow color: mean of the darkest 40 percent
    srt = sorted(px, key=lambda c: sum(c)); dark = srt[: int(len(srt) * 0.4)]
    sh = tuple(sum(c[i] for c in dark) / len(dark) / 255 for i in range(3))
    return {"hue": hue, "mean_sat": mean_sat, "shadow": sh, "neutral": mean_sat < R["neutral_photo_max_saturation"] or hue is None}

def lab(rgb):
    def f(v): return ((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92
    r, g, b = [f(v) for v in rgb]
    X, Y, Z = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047, 0.2126 * r + 0.7152 * g + 0.0722 * b, (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    g_ = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = g_(X), g_(Y), g_(Z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)

def delta_e(c1, c2):
    a, b = lab(c1), lab(c2)
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))

def tohex(rgb): return "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in rgb)

def check(m, base=None, accent=None):
    out, ok = [], True
    if accent:
        ah, al, as_ = hls(hexrgb(accent))
        if m["neutral"]:
            out.append("accent: photo is near neutral, any accent outside the banned hues fits")
        else:
            d = hdist(ah, m["hue"]); good = d <= R["accent_hue_tolerance_deg"]; ok &= good
            out.append(f"accent hue {ah:.0f} vs photo hue {m['hue']:.0f}: {d:.0f} degrees apart, limit {R['accent_hue_tolerance_deg']} -> {'ok' if good else 'CLASH'}")
    if base:
        de = delta_e(hexrgb(base), m["shadow"]); good = de <= R["shadow_max_delta_e"]; ok &= good
        out.append(f"base {base} vs photo shadows {tohex(m['shadow'])}: color difference {de:.1f}, limit {R['shadow_max_delta_e']} -> {'ok' if good else 'MISMATCH (photo edges will show as a visible box)'}")
    return ok, out

def suggest(m):
    P = json.load(open(os.path.join(ROOT, "commands", "palette", "tokens", "palettes.json"), encoding="utf-8"))["palettes"]
    rows = []
    for p in P:
        ah = hls(hexrgb(p["accent"]))[0]
        d = 0 if m["neutral"] else hdist(ah, m["hue"])
        rows.append((d, p))
    rows.sort(key=lambda r: r[0])
    return rows

def main(a):
    if not a: sys.exit(__doc__)
    path = a[0]
    m = measure(path)
    print("PHOTO")
    if m["neutral"]:
        print("  mostly neutral (low saturation); the photo does not constrain the accent")
    else:
        print(f"  dominant hue {m['hue']:.0f} degrees ({temperature(m['hue'])}), mean saturation {m['mean_sat']:.2f}")
    print(f"  shadow color {tohex(m['shadow'])}  (use this tint for the base and for any flat overlay)")
    base = a[a.index("--base") + 1] if "--base" in a else None
    acc = a[a.index("--accent") + 1] if "--accent" in a else None
    code = 0
    if base or acc:
        ok, lines = check(m, base, acc)
        print("PALETTE CHECK")
        for l in lines: print("  -", l)
        print("RESULT:", "fits the photo" if ok else "does not fit the photo")
        code = 0 if ok else 1
    if "--suggest" in a:
        print("PALETTES BY FIT (accent hue distance from the photo, library in commands/palette/tokens/palettes.json)")
        for d, p in suggest(m)[:5]:
            print(f"  {d:4.0f} deg  {p['name']:22} accent {p['accent']}  (text {p['text']}, button text {p['accent_ink']})")
        print(f"  Use the accent from a row above, but set the base to the photo shadow {tohex(m['shadow'])} so the photo edges disappear.")
    sys.exit(code)

if __name__ == "__main__":
    main(sys.argv[1:])
