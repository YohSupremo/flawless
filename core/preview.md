# Preview mode (dry run)

Commands that change a page can show the change first. Add `--preview` to the request:

```text
/edit --preview make the headline shorter
/palette --preview warmer accent
/mobile --preview
/a11y --preview
```

Commands that support it are marked "Preview mode: yes" in `/help` (`supports_preview` in `manifest.json`).

## What a preview does

1. Resolve the target page exactly as the normal command would.
2. Work out the change in full, including the audit it would trigger.
3. **Write nothing.** No snapshot, no file change, no state change, no history entry.
4. Show the proposed change as a short before and after for each affected piece (a line of copy, a token value, a CSS rule), plus the audit result the page would have afterwards, run against a temporary copy.
5. Ask one question: apply, change the request, or drop it.
6. On "apply", run the real command (pre-hooks, change, post-hooks) using the previewed change. Do not redo the thinking or surprise the user with a different result.

## Rules

- A preview never edits the original file. Audit a temporary copy if the audit needs a file.
- A preview is not a hook skip for the real run: applying it still saves a snapshot first.
- If the change would alter the scheme, say so in the preview. That is the same confirmation the normal command would ask for.
- Keep it short. Show only what changes.

## Audit explain mode

Separate from preview, `/audit --explain` adds the design principle and a suggested fix under every finding. It runs `python core/scripts/audit.py <file> --a11y --mobile --explain`. See `docs/audit-coverage.md` for what the audit can and cannot check.
