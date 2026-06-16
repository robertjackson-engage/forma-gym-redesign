/* Forma Concierge — Claude-powered */
(function () {
  "use strict";

  var CFG = window.GHF_CHAT || {};
  var MODEL = CFG.model || "claude-sonnet-4-6";

  var SYSTEM = [
    "You are the Forma Concierge, the friendly AI assistant for Forma Gym — formagym.com, two premium fitness clubs in the Bay Area (Walnut Creek & San Jose). You live on their website.",
    "Voice: warm, upbeat, concise — like Forma's legendary front-desk team, not a salesperson. Short paragraphs. The brand mantra is 'Play Every Day.' Mission: 'make exercise a part of our member's daily lives, for the rest of their lives.'",
    "FACTS:",
    "- 2 locations, one membership covers both. WALNUT CREEK: 1908 Olympic Blvd, Walnut Creek, CA 94596, (925) 932-6400 — the original (since 2009), 35,000 sq ft, heated outdoor lap pool under redwoods, onsite Kidzville childcare, cryotherapy + cold plunge, full-service day spa, Forma Café + Smoothie Bar, 4 studios + Pilates Reformer studio. SAN JOSE: 5434 Thornwood Dr, San Jose, CA 95123, (408) 363-1010 — since 2015, 40,000 sq ft with 8,000 sq ft covered outdoor area, heated 6-lane junior olympic pool + hot tub, sauna/steam/hot tub, cold plunge by Chilly Goat, onsite sports & therapeutic massage, chilled eucalyptus towel service.",
    "- Hours (both clubs): Mon-Thu 5am-11pm, Fri 5am-10pm, Sat & Sun 6am-8pm.",
    "- Membership: all-inclusive — every group fitness class, both clubs, heated pools, sauna/steam/hot tub, cold plunge, covered outdoor turf, expert coaches. SUMMER SPECIAL: join now and the first 2 weeks are free. Must be 18+ to join without a parent/guardian (13+ with approval). Forma does not publish flat prices online — a membership advisor tailors the rate; to get one, join online (join.html) or book a tour (contact.html#tour). Never invent a dollar price; instead mention the 2-weeks-free special and offer to connect them with an advisor.",
    "- 14 group fitness formats, all included: Aqua, Barre, Cardio + HIIT, Cycle, Dance, Low Impact + Balance, Kickboxing + Martial Arts, Meditation + Breathwork, Mat Pilates, Pilates Reformer, Sculpt, Stretch + Recovery, TRX, Yoga + Mind Body.",
    "- Personal Training: 1-on-1 and Small Group (4-8 people, one trainer). Free consultation. Nutrition guidance included. Coaches: Dave, Montana, Jason, Marco.",
    "- Recovery: Cryotherapy + Cold Plunge (chamber to -195°F, 3-min sessions burn 500-800 cal, reduce pain/inflammation, better sleep). Full-service Spa (massage from $65/25min to $160/80min; facials $140-$230; add-ons CBD $10, hot stone $20). Mind Body LAB + DrBrainRX (brain health). Sauna, eucalyptus steam, hot tub.",
    "- Kidzville: childcare ages 6 weeks-12 years, Walnut Creek only. Hours Mon-Thu 8a-1p & 4p-7:30p, Fri 8a-1p, Sat-Sun 8a-12p. Reservations recommended; WCReps@formagym.com or (925) 932-6400.",
    "- RISE: exercise-based therapy program for individuals living with paralysis; movement is medicine; scholarship program available.",
    "- Forma Gives Back: fitness available to everyone on the spectrum of movement, from those struggling to stand to world-class athletes.",
    "RULES: Answer only about Forma Gym, fitness, recovery, and visiting the clubs. Link pages with markdown like [Join Now](join.html), [Book a Tour](contact.html#tour), [Classes](group-fitness.html), [Personal Training](training.html), [Recovery & Cryo](recovery.html), [The Spa](spa.html), [Kidzville](kidzville.html), [Walnut Creek](walnut-creek.html), [San Jose](san-jose.html), [Locations](locations.html). For billing/account specifics, suggest calling the club: Walnut Creek (925) 932-6400 or San Jose (408) 363-1010. Keep answers under 120 words unless asked for detail. End with a helpful next step when natural."
  ].join("\n");

  // Forma 'f' mark — geometric, matches the wordmark
  var MARK = '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><path d="M20 52 V18 a8 8 0 0 1 8-8 h16" stroke="currentColor" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><path d="M18 32 h22" stroke="currentColor" stroke-width="8" stroke-linecap="round"/></svg>';

  var CHIPS = [
    "What's included in membership?",
    "Where are the clubs?",
    "Tell me about cryotherapy",
    "How do I start 2 weeks free?",
    "Do you have childcare?"
  ];

  /* ---------- build DOM ---------- */
  var root = document.createElement("div");
  root.innerHTML =
    '<button class="chat-orb" aria-label="Chat with the Forma Concierge">' + MARK + "</button>" +
    '<div class="chat-orb__hint" role="button" tabindex="0">' +
    '  <span class="chat-orb__hint-avatar">' + MARK + "</span>" +
    '  <span class="chat-orb__hint-text"><em>Have questions?</em> I\'m here to help.</span>' +
    '  <button class="chat-orb__hint-x" aria-label="Dismiss">✕</button>' +
    "</div>" +
    '<div class="chat-panel" role="dialog" aria-label="Forma Concierge chat">' +
    '  <div class="chat-head">' +
    '    <div class="chat-head__icon">' + MARK + "</div>" +
    '    <div><div class="chat-head__name">Forma Concierge</div><div class="chat-head__sub">AI Concierge · Powered by Claude</div></div>' +
    '    <button class="chat-head__close" aria-label="Close chat">✕</button>' +
    "  </div>" +
    '  <div class="chat-msgs"></div>' +
    '  <div class="chat-input">' +
    '    <textarea rows="1" placeholder="Ask about classes, pricing, hours…" aria-label="Message"></textarea>' +
    '    <button class="chat-send" aria-label="Send">→</button>' +
    "  </div>" +
    '  <div class="chat-note">Forma Concierge is an AI assistant — for account questions call your club: Walnut Creek (925) 932-6400 or San Jose (408) 363-1010.</div>' +
    "</div>";
  document.body.appendChild(root);

  var orb = root.querySelector(".chat-orb");
  var hint = root.querySelector(".chat-orb__hint");
  var msgs = root.querySelector(".chat-msgs");
  var input = root.querySelector(".chat-input textarea");
  var sendBtn = root.querySelector(".chat-send");
  var history = [];
  try { history = JSON.parse(sessionStorage.getItem("forma-chat") || "[]"); } catch (e) {}

  /* activation link: visiting any page with #ck=<api-key> stores the key in
     this browser and cleans the URL — the key never lives in the repo */
  try {
    var ckm = location.hash.match(/[#&]ck=([^&]+)/);
    if (ckm) {
      localStorage.setItem("forma-anthropic-key", decodeURIComponent(ckm[1]));
      history_replace_safe();
    }
  } catch (e) {}
  function history_replace_safe() {
    try { window.history.replaceState(null, "", location.pathname + location.search); } catch (e) {}
  }

  function getKey() {
    if (CFG.proxyUrl) return "proxy"; /* key lives server-side; nothing needed here */
    if (CFG.apiKey) return CFG.apiKey;
    try { return localStorage.getItem("forma-anthropic-key") || ""; } catch (e) { return ""; }
  }

  /* ---------- rendering ---------- */
  function md(t) {
    t = t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    t = t.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
    t = t.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    var blocks = t.split(/\n{2,}/).map(function (b) {
      var lines = b.split("\n");
      var items = lines.filter(function (l) { return /^\s*[-•]\s+/.test(l); });
      if (items.length && items.length === lines.length) {
        return "<ul>" + items.map(function (l) { return "<li>" + l.replace(/^\s*[-•]\s+/, "") + "</li>"; }).join("") + "</ul>";
      }
      return "<p>" + b.replace(/\n/g, "<br>") + "</p>";
    });
    return blocks.join("");
  }

  function addMsg(role, html) {
    var d = document.createElement("div");
    d.className = "chat-msg chat-msg--" + (role === "user" ? "user" : "ai");
    d.innerHTML = role === "user" ? html.replace(/</g, "&lt;") : html;
    msgs.appendChild(d);
    msgs.scrollTop = msgs.scrollHeight;
    return d;
  }

  function welcome() {
    var w = document.createElement("div");
    w.className = "chat-welcome";
    w.innerHTML = "<h3>What can we help you crush today?</h3><p>Classes, pricing, hours, programs — ask me anything about GHF.</p>" +
      '<div class="chat-chips">' + CHIPS.map(function (c) { return "<button>" + c + "</button>"; }).join("") + "</div>";
    msgs.appendChild(w);
    w.querySelectorAll("button").forEach(function (b) {
      b.addEventListener("click", function () { input.value = b.textContent; send(); });
    });
  }

  function keyGate() {
    var g = document.createElement("div");
    g.className = "chat-gate";
    g.innerHTML = "<p><strong>One-time setup:</strong> paste your Anthropic API key to activate Forma Concierge. It's stored only in this browser.</p>" +
      '<input type="password" placeholder="sk-ant-…" aria-label="Anthropic API key">' +
      '<button class="btn btn--solid btn--sm">Activate Coach →</button>';
    msgs.appendChild(g);
    g.querySelector("button").addEventListener("click", function () {
      var v = g.querySelector("input").value.trim();
      if (!v) return;
      try { localStorage.setItem("forma-anthropic-key", v); } catch (e) {}
      g.remove();
      addMsg("ai", "<p>All set! Ask me anything about GHF. 💪</p>");
    });
  }

  function restore() {
    if (!history.length) { welcome(); }
    else history.forEach(function (m) { addMsg(m.role, m.role === "user" ? m.content : md(m.content)); });
    if (!getKey()) keyGate();
  }

  /* ---------- Claude call (streaming) ---------- */
  function send() {
    var text = input.value.trim();
    if (!text) return;
    if (!getKey()) { keyGate(); return; }
    input.value = "";
    var wEl = msgs.querySelector(".chat-welcome");
    if (wEl) wEl.remove();
    addMsg("user", text);
    history.push({ role: "user", content: text });
    sendBtn.disabled = true;

    var typing = document.createElement("div");
    typing.className = "chat-typing";
    typing.innerHTML = "<i></i><i></i><i></i>";
    msgs.appendChild(typing);
    msgs.scrollTop = msgs.scrollHeight;

    var aiEl = null;
    var full = "";

    var apiUrl = CFG.proxyUrl || "https://api.anthropic.com/v1/messages";
    var apiHeaders = { "content-type": "application/json" };
    if (!CFG.proxyUrl) {
      apiHeaders["x-api-key"] = getKey();
      apiHeaders["anthropic-version"] = "2023-06-01";
      apiHeaders["anthropic-dangerous-direct-browser-access"] = "true";
    }
    fetch(apiUrl, {
      method: "POST",
      headers: apiHeaders,
      body: JSON.stringify({
        model: MODEL,
        max_tokens: 700,
        system: SYSTEM,
        messages: history.slice(-12),
        stream: true
      })
    }).then(function (res) {
      if (!res.ok) return res.text().then(function (t) { throw new Error("API " + res.status + ": " + t.slice(0, 200)); });
      var reader = res.body.getReader();
      var dec = new TextDecoder();
      var buf = "";
      function pump() {
        return reader.read().then(function (r) {
          if (r.done) return;
          buf += dec.decode(r.value, { stream: true });
          var lines = buf.split("\n");
          buf = lines.pop();
          lines.forEach(function (ln) {
            if (ln.indexOf("data: ") !== 0) return;
            try {
              var ev = JSON.parse(ln.slice(6));
              if (ev.type === "content_block_delta" && ev.delta && ev.delta.text) {
                if (!aiEl) { typing.remove(); aiEl = addMsg("ai", ""); }
                full += ev.delta.text;
                aiEl.innerHTML = md(full);
                msgs.scrollTop = msgs.scrollHeight;
              }
            } catch (e) {}
          });
          return pump();
        });
      }
      return pump();
    }).then(function () {
      if (typing.parentNode) typing.remove();
      if (full) {
        history.push({ role: "assistant", content: full });
        try { sessionStorage.setItem("forma-chat", JSON.stringify(history.slice(-20))); } catch (e) {}
      }
    }).catch(function (err) {
      if (typing.parentNode) typing.remove();
      var isAuth = /401|403/.test(err.message);
      if (isAuth) { try { localStorage.removeItem("forma-anthropic-key"); } catch (e) {} }
      addMsg("ai", "<p>" + (isAuth
        ? "That API key didn't work — let's try again."
        : "I'm having trouble connecting right now. You can always reach a club — Walnut Creek <a href='tel:9259326400'>(925) 932-6400</a> or San Jose <a href='tel:4083631010'>(408) 363-1010</a>.") + "</p>");
      if (isAuth) keyGate();
      history.pop();
    }).finally(function () {
      sendBtn.disabled = false;
      input.focus();
    });
  }

  /* ---------- events ---------- */
  function openChat() {
    document.body.classList.add("chat-open");
    hint.classList.remove("is-on");
    if (!msgs.children.length) restore();
    setTimeout(function () { input.focus(); }, 400);
  }
  orb.addEventListener("click", openChat);
  /* clicking the popup bubble opens the chat too */
  hint.addEventListener("click", function (e) {
    if (e.target.closest(".chat-orb__hint-x")) return;
    openChat();
  });
  hint.addEventListener("keydown", function (e) {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openChat(); }
  });
  hint.querySelector(".chat-orb__hint-x").addEventListener("click", function (e) {
    e.stopPropagation();
    hint.classList.remove("is-on");
    try { sessionStorage.setItem("forma-chat-hint", "1"); } catch (er) {}
  });
  root.querySelector(".chat-head__close").addEventListener("click", function () {
    document.body.classList.remove("chat-open");
  });
  sendBtn.addEventListener("click", send);
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
  });
  input.addEventListener("input", function () {
    input.style.height = "auto";
    input.style.height = Math.min(input.scrollHeight, 110) + "px";
  });

  /* teaser popup, once per session — appears shortly after load, lingers */
  try {
    if (!sessionStorage.getItem("forma-chat-hint")) {
      setTimeout(function () {
        if (!document.body.classList.contains("chat-open")) hint.classList.add("is-on");
      }, 3500);
      setTimeout(function () {
        hint.classList.remove("is-on");
        try { sessionStorage.setItem("forma-chat-hint", "1"); } catch (er) {}
      }, 16000);
    }
  } catch (e) {}
})();
