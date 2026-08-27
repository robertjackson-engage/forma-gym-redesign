/* GHF — interactions */
(function () {
  "use strict";

  var docEl = document.documentElement;
  docEl.classList.add("js");

  /* ---------- guest/member view ---------- */
  function setView(v, persist) {
    docEl.setAttribute("data-view", v);
    if (persist !== false) {
      try { localStorage.setItem("forma-view", v); } catch (e) {}
      docEl.classList.add("has-view");
    }
  }
  document.querySelectorAll("[data-view-set]").forEach(function (b) {
    b.addEventListener("click", function () { setView(b.getAttribute("data-view-set")); });
  });

  /* ---------- preloader intro + experience chooser sequencing ---------- */
  var pre = document.querySelector(".preloader");
  var skipIntro = docEl.classList.contains("no-preloader");
  var chooser = document.querySelector(".view-chooser");
  var needChoice = chooser && !docEl.classList.contains("has-view");

  function reveal() { document.body.classList.add("is-loaded"); }

  /* The gate is a fixed overlay, but nothing stopped the page behind it from
     scrolling — the guest site showed and scrolled underneath. overflow:hidden on
     body is not enough on iOS Safari, so pin the body and restore the offset. */
  var lockedY = 0;
  function lockScroll() {
    lockedY = window.pageYOffset || document.documentElement.scrollTop || 0;
    document.body.style.top = (-lockedY) + "px";
    document.body.classList.add("choice-open");
  }
  function unlockScroll() {
    document.body.classList.remove("choice-open");
    document.body.style.top = "";
    window.scrollTo(0, lockedY);
  }

  function ready() {
    if (!needChoice) { reveal(); return; }
    lockScroll();
    chooser.querySelectorAll("[data-choose]").forEach(function (p) {
      p.addEventListener("click", function () {
        setView(p.getAttribute("data-choose"));
        finishChoice();
      });
    });
    /* Sign me up leaves for the join page, so persist a guest view first —
       otherwise has-view is unset and the chooser greets them again there. */
    var join = chooser.querySelector(".vc-join");
    if (join) join.addEventListener("click", function () { setView("guest"); });
    /* The hamburger is the way through for someone who does not want to pick a
       side. Land them on the public (guest) site and remember it, so the gate
       does not reappear on the next page. */
    var skip = chooser.querySelector(".vc-skip");
    if (skip) skip.addEventListener("click", function () {
      setView("guest");
      finishChoice();
    });
    /* Escape does the same — a dialog that traps you is a dialog people fight. */
    document.addEventListener("keydown", function onEsc(e) {
      if (e.key !== "Escape" || !document.body.classList.contains("choice-open")) return;
      document.removeEventListener("keydown", onEsc);
      setView("guest");
      finishChoice();
    });
  }
  function finishChoice() {
    unlockScroll();
    document.body.classList.add("choice-done");
    setTimeout(reveal, 350);
    setTimeout(function () { chooser.remove(); document.body.classList.remove("choice-done"); }, 1000);
  }

  if (!pre || skipIntro) {
    if (pre) pre.remove();
    /* two frames so hero line transitions still play on entry */
    requestAnimationFrame(function () { requestAnimationFrame(ready); });
  } else {
    var bar = pre.querySelector(".preloader__bar i");
    var count = pre.querySelector(".preloader__count");
    var t0 = null;
    var INTRO_MS = 1500;
    var introFinished = false;
    function tick(t) {
      if (introFinished) return;
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / INTRO_MS, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      if (bar) bar.style.transform = "scaleX(" + eased + ")";
      if (count) count.textContent = Math.round(eased * 100);
      if (p < 1) requestAnimationFrame(tick);
      else setTimeout(introDone, 250);
    }
    function introDone() {
      if (introFinished) return;
      introFinished = true;
      if (bar) bar.style.transform = "scaleX(1)";
      if (count) count.textContent = "100";
      pre.classList.add("is-done");
      ready();
      try { sessionStorage.setItem("forma-intro", "1"); } catch (e) {}
      setTimeout(function () { pre.remove(); }, 1100);
    }
    requestAnimationFrame(tick);
    /* rAF pauses in background tabs — never let the intro hold the page */
    setTimeout(introDone, INTRO_MS + 1400);
  }

  /* ---------- page-to-page fade transition ---------- */
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a[href]");
    if (!a || a.target || e.metaKey || e.ctrlKey || e.shiftKey) return;
    var href = a.getAttribute("href");
    if (!href || href.charAt(0) === "#" || /^(https?:|tel:|mailto:)/.test(href)) return;
    var url = new URL(a.href, location.href);
    if (url.pathname === location.pathname && url.hash) return; /* same-page anchor */
    e.preventDefault();
    document.body.classList.remove("menu-open");
    document.body.classList.add("page-exit");
    setTimeout(function () { location.href = a.href; }, 300);
  });
  /* bfcache restore (Safari back button): never come back faded out */
  window.addEventListener("pageshow", function (ev) {
    if (ev.persisted) {
      document.body.classList.remove("page-exit");
      document.body.classList.add("is-loaded");
    }
  });

  /* ---------- header behavior ---------- */
  /* persistent nav: always visible so Get Pricing never leaves the screen;
     compacts into a glass bar once scrolled */
  var header = document.querySelector(".site-header");
  function onScrollHeader() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 60);
  }
  window.addEventListener("scroll", onScrollHeader, { passive: true });
  onScrollHeader();

  /* ---------- menu overlay ---------- */
  var toggle = document.querySelector(".menu-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("menu-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      var links = document.querySelectorAll(".menu-list a");
      links.forEach(function (a, i) {
        a.style.transitionDelay = open ? 0.18 + i * 0.05 + "s" : "0s";
      });
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") document.body.classList.remove("menu-open");
  });

  /* ---------- reveal on scroll ---------- */
  var io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add("is-in");
          io.unobserve(en.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
  );
  document.querySelectorAll(".reveal, .reveal-img, [data-stagger]").forEach(function (el) {
    io.observe(el);
  });

  /* ---------- counters ---------- */
  var cio = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        cio.unobserve(el);
        var target = parseFloat(el.getAttribute("data-count"));
        var dur = 1800;
        var t0 = null;
        function tick(t) {
          if (!t0) t0 = t;
          var p = Math.min((t - t0) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 4);
          el.textContent = Math.round(target * eased).toLocaleString();
          if (p < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
      });
    },
    { threshold: 0.5 }
  );
  document.querySelectorAll("[data-count]").forEach(function (el) { cio.observe(el); });

  /* ---------- parallax (media inside masked containers) ---------- */
  /* split/loc media use the wipe + zoom-settle reveal; hero media shows its
     full frame (no over-scan), so only CTA bands keep the parallax drift */
  var pxItems = [];
  document.querySelectorAll(".cta-band__media img").forEach(function (el) {
    pxItems.push(el);
  });
  var ticking = false;
  function parallax() {
    var vh = window.innerHeight;
    pxItems.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < -100 || r.top > vh + 100) return;
      var p = (r.top + r.height / 2 - vh / 2) / (vh / 2 + r.height / 2); // -1..1
      var range = el.closest(".hero") ? 0.1 : 0.14;
      el.style.transform = "translateY(" + (-p * range * 100).toFixed(2) + "px)";
    });
    ticking = false;
  }
  function onScrollPx() {
    if (!ticking) { requestAnimationFrame(parallax); ticking = true; }
  }
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    window.addEventListener("scroll", onScrollPx, { passive: true });
    window.addEventListener("resize", onScrollPx);
    parallax();
  }

  /* ---------- accordion ---------- */
  document.querySelectorAll(".acc__item").forEach(function (item) {
    var head = item.querySelector(".acc__head");
    var body = item.querySelector(".acc__body");
    head.addEventListener("click", function () {
      var isOpen = item.classList.contains("is-open");
      var parent = item.closest(".acc");
      parent.querySelectorAll(".acc__item.is-open").forEach(function (o) {
        o.classList.remove("is-open");
        o.querySelector(".acc__body").style.maxHeight = "0px";
      });
      if (!isOpen) {
        item.classList.add("is-open");
        body.style.maxHeight = body.scrollHeight + "px";
      }
    });
  });

  /* ---------- testimonial slider ---------- */
  document.querySelectorAll(".t-slider").forEach(function (slider) {
    var track = slider.querySelector(".t-slider__track");
    var slides = track.children.length;
    var idx = 0;
    var auto;
    function go(n) {
      idx = (n + slides) % slides;
      track.style.transform = "translateX(-" + idx * 100 + "%)";
    }
    slider.querySelectorAll("[data-dir]").forEach(function (b) {
      b.addEventListener("click", function () {
        go(idx + (b.getAttribute("data-dir") === "next" ? 1 : -1));
        clearInterval(auto);
        auto = setInterval(function () { go(idx + 1); }, 6000);
      });
    });
    auto = setInterval(function () { go(idx + 1); }, 6000);
  });

  /* ---------- custom cursor ---------- */
  if (window.matchMedia("(hover: hover) and (min-width: 901px)").matches) {
    var dot = document.createElement("div");
    var ring = document.createElement("div");
    dot.className = "cursor-dot";
    ring.className = "cursor-ring";
    document.body.appendChild(dot);
    document.body.appendChild(ring);
    var mx = -100, my = -100, rx = -100, ry = -100;
    window.addEventListener("mousemove", function (e) { mx = e.clientX; my = e.clientY; });
    (function loop() {
      rx += (mx - rx) * 0.16;
      ry += (my - ry) * 0.16;
      dot.style.transform = "translate(" + mx + "px," + my + "px) translate(-50%,-50%)";
      ring.style.transform = "translate(" + rx + "px," + ry + "px) translate(-50%,-50%)";
      requestAnimationFrame(loop);
    })();
    document.addEventListener("mouseover", function (e) {
      if (e.target.closest("a, button, .acc__head")) ring.classList.add("is-hover");
      else ring.classList.remove("is-hover");
    });
  }

  /* ---------- floating labels: keep selects marked ---------- */
  document.querySelectorAll(".field select").forEach(function (s) {
    function mark() { s.closest(".field").classList.toggle("has-value", !!s.value); }
    s.addEventListener("change", mark);
    mark();
  });

  /* ---------- fake submit (demo) ---------- */
  document.querySelectorAll("form[data-demo]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var btn = f.querySelector("button[type=submit]");
      if (btn) {
        var txt = btn.innerHTML;
        btn.innerHTML = "Request received – we'll be in touch";
        btn.disabled = true;
        setTimeout(function () { btn.innerHTML = txt; btn.disabled = false; f.reset(); }, 4200);
      }
    });
  });

  /* The AC forms carry Forma's ad-attribution fields (GCLID + utm_source /
     medium / campaign / term — field[354] and field[357..360] on forms 9, 33,
     72, 93). They are meant to be invisible plumbing, but AC renders them as
     ordinary labelled inputs, and nothing fills them. Hide them and copy the
     values off the landing URL so Google Ads / campaign attribution still
     reaches ActiveCampaign. Matched on label text, not field numbers, so this
     survives someone reordering fields in the AC form designer. */
  function wireAcTracking(form) {
    var params = new URLSearchParams(window.location.search);
    form.querySelectorAll("._form_element").forEach(function (row) {
      var label = row.querySelector("label,._form-label");
      if (!label) return;
      var key = label.textContent.trim().replace(/\*$/, "").toLowerCase();
      if (key !== "gclid" && key.indexOf("utm_") !== 0) return;
      row.style.setProperty("display", "none", "important");   // plumbing, not UI
      var input = row.querySelector("input");
      if (input) {
        var val = params.get(key);
        if (val) input.value = val;
      }
    });
  }

  /* AC ships an inline stylesheet keyed to randomly-generated form IDs
     (#_form_A1B2C3_ ._submit {...!important}). An ID + !important outranks any
     class rule we can write, and the ID changes on every render — so these few
     properties have to be set on the elements themselves. Everything else is
     handled by the ._form rules in main.css. */
  function brandAcForm(form) {
    var cs = getComputedStyle(document.documentElement);
    var v = function (n) { return cs.getPropertyValue(n).trim(); };
    var set = function (el, prop, val) { el.style.setProperty(prop, val, "important"); };
    form.querySelectorAll("input[type=text],input[type=email],input[type=tel],input[type=number],textarea,select")
      .forEach(function (el) {
        set(el, "color", v("--bone"));
        set(el, "background-color", v("--ink-2"));
        set(el, "border-color", "rgba(244,247,248,0.14)");
      });
    form.querySelectorAll("._submit,button[type=submit],input[type=submit]").forEach(function (el) {
      set(el, "background", v("--accent"));
      set(el, "color", v("--ink"));
    });
    form.querySelectorAll("._form-label,label").forEach(function (el) {
      set(el, "color", "rgba(244,247,248,0.60)");
    });
  }

  /* ---------- ActiveCampaign: move each embedded form into its slot ----------
     AC's embed script appends the rendered form to <body> rather than where the
     <script> sits, so it would otherwise land at the bottom of the page. Each
     wrapper is .ac-form--<id>; the rendered form is ._form_<id>. AC renders
     async, so watch for it instead of assuming it's there on DOMContentLoaded. */
  var acSlots = document.querySelectorAll("[class*='ac-form--']");
  if (acSlots.length) {
    var placeAcForms = function () {
      var pending = 0;
      acSlots.forEach(function (slot) {
        var m = /ac-form--(\d+)/.exec(slot.className);
        if (!m) return;
        if (slot.querySelector("._form_" + m[1])) return;   // already placed
        var form = document.querySelector("._form_" + m[1]);
        if (form) {
          var holder = form.closest("div:not([class])") || form;
          slot.appendChild(holder);
          brandAcForm(form);
          wireAcTracking(form);
        } else {
          pending++;
        }
      });
      return pending === 0;
    };
    if (!placeAcForms()) {
      var acObserver = new MutationObserver(function () {
        if (placeAcForms()) acObserver.disconnect();
      });
      acObserver.observe(document.body, { childList: true, subtree: false });
      setTimeout(function () { acObserver.disconnect(); }, 10000);  // stop watching eventually
    }
  }

  /* ---------- photo strip: auto-scroll, and swipe/drag to take over ---------- */
  /* The text marquees still run on the CSS keyframe. This one cannot: a
     transform is not grabbable, so the strip is a real scroll container and we
     move scrollLeft ourselves. Two identical tracks let it wrap seamlessly. */
  document.querySelectorAll(".marquee--photo").forEach(function (el) {
    var track = el.querySelector(".marquee__track");
    if (!track) return;
    var slow = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var TRACK_GAP = 8;                 // matches .marquee--photo .marquee__track + .marquee__track
    var LOOP_MS = 52000;               // the duration the keyframe used, kept identical
    var held = false, resumeAt = 0, onScreen = true, last = 0;
    var dragging = false, startX = 0, startLeft = 0;

    function loopWidth() {
      var w = track.getBoundingClientRect().width;
      return w > 0 ? w + TRACK_GAP : 0;
    }
    function wrap() {
      var w = loopWidth();
      if (!w) return;
      if (el.scrollLeft >= w) el.scrollLeft -= w;
      else if (el.scrollLeft <= 0) el.scrollLeft += w;
    }
    function frame(ts) {
      var dt = last ? Math.min(ts - last, 50) : 16;   // cap so a background tab cannot jump it
      last = ts;
      if (!slow && !held && !dragging && onScreen && ts >= resumeAt) {
        var w = loopWidth();
        if (w) {
          el.scrollLeft += (w / LOOP_MS) * dt;
          if (el.scrollLeft >= w) el.scrollLeft -= w;
        }
      }
      requestAnimationFrame(frame);
    }

    // Pause while the user is on it, then hand it back after a beat.
    function hold() { held = true; }
    function release() { held = false; resumeAt = performance.now() + 1200; }
    el.addEventListener("pointerdown", function (e) {
      hold();
      if (e.pointerType === "mouse") {   // touch keeps native scrolling; only mouse needs a drag
        // The strip is all <img>, so without this the browser starts its own
        // image drag on mousedown+move and eats the gesture — which is why it
        // used to take a click before a drag would take.
        e.preventDefault();
        dragging = true; startX = e.clientX; startLeft = el.scrollLeft;
        el.classList.add("is-dragging");
        try { el.setPointerCapture(e.pointerId); } catch (err) {}
      }
    });
    el.addEventListener("dragstart", function (e) { e.preventDefault(); });
    el.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      el.scrollLeft = startLeft - (e.clientX - startX);
      wrap();
    });
    ["pointerup", "pointercancel"].forEach(function (evt) {
      el.addEventListener(evt, function () {
        dragging = false; el.classList.remove("is-dragging"); release();
      });
    });
    el.addEventListener("touchstart", hold, { passive: true });
    el.addEventListener("touchend", release, { passive: true });
    el.addEventListener("wheel", function () { release(); }, { passive: true });
    // A swipe carries past the seam on its own momentum, so keep wrapping after release.
    el.addEventListener("scroll", function () { if (!dragging) wrap(); }, { passive: true });

    if (window.IntersectionObserver) {
      new IntersectionObserver(function (entries) {
        onScreen = entries[0].isIntersecting;
      }, { rootMargin: "100px" }).observe(el);
    }
    requestAnimationFrame(frame);
  });

  /* ---------- hero video: pick desktop/mobile source by viewport, respect data saver ---------- */
  var heroVids = document.querySelectorAll(".hero__media video[data-src-desktop]");
  if (heroVids.length) {
    var saveData = navigator.connection && navigator.connection.saveData;
    var mqMobile = window.matchMedia("(max-width: 820px)");
    var applyHeroSrc = function () {
      // Poster first, and outside the data-saver check: the phone hero is
      // portrait and the desktop hero is landscape, so the wrong crop loses the
      // subject — and on a saved-data connection the poster is the whole hero.
      heroVids.forEach(function (v) {
        var wantP = mqMobile.matches ? v.dataset.posterMobile : v.dataset.posterDesktop;
        if (wantP && v.getAttribute("poster") !== wantP) v.setAttribute("poster", wantP);
      });
      if (saveData) return; // poster only — don't pull a hero video
      var want = mqMobile.matches ? "srcMobile" : "srcDesktop";
      heroVids.forEach(function (v) {
        var src = v.dataset[want];
        if (!src || v.getAttribute("src") === src) return;
        // The poster-only scrim comes off the moment real footage is up.
        v.addEventListener("playing", function () {
          var media = v.closest(".hero__media");
          if (media) media.classList.add("is-playing");
        }, { once: true });
        v.setAttribute("src", src);   // autoplay attr starts playback once the src loads
        var p = v.play();             // best-effort nudge; ignore autoplay-policy rejects
        if (p && p.catch) p.catch(function () {});
      });
    };
    applyHeroSrc();
    if (mqMobile.addEventListener) mqMobile.addEventListener("change", applyHeroSrc);
    else if (mqMobile.addListener) mqMobile.addListener(applyHeroSrc);
  }
})();
