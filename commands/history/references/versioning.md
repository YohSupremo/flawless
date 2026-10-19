# Versioning

- Location: `<page>.history/v1.html`, `v2.html`, and so on, next to the page.
- A snapshot is saved by the pre-hook before any change by `/new` (when overwriting), `/edit`, `/palette` (apply), `/copy`, `/section`, `/mobile`, `/a11y`, and `/revert`.
- Versions are whole files. There is no diff view.
- Versions are numbered upward and never renumbered. Restoring v2 creates a new latest version containing the state before the restore.
- Snapshots are not saved for read-only commands (`/audit`, `/history`, `/flawless-c`).
