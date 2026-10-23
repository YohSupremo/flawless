# After the fixes

```text
> /audit examples/audit-after.html
CURRENT SCHEME
  base: #f1eadd
  surface: #e7dfce
  text: #1f1a15
  accent: #b23a14
  fonts: ['"Anton", Impact, "Arial Narrow", sans-serif', '"DM Sans", system-ui, sans-serif']
  radius: 4px
  contrast: {'text on base': 14.43, 'muted text on base': 8.45, 'accent on base (marker)': 5.0, 'text on surface': 13.02, 'button text on accent': 5.99}
  mode: strict
NO ERRORS
```

Strictness modes on the same page that used a banned hue:

```text
> python core/scripts/audit.py examples/audit-before.html --mode brand-first
CURRENT SCHEME
  base: #f1eadd
  surface: #e7dfce
  text: #1f1a15
  accent: #7c3aed
  fonts: ['"Anton", Impact, "Arial Narrow", sans-serif', '"DM Sans", system-ui, sans-serif']
  radius: 4px
  contrast: {'text on base': 14.43, 'muted text on base': 8.45, 'accent on base (marker)': 4.76, 'text on surface': 13.02, 'button text on accent': 5.7}
  mode: brand-first
ERRORS
  - visible copy contains middle dot '·'
  - banned hero word/phrase: 'elevate'
  - banned hero word/phrase: 'seamless'
  - banned hero word/phrase: 'journey'
  - banned hero word/phrase: 'learn more'
  - banned hero word/phrase: 'get started'
  - banned hero word/phrase: 'where innovation'
  - filler/placeholder text in visible copy: 'lorem ipsum'
  - hero has 3 buttons (maximum 2)
WARNINGS
```
