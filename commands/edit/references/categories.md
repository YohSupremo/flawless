# Edit categories

| Category | Covers | Follow-up question (current value first) | Rule check on the answer | Routed to |
|---|---|---|---|---|
| Colors and fonts | base, surface, text, accent, display font, body font | Which one: base, accent, text, fonts? Then the new value or direction | hue outside 230 to 300, no gradients, one accent, contrast passes | `/palette` apply mode, or direct font token edit |
| Copy | brand line, headline, supporting text, button labels, section text | Which part? Then what it should say or the tone | no banned phrases, no `/` or `·`, no invented stats, headline 8 words or fewer | `/copy` |
| Layout and spacing | section order, columns, alignment, padding, gaps, max width | Which part: order, alignment, columns, tighter or looser? | spacing on the scale, left-aligned by default, hero keeps headline, one sentence, two buttons | `/section` (add), `/mobile` (responsive), direct edit |
| Components and images | buttons, cards, radius, illustration or photo, motion | Which part: buttons, cards, radius, image, motion? | one radius everywhere (0 to 6px), no glass or glow, no looping animation, no gradient stand-in for a photo | direct edit; `/animate` for motion; `/match` after a photo change |

## Follow-up rules

- Offer the current value as the first option so "keep" is one tap.
- Never ask more than one follow-up round. If the user's answer is specific enough, apply it.
- If the answer fails its rule check, switch to the keep-or-override question (EDIT step 5) instead of applying.
