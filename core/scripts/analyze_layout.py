#!/usr/bin/env python3
"""Measure composition facts from a reference image (for /ref idea briefs).

Usage: python scripts/analyze_layout.py image.png
Reports where the visual weight sits, how much of the frame is accent color,
how much is calm space, and the contrast range. Numbers support the written
analysis; they do not replace looking at the image.
Needs Pillow.
"""
import sys, colorsys, warnings
warnings.filterwarnings("ignore")

def main(path):
    from PIL import Image, ImageFilter
    im = Image.open(path).convert("RGB")
    im.thumbnail((400, 400))
    w, h = im.size
    gray = im.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    gp, ep, cp = list(gray.getdata()), list(edges.getdata()), list(im.getdata())

    def band(x0, x1):
        lums, eds = [], []
        for y in range(h):
            for x in range(int(w * x0), int(w * x1)):
                lums.append(gp[y * w + x]); eds.append(ep[y * w + x])
        n = len(lums)
        return sum(lums) / n, sum(eds) / n

    thirds = [band(i / 3, (i + 1) / 3) for i in range(3)]
    names = ["left", "middle", "right"]
    print("VISUAL WEIGHT (mean brightness 0-255, edge detail 0-255)")
    for n, (l, e) in zip(names, thirds):
        print(f"  {n:6} brightness {l:5.0f}  detail {e:5.1f}")
    busy = max(range(3), key=lambda i: thirds[i][1])
    calm = min(range(3), key=lambda i: thirds[i][1])
    print(f"  most detail: {names[busy]};  calmest: {names[calm]}")
    print("  (text adds detail too, so confirm the subject and text zones by eye)")

    n = len(cp)
    sat = 0
    for r, g, b in cp:
        hh, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        if s >= 0.6 and 0.3 <= l <= 0.7:
            sat += 1
    print(f"ACCENT SHARE: {100 * sat / n:.1f}% of pixels are strongly saturated")

    calm_px = sum(1 for e in ep if e < 6)
    print(f"CALM SPACE:   {100 * calm_px / n:.0f}% of the frame has almost no detail")
    srt = sorted(gp)
    lo, hi = srt[int(n * 0.05)], srt[int(n * 0.95)]
    print(f"CONTRAST:     5th percentile {lo}, 95th percentile {hi} (spread {hi - lo})")
    print(f"ASPECT:       {Image.open(path).size[0]}x{Image.open(path).size[1]}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1])
