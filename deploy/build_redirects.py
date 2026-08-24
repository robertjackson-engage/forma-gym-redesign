#!/usr/bin/env python3
"""
Generate the formagym.com URL redirect map for the static-redesign cutover.

Input:  /tmp/live_current.txt  (live URL inventory, from the Wayback CDX API)
Output: deploy/_redirects          Cloudflare Pages / Netlify format
        deploy/redirect-map.csv    reviewable table
        deploy/UNMAPPED.md         URLs needing a human decision

Two groups:
  NATIVE   - the redesign emits this exact path (no redirect needed)
  REDIRECT - 301 to the mapped target
"""
import csv
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/tmp/live_current.txt"

# ---------------------------------------------------------------- NATIVE
# Paths the redesign will serve directly (Option A: directory-style output
# matching the live URLs exactly). No redirect required for these.
NATIVE = {
    "/", "/about", "/group-fitness", "/training", "/cryo",
    "/kidzville", "/rise", "/givesback", "/locations", "/locations/walnut-creek",
    "/locations/san-jose", "/locations/walnut-creek/spa", "/locations/san-jose/spa",
    "/join-now", "/trial-pass", "/outdoor-training", "/drbrainrx", "/app",
    "/merchant", "/accessibility-statement", "/privacy-policy",
    "/freeze-cancel", "/cardio-hiit",
    "/aqua-gfit", "/barre-gfit", "/cycle-gfit", "/dance-gfit", "/kbox-gfit",
    "/low-gfit", "/mat-gfit", "/meditation-gfit", "/pilates-gfit",
    "/sculpy-gfit", "/stretch-gfit", "/trx-gfit",
}

# ---------------------------------------------------------------- EXPLICIT
# Hand-mapped redirects. Ordered dict semantics not needed; exact match only.
EXPLICIT = {
    # --- old/duplicate class URLs -> current class pages
    "/aqua": "/aqua-gfit",
    "/cycle": "/cycle-gfit",
    "/yoga_gfit": "/yoga-gfit",
    "/yoga.html": "/yoga-gfit",
    "/athletic-gfit": "/group-fitness",
    "/groupfit": "/group-fitness",
    "/groupx": "/group-fitness",
    "/mind-body": "/group-fitness",
    "/mind-body/barre": "/barre-gfit",
    "/mind-body/mat-pilates": "/mat-gfit",
    "/mind-body/yoga": "/yoga-gfit",
    "/mind-body/gen-do": "/group-fitness",

    # --- membership / join funnel
    "/memberships": "/join-now",
    "/memberships-2": "/join-now",
    "/membership-change": "/freeze-cancel",
    "/enroll-online": "/join-now",
    "/get-started": "/join-now",
    "/fees.html": "/join-now",
    "/benefits.html": "/join-now",
    "/gift_certificates.html": "/join-now",

    # --- trial / pass funnel
    "/1-day-pass": "/trial-pass",
    "/1-day-trial-pass-active-form": "/trial-pass",
    "/yelp-trial": "/trial-pass",
    "/halfoff": "/join-now",
    "/email-offer": "/join-now",
    "/welcomeback": "/join-now",

    # --- training
    "/training-request": "/training",
    "/personal_training.html": "/training",
    "/youth_training.html": "/training",
    "/be_a_trainer.html": "/about",
    "/athlete-2": "/training",

    # --- legacy info pages (old Drupal/static site)
    "/index.html": "/",
    "/home-2": "/",
    "/about_forma.html": "/about",
    "/mission.html": "/about",
    "/general_info.html": "/about",
    "/Services.html": "/group-fitness",
    "/contact_us.html": "/contact",
    "/hours.html": "/locations",
    "/map.html": "/locations",
    "/parking.html": "/locations",
    "/open_gym.html": "/locations",
    "/chiropractic.html": "/recovery",
    "/walnut-creek-staff": "/locations/walnut-creek",

    # --- blog retired (Aug 2026) — all blog URLs go to the homepage
    "/blog": "/",

    # --- resolved on review
    "/schedules": "/group-fitness",
    "/san-jose-staff": "/locations/san-jose",
    "/pilates": "/pilates-gfit",
    "/rise-2-0": "/rise",
    "/sitemap": "/",
    "/tabata-workout": "/",
    "/happy_healthy_habits_2020": "/",
    "/massage_therapy_works_out_more_than_kinks": "/",
    "/recover_re-energize_whole-body_cryotherapy_forma_gym": "/cryo",

    # --- misc / orphan
    "/alc": "/group-fitness",
    "/gracie": "/group-fitness",
    "/display": "/",
    "/dog-hikes": "/givesback",
    "/events": "/",
    "/events-calendar": "/",
    "/fg-virtual": "/app",
    "/mindset": "/recovery",
    "/mindbodylab": "/recovery",
    "/sync-demo": "/",
    "/morning-exercise-download": "/",
    "/image_captcha": "/",
}

# Patterns handled in bulk
BLOG_TAXONOMY = re.compile(r"^/(category|author)/")
PAGED = re.compile(r"/page/\d+$")
LEGACY_ASSET = re.compile(r"^/sites/all/")
XMLRPC = re.compile(r"^/xmlrpc\.php$")
# Drupal-era system endpoints — never were pages
SYS_ENDPOINT = re.compile(r"^/(poormanscron|image_captcha)(/|$)")

# Conversion / ad-landing pages: MUST be reviewed by the marketing side.
# These are live ad destinations and tracking endpoints - a wrong target
# silently breaks attribution even if it doesn't 404.
NEEDS_DECISION = {
    "/digital-ads-wc1", "/digital-ads-wc2", "/digital-ads-sj1", "/digital-ads-sj2",
    "/thank-you-digital-ad", "/thank-you-trial-pass", "/thank-you-yelp",
    "/thank-you-email", "/thank-you-bold", "/morning-routine-thank-you",
}


def classify(url):
    """Return (group, target, note)."""
    if url in NATIVE:
        return "NATIVE", url, "redesign serves this path directly"
    if url in NEEDS_DECISION:
        return "DECIDE", "", "AD/CONVERSION PAGE - confirm target with marketing"
    if url in EXPLICIT:
        return "REDIRECT", EXPLICIT[url], "explicit mapping"
    if LEGACY_ASSET.match(url) or XMLRPC.match(url) or SYS_ENDPOINT.match(url):
        return "IGNORE", "", "asset/endpoint, not a page"
    if BLOG_TAXONOMY.match(url) or PAGED.search(url):
        return "REDIRECT", "/", "blog removed -> homepage"
    # Long hyphenated slugs with no other match = blog posts
    if re.match(r"^/[a-z0-9-]{15,}$", url):
        return "REDIRECT", "/", "blog removed -> homepage"
    return "DECIDE", "", "unclassified - needs review"


def main():
    with open(SRC) as fh:
        urls = [l.strip() for l in fh if l.strip()]

    rows = []
    for u in sorted(set(urls)):
        group, target, note = classify(u)
        rows.append({"live_url": u, "group": group, "target": target, "note": note})

    os.makedirs(HERE, exist_ok=True)

    # CSV for review
    with open(os.path.join(HERE, "redirect-map.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["live_url", "group", "target", "note"])
        w.writeheader()
        w.writerows(rows)

    # _redirects (Cloudflare Pages / Netlify)
    with open(os.path.join(HERE, "_redirects"), "w") as fh:
        fh.write("# formagym.com - redirect map for static redesign cutover\n")
        fh.write("# Generated by deploy/build_redirects.py. 301 = permanent (preserves SEO).\n")
        fh.write("# NATIVE paths are served directly by the site and need no rule.\n\n")
        for r in rows:
            if r["group"] == "REDIRECT" and r["target"]:
                fh.write(f'{r["live_url"]}  {r["target"]}  301\n')
        fh.write("\n# --- REVIEW REQUIRED: ad/conversion pages (uncomment once confirmed) ---\n")
        for r in rows:
            if r["group"] == "DECIDE":
                fh.write(f'# {r["live_url"]}  ???  301   # {r["note"]}\n')

    # Unmapped report
    decide = [r for r in rows if r["group"] == "DECIDE"]
    with open(os.path.join(HERE, "UNMAPPED.md"), "w") as fh:
        fh.write("# URLs needing a decision before cutover\n\n")
        fh.write("These have **no automatic target**. Ad/conversion pages are listed first —\n")
        fh.write("they are live ad destinations, so a wrong target breaks attribution.\n\n")
        fh.write("| Live URL | Why |\n|---|---|\n")
        for r in decide:
            fh.write(f'| `{r["live_url"]}` | {r["note"]} |\n')

    counts = {}
    for r in rows:
        counts[r["group"]] = counts.get(r["group"], 0) + 1
    print("URL inventory:", len(rows))
    for k in ("NATIVE", "REDIRECT", "DECIDE", "IGNORE"):
        print(f"  {k:9} {counts.get(k, 0)}")
    print("\nwrote: _redirects, redirect-map.csv, UNMAPPED.md")


if __name__ == "__main__":
    main()
