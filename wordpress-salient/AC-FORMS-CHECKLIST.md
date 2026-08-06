# ActiveCampaign Forms — Migration/Refresh Test Checklist

Account: **formagym.activehosted.com** · **6 live forms**. Do all testing on the
**Pressidium staging** site first. Since we're *refreshing* the existing Salient
site (not replacing it), these forms should already be present — the goal is to
confirm the restyle didn't break them and that submissions still reach AC.

---

## Form inventory (what to test, where)

| Form | Live page(s) | Purpose | Watch for |
|---|---|---|---|
| **9** | Footer of **every** page | Newsletter / email capture | It's sitewide — check it in the footer on several different templates |
| **33** | ~25 service/class pages (about, training, group-fitness, spa, all `*-gfit`, cryo, kidzville, givesback, merchant, outdoor…) | Inline "get info" lead form | Appears the most places — spot-check ~5 different page types |
| **49** | /blog/ | Blog subscribe (name + email) | Simple; confirm placeholders styled |
| **72** | /cryo/ | Cryo lead — **includes phone field** | Verify the phone field renders + validates |
| **93** | /freeze-cancel/ | Freeze / cancel request | Has an extra field (`field[376]`) — confirm it shows |
| **103** | /join-now/ | Join / membership — **has option groups (`ca[…]`)** | Most complex: test every checkbox/radio option group submits |

---

## Per-form test (run for each of the 6)

For each form, on **staging**:

- [ ] **Renders** — the form appears on the page (AC loads via JS; give it a second).
- [ ] **Styled on-brand** — dark inputs, bone labels, **cyan submit button**, readable placeholder text; nothing white-on-white or clipped.
- [ ] **All fields present** — no field hidden/removed by the refresh CSS (compare against the live site). Especially: phone (72), extra field (93), option groups (103).
- [ ] **Required-field validation** still fires (submit empty → see the orange error).
- [ ] **Submit a real test entry** (use a tag-able test email, e.g. `yourname+actest9@formagym.com`).
- [ ] **Confirmation** — the form's success message / redirect happens as before.
- [ ] **Lands in ActiveCampaign** — the test contact appears in `formagym.activehosted.com`, with the right **list/tag** and any **automation** triggered (this is the real proof, not just the form UI).

## Sitewide / cross-cutting checks

- [ ] **Form 9 in the footer** works on Home + a class page + a location page (different templates).
- [ ] **Mobile** — forms usable and styled at phone width.
- [ ] **Submit button visible & clickable** — confirm the refresh CSS didn't hide `._submit` anywhere.
- [ ] **No duplicate/broken embeds** — each page shows its form once.
- [ ] **Spam/consent** — if any form has a reCAPTCHA or consent checkbox, confirm it still appears and blocks/allows correctly.

## If a form looks wrong after the refresh
AC injects its own high-specificity `<style>` per form. If a rule doesn't take,
we scope it to the form id — e.g. `#_form_103_ ._submit { … }`. Note the **form
number + field** that's off and Justin/Claude tighten the selector.

---

## Sign-off
- [ ] All 6 forms styled, submitting, and landing in ActiveCampaign on **staging**
- [ ] Re-verify the 6 once more **after** pushing staging → live
