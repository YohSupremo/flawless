# Reference tokens: dark motorcycle hero

Derived from the reference screenshot. Use as a starting point when the user wants this exact look; swap the accent and fonts for other brands.

```css
:root {
  --base: #0e0e0e;
  --surface: #181818;
  --text: #ffffff;
  --text-muted: rgba(255,255,255,.72);
  --line: rgba(255,255,255,.28);
  --accent: #f4502e;          /* orange-red, used sparingly */

  --font-display: "Bebas Neue", "Barlow Condensed", Impact, sans-serif;
  --font-body: "Barlow", system-ui, sans-serif;

  --s1: 4px;  --s2: 8px;  --s3: 16px; --s4: 24px;
  --s5: 32px; --s6: 48px; --s7: 64px; --s8: 96px;
  --radius: 2px;
}
```

## Hero skeleton

```html
<section class="hero">
  <div class="hero-copy">
    <p class="brand">Torque Motor Co.</p>
    <h1>Built for<br>the open road.</h1>
    <p class="lede">More than a motorcycle. Find the ride that moves you.</p>
    <div class="actions">
      <a class="btn btn-primary" href="#models">Explore motorcycles</a>
      <a class="btn btn-secondary" href="#showroom">Visit our showroom</a>
    </div>
  </div>
</section>
```

```css
.hero {
  min-height: 100svh;
  display: flex; align-items: center;
  padding: 0 clamp(24px, 5vw, 64px);
  position: relative;
  background: var(--base) url("hero.jpg") right center / cover no-repeat;
  color: var(--text);
}
/* flat overlay for legibility, no gradient */
.hero::before { content: ""; position: absolute; inset: 0; background: rgba(14,14,14,.55); }
.hero-copy { position: relative; }
.hero-copy { max-width: 560px; }
.brand { font: 600 16px var(--font-body); letter-spacing: .04em; text-transform: uppercase; margin: 0 0 var(--s4); }
h1 { font: 400 clamp(56px, 9vw, 112px)/.95 var(--font-display); text-transform: uppercase; margin: 0 0 var(--s4); }
.lede { font: 400 18px/1.55 var(--font-body); color: var(--text-muted); max-width: 36ch; margin: 0 0 var(--s5); }
.actions { display: flex; gap: var(--s3); flex-wrap: wrap; }
.btn { padding: 16px 32px; border-radius: var(--radius); font: 600 14px var(--font-body); text-transform: uppercase; letter-spacing: .04em; text-decoration: none; }
.btn-primary { background: var(--accent); color: #fff; }
.btn-secondary { border: 1px solid var(--line); color: var(--text); }
```

There are no gradients anywhere. If the photo's left side is too bright for text, raise the overlay opacity or crop the photo so the subject sits right and a dark area sits left.

Base alternatives (all flat, none in the blue-violet range): charcoal `#161616`, warm espresso `#1f1612`, forest `#0f1f17`, deep maroon `#1e0f12`, sand `#efe8dc`, paper `#f7f5f0`.
