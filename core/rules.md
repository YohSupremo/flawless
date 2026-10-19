# Core design rules

Every command that builds or changes UI follows these. They are defaults: when a user request breaks one, ask keep-or-override once, then follow the answer.

## Color

- **Base: any hue is allowed**, as long as it is not in the blue-violet range (see below). Near-black, charcoal, warm brown, forest green, deep maroon, sand, off-white, and plain white all work. Choose the base from the brand, not from habit. The base is always a flat solid color or a photo.
- **One accent**, used only for the primary button, one small marker (an eyebrow line, rating stars), and hover states. Roughly 5 percent of the screen. Never two competing accents.
- **Text:** full-opacity white or near-black for headlines, around 70 to 75 percent for body. No more than two gray shades.
- **Banned hue range:** HSL hue 230 to 300 degrees (blue-violet through purple) for any base, accent, tint, shadow, border, or glow. This is the default palette of AI-generated UI, so avoid it even when it is not a gradient. Plain neutrals (very low saturation) are fine, and so are blues outside this range only if the brand genuinely needs one (for example a teal at 180 to 200 degrees).
- **Banned entirely: gradients of any kind.** That covers `linear-gradient`, `radial-gradient`, `conic-gradient`, mesh or blurred color blobs, gradient text fills, gradient borders, and gradient buttons. Glassmorphism blur cards, neon glow shadows, and rainbow borders are banned too.
- **Legibility over a photo:** use a flat semi-transparent overlay (for example `background: rgba(14,14,14,.55)` on a pseudo-element), or position the text over a naturally dark part of the photo. Do not use a gradient scrim.
- **No photo available:** use a flat base color with a simple, flat, single-color illustration or a labeled placeholder. Never fill the gap with a gradient blob.

## Typography

- Headline: very large, heavy, uppercase or tight sentence case, line-height 0.95 to 1.05, left-aligned. Maximum two lines.
- Body: one size, 16 to 18px, line-height 1.5 to 1.6, max width about 40 characters per line in a hero.
- No gradient-filled text. No more than two weights per family in use.
- Do not set a tiny uppercase tracking-wide label above every section. At most one eyebrow on the whole page, and only if it carries real information.

## Symbols and punctuation

- **No `/` as a separator** ("Design / Build / Ship") and **no `·` or `•` as a separator** ("Fast · Secure · Simple"). Use separate elements with spacing, or rewrite as a sentence.
- No em dashes in UI copy. Use a period or a comma.
- No emoji as icons. No sparkle icons, no "AI" badges, no decorative arrows scattered around. One arrow icon inside a button is fine when it signals a link out.
- Icons come from a single consistent set at one stroke width, and only where they aid scanning.

## Information budget

The hero holds at most: headline, one supporting sentence, two buttons. A tiny trust line (like a star rating with a few words) is allowed as a single optional element, only if real data exists.

Do not add:
- Pill tags or badges ("New", "Trending", "Powered by AI", "2026 Edition") unless the user supplied them.
- A subheading and a paragraph and a tagline. Choose one.
- Statistic strips with invented numbers ("10K+ riders", "99% satisfaction"). Never fabricate figures, testimonials, logos, or reviews. Use clearly marked placeholders if the user needs them.
- Scroll indicators, "trusted by" rows, floating cards, fake UI overlays, marquees.
- Footer-corner microcopy that repeats the page ("Your next chapter starts here").

Every section after the hero gets one job, one heading, and the content itself. No section intro paragraph that restates the heading.

## Hero copy

- Say what it is and who it is for, in words a customer would use. "Built for the open road." works because it is short and concrete. 
- **Banned:** "Elevate", "Unleash", "Reimagine", "Seamless", "Empower", "Next-generation", "Crafted for the modern X", "Where X meets Y", "Journey", "Experience the difference", abstract nouns standing in for the product.
- Button labels are verbs or destinations: "Explore motorcycles", "Visit our showroom", "Book a test ride". Not "Get started" with no object, not "Learn more".
- Brand name appears once, small, above the headline.

## Layout variety

No two consecutive sections share a layout. Three equal cards in a row is allowed once per page and only for a true set of three. Alternate flat base and surface backgrounds. Pattern library: `commands/section/references/sections.md`.

## Invented content and placeholders

Never invent statistics, reviews, awards, logos, prices, hours, or addresses. Ask the user for real ones. For a layout preview, write short realistic sample content and say in your reply which parts are samples. Never write "Sample copy", "Lorem ipsum", "Coming soon", or bracketed placeholder tags in the page. Copy bank and rewrites: `commands/copy/references/copy.md`.

## Spacing and layout

Unwanted spacing is the second most common tell, so use a scale and stick to it: 4, 8, 16, 24, 32, 48, 64, 96.

- Hero: fill the viewport (`min-height: 100vh` or 100svh), content left-aligned in a column, vertically centered or bottom-weighted. Do not stack huge empty gaps between headline, text, and buttons. Headline to body: 24. Body to buttons: 32.
- Sections: 64 to 96 vertical padding on desktop, 48 on mobile. Not 160 or 200.
- Cards: 24 padding, 16 to 24 gap. Do not pad every container the same big amount.
- Content width: 1200 to 1280 max, with 24 to 48 side padding. Avoid centered narrow columns of text floating in empty space.
- Alignment: left-align by default. Center only short single-line elements.

## Components

- Primary button: solid accent, white text, 0 to 4px radius, 14 to 16px uppercase or medium weight, padding about 16 by 32. Secondary: transparent with a 1px border at about 30 percent white, same size.
- Corners: pick one radius (0 to 6px for rugged brands) and use it everywhere. No pill-shaped everything.
- Shadows: almost none. Separate surfaces with background tone or a 1px border.
- Imagery: one strong full-bleed photo with the subject on the right and text on the left over a darkened area. Check contrast. Use real image paths or a clearly named placeholder, never a gradient blob as a stand-in for a photo.
- Motion: one entrance fade or slide on load and a hover state on buttons. No parallax, floating, or looping animations.

## Responsive

Stack the hero on mobile: image behind with a stronger scrim, text bottom-aligned, buttons full width. Headline scales with `clamp()`, never below about 40px. Keep the same copy; do not add or remove content per breakpoint.


## Imagery harmony

A palette and a photo must agree. One is fixed and the other adapts; the user decides which, never Claude.

- **Palette fixed** (the user chose it, or has brand colors): grade the photo to the palette with `core/scripts/grade_photo.py`, or swap the photo for one in the accent's hue family.
- **Photo fixed** (brand photography, no palette yet): the base matches the photo's shadow color (color difference 6 or less) and the accent sits within 45 degrees of the photo's dominant hue, or the photo is neutral.
- **Measure** with `core/scripts/image_harmony.py`. Grades are baked into a new image file; never use CSS filters, blend modes, gradients, or blur to force a match.
- **Flat overlay** for text legibility is tinted with the base color (palette fixed) or the photo's shadow color (photo fixed), not pure black.
- No photo on the page: these checks do not apply.

## Headline wrapping and the eyebrow

- Headlines use `text-wrap: balance`. No single-word last line ("ROAD.") on its own.
- No eyebrow, kicker, overline, or tagline label above the headline by default. It is allowed only when it carries information the headline lacks (one per page), and never as a list of services joined with `&`, `/`, or `·`.
- `&` is fine inside a brand name; elsewhere write "and".

## Motion

- Animate `opacity`, `transform`, and `clip-path` only. Never width, height, top, left, margin, filter, or box-shadow.
- Durations 120 to 700ms; stagger 120ms at most; decelerate easing, no bounce or elastic.
- Each element has at most one entrance. Nothing loops. No parallax, floating, marquee, glow pulse, typewriter text, or shimmer.
- A `prefers-reduced-motion` rule is required whenever any motion exists. Tokens and the rule: `core/tokens/motion.css`.
