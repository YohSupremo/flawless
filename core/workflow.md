# Build workflow

Used by `/new`, and by any session-mode request that produces a new page or component. Thresholds come from `core/tokens/rules.json`; rules are in `core/rules.md`.

1. **Decide the one thing.** Write down, in plain words, what the page is and what the visitor should do. That becomes the headline and the primary button.
2. **Settle the scheme.** Priority: the session scheme in state (`core/state.md`), then the user's page or brand colors, then a palette the user picks through `/palette`. One flat base, one accent, outside the blue-violet range.
3. **Pick fonts** for the brand: one display, one body, with real fallback stacks. Reuse the session fonts when they exist.
4. **Write copy plain, then cut.** Use `/copy` rules (`commands/copy/references/copy.md`). Never make it more poetic afterward.
5. **Build from `core/tokens/base.css`** and the hero skeleton in `commands/new/tokens/hero.html`. Add sections through `/section` patterns, not ad hoc.
6. **Run the post-hooks** in `core/hooks.md` (audit, state update) and fix every error before delivering.
