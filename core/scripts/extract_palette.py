#!/usr/bin/env python3
"""Pull a color scheme out of a reference screenshot (for /ref).

Usage: python scripts/extract_palette.py image.png
Prints dominant colors, the likely base and accent, and flags banned hues.
Needs Pillow (pip install pillow --break-system-packages).
"""
import sys, colorsys, warnings
warnings.filterwarnings('ignore')
from collections import Counter

def main(path):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    im.thumbnail((200, 200))
    q = im.quantize(colors=16, method=Image.Quantize.MEDIANCUT).convert("RGB")
    cnt = Counter(q.getdata())
    total = sum(cnt.values())
    rows = []
    for (r, g, b), n in cnt.most_common():
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        rows.append((n / total, "#%02x%02x%02x" % (r, g, b), round(h * 360), round(s, 2), round(l, 2)))
    print("DOMINANT COLORS (share, hex, hue, sat, light)")
    for sh, hx, h, s, l in rows[:10]:
        flag = "  BANNED blue-violet" if s > 0.15 and 230 <= h <= 300 else ""
        print(f"  {sh:5.1%}  {hx}  hue {h:3}  sat {s:.2f}  light {l:.2f}{flag}")
    # base: average of the darkest 40 percent of pixels (a photo skews the top colors)
    full = Image.open(path).convert("RGB")
    full.thumbnail((400, 400))
    px = list(full.getdata())
    px.sort(key=lambda c: sum(c))
    dark = px[: int(len(px) * 0.4)]
    base = tuple(int(sum(c[i] for c in dark) / len(dark)) for i in range(3))
    print("LIKELY BASE:   #%02x%02x%02x  (mean of the darkest 40%% of pixels)" % base)
    # accent: strongly saturated, mid-light pixels, grouped by 20-degree hue bucket
    buckets = {}
    for r, g, b in px:
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        if s >= 0.6 and 0.3 <= l <= 0.7:
            buckets.setdefault(int(h * 360) // 20, []).append((r, g, b))
    if buckets:
        key = max(buckets, key=lambda k: len(buckets[k]))
        grp = buckets[key]
        a = tuple(int(sum(c[i] for c in grp) / len(grp)) for i in range(3))
        h = round(colorsys.rgb_to_hls(*[v / 255 for v in a])[0] * 360)
        flag = "  BANNED blue-violet" if 230 <= h <= 300 else ""
        print("LIKELY ACCENT: #%02x%02x%02x  (hue %d, %.1f%% of pixels)%s" % (*a, h, 100 * len(grp) / len(px), flag))
    else:
        print("LIKELY ACCENT: none clearly saturated; check the image by eye")
    print("Photo pixels skew these numbers; confirm the accent from buttons or small markers.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1])
