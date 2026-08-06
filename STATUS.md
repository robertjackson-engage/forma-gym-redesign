# formagym.com — Replacement Site Status

**For:** Robert Jackson
**From:** Justin Kanalakis
**Updated:** 2026-08-06
**Repo:** `robertjackson-engage/forma-gym-redesign` · latest commit `e31d22a`

---

## Situation

formagym.com (WordPress / Salient, hosted on Pressidium) was compromised and is
currently returning **HTTP 403** — walled off, not serving.

The plan is to replace it with the **static redesign** in this repo. A static
site has no database, no PHP and no plugins, so the attack surface that was
exploited simply isn't there. It is built, tested, and ready pending the
decisions listed below.

---

## Where things stand

| Area | Status |
|---|---|
| Redesign site (34 pages) | ✅ Built and working |
| Live URL preservation | ✅ Done — see below |
| Redirect map (198 URLs) | ✅ 125 rules generated |
| Link/asset integrity | ✅ 2,747 links checked, 0 broken |
| Member freeze/cancel page | ✅ Built (needs form + policy text) |
| Blog | ✅ Retired, URLs redirected |
| **Hosting decision** | ❌ **Not made — blocking** |
| **Ad/conversion URLs** | ❌ **10 need marketing input — blocking** |
| ActiveCampaign forms | ❌ Not yet re-embedded |
| Pushed to GitHub | ⏳ Pending (Justin, with his access token) |

---

## The URL question (most important for SEO + ads)

The redesign originally used different URLs than the live site
(`/join.html` vs `/join-now/`, `/aqua.html` vs `/aqua-gfit/`, and so on).
Launching that way would have broken **every** existing search result, inbound
link and ad landing page.

**This is fixed.** The site now builds to the exact paths formagym.com already
uses. A full inventory of the live site was taken (via the Wayback Machine,
since the site itself is down) and every URL accounted for:

| Group | Count | Meaning |
|---|---|---|
| **Native** | 35 | New site serves the identical URL — nothing changes |
| **Redirect** | 125 | 301 redirect to the closest equivalent |
| **Needs decision** | 10 | Ad/conversion pages — see below |
| **Ignore** | 28 | Old fonts, `xmlrpc.php`, cron endpoints — never were pages |

Full detail: `deploy/redirect-map.csv` · rules: `deploy/_redirects`

---

## ⚠️ What we need from you / marketing

### 1. Ten ad + conversion URLs (highest priority)

These are live ad destinations and conversion-tracking endpoints. They have
been deliberately **left unmapped rather than guessed**, because a wrong target
does not 404 — it silently breaks attribution, which is worse, since nobody
notices for weeks.

**Ad landing pages** (note they are club-specific — wc = Walnut Creek, sj = San Jose):
- `/digital-ads-wc1`, `/digital-ads-wc2`
- `/digital-ads-sj1`, `/digital-ads-sj2`

**Thank-you / conversion pages:**
- `/thank-you-digital-ad`, `/thank-you-trial-pass`, `/thank-you-yelp`
- `/thank-you-email`, `/thank-you-bold`, `/morning-routine-thank-you`

**What would settle it:** the landing-page URLs and conversion-tracking
destinations from Google Ads / Meta Ads Manager. That tells us which are still
active and what each must do.

Note: if Google Ads counts a conversion when someone reaches
`/thank-you-trial-pass`, that page may need to **exist as a real page**, not be
redirected — otherwise conversion tracking stops working.

### 2. Where should the site be hosted?

DNS is already on **Cloudflare** (nameservers `cody`/`pam.ns.cloudflare.com`;
the domain is registered at Domain.com). **Cloudflare Pages** is the natural
fit — free, fast, and DNS is already there. Alternatives: Netlify, or static
hosting on Pressidium. This is the long pole for launch.

### 3. Membership policy wording

The new `/freeze-cancel/` page is built but contains **no policy specifics** —
no freeze durations, fees, or notice periods. Those are contractual terms and
were not invented. Please supply the current wording.

### 4. ActiveCampaign forms

The live site runs **6 AC forms** (account `formagym.activehosted.com`). The
static redesign's forms are currently demo-only placeholders and **submit
nowhere**. They must be re-embedded before launch or leads are lost:

| Form | Where | Purpose |
|---|---|---|
| 9 | Every page (footer) | Newsletter capture |
| 33 | ~25 service/class pages | Lead / "get info" |
| 49 | Blog | *No longer needed — blog retired* |
| 72 | /cryo/ | Cryo lead (includes phone) |
| 93 | /freeze-cancel/ | Freeze/cancel request |
| 103 | /join-now/ | Join / membership (most complex) |

Test plan: `wordpress-salient/AC-FORMS-CHECKLIST.md`

### 5. Security follow-up

Independent of the new site — worth confirming:
- **Entry vector** from Pressidium (vulnerable plugin vs. stolen credentials).
  This determines whether it was a software problem or an account problem.
- **Rotate credentials** regardless: WordPress, Pressidium, Cloudflare,
  Domain.com, ActiveCampaign, GitHub. A clean site behind old passwords can be
  re-compromised.

---

## What changed in the site itself

- **Hero video** — club walkthrough footage, with separate desktop and mobile
  cuts loaded per device.
- **Offer language removed** — "two free weeks", "free pass", "free trial" and
  similar wording is gone site-wide; primary CTAs now read "Visit Us".
  `$0 enrollment` was kept.
- **About headline** — now "More than a gym. It's Family."
- **Blog retired** — not considered relevant to the site or SEO.
- **New member page** — `/freeze-cancel/`, visible only in Member view.

---

## Notes / open items

- `/contact/` and `/recovery/` are **new** pages with no equivalent on the old
  site. Harmless (no old URL to break), but Google hasn't seen them.
- `/yoga-gfit/` is an inference. The old site used `/yoga_gfit` with an
  underscore, which breaks the pattern every other class page follows. The
  hyphenated version is served and the underscore one redirects to it — worth
  a sanity check against Search Console.
- Old blog URLs (~58 including `/category/` and `/author/` archives) redirect
  to the homepage. They will drop out of Google's index over several weeks.

---

## Suggested order of operations

1. Marketing supplies the ad/conversion URL targets *(unblocks the redirect map)*
2. Pick a host and stage the site there *(nothing points at it yet — zero risk)*
3. Re-embed the ActiveCampaign forms and test all submissions land in AC
4. Verify redirects and spot-check ad landing pages on staging
5. Cut DNS over in Cloudflare
6. Re-verify forms and key URLs on the live domain

Steps 2–4 can all happen before any DNS change, so the current site's downtime
is unaffected by this work.
