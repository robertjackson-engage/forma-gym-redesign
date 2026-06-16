# Forma Gym — Redesign

A first-class static rebuild of [formagym.com](https://formagym.com) for Forma Gym's two
Bay Area clubs (Walnut Creek & San Jose). Modern editorial design system on a pure-black
canvas with Forma's cyan brand accent, the real Forma wordmark, scroll-reveal animations,
a full-screen menu, member/guest personalization, an interactive Join wizard, and a
Claude-powered AI concierge.

## View locally

```bash
python3 serve.py          # serves docs/ on http://localhost:4174
```
`serve.py` also proxies the AI concierge using the key in `.env` (gitignored) so it
never ships to the browser. To activate the concierge on the static GitHub Pages build,
visit any page with `#ck=YOUR_ANTHROPIC_KEY` once (stored locally, scrubbed from the URL).

## Pages (24)

index, about, group-fitness, training, recovery, cryo, spa, mindbodylab, kidzville, rise,
givesback, walnut-creek, san-jose, locations, join, contact, plus class pages
(cycle, yoga, pilates-reformer, barre, trx, aqua, dance, sculpt).

## Structure

- `docs/` — the built site (GitHub Pages root)
- `build.py` — static generator; edit content here, run `python3 build.py`
- `serve.py` — local server + Anthropic proxy (reads `.env`)
- `scrape/` — original-site copy & asset source (gitignored)

Content is Forma's own (verbatim where it sells, sharpened in their "Play Every Day" voice);
photography is from formagym.com. Forms are demo-only.
