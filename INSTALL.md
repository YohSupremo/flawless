# Installing Flawless

Flawless is a folder of instructions, data, and small Python scripts. It has no runtime and no required dependencies beyond Python 3.9 or newer.

## 1. Put the folder where your agent looks for skills

The folder must contain `SKILL.md` at its top level. The agent reads that file first.

| Environment | Where to put it |
| --- | --- |
| Claude Code (personal) | `~/.claude/skills/flawless/` |
| Claude Code (one project) | `<project>/.claude/skills/flawless/` |
| Claude.ai skills upload | Zip the folder so `SKILL.md` is at the zip's top level, then upload it in Settings |
| Another agent with skill-file support | Wherever that tool loads skills from; point it at the folder containing `SKILL.md` |

Locations change between tool versions. If yours is not listed, check its documentation for "skills" and use the same layout. The folder name does not matter to Flawless. The skill's internal identifier is `clean-ui` (see [`docs/naming.md`](./docs/naming.md)).

## 2. How commands find the skill

Nothing is registered. `SKILL.md` has a description that tells the agent when to load the skill (UI work, or a message that starts with one of the slash commands). Once loaded, `SKILL.md` routes each command to `commands/<name>/COMMAND.md`. The slash commands are conventions the agent follows, not shell commands, so they work in any agent that loads the skill.

## 3. Dependencies

| Tool | Needs |
| --- | --- |
| `audit.py`, `build.py`, `validate.py`, `state.py`, `snapshot.py`, `palette.py` | Python 3.9+ standard library only |
| `extract_palette.py`, `image_harmony.py`, `grade_photo.py`, `analyze_layout.py` (the `/match` and `/ref` image tools) | Pillow (`pip install pillow`) |
| `browser_check.py` (optional) | Playwright (`pip install playwright && playwright install chromium`) |

Check the install:

```text
python core/scripts/validate.py
python -m unittest discover -s tests
```

## 4. Where state is stored

Session state (is the skill on, the current color and font scheme, which pages were audited) is one small JSON file. The location is the first of these that is set:

1. `FLAWLESS_STATE`, a file path
2. `CLEAN_UI_STATE`, the older name, still honored
3. `FLAWLESS_PROJECT_ROOT`, a folder; the file is `<folder>/.flawless-state.json`, and page paths are stored relative to that folder
4. `~/.clean-ui-state.json`, the default

Use option 3 to keep each project's state separate:

```text
export FLAWLESS_PROJECT_ROOT=/path/to/my-site
python core/scripts/state.py path      # prints the file in use
```

State is best effort. Writes are atomic, a corrupt file is moved to `<file>.corrupt` and a fresh state is started, and the file carries a `version` for future migrations. If it is lost, `python core/scripts/state.py init --scheme-from page.html` rebuilds the scheme from a page.

## 5. Project configuration (optional)

Copy [`flawless.config.example.json`](./flawless.config.example.json) to `flawless.config.json` next to your pages to set the strictness mode, brand colors, and accessibility target. See [`docs/configuration.md`](./docs/configuration.md).

## Uninstall

Delete the folder, and the state file if you want (`python core/scripts/state.py path` prints where it is).
