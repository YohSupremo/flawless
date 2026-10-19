# Session state

Commands share one small state record so they stay consistent. It is managed by `core/scripts/state.py`.

```json
{
  "active": true,
  "scheme": { "base": "#f1eadd", "surface": "#e7dfce", "text": "#1f1a15",
              "accent": "#c2441c", "font_display": "Anton", "font_body": "DM Sans", "radius": "6px" },
  "pages": { "ember-coffee.html": { "audit": "clean" } }
}
```

## Who reads and writes

| Field | Written by | Read by |
|---|---|---|
| `active` | `/flawless` (on, off) | every command, to decide whether to apply session rules |
| `scheme` | `/flawless`, `/palette`, `/match`, `/edit` (colors and fonts), `/ref` (only when the user asks to take the reference's colors) | `/new`, `/section`, `/copy`, `/mobile`, `/audit`, `/a11y` |
| `pages` | post-hook after any command that changes a file, and `/new` | `/flawless status`, `/history`, `/revert`, `/audit` |

## Rules

- The state file is best effort. The conversation itself is the record: also state the session scheme in plain words when it is set or changed.
- If the file is missing, rebuild the scheme from the newest page with `python core/scripts/state.py init --scheme-from <page.html>`.
- A command never changes `scheme` as a side effect. Only the commands in the table above write it, and only when the user asked for a color or font change.
- State is per conversation. A new conversation starts empty.
