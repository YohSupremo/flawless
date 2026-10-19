# Delivery

- Output a single self-contained HTML file (CSS in a `<style>` tag, fonts from Google Fonts with a real fallback stack) unless the user asks for a framework.
- Declare the tokens from `core/tokens/base.css` at the top so a retheme is a change to `:root` only.
- Run `python core/scripts/audit.py <file> --a11y --mobile` and walk `commands/audit/references/slop-audit.md`. Fix every error.
- Reply in two or three sentences: the accent, the fonts, anything you cut, and which content is sample. In session mode, end with one audit line.
- A published artifact gets small changes as edits on the publish call, so the file and page update together.
