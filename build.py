#!/usr/bin/env python3
# FORMA GYM — static site generator (Walnut Creek & San Jose)
import os, time

OUT = os.path.join(os.path.dirname(__file__), "docs")
IMG = "assets/img"

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
    return f'<img class="brand__logo {cls}" src="{LOGO}" alt="Forma Gym" width="422" height="37" />'


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
    ("Blog", "blog.html"),
    ("Book a Tour", "contact.html#tour"),
]

# Every group-fitness format gets its own detail page.
# slug, title, img, lead, short (for the group-fitness list)
CLASS_PAGES = [
    ("aqua", "Aqua Studio", "slider-aqua_v3.jpg",
     "A refreshing, low-impact workout in our heated pools. Improve cardiovascular fitness, muscle strength and conditioning with water's natural resistance — ideal for every level, including recovery and joint-friendly training.",
     "Low-impact strength &amp; cardio in heated water"),
    ("barre", "Barre", "slider-locations_group_dance.jpg",
     "Ballet, Pilates and strength training in one elegant burn. Using the barre for support, you'll move through small, isometric movements that target specific muscle groups for a toned, sculpted physique.",
     "Ballet, Pilates &amp; strength for a sculpted body"),
    ("cardio-hiit", "Cardio + HIIT", "annabelle_kettle_HERO_2.jpg",
     "High-energy intervals that torch calories and build serious conditioning. Cardio and HIIT classes alternate bursts of intense effort with active recovery — an efficient, heart-pumping way to get stronger and faster, scaled to every level.",
     "High-intensity intervals that torch calories"),
    ("cycle", "Cycle Studio", "slider-WC_cycle_indoor_v2.jpg",
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
    ("yoga", "Yoga + Mind Body", "yoga_background_2000px_wide.jpg",
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
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Abril+Fatface&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="{LOGO}">
<link rel="stylesheet" href="assets/css/main.css?v={V}">
<script>(function(){{try{{
  if(sessionStorage.getItem("forma-intro"))document.documentElement.classList.add("no-preloader");
  var v=localStorage.getItem("forma-view");
  document.documentElement.setAttribute("data-view", v==="member"?"member":"guest");
  if(v||sessionStorage.getItem("forma-view-skip"))document.documentElement.classList.add("has-view");
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
        menu_links += f'<a href="{href}"><span class="idx">{i:02d}</span>{label}</a>'
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
        <span>Menu</span>
        <span class="menu-toggle__icon"><i></i><i></i></span>
      </button>
    </div>
  </div>
</header>

<div class="menu-overlay" role="dialog" aria-label="Site menu">
  <div class="menu-overlay__grid">
    <nav class="menu-list" aria-label="All pages">{menu_links}</nav>
    <aside class="menu-side">
      <div class="menu-side__pass">
        <p>Summer Special — join now &amp; your first <em>2 weeks are free</em>. Come Play Every Day.</p>
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
        <div class="socials">
          <a href="https://www.instagram.com/formagym" aria-label="Instagram">IG</a>
          <a href="https://www.facebook.com/formagym" aria-label="Facebook">FB</a>
          <a href="https://www.youtube.com/" aria-label="YouTube">YT</a>
          <a href="https://www.tiktok.com/" aria-label="TikTok">TT</a>
        </div>
      </div>
      <div>
        <h5>Move</h5>
        <div class="site-footer__links">
          <a href="group-fitness.html">Group Fitness</a>
          <a href="blog.html">Blog</a>
          <a href="training.html">Personal Training</a>
          <a href="cycle.html">Cycle</a>
          <a href="yoga.html">Yoga + Mind Body</a>
          <a href="pilates-reformer.html">Pilates Reformer</a>
          <a href="trx.html">TRX&reg;</a>
          <a href="aqua.html">Aqua</a>
        </div>
      </div>
      <div>
        <h5>Recover &amp; More</h5>
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
        <a class="tel" href="tel:4083631010" style="margin-top:14px">San Jose</a>
        <a href="san-jose.html">5434 Thornwood Dr · (408) 363-1010</a>
        <form class="news-form" data-demo>
          <input type="email" placeholder="Join our newsletter" aria-label="Email address" required>
          <button type="submit">Join</button>
        </form>
      </div>
    </div>
  </div>
  <div class="site-footer__mega" aria-hidden="true">FORMA</div>
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
         actions=None, meta=None, page=False):
    lns = ""
    for i, ln in enumerate(lines):
        lns += f'<span class="ln"><span style="transition-delay:{0.12 + i * 0.09:.2f}s">{ln}</span></span>'
    media = ""
    if video:
        media = f'<video src="{video}" poster="{poster or ""}" autoplay muted loop playsinline></video>'
    elif img:
        media = f'<img src="{img}" alt="" fetchpriority="high">'
    acts = ""
    if actions:
        acts = '<div class="hero__actions">'
        for a in actions:
            label, href, solid = a[0], a[1], a[2]
            extra = (" " + a[3]) if len(a) > 3 else ""
            cls = ("btn btn--solid" if solid else "btn") + extra
            acts += f'<a class="{cls}" href="{href}">{label} <span class="arr">→</span></a>'
        acts += "</div>"
    crumb_html = ""
    if crumb:
        crumb_html = f'<div class="hero__crumb"><div><a href="index.html">Home</a> &nbsp;/&nbsp; {crumb}</div></div>'
    meta_html = ""
    if meta:
        meta_html = '<div class="hero__meta">' + "".join(f"<span>{m}</span>" for m in meta) + "</div>"
    sub_html = f'<p class="hero__sub">{sub}</p>' if sub else ""
    return f"""
<section class="hero{' hero--page' if page else ''}">
  <div class="hero__media">{media}</div>
  {crumb_html}
  <div class="hero__inner">
    <p class="hero__kicker">{kicker}</p>
    <h1 class="hero__title">{lns}</h1>
    {sub_html}
    {acts}
  </div>
  {meta_html}
  <div class="hero__scroll" aria-hidden="true"></div>
</section>
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
<section class="section--flush{' section--light' if light else ''}">
  <div class="stats"><div class="wrap" style="padding:0"><div class="stats__grid">{cells}</div></div></div>
</section>
"""


def split(eyebrow, num, title, paras, img, alt, rev=False, cta=None, tag=None, light=False, wide=False):
    body_paras = "".join(f'<p class="body-copy">{p}</p>' for p in paras)
    cta_html = f'<div class="split__cta"><a class="inline-link" href="{cta[1]}">{cta[0]} →</a></div>' if cta else ""
    tag_html = f'<span class="tag">{tag}</span>' if tag else ""
    return f"""
<section class="section{' section--light' if light else ''}">
  <div class="wrap">
    <div class="split{' split--rev' if rev else ''}">
      <div class="split__media{' split__media--wide' if wide else ''} reveal-img">
        <img src="{img}" alt="{alt}" loading="lazy">{tag_html}
      </div>
      <div class="split__body">
        <p class="eyebrow"><span class="num">{num}</span> {eyebrow}</p>
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


def form_section(sec_id, num, eyebrow, title_html, text, btn, light=True, extra=""):
    fields = [("text", "first", "First name"), ("text", "last", "Last name"),
              ("email", "email", "Email address"), ("tel", "phone", "Phone")]
    f_html = ""
    for ftype, name, label in fields:
        f_html += f"""
        <div class="field"><input type="{ftype}" name="{name}" id="{sec_id}-{name}" placeholder=" " required><label for="{sec_id}-{name}">{label}</label></div>"""
    return f"""
<section class="section{' section--light' if light else ''}" id="{sec_id}">
  <div class="wrap">
    <div class="intro-grid">
      <div>
        <p class="eyebrow"><span class="num">{num}</span> {eyebrow}</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">{title_html}</h2>
        <p class="lede reveal" style="margin-top:28px">{text}</p>
        {extra}
      </div>
      <div class="intro-grid__right reveal">
        <form class="form-grid" data-demo>
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
        </form>
        <p class="form-note">By submitting, you confirm you're at least 13 and agree to our Privacy Policy &amp; Terms. Forma is a SPAM-FREE ZONE — we never share or sell your info.</p>
      </div>
    </div>
  </div>
</section>
"""


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


def page(filename, title, desc, active, body):
    html = head(title, desc) + header_html(active) + body + footer_html()
    with open(os.path.join(OUT, filename), "w") as f:
        f.write(html)
    print("built", filename)


# ============================================================ shared blocks
view_chooser = f"""
<div class="view-chooser" role="dialog" aria-label="Choose your experience">
  <button class="vc-skip" type="button">Just browsing →</button>
  <div class="view-chooser__head">
    <span class="kicker">Welcome to Forma Gym</span>
    <h2>How are you visiting today?</h2>
  </div>
  <div class="view-chooser__panels">
    <button class="vc-panel" type="button" data-choose="guest">
      <img src="{IMG}/annabelle_kettle_HERO_2.jpg" alt="">
      <div class="vc-panel__body">
        <span class="vc-panel__kicker">First time here?</span>
        <h3>I'm a <span class="serif">guest</span></h3>
        <p>Tour a club, explore classes, and start with two free weeks.</p>
        <span class="go">Show me around →</span>
      </div>
    </button>
    <button class="vc-panel" type="button" data-choose="member">
      <img src="{IMG}/slider-WC_cycle_indoor_v2.jpg" alt="">
      <div class="vc-panel__body">
        <span class="vc-panel__kicker">Welcome back</span>
        <h3>I'm a <span class="serif">member</span></h3>
        <p>Class schedules, club hours, Kidzville and your member perks.</p>
        <span class="go">Take me in →</span>
      </div>
    </button>
  </div>
</div>
"""

member_strip = """
<div class="member-strip only-member">
  <div class="wrap">
    <span class="hello">Welcome back.</span>
    <a href="group-fitness.html#schedule">Class Schedules</a>
    <a href="recovery.html">Recovery &amp; Cryo</a>
    <a href="spa.html">Book the Spa</a>
    <a href="kidzville.html">Kidzville</a>
    <a href="walnut-creek.html">Walnut Creek</a>
    <a href="san-jose.html">San Jose</a>
  </div>
</div>
"""


# ============================================================ HOME
home_body = view_chooser + hero(
    "Walnut Creek &amp; San Jose · Est. 2009",
    ["Play", '<span class="serif">every</span> day'],
    "Two luxury Bay Area clubs built around one idea: make movement the best part of your day. World-class instructors, resort-style amenities, and a community that actually feels like one.",
    video="assets/video/forma-hero.mp4",
    poster=f"{IMG}/forma-hero-poster.jpg",
    actions=[
        ("Start 2 Weeks Free", "join.html", True, "only-guest"),
        ("Explore the Clubs", "locations.html", False, "only-guest"),
        ("Class Schedule", "group-fitness.html#schedule", True, "only-member"),
        ("Book Recovery", "recovery.html", False, "only-member"),
    ],
    meta=["2 Bay Area locations", "75,000+ sq ft of fitness", "All classes included"],
) + member_strip + marquee(
    ["Group Fitness", "Personal Training", "Cycle", "Yoga", "Pilates Reformer", "Aqua", "Cryotherapy", "The Spa", "Kidzville"]
) + f"""
<section class="section">
  <div class="wrap">
    <div class="intro-grid">
      <div>
        <p class="eyebrow"><span class="num">01</span> Our mission</p>
        <h2 class="h-display reveal">Fitness that becomes part of your <span class="serif">life</span></h2>
      </div>
      <div class="intro-grid__right">
        <p class="lede reveal">"To make exercise a part of our member's daily lives, for the rest of their lives." That's the whole point of Forma.</p>
        <p class="body-copy reveal">From luxury amenities to the industry's best instructors, we give you a safe, motivating space to show up and Play Every Day. Two unique Bay Area locations. A holistic approach to fitness. Modern, cutting-edge design with an authentic community feel.</p>
        <div class="reveal"><a class="inline-link" href="about.html">The Forma story →</a></div>
      </div>
    </div>
  </div>
</section>
""" + stats_band([
    (2, "", "Bay Area clubs, one membership"),
    (75, "K+", "Square feet of indoor + outdoor fitness"),
    (14, "", "Group fitness formats, all included"),
    (2, "wks", "Free when you join this summer"),
]) + f"""
<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow"><span class="num">02</span> Find your movement</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Every way to <span class="serif">play</span></h2>
      </div>
      <a class="inline-link reveal" href="group-fitness.html">View all classes →</a>
    </div>
    <div class="card-grid" data-stagger>
      <a class="card" href="group-fitness.html"><div class="card__media"><img src="{IMG}/slider-locations_group_dance.jpg" alt="Group fitness class" loading="lazy"><span class="card__num">01</span><div class="card__label"><h3>Group<br>Fitness</h3><span class="go">Explore →</span></div></div></a>
      <a class="card" href="training.html"><div class="card__media"><img src="{IMG}/jason_johnson_turf2.jpg" alt="Personal training" loading="lazy"><span class="card__num">02</span><div class="card__label"><h3>Personal<br>Training</h3><span class="go">Explore →</span></div></div></a>
      <a class="card" href="cycle.html"><div class="card__media"><img src="{IMG}/slider-WC_cycle_indoor_v2.jpg" alt="Cycle studio" loading="lazy"><span class="card__num">03</span><div class="card__label"><h3>Cycle</h3><span class="go">Explore →</span></div></div></a>
      <a class="card" href="recovery.html"><div class="card__media"><img src="{IMG}/Forma_WalnutCreek_locations_cryo.jpg" alt="Forma cryotherapy chamber" loading="lazy"><span class="card__num">04</span><div class="card__label"><h3>Recovery<br>&amp; Cryo</h3><span class="go">Explore →</span></div></div></a>
      <a class="card" href="aqua.html"><div class="card__media"><img src="{IMG}/slider-aqua_v3.jpg" alt="Aqua studio" loading="lazy"><span class="card__num">05</span><div class="card__label"><h3>Aqua</h3><span class="go">Explore →</span></div></div></a>
      <a class="card" href="spa.html"><div class="card__media"><img src="{IMG}/Forma_Walnut-Creek_Spa_Header_2018.jpg" alt="The spa" loading="lazy"><span class="card__num">06</span><div class="card__label"><h3>The<br>Spa</h3><span class="go">Explore →</span></div></div></a>
    </div>
  </div>
</section>
""" + marquee(["35,000 sq ft in Walnut Creek", "40,000 sq ft in San Jose", "Heated outdoor pools", "Covered outdoor turf"], ghost=True) + split(
    "Two clubs, one membership", "03",
    'Walnut <span class="serif">Creek</span>',
    ["The birthplace of Forma since 2009. Right off the 680/24 corridor and completely renovated — 35,000 square feet of indoor and outdoor fitness motivation, a heated outdoor lap pool under towering redwoods, onsite Kidzville, cryotherapy, a full-service day spa and the Forma Café.",
     "Open Monday–Thursday 5am–11pm, Friday 5am–10pm, weekends 6am–8pm. 1908 Olympic Blvd, Walnut Creek."],
    f"{IMG}/formaWC_facade_bkgrnd.jpg",
    "Forma Gym Walnut Creek facade",
    cta=("Explore Walnut Creek", "walnut-creek.html"), tag="Since 2009",
) + split(
    "Two clubs, one membership", "04",
    'San <span class="serif">Jose</span>',
    ["Serving South San Jose since 2015. A 40,000 sq. ft. luxury facility with an 8,000 sq. ft. covered outdoor fitness area — cardio, strength, group fitness, a heated 6-lane junior olympic pool with hot tub, and full-service locker rooms with sauna, steam and a Chilly Goat® cold plunge.",
     "Open Monday–Thursday 5am–11pm, Friday 5am–10pm, weekends 6am–8pm. 5434 Thornwood Dr, San Jose."],
    f"{IMG}/formaSJ_facade_bkgrnd4.jpg",
    "Forma Gym San Jose facade",
    rev=True, cta=("Explore San Jose", "san-jose.html"), tag="Since 2015",
) + f"""
<section class="section section--light">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow"><span class="num">05</span> Recover like an athlete</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Wellness, <span class="serif">elevated</span></h2>
      </div>
      <a class="inline-link reveal" href="recovery.html">More recovery →</a>
    </div>
    <div class="card-grid card-grid--2" data-stagger>
      <div class="card"><div class="card__media card__media--wide"><img src="{IMG}/chillyGOAT_SJ_500px.jpg" alt="Chilly Goat cold plunge" loading="lazy"><div class="card__label"><h3>Cryotherapy + Cold Plunge</h3></div></div><div class="card__below"><p>Burn 500–800 calories in a single 3-minute session, reduce inflammation and pain, heal injuries faster, and sleep better. A natural, non-invasive reset trusted by Olympic and pro athletes — and now part of your club.</p></div></div>
      <div class="card"><div class="card__media card__media--wide"><img src="{IMG}/Forma_Walnut-Creek_Spa_Header_2018.jpg" alt="The Spa" loading="lazy"><div class="card__label"><h3>The Full-Service Day Spa</h3></div></div><div class="card__below"><p>Massage, facials and clinical skin care from skilled therapists — steps from the sauna, steam and hot tub. Restore, rejuvenate and walk out feeling like a brand new person.</p></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow"><span class="num">06</span> More than a gym</p>
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
    'Your first <span class="serif">two weeks</span> are free',
    "Summer Special — join now and the first two weeks are on us. Tour a club, take a class, hit the spa. Come see why Forma members never want to leave.",
    f"{IMG}/slider-locations_turf_alysse_torey.jpg",
)

# ============================================================ ABOUT
about_body = hero(
    "About Forma Gym",
    ["More than a gym.", 'A <span class="serif">way to live</span>.'],
    "“To make exercise a part of our member's daily lives, for the rest of their lives.” That mission has driven everything we've built since 2009.",
    img=f"{IMG}/slider-locations_turf_alysse_torey.jpg",
    crumb="About",
    actions=[("Book a Tour", "contact.html#tour", True)],
    page=True,
) + f"""
<section class="section section--tight">
  <div class="wrap">
    <div class="intro-grid">
      <div>
        <p class="eyebrow"><span class="num">01</span> Our mission</p>
        <h2 class="h-display reveal">Movement, for <span class="serif">life</span></h2>
      </div>
      <div class="intro-grid__right">
        <p class="lede reveal">The goal at Forma has always been to create a community where fitness and health is available to EVERYONE on the spectrum of movement — from those struggling just to stand, to world-class athletes.</p>
        <p class="body-copy reveal">We're very proud of what we've created, and we love our Members, our Team, our Community — and we LOVE being here for you. That's not a slogan. It's how the clubs feel the moment you walk in.</p>
      </div>
    </div>
  </div>
</section>
""" + marquee(["Play Every Day", "Embrace Change", "Life is Good", "Be an Adventure"], accent=True) + f"""
<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow"><span class="num">02</span> Our core values</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">What we live <span class="serif">by</span></h2>
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
    cta=("Visit a club", "locations.html"), tag="The Forma Family",
) + form_section(
    "tour", "04", "Book a tour",
    'Come see it for <span class="serif">yourself</span>',
    "Join the Forma Family and experience how we can help you — featuring the best trainers, programs and classes in the Bay Area. Tell us a little about you and we'll set up your visit.",
    "Book My Tour",
) + cta_band(
    'Come <span class="serif">play</span> with us',
    "Two clubs, two free weeks, one community that can't wait to meet you.",
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
    actions=[("Start 2 Weeks Free", "join.html", True), ("Book a Tour", "contact.html#tour", False)],
    meta=["14 class formats", "All included in membership", "Indoor + outdoor studios"],
    page=True,
) + marquee(["Cycle", "Yoga", "Barre", "HIIT", "Pilates", "Dance", "TRX", "Aqua", "Kickboxing", "Sculpt", "Meditation"]) + f"""
<section class="section" id="classes">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow"><span class="num">01</span> The full lineup</p>
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
    rev=True, cta=("See the locations", "locations.html"), tag="Indoor + Outdoor",
) + form_section(
    "schedule", "03", "Schedule a visit",
    'Find your first <span class="serif">class</span>',
    "Join the Forma Family and experience the difference — featuring the best trainers, programs and classes in the Bay Area. Tell us your preferred club and we'll get you on the schedule.",
    "Get the Schedule",
) + cta_band(
    'Your first <span class="serif">two weeks</span> are free',
    "Come try a class — or five. Every format is included, and the first two weeks are on us.",
    f"{IMG}/slider-kickbox_v3.jpg",
)

# ============================================================ TRAINING
training_body = hero(
    "Personal Training",
    ["Your goal.", 'Our <span class="serif">obsession</span>.'],
    "A team of fitness professionals with diverse backgrounds, deep experience, and a shared passion for health and wellness. We'll meet you where you are and build the plan that gets you where you want to be.",
    img=f"{IMG}/annabelle_kettle_HERO_2.jpg",
    crumb="Training",
    actions=[("Book a Free Consult", "contact.html#tour", True), ("Meet the Team", "#team", False)],
    meta=["1-on-1 &amp; small group", "Nutrition guidance included", "Both clubs"],
    page=True,
) + f"""
<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="split__media reveal-img"><img src="{IMG}/jason_johnson_turf2.jpg" alt="1 on 1 personal training" loading="lazy"><span class="tag">1-on-1</span></div>
      <div class="split__body">
        <p class="eyebrow"><span class="num">01</span> One-on-one personal training</p>
        <h2 class="h-display" style="font-size:clamp(30px,3.8vw,58px)">A plan built around <span class="serif">you</span></h2>
        <ul class="checklist reveal" style="margin-top:10px">
          <li>Assess where you are now and where to start</li>
          <li>Nutritional consultation &amp; guidance — understand the power of food</li>
          <li>Education on movement technique and equipment — master your exercise</li>
          <li>The perfect strategy for your individual goals</li>
          <li>Accountability for your fitness journey</li>
          <li>Learn to repair and recover, and keep your work/life balance</li>
        </ul>
        <div class="split__cta"><a class="inline-link" href="contact.html#tour">Book a free consult →</a></div>
      </div>
    </div>
  </div>
</section>
""" + split(
    "Small group training", "02",
    'The best of both <span class="serif">worlds</span>',
    ["Small Group Training brings 4–8 people together with one trainer — the energy and accountability of community, with the attention and programming of personal training.",
     "It's affordable, it's motivating, and the workouts change constantly so you never plateau or get bored."],
    f"{IMG}/Darlene_ropes2.jpg",
    "Small group training at Forma",
    rev=True, cta=("Ask about small group", "contact.html#tour"), tag="4–8 people",
) + f"""
<section class="section section--light" id="team">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow"><span class="num">03</span> Meet our training team</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Coaches who <span class="serif">care</span></h2>
      </div>
      <p class="body-copy reveal" style="max-width:34ch">Years of experience, a range of specialties, and a genuine passion for helping you feel strong, confident and excited about fitness.</p>
    </div>
    {accordion([
        ("Dave — Fitness Coach", "<strong>Specialties:</strong> Athletic Performance · Movement Assessment · Program Development · Weightlifting · Exercise Therapy.<br><br>“Your happiness is your health. The world is best experienced with high energy, low pain, and high function. Physical activity is a source of great joy — find your motivation and stay active.”"),
        ("Montana — Fitness Coach", "<strong>Specialties:</strong> Weight Lifting · Strength Training · Athletic Performance · Functional Movement · Nutrition Coaching · Weight Loss Management.<br><br>“Consistency is more important than perfection. I love helping people feel comfortable in their own skin while building long-lasting, healthy habits.”"),
        ("Jason — Fitness Coach", "<strong>Specialties:</strong> Creative Movement · Interval Training · Kickboxing.<br><br>After losing 50 lbs and reversing his hypertension, Jason made it his life goal to change the lives of others. “Everything should feel good, from start to finish.”"),
        ("Marco — Fitness Coach", "<strong>Specialties:</strong> Cross Training · Bodybuilding · Muscle Definition &amp; Development.<br><br>A coach who blends serious strength knowledge with the patience to teach it — helping clients build the physique and the confidence to match."),
    ], open_first=False)}
  </div>
</section>
""" + cta_band(
    'Train with the <span class="serif">best</span> in the Bay',
    "Book a free consultation, tell us your goal, and we'll pair you with the coach who's right for you.",
    f"{IMG}/Dave2.jpg",
)

# ============================================================ LOCATIONS
locations_body = hero(
    "Locations &amp; Hours",
    ["Two clubs.", 'One <span class="serif">membership</span>.'],
    "Walnut Creek and San Jose — both premium, both all-inclusive, both yours with a single membership. Find your home club below.",
    img=f"{IMG}/Forma_WalnutCreek_locations_pool_birdeye-2.jpg",
    crumb="Locations",
    actions=[("Start 2 Weeks Free", "join.html", True)],
    page=True,
) + f"""
<section class="section">
  <div class="wrap">
    <div class="loc">
      <div class="loc-item">
        <div class="loc-item__media reveal-img"><img src="{IMG}/formaWC_facade_bkgrnd.jpg" alt="Forma Walnut Creek" loading="lazy"></div>
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
        <div class="loc-item__media reveal-img"><img src="{IMG}/formaSJ_facade_bkgrnd4.jpg" alt="Forma San Jose" loading="lazy"></div>
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
    (1, "", "Membership covers both"),
    (75, "K+", "Combined square feet"),
    (14, "", "Group fitness formats"),
]) + cta_band(
    'Find your <span class="serif">home club</span>',
    "Both locations are all-inclusive — every class, the pools, the recovery suites. Start with two free weeks at whichever is closest.",
    f"{IMG}/pool_sunset_SJ_500px.jpg",
)


def location_page(name, badge, phone, tel, address, intro, amenities, hero_img, gallery_imgs, hours):
    am = "".join(f"<li>{a}</li>" for a in amenities)
    g = ""
    cls = ["g-item--a", "g-item--b", "g-item--c"]
    for i, im in enumerate(gallery_imgs[:3]):
        g += f'<div class="g-item {cls[i]} reveal-img"><img src="{IMG}/{im}" alt="{name}" loading="lazy"></div>'
    hrs = "".join(f'<div><dt>{d}</dt><dd>{h}</dd></div>' for d, h in hours)
    return hero(
        f"Forma {name}", [name.split()[0], f'<span class="serif">{name.split()[-1] if len(name.split())>1 else "Club"}</span>'],
        intro, img=f"{IMG}/{hero_img}", crumb=f'<a href="locations.html">Locations</a> &nbsp;/&nbsp; {name}',
        actions=[("Start 2 Weeks Free", "join.html", True), (f"Call {phone}", f"tel:{tel}", False)],
        meta=[badge], page=True,
    ) + f"""
<section class="section section--tight">
  <div class="wrap">
    <div class="intro-grid">
      <div>
        <p class="eyebrow"><span class="num">01</span> What's inside</p>
        <h2 class="h-display reveal">Premium spaces, <span class="serif">all-inclusive</span></h2>
        <address style="font-style:normal;color:var(--muted);margin-top:22px;line-height:1.8;font-size:15.5px">{address}<br><a href="tel:{tel}" style="color:var(--accent)">{phone}</a></address>
        <div class="loc-hours" style="max-width:340px;margin-top:20px">{hrs}</div>
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
        "Book a tour or jump straight in with two free weeks. Every class and amenity, included.",
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
    "formaWC_facade_bkgrnd.jpg",
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
    "formaSJ_facade_bkgrnd4.jpg",
    ["pool_sunset_SJ_500px.jpg", "SJ_gym_floor_HERO_gradient-scaled.jpg", "SJ_pool_662x501_v1.jpg"],
    [("Mon–Thu", "5am – 11pm"), ("Friday", "5am – 10pm"), ("Sat–Sun", "6am – 8pm")],
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
    cta=("All about cryo", "cryo.html"), tag="Chilly Goat®",
) + split(
    "The spa", "02",
    'The optimum wellness <span class="serif">experience</span>',
    ["A comprehensive menu of therapeutic treatments — massage, facials and clinical skin care — performed by skilled, professional therapists dedicated to easing pain, restoring function and rejuvenating face and body.",
     "Conveniently located adjacent to the locker rooms, so sauna, steam or Jacuzzi can be enjoyed before or after your treatment."],
    f"{IMG}/Forma_Walnut-Creek_Spa_Header_2018.jpg",
    "The Spa at Forma",
    rev=True, cta=("See spa menu &amp; pricing", "spa.html"), tag="Day Spa",
) + split(
    "Mind Body LAB", "03",
    'Where science meets <span class="serif">self-care</span>',
    ["Our Mind Body LAB brings together recovery technology, brain health and the mind-body connection — including DrBrainRX — to help you feel as good mentally as you do physically.",
     "Because true wellness isn't just how you move. It's how you think, recover, and feel."],
    f"{IMG}/slider-meditate_v2.jpg",
    "Mind Body LAB at Forma",
    cta=("Explore the LAB", "mindbodylab.html"), tag="Mind Body LAB",
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
        <p class="eyebrow"><span class="num">01</span> The benefits</p>
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
    rev=True, tag="-195°F",
) + f"""
<section class="section section--light">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow"><span class="num">03</span> Real members, real results</p>
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
""" + cta_band(
    'Book your first <span class="serif">session</span>',
    "Three minutes to less pain, better sleep, and faster recovery. Members and guests welcome.",
    f"{IMG}/chillyGOAT_SJ_500px.jpg",
    primary=("Book a Session", "contact.html#tour"),
)

# ============================================================ SPA
spa_body = hero(
    "The Spa",
    ["Pause.", '<span class="serif">Restore.</span>'],
    "A comprehensive menu of therapeutic treatments — massage, facials and clinical skin care — in a cozy, luxurious setting steps from the sauna, steam and Jacuzzi. Skilled therapists dedicated to easing pain and rejuvenating face and body.",
    img=f"{IMG}/Forma_Walnut-Creek_Spa_Header_2018.jpg",
    crumb="The Spa",
    actions=[("Book a Treatment", "tel:9259326400", True)],
    meta=["Massage · facials · skin care", "Walnut Creek &amp; San Jose"],
    page=True,
) + f"""
<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow"><span class="num">01</span> Massage</p>
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

<section class="section section--light">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow"><span class="num">02</span> Skincare</p>
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
    cta=("Ask us about DrBrainRX", "contact.html#tour"), tag="DrBrainRX",
) + split(
    "Meditation + breathwork", "02",
    'Find your <span class="serif">stillness</span>',
    ["Our meditation and breathwork classes offer a structured, peaceful space to reduce stress and build mental clarity — guided by experienced instructors, suitable for everyone from first-timers to seasoned practitioners.",
     "Reset your nervous system, then carry that calm into the rest of your day."],
    f"{IMG}/slider-meditate_v2.jpg",
    "Meditation class at Forma",
    rev=True, cta=("See the class lineup", "group-fitness.html#classes"), tag="GroupFit",
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
        <p class="eyebrow"><span class="num">01</span> Safe · active · educational</p>
        <h2 class="h-display reveal">Where kids actually want to <span class="serif">be</span></h2>
      </div>
      <div class="intro-grid__right">
        <p class="lede reveal">We offer you the time and space to break free from family responsibilities for a little while — to socialize and work out — while our reliable, capable staff helps your kids enjoy plenty of play and learning.</p>
        <p class="body-copy reveal">Forma Kidzville was created to provide a safe, stimulating and playful environment where children and preteens are free to learn, explore, experiment, and be active, imaginative and creative. We incorporate innovative games and activities — giving your child the chance to participate with groups, pursue individual interests, or just play with old and new friends.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--light" id="hours">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow"><span class="num">02</span> Kidzville hours</p>
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
        <p class="eyebrow"><span class="num">01</span> What RISE delivers</p>
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

<section class="section section--light" id="method">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow"><span class="num">02</span> Our methodology</p>
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
) + split(
    "Our belief", "01",
    'A community for <span class="serif">all</span>',
    ["We're very proud of what we've created, and we love our Members, our Team, and our Community. That love shows up in how we give back — making space, programs and scholarships available to people who need them most.",
     "The RISE Program's scholarship fund, accessible programming, and local partnerships are all part of how Forma shows up for the Bay Area."],
    f"{IMG}/slider-locations_turf_alysse_torey.jpg",
    "Forma community giving back",
    cta=("Learn about RISE", "rise.html"), tag="Community",
) + cta_band(
    'Play it <span class="serif">forward</span>',
    "Want to get involved, donate, or nominate someone for a scholarship? We'd love to hear from you.",
    f"{IMG}/slider-locations_group_dance.jpg",
    primary=("Get Involved", "contact.html#tour"),
)

# ============================================================ CLASS DETAIL PAGES
def class_page(slug, title, img, lead, others):
    other_cards = ""
    for ol, oh, od in others:
        other_cards += f'<a class="row-item" href="{oh}"><span class="row-item__idx">→</span><span class="row-item__title">{ol}</span><span class="row-item__desc">{od}</span><span class="row-item__arrow">→</span></a>'
    return hero(
        "Group Fitness", [title.split()[0], f'<span class="serif">{" ".join(title.split()[1:]) or "Studio"}</span>'] if len(title.split()) > 1 else [f'<span class="serif">{title}</span>'],
        lead, img=f"{IMG}/{img}", crumb=f'<a href="group-fitness.html">Group Fitness</a> &nbsp;/&nbsp; {title}',
        actions=[("Start 2 Weeks Free", "join.html", True), ("Full Schedule", "group-fitness.html#schedule", False)],
        meta=["Included with membership", "All levels welcome"], page=True,
    ) + f"""
<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow"><span class="num">01</span> More ways to move</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Mix it <span class="serif">up</span></h2>
      </div>
      <a class="inline-link reveal" href="group-fitness.html">All 14 classes →</a>
    </div>
    <div class="rows reveal">{other_cards}</div>
  </div>
</section>
""" + cta_band(
        f'Try {title.split()[0]} <span class="serif">free</span>',
        "Every class is included with membership — and your first two weeks are on us. Come find your format.",
        f"{IMG}/{img}",
    )


# ============================================================ JOIN
join_body = hero(
    "Join Forma Online",
    ["Join in", '<span class="serif">minutes</span>'],
    'Pick your club, choose your membership, and you\'re in. Right now: <strong>$0 enrollment + your first two weeks free.</strong> <em>Must be 18+ to join without a parent or guardian.</em>',
    img=f"{IMG}/gym_floor_WC_500px.jpg",
    crumb="Join Now",
    actions=[("Start My Membership", "#wizard", True), ("Book a Tour Instead", "contact.html#tour", False)],
    meta=["$0 enrollment", "First 2 weeks free", "Cancel after minimum term"],
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
              <button class="choice" type="button" data-club="Walnut Creek" data-img="{IMG}/formaWC_facade_bkgrnd.jpg">
                <span class="choice__chip">Since 2009</span><span class="choice__check">✓</span>
                <div class="choice__img"><img src="{IMG}/formaWC_facade_bkgrnd.jpg" alt="Walnut Creek" loading="lazy"></div>
                <h3>Forma Walnut Creek</h3>
                <p class="meta">1908 Olympic Blvd · 35,000 sq ft</p>
                <ul class="choice__perks"><li>Complimentary Fitness Consultation</li><li>Complimentary Nutrition Consultation</li><li>30-Day Money-Back Guarantee</li></ul>
              </button>
              <button class="choice" type="button" data-club="San Jose" data-img="{IMG}/formaSJ_facade_bkgrnd4.jpg">
                <span class="choice__chip">Since 2015</span><span class="choice__check">✓</span>
                <div class="choice__img"><img src="{IMG}/formaSJ_facade_bkgrnd4.jpg" alt="San Jose" loading="lazy"></div>
                <h3>Forma San Jose</h3>
                <p class="meta">5434 Thornwood Dr · 40,000 sq ft</p>
                <ul class="choice__perks"><li>Complimentary Fitness Consultation</li><li>Complimentary Nutrition Consultation</li><li>30-Day Money-Back Guarantee</li></ul>
              </button>
            </div>
          </div>

          <div class="join-step" data-step="2">
            <h2 class="join-step__title">Choose your <span class="serif">membership</span></h2>
            <p class="join-step__hint">Select the plan that fits your fitness goals.</p>
            <div class="join-promo">JOIN NOW — $0 ENROLLMENT + 1ST TWO WEEKS FREE</div>
            <div class="plan-grid">
              <button class="plan-card" type="button" data-plan="Premier" data-primary="215" data-addl="160" data-enroll="350">
                <span class="plan-card__chip">Most Popular</span><span class="choice__check">✓</span>
                <h3>Premier Membership</h3>
                <div class="plan-card__price">$215<small>/mo</small></div>
                <p class="plan-card__fee"><s>$350 enrollment</s> &nbsp;$0 today</p>
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
                <p class="plan-card__fee"><s>$350 enrollment</s> &nbsp;$0 today</p>
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
            <p class="join-step__foot">Both plans include a complimentary Formation Session. 12-month commitment with monthly billing; cancel anytime after the minimum term with 30-day notice.</p>
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
            <p class="join-step__hint">With the Summer Special, enrollment is $0 and your first two weeks are free — your first monthly payment comes after.</p>
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
            <label class="review-agree"><input type="checkbox" id="agree"><span>I'm 18+ (or joining with a parent/guardian), I agree to the <a href="contact.html">Terms of Service</a> and <a href="privacy.html">Privacy Policy</a>, and I understand this is a 12-month commitment with monthly billing, cancellable after the minimum term with 30-day notice. This is a design demo — no payment will be processed.</span></label>
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
          <p class="sum-note">$0 enrollment &amp; first two weeks free with the Summer Special. Monthly billing begins after your free weeks.</p>
          <span class="sum-badge">30-Day Money-Back Guarantee</span>
        </div>
      </aside>
    </div>
  </div>
</section>

<div class="join-success" role="dialog" aria-modal="true" aria-label="Membership confirmed">
  <div class="join-success__inner">
    <div class="mark">✓</div>
    <h2 data-success-name>Welcome to the Forma Family.</h2>
    <p>Your membership request is in. Because this is a design demo, no payment was processed — on the live site you'd be all set to walk in and start your two free weeks. Time to Play Every Day.</p>
    <div class="hero__actions">
      <a class="btn btn--solid" href="index.html">Back to Home <span class="arr">→</span></a>
      <a class="btn" href="group-fitness.html">Browse Classes <span class="arr">→</span></a>
    </div>
  </div>
</div>
<script src="assets/js/join.js?v={V}" defer></script>
""" + cta_band(
    'Questions before you <span class="serif">join?</span>',
    "Book a free tour and we'll show you around, answer everything, and help you pick the right membership.",
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
    "Book My Tour", light=True,
) + f"""
<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow"><span class="num">02</span> Two locations</p>
        <h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">Reach a <span class="serif">club</span></h2>
      </div>
    </div>
    <div class="card-grid card-grid--2" data-stagger>
      <div class="card"><div class="card__media card__media--wide"><img src="{IMG}/formaWC_facade_bkgrnd.jpg" alt="Walnut Creek" loading="lazy"><div class="card__label"><h3>Walnut Creek</h3></div></div><div class="card__below"><p>1908 Olympic Blvd, Walnut Creek, CA 94596<br><a href="tel:9259326400" style="color:var(--accent)">(925) 932-6400</a><br>Mon–Thu 5am–11pm · Fri 5am–10pm · Sat–Sun 6am–8pm</p></div></div>
      <div class="card"><div class="card__media card__media--wide"><img src="{IMG}/formaSJ_facade_bkgrnd4.jpg" alt="San Jose" loading="lazy"><div class="card__label"><h3>San Jose</h3></div></div><div class="card__below"><p>5434 Thornwood Dr, San Jose, CA 95123<br><a href="tel:4083631010" style="color:var(--accent)">(408) 363-1010</a><br>Mon–Thu 5am–11pm · Fri 5am–10pm · Sat–Sun 6am–8pm</p></div></div>
    </div>
  </div>
</section>
""" + cta_band(
    'Two free weeks are <span class="serif">waiting</span>',
    "Ready when you are. Join online in minutes, or book a tour and let us show you around.",
    f"{IMG}/slider-locations_turf_alysse_torey.jpg",
)

# ============================================================ TRIAL PASS
trial_body = hero(
    "Schedule Your Visit",
    ["Try Forma.", 'First two weeks <span class="serif">free</span>.'],
    "Fill out the form below to schedule a visit, a tour, and/or a guest workout — and take advantage of our Summer Special. $0 enrollment and a free fitness coaching session.",
    img=f"{IMG}/annabelle_kettle_HERO_2.jpg",
    crumb="Trial Pass",
    actions=[("Schedule My Visit", "#tour", True), ("Join Online", "join.html", False)],
    meta=["First 2 weeks free", "$0 enrollment", "Free coaching session"],
    page=True,
) + f"""
<section class="section section--tight">
  <div class="wrap">
    <div class="intro-grid">
      <div>
        <p class="eyebrow"><span class="num">01</span> We're here for you</p>
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
    'Your <span class="serif">$0</span> enrollment offer',
    "We have a fitness solution for you — hundreds of monthly classes across every intensity and experience level, whether you've never had a gym membership or you've tried them all. Complete the form and we'll set up your visit and free coaching session.",
    "Claim My Free Pass",
) + cta_band(
    'Come <span class="serif">play</span> with us',
    "Two clubs, two free weeks, $0 enrollment. The only thing left to do is show up.",
    f"{IMG}/slider-locations_turf_alysse_torey.jpg",
)

# ============================================================ OUTDOOR
outdoor_body = hero(
    "Outdoor Fitness",
    ["Train under the", '<span class="serif">California sky</span>'],
    "Our members LOVE to exercise outdoors — and we LOVE giving them the environment and tools to show up and move every day. We've expanded our outdoor footprint so you have everything you need, all year-round.",
    img=f"{IMG}/slider-locations_turf_alysse_torey.jpg",
    crumb="Outdoor",
    actions=[("Start 2 Weeks Free", "join.html", True)],
    meta=["Covered outdoor turf", "Rain or shine", "Both clubs"],
    page=True,
) + f"""
<section class="section">
  <div class="wrap">
    <div class="cards-head">
      <div>
        <p class="eyebrow"><span class="num">01</span> The outdoor playground</p>
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
        <p class="eyebrow"><span class="num">01</span> What DrBrainRX offers</p>
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

<section class="section section--light" id="offer">
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
        <p class="eyebrow"><span class="num">01</span> Everything in one place</p>
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
    "Not a member yet? Start with two free weeks and we'll get you set up on the app on day one.",
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
) + f"""
<section class="section section--tight">
  <div class="wrap">
    <div class="intro-grid">
      <div>
        <p class="eyebrow"><span class="num">01</span> Locally owned, member first</p>
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
    "Preferred pricing is just one of the perks. Start with two free weeks and discover the rest.",
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

# ============================================================ BUILD ALL
PAGES = [
    ("index.html", "Forma Gym | Walnut Creek &amp; San Jose | Play Every Day", "Two luxury Bay Area fitness clubs — Walnut Creek &amp; San Jose. All group fitness, personal training, pools, cryotherapy, spa and Kidzville. Start with two free weeks.", "", home_body),
    ("about.html", "About Forma Gym | Our Mission &amp; Story", "To make exercise a part of our member's daily lives, for the rest of their lives. Meet Forma Gym — two Bay Area clubs and one community.", "about.html", about_body),
    ("group-fitness.html", "Group Fitness Classes | Forma Gym", "14 group fitness formats included with membership — Cycle, Yoga, Barre, HIIT, Pilates, Dance, TRX, Aqua and more, across Walnut Creek &amp; San Jose.", "group-fitness.html", groupfit_body),
    ("training.html", "Personal Training | Forma Gym", "1-on-1 and small group personal training with the best coaches in the Bay Area. Nutrition guidance, accountability, and a plan built around you.", "training.html", training_body),
    ("recovery.html", "Recovery, Cryotherapy &amp; Cold Plunge | Forma Gym", "Recover like an athlete — cryotherapy, cold plunge, full-service spa, sauna, steam and hot tubs at Forma Gym.", "recovery.html", recovery_body),
    ("cryo.html", "Cryotherapy + Cold Plunge | Forma Gym", "Whole-body cryotherapy and cold plunge at Forma Gym. Burn 500–800 calories per session, reduce pain and inflammation, recover faster.", "", cryo_body),
    ("spa.html", "The Spa at Forma | Massage, Facials &amp; Skin Care", "A full-service day spa at Forma Gym — therapeutic massage, facials and clinical skin care in Walnut Creek &amp; San Jose.", "", spa_body),
    ("mindbodylab.html", "Mind Body LAB &amp; DrBrainRX | Forma Gym", "Where science meets self-care — brain health, recovery tech, meditation and the mind-body connection at Forma Gym.", "", mbl_body),
    ("kidzville.html", "Kidzville Childcare | Forma Gym Walnut Creek", "Free, safe, active childcare for ages 6 weeks–12 years while you work out. Forma Kidzville at Walnut Creek.", "", kidz_body),
    ("rise.html", "RISE Program | Exercise-Based Therapy for Paralysis | Forma", "RISE is an exercise-based therapy program for individuals living with paralysis. Movement is medicine. Scholarships available.", "", rise_body),
    ("givesback.html", "Forma Gives Back | Fitness for Everyone", "Forma believes fitness should be available to everyone on the spectrum of movement. Learn how Forma Gives Back to the Bay Area.", "", givesback_body),
    ("walnut-creek.html", "Forma Gym Walnut Creek | 1908 Olympic Blvd", "Forma Gym Walnut Creek — 35,000 sq ft of indoor &amp; outdoor fitness, heated pool, Kidzville, cryotherapy, day spa and Café.", "locations.html", walnutcreek_body),
    ("san-jose.html", "Forma Gym San Jose | 5434 Thornwood Dr", "Forma Gym San Jose — 40,000 sq ft luxury facility with covered outdoor turf, heated 6-lane pool, cold plunge and massage services.", "locations.html", sanjose_body),
    ("locations.html", "Locations &amp; Hours | Forma Gym Walnut Creek &amp; San Jose", "Two premium Bay Area clubs, one membership. Hours, addresses and amenities for Forma Gym Walnut Creek &amp; San Jose.", "locations.html", locations_body),
    ("join.html", "Join Now — 2 Weeks Free | Forma Gym", "Join Forma Gym and your first two weeks are free. All-inclusive access to both Bay Area clubs, every class and recovery amenity.", "", join_body),
    ("trial-pass.html", "Trial Pass — Free Visit &amp; 2 Weeks Free | Forma Gym", "Schedule a visit, tour or guest workout at Forma Gym. $0 enrollment, a free coaching session, and your first two weeks free.", "", trial_body),
    ("outdoor-training.html", "Outdoor Fitness | Forma Gym", "Strength, cardio, group exercise and cycle — outdoors, year-round, at both Forma Gym clubs.", "", outdoor_body),
    ("drbrainrx.html", "DrBrainRX — GLP-1, Peptides &amp; Longevity | Forma Gym", "GLP-1 weight loss care, peptide therapy and longevity medicine for Forma members through DrBrainRX. 1 month free + $70 off, code FORMAGYM.", "", drbrain_body),
    ("app.html", "The Forma App | Forma Gym", "Book classes, reserve lanes, check schedules and manage your membership with the Forma app.", "", app_body),
    ("merchant.html", "Preferred Merchant Program | Forma Gym", "Forma members get preferred pricing at locally owned Bay Area businesses through our Preferred Merchant Program.", "", merchant_body),
    ("contact.html", "Contact &amp; Book a Tour | Forma Gym", "Book a tour or reach a Forma Gym club — Walnut Creek (925) 932-6400 or San Jose (408) 363-1010.", "", contact_body),
    ("accessibility.html", "Accessibility Statement | Forma Gym", "Forma Gym is committed to making our clubs and website accessible and welcoming to everyone.", "", accessibility_body),
    ("privacy.html", "Privacy Policy | Forma Gym", "Forma is a SPAM-FREE ZONE — we never share or sell your information.", "", privacy_body),
]

# class detail pages — all 14 formats
_others_pool = [(l, h, d) for l, h, d in ALL_CLASSES]
for slug, title, img, lead, short in CLASS_PAGES:
    others = [o for o in _others_pool if o[1] != f"{slug}.html"][:6]
    PAGES.append((f"{slug}.html", f"{title} | Group Fitness | Forma Gym",
                  f"{title} at Forma Gym — included with membership, all levels welcome. Start with two free weeks.",
                  "group-fitness.html", class_page(slug, title, img, lead, others)))


# ============================================================ BLOG (CMS-driven)
POSTS = load_collection("blog")

def blog_index_body():
    if not POSTS:
        cards = '<p class="body-copy">No posts yet — check back soon.</p>'
    else:
        cards = ""
        for p in POSTS:
            num = f'<span class="card__num">{fmt_date(p.get("date"))} · {p.get("author","")}</span>'
            cards += (f'<a class="card" href="blog/{p["_slug"]}.html"><div class="card__media card__media--wide">'
                      f'<img src="{cms_img(p.get("image"))}" alt="{p.get("title","")}" loading="lazy">{num}'
                      f'<div class="card__label"><h3>{p.get("title","")}</h3></div></div>'
                      f'<div class="card__below"><p>{p.get("excerpt","")}</p></div></a>')
    return hero("Forma Blog", ["News &amp;", '<span class="serif">stories</span>'],
        "Member stories, training tips, club news and behind-the-scenes fun — fresh from the team.",
        img=f"{IMG}/slider-locations_turf_alysse_torey.jpg", crumb="Blog",
        actions=[("Join Now", "join.html", True)], page=True,
    ) + f"""
<section class="section"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">01</span> Latest</p><h2 class="h-display reveal" style="font-size:clamp(34px,4.6vw,72px)">On the <span class="serif">blog</span></h2></div></div>
  <div class="card-grid" data-stagger>{cards}</div>
</div></section>
""" + cta_band('Come be part of the <span class="serif">story</span>', "There's always something happening. Come see for yourself.", f"{IMG}/slider-locations_group_dance.jpg")

def blog_post_body(p):
    others = "".join(
        f'<a class="row-item" href="../blog/{o["_slug"]}.html"><span class="row-item__idx">→</span>'
        f'<span class="row-item__title">{o.get("title","")}</span>'
        f'<span class="row-item__desc">{o.get("excerpt","")}</span><span class="row-item__arrow">→</span></a>'
        for o in POSTS if o["_slug"] != p["_slug"])
    more = f"""
<section class="section section--light"><div class="wrap">
  <div class="cards-head"><div><p class="eyebrow"><span class="num">02</span> Keep reading</p><h2 class="h-display reveal" style="font-size:clamp(30px,3.4vw,52px)">More from <span class="serif">the blog</span></h2></div>
  <a class="inline-link reveal" href="../blog.html">All posts →</a></div><div class="rows reveal">{others}</div>
</div></section>""" if others else ""
    return f"""
<section class="hero hero--page hero--post">
  <div class="hero__media"><img src="../{cms_img(p.get('image'))}" alt=""></div>
  <div class="hero__crumb"><div><a href="../index.html">Home</a> &nbsp;/&nbsp; <a href="../blog.html">Blog</a></div></div>
  <div class="hero__inner">
    <p class="hero__kicker">{fmt_date(p.get('date'))} &nbsp;·&nbsp; {p.get('author','Team')}</p>
    <h1 class="hero__title"><span class="ln"><span style="transition-delay:.12s">{p.get('title','')}</span></span></h1>
  </div>
  <div class="hero__scroll" aria-hidden="true"></div>
</section>
<section class="section section--tight"><div class="wrap" style="max-width:760px">
  <div class="post-body reveal">{p['_body']}</div>
  <div class="reveal" style="margin-top:40px"><a class="btn btn--solid" href="../blog.html">← Back to the blog</a></div>
</div></section>
{more}
""" + cta_band('Like what you\'re <span class="serif">reading?</span>', "Come see it in person.", f"../{IMG}/slider-locations_group_dance.jpg")

def page_sub(filename, title, desc, body):
    html = head(title, desc) + header_html("blog.html") + body + footer_html()
    html = _re.sub(r'(href|src)="/(?!/)', r'\1="../', html)
    html = _re.sub(r'(href|src)="assets/', r'\1="../assets/', html)
    html = _re.sub(r'(href)="([a-z0-9-]+\.html)(#[^"]*)?"', r'\1="../\2\3"', html)
    os.makedirs(os.path.join(OUT, "blog"), exist_ok=True)
    with open(os.path.join(OUT, filename), "w") as f:
        f.write(html)
    print("built", filename)
# ============================================================ end BLOG

PAGES.append(("blog.html", f"Blog | Forma", "News, stories and tips from Forma.", "blog.html", blog_index_body()))

for fn, title, desc, active, body in PAGES:
    page(fn, title, desc, active, body)

print("\nDone:", len(PAGES), "pages")

for _p in POSTS:
    page_sub(f"blog/{_p['_slug']}.html", f"{_p.get('title','Post')} | Forma Blog", _p.get("excerpt","")[:160], blog_post_body(_p))
print("blog posts:", len(POSTS))
