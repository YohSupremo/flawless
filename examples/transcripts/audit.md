# /audit on a page with problems

Real output of the audit script. Page: `examples/audit-before.html`.

```text
> /audit examples/audit-before.html
CURRENT SCHEME
  base: #f1eadd
  surface: #e7dfce
  text: #1f1a15
  accent: #7c3aed
  fonts: ['"Anton", Impact, "Arial Narrow", sans-serif', '"DM Sans", system-ui, sans-serif']
  radius: 4px
  contrast: {'text on base': 14.43, 'muted text on base': 8.45, 'accent on base (marker)': 4.76, 'text on surface': 13.02, 'button text on accent': 5.7}
  mode: strict
ERRORS
  - gradients: 2 found (all gradients are banned)
  - color #6a4cff: hue 250 is in the banned 230-300 blue-violet range
  - color #7c3aed: hue 262 is in the banned 230-300 blue-violet range
  - visible copy contains middle dot '·'
  - banned hero word/phrase: 'elevate'
  - banned hero word/phrase: 'seamless'
  - banned hero word/phrase: 'journey'
  - banned hero word/phrase: 'learn more'
  - banned hero word/phrase: 'get started'
  - banned hero word/phrase: 'where innovation'
  - filler/placeholder text in visible copy: 'lorem ipsum'
  - spacing off the scale (4,8,16,24,32,48,64,96): 15px, 30px
  - hero has 3 buttons (maximum 2)
WARNINGS
  - headline has 11 words (aim for 8 or fewer)
  - possible statistic in copy; confirm the user supplied it
  - possible trust claim in copy; confirm it is real and supplied
  - possible second accent: saturated hues near 222, 250
```
