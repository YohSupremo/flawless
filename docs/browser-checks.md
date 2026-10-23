# Browser checks (optional)

`core/scripts/browser_check.py` renders the page in Chromium through Playwright and checks what a text audit cannot. It is optional: the rest of the skill works without it.

```text
pip install playwright
playwright install chromium
python core/scripts/browser_check.py page.html
python core/scripts/browser_check.py page.html --shots shots/            # also save screenshots
python core/scripts/browser_check.py page.html --shots shots/ --baseline approved/   # compare to approved shots
```

If Playwright is missing the script prints the install line and exits with code 2.

| Check | Viewport | Result |
| --- | --- | --- |
| Horizontal overflow | phone 375x812 and desktop 1280x800 | error |
| Touch targets under 44x44 px | phone | warning |
| A visible outline or shadow when each control is reached with Tab | both | error |
| Infinite animations still running with `prefers-reduced-motion: reduce` | desktop | error |
| Screenshot differs from a baseline | both | warning (byte comparison, so any rendering change shows) |

Fonts loaded from the network will not load in an offline sandbox, so screenshots there use the fallback stack. Screenshots differ slightly between machines; keep baselines from the same environment you compare in.

Not covered: screen reader output, real device behavior, color-vision simulation, and keyboard traps beyond the first 30 tab stops.
