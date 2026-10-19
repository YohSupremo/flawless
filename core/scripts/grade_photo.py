#!/usr/bin/env python3
"""Bake a color grade into a photo so it fits a palette (palette-led /match).

Usage:
  grade_photo.py IN OUT --base "#hex" --accent "#hex" [--strength 0.85] [--keep-saturation 0.6] [--preview OUT_PREVIEW]

What it does (a real edit of a new image file, never a CSS filter or gradient):
  1. Finds the photo's dominant hue and rotates colors from that family toward the accent's hue,
     keeping the spread between colors so the picture stays natural (not a flat tint).
  2. Scales saturation by --keep-saturation so no color shouts.
  3. Pulls the shadows toward the palette base so the photo edge melts into the page.
The original file is never overwritten. Needs Pillow and numpy.
"""
import sys, os, math, colorsys
import numpy as np
from PIL import Image

def hexrgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32) / 255

def arg(a, k, d=None):
    return a[a.index(k) + 1] if k in a else d

def dominant_hue(hsv):
    h = hsv[..., 0] / 255 * 360; s = hsv[..., 1] / 255; v = hsv[..., 2] / 255
    m = (s > 0.10) & (s < 0.60) & (v > 0.08)
    if m.sum() < 50:
        return None
    x = np.cos(np.radians(h[m])).sum(); y = np.sin(np.radians(h[m])).sum()
    return math.degrees(math.atan2(y, x)) % 360

def grade(img, base, accent, strength=0.85, keep=0.6):
    hsv = np.array(img.convert("HSV")).astype(np.float32)
    ph = dominant_hue(hsv)
    ah = colorsys.rgb_to_hls(*accent)[0] * 360
    if ph is None:                       # neutral photo: just tint
        ph = ah
    h = hsv[..., 0] / 255 * 360
    diff = (h - ph + 180) % 360 - 180    # signed distance from the photo's family, -180..180
    new_h = (ah + diff * 0.35) % 360     # compress the spread so everything sits near the accent family
    h_out = h + ((new_h - h + 180) % 360 - 180) * strength
    hsv[..., 0] = (h_out % 360) / 360 * 255
    hsv[..., 1] = hsv[..., 1] * (1 - strength * (1 - keep))
    rgb = np.array(Image.fromarray(hsv.astype(np.uint8), "HSV").convert("RGB")).astype(np.float32) / 255
    v = rgb.max(axis=2, keepdims=True)
    w = np.clip((0.32 - v) / 0.32, 0, 1) ** 1.4 * strength   # shadows toward the base
    rgb = rgb * (1 - w) + base[None, None, :] * w
    return Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)), ph, ah

def main(a):
    if len(a) < 2 or "--base" not in a or "--accent" not in a:
        sys.exit(__doc__)
    src, dst = a[0], a[1]
    if os.path.abspath(src) == os.path.abspath(dst):
        sys.exit("refusing to overwrite the original; give a different output path")
    img = Image.open(src).convert("RGB")
    out, ph, ah = grade(img, hexrgb(arg(a, "--base")), hexrgb(arg(a, "--accent")),
                        float(arg(a, "--strength", 0.85)), float(arg(a, "--keep-saturation", 0.6)))
    out.save(dst, quality=92)
    print(f"graded {src} -> {dst}  (photo hue {ph:.0f} moved toward accent hue {ah:.0f})")
    pv = arg(a, "--preview")
    if pv:
        w, h = img.size
        sheet = Image.new("RGB", (w * 2 + 12, h), (255, 255, 255))
        sheet.paste(img, (0, 0)); sheet.paste(out, (w + 12, 0)); sheet.save(pv, quality=90)
        print("preview (before left, after right):", pv)

if __name__ == "__main__":
    main(sys.argv[1:])
