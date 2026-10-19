# Using commands

- A command starts at the beginning of a message and begins with `/`. Text after it is the request: `/edit make the headline shorter`.
- Commands are case-insensitive. `/Audit` works.
- If a message starts with a command that does not exist, say so and show the table. Do not guess.
- A command with no target applies to the page the user named, attached, or was last working on. If two pages could match, Claude asks which one.
- `/flawless` makes every command available without further setup and applies the rules to ordinary requests too.
- Commands never change colors, fonts, radius, or spacing unless the command is about the scheme (`/palette`, or the colors category of `/edit`).
- Every command that changes a file saves a snapshot first, so `/revert` can undo it.
