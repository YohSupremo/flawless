<!-- GENERATED FILE. Do not edit by hand: edit manifest.json (or the token file named below), then run python core/scripts/build.py. CI fails if this file is out of date. -->

| Command | What it does | Example |
|---|---|---|
| `/flawless` | Turns the skill on for the whole conversation. `status` shows the session scheme and pages built; `off` turns it off | `/flawless`, `/flawless status`, `/flawless off` |
| `/flawless-c` | Lists every command with its description | `/flawless-c` |
| `/help` | Same as `/flawless-c` | `/help` |
| `/new` | Builds a page from scratch. Asks only for what is missing, then a palette choice | `/new landing page for a bike workshop` |
| `/edit` | Changes an existing page and keeps its scheme. With no change described, asks which category to change | `/edit make the headline shorter` |
| `/audit` | Checks a page against every rule and reports errors and warnings. Asks before fixing | `/audit the coffee page` |
| `/palette` | Shows compliant palettes with contrast values and applies your pick to the color tokens | `/palette warmer accent` |
| `/copy` | Offers three plain rewrites of the headline, supporting text, buttons, or a section | `/copy headline` |
| `/section` | Adds a section from the pattern library, with a layout different from its neighbors | `/section how it works` |
| `/match` | Makes the palette and photo agree: grades or swaps the photo to your palette, or takes the palette from a photo you must keep | `/match` |
| `/animate` | Adds restrained motion after asking what kind: entrance, scroll reveal, hover, or image motion | `/animate hero entrance` |
| `/mobile` | Checks and fixes the phone layout | `/mobile` |
| `/ref` | Reads the idea behind a reference image and builds something new, keeping your current palette | `/ref` with an image attached |
| `/a11y` | Checks contrast, language, alt text, focus styles, and reduced motion | `/a11y` |
| `/history` | Lists the saved versions of a page | `/history` |
| `/revert` | Restores the previous version, or a numbered one | `/revert`, `/revert 2` |

## Command details

| Command | Changes files | Needs a page | Asks to confirm | Preview mode | Related | Typical output |
|---|---|---|---|---|---|---|
| `/flawless` | no | no | no | no | `/flawless-c`, `/new`, `/edit` | Session status: on or off, scheme, pages built |
| `/flawless-c` | no | no | no | no | `/flawless` | Table of every command with description, example, and details |
| `/new` | yes | no | no | no | `/edit`, `/palette`, `/audit` | One self-contained HTML file and a one-line audit result |
| `/edit` | yes | yes | no | yes | `/revert`, `/history`, `/audit` | Changed page, one or two sentences, audit line |
| `/audit` | no | yes | yes | no | `/a11y`, `/mobile`, `/edit` | Report in three groups (errors, warnings, passes) then one fix question |
| `/palette` | yes | no | yes | yes | `/match`, `/edit` | Palette choice with contrast figures, applied to the page when one is named |
| `/copy` | yes | yes | no | yes | `/edit`, `/audit` | Plain rewrite options for the named copy |
| `/section` | yes | yes | no | yes | `/new`, `/edit` | New section added from the pattern library, audit line |
| `/match` | yes | yes | yes | yes | `/palette`, `/new` | Photo graded or palette adapted so they agree, with the choice made explicit |
| `/animate` | yes | yes | no | yes | `/edit`, `/a11y` | Restrained entrance, scroll, hover or image motion added, audit line |
| `/mobile` | yes | yes | no | yes | `/a11y`, `/audit` | Phone layout checked and fixed, list of what changed |
| `/ref` | no | no | yes | no | `/new`, `/edit` | Reference analysis and a new, original direction brief |
| `/a11y` | yes | yes | no | yes | `/mobile`, `/audit` | Contrast, alt text, focus, language and reduced-motion checks with fixes |
| `/history` | no | yes | no | no | `/revert`, `/edit` | List of saved versions of the page |
| `/revert` | yes | yes | yes | no | `/history`, `/edit` | Page restored to the chosen version; the replaced version is saved first |

## Common failure cases

- `/flawless`: State file missing: rebuild with state.py init --scheme-from <page>
- `/flawless-c`: Unknown command typed: this list is shown
- `/new`: Brief names no purpose: asks one question round; Rule conflict with the brief: asks keep or override once
- `/edit`: More than one page could match: asks which; Change would alter the scheme: asks before doing it
- `/audit`: External stylesheet: CSS not readable, markup only; Rule overridden earlier: listed as overridden
- `/palette`: Requested color fails contrast or sits in the banned hue range: offers the nearest passing color
- `/copy`: Facts missing: asks rather than inventing them
- `/section`: No existing page: hands off to /new; Same layout as the section above: picks another
- `/match`: No photo on the page: nothing to match; Pillow missing for the image scripts
- `/animate`: Request for looping or parallax motion: refused with an alternative
- `/mobile`: No viewport meta tag: added; Cannot render the page: static checks only
- `/ref`: No image attached: asks for one; Pillow missing for palette extraction
- `/a11y`: Contrast failure caused by a user-chosen color: asks before changing it
- `/history`: No versions saved yet: says so
- `/revert`: Version number not found: lists the available ones
