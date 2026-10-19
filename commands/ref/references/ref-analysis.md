# Reading a reference for its idea

A reference is evidence of what works, not a template to repaint. `/ref` extracts the idea and builds something new from it. Copying the layout and swapping the palette produces a knock-off; understanding why the reference works lets you apply it to any subject.

## Two layers

| Layer | What it is | What to do with it |
|---|---|---|
| **Principles** (transferable) | Why the design works: focal point, hierarchy, content budget, contrast strategy, tone, rhythm | Keep these |
| **Surface** (specific) | The reference's exact photo, brand name, copy, palette, fonts, pixel positions | Replace these |

If the user asks for a close match, they must say so. Default to idea only.

## Steps

1. **Look at the image** and run `core/scripts/analyze_layout.py` and `core/scripts/extract_palette.py`. Numbers support what you see; they do not replace it.
2. **Write the idea brief** (format below). Keep it to what a designer would say out loud, in plain words.
3. **Show the brief to the user** and ask what to carry over: all principles, or a chosen few. One question.
4. **Build with the principles and a new surface:** new subject, new copy written from `commands/copy/references/copy.md`, and fonts chosen for this brand. Palette priority: the existing page's current colors first, then the brand's own, then a pick from `commands/palette/references/palettes.md`. The reference's palette and fonts are never used unless the user asks for them by name.
5. **Check for echoes.** Keep a do-not-reuse list of the reference's text and run the avoid-list audit after building. A repeated headline or eyebrow is an error.
6. **Change at least one structural choice** so the result is not a copy: flip the subject side, change the type style (condensed to serif, say), change the button treatment, or restructure the lower sections. Say which one you changed.
7. Run `/match` if the page has a photo (the palette stays fixed when the user stated it; the photo adapts), then audit and deliver.

## Idea brief format

Use these headings, one or two lines each:

- **Focal point:** what the eye lands on first and why (size, contrast, isolation).
- **Composition:** where text and subject sit, how they share the frame, how much space is left empty.
- **Hierarchy:** the order the eye reads (for example brand line, headline, supporting line, buttons) and the size jump between levels.
- **Content budget:** how many elements the hero holds and what was left out.
- **Contrast strategy:** how legibility is protected (dark area under text, flat overlay) and how the accent is rationed.
- **Type character:** the personality of the type (heavy condensed, wide, serif, light) and why it suits the subject.
- **Copy tone:** length, directness, and sentence shape of the words.
- **Rhythm:** spacing between elements and sections; calm or dense.
- **Mood:** two or three plain adjectives.
- **Rule breakers:** anything in the reference that conflicts with this skill (extra tags, symbols, stat lines, gradients), and that it will be left out.

## Example: the Torque Motor Co. hero

- **Focal point:** the motorcycle, lit from the side against a dark room; it is the brightest and most detailed thing in the frame.
- **Composition:** text in a left column over the darkest area, subject on the right at large scale, about two thirds of the frame calm.
- **Hierarchy:** small brand line, very large two-line headline, short supporting lines, two buttons. The headline is several times larger than anything else.
- **Content budget:** five elements in the hero. No navigation clutter, no cards.
- **Contrast strategy:** text sits on dark; the orange accent appears only on the primary button and small markers, about one percent of the pixels.
- **Type character:** heavy condensed capitals, rugged and mechanical, matching the subject.
- **Copy tone:** short, concrete, confident. "Built for the open road."
- **Rhythm:** generous but controlled spacing; headline close to its supporting text, buttons set apart.
- **Mood:** rugged, quiet, confident.
- **Rule breakers:** the star rating line, the corner microcopy, the "collection 2026" label. Left out in a build.

A new build from this idea for, say, a bicycle workshop would keep the large subject on one side, dark calm text zone, one rationed accent, a heavy headline, and five hero elements. It would change the surface: a warm paper base with dark text, a serif or wide display face, the subject on the left, and copy such as "Bikes fixed while you wait."
