#!/usr/bin/env python3
# FORMA GYM — static site generator (Walnut Creek & San Jose)
import os, time

OUT = os.path.join(os.path.dirname(__file__), "docs")
IMG = "assets/img"
# The club photo strip from formagym.com, in the order the live site runs it.
# These are Forma's own carousel images — pulled from the live site so the
# redesign's strips show the real thing rather than stand-ins.
STRIP_PHOTOS = [
    "SJ_pool_662x501_v1.jpg",
    "gym_floor2_WC_500px.jpg",
    "gym_floor3_WC_500px.jpg",
    "SJ_dumbells_662x501_v1.jpg",
    "carousel_MOTR_v1.jpg",
    "gym_floor_WC_500px.jpg",
    "gym_floor3_SJ_500px.jpg",
    "WC_pool_class_662x501_v1.jpg",
    "massage_300px_high.jpg",
    "cycle_studio_SJ_500px.jpg",
]

# Path prefix for when the site is NOT served from a domain root.
#
# The deploy workflow rebuilds from source and publishes its own docs/, so this
# default is what actually reaches GitHub Pages — and Pages serves the project
# at /forma-gym-redesign/. Hence the default is the preview prefix, not "".
#
# FOR THE formagym.com CUTOVER: build with SITE_BASE="" (the site will sit at a
# domain root). Setting it in .github/workflows/build-deploy.yml would be the
# tidier home for this, but pushing workflow changes needs a PAT with `workflow`
# scope, which the current token lacks.
#   production: SITE_BASE="" python3 build.py
SITE_BASE = os.environ.get("SITE_BASE", "/forma-gym-redesign").rstrip("/")

FOUNDED = 2009            # Walnut Creek opened; drives the "years in the Bay Area" stat

HERO_VIDEO_DESKTOP = "assets/video/SJ_WC_walkthru_combo_desktop_hero_18sec.m4v"  # landscape 1280x720, 18s
HERO_VIDEO_MOBILE = "assets/video/WC_SJ_mobile_hero_18sec_edit.m4v"    # portrait 720x1280, 18s, ≤820px only

# ============================================================ CMS content engine
CONTENT = os.path.join(os.path.dirname(__file__), "content")
import glob as _glob, re as _re

def _parse_md(path):
    raw = open(path, encoding="utf-8").read(); meta, body = {}, raw
    m = _re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", raw, _re.S)
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, _, v = line.partition(":"); meta[k.strip()] = v.strip().strip('"').strip("'")
        body = m.group(2)
    return meta, _md_to_html(body.strip())

def _md_to_html(md):
    md = md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    out, lines, i = [], md.split("\n"), 0
    while i < len(lines):
        ln = lines[i]
        if _re.match(r"^\s*[-*]\s+", ln):
            items = []
            while i < len(lines) and _re.match(r"^\s*[-*]\s+", lines[i]):
                items.append("<li>" + _inline(_re.sub(r"^\s*[-*]\s+", "", lines[i])) + "</li>"); i += 1
            out.append("<ul>" + "".join(items) + "</ul>"); continue
        h = _re.match(r"^(#{1,4})\s+(.*)$", ln)
        if h:
            lvl = len(h.group(1)); out.append(f"<h{lvl+1}>{_inline(h.group(2))}</h{lvl+1}>"); i += 1; continue
        if ln.strip() == "":
            i += 1; continue
        para = [ln]; i += 1
        while i < len(lines) and lines[i].strip() and not _re.match(r"^(#{1,4}\s|\s*[-*]\s)", lines[i]):
            para.append(lines[i]); i += 1
        out.append("<p>" + _inline(" ".join(para)) + "</p>")
    return "\n".join(out)

def _inline(t):
    t = _re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = _re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    t = _re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return t

def load_collection(folder):
    items = []
    for p in _glob.glob(os.path.join(CONTENT, folder, "*.md")):
        meta, body = _parse_md(p)
        meta["_slug"] = os.path.splitext(os.path.basename(p))[0]; meta["_body"] = body
        items.append(meta)
    items.sort(key=lambda m: m.get("date", ""), reverse=True)
    return items

def cms_img(path):
    return (path or "").lstrip("/") or f"assets/img/slider-locations_turf_alysse_torey.jpg"

def fmt_date(d):
    months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    m = _re.match(r"(\d{4})-(\d{2})-(\d{2})", d or "")
    return f"{months[int(m.group(2))]} {int(m.group(3))}, {m.group(1)}" if m else (d or "")
# ============================================================ end CMS content engine

V = str(int(time.time()))  # cache-bust CSS/JS on every build

LOGO = "assets/img/forma-logo.svg"   # white vector wordmark


def brand_logo(cls=""):
    return f'<img class="brand__logo {cls}" src="{LOGO}" alt="Forma Gym" width="385" height="34" />'


# Brand glyphs, inline so they inherit currentColor and cost no extra request.
SOCIAL_ICONS = {
    "facebook": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M15.1 8.6h2.1V5.7c-.36-.05-1.6-.16-3.04-.16-3.01 0-5.07 1.79-5.07 5.07V12H6.4v3.4h2.69V23h3.4v-7.6h2.78l.42-3.4h-3.2v-1.98c0-.98.27-1.65 1.61-1.65z"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5.2"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1.15" fill="currentColor" stroke="none"/></svg>',
    "x": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 3h3.2l-7 8 8.2 10h-6.4l-5-6.1L4.7 21H1.5l7.5-8.6L1.1 3h6.6l4.5 5.6L17.5 3zm-1.1 16.1h1.8L7.7 4.8H5.8l10.6 14.3z"/></svg>',
    "youtube": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M22.5 7.2a2.75 2.75 0 0 0-1.94-1.94C18.85 4.8 12 4.8 12 4.8s-6.85 0-8.56.46A2.75 2.75 0 0 0 1.5 7.2C1.05 8.9 1.05 12 1.05 12s0 3.1.45 4.8a2.75 2.75 0 0 0 1.94 1.94c1.71.46 8.56.46 8.56.46s6.85 0 8.56-.46a2.75 2.75 0 0 0 1.94-1.94c.45-1.7.45-4.8.45-4.8s0-3.1-.45-4.8zM9.8 15.3V8.7l5.7 3.3-5.7 3.3z"/></svg>',
}

# Facebook and Instagram are per-club; X and YouTube are one brand-wide account,
# so both clubs point at the same handle — matching formagym.com's footer.
SOCIAL_X = "https://twitter.com/FormaGym"
SOCIAL_YOUTUBE = "https://www.youtube.com/channel/UCT5TxhGM45g22KkG4TEaVAw"


def socials(handle, club):
    links = [
        ("facebook", f"https://www.facebook.com/{handle}/", "Facebook"),
        ("instagram", f"https://www.instagram.com/{handle}/", "Instagram"),
        ("x", SOCIAL_X, "X"),
        ("youtube", SOCIAL_YOUTUBE, "YouTube"),
    ]
    out = f'<div class="socials socials--club" role="list" aria-label="{club} social media">'
    for key, href, label in links:
        out += (f'<a role="listitem" href="{href}" target="_blank" rel="noopener" '
                f'aria-label="{club} on {label}">{SOCIAL_ICONS[key]}</a>')
    return out + "</div>"


NAV = [
    ("Classes", "group-fitness.html"),
    ("Training", "training.html"),
    ("Recovery", "recovery.html"),
    ("Locations", "locations.html"),
    ("About", "about.html"),
]

MENU = [
    ("Home", "index.html"),
    ("Group Fitness", "group-fitness.html"),
    ("Personal Training", "training.html"),
    ("Outdoor Fitness", "outdoor-training.html"),
    ("Recovery &amp; Cryo", "recovery.html"),
    ("The Spa", "spa.html"),
    ("Mind Body LAB", "mindbodylab.html"),
    ("DrBrainRX", "drbrainrx.html"),
    ("Kidzville", "kidzville.html"),
    ("RISE Program", "rise.html"),
    ("Forma Gives Back", "givesback.html"),
    ("Walnut Creek", "walnut-creek.html"),
    ("San Jose", "san-jose.html"),
    ("Locations &amp; Hours", "locations.html"),
    ("About Forma", "about.html"),
    ("The Forma App", "app.html"),
    ("Join Now", "join.html"),
    ("Book a Tour", "contact.html#tour"),
]

# Every group-fitness format gets its own detail page.
# slug, title, img, lead, short (for the group-fitness list)
CLASS_PAGES = [
    ("aqua", "Aqua Studio", "slider-aqua_v3.jpg",
     "A refreshing, low-impact workout in our heated pools. Improve cardiovascular fitness, muscle strength and conditioning with water's natural resistance — ideal for every level, including recovery and joint-friendly training.",
     "Low-impact strength &amp; cardio in heated water"),
    ("barre", "Barre", "slider-loan_long_stretch_v5-1.jpg",
     "Ballet, Pilates and strength training in one elegant burn. Using the barre for support, you'll move through small, isometric movements that target specific muscle groups for a toned, sculpted physique.",
     "Ballet, Pilates &amp; strength for a sculpted body"),
    ("cardio-hiit", "Cardio + HIIT", "slider-cardio_HIIT_v1.jpg",
     "High-energy intervals that torch calories and build serious conditioning. Cardio and HIIT classes alternate bursts of intense effort with active recovery — an efficient, heart-pumping way to get stronger and faster, scaled to every level.",
     "High-intensity intervals that torch calories"),
    ("cycle", "Cycle Studio", "SJ_cycle_studio_2500px.jpg",
     "An exhilarating, immersive cardio ride for every fitness level. Simulated terrain, climbs, sprints and endurance sets — all driven by the beat. The music keeps you engaged and pushes you to match its rhythm and intensity.",
     "Immersive, beat-driven indoor rides"),
    ("dance", "Dance", "slider-locations_group_dance.jpg",
     "Music, movement and pure joy. Our dance classes combine rhythm and technique into a workout that never feels like one — building coordination, cardio and confidence while you have an absolute blast.",
     "Cardio that feels like a celebration"),
    ("low-impact", "Low Impact + Balance", "slider-LIT_balance_v3.jpg",
     "Build fitness, strength, coordination and stability with a gentler approach. Low Impact and Balance classes create a supportive environment for anyone who prefers — or needs — to move with care, without sacrificing results.",
     "Gentle, supportive strength &amp; stability"),
    ("kickboxing", "Kickboxing + Martial Arts", "slider-kickbox_v3.jpg",
     "Dynamic, engaging classes that combine cardiovascular fitness, self-defense technique, discipline and mental focus — improving strength, flexibility, coordination and confidence while you punch, kick and sweat it out.",
     "Power, focus and serious cardio"),
    ("meditation", "Meditation + Breathwork", "slider-meditate_v2.jpg",
     "A peaceful, rejuvenating space for relaxation, stress reduction and mental clarity. Learn and practice meditation and breathwork techniques under expert guidance — for everyone from first-timers to seasoned practitioners.",
     "Reset your nervous system and mind"),
    ("mat-pilates", "Mat Pilates", "slider-mat_pilates_v2.jpg",
     "A comprehensive, full-body workout focused on core strength, flexibility and muscular endurance. Classes take place on a mat, making them accessible and suitable for individuals of all fitness levels.",
     "Core, flexibility and control on the mat"),
    ("pilates-reformer", "Pilates Reformer", "slider-pilates_reformer_v2.jpg",
     "A dynamic, full-body workout combining the principles of Pilates with the specialized Reformer. Build long, lean strength, flexibility, balance and core control with spring-loaded resistance and expert guidance.",
     "Spring-loaded, full-body Pilates"),
    ("sculpt", "Sculpt", "slider-sculpt_v2.jpg",
     "A dynamic, challenging session built to tone and define. Sculpt classes build lean muscle, increase strength and transform overall body composition — every rep with intention.",
     "Tone, define and build lean muscle"),
    ("stretch", "Stretch + Recovery", "slider-stretch_recovery_v1.jpg",
     "A rejuvenating, restorative class to increase flexibility, relieve muscle tension and promote overall recovery and well-being. A dedicated space to unwind, restore your body and feel better — the perfect complement to any workout.",
     "Mobility, release and deep recovery"),
    ("trx", "TRX&reg; Suspension", "slider-TRX_v4.jpg",
     "Leverage your own body weight as resistance on the TRX suspension system. Adjustable straps let you scale every move — building strength, stability and control from your first rep to your hardest.",
     "Suspension training that scales to you"),
    ("yoga", "Yoga + Mind Body", "slider-mind_body_v1.jpg",
     "Move, breathe, and reconnect. From gentle restorative flows to dynamic vinyasa, our yoga and mind-body classes build flexibility, strength and calm — guided by instructors who meet you exactly where you are.",
     "Flexibility, strength and stillness"),
]

# derived: the list used across nav/footer/group-fitness, each linking to its page
ALL_CLASSES = [(t, f"{slug}.html", short) for slug, t, img, lead, short in CLASS_PAGES]


def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="{LOGO}">
<link rel="stylesheet" href="assets/css/main.css?v={V}">
<script>(function(){{try{{
  if(sessionStorage.getItem("forma-intro"))document.documentElement.classList.add("no-preloader");
  var v=localStorage.getItem("forma-view");
  document.documentElement.setAttribute("data-view", v==="member"?"member":"guest");
  if(v)document.documentElement.classList.add("has-view");
}}catch(e){{}}}})();</script>
</head>
<body>
<div class="preloader" aria-hidden="true">
  <img class="preloader__logo" src="{LOGO}" alt="Forma Gym" width="422" height="37" />
  <div class="preloader__sub">Play Every Day</div>
  <div class="preloader__bar"><i></i></div>
  <div class="preloader__count">0</div>
</div>
"""


def header_html(active=""):
    links = ""
    for label, href in NAV:
        cls = ' class="is-active"' if href == active else ""
        links += f'<a href="{href}"{cls}>{label}</a>'
    menu_links = ""
    for i, (label, href) in enumerate(MENU, 1):
        menu_links += f'<a href="{href}">{label}</a>'
    return f"""
<header class="site-header">
  <div class="site-header__inner">
    <a class="brand" href="index.html" aria-label="Forma Gym — home">
      {brand_logo()}
    </a>
    <nav class="nav-desktop" aria-label="Primary">{links}</nav>
    <div class="header-cta">
      <div class="view-toggle" role="group" aria-label="View site as">
        <button type="button" data-view-set="guest">Guest</button>
        <button type="button" data-view-set="member">Member</button>
      </div>
      <a class="btn btn--sm only-guest header-pricing" href="contact.html#tour">Book a Tour</a>
      <a class="btn btn--solid btn--sm only-guest" href="join.html">Join Now</a>
      <a class="btn btn--solid btn--sm only-member" href="group-fitness.html#schedule">Class Schedule</a>
      <button class="menu-toggle" aria-expanded="false" aria-label="Open menu">
        <span class="menu-toggle__icon"><i></i><i></i><i></i></span>
      </button>
    </div>
  </div>
</header>

<div class="menu-overlay" role="dialog" aria-label="Site menu">
  <div class="menu-overlay__grid">
    <nav class="menu-list" aria-label="All pages">{menu_links}</nav>
    <aside class="menu-side">
      <div class="menu-side__controls">
        <div class="view-toggle" role="group" aria-label="View site as">
          <button type="button" data-view-set="guest">Guest</button>
          <button type="button" data-view-set="member">Member</button>
        </div>
        <a class="btn btn--sm only-guest" href="contact.html#tour">Book a Tour</a>
        <a class="btn btn--solid btn--sm only-member" href="group-fitness.html#schedule">Class Schedule</a>
      </div>
      <div class="menu-side__pass">
        <p>Two unique Bay Area clubs. Come Play Every Day.</p>
        <a class="btn btn--solid btn--sm" href="join.html">Join Now <span class="arr">→</span></a>
      </div>
      <div class="menu-side__group">
        <h6>Visit</h6>
        <a href="walnut-creek.html">Walnut Creek — 1908 Olympic Blvd</a>
        <a href="san-jose.html">San Jose — 5434 Thornwood Dr</a>
      </div>
      <div class="menu-side__group">
        <h6>Talk to us</h6>
        <a href="tel:9259326400">Walnut Creek · (925) 932-6400</a>
        <a href="tel:4083631010">San Jose · (408) 363-1010</a>
      </div>
    </aside>
  </div>
</div>

<main id="mainContent">
"""


def footer_html():
    cls_links = "".join(f'<a href="{href}">{label}</a>' for label, href, _ in ALL_CLASSES[:8])
    return f"""
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="site-footer__top">
      <div class="site-footer__brand">
        <a class="brand brand--footer" href="index.html">{brand_logo()}</a>
        <p>Two Bay Area clubs. A holistic, luxury approach to fitness — and a community that shows up to Play Every Day.</p>
      </div>
      <div>
        <div class="site-footer__links">
          <a href="group-fitness.html">Group Fitness</a>
          <a href="training.html">Personal Training</a>
          <a href="cycle.html">Cycle</a>
          <a href="yoga.html">Yoga + Mind Body</a>
          <a href="pilates-reformer.html">Pilates Reformer</a>
          <a href="trx.html">TRX&reg;</a>
          <a href="aqua.html">Aqua</a>
        </div>
      </div>
      <div>
        <div class="site-footer__links">
          <a href="recovery.html">Recovery &amp; Cryo</a>
          <a href="spa.html">The Spa</a>
          <a href="mindbodylab.html">Mind Body LAB</a>
          <a href="kidzville.html">Kidzville</a>
          <a href="outdoor-training.html">Outdoor Fitness</a>
          <a href="rise.html">RISE Program</a>
          <a href="merchant.html">Member Savings</a>
          <a href="about.html">About Forma</a>
        </div>
      </div>
      <div class="site-footer__contact">
        <h5>Two Locations</h5>
        <a class="tel" href="tel:9259326400">Walnut Creek</a>
        <a href="walnut-creek.html">1908 Olympic Blvd · (925) 932-6400</a>
        {socials("formawalnutcreek", "Walnut Creek")}
        <a class="tel" href="tel:4083631010">San Jose</a>
        <a href="san-jose.html">5434 Thornwood Dr · (408) 363-1010</a>
        {socials("formasanjose", "San Jose")}
      </div>
    </div>
  </div>
  <div class="wrap">
    <div class="site-footer__bottom">
      <span>©2026 Forma Gym. All Rights Reserved.</span>
      <div class="legal">
        <a href="contact.html">Contact</a>
        <a href="app.html">Forma App</a>
        <a href="privacy.html">Privacy Policy</a>
        <a href="accessibility.html">Accessibility</a>
      </div>
    </div>
  </div>
</footer>
<script src="assets/js/main.js?v={V}"></script>
<script src="assets/js/chat-config.js?v={V}"></script>
<script src="assets/js/chat.js?v={V}" defer></script>
</body>
</html>
"""


def hero(kicker, lines, sub="", img=None, video=None, poster=None, crumb=None,
         actions=None, meta=None, page=False, title_mod="", focal=None,
         walkthrough=False, tinted=False, media_mod=""):
    lns = ""
    for i, ln in enumerate(lines):
        lns += f'<span class="ln"><span style="transition-delay:{0.12 + i * 0.09:.2f}s">{ln}</span></span>'
    # Only the home hero runs the club walkthrough video (walkthrough=True); at
    # ~9.7 MB on mobile it is far too heavy to repeat on every page. Everywhere
    # else the page's own photo IS the background, as on formagym.com. `focal`
    # sets object-position so a 2:1 landscape still crops sensibly into a tall
    # phone hero. main.js picks the desktop or mobile video source by viewport.
    post = poster or img or ""
    fstyle = f' style="object-position:{focal}"' if focal else ""
    if video:
        media = f'<video src="{video}" poster="{post}" autoplay muted loop playsinline preload="auto"></video>'
    elif walkthrough:
        media = (f'<video poster="{post}" autoplay muted loop playsinline preload="none" '
                 f'data-src-desktop="{HERO_VIDEO_DESKTOP}" data-src-mobile="{HERO_VIDEO_MOBILE}"></video>')
    else:
        media = f'<img src="{post}" alt="" fetchpriority="high"{fstyle}>'
    acts = ""
    if actions:
        acts = '<div class="hero__actions">'
        for a in actions:
            label, href, solid = a[0], a[1], a[2]
            extra = (" " + a[3]) if len(a) > 3 else ""
            cls = ("btn btn--solid" if solid else "btn") + extra
            acts += f'<a class="{cls}" href="{href}">{label} <span class="arr">→</span></a>'
        acts += "</div>"
    # Breadcrumbs removed site-wide. The `crumb` arg is still accepted (many
    # call sites pass it) but no longer rendered.
    meta_html = ""
    if meta:
        meta_html = '<div class="hero__meta">' + "".join(f"<span>{m}</span>" for m in meta) + "</div>"
    sub_html = f'<p class="hero__sub">{sub}</p>' if sub else ""
    return f"""
<section class="hero{' hero--page' if page else ''}">
  <div class="hero__media{' hero__media--tinted' if tinted else ''}{f' {media_mod}' if media_mod else ''}">{media}</div>
  <div class="hero__inner">
    <p class="hero__kicker">{kicker}</p>
    <h1 class="hero__title{(' ' + title_mod) if title_mod else ''}">{lns}</h1>
    {sub_html}
    {acts}
  </div>
  {meta_html}
  <div class="hero__scroll" aria-hidden="true"></div>
</section>
"""


def photo_marquee(images):
    """Continuously scrolling strip of club photos — the visual counterpart to
    the text marquee. Decorative, so the images carry empty alt text."""
    seg = "".join(f'<span><img src="{IMG}/{im}" alt="" loading="lazy"></span>' for im in images)
    return f"""
<div class="marquee marquee--photo" aria-hidden="true">
  <div class="marquee__track">{seg}</div>
  <div class="marquee__track">{seg}</div>
</div>
"""


def marquee(words, accent=False, ghost=False):
    cls = "marquee" + (" marquee--accent" if accent else "") + (" marquee--ghost" if ghost else "")
    seg = "".join(f"<span>{w} <i>●</i></span>" for w in words)
    return f"""
<div class="{cls}" aria-hidden="true">
  <div class="marquee__track">{seg}</div>
  <div class="marquee__track">{seg}</div>
</div>
"""


def stats_band(items, light=False):
    cells = ""
    for num, sfx, label in items:
        cells += f"""
      <div class="stat">
        <div class="stat__num"><span data-count="{num}">0</span><span class="sfx">{sfx}</span></div>
        <div class="stat__label">{label}</div>
      </div>"""
    return f"""
<section class="section--flush{' section--panel' if light else ''}">
  <div class="stats"><div class="wrap" style="padding:0"><div class="stats__grid">{cells}</div></div></div>
</section>
"""


def split(eyebrow, num, title, paras, img, alt, rev=False, cta=None, light=False, wide=False, focal=None, ratio=None):
    body_paras = "".join(f'<p class="body-copy">{p}</p>' for p in paras)
    cta_html = f'<div class="split__cta"><a class="inline-link" href="{cta[1]}">{cta[0]} →</a></div>' if cta else ""
    return f"""
<section class="section{' section--panel' if light else ''}">
  <div class="wrap">
    <div class="split{' split--rev' if rev else ''}">
      <div class="split__media{' split__media--wide' if wide else ''} reveal-img"{f' style="aspect-ratio:{ratio}"' if ratio else ''}>
        <img src="{img}" alt="{alt}" loading="lazy"{f' style="object-position:{focal}"' if focal else ''}>
      </div>
      <div class="split__body">
        <p class="eyebrow">{f'' if num else ''}{eyebrow}</p>
        <h2 class="h-display" style="font-size:clamp(30px,3.8vw,58px)">{title}</h2>
        <div class="reveal">{body_paras}{cta_html}</div>
      </div>
    </div>
  </div>
</section>
"""


def cta_band(title_html, text, img, primary=("Join Now", "join.html"),
             secondary=("Book a Tour", "contact.html#tour")):
    sec = f'<a class="btn" href="{secondary[1]}">{secondary[0]} <span class="arr">→</span></a>' if secondary else ""
    return f"""
<section class="cta-band">
  <div class="cta-band__media"><img src="{img}" alt="" loading="lazy"></div>
  <div class="wrap">
    <h2 class="reveal">{title_html}</h2>
    <p class="reveal">{text}</p>
    <div class="hero__actions reveal">
      <a class="btn btn--solid" href="{primary[1]}">{primary[0]} <span class="arr">→</span></a>
      {sec}
    </div>
  </div>
</section>
"""


# ---------------------------------------------------------------- ACTIVECAMPAIGN
# The live site's lead capture runs through ActiveCampaign. These are the same
# form IDs the old formagym.com used, so existing lists, tags and automations
# keep working unchanged.
#   9   sitewide newsletter (footer, every page)
#   33  service / class page lead form
#   72  cryo lead (includes a phone field)
#   93  freeze / cancel request
#   103 join / membership (has conditional option groups)
# Form 49 (blog subscribe) is intentionally unused — the blog was retired.
AC_ACCOUNT = "https://formagym.activehosted.com"


def ac_form(form_id):
    """ActiveCampaign embed. The script renders the form where it sits."""
    return (f'<div class="ac-form ac-form--{form_id}">'
            f'<script src="{AC_ACCOUNT}/f/embed.php?id={form_id}" charset="utf-8"></script>'
            f"</div>")


def form_section(sec_id, num, eyebrow, title_html, text, btn, light=True, extra="", ac_id=None):
    fields = [("text", "first", "First name"), ("text", "last", "Last name"),
              ("email", "email", "Email address"), ("tel", "phone", "Phone")]
    f_html = ""
    for ftype, name, label in fields:
        f_html += f"""
        <div class="field"><input type="{ftype}" name="{name}" id="{sec_id}-{name}" placeholder=" " required><label for="{sec_id}-{name}">{label}</label></div>"""
    return f"""
<section class="section{' section--panel' if light else ''}" id="{sec_id}">
  <div class="wrap">
    <div class="intro-grid">
      <div>
        <p class="eyebrow">{eyebrow}</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">{title_html}</h2>
        <p class="lede reveal" style="margin-top:28px">{text}</p>
        {extra}
      </div>
      <div class="intro-grid__right reveal">
        {ac_form(ac_id) if ac_id else f'''<form class="form-grid" data-demo>
          {f_html}
          <div class="field field--full">
            <select name="location" id="{sec_id}-loc" aria-label="Preferred location">
              <option value="">&nbsp;</option>
              <option>Walnut Creek</option>
              <option>San Jose</option>
            </select>
            <label for="{sec_id}-loc">Preferred location</label>
          </div>
          <button class="btn {'btn--dark' if light else ''} field--full" type="submit" style="justify-content:center">{btn} <span class="arr">→</span></button>
        </form>'''}
        <p class="form-note">By submitting, you confirm you're at least 13 and agree to our Privacy Policy &amp; Terms. Forma is a SPAM-FREE ZONE — we never share or sell your info.</p>
      </div>
    </div>
  </div>
</section>
"""


WC_TRAINERS = [
    {
        "name": 'Dave', "role": 'Fitness Coach', "photo": 'coach_dave.jpg',
        "spec": ['Athletic Performance', 'Movement Assessment', 'Program Development', 'Weightlifting', 'Exercise Therapy + getting strong'],
        "story": 'When I was young I drove my parents crazy converting everything in the barn into exercise equipment. I would rather read anything about weightlifting and fitness than what I needed to for school. It became very evident that this was going to be more than an occupation, it was going to be a lifetime passion. I was fortunate to have some great mentors from the fitness world that gave me a respect for the history of strength, yet also challenged me to discover what is new and provoking. I spend my days sharing my passion with all kinds of wonderful people...my life is great!',
        "phil": 'Your happiness is your health. The world is best experienced with high energy, low pain, and high function. Physical activity is a source of great joy; find your motivation and stay active.',
    },
    {
        "name": 'Montana', "role": 'Fitness Coach', "photo": 'coach_montana.jpg',
        "spec": ['Weight Lifting', 'Strength Training', 'Athletic Performance', 'Functional Movement', 'Nutrition Coaching', 'Weight Loss Management'],
        "story": 'I grew up playing competitive sports my whole life, and developed a passion for health and fitness early on! I earned my B.S degree from The University of Hawaii in Nutrition/Sports &amp; Wellness, and am currently earning my masters in sports &amp; nutrition performance. I love helping people feel comfortable in their own skin, while helping to implement long lasting habits to achieve a healthy/balanced lifestyle. Main focus is for you to feel strong, confident, and excited about fitness! I’m passionate about helping people become the best version of themselves through finding the correct form of exercise and nutrition for each individual!',
        "phil": 'Consistency is more important than perfection.',
    },
    {
        "name": 'Jason', "role": 'Fitness Coach', "photo": 'coach_jason.jpg',
        "spec": ['Creative Movement', 'Interval Training', 'Kickboxing'],
        "story": 'Jason learned early, through his own experiences with weight loss and healing, about the potential for fitness to change lives. After losing 50 lbs. and reversing his hypertension, he made it his life goal to change the lives of others. His passion and infectious positive energy make him a great coach and motivator. He creates a safe and non-judgemental atmosphere for his clients, regardless of their fitness or experience level. Jason’s objective for his clients is to help them feel and understand the body in a new and deeper way.',
        "phil": 'Everything should feel good, from start to finish.',
    },
    {
        "name": 'Marco', "role": 'Fitness Coach', "photo": 'coach_marco.jpg',
        "spec": ['Cross Training', 'Bodybuilding', 'Muscle Definition + Development', 'Fat Loss', 'Strength Training', 'Bilingual (Spanish)'],
        "story": 'My passion for exercise began at an early age when I was in junior high school. I was very fortunate to have support in the process. Each year, I had mentors in nutrition and training which led me to improve more and more and by the second year of training, I was able to accomplish competing in various bodybuilding competitions. This sport completely changed me, giving me confidence and a strong mindset and now it is my life.',
        "phil": 'Exercise is a way to connect with the body, mind, and spirit. It provides an equilibrium in your life maintaining focus, motivation, strength, and happiness.',
    },
    {
        "name": 'Luis', "role": 'Fitness Coach', "photo": 'coach_luis.jpg',
        "spec": ['Strength', 'Kickboxing', 'Fllexibility', 'Body Sculpting', 'Functional Skill Activation'],
        "story": 'My passion for fitness started in college, where I played soccer and started learning Karate. While working on my degree in Economics, I opened up a Karate studio and trained students that achieved ranking championships. I became a Sport Massage Therapist and Fitness Trainer in 1996, then worked as a trainer for several years, and eventually opened up a fitness studio. I later moved to California to be closer to my family and became a Les Mills and Zumba instructor in 2011 and have been working as an instructor since then.',
        "phil": 'Master your training. Feel your change. End with a smile. Learning is endless.',
    },
    {
        "name": 'Kevin A.', "role": 'Fitness Coach', "photo": 'coach_kevina.jpg',
        "spec": ['Athletic Training', 'Post-Rehab Strength Training', 'Small Groups', 'Fat Loss'],
        "story": "I grew up in a small town on an Island in the Pacific Northwest. Naturally, I have always been drawn to outdoor activities and sports. Since I was a child, I participated in all sports ranging from snowboarding to baseball. I am currently certified as a Personal Trainer and a Performance Enhancement Specialist by the highly respected National Academy of Sports Medicine. In 2010, I received a Bachelor of Science degree in Exercise Physiology from San Franscico State. I believe the key to my success as a strength coach has been the ability to understand each person’s individual goal and challenges, whether they are a CEO, stay at home parent or an athlete. Knowing what motivates and inspires my client's specific goals, allows for a successful design program with a variety of exercises specifically designed to keep them engaged and on the path to success.",
        "phil": 'I believe that health and exercise should never feel like a chore, but rather something that you should look forward to in order to keep your mind and body as healthy as possible for yourself and loved ones, while enjoying everything life has to offer.',
    },
    {
        "name": 'Tracy', "role": 'Fitness Coach', "photo": 'coach_tracy.jpg',
        "spec": ['Nutrition Education', 'Strength Training', 'Posture Correction', 'Total-Body Conditioning', 'Functional Training', 'Physique Contest Preparation'],
        "story": 'I trained for and won my first bodybuilding show in 1987, and went on to represent Team Canada at the IFBB Hawaii International Invitational contest. Twenty years later, I was on Team USA and turned IFBB Pro, which was a dream come true for me. I have been an athlete all of my life, but strength training has made such a difference in my life and physique.',
        "phil": 'I found nutrition to be the missing link for success in achieving your fitness goals, so I became certified in nutrition. No matter what level you’re training at or what goal you’re reaching for, I believe in four things: nutrition, strength training, cardio and hormonal balance. I believe in incorporating fun, innovative and effective training techniques that fit into my client’s daily lives.',
    },
    {
        "name": 'Kevin', "role": 'Fitness Coach', "photo": 'coach_kevin.jpg',
        "spec": ['Body Weight Strength Training', 'Full Body Mobility', 'Functional Movement', 'Gymnastics Skill + Technique Development'],
        "story": 'Combining a unique approach to gymnastics and strength training, Kevin focuses on foundational techniques for strength and mobility. He accommodates different fitness levels and includes mobility techniques to enhance joint and muscle flexibility for effective strength training.',
        "phil": '',
    },
    {
        "name": 'Darlene', "role": 'Fitness Coach', "photo": 'coach_darlene.jpg',
        "spec": ['Strength Training', 'Weight Loss', 'Bodybuilding', 'Competition Prep', 'Total Body Transformations'],
        "story": 'I began my fitness career as a Health Coach specializing in weight loss and soon discovered a passion for powerlifting. To date, I have competed in 8 bodybuilding competitions and continue to compete in strength competitions. I love empowering people, and am equally passionate at working with beginners and coaching bodybuilding competitors. I work with beginners on foundational movement patterns, building confidence and getting rid of the intimidation they may feel as they get comfortable in the weight room. Some of my clients came to me being new to exercise and are now being coached to compete in Bikini and Figure Division bodybuilding competitions!',
        "phil": 'Lift for power. Lift for health. Lift for YOU!',
    },
    {
        "name": 'Sergio', "role": 'Fitness Coach', "photo": 'coach_sergio.jpg',
        "spec": ['Program Development', 'Strength + Metabolic Conditioning', 'Injury Prevention/Recovery', 'Biomechanics', 'Fitness + Behavior Expert', 'Nutrition Specialist'],
        "story": "Like most coaches, I have paved my own path to be the best coach I can be. With 21 years of experience in psychology and exercise science, my ability to understand people on a deeper level helps clients create successful health and fitness paths. I can compose some of the best fitness programs you have never experienced, provide you with the best workouts that will have you feeling amazing, and get you strong like never before, and even help with weight management. But, what I'm truly passionate about is providing life changing experiences that will transform you into the best version of yourself!",
        "phil": 'I believe in simple fitness and nutrition strategies, and providing clients with the right tools for success. The goal is to always optimize health and wellness.',
    },
    {
        "name": 'Annabell', "role": 'Fitness Coach', "photo": 'coach_annabell.jpg',
        "spec": ['Individualized Program Development', 'Strength Training', 'Functional Movement', 'Weight Loss Management', 'Nutrition Coaching', 'HIIT'],
        "story": "As a passionate fitness professional, I'm committed to helping people transform their lives through fitness. Whether you're looking to lose weight, build strength, or simply adopt a healthier lifestyle, I'm here to support you every step of the way. By working with me, you'll get personalized guidance and a tailored approach that's designed to meet your unique needs and goals. Train with me to transform your lifestyle and discover the joy and fulfillment that comes with taking care of your body and mind. Together, we'll create a plan that fits your schedule and preferences, and I'lI be there to motivate you, celebrate your progress, and help you overcome any obstacles that come your way. Let's work together to make your fitness journey a success!",
        "phil": 'The body achieves what the mind believes',
    },
    {
        "name": 'Rachel', "role": 'Fitness Coach', "photo": 'coach_rachel.jpg',
        "spec": ['Weight Lifting', 'Strength Training', 'Functional Movement', 'Athletic Performance', 'Injury Prevention', 'Post-Surgery Recovery', 'Neurosensory Specialist'],
        "story": 'I grew up a top 5 ranked junior tennis player in Montreal, Canada. Tennis was my life from the age of 3 all the way through college. I was offered a walk-on scholarship for tennis my freshman year, but turned it down due to a torn ACL. After rehabbing my ACL, I started an internship as an assistant athletic trainer in a sports performance facility. During that time, my mentor challenged me mentally &amp; physically. I was encouraged to further my career in athletic training, especially learning about the mind to body connection.',
        "phil": 'Live with a relentless pursuit of better!',
    },
    {
        "name": 'Armani', "role": 'Fitness Coach', "photo": 'coach_armani.jpg',
        "spec": ['Strength Training', 'Athletic Training', 'Youth Athletics', 'Power Lifting', 'HIIT Workouts', 'Conditioning'],
        "story": 'I believe that with proper training and consistency anything can be achieved. With an extensive background in sports and fitness, I decided to use my knowledge to help others. My goal is to help others feel comfortable and confident in the gym, from beginners to more experienced lifters. Whether I’m training a young athlete for a specific sport, or someone who wants to get stronger or change their physique. Every workout is tailored to the individual to help you achieve your goals.',
        "phil": 'With consistency and hard work anything is possible.',
    },
    {
        "name": 'Jacki', "role": 'Fitness Coach', "photo": 'coach_jacki.jpg',
        "spec": ['Injury Prevention', 'Rehabilitation', 'Bodybuilding', 'Strength &amp; Conditioning', 'Functional Training', 'Mobility &amp; Flexibility', 'Aquatic Fitness Training'],
        "story": 'After dealing with multiple injuries as a student-athlete, I shifted focus to athletic training, where I developed a deep understanding of recovery, injury prevention, and mental resilience. This experience allows me to approach fitness from both a physical and psychological perspective, offering personalized support for clients at all levels. I have over 13 years of training experience and specialize in crafting personalized, injury-conscious fitness plans that focus on strength, mobility, and overall functionality.',
        "phil": "Fitness is not just about the body—it's about healing, rebuilding, and becoming stronger in mind and spirit. True strength is found in overcoming the obstacles we face, both physical and mental.",
    },
]


SJ_TRAINERS = [
    {
        "name": 'Ana', "role": 'Fitness Coach', "photo": 'coach_sj_ana.jpg',
        "spec": ['Body Recomposition', 'HIIT Workouts', 'Weight Loss', 'Strength Training'],
        "story": 'My primary goal is to help and guide individuals on their unique fitness journeys. We all have our own paths, and I truly believe that through love, positive energy, and kindness, I can be a source of inspiration and a positive example for my clients. Additionally, as a bilingual trainer, I am able to build stronger connections and provide more personalized support to a diverse range of clients.',
        "phil": '',
    },
    {
        "name": 'Sean', "role": 'Fitness Coach', "photo": 'coach_sj_sean.jpg',
        "spec": ['Corrective Exercise', 'Squat Assessment', 'Mobility + Stability', 'Balance', 'Strength Training'],
        "story": "Since I've been involved with the fitness industry for over 30 years, I believe you must first be Healthy before you can be Fit. Health and fitness starts and stops with understanding what works best for the individual and their lifestyle. Not only have I learned invaluable training from working with a wide variety of clients I've also gained first hand experience from my own successes and failures.",
        "phil": '',
    },
    {
        "name": 'Jaden', "role": 'Fitness Coach', "photo": 'coach_sj_jaden.jpg',
        "spec": ['Body Recomposition', 'Muscle Building', 'Functional Strength Development'],
        "story": "I’ve been around fitness since I was young. Great mentors taught me that fitness is less about looks and more about values. What I’ve learned is that most people stay stuck, not from a lack of effort but from a lack of direction. I use a well balanced program to help you build muscle, lose fat, and become someone you’re proud of. I’d love to be part of your journey. Let's push past your limits, and get real results.",
        "phil": '',
    },
    {
        "name": 'Emir', "role": 'Fitness Coach', "photo": 'coach_sj_emir.jpg',
        "spec": ['Muscle Building', 'Nutritional Guidance', 'Strength Training', 'Body Recomposition', 'Weight Loss', 'Functional Fitness'],
        "story": 'To me, fitness isn’t just about the physical transformation—it’s about reclaiming your mindset, your self-worth, and your belief in what’s possible. My mission is to empower people with the tools, support, and accountability they need to feel strong—inside and out. You don’t have to walk the journey alone. I’m here to guide you every step of the way.',
        "phil": '',
    },
    {
        "name": 'Erin', "role": 'Fitness Coach', "photo": 'coach_sj_erin.jpg',
        "spec": ['Strength Training', 'Functional Movement', 'Nutrition Coaching', 'Habit Formation'],
        "story": 'As a former athlete and now mother to teen athletes, I am passionate about growing your strength and skill as well as optimizing for good quality fuel. I have lived with and adjusted to the ever-changing complexities of aging and prioritizing health and fitness while balancing job and family. My hope is to work with your goals and limitations, to empower growth in wellness, to simplify the fitness process and to foster habits that will most effectively and efficiently grow sustainable lifestyle results.',
        "phil": '',
    },
    {
        "name": 'Arvi', "role": 'Fitness Coach', "photo": 'coach_sj_arvi.jpg',
        "spec": ['Strength &amp; Conditioning', 'Body Recomposition', 'Metabolic Conditioning', 'Kettlebell Training', 'Olympic Lifts', 'Injury Prevention/Rehab'],
        "story": 'I got into training because I used to play varsity basketball. I wanted to learn how to improve my performance. After years of playing ball, I injured both my knees and was in pain. I met my coach/ mentor. Through his guidance, I was able to regain strength, mobility, and most important of all, I was finally pain free to play the game that I love again. I am here at Forma to help our members startfeeling good again.',
        "phil": '',
    },
    {
        "name": 'Bernadette', "role": 'Fitness Coach', "photo": 'coach_sj_bernadette.jpg',
        "spec": ['Bodybuilding', 'Busy Moms', 'Seniors', 'Mobility', 'Flexibility'],
        "story": 'I entered the fitness industry in the 1980s with an interest in helping people stay fit and am still here now with much more energy and drive. I have had 34 years of experience in the fitness industry teaching group fitness. As an effective personal trainer, I have created workouts that are safe and individualized to the clients needs, and executed with proper form. I have always tried to emphasized a healthy, happy lifestyle and that the key to success is consistency. I encourage clients to have a positive attitude and passion toward their goal. Its rewarding for me to see them embrace this new lifestyle.',
        "phil": 'I want to spread the passion and love for personal fitness, health and happiness. I truly love what I do!',
    },
    {
        "name": 'Nora', "role": 'Fitness Coach', "photo": 'coach_sj_nora.jpg',
        "spec": ['Body Recomposition', 'Strength + Conditioning', 'Athletic Training', 'Nutrition Coaching', 'Mental Coaching', 'Preventative/Corrective Exercise', 'Holistic Wellness'],
        "story": 'My passion for training started blooming in college when I became quickly obsessed with strength and conditioning. With discipline, it became part of my lifestyle and, as time went on, I noticed how much it improved my overall well-being. I was excited to keep challenging myself in new ways, which kept me motivated to accomplish more every time. During the pandemic, I was gutted that everything shut down. I felt helpless. After wiping my tears, I chose to keep moving forward. The endless time I spent indoors was an opportunity for me to brainstorm what I wanted out of life. One day it just hit me...if I love training that much, why not help others do the same? And so I decided to become a certified personal trainer and it was one of the best decisions I ever made.',
        "phil": '',
    },
    {
        "name": 'Chelsea', "role": 'Fitness Coach', "photo": 'coach_sj_chelsea.jpg',
        "spec": ['Functional Strength &amp; Cardio Conditioning', 'Nutrition Coaching', 'Weight Loss', 'Nutrition Coaching', 'Mobility &amp; Flexibility', 'Body Recomposition', 'NASM Weight Loss Specialist'],
        "story": "From a young age, I knew I wanted a career helping others recover and grow stronger. My life took a dramatic turn in 2017 when I discovered strength training during a particularly dark time in my life where I was battling depression and was extremely underweight. As I witnessed my physical and mental transformation through consistent training, a newfound passion ignited – sharing this empowering knowledge with others. As a coach, work doesn't feel like work; it's a calling that has allowed me to connect with others while helping them grow physically and mentally stronger. My approach is straightforward: a balanced program combines resistance training, cardiovascular conditioning, proper nutrition, and recovery strategies. This holistic formula fosters long-term health and well-being. As a trainer, I aim to practice what I preach. I craft workouts that are both fun and challenging. I add in elements of play while pushing boundaries. By keeping things engaging and demanding, my clients build mental toughness alongside physical strength.",
        "phil": '',
    },
    {
        "name": 'Steve', "role": 'Fitness Coach', "photo": 'coach_sj_steve.jpg',
        "spec": ['Bodybuilding', 'Fat Loss', 'Nutrition'],
        "story": 'With a background in MMA and wrestling, Steve developed a deep passion for discipline, strength, and high-performance training early in life. After competing in Division I athletics, he transitioned from competitive sports into coaching, with the goal of helping others improve their health, confidence, and overall performance. Steve is a certified personal trainer and certified nutritionist who specializes in helping clients lose weight, lower body fat, build lean muscle, and improve endurance. His training philosophy combines athletic conditioning, strength training, and practical nutrition strategies designed for real-world results. Drawing from his competitive athletic experience, Steve designs programs that focus on functional strength, mobility, metabolic conditioning, and sustainable nutrition habits. Whether someone is beginning their fitness journey or looking to break through a plateau, his coaching emphasizes accountability, discipline, and long-term lifestyle change.',
        "phil": 'I believe fitness is not just about appearance – it’s about building resilience, confidence, and a strong version of yourself both physically and mentally. I am a NASM Certified Personal Trainer (CPT) and Certified Nutritionist.',
    },
    {
        "name": 'Nicole', "role": 'Fitness Coach', "photo": 'coach_sj_nicole.jpg',
        "spec": ['Body Recomposition', 'Strength + Conditioning', 'Weightlifting', 'Weight Loss', 'Nutritional Guidance'],
        "story": 'My mission is to empower clients to transform both physically and mentally, guiding them toward a life that’s healthier, happier, and more fulfilling. I focus on sustainable habits, mindset shifts, and personalized strategies to support lasting change. And as I continue learning and growing in the areas of fitness, nutrition, and overall well-being, I’m committed to giving every client the absolute best of what I’ve learned.',
        "phil": 'I believe everyone deserves to feel strong, confident, and capable.',
    },
    {
        "name": 'Martin', "role": 'Fitness Coach', "photo": 'coach_sj_martin.jpg',
        "spec": ['Weight Management', 'Body Recomposition', 'Nutrition'],
        "story": 'My passion for fitness started at a young age through soccer and endurance training. Over time, that passion grew into strength training and learning the science behind proper workouts and nutrition. Before becoming a certified personal trainer, I helped coach three of my family members on their fitness journeys, and together they lost over 150 pounds. Seeing how much their lives changed motivated me to pursue my certifications and turn my passion into a career. Today, my goal is to help others build sustainable habits, live an active lifestyle, and reach their fitness goals.',
        "phil": '',
    },
    {
        "name": 'Jackie', "role": 'Fitness Coach', "photo": 'coach_sj_jackie.jpg',
        "spec": ['Weight Loss', 'Endurance', 'Multi-Sport Training', 'Athletic Performance', 'Mobility + Balance', 'Senior Wellness'],
        "story": 'Physical fitness and mental discipline have shaped my life since childhood, helping me manage ADHD and a thyroid condition. Regular exercise, sports, and nutrition improved my focus and body image. As a competitive athlete in softball and swimming, I strengthened my skills through rigorous training. My journey continued as a group exercise instructor, teaching various fitness classes. Inspired by triathlons, I competed for decades, achieving Bronze level All World Athlete status in Ironman 70.3, qualifying for seven national championships, and finishing fifth in my age group in my first full Ironman. Now, I aim to share these benefits with others as a dedicated personal trainer.',
        "phil": '',
    },
]

def trainer_accordion(trainers):
    """Coach photo beside their bio. The photos are WordPress 500x500 crops,
    already centred on the coach, so no per-photo focal point is needed."""
    items = []
    for t in trainers:
        head = (f'<span class="acc__name">{t["name"]}</span>'
                f'<span class="acc__role">{t["role"]}</span>')
        specs = "".join(f"<li>{s}</li>" for s in t["spec"])
        body = (f'<p class="trainer-bio__label"><strong>Specialties</strong></p>'
                f'<ul class="trainer-bio__specs">{specs}</ul>'
                f'<p>{t["story"]}</p>')
        if t["phil"]:
            body += f'<p class="trainer-bio__quote">“{t["phil"]}”</p>'
        items.append((head,
                      f'<div class="trainer-bio">'
                      f'<img class="trainer-bio__photo" src="{IMG}/{t["photo"]}" '
                      f'alt="{t["name"]}, {t["role"].lower()} at Forma Gym Walnut Creek" '
                      f'loading="lazy" width="320" height="320">'
                      f'<div class="trainer-bio__text">{body}</div>'
                      f'</div>'))
    return accordion(items, open_first=False)


def accordion(items, open_first=True):
    out = '<div class="acc reveal">'
    for i, (q, a) in enumerate(items):
        out += f"""
      <div class="acc__item{' is-open' if (open_first and i == 0) else ''}">
        <button class="acc__head" aria-expanded="{'true' if (open_first and i == 0) else 'false'}">
          <h3>{q}</h3><span class="acc__icon"></span>
        </button>
        <div class="acc__body" {'style="max-height:600px"' if (open_first and i == 0) else ''}><div class="acc__body-inner">{a}</div></div>
      </div>"""
    out += "</div>"
    return out


# ============================================================ LIVE URL STRUCTURE
# Option A: the built site emits the SAME paths formagym.com already uses, so
# existing Google results, inbound links and ad landing pages keep working.
# Internal name (flat .html)  ->  live path (directory-style, no extension)
URL_MAP = {
    "index.html": "",
    "about.html": "about",
    "group-fitness.html": "group-fitness",
    "training.html": "training",
    "recovery.html": "recovery",
    "cryo.html": "cryo",
    "spa.html": "locations/walnut-creek/spa",
    "mindbodylab.html": "mindbodylab",
    "kidzville.html": "kidzville",
    "rise.html": "rise",
    "givesback.html": "givesback",
    "walnut-creek.html": "locations/walnut-creek",
    "san-jose.html": "locations/san-jose",
    "locations.html": "locations",
    "join.html": "join-now",
    "trial-pass.html": "trial-pass",
    "outdoor-training.html": "outdoor-training",
    "drbrainrx.html": "drbrainrx",
    "app.html": "app",
    "merchant.html": "merchant",
    "contact.html": "contact",
    "accessibility.html": "accessibility-statement",
    "privacy.html": "privacy-policy",
    "freeze-cancel.html": "freeze-cancel",
    # class pages — live site uses the -gfit suffix
    "aqua.html": "aqua-gfit",
    "barre.html": "barre-gfit",
    "cycle.html": "cycle-gfit",
    "dance.html": "dance-gfit",
    "kickboxing.html": "kbox-gfit",
    "low-impact.html": "low-gfit",
    "mat-pilates.html": "mat-gfit",
    "meditation.html": "meditation-gfit",
    "pilates-reformer.html": "pilates-gfit",
    "sculpt.html": "sculpy-gfit",
    "stretch.html": "stretch-gfit",
    "trx.html": "trx-gfit",
    "cardio-hiit.html": "cardio-hiit",
    "yoga.html": "yoga-gfit",
}

# Same content served at more than one live path (the two club spa pages).
ALIAS_PATHS = {
    "spa.html": ["locations/san-jose/spa"],
}


def url_for(filename):
    """Flat internal filename -> live site URL."""
    if filename in URL_MAP:
        p = URL_MAP[filename]
        return f"{SITE_BASE}/" if p == "" else f"{SITE_BASE}/{p}/"
    return f"{SITE_BASE}/{filename}"


# ============================================================ RESPONSIVE IMAGES
# Variants are produced by tools/gen_responsive.py and committed, because that
# script needs macOS `sips` and CI runs on Linux. Everything here only reads
# what is on disk: no variants found means no srcset, and the plain src still
# serves the full-size file. So a build without them is degraded, never broken.
_VARIANT_DIR = os.path.join(OUT, "assets", "img", "r")

# How wide each image actually renders, per context. Getting these right is the
# whole point — a wrong `sizes` makes the browser pick the wrong file.
SIZES_BY_CONTEXT = {
    "hero__media":      "100vw",
    "cta-band__media":  "100vw",
    "vc-panel":         "100vw",
    "choice__img":      "100vw",
    # two-up on a phone, three-up above that
    "card__media":      "(max-width: 820px) 50vw, 33vw",
    # stacks full-width on a phone, half the row on desktop
    "split__media":     "(max-width: 900px) 100vw, 50vw",
    "loc-item__media":  "(max-width: 900px) 100vw, 50vw",
    "g-item":           "(max-width: 900px) 100vw, 33vw",
    # the strip is a fixed-height scroller
    "marquee__track":   "320px",
    "trainer-bio":      "150px",
}


def _variants(filename):
    """[(width, filename), …] for whatever this image has on disk, ascending."""
    stem, ext = os.path.splitext(filename)
    out = []
    for w in (400, 700, 1000, 1400):
        cand = f"{stem}-{w}{ext}"
        if os.path.exists(os.path.join(_VARIANT_DIR, cand)):
            out.append((w, cand))
    return out


def _srcset_for(filename):
    """srcset value, or "" when this image has no variants."""
    v = _variants(filename)
    if not v:
        return ""
    parts = [f"{SITE_BASE}/assets/img/r/{fn} {w}w" for w, fn in v]
    # the untouched original is the top of the set
    src_w = _natural_width(filename)
    if src_w:
        parts.append(f"{SITE_BASE}/assets/img/{filename} {src_w}w")
    return ", ".join(parts)


_WIDTH_CACHE = {}


def _natural_width(filename):
    """Pixel width of the full-size image, read once per build."""
    if filename in _WIDTH_CACHE:
        return _WIDTH_CACHE[filename]
    path = os.path.join(OUT, "assets", "img", filename)
    w = None
    try:
        with open(path, "rb") as fh:
            head = fh.read(32)
        if head[:2] == b"\xff\xd8":                      # JPEG
            w = _jpeg_width(path)
        elif head[:8] == b"\x89PNG\r\n\x1a\n":           # PNG
            w = int.from_bytes(head[16:20], "big")
    except OSError:
        w = None
    _WIDTH_CACHE[filename] = w
    return w


def _jpeg_width(path):
    """Walk the JPEG segments to the frame header — avoids a Pillow dependency."""
    with open(path, "rb") as fh:
        fh.read(2)
        while True:
            b = fh.read(1)
            if not b:
                return None
            if b != b"\xff":
                continue
            marker = fh.read(1)
            while marker == b"\xff":
                marker = fh.read(1)
            if marker in (b"\xd8", b"\xd9") or b"\xd0" <= marker <= b"\xd7":
                continue
            length = int.from_bytes(fh.read(2), "big")
            if 0xC0 <= marker[0] <= 0xCF and marker not in (b"\xc4", b"\xc8", b"\xcc"):
                fh.read(3)
                return int.from_bytes(fh.read(2), "big")
            fh.read(length - 2)


def add_srcset(html):
    """Give every <img> a srcset + a `sizes` matched to how it actually renders.

    Walks the document once tracking the most recent container class, rather
    than peeking at a fixed window behind each tag — the photo strip holds a
    dozen <img> in a row, so a window never reaches back to its wrapper. The
    context resets at each </section> so a component cannot leak into the next.
    """
    token = _re.compile(r'class="(?P<cls>[^"]*)"|(?P<close></section>)'
                        r'|(?P<img><img[^>]+src="[^"]*assets/img/(?P<file>[A-Za-z0-9._@%-]+)"[^>]*>)')
    out, pos, context = [], 0, None
    for m in token.finditer(html):
        out.append(html[pos:m.start()])
        pos = m.end()
        if m.group("close"):
            context = None
            out.append(m.group(0))
        elif m.group("cls") is not None:
            hit = next((v for k, v in SIZES_BY_CONTEXT.items() if k in m.group("cls")), None)
            if hit:
                context = hit
            out.append(m.group(0))
        else:
            tag, filename = m.group("img"), m.group("file")
            srcset = "" if ("srcset=" in tag or filename.endswith(".svg")) else _srcset_for(filename)
            out.append(tag if not srcset
                       else tag[:-1] + f' srcset="{srcset}" sizes="{context or "100vw"}">')
    out.append(html[pos:])
    return "".join(out)


def rewrite_urls(html):
    """Make every asset + internal link absolute-from-root and extensionless.
    Required because pages now live in subdirectories, so relative paths break.
    SITE_BASE prefixes them when the site is not served from a domain root —
    GitHub Pages serves this project under /forma-gym-redesign/."""
    # srcset first, while the src paths are still relative and easy to match.
    # It emits SITE_BASE-prefixed URLs itself, so the rewrites below skip it.
    html = add_srcset(html)
    html = _re.sub(r'(href|src)="assets/', rf'\1="{SITE_BASE}/assets/', html)
    # data-src-* and poster carry asset paths too, and are not href/src.
    html = _re.sub(r'(data-src-desktop|data-src-mobile|poster)="assets/',
                   rf'\1="{SITE_BASE}/assets/', html)

    def _link(m):
        attr, fn, frag = m.group(1), m.group(2), m.group(3) or ""
        return f'{attr}="{url_for(fn)}{frag}"'

    return _re.sub(r'(href)="((?:blog/)?[A-Za-z0-9._-]+\.html)(#[^"]*)?"', _link, html)


def _write(path_rel, html):
    """path_rel '' -> docs/index.html ; 'about' -> docs/about/index.html"""
    out_dir = OUT if path_rel == "" else os.path.join(OUT, path_rel)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w") as f:
        f.write(html)


def page(filename, title, desc, active, body):
    html = rewrite_urls(head(title, desc) + header_html(active) + body + footer_html())
    targets = [URL_MAP.get(filename, filename.replace(".html", ""))]
    targets += ALIAS_PATHS.get(filename, [])
    for t in targets:
        _write(t, html)
    print("built", "/" + (targets[0] + "/" if targets[0] else ""))


# ============================================================ shared blocks
view_chooser = f"""
<div class="view-chooser" role="dialog" aria-label="Choose your experience">
  <div class="view-chooser__bar">
    <span class="vc-bar__spacer" aria-hidden="true"></span>
    <span class="brand brand--chooser">{brand_logo()}</span>
    <button class="menu-toggle vc-skip" type="button" aria-label="Skip and browse the site">
      <span class="menu-toggle__icon"><i></i><i></i><i></i></span>
    </button>
  </div>
  <div class="view-chooser__panels">
    <button class="vc-panel" type="button" data-choose="guest">
      <img src="{IMG}/guest_kettle.jpg" alt="">
      <div class="vc-panel__body">
        <span class="vc-panel__kicker">Welcome to Forma Gym</span>
        <h3>I'm a <span class="serif">guest</span></h3>
        <p>Tour a club and explore classes.</p>
        <span class="go">Show me around →</span>
      </div>
    </button>
    <button class="vc-panel" type="button" data-choose="member">
      <img src="{IMG}/SJ_pool_birdseye.jpg" alt="">
      <div class="vc-panel__body">
        <span class="vc-panel__kicker">Welcome back Forma family</span>
        <h3>I'm a <span class="serif">member</span></h3>
        <p>Class schedules, club hours, Kidzville and your member perks.</p>
        <span class="go">Take me in →</span>
      </div>
    </button>
  </div>
  <div class="view-chooser__foot">
    <span>I&rsquo;m ready to join now &mdash; let&rsquo;s go!</span>
    <a class="btn btn--solid btn--sm vc-join" href="join.html">Sign me up</a>
  </div>
</div>
"""

# ============================================================ HOME
home_body = view_chooser + hero(
    "Walnut Creek &amp; San Jose · Est. 2009",
    ["Play", '<span class="serif">every</span> day'],
    "Two unique Bay Area clubs built around one idea: making movement a part of your day - "
    "every day. Featuring world-class trainers &amp; instructors, resort-style amenities &amp; an "
    "authentic community atmosphere, Forma offers a dynamic, holistic approach to fitness.",
    poster=f"{IMG}/forma-hero-poster.jpg",
    walkthrough=True,
    actions=[
        ("Visit Us", "join.html", True, "only-guest"),
        ("Explore the Clubs", "locations.html", False, "only-guest"),
        ("Class Schedule", "group-fitness.html#schedule", True, "only-member"),
        ("Book Recovery", "recovery.html", False, "only-member"),
    ],
    meta=["2 Bay Area locations", "75,000+ sq ft of fitness", "All classes included"],
) + photo_marquee(STRIP_PHOTOS) + f"""
<section class="section">
  <div class="wrap">
    <div class="intro-grid">
      <div>
        <p class="eyebrow">Our mission</p>
        <h2 class="h-display reveal">Making exercise a part of your daily life. <span class="serif">For the rest of your life.</span></h2>
      </div>
      <div class="intro-grid__right">
        <p class="lede reveal">Our goal at Forma has always been to create a community where fitness and health is available to EVERYONE on the spectrum of movement - from those individuals that are struggling just to stand, to world-class athletes. We are very proud of what we’ve created and we love our Members, our Team, our Community and we LOVE being here for you!</p>
        <div class="reveal"><a class="inline-link" href="about.html">The Forma story →</a></div>
      </div>
    </div>
  </div>
</section>
""" + stats_band([
    (2, "", "Unique Bay Area clubs"),
    (75, "K+", "Sq. ft. of indoor/outdoor fitness"),
    (14, "", "All-inclusive group fitness formats"),
    (time.localtime().tm_year - FOUNDED, "", "Years in the Bay Area"),
]) + f"""
<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">Find your movement</p>
        <h2 class="h-display reveal break-accent" style="font-size:clamp(34px,4.6vw,72px)">Play every day. <span class="serif">In every way.</span></h2>
      </div>
    </div>
    <div class="card-grid" data-stagger>
      <a class="card" href="group-fitness.html"><div class="card__media"><img src="{IMG}/group_fit_jess.jpg" alt="Group fitness class" loading="lazy"><div class="card__label"><h3>Group Fitness</h3><span class="go">Explore →</span></div></div></a>
      <a class="card" href="training.html"><div class="card__media"><img src="{IMG}/pt_liz.jpg" alt="Personal training" loading="lazy"><div class="card__label"><h3>Personal Training</h3><span class="go">Explore →</span></div></div></a>
      <a class="card" href="cycle.html"><div class="card__media"><img src="{IMG}/cycle_sj.jpg" alt="Cycle studio" loading="lazy"><div class="card__label"><h3>Cycle</h3><span class="go">Explore →</span></div></div></a>
      <a class="card" href="recovery.html"><div class="card__media"><img src="{IMG}/cryo_recovery.jpg" alt="Forma cryotherapy chamber" loading="lazy"><div class="card__label"><h3>Recovery &amp; Cryo</h3><span class="go">Explore →</span></div></div></a>
      <a class="card" href="aqua.html"><div class="card__media"><img src="{IMG}/pool_wc.jpg" alt="Aqua studio" loading="lazy"><div class="card__label"><h3>Aqua</h3><span class="go">Explore →</span></div></div></a>
      <a class="card" href="spa.html"><div class="card__media"><img src="{IMG}/spa_wc.jpg" alt="The spa" loading="lazy"><div class="card__label"><h3>The Spa</h3><span class="go">Explore →</span></div></div></a>
    </div>
  </div>
</section>
""" + split(
    "Our clubs", "03",
    'Walnut <span class="serif">Creek</span>',
    ["The birthplace of Forma since 2009. Right off the 680/24 corridor and completely renovated — 35,000 square feet of indoor and outdoor fitness motivation, a heated outdoor lap pool under towering redwoods, onsite Kidzville, cryotherapy, a full-service day spa and the Forma Café.",
     "Open Monday–Thursday 5am–11pm, Friday 5am–10pm, weekends 6am–8pm. 1908 Olympic Blvd, Walnut Creek."],
    f"{IMG}/wc_facade.jpg",
    "Forma Gym Walnut Creek facade",
    cta=("Explore Walnut Creek", "walnut-creek.html"),
    # The default portrait 4/4.6 crops the facades down to the sign. 4/3.4 is what
    # the phone already used, and the extra width is what shows the building.
    ratio="4/3.4",
) + split(
    "Our clubs", "04",
    'San <span class="serif">Jose</span>',
    ["Serving South San Jose since 2015. A 40,000 sq. ft. luxury facility with an 8,000 sq. ft. covered outdoor fitness area — cardio, strength, group fitness, a heated 6-lane junior olympic pool with hot tub, and full-service locker rooms with sauna, steam and a Chilly Goat® cold plunge.",
     "Open Monday–Thursday 5am–11pm, Friday 5am–10pm, weekends 6am–8pm. 5434 Thornwood Dr, San Jose."],
    f"{IMG}/sj_facade.jpg",
    "Forma Gym San Jose facade",
    rev=True, cta=("Explore San Jose", "san-jose.html"),
    ratio="4/3.4",
) + f"""
<section class="section section--panel">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">Recover like an athlete</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Wellness, <span class="serif">elevated</span></h2>
      </div>
    </div>
    <div class="card-grid card-grid--2" data-stagger>
      <div class="card card--stack"><div class="card__media card__media--wide"><img src="{IMG}/chillyGOAT_SJ_500px.jpg" alt="Chilly Goat cold plunge" loading="lazy"></div><div class="card__below"><h3 class="card__title">Cryo + Cold Plunge</h3><p>Burn 500–800 calories in a single 3-minute session, reduce inflammation and pain, heal injuries faster, and sleep better. A natural, non-invasive reset trusted by Olympic and pro athletes — and now part of your club.</p></div></div>
      <div class="card card--stack"><div class="card__media card__media--wide"><img src="{IMG}/Forma_Walnut-Creek_Spa_Header_2018.jpg" alt="The Spa" loading="lazy"></div><div class="card__below"><h3 class="card__title">The Spa at Forma</h3><p>Massage, facials, Reiki and clinical skin care from skilled therapists — steps from the sauna, steam and hot tub. Restore, rejuvenate and walk out feeling like a brand new person.</p></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">More than a gym</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Built for your whole <span class="serif">life</span></h2>
      </div>
    </div>
    <div class="rows reveal">
      <a class="row-item" href="kidzville.html"><span class="row-item__idx">01</span><span class="row-item__title">Kidzville</span><span class="row-item__desc">A guilt-free workout while your kids (6 weeks–12 years) play in a safe, active, educational space.</span><span class="row-item__arrow">→</span></a>
      <a class="row-item" href="mindbodylab.html"><span class="row-item__idx">02</span><span class="row-item__title">Mind Body LAB</span><span class="row-item__desc">Where science meets self-care — brain health, recovery tech and the mind-body connection.</span><span class="row-item__arrow">→</span></a>
      <a class="row-item" href="rise.html"><span class="row-item__idx">03</span><span class="row-item__title">RISE Program</span><span class="row-item__desc">Exercise-based therapy for individuals living with paralysis. Movement is medicine.</span><span class="row-item__arrow">→</span></a>
      <a class="row-item" href="givesback.html"><span class="row-item__idx">04</span><span class="row-item__title">Forma Gives Back</span><span class="row-item__desc">Fitness available to everyone on the spectrum of movement — and a community that shows up.</span><span class="row-item__arrow">→</span></a>
    </div>
  </div>
</section>
""" + cta_band(
    'Your <span class="serif">club</span> is waiting',
    "Tour a club, take a class, hit the spa. Come see why Forma members never want to leave.",
    f"{IMG}/slider-locations_turf_alysse_torey.jpg",
)

# ============================================================ ABOUT
about_body = hero(
    "About Forma Gym",
    ["More than a gym.", 'It\'s <span class="serif">Family</span>.'],
    "Our mission has driven everything we've built since 2009. It's simple – make exercise a part of "
    "our member's daily lives, for the rest of their lives. The goal at Forma has always been to create "
    "a community where fitness and health is available to EVERYONE on the spectrum of movement — from "
    "those struggling just to stand, to Olympic athletes.",
    img=f"{IMG}/slider-locations_turf_alysse_torey.jpg",
    crumb="About",
    actions=[("Book a Tour", "contact.html#tour", True)],
    page=True,
    title_mod="hero__title--fit",
) + f"""
<section class="section section--tight">
  <div class="wrap">
    <div class="intro-grid intro-grid--copy">
      <div>
        <p class="eyebrow">Our mission</p>
        <h2 class="h-display reveal">Play + move<br><span class="serif">every day</span></h2>
      </div>
      <div class="intro-grid__right">
        <p class="lede reveal">We're very proud of what we've created, and we love our Members, our Team, our Community — and we LOVE being here for you. That's not a slogan. It's how the clubs feel the moment you walk in.</p>
      </div>
    </div>
  </div>
</section>
""" + photo_marquee(STRIP_PHOTOS) + f"""
<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">Our core values</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">What we <span class="serif">live</span> by</h2>
      </div>
    </div>
    <div class="pillars" data-stagger>
      <div class="pillar"><span class="pillar__num">01</span><h3>Legendary service</h3><p>Deliver an unimaginable experience through legendary customer service.</p></div>
      <div class="pillar"><span class="pillar__num">02</span><h3>Life is good</h3><p>Be optimistic and energetic. Bring that energy every single day.</p></div>
      <div class="pillar"><span class="pillar__num">03</span><h3>Always growing</h3><p>Continuously pursue personal and professional growth and improvement.</p></div>
      <div class="pillar"><span class="pillar__num">04</span><h3>Open &amp; honest</h3><p>Build trust through open and honest communication.</p></div>
      <div class="pillar"><span class="pillar__num">05</span><h3>Stay open-minded</h3><p>Make your life an adventure, be creative, and stay completely open-minded.</p></div>
      <div class="pillar"><span class="pillar__num">06</span><h3>Play every day</h3><p>Embrace change. And above all — play every day.</p></div>
    </div>
  </div>
</section>
""" + split(
    "The community", "03",
    'Everyone on the spectrum of <span class="serif">movement</span>',
    ["From first-timers nervous to walk in, to parents reclaiming an hour, to athletes chasing a PR — Forma was built for all of it. Our instructors meet you where you are and help you go further than you thought you could.",
     "It's why people don't just join Forma. They belong to it."],
    f"{IMG}/slider-hero_ladies_v1.jpg",
    "Forma community members in class",
    cta=("Visit a club", "locations.html"),
    # 2000x954 in the default portrait box shows only the middle 41.5% — the three
    # figures span 54.5%, so the right-hand one was always cut. Wide box + a shift
    # right onto the group's true centre (60% of the frame, not 50%).
    wide=True, focal="78% 50%",
) + form_section(
    "tour", "04", "Book a tour",
    'Come see it for <span class="serif">yourself</span>',
    "Join the Forma Family and experience the best trainers, programs and classes in the Bay Area. Tell us a little about you and we'll set up your visit.",
    "Book My Tour", ac_id=33,
) + cta_band(
    'Come <span class="serif">play</span> with us',
    "Two clubs, one community that can't wait to meet you.",
    f"{IMG}/slider-locations_group_dance.jpg",
)

# ============================================================ GROUP FITNESS
class_rows = ""
for i, (label, href, desc) in enumerate(ALL_CLASSES, 1):
    class_rows += f'<a class="row-item" href="{href}"><span class="row-item__idx">{i:02d}</span><span class="row-item__title">{label}</span><span class="row-item__desc">{desc}</span><span class="row-item__arrow">→</span></a>'

groupfit_body = hero(
    "Group Fitness",
    ["Stronger", '<span class="serif">together</span>'],
    "Forma Gym is your destination for group fitness that takes your workout to the next level. A vibrant community, expertly crafted classes, and 14 formats that energize, motivate and challenge — for every level, beginner to advanced.",
    img=f"{IMG}/slider-locations_group_dance.jpg",
    crumb="Group Fitness",
    actions=[("Visit Us", "join.html", True), ("Book a Tour", "contact.html#tour", False)],
    meta=["14 class formats", "All included in membership", "Indoor + outdoor studios"],
    page=True,
) + photo_marquee(STRIP_PHOTOS[3:] + STRIP_PHOTOS[:3]) + f"""
<section class="section" id="classes">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">The full lineup</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Fourteen ways to <span class="serif">move</span></h2>
      </div>
      <p class="body-copy reveal" style="max-width:36ch">Whether you're kickstarting your journey or chasing your next level, there's a class with your name on it — included with every membership.</p>
    </div>
    <div class="rows reveal">{class_rows}</div>
  </div>
</section>

<section class="section section--flush">
  <div class="gallery wrap">
    <div class="g-item g-item--a reveal-img"><img src="{IMG}/slider-WC_cycle_indoor_v2.jpg" alt="Cycle class" loading="lazy"></div>
    <div class="g-item g-item--b reveal-img"><img src="{IMG}/slider-TRX_v4.jpg" alt="TRX class" loading="lazy"></div>
    <div class="g-item g-item--c reveal-img"><img src="{IMG}/slider-sculpt_v2.jpg" alt="Sculpt class" loading="lazy"></div>
  </div>
</section>
""" + split(
    "Where you'll sweat", "02",
    'Studios built for <span class="serif">energy</span>',
    ["Across both clubs you'll find dedicated studios — cycle, reformer Pilates, mind-body, and multi-purpose group fitness rooms — plus covered outdoor turf and heated pools for classes under the California sky.",
     "Walnut Creek features 4 studios plus a Pilates Reformer studio. San Jose brings indoor and outdoor classes across 40,000 square feet."],
    f"{IMG}/SJ_cycle_studio_2500px.jpg",
    "Cycle studio at Forma San Jose",
    rev=True, cta=("See the locations", "locations.html"),
) + form_section(
    "schedule", "03", "Schedule a visit",
    'Find your first <span class="serif">class</span>',
    "Join the Forma Family and experience the difference — featuring the best trainers, programs and classes in the Bay Area. Tell us your preferred club and we'll get you on the schedule.",
    "Get the Schedule", ac_id=33,
) + cta_band(
    'Come <span class="serif">move</span> with us',
    "Come try a class — or five. Every format is included with membership.",
    f"{IMG}/slider-kickbox_v3.jpg",
)

# ============================================================ TRAINING
training_body = hero(
    "Personal Training",
    ["The best", 'in the <span class="serif">Bay</span>.'],
    "A team of fitness professionals with diverse backgrounds, deep experience, and a shared passion for health and wellness. We'll meet you where you are and build the plan that gets you where you want to be.",
    img=f"{IMG}/training_hero.jpg",
    crumb="Training",
    actions=[("Book a Consult", "contact.html#tour", True), ("Meet the Team", "#team", False)],
    meta=["1-on-1 &amp; small group", "Nutrition guidance included", "Both clubs"],
    page=True,
) + f"""
<section class="section">
  <div class="wrap">
    <div class="split split--solo">
      <div class="split__body">
        <p class="eyebrow">One-on-one personal training</p>
        <h2 class="h-display" style="font-size:clamp(30px,3.8vw,58px)">A plan built around <span class="serif">you</span></h2>
        <ul class="checklist reveal" style="margin-top:10px">
          <li>Assess where you are now and where to start</li>
          <li>Nutritional consultation &amp; guidance — understand the power of food</li>
          <li>Education on movement technique and equipment — master your exercise</li>
          <li>The perfect strategy for your individual goals</li>
          <li>Accountability for your fitness journey</li>
          <li>Learn to repair and recover, and keep your work/life balance</li>
        </ul>
        <div class="split__cta"><a class="inline-link" href="contact.html#tour">Book a consult →</a></div>
      </div>
    </div>
  </div>
</section>
""" + split(
    "Small group training", "",
    'The best of both <span class="serif">worlds</span>',
    ["Small Group Training brings 4–8 people together with one trainer — the energy and accountability of community, with the attention and programming of personal training.",
     "It's affordable, it's motivating, and the workouts change constantly so you never plateau or get bored."],
    f"{IMG}/Darlene_ropes2.jpg",
    "Small group training at Forma",
    rev=True, cta=("Ask about small group", "contact.html#tour"),
) + f"""
<section class="section section--panel" id="team">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">Meet our training team</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Coaches who <span class="serif">care</span></h2>
      </div>
      <p class="body-copy reveal" style="max-width:34ch">Years of experience, a range of specialties, and a genuine passion for helping you feel strong, confident and excited about fitness.</p>
    </div>
    <h3 class="team-club">Walnut Creek</h3>
    {trainer_accordion(WC_TRAINERS)}
    <h3 class="team-club">San Jose</h3>
    {trainer_accordion(SJ_TRAINERS)}
  </div>
</section>
""" + cta_band(
    'Train with the <span class="serif">best</span> in the Bay',
    "Book a consultation, tell us your goal, and we'll pair you with the coach who's right for you.",
    f"{IMG}/Dave2.jpg",
)

# ============================================================ LOCATIONS
locations_body = hero(
    "Locations &amp; Hours",
    ["Two unique", 'Bay Area <span class="serif">clubs</span>.'],
    "Walnut Creek and San Jose — both premium, both all-inclusive. Find your home club below.",
    img=f"{IMG}/Forma_WalnutCreek_locations_pool_birdeye-2.jpg",
    crumb="Locations",
    actions=[("Visit Us", "join.html", True)],
    page=True,
) + f"""
<section class="section">
  <div class="wrap">
    <div class="loc">
      <div class="loc-item">
        <div class="loc-item__media reveal-img"><img src="{IMG}/wc_facade.jpg" alt="Forma Walnut Creek" loading="lazy"></div>
        <div>
          <span class="loc-badge">Since 2009 · 35,000 sq ft</span>
          <h3>Walnut Creek</h3>
          <a class="phone" href="tel:9259326400">(925) 932-6400</a>
          <div class="loc-hours">
            <div><dt>Mon–Thu</dt><dd>5am – 11pm</dd></div>
            <div><dt>Friday</dt><dd>5am – 10pm</dd></div>
            <div><dt>Sat–Sun</dt><dd>6am – 8pm</dd></div>
          </div>
          <address>1908 Olympic Blvd, Walnut Creek, CA 94596</address>
          <div class="hero__actions" style="opacity:1;transform:none;margin-top:26px">
            <a class="btn btn--sm" href="walnut-creek.html">Explore Walnut Creek <span class="arr">→</span></a>
          </div>
        </div>
      </div>
      <div class="loc-item">
        <div class="loc-item__media reveal-img"><img src="{IMG}/sj_facade.jpg" alt="Forma San Jose" loading="lazy"></div>
        <div>
          <span class="loc-badge">Since 2015 · 40,000 sq ft</span>
          <h3>San Jose</h3>
          <a class="phone" href="tel:4083631010">(408) 363-1010</a>
          <div class="loc-hours">
            <div><dt>Mon–Thu</dt><dd>5am – 11pm</dd></div>
            <div><dt>Friday</dt><dd>5am – 10pm</dd></div>
            <div><dt>Sat–Sun</dt><dd>6am – 8pm</dd></div>
          </div>
          <address>5434 Thornwood Dr, San Jose, CA 95123</address>
          <div class="hero__actions" style="opacity:1;transform:none;margin-top:26px">
            <a class="btn btn--sm" href="san-jose.html">Explore San Jose <span class="arr">→</span></a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
""" + stats_band([
    (2, "", "Premium Bay Area clubs"),
    (75, "K+", "Combined square feet"),
    (14, "", "Group fitness formats"),
    (time.localtime().tm_year - FOUNDED, "", "Years in the Bay Area"),
]) + cta_band(
    'Find your <span class="serif">home club</span>',
    "Both locations are all-inclusive: every class, the pool, the recovery suites - the works.",
    # was pool_sunset_SJ_500px.jpg — a 500px square stretched across a 100vw band
    f"{IMG}/sj_pool_sunset.jpg",
)


def location_page(name, badge, phone, tel, address, intro, amenities, hero_img, gallery_imgs, hours,
                  hero_focal="50% 50%", hero_media_mod=""):
    am = "".join(f"<li>{a}</li>" for a in amenities)
    g = ""
    cls = ["g-item--a", "g-item--b", "g-item--c"]
    for i, im in enumerate(gallery_imgs[:3]):
        g += f'<div class="g-item {cls[i]} reveal-img"><img src="{IMG}/{im}" alt="{name}" loading="lazy"></div>'
    hrs = "".join(f'<div><dt>{d}</dt><dd>{h}</dd></div>' for d, h in hours)
    return hero(
        f"Forma {name}", [f'{name.split()[0]} <span class="serif">{name.split()[-1] if len(name.split())>1 else "Club"}</span>'],
        intro, img=f"{IMG}/{hero_img}", crumb=f'<a href="locations.html">Locations</a> &nbsp;/&nbsp; {name}',
        actions=[("Visit Us", "join.html", True), (f"Call {phone}", f"tel:{tel}", False)],
        meta=[badge], page=True, focal=hero_focal, media_mod=hero_media_mod,
    ) + f"""
<section class="section section--tight">
  <div class="wrap">
    <div class="intro-grid">
      <div>
        <p class="eyebrow">What's inside</p>
        <h2 class="h-display reveal">Premium. <span class="serif">All-inclusive.</span></h2>
        <address style="font-style:normal;color:var(--muted);margin-top:22px;line-height:1.8;font-size:15.5px">{address}<br><a href="tel:{tel}" style="color:var(--accent)">{phone}</a></address>
        <div class="loc-hours loc-hours--inline" style="max-width:340px;margin-top:20px">{hrs}</div>
      </div>
      <div class="intro-grid__right reveal">
        <ul class="checklist">{am}</ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--flush">
  <div class="gallery wrap">{g}</div>
</section>
""" + cta_band(
        f'Come play in <span class="serif">{name.split()[-1]}</span>',
        "Book a tour or jump straight in. Every class and amenity, included.",
        f"{IMG}/{gallery_imgs[0]}",
    )


walnutcreek_body = location_page(
    "Walnut Creek", "Open Mon–Thu 5am–11pm", "(925) 932-6400", "9259326400",
    "1908 Olympic Blvd, Walnut Creek, CA 94596",
    "The birthplace of Forma since 2009. Completely renovated, right off the 680/24 corridor — 35,000 square feet of indoor and outdoor fitness motivation. Come experience why we're Walnut Creek's premier fitness club.",
    ["Indoor + covered outdoor, fully-equipped fitness playgrounds", "4 Studios + a dedicated Pilates Reformer Studio",
     "All group fitness: Zumba, Yoga, Barre, HIIT, Pilates, Dance &amp; Cycle", "Expert fitness &amp; nutrition coaches",
     "Heated, outdoor lap pool under the redwoods", "Onsite Kidzville childcare", "Cryotherapy + Cold Plunge by Chilly Goat®",
     "Full-service day spa", "Luxury amenities: sauna, eucalyptus steam room, hot tub", "Forma Café + Smoothie Bar"],
    "wc_facade.jpg",
    ["Forma_WalnutCreek_locations_pool_birdeye-2.jpg", "facade2_WC_500px.jpg", "WC_pool_class_662x501_v1.jpg"],
    [("Mon–Thu", "5am – 11pm"), ("Friday", "5am – 10pm"), ("Sat–Sun", "6am – 8pm")],
)

sanjose_body = location_page(
    "San Jose", "Open Mon–Thu 5am–11pm", "(408) 363-1010", "4083631010",
    "5434 Thornwood Dr, San Jose, CA 95123",
    "Serving the South San Jose community since 2015. A 40,000 sq. ft. luxury fitness facility with an 8,000 sq. ft. covered outdoor fitness area — complete with cardio, strength, group fitness, a heated 6-lane junior olympic pool with hot tub, and full-service locker rooms.",
    ["8,000 sq. ft. fully-equipped, covered outdoor playground", "Heated, outdoor 6-lane junior olympic pool &amp; hot tub",
     "Indoor &amp; outdoor group fitness: Zumba, Yoga, Barre, HIIT, Pilates, Dance &amp; Cycle",
     "Full-service locker rooms with sauna, steam room &amp; hot tub", "Onsite sports &amp; therapeutic massage services",
     "Expert fitness &amp; nutrition coaches", "Towel service, including chilled eucalyptus towels", "NEW Cold Plunge by Chilly Goat®"],
    "sj_pool_sunset.jpg",
    # pool_sunset_SJ_500px.jpg dropped — it is this same shot, and the hero already carries it
    ["SJ_gym_floor_HERO_gradient-scaled.jpg", "SJ_pool_662x501_v1.jpg"],
    [("Mon–Thu", "5am – 11pm"), ("Friday", "5am – 10pm"), ("Sat–Sun", "6am – 8pm")],
    # Desktop has no horizontal overflow on this frame, so the x value is purely a
    # phone crop: 32% lands on the palm cluster, pink sky and lane lines. Anything
    # past ~50% slides onto the perimeter wall and loses both the sunset and the pool.
    hero_focal="32% 50%",
    hero_media_mod="hero__media--sky",
)

# ============================================================ RECOVERY
recovery_body = hero(
    "Recovery",
    ["Recover like an", '<span class="serif">athlete</span>'],
    "At Forma, recovery isn't an afterthought — it's part of the work. Cryotherapy, cold plunge, a full-service spa, sauna, steam and hot tubs. An integrated view of wellness, all under one roof.",
    img=f"{IMG}/neck_hold_BLUR_2000x1333px_v2.jpg",
    crumb="Recovery",
    actions=[("Book Recovery", "contact.html#tour", True), ("Explore Cryo", "cryo.html", False)],
    meta=["Cryo + cold plunge", "Full-service spa", "Sauna · steam · hot tub"],
    page=True,
) + split(
    "Cryotherapy + cold plunge", "01",
    'Perform better, recover <span class="serif">faster</span>',
    ["After experiencing cryotherapy and cold plunges for ourselves, we brought them in-house so you can enjoy the benefits and the convenience of a comprehensive wellness solution in one location.",
     "Burn 500–800 calories in a single 3-minute session, reduce inflammation and pain, heal injuries faster, improve circulation, sleep better and feel invigorated. Natural, non-invasive, and trusted by Olympic and professional athletes."],
    f"{IMG}/Forma_WalnutCreek_locations_cryo.jpg",
    "Cryotherapy chamber at Forma",
    cta=("All about cryo", "cryo.html"),
) + split(
    "The spa", "02",
    'The optimum wellness <span class="serif">experience</span>',
    ["A comprehensive menu of therapeutic treatments — massage, facials, Reiki and clinical skin care — performed by skilled, professional therapists dedicated to easing pain, restoring function and rejuvenating face and body.",
     "Conveniently located adjacent to the locker rooms, so sauna, steam or Jacuzzi can be enjoyed before or after your treatment."],
    f"{IMG}/Forma_Walnut-Creek_Spa_Header_2018.jpg",
    "The Spa at Forma",
    rev=True, cta=("See spa menu &amp; pricing", "spa.html"),
) + split(
    "Mind Body LAB", "03",
    'Where science meets <span class="serif">self-care</span>',
    ["Our Mind Body LAB brings together recovery technology, brain health and the mind-body connection — including DrBrainRX — to help you feel as good mentally as you do physically.",
     "Because true wellness isn't just how you move. It's how you think, recover, and feel."],
    f"{IMG}/slider-meditate_v2.jpg",
    "Mind Body LAB at Forma",
    cta=("Explore the LAB", "mindbodylab.html"),
) + cta_band(
    'Restore. Rejuvenate. <span class="serif">Repeat.</span>',
    "Recovery is included in the Forma experience. Book a session and walk out feeling brand new.",
    f"{IMG}/chillyGOAT_SJ_500px.jpg",
)

# ============================================================ CRYO
cryo_body = hero(
    "Cryotherapy + Cold Plunge",
    ["Three minutes.", 'Total <span class="serif">reset</span>.'],
    "An integrated view of wellness and recovery. We experienced cryotherapy and cold plunges ourselves — then brought them here so you can enjoy the benefits and the convenience, all in one location.",
    img=f"{IMG}/Forma_WalnutCreek_locations_cryo.jpg",
    crumb='<a href="recovery.html">Recovery</a> &nbsp;/&nbsp; Cryotherapy',
    actions=[("Book a Session", "contact.html#tour", True)],
    meta=["-195°F chamber", "Burn 500–800 cal", "Trusted by pro athletes"],
    page=True,
) + f"""
<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">The benefits</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">What three minutes <span class="serif">does</span></h2>
      </div>
    </div>
    <div class="pillars" data-stagger>
      <div class="pillar"><span class="pillar__num">Body</span><h3>Perform better + recover faster</h3><p>Improve energy and stamina, reduce inflammation, pain and swelling, and heal injuries faster.</p></div>
      <div class="pillar"><span class="pillar__num">Skin</span><h3>Look younger</h3><p>Improve circulation and oxygenation, increase collagen production, and reduce cellulite.</p></div>
      <div class="pillar"><span class="pillar__num">Weight</span><h3>Lose weight</h3><p>Burn 500–800 calories in a single 3-minute session, improve metabolic rate, and reduce fat deposits.</p></div>
      <div class="pillar"><span class="pillar__num">Mind</span><h3>Sleep + feel better</h3><p>Improve mood and cognition, feel invigorated, and promote deeper, more restful sleep.</p></div>
    </div>
  </div>
</section>
""" + split(
    "How it works", "02",
    'Natural, non-invasive, <span class="serif">cutting-edge</span>',
    ["Cryotherapy uses brief, intense exposure to gasiform nitrogen to lower the skin's temperature to 41–50°F, with the chamber dropping to -195°F. The skin signals the brain, stimulating immune and basic body systems, releasing endorphins and blocking pain.",
     "The result is vasoconstriction followed by vasodilation — blood returning to your extremities highly oxygenated and nutrient-rich, helping the body repair and strengthen. The buoyant effects can last up to 8 hours, and many clients report better sleep after a single session."],
    f"{IMG}/chillyGOAT_SJ_500px.jpg",
    "Cryotherapy facility",
    rev=True,
) + f"""
<section class="section section--panel">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">Real members, real results</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Feel the <span class="serif">difference</span></h2>
      </div>
    </div>
    <div class="card-grid" data-stagger>
      <div class="card"><div class="card__below" style="padding-top:0"><blockquote style="font-family:var(--font-serif);font-style:italic;font-size:24px;line-height:1.4;margin-bottom:18px">“I was able to reduce the inflammation, reduce the soreness… it's prolonged my enjoyment of exercise and weightlifting.”</blockquote><p style="color:var(--accent-ink);font-weight:600;letter-spacing:.04em">— Dave M.</p></div></div>
      <div class="card"><div class="card__below" style="padding-top:0"><blockquote style="font-family:var(--font-serif);font-style:italic;font-size:24px;line-height:1.4;margin-bottom:18px">“When I came in, I had sharp pains in my back… and I just didn't have the pain like I had when I walked in.”</blockquote><p style="color:var(--accent-ink);font-weight:600;letter-spacing:.04em">— Tracy B.</p></div></div>
      <div class="card"><div class="card__below" style="padding-top:0"><blockquote style="font-family:var(--font-serif);font-style:italic;font-size:24px;line-height:1.4;margin-bottom:18px">“Movement is medicine — and recovery is how you keep moving. Cryo is part of my weekly routine now.”</blockquote><p style="color:var(--accent-ink);font-weight:600;letter-spacing:.04em">— Joshua S.</p></div></div>
    </div>
  </div>
</section>
""" + form_section(
    "book", "04", "Book cryotherapy",
    'Ready to <span class="serif">chill</span>?',
    "Tell us how to reach you and which club works best, and we'll get your first cryotherapy session on the calendar. Members and guests are both welcome.",
    "Book My Session", light=False, ac_id=72,
) + cta_band(
    'Book your first <span class="serif">session</span>',
    "Three minutes to less pain, better sleep, and faster recovery. Members and guests welcome.",
    f"{IMG}/chillyGOAT_SJ_500px.jpg",
    primary=("Book a Session", "contact.html#tour"),
)

# ============================================================ SPA
spa_body = hero(
    "The Spa",
    ["Pause.", '<span class="serif">Restore.</span>'],
    "A comprehensive menu of therapeutic treatments — massage, facials, Reiki and clinical skin care — in a cozy, luxurious setting steps from the sauna, steam and Jacuzzi. Skilled therapists dedicated to easing pain and rejuvenating face and body.",
    img=f"{IMG}/Forma_San-Jose-spa_Header_2018.jpg",
    focal="50% 68%", tinted=True,
    crumb="The Spa",
    actions=[("Book a Treatment", "tel:9259326400", True)],
    meta=["Massage · facials · Reiki · skin care", "Walnut Creek &amp; San Jose"],
    page=True,
) + f"""
<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">Massage</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Therapeutic <span class="serif">touch</span></h2>
      </div>
      <p class="body-copy reveal" style="max-width:32ch">Call to schedule: <a href="tel:9259326400" style="color:var(--accent)">(925) 932-6400</a></p>
    </div>
    <div class="sched" data-stagger>
      <div class="sched__col"><h4>Signature Swedish</h4><span class="where">Relax &amp; restore</span><dl><div><dt>25 min</dt><dd>$65</dd></div><div><dt>50 min</dt><dd>$115</dd></div><div><dt>80 min</dt><dd>$160</dd></div></dl></div>
      <div class="sched__col"><h4>Deep Tissue</h4><span class="where">Release tension</span><dl><div><dt>25 min</dt><dd>$65</dd></div><div><dt>50 min</dt><dd>$115</dd></div><div><dt>80 min</dt><dd>$160</dd></div></dl></div>
      <div class="sched__col"><h4>Sports Massage</h4><span class="where">Recover faster</span><dl><div><dt>25 min</dt><dd>$65</dd></div><div><dt>50 min</dt><dd>$115</dd></div><div><dt>80 min</dt><dd>$160</dd></div></dl></div>
      <div class="sched__col"><h4>Prenatal</h4><span class="where">Gentle care</span><dl><div><dt>25 min</dt><dd>$65</dd></div><div><dt>50 min</dt><dd>$115</dd></div><div><dt>80 min</dt><dd>$160</dd></div></dl></div>
      <div class="sched__col"><h4>Reflexology</h4><span class="where">Pressure points</span><dl><div><dt>25 min</dt><dd>$65</dd></div><div><dt>50 min</dt><dd>$115</dd></div><div><dt>80 min</dt><dd>$160</dd></div></dl></div>
      <div class="sched__col"><h4>Reiki</h4><span class="where">Energy work</span><dl><div><dt>25 min</dt><dd>$65</dd></div><div><dt>50 min</dt><dd>$115</dd></div><div><dt>80 min</dt><dd>$160</dd></div></dl></div>
    </div>
    <p class="body-copy reveal" style="margin-top:22px">Add-ons: Aroma-Free CBD $10 · Hot Stone $20</p>
  </div>
</section>

<section class="section section--panel">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">Skincare</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Glow, <span class="serif">restored</span></h2>
      </div>
    </div>
    <div class="sched" data-stagger>
      <div class="sched__col"><h4>Forma Signature Facial</h4><dl><div><dt>Single</dt><dd>$140</dd></div><div><dt>3-pack</dt><dd>$375</dd></div></dl></div>
      <div class="sched__col"><h4>About Face Total Renewal</h4><dl><div><dt>Intro</dt><dd>$165</dd></div><div><dt>Single</dt><dd>$230</dd></div><div><dt>3-pack</dt><dd>$645</dd></div></dl></div>
      <div class="sched__col"><h4>Microdermabrasion Plus Light</h4><dl><div><dt>Single</dt><dd>$145</dd></div><div><dt>3-pack</dt><dd>$390</dd></div></dl></div>
      <div class="sched__col"><h4>Customized Pro Peels</h4><dl><div><dt>Range</dt><dd>$115–$195</dd></div></dl></div>
    </div>
  </div>
</section>
""" + cta_band(
    'Your body has earned <span class="serif">this</span>',
    "Treatments can be enjoyed before or after the sauna, steam or hot tub. Call your club to book.",
    f"{IMG}/Forma_San-Jose-spa_Header_2018.jpg",
    primary=("Call to Book", "tel:9259326400"), secondary=("San Jose Spa", "tel:4083631010"),
)

# ============================================================ MIND BODY LAB
mbl_body = hero(
    "Mind Body LAB",
    ["Train your", '<span class="serif">brain</span>, too'],
    "Where science meets self-care. The Mind Body LAB brings together recovery technology, brain health and the mind-body connection — because true wellness is how you think and feel, not just how you move.",
    img=f"{IMG}/circle_connect_BLUR_2000x1333px.jpg",
    crumb="Mind Body LAB",
    actions=[("Book a Tour", "contact.html#tour", True)],
    page=True,
) + split(
    "DrBrainRX", "01",
    'Fitness for your <span class="serif">mind</span>',
    ["DrBrainRX brings brain-training and cognitive wellness into the club — tools to sharpen focus, manage stress, and support long-term brain health as part of your overall fitness.",
     "Because the strongest version of you is sharp, calm and resilient — not just physically fit."],
    f"{IMG}/drsara_square_transparent_HERO_v2.png",
    "DrBrainRX brain health",
    cta=("Ask us about DrBrainRX", "contact.html#tour"),
) + split(
    "Meditation + breathwork", "02",
    'Find your <span class="serif">stillness</span>',
    ["Our meditation and breathwork classes offer a structured, peaceful space to reduce stress and build mental clarity — guided by experienced instructors, suitable for everyone from first-timers to seasoned practitioners.",
     "Reset your nervous system, then carry that calm into the rest of your day."],
    f"{IMG}/slider-meditate_v2.jpg",
    "Meditation class at Forma",
    rev=True, cta=("See the class lineup", "group-fitness.html#classes"),
) + cta_band(
    'Strong body. <span class="serif">Clear mind.</span>',
    "The Mind Body LAB is part of the Forma experience. Come explore what whole-person wellness feels like.",
    f"{IMG}/slider-stretch_recovery_v1.jpg",
)

# ============================================================ KIDZVILLE
kidz_body = hero(
    "Kidzville",
    ["A guilt-free", '<span class="serif">workout</span>'],
    "We created a unique indoor and outdoor environment where you can enjoy your workout while your kids (ages 6 weeks–12 years) are free to play in a safe, active, and educational space. Walnut Creek location.",
    img=f"{IMG}/forma-kids-header-background-tug_WIDE.jpg",
    crumb="Kidzville",
    actions=[("Reserve a Spot", "tel:9259326400", True)],
    meta=["Ages 6 weeks–12 years", "Walnut Creek location", "Reservations recommended"],
    page=True,
) + f"""
<section class="section">
  <div class="wrap">
    <div class="intro-grid">
      <div>
        <p class="eyebrow">Safe · active · educational</p>
        <h2 class="h-display reveal">Where kids actually want to <span class="serif">be</span></h2>
      </div>
      <div class="intro-grid__right">
        <p class="lede reveal">We offer you the time and space to break free from family responsibilities for a little while — to socialize and work out — while our reliable, capable staff helps your kids enjoy plenty of play and learning.</p>
        <p class="body-copy reveal">Forma Kidzville was created to provide a safe, stimulating and playful environment where children and preteens are free to learn, explore, experiment, and be active, imaginative and creative. We incorporate innovative games and activities — giving your child the chance to participate with groups, pursue individual interests, or just play with old and new friends.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--panel" id="hours">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">Kidzville hours</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">When we're <span class="serif">open</span></h2>
      </div>
      <p class="body-copy reveal" style="max-width:34ch">Questions or sign-ups: <a href="mailto:WCReps@formagym.com" style="color:var(--accent-ink)">WCReps@formagym.com</a> or call the front desk at (925) 932-6400. Reservations recommended.</p>
    </div>
    <div class="sched" data-stagger>
      <div class="sched__col"><h4>Mon–Thu</h4><span class="where">Morning &amp; evening</span><dl><div><dt>AM</dt><dd>8:00am – 1:00pm</dd></div><div><dt>PM</dt><dd>4:00pm – 7:30pm</dd></div></dl></div>
      <div class="sched__col"><h4>Friday</h4><span class="where">Mornings</span><dl><div><dt>AM</dt><dd>8:00am – 1:00pm</dd></div></dl></div>
      <div class="sched__col"><h4>Sat–Sun</h4><span class="where">Mornings</span><dl><div><dt>AM</dt><dd>8:00am – 12:00pm</dd></div></dl></div>
    </div>
  </div>
</section>
""" + cta_band(
    'Bring the <span class="serif">whole family</span>',
    "Your kids will look forward to it as much as you look forward to your workout. Reserve a spot and Play Every Day.",
    f"{IMG}/kidzville_header_v3.jpg",
    primary=("Reserve a Spot", "tel:9259326400"),
)

# ============================================================ RISE
rise_body = hero(
    "RISE Program",
    ["Movement is", '<span class="serif">medicine</span>'],
    "RISE is an exercise-based therapy program for individuals living with paralysis — focused on function, strength, and improving the physiological and neurological function of the body. Your life is an opportunity. RISE to it.",
    img=f"{IMG}/rise_room_blur.jpg",
    crumb="RISE",
    actions=[("Get Started", "contact.html#tour", True), ("Learn More", "#method", False)],
    page=True,
) + f"""
<section class="section section--tight">
  <div class="wrap">
    <figure class="quote-band reveal">
      <span class="quote-band__mark">“</span>
      <blockquote>We believe MOVEMENT IS MEDICINE — and we encourage you to play every day, embrace change, and build an open-minded environment to improve function and your quality of life.</blockquote>
      <figcaption>The RISE Program</figcaption>
    </figure>
  </div>
</section>
""" + f"""
<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">What RISE delivers</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Get moving <span class="serif">again</span></h2>
      </div>
    </div>
    <div class="pillars" data-stagger style="grid-template-columns:repeat(3,1fr)">
      <div class="pillar"><span class="pillar__num">01</span><h3>Wheelchair free</h3><p>Your body was designed to MOVE. Recovery sessions are conducted out of your chair to get you moving again.</p></div>
      <div class="pillar"><span class="pillar__num">02</span><h3>Less medication</h3><p>Many clients find a reduced dependency on medication — or rid their use of it entirely.</p></div>
      <div class="pillar"><span class="pillar__num">03</span><h3>Better quality of life</h3><p>We stimulate your central nervous system to promote neuroplasticity — rebuilding the pathways your brain needs.</p></div>
    </div>
  </div>
</section>

<section class="section section--panel" id="method">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">Our methodology</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">A step-by-step <span class="serif">method</span></h2>
      </div>
      <p class="body-copy reveal" style="max-width:34ch">Each client's needs are carefully addressed to support our mission of achieving your recovery goals.</p>
    </div>
    <div class="steps reveal">
      <div class="step"><span class="step__num">01</span><h3>Assess</h3><p>The most important first step is the client's body, mindset and willingness to overcome obstacles.</p></div>
      <div class="step"><span class="step__num">02</span><h3>Diagnose</h3><p>Identifying and understanding the injury or condition is crucial to educate ourselves and the client and build a plan.</p></div>
      <div class="step"><span class="step__num">03</span><h3>Educate</h3><p>We review the assessment, recovery goals, and the mental and physical fortitude the journey will require.</p></div>
      <div class="step"><span class="step__num">04</span><h3>Program</h3><p>We design a program according to the client — built entirely around their recovery needs and goals.</p></div>
    </div>
  </div>
</section>
""" + cta_band(
    'Your life is an <span class="serif">opportunity</span>',
    "RISE includes a scholarship program so cost is never the reason you can't start. Reach out and let's begin.",
    f"{IMG}/rise_room_blur.jpg",
    primary=("Get Started", "contact.html#tour"), secondary=("Scholarship Program", "contact.html#tour"),
)

# ============================================================ GIVES BACK
givesback_body = hero(
    "Forma Gives Back",
    ["Fitness for", '<span class="serif">everyone</span>'],
    "From those struggling just to stand to world-class athletes, we believe fitness and health should be available to EVERYONE on the spectrum of movement. Giving back isn't a campaign at Forma — it's who we are.",
    img=f"{IMG}/slider-hero_ladies_v1.jpg",
    crumb="Gives Back",
    actions=[("Get Involved", "contact.html#tour", True)],
    page=True,
    # A 2.1:1 frame in a 0.6:1 phone hero shows only 29% of the width, so the
    # default centre landed on mid-thigh. 64% puts two faces in shot instead, and
    # still clears the whole group on desktop, where 88% of the width is visible.
    focal="64% 50%",
) + split(
    "Our belief", "01",
    'A community for <span class="serif">all</span>',
    ["We're very proud of what we've created, and we love our Members, our Team, and our Community. That love shows up in how we give back — making space, programs and scholarships available to people who need them most.",
     "The RISE Program's scholarship fund, accessible programming, and local partnerships are all part of how Forma shows up for the Bay Area."],
    f"{IMG}/slider-locations_turf_alysse_torey.jpg",
    "Forma community giving back",
    cta=("Learn about RISE", "rise.html"),
) + cta_band(
    'Play it <span class="serif">forward</span>',
    "Want to get involved, donate, or nominate someone for a scholarship? We'd love to hear from you.",
    f"{IMG}/slider-locations_group_dance.jpg",
    primary=("Get Involved", "contact.html#tour"),
)

# ============================================================ CLASS DETAIL PAGES
# A phone hero is portrait (~0.56:1) but these stills are 2:1, so cover shows
# only ~27% of the frame — a narrow vertical strip. Where the subject sits well
# off-centre, pin the crop to it. Slugs not listed here read fine centred.
CLASS_FOCAL = {
    "low-impact":       "74% 50%",
    "kickboxing":       "76% 50%",
    "meditation":       "78% 50%",
    "pilates-reformer": "72% 50%",
    "trx":              "68% 50%",
}


def class_page(slug, title, img, lead, others):
    other_cards = ""
    for ol, oh, od in others:
        other_cards += f'<a class="row-item" href="{oh}"><span class="row-item__idx">→</span><span class="row-item__title">{ol}</span><span class="row-item__desc">{od}</span><span class="row-item__arrow">→</span></a>'
    return hero(
        "Group Fitness", [title.split()[0], f'<span class="serif">{" ".join(title.split()[1:]) or "Studio"}</span>'] if len(title.split()) > 1 else [f'<span class="serif">{title}</span>'],
        lead, img=f"{IMG}/{img}", crumb=f'<a href="group-fitness.html">Group Fitness</a> &nbsp;/&nbsp; {title}',
        actions=[("Visit Us", "join.html", True), ("Full Schedule", "group-fitness.html#schedule", False)],
        meta=["Included with membership", "All levels welcome"], page=True,
        focal=CLASS_FOCAL.get(slug),
    ) + f"""
<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">More ways to move</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Mix it <span class="serif">up</span></h2>
      </div>
    </div>
    <div class="rows reveal">{other_cards}</div>
  </div>
</section>
""" + cta_band(
        f'Try <span class="serif">{title.split()[0]}</span>',
        "Every class is included with membership. Come find your format.",
        f"{IMG}/{img}",
    )


# ============================================================ JOIN
join_body = hero(
    "Join Forma Online",
    ["Join in", '<span class="serif">minutes</span>'],
    'Pick your club, choose your membership, and you\'re in. <em>Must be 18+ to join without a parent or guardian.</em>',
    img=f"{IMG}/gym_floor_WC_500px.jpg",
    crumb="Join Now",
    actions=[("Start My Membership", "#wizard", True), ("Book a Tour", "contact.html#tour", False)],
    meta=["30 day money back guarantee"],
    page=True,
) + f"""
<section class="join" id="wizard">
  <div class="wrap">
    <div class="join__grid">
      <div class="join__main">
        <div class="join__progress">
          <div class="join__progress-bar"><i></i></div>
          <ol class="join__steps-nav">
            <li class="is-active"><span class="n">01</span><span class="lbl">Club</span></li>
            <li><span class="n">02</span><span class="lbl">Membership</span></li>
            <li><span class="n">03</span><span class="lbl">Details</span></li>
            <li><span class="n">04</span><span class="lbl">Family</span></li>
            <li><span class="n">05</span><span class="lbl">Add-ons</span></li>
            <li><span class="n">06</span><span class="lbl">Payment</span></li>
          </ol>
        </div>
        <div class="join__steps">

          <div class="join-step is-active" data-step="1">
            <h2 class="join-step__title">Select your <span class="serif">club</span></h2>
            <p class="join-step__hint">Choose the Forma location most convenient for you. Premier members get both.</p>
            <div class="choice-grid">
              <button class="choice" type="button" data-club="Walnut Creek" data-img="{IMG}/wc_facade.jpg">
                <span class="choice__chip">Since 2009</span><span class="choice__check">✓</span>
                <div class="choice__img"><img src="{IMG}/wc_facade.jpg" alt="Walnut Creek" loading="lazy"></div>
                <h3>Forma Walnut Creek</h3>
                <p class="meta">1908 Olympic Blvd · 35,000 sq ft</p>
                <ul class="choice__perks"><li>Complimentary Fitness Consultation</li><li>Complimentary Nutrition Consultation</li><li>30-Day Money-Back Guarantee</li></ul>
              </button>
              <button class="choice" type="button" data-club="San Jose" data-img="{IMG}/sj_facade.jpg">
                <span class="choice__chip">Since 2015</span><span class="choice__check">✓</span>
                <div class="choice__img"><img src="{IMG}/sj_facade.jpg" alt="San Jose" loading="lazy"></div>
                <h3>Forma San Jose</h3>
                <p class="meta">5434 Thornwood Dr · 40,000 sq ft</p>
                <ul class="choice__perks"><li>Complimentary Fitness Consultation</li><li>Complimentary Nutrition Consultation</li><li>30-Day Money-Back Guarantee</li></ul>
              </button>
            </div>
          </div>

          <div class="join-step" data-step="2">
            <h2 class="join-step__title">Choose your <span class="serif">membership</span></h2>
            <p class="join-step__hint">Select the plan that fits your fitness goals.</p>
            <div class="plan-grid">
              <button class="plan-card" type="button" data-plan="Premier" data-primary="215" data-addl="160" data-enroll="350">
                <span class="plan-card__chip">Most Popular</span><span class="choice__check">✓</span>
                <h3>Premier Membership</h3>
                <div class="plan-card__price">$215<small>/mo</small></div>
                <p class="plan-card__addl">2nd adult $160/mo · 3rd+ adult $160/mo</p>
                <h6>Included</h6>
                <ul class="plan-card__list">
                  <li>Everything in Standard, plus:</li>
                  <li>Four cryotherapy sessions a month</li>
                  <li>Four guest passes a month</li>
                  <li>10% off retail items</li>
                  <li>Access to <strong>both</strong> San Jose &amp; Walnut Creek</li>
                </ul>
                <h6>Premier service perk</h6>
                <ul class="plan-card__list"><li>One Personal Training, Massage, Private Pilates, <em>or</em> two Kidzville memberships</li></ul>
                <span class="plan-card__pick">Select Premier</span>
              </button>
              <button class="plan-card" type="button" data-plan="Standard" data-primary="119" data-addl="95" data-enroll="350">
                <span class="choice__check">✓</span>
                <h3>Standard Membership</h3>
                <div class="plan-card__price">$119<small>/mo</small></div>
                <p class="plan-card__addl">2nd adult $95/mo · 3rd+ adult $95/mo</p>
                <h6>Included</h6>
                <ul class="plan-card__list">
                  <li>Access to Walnut Creek location</li>
                  <li>Indoor &amp; outdoor fitness spaces</li>
                  <li>1-hour fitness consultation</li>
                  <li>85+ group fitness classes a week</li>
                  <li>Full-service locker rooms</li>
                  <li>Forma App for access &amp; reservations</li>
                </ul>
                <span class="plan-card__pick">Select Standard</span>
              </button>
            </div>
            <p class="join-step__foot">Both plans include a complimentary Formation Session. 12-month commitment with monthly billing, backed by our 30-day money-back guarantee.</p>
          </div>

          <div class="join-step" data-step="3">
            <h2 class="join-step__title">Your <span class="serif">details</span></h2>
            <p class="join-step__hint">The primary member on the account. Must be 18 or older.</p>
            <div class="form-grid">
              <div class="field"><input type="text" name="first" id="j-first" placeholder=" " required><label for="j-first">First name</label></div>
              <div class="field"><input type="text" name="last" id="j-last" placeholder=" " required><label for="j-last">Last name</label></div>
              <div class="field"><input type="email" name="email" id="j-email" placeholder=" " required><label for="j-email">Email address</label></div>
              <div class="field"><input type="tel" name="phone" id="j-phone" placeholder=" " required><label for="j-phone">Phone</label></div>
              <div class="field field--full"><input type="text" name="address" id="j-address" placeholder=" "><label for="j-address">Home address</label></div>
            </div>
          </div>

          <div class="join-step" data-step="4">
            <h2 class="join-step__title">Add <span class="serif">family</span></h2>
            <p class="join-step__hint">Add household members at the additional-adult rate. Skip this step if it's just you.</p>
            <div class="family-list" id="familyList"></div>
            <button class="btn btn--sm add-family" type="button" style="margin-top:8px">+ Add a family member</button>
          </div>

          <div class="join-step" data-step="5">
            <h2 class="join-step__title">Enhance your <span class="serif">membership</span></h2>
            <p class="join-step__hint">All optional. Add what you want — skip the rest.</p>

            <h6 class="addon-head">Jump Start Packages <span>one-time, available only at sign-up</span></h6>
            <div class="addon-grid">
              <label class="addon"><input type="checkbox" data-addon="onetime" data-label="Personal Training Jump Start" data-amt="175"><div><h4>Personal Training</h4><p>5 sessions, 1-on-1 — up to a $XXX value.</p><span class="addon__price">$175</span></div></label>
              <label class="addon"><input type="checkbox" data-addon="onetime" data-label="Recovery Jump Start" data-amt="175"><div><h4>Recovery</h4><p>Sensitivity session, trigger-point or sports massage + Echo Brain Water.</p><span class="addon__price">$175</span></div></label>
              <label class="addon"><input type="checkbox" data-addon="onetime" data-label="Stretch &amp; Recovery" data-amt="50"><div><h4>Stretch &amp; Recovery</h4><p>Improve flexibility, range of motion and circulation.</p><span class="addon__price">$50</span></div></label>
            </div>

            <h6 class="addon-head">Add to your monthly plan</h6>
            <div class="addon-grid">
              <label class="addon"><input type="checkbox" data-addon="monthly" data-label="Mobile App Premium" data-amt="5"><div><h4>Mobile App Premium</h4><p>Advanced workout tracking, exclusive content and priority booking.</p><span class="addon__price">$5/mo</span></div></label>
              <label class="addon"><input type="checkbox" data-addon="monthly" data-label="Virtual Coaching" data-amt="30"><div><h4>Virtual Coaching</h4><p>Check in with a personal trainer to review progress and adjust your plan.</p><span class="addon__price">$30/mo</span></div></label>
              <label class="addon"><input type="checkbox" data-addon="monthly" data-label="Workout Planner" data-amt="10"><div><h4>Workout Planner</h4><p>An AI-powered workout planner that adapts to your progress and schedule.</p><span class="addon__price">$10/mo</span></div></label>
            </div>

            <div class="premier-perk" hidden>
              <h6 class="addon-head">Your Premier perk <span>included — choose one</span></h6>
              <div class="seg seg--wrap" role="group" aria-label="Premier perk">
                <button type="button" class="is-on" data-perk="One Personal Training">Personal Training</button>
                <button type="button" data-perk="One Massage">Massage</button>
                <button type="button" data-perk="Private Pilates">Private Pilates</button>
                <button type="button" data-perk="Two Kidzville memberships">Two Kidzville</button>
              </div>
            </div>
          </div>

          <div class="join-step" data-step="6">
            <h2 class="join-step__title">Review &amp; <span class="serif">payment</span></h2>
            <p class="join-step__hint">Your first monthly payment comes after you join.</p>
            <div id="reviewList"></div>
            <div class="seg" role="group" aria-label="Payment method" style="margin-top:24px">
              <button type="button" class="is-on" data-pay="card">Credit Card</button>
              <button type="button" data-pay="bank">Bank Account</button>
            </div>
            <div class="form-grid" style="margin-top:18px">
              <div class="field field--full"><input type="text" name="ccname" id="j-ccname" placeholder=" "><label for="j-ccname">Card holder name</label></div>
              <div class="field field--full"><input type="text" name="ccnum" id="j-ccnum" placeholder=" " inputmode="numeric"><label for="j-ccnum">Card number</label></div>
              <div class="field"><input type="text" name="ccexp" id="j-ccexp" placeholder=" "><label for="j-ccexp">Expiry (MM/YY)</label></div>
              <div class="field"><input type="text" name="cccvc" id="j-cccvc" placeholder=" " inputmode="numeric"><label for="j-cccvc">CVC</label></div>
            </div>
            <label class="review-agree"><input type="checkbox" id="agree"><span>I'm 18+ (or joining with a parent/guardian), I agree to the <a href="contact.html">Terms of Service</a> and <a href="privacy.html">Privacy Policy</a>, and I understand this is a 12-month commitment with monthly billing, backed by a 30-day money-back guarantee. This is a design demo — no payment will be processed.</span></label>
          </div>

        </div>
        <div class="join__nav-row">
          <button class="btn btn--sm back" type="button">← Back</button>
          <span class="join__count">Step 01 / 06</span>
          <button class="btn btn--solid next" type="button" disabled><span class="lbl">Continue</span> <span class="arr">→</span></button>
        </div>
      </div>

      <aside class="join__summary" aria-label="Order summary">
        <div class="join__summary-head"><h4>Order Summary</h4><span>FORMA</span></div>
        <div class="join__summary-body">
          <div class="sum-row"><dt>Club</dt><dd class="empty" data-sum="loc">—</dd></div>
          <div class="sum-row"><dt>Membership</dt><dd class="empty" data-sum="plan">—</dd></div>
          <div class="sum-lines" data-sum-lines></div>
          <div class="sum-rate"><span class="lbl">Monthly total</span><span class="amt" data-sum-monthly>$0<small>/mo</small></span></div>
          <div class="sum-due"><span>Due today</span><b data-sum-today>$0.00</b></div>
          <p class="sum-note">Monthly billing begins with your first month.</p>
          <span class="sum-badge">30-Day Money-Back Guarantee</span>
        </div>
      </aside>
    </div>
  </div>
</section>

<!-- Lead bridge: the wizard is the visible experience, but the lead still has to
     reach ActiveCampaign. join.js fills this hidden form 103 on completion and
     submits it, so joins land on the same list/tags/automations as before. -->
<div class="ac-bridge ac-form ac-form--103" aria-hidden="true">{ac_form(103)}</div>

<div class="join-success" role="dialog" aria-modal="true" aria-label="Membership confirmed">
  <div class="join-success__inner">
    <div class="mark">✓</div>
    <h2 data-success-name>Welcome to the Forma Family.</h2>
    <p>Your membership request is in. Because this is a design demo, no payment was processed — on the live site you'd be all set to walk in and get started. Time to Play Every Day.</p>
    <div class="hero__actions">
      <a class="btn btn--solid" href="index.html">Back to Home <span class="arr">→</span></a>
      <a class="btn" href="group-fitness.html">Browse Classes <span class="arr">→</span></a>
    </div>
  </div>
</div>
<script src="assets/js/join.js?v={V}" defer></script>
""" + cta_band(
    'Questions before you <span class="serif">join?</span>',
    "Book a tour and we'll show you around, answer everything, and help you pick the right membership.",
    f"{IMG}/jason_johnson_turf2.jpg",
    primary=("Book a Tour", "contact.html#tour"), secondary=None,
)

# ============================================================ CONTACT
contact_body = hero(
    "Contact &amp; Tours",
    ["Come <span class=\"serif\">say hi</span>"],
    "Book a tour, ask a question, or just tell us your goal — we'll point you to the right club, class or coach. No pressure, no scripts.",
    img=f"{IMG}/jason_johnson_turf2.jpg",
    crumb="Contact",
    actions=[("Book a Tour", "#tour", True)],
    page=True,
) + form_section(
    "tour", "01", "Book a tour",
    'Let\'s find your <span class="serif">fit</span>',
    "Tell us a little about you and your preferred club, and we'll set up your visit — featuring the best trainers, programs and classes in the Bay Area.",
    "Book My Tour", light=True, ac_id=33,
) + f"""
<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">Two locations</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Reach a <span class="serif">club</span></h2>
      </div>
    </div>
    <div class="card-grid card-grid--2" data-stagger>
      <div class="card"><div class="card__media card__media--wide"><img src="{IMG}/wc_facade.jpg" alt="Walnut Creek" loading="lazy"><div class="card__label"><h3>Walnut Creek</h3></div></div><div class="card__below"><p>1908 Olympic Blvd, Walnut Creek, CA 94596<br><a href="tel:9259326400" style="color:var(--accent)">(925) 932-6400</a><br>Mon–Thu 5am–11pm · Fri 5am–10pm · Sat–Sun 6am–8pm</p></div></div>
      <div class="card"><div class="card__media card__media--wide"><img src="{IMG}/sj_facade.jpg" alt="San Jose" loading="lazy"><div class="card__label"><h3>San Jose</h3></div></div><div class="card__below"><p>5434 Thornwood Dr, San Jose, CA 95123<br><a href="tel:4083631010" style="color:var(--accent)">(408) 363-1010</a><br>Mon–Thu 5am–11pm · Fri 5am–10pm · Sat–Sun 6am–8pm</p></div></div>
    </div>
  </div>
</section>
""" + cta_band(
    'Two clubs, one <span class="serif">membership</span>',
    "Ready when you are. Join online in minutes, or book a tour and let us show you around.",
    f"{IMG}/slider-locations_turf_alysse_torey.jpg",
)

# ============================================================ TRIAL PASS
trial_body = hero(
    "Schedule Your Visit",
    ["Try Forma.", 'Book your <span class="serif">visit</span>.'],
    "Fill out the form below to schedule a visit, a tour, and/or a guest workout — and a complimentary fitness coaching session.",
    img=f"{IMG}/annabelle_kettle_HERO_2.jpg",
    crumb="Trial Pass",
    actions=[("Schedule My Visit", "#tour", True), ("Join Online", "join.html", False)],
    meta=["Coaching session"],
    page=True,
) + f"""
<section class="section section--tight">
  <div class="wrap">
    <div class="intro-grid">
      <div>
        <p class="eyebrow">We're here for you</p>
        <h2 class="h-display reveal">A lifestyle change, not a <span class="serif">quick fix</span></h2>
      </div>
      <div class="intro-grid__right">
        <p class="lede reveal">Forma Gym is a family-run gym created not only to help you shape your body, but to help you take control of every aspect of your life.</p>
        <p class="body-copy reveal">Our metric of wellness is your outlook on life — connection, gratitude, eating well, moving every day, and living a life of fulfillment. Whether you're recapturing your health, increasing your capacity, or changing your physique, we understand that everyone has obstacles to achieving their goals. Forma has the tools and support you need to feel comfortable, have fun, and enjoy the journey.</p>
      </div>
    </div>
  </div>
</section>
""" + form_section(
    "tour", "02", "Schedule your visit",
    'Book your <span class="serif">visit</span>',
    "We have a fitness solution for you — hundreds of monthly classes across every intensity and experience level, whether you've never had a gym membership or you've tried them all. Complete the form and we'll set up your visit and coaching session.",
    "Visit Us", ac_id=33,
) + cta_band(
    'Come <span class="serif">play</span> with us',
    "Two unique Bay Area clubs. The only thing left to do is show up.",
    f"{IMG}/slider-locations_turf_alysse_torey.jpg",
)

# ============================================================ OUTDOOR
outdoor_body = hero(
    "Outdoor Fitness",
    ["Train under the", '<span class="serif">California sky</span>'],
    "Our members LOVE to exercise outdoors — and we LOVE giving them the environment and tools to show up and move every day. We've expanded our outdoor footprint so you have everything you need, all year-round.",
    img=f"{IMG}/slider-locations_turf_alysse_torey.jpg",
    crumb="Outdoor",
    actions=[("Visit Us", "join.html", True)],
    meta=["Covered outdoor turf", "Rain or shine", "Both clubs"],
    page=True,
) + f"""
<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">The outdoor playground</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Everything you need, <span class="serif">outside</span></h2>
      </div>
      <p class="body-copy reveal" style="max-width:34ch">Walnut Creek's turf sits under towering redwoods. San Jose's 8,000 sq. ft. covered outdoor area runs year-round beneath the palms.</p>
    </div>
    <div class="pillars" data-stagger style="grid-template-columns:repeat(2,1fr)">
      <div class="pillar"><span class="pillar__num">01</span><h3>Strength Training</h3><p>Full outdoor strength setups so you never have to choose between iron and fresh air.</p></div>
      <div class="pillar"><span class="pillar__num">02</span><h3>Cardio Equipment</h3><p>Treadmills, bikes and more, set up under cover for year-round outdoor sessions.</p></div>
      <div class="pillar"><span class="pillar__num">03</span><h3>Group Exercise</h3><p>Take your favorite classes into the open air — energy hits different outside.</p></div>
      <div class="pillar"><span class="pillar__num">04</span><h3>Outdoor Cycle</h3><p>Beat-driven rides with a view — the best seat in the house is outdoors.</p></div>
    </div>
  </div>
</section>
""" + cta_band(
    'Move <span class="serif">every day</span> — indoors or out',
    "It's all included with your membership. Come find your favorite spot under the sky.",
    f"{IMG}/SJ_gym_floor_HERO_gradient-scaled.jpg",
)

# ============================================================ DRBRAINRX
drbrain_body = hero(
    "DrBrainRX",
    ["Longevity,", '<span class="serif">optimized</span>'],
    "GLP-1 weight loss care, peptide therapy and longevity medicine — available to Forma members through our DrBrainRX partnership. Because feeling your best is about more than the workout.",
    img=f"{IMG}/circle_connect_BLUR_2000x1333px.jpg",
    crumb='<a href="mindbodylab.html">Mind Body LAB</a> &nbsp;/&nbsp; DrBrainRX',
    actions=[("Member Offer", "#offer", True)],
    meta=["GLP-1 weight loss care", "Peptide therapy", "Longevity medicine"],
    page=True,
) + f"""
<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">What DrBrainRX offers</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Modern wellness <span class="serif">medicine</span></h2>
      </div>
    </div>
    <div class="pillars" data-stagger style="grid-template-columns:repeat(3,1fr)">
      <div class="pillar"><span class="pillar__num">01</span><h3>GLP-1 Weight Loss Care</h3><p>Physician-guided, modern weight-management care tailored to your body and your goals.</p></div>
      <div class="pillar"><span class="pillar__num">02</span><h3>Peptide Therapy</h3><p>Targeted peptide protocols to support recovery, performance and healthy aging.</p></div>
      <div class="pillar"><span class="pillar__num">03</span><h3>Longevity Medicine</h3><p>A proactive, science-led approach to living stronger and sharper for longer.</p></div>
    </div>
  </div>
</section>

<section class="section section--panel" id="offer">
  <div class="wrap">
    <figure class="quote-band reveal">
      <span class="quote-band__mark">“</span>
      <blockquote>Exclusive offer for Forma members: 1 month free + $70 off products. Use code FORMAGYM.</blockquote>
      <figcaption>DrBrainRX × Forma Gym</figcaption>
    </figure>
  </div>
</section>
""" + cta_band(
    'Feel as good as you <span class="serif">look</span>',
    "Ask the front desk about DrBrainRX, or mention it on your tour. Your strongest, sharpest self is the goal.",
    f"{IMG}/slider-locations_group_dance.jpg",
    primary=("Book a Tour", "contact.html#tour"),
)

# ============================================================ APP
app_body = hero(
    "The Forma App",
    ["Your club, in", 'your <span class="serif">pocket</span>'],
    "Book classes, reserve your lane, check schedules and manage your membership — all from the Forma app. Your whole Forma experience, wherever you are.",
    img=f"{IMG}/slider-WC_cycle_indoor_v2.jpg",
    crumb="App",
    actions=[("Get the App", "#download", True)],
    page=True,
) + f"""
<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow">Everything in one place</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Plan your day to <span class="serif">play</span></h2>
      </div>
    </div>
    <div class="pillars" data-stagger style="grid-template-columns:repeat(3,1fr)">
      <div class="pillar"><span class="pillar__num">01</span><h3>Reserve classes &amp; lanes</h3><p>Grab your spot in any group fitness class or book a swim lane in seconds.</p></div>
      <div class="pillar"><span class="pillar__num">02</span><h3>Live schedules</h3><p>See what's on today across both clubs — and never miss your favorite instructor.</p></div>
      <div class="pillar"><span class="pillar__num">03</span><h3>Manage membership</h3><p>Your account, check-ins and member perks, all in the palm of your hand.</p></div>
    </div>
    <div class="hero__actions reveal" id="download" style="opacity:1;transform:none;margin-top:48px">
      <a class="btn btn--solid" href="#">Download on the App Store <span class="arr">→</span></a>
      <a class="btn" href="#">Get it on Google Play <span class="arr">→</span></a>
    </div>
  </div>
</section>
""" + cta_band(
    'Bring Forma <span class="serif">everywhere</span>',
    "Not a member yet? Join today and we'll get you set up on the app on day one.",
    f"{IMG}/annabelle_kettle_HERO_2.jpg",
)

# ============================================================ MERCHANT
merchant_body = hero(
    "Preferred Merchant Program",
    ["Member perks,", 'around <span class="serif">town</span>'],
    "As a locally owned, private fitness club, Forma's goal is to deliver exceptional service and benefits to our members — including preferred pricing at local businesses we love.",
    img=f"{IMG}/slider-hero_ladies_v1.jpg",
    crumb="Member Savings",
    actions=[("Become a Member", "join.html", True)],
    page=True,
    focal="64% 50%",   # same reason as the Gives Back hero
) + f"""
<section class="section section--tight">
  <div class="wrap">
    <div class="intro-grid">
      <div>
        <p class="eyebrow">Locally owned, member first</p>
        <h2 class="h-display reveal">Save with our local <span class="serif">partners</span></h2>
      </div>
      <div class="intro-grid__right">
        <p class="lede reveal">We're partnering with local businesses to give you preferred pricing — a discount to locally owned and operated shops, restaurants and services around the Bay.</p>
        <p class="body-copy reveal">It's our way of supporting the community that supports us — and giving members one more reason to love being part of the Forma Family. Ask the front desk for the current list of preferred merchants.</p>
      </div>
    </div>
  </div>
</section>
""" + cta_band(
    'More reasons to be a <span class="serif">member</span>',
    "Preferred pricing is just one of the perks. Join today and discover the rest.",
    f"{IMG}/slider-locations_group_dance.jpg",
)


def legal_page(title, intro):
    return hero(
        title, [title], intro, img=f"{IMG}/dark_grey_texture_background.jpg",
        crumb=title, page=True,
    ) + f"""
<section class="section section--tight">
  <div class="wrap" style="max-width:820px">
    <p class="body-copy reveal">This is a redesign demonstration of formagym.com. The full {title.lower()} from Forma Gym applies to all members and visitors. For the complete, current policy, please contact a club directly — Walnut Creek (925) 932-6400 or San Jose (408) 363-1010 — or visit the front desk.</p>
    <p class="body-copy reveal">Forma Gym is committed to providing an inclusive, welcoming experience for every member and guest, online and in our clubs. If you encounter any difficulty using this site or need assistance, our team is happy to help.</p>
  </div>
</section>
"""


accessibility_body = legal_page("Accessibility Statement",
    "Forma Gym is committed to making our clubs and our website accessible and welcoming to everyone.")
privacy_body = legal_page("Privacy Policy",
    "Forma is a SPAM-FREE ZONE. We never share or sell your email address or phone number.")

# ============================================================ FREEZE / CANCEL  (MEMBER-ONLY)
# Replaces the live site's /freeze-cancel/ page. Member-facing only: the request
# section is wrapped in .only-member, and guests see a redirect notice instead.
# NOTE: the live page runs ActiveCampaign form 93 (name, email, field[376]).
# The form below is the redesign's demo form — swap in the AC 93 embed on launch.
# NOTE: policy specifics (freeze length, fees, notice period) are intentionally
# NOT stated here — confirm Forma's current terms before publishing.
freeze_body = hero(
    "Member Services",
    ["Freeze or cancel", 'your <span class="serif">membership</span>.'],
    "Life changes — travel, injury, a season away. Put your membership on hold, or close it out. Either way, start the request here and our membership team will confirm by email.",
    img=f"{IMG}/neck_hold_BLUR_2000x1333px_v2.jpg",
    crumb="Freeze or Cancel",
    meta=["Members only", "Requests handled by the membership team", "Written request required"],
    page=True,
) + """
<!-- guests: this page isn't for them -->
<section class="section section--tight only-guest">
  <div class="wrap" style="max-width:820px">
    <p class="eyebrow">Members only</p>
    <h2 class="h-display reveal" style="font-size:clamp(30px,4vw,58px)">This page is for <span class="serif">members</span></h2>
    <p class="lede reveal" style="margin-top:24px">Freeze and cancellation requests are handled for active Forma members. If you're already a member, switch to the Member view using the toggle at the top of the page.</p>
    <p class="body-copy reveal" style="margin-top:18px">Not a member yet? <a class="inline-link" href="join.html">Join Forma</a> or <a class="inline-link" href="contact.html#tour">book a tour</a>.</p>
  </div>
</section>

<!-- members: the real content -->
<div class="only-member">
<section class="section section--tight">
  <div class="wrap">
    <div class="intro-grid">
      <div>
        <p class="eyebrow">Choose your option</p>
        <h2 class="h-display reveal">Freeze, or <span class="serif">cancel</span></h2>
      </div>
      <div class="intro-grid__right">
        <p class="lede reveal">Most members who need a break choose a freeze — it holds your membership and your rate while you're away, so you can pick up where you left off.</p>
        <p class="body-copy reveal">A cancellation closes your membership. Both require a written request, which is what the form below creates. Your club can confirm current terms, any applicable fees, and your minimum-term status before anything is finalized.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="pillars" data-stagger>
      <div class="pillar"><span class="pillar__num">01</span><h3>Freeze</h3><p>Temporarily pause your membership and hold your current rate. Good for travel, injury, deployment, or a season away.</p></div>
      <div class="pillar"><span class="pillar__num">02</span><h3>Cancel</h3><p>Close your membership. A written request is required — this form submits one and starts the confirmation process.</p></div>
      <div class="pillar"><span class="pillar__num">03</span><h3>Not sure?</h3><p>Talk to us first. Walnut Creek <a href="tel:9259326400" style="color:var(--accent)">(925) 932-6400</a> · San Jose <a href="tel:4083631010" style="color:var(--accent)">(408) 363-1010</a>.</p></div>
    </div>
  </div>
</section>
""" + form_section(
    "request", "02", "Submit your request",
    'Start your <span class="serif">request</span>',
    "Tell us your name, the email on your account, and your home club. Add your request details in the message — whether you're freezing or cancelling, and the dates involved. A membership team member will reply by email to confirm.",
    "Submit Request",
    light=False, ac_id=93,
) + """
<section class="section section--tight">
  <div class="wrap" style="max-width:820px">
    <p class="body-copy reveal">Submitting this form creates your written request and time-stamps it. It is not an instant cancellation — you'll receive an email confirming the details and effective date. If you don't hear back within a few business days, please call your home club directly.</p>
  </div>
</section>
</div>
""" + cta_band(
    'Still want to <span class="serif">stay</span>?',
    "If it's a schedule or cost issue, a membership change might solve it. Talk to the team before you go — we'd rather keep you.",
    f"{IMG}/slider-locations_turf_alysse_torey.jpg",
)

# ============================================================ BUILD ALL
PAGES = [
    ("index.html", "Forma Gym | Walnut Creek &amp; San Jose | Play Every Day", "Two luxury Bay Area fitness clubs — Walnut Creek &amp; San Jose. All group fitness, personal training, pools, cryotherapy, spa and Kidzville.", "", home_body),
    ("about.html", "About Forma Gym | Our Mission &amp; Story", "To make exercise a part of our member's daily lives, for the rest of their lives. Meet Forma Gym — two Bay Area clubs and one community.", "about.html", about_body),
    ("group-fitness.html", "Group Fitness Classes | Forma Gym", "14 group fitness formats included with membership — Cycle, Yoga, Barre, HIIT, Pilates, Dance, TRX, Aqua and more, across Walnut Creek &amp; San Jose.", "group-fitness.html", groupfit_body),
    ("training.html", "Personal Training | Forma Gym", "1-on-1 and small group personal training with the best coaches in the Bay Area. Nutrition guidance, accountability, and a plan built around you.", "training.html", training_body),
    ("recovery.html", "Recovery, Cryotherapy &amp; Cold Plunge | Forma Gym", "Recover like an athlete — cryotherapy, cold plunge, full-service spa, sauna, steam and hot tubs at Forma Gym.", "recovery.html", recovery_body),
    ("cryo.html", "Cryotherapy + Cold Plunge | Forma Gym", "Whole-body cryotherapy and cold plunge at Forma Gym. Burn 500–800 calories per session, reduce pain and inflammation, recover faster.", "", cryo_body),
    ("spa.html", "The Spa at Forma | Massage, Facials, Reiki &amp; Skin Care", "A full-service day spa at Forma Gym — therapeutic massage, facials, Reiki and clinical skin care in Walnut Creek &amp; San Jose.", "", spa_body),
    ("mindbodylab.html", "Mind Body LAB &amp; DrBrainRX | Forma Gym", "Where science meets self-care — brain health, recovery tech, meditation and the mind-body connection at Forma Gym.", "", mbl_body),
    ("kidzville.html", "Kidzville Childcare | Forma Gym Walnut Creek", "Free, safe, active childcare for ages 6 weeks–12 years while you work out. Forma Kidzville at Walnut Creek.", "", kidz_body),
    ("rise.html", "RISE Program | Exercise-Based Therapy for Paralysis | Forma", "RISE is an exercise-based therapy program for individuals living with paralysis. Movement is medicine. Scholarships available.", "", rise_body),
    ("givesback.html", "Forma Gives Back | Fitness for Everyone", "Forma believes fitness should be available to everyone on the spectrum of movement. Learn how Forma Gives Back to the Bay Area.", "", givesback_body),
    ("walnut-creek.html", "Forma Gym Walnut Creek | 1908 Olympic Blvd", "Forma Gym Walnut Creek — 35,000 sq ft of indoor &amp; outdoor fitness, heated pool, Kidzville, cryotherapy, day spa and Café.", "locations.html", walnutcreek_body),
    ("san-jose.html", "Forma Gym San Jose | 5434 Thornwood Dr", "Forma Gym San Jose — 40,000 sq ft luxury facility with covered outdoor turf, heated 6-lane pool, cold plunge and massage services.", "locations.html", sanjose_body),
    ("locations.html", "Locations &amp; Hours | Forma Gym Walnut Creek &amp; San Jose", "Two premium Bay Area clubs. Hours, addresses and amenities for Forma Gym Walnut Creek &amp; San Jose.", "locations.html", locations_body),
    ("join.html", "Join Now | Forma Gym", "Join Forma Gym — all-inclusive access to both Bay Area clubs, every class and recovery amenity.", "", join_body),
    ("trial-pass.html", "Schedule a Visit | Forma Gym", "Schedule a visit, tour or guest workout at Forma Gym, plus a complimentary coaching session.", "", trial_body),
    ("outdoor-training.html", "Outdoor Fitness | Forma Gym", "Strength, cardio, group exercise and cycle — outdoors, year-round, at both Forma Gym clubs.", "", outdoor_body),
    ("drbrainrx.html", "DrBrainRX — GLP-1, Peptides &amp; Longevity | Forma Gym", "GLP-1 weight loss care, peptide therapy and longevity medicine for Forma members through DrBrainRX. 1 month free + $70 off, code FORMAGYM.", "", drbrain_body),
    ("app.html", "The Forma App | Forma Gym", "Book classes, reserve lanes, check schedules and manage your membership with the Forma app.", "", app_body),
    ("merchant.html", "Preferred Merchant Program | Forma Gym", "Forma members get preferred pricing at locally owned Bay Area businesses through our Preferred Merchant Program.", "", merchant_body),
    ("contact.html", "Contact &amp; Book a Tour | Forma Gym", "Book a tour or reach a Forma Gym club — Walnut Creek (925) 932-6400 or San Jose (408) 363-1010.", "", contact_body),
    ("freeze-cancel.html", "Freeze or Cancel Your Membership | Forma Gym", "Active Forma Gym members can request a membership freeze or cancellation. Submit your written request and the membership team will confirm by email.", "", freeze_body),
    ("accessibility.html", "Accessibility Statement | Forma Gym", "Forma Gym is committed to making our clubs and website accessible and welcoming to everyone.", "", accessibility_body),
    ("privacy.html", "Privacy Policy | Forma Gym", "Forma is a SPAM-FREE ZONE — we never share or sell your information.", "", privacy_body),
]

# class detail pages — all 14 formats
_others_pool = [(l, h, d) for l, h, d in ALL_CLASSES]
for slug, title, img, lead, short in CLASS_PAGES:
    others = [o for o in _others_pool if o[1] != f"{slug}.html"][:6]
    PAGES.append((f"{slug}.html", f"{title} | Group Fitness | Forma Gym",
                  f"{title} at Forma Gym — included with membership, all levels welcome.",
                  "group-fitness.html", class_page(slug, title, img, lead, others)))





for fn, title, desc, active, body in PAGES:
    page(fn, title, desc, active, body)

print("\nDone:", len(PAGES), "pages")


# ============================================================ DEPLOY ARTIFACTS
# Files a real host needs. Generated here so they can never drift from the
# page list. `_redirects` in particular MUST sit in the publish root (docs/) —
# Cloudflare Pages / Netlify ignore it anywhere else.
SITE_ORIGIN = "https://formagym.com"


def build_404():
    body = hero(
        "404",
        ["Page not", '<span class="serif">found</span>.'],
        "That page has moved or no longer exists. The links below will get you back on track.",
        img=f"{IMG}/slider-locations_turf_alysse_torey.jpg",
        actions=[("Back to Home", "index.html", True), ("Locations &amp; Hours", "locations.html", False)],
        page=True,
    ) + """
<section class="section section--tight">
  <div class="wrap">
    <div class="rows reveal">
      <a class="row-item" href="group-fitness.html"><span class="row-item__idx">01</span><span class="row-item__title">Group Fitness</span><span class="row-item__desc">Every class included with membership.</span><span class="row-item__arrow">&rarr;</span></a>
      <a class="row-item" href="training.html"><span class="row-item__idx">02</span><span class="row-item__title">Personal Training</span><span class="row-item__desc">Coaching built around your goal.</span><span class="row-item__arrow">&rarr;</span></a>
      <a class="row-item" href="join.html"><span class="row-item__idx">03</span><span class="row-item__title">Join Forma</span><span class="row-item__desc">Two unique Bay Area clubs.</span><span class="row-item__arrow">&rarr;</span></a>
      <a class="row-item" href="contact.html"><span class="row-item__idx">04</span><span class="row-item__title">Contact a Club</span><span class="row-item__desc">Walnut Creek &amp; San Jose.</span><span class="row-item__arrow">&rarr;</span></a>
    </div>
  </div>
</section>
"""
    html = rewrite_urls(head("Page Not Found | Forma Gym", "That page has moved or no longer exists.")
                        + header_html("") + body + footer_html())
    with open(os.path.join(OUT, "404.html"), "w") as f:
        f.write(html)
    print("built /404.html")


def build_sitemap():
    # Only real, indexable pages — one entry per canonical URL.
    paths = sorted({url_for(fn) for fn, *_ in PAGES})
    urls = "".join(f"  <url><loc>{SITE_ORIGIN}{p}</loc></url>\n" for p in paths)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f"{urls}</urlset>\n")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(xml)
    print(f"built /sitemap.xml ({len(paths)} urls)")


def build_robots():
    txt = ("User-agent: *\n"
           "Allow: /\n\n"
           f"Sitemap: {SITE_ORIGIN}/sitemap.xml\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(txt)
    print("built /robots.txt")


def build_headers():
    # Baseline security headers. Worth having on any site; more so after an
    # incident. No CSP here — it needs testing against the inline scripts first.
    txt = """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
"""
    with open(os.path.join(OUT, "_headers"), "w") as f:
        f.write(txt)
    print("built /_headers")


def copy_redirects():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy", "_redirects")
    if not os.path.exists(src):
        print("WARNING: deploy/_redirects missing — run deploy/build_redirects.py")
        return
    with open(src) as f:
        rules = f.read()
    with open(os.path.join(OUT, "_redirects"), "w") as f:
        f.write(rules)
    n = sum(1 for l in rules.splitlines() if l.strip() and not l.startswith("#"))
    print(f"built /_redirects ({n} rules)")


build_404()
build_sitemap()
build_robots()
build_headers()
copy_redirects()

