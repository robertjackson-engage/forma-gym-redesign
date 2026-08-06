# Forma → Salient "Brand Refresh" — Setup Guide (v1)

Goal: shift your Salient site toward the redesign's look (dark, editorial, cyan
accent, Anton + Montserrat) using Salient's own settings + a custom-CSS layer —
so pages stay editable in the Salient builder and you fine-tune from there.

**Do this on a Pressidium STAGING site first.** Nothing here touches the live
site until you push staging → live.

---

## Step 1 — Clone to staging (Pressidium)
In the Pressidium dashboard → your site → **Staging** → create/refresh a staging
copy of the live site. Work only on that URL until it's approved.

## Step 2 — Set the fonts (Salient Theme Options → Typography)
Salient can load Google Fonts natively.
- **Headings (H1–H4):** `Anton`
- **Body / paragraphs / H5–H6:** `Montserrat`
- If Salient exposes per-heading controls, set H1–H3 to Anton; leave smaller
  UI text on Montserrat.

## Step 3 — Set the accent color (Salient Theme Options)
- **Theme Options → (General / Styling) → Accent Color:** `#08d6dd`
  This recolors links, buttons, and highlights site-wide in one shot.

## Step 4 — Paste the CSS layer
- **Theme Options → Custom CSS/JS → Custom CSS**
- Paste the entire contents of `forma-refresh.css`.
- Save, then hard-refresh the staging site (Cmd/Ctrl+Shift+R).

## Step 5 — Fine-tune per page in the builder
The CSS gives you global vibe + a few helper classes you apply as you edit:

| Want | Do this in the builder |
|---|---|
| Cyan accent on a word in a heading | Wrap it: `<span class="forma-accent">Doom</span>` |
| A dark editorial section | Set the Row background to `#060709`, or add Row CSS class `forma-section-dark` |
| Outlined (secondary) button | Add the button Extra Class `forma-btn-outline` |
| Small cyan-dash eyebrow label | Add a Text block with `<span class="forma-eyebrow">Walnut Creek & San Jose</span>` |

(Salient rows/elements accept a **CSS Class / Extra Class** field under their
Design/Advanced tab — that's how you attach the helpers above.)

---

## Honest notes
- This is a **starting refresh**, not a pixel copy — exactly the "refresh then
  fine-tune" you asked for. Expect to nudge spacing/sizes per page.
- Selector caveat: Salient's exact class names vary slightly by version. If a
  button or heading doesn't pick up the style, tell me the element and I'll
  tighten the selector to your Salient version.
- The special interactive pieces from the redesign (video hero autoplay, the
  Join wizard, guest/member personalization, AI concierge) are **not** in this
  CSS layer — those need small embeds/shortcodes. We can add them one at a time
  after the base refresh looks right.
- Reverting is trivial: delete the CSS from the box and reset the two Theme
  Option values.

## Suggested first test
Apply Steps 1–4, then open your **homepage** on staging and drop in one dark
Row with a big Anton headline + a `forma-accent` word + a cyan button. If that
looks and edits the way you want, we roll it across the key pages.
