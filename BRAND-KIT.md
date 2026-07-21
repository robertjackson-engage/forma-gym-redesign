# Forma Gym — Website Brand Kit
**The single source of truth for every change to the Forma Gym site.**
Repo: `robertjackson-engage/forma-gym-redesign` · Live: https://robertjackson-engage.github.io/forma-gym-redesign/
All values below are derived from the original **formagym.com** brand and locked here. If a change isn't consistent with this kit, don't ship it.

---

## 1 · Logo
- Primary lockup: white Forma wordmark on dark ground (`docs/assets/img/` — header uses the white mark; never recolor it).
- Clear space: keep at least the height of the "F" around the mark. Never skew, glow, or shadow the logo.
- On photography: only over dark or scrimmed areas — never over busy/light zones.

## 2 · Color
| Role | Token | Hex | Use |
|---|---|---|---|
| Forma Black | `--ink` | `#060709` | Primary ground (site is dark-first) |
| Panel Black | `--ink-2 / --ink-3` | steps up from ink | Cards, panels, alternating sections |
| White | `--white` | `#ffffff` | Primary text on dark |
| **Forma Cyan** | `--brand / --accent` | **`#08d6dd`** | THE brand accent — CTAs, highlights, serif accent words. Exact hex from formagym.com; never substitute another cyan/teal. |
| Cyan Soft | `--accent-soft` | `#6ef0f4` | On-dark accent text where full cyan is too loud |
| Cyan Deep | `--accent-ink` | dark cyan | Accent TEXT on light sections only (contrast-safe) |
| Ember Orange | secondary | `#fb8e28` | From formagym.com — rare secondary pop (tags, one-off highlights). Never compete with cyan; max one orange element per screen. |

**Rules:** cyan on black = the brand look. On light sections, use the deep cyan for text (never bright cyan on white). Buttons: cyan fill + near-black text, or outlined white.

## 3 · Typography (updated 2026-07-21)
Three voices, from the original site:

| Voice | Font | Source | Usage |
|---|---|---|---|
| **Display** | **Anton**, caps | Google Fonts | Structural headlines, nav, buttons. Uppercase, tight leading. |
| **Accent serif** | **Abril Fatface**, *upright only* | Google Fonts — **used on formagym.com** | The 1–2 accent word(s) inside headlines (`.serif` spans). **Never italic** (Abril has no italic; faux-italic is banned). Replaces the retired Instrument Serif italic. |
| **Body** | **Inter** | Google Fonts | All body copy, forms, UI. Stands in for the original site's Proxima Nova (Adobe-licensed) / Open Sans; if the client's Adobe Fonts kit becomes available, Proxima Nova may replace Inter site-wide — nothing else. |

**Type rules (non-negotiable):**
1. Headline accent = **max 2 words** per headline in Abril Fatface, colored cyan/cyan-soft. More than that reads as decoration.
2. Kinetic hero headlines: **≤16 characters per authored line**, 2–3 lines max. Audit after any headline change.
3. Nav labels never wrap (`white-space: nowrap` stays).
4. No new typefaces. Ever. Requests for "a fun font" route back to this kit.

## 4 · Components (the approved set)
Kinetic hero (video/photo + 2–3 line headline + ≤2 CTAs) · marquee strip · stats band (count-up) · split (photo + copy) · card grid · accordion · rows list · price cards · quote band · CTA band · view-chooser (Guest/Member) · member strip · AI concierge widget (cyan orb, bottom-right).
- Build pages from these blocks via `build.py` — no bespoke one-off layouts without updating this kit first.
- Radius, spacing, and animation timings live in `docs/assets/css/main.css` `:root` — change tokens, not individual rules.

## 5 · Photography
Real Forma clubs and members, dark and cinematic; cyan/magenta studio lighting (FORMA CYCLE) encouraged. No sterile stock. Verify any sourced image against its page context before use — never trust filenames.
**Crops:** wide banner assets placed in tall cards MUST set a subject-position utility on the `<img>` (`.obj-r` / `.obj-l`) so the subject survives the crop — default is center, which beheads edge-framed subjects. Mobile cards use a shorter 4/3.2 frame. Audit every new card image at 390px before shipping.

## 6 · Voice & copy
Energetic, welcoming, plain-spoken — "Play every day." Short sentences. Benefits before features. Walnut Creek & San Jose named where locality matters. Guests are nurtured ("I'm a guest" / two free weeks), members are served (schedules, hours, Kidzville, perks).

## 7 · Interaction standards
- Page entry is instant — `scroll-behavior: smooth` only arms after load (`html.smooth-scroll`); `scroll-padding-top` keeps anchored sections clear of the fixed header.
- Every CTA lands somewhere real (no dead `#` links).
- Reduced-motion users get no autoplaying kinetic effects.
- Mobile first: check 390px on every change; sticky CTAs stay.

## 8 · Shipping process
1. Edit `build.py` (content) or `main.css` tokens (style) → `python3 build.py`.
2. Check: no wrapped hero lines, no broken links/images, zero console errors.
3. Push to `main` → GitHub Action rebuilds and deploys production automatically (~2 min).
4. Anything not covered by this kit → update the kit in the same PR, or don't do it.

*Kit v1.0 — established 2026-07-21 (Abril Fatface adopted from formagym.com, replacing Instrument Serif italic).*
