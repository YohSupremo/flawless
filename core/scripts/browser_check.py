#!/usr/bin/env python3
"""Optional browser-based checks for a page. Needs Playwright; the rest of the skill does not.

Usage: python core/scripts/browser_check.py page.html [--json] [--shots DIR] [--baseline DIR]

Install once:  pip install playwright && playwright install chromium

Checks, at phone (375x812) and desktop (1280x800) viewports:
  - horizontal overflow (page wider than the viewport)
  - touch targets under 44x44 px on the phone viewport (links, buttons, inputs)
  - keyboard focus: tabbing to each control must change its outline or box-shadow
  - reduced motion: with prefers-reduced-motion emulated, no running CSS animations
  - screenshots (--shots DIR); with --baseline DIR, reports pages whose screenshot differs

Exit code 1 if any error is found, 2 if Playwright is not installed. See docs/browser-checks.md.
"""
import sys, os, json

MIN_TAP = 44
VIEWPORTS = {"phone": (375, 812), "desktop": (1280, 800)}


def main(page_path):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright is not installed. Run: pip install playwright && playwright install chromium", file=sys.stderr)
        return 2
    url = "file://" + os.path.abspath(page_path)
    shots = sys.argv[sys.argv.index("--shots") + 1] if "--shots" in sys.argv else None
    base = sys.argv[sys.argv.index("--baseline") + 1] if "--baseline" in sys.argv else None
    errors, warnings = [], []
    if shots:
        os.makedirs(shots, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for name, (w, h) in VIEWPORTS.items():
            ctx = browser.new_context(viewport={"width": w, "height": h}, reduced_motion="no-preference")
            pg = ctx.new_page()
            pg.goto(url)
            pg.wait_for_load_state("load")

            over = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            if over > 0:
                errors.append(f"{name}: page overflows horizontally by {over}px")

            if name == "phone":
                small = pg.evaluate("""() => [...document.querySelectorAll('a[href],button,input,select,textarea,[role=button]')]
                    .filter(e => e.offsetParent !== null).map(e => { const r = e.getBoundingClientRect();
                    return {t: (e.innerText || e.getAttribute('aria-label') || e.tagName).trim().slice(0, 30), w: Math.round(r.width), h: Math.round(r.height)} })
                    .filter(x => x.w < %d || x.h < %d)""" % (MIN_TAP, MIN_TAP))
                for s in small:
                    warnings.append(f"phone: touch target '{s['t']}' is {s['w']}x{s['h']}px (minimum {MIN_TAP}x{MIN_TAP})")

            # keyboard focus visibility
            n = pg.evaluate("document.querySelectorAll('a[href],button,input,select,textarea,[tabindex]').length")
            seen = set()
            for _ in range(min(n, 30)):
                pg.keyboard.press("Tab")
                info = pg.evaluate("""() => { const e = document.activeElement; if (!e || e === document.body) return null;
                    const s = getComputedStyle(e); const key = e.outerHTML.slice(0, 60);
                    return {key, label: (e.innerText || e.tagName).trim().slice(0, 30),
                            visible: (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0) || s.boxShadow !== 'none'} }""")
                if info and info["key"] not in seen:
                    seen.add(info["key"])
                    if not info["visible"]:
                        errors.append(f"{name}: '{info['label']}' shows no visible focus indicator")

            if shots:
                out = os.path.join(shots, f"{os.path.basename(page_path)}.{name}.png")
                pg.screenshot(path=out, full_page=True)
                ref = os.path.join(base, os.path.basename(out)) if base else None
                if ref and os.path.exists(ref):
                    with open(ref, "rb") as a, open(out, "rb") as b:
                        if a.read() != b.read():
                            warnings.append(f"{name}: screenshot differs from baseline {ref}")
            ctx.close()

        ctx = browser.new_context(reduced_motion="reduce")
        pg = ctx.new_page(); pg.goto(url); pg.wait_for_timeout(300)
        running = pg.evaluate("document.getAnimations().filter(a => a.playState === 'running' && a.effect && a.effect.getComputedTiming().iterations === Infinity).length")
        if running:
            errors.append(f"reduced motion: {running} infinite animation(s) still running")
        browser.close()

    out = {"errors": errors, "warnings": warnings}
    if "--json" in sys.argv:
        print(json.dumps(out, indent=2))
    else:
        print("ERRORS" if errors else "NO ERRORS")
        for e in errors: print("  -", e)
        if warnings:
            print("WARNINGS")
            for w in warnings: print("  -", w)
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
