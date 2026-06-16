/* Forma — Join Online wizard (real 6-step flow with live pricing) */
(function () {
  "use strict";

  var wizard = document.querySelector(".join");
  if (!wizard) return;

  var TOTAL = 6;
  var step = 1;
  var state = {
    club: null, plan: null, primary: 0, addl: 0, enroll: 0,
    first: "", last: "", email: "", phone: "", address: "",
    family: [],            // array of {name}
    onetime: [],           // [{label, amt}]
    monthly: [],           // [{label, amt}]
    perk: "One Personal Training",
    pay: "card",
  };
  var money = function (n) { return "$" + n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
  var money0 = function (n) { return "$" + n.toLocaleString("en-US"); };

  var stepsEls = wizard.querySelectorAll(".join-step");
  var navItems = wizard.querySelectorAll(".join__steps-nav li");
  var barFill = wizard.querySelector(".join__progress-bar i");
  var backBtn = wizard.querySelector(".join__nav-row .back");
  var nextBtn = wizard.querySelector(".join__nav-row .next");
  var countEl = wizard.querySelector(".join__count");

  /* ---------- pricing ---------- */
  function monthlyTotal() {
    var t = state.primary;
    t += state.family.length * state.addl;
    state.monthly.forEach(function (a) { t += a.amt; });
    return t;
  }
  function dueToday() {
    // $0 enrollment + first 2 weeks free → only one-time jump-start packages are due now
    var t = 0;
    state.onetime.forEach(function (a) { t += a.amt; });
    return t;
  }

  /* ---------- summary ---------- */
  function renderSummary() {
    set("loc", state.club);
    set("plan", state.plan ? state.plan + " Membership" : "");
    var lines = wizard.querySelector("[data-sum-lines]");
    var html = "";
    if (state.plan) {
      html += sline("Primary member", money0(state.primary) + "/mo");
      state.family.forEach(function (f, i) {
        html += sline("Family member " + (i + 1), money0(state.addl) + "/mo");
      });
      state.monthly.forEach(function (a) { html += sline(a.label, money0(a.amt) + "/mo"); });
      if (state.plan === "Premier") html += sline("Premier perk · " + state.perk.replace(/^(One |Two )/, ""), "Included");
      state.onetime.forEach(function (a) { html += sline(a.label + " (one-time)", money0(a.amt)); });
    }
    lines.innerHTML = html;
    wizard.querySelector("[data-sum-monthly]").innerHTML = state.plan ? money0(monthlyTotal()) + "<small>/mo</small>" : "$0<small>/mo</small>";
    wizard.querySelector("[data-sum-today]").textContent = money(dueToday());
  }
  function sline(dt, dd) { return '<div class="sum-row sum-row--sm"><dt>' + dt + "</dt><dd>" + dd + "</dd></div>"; }
  function set(key, val) {
    var dd = wizard.querySelector('[data-sum="' + key + '"]');
    if (!dd) return;
    dd.textContent = val || "—";
    dd.classList.toggle("empty", !val);
  }

  /* ---------- step navigation ---------- */
  function canLeave(n) {
    if (n === 1) return !!state.club;
    if (n === 2) return !!state.plan;
    if (n === 3) {
      var ok = true;
      wizard.querySelectorAll('[data-step="3"] input[required]').forEach(function (i) {
        var valid = i.value.trim() && i.checkValidity();
        i.style.borderBottomColor = valid ? "" : "var(--accent)";
        if (!valid) ok = false;
      });
      return ok;
    }
    if (n === 6) return wizard.querySelector("#agree").checked;
    return true; // 4 (family) and 5 (add-ons) are optional
  }
  function refreshNext() {
    if (step === 1) nextBtn.disabled = !state.club;
    else if (step === 2) nextBtn.disabled = !state.plan;
    else if (step === 6) nextBtn.disabled = !wizard.querySelector("#agree").checked;
    else nextBtn.disabled = false;
    nextBtn.querySelector(".lbl").textContent = step === TOTAL ? "Complete Membership" : "Continue";
  }
  function goStep(n) {
    if (n < 1 || n > TOTAL) return;
    step = n;
    stepsEls.forEach(function (s) { s.classList.toggle("is-active", +s.dataset.step === n); });
    navItems.forEach(function (li, i) {
      li.classList.toggle("is-active", i + 1 === n);
      li.classList.toggle("is-done", i + 1 < n);
    });
    barFill.style.width = (n / TOTAL) * 100 + "%";
    backBtn.classList.toggle("is-visible", n > 1);
    countEl.textContent = "Step 0" + n + " / 0" + TOTAL;
    if (n === 6) renderReview();
    refreshNext();
    var top = wizard.getBoundingClientRect().top + window.scrollY - 90;
    if (window.scrollY > top) window.scrollTo({ top: top, behavior: "smooth" });
  }

  /* ---------- step 1: club ---------- */
  wizard.querySelectorAll('[data-step="1"] .choice').forEach(function (c) {
    c.addEventListener("click", function () {
      wizard.querySelectorAll('[data-step="1"] .choice').forEach(function (x) { x.classList.remove("is-selected"); });
      c.classList.add("is-selected");
      state.club = c.dataset.club;
      renderSummary(); refreshNext();
      setTimeout(function () { goStep(2); }, 380);
    });
  });

  /* ---------- step 2: plan ---------- */
  wizard.querySelectorAll('[data-step="2"] .plan-card').forEach(function (c) {
    c.addEventListener("click", function () {
      wizard.querySelectorAll('[data-step="2"] .plan-card').forEach(function (x) { x.classList.remove("is-selected"); });
      c.classList.add("is-selected");
      state.plan = c.dataset.plan;
      state.primary = +c.dataset.primary;
      state.addl = +c.dataset.addl;
      state.enroll = +c.dataset.enroll;
      // Premier perk only relevant for Premier
      var pp = wizard.querySelector(".premier-perk");
      if (pp) pp.hidden = state.plan !== "Premier";
      renderSummary(); refreshNext();
      setTimeout(function () { goStep(3); }, 380);
    });
  });

  /* ---------- step 3: details ---------- */
  wizard.querySelectorAll('[data-step="3"] input').forEach(function (i) {
    i.addEventListener("input", function () { state[i.name] = i.value.trim(); renderReview(); });
  });

  /* ---------- step 4: family ---------- */
  var familyList = wizard.querySelector("#familyList");
  function renderFamily() {
    familyList.innerHTML = state.family.map(function (f, i) {
      return '<div class="family-row"><span class="family-row__n">' + (i + 1) + '</span>' +
        '<input type="text" placeholder="Family member name" value="' + (f.name || "") + '" data-fi="' + i + '">' +
        '<span class="family-row__price">' + (state.addl ? "+$" + state.addl + "/mo" : "") + '</span>' +
        '<button type="button" class="family-row__x" data-rm="' + i + '" aria-label="Remove">✕</button></div>';
    }).join("");
    familyList.querySelectorAll("[data-fi]").forEach(function (inp) {
      inp.addEventListener("input", function () { state.family[+inp.dataset.fi].name = inp.value; renderSummary(); });
    });
    familyList.querySelectorAll("[data-rm]").forEach(function (b) {
      b.addEventListener("click", function () { state.family.splice(+b.dataset.rm, 1); renderFamily(); renderSummary(); });
    });
    renderSummary();
  }
  wizard.querySelector(".add-family").addEventListener("click", function () {
    state.family.push({ name: "" }); renderFamily();
  });

  /* ---------- step 5: add-ons ---------- */
  wizard.querySelectorAll('.addon input[type="checkbox"]').forEach(function (cb) {
    cb.addEventListener("change", function () {
      var bucket = cb.dataset.addon === "onetime" ? state.onetime : state.monthly;
      var item = { label: cb.dataset.label, amt: +cb.dataset.amt };
      var idx = bucket.findIndex(function (x) { return x.label === item.label; });
      if (cb.checked && idx < 0) bucket.push(item);
      else if (!cb.checked && idx > -1) bucket.splice(idx, 1);
      cb.closest(".addon").classList.toggle("is-on", cb.checked);
      renderSummary();
    });
  });
  wizard.querySelectorAll(".premier-perk .seg button").forEach(function (b) {
    b.addEventListener("click", function () {
      wizard.querySelectorAll(".premier-perk .seg button").forEach(function (x) { x.classList.remove("is-on"); });
      b.classList.add("is-on");
      state.perk = b.dataset.perk;
      renderSummary();
    });
  });

  /* ---------- step 6: review + payment ---------- */
  function renderReview() {
    var list = wizard.querySelector("#reviewList");
    var rows = [
      ["Club", state.club],
      ["Membership", state.plan ? state.plan + " — " + money0(state.primary) + "/mo" : "—"],
      ["Member", (state.first + " " + state.last).trim() || "—"],
      ["Email", state.email || "—"],
      ["Phone", state.phone || "—"],
    ];
    state.family.forEach(function (f, i) { rows.push(["Family member " + (i + 1), (f.name || "Additional adult") + " — " + money0(state.addl) + "/mo"]); });
    if (state.plan === "Premier") rows.push(["Premier perk", state.perk]);
    state.monthly.forEach(function (a) { rows.push([a.label, money0(a.amt) + "/mo"]); });
    state.onetime.forEach(function (a) { rows.push([a.label, money0(a.amt) + " one-time"]); });
    rows.push(["Monthly total", money0(monthlyTotal()) + "/mo"]);
    rows.push(["Due today", money(dueToday())]);
    list.innerHTML = rows.map(function (r, i) {
      var strong = i >= rows.length - 2 ? " sum-row--total" : "";
      return '<div class="sum-row' + strong + '"><dt>' + r[0] + "</dt><dd>" + (r[1] || "—") + "</dd></div>";
    }).join("");
  }
  wizard.querySelectorAll('[data-step="6"] .seg button').forEach(function (b) {
    b.addEventListener("click", function () {
      wizard.querySelectorAll('[data-step="6"] .seg button').forEach(function (x) { x.classList.remove("is-on"); });
      b.classList.add("is-on"); state.pay = b.dataset.pay;
    });
  });
  wizard.querySelector("#agree").addEventListener("change", refreshNext);

  /* ---------- nav buttons ---------- */
  backBtn.addEventListener("click", function () { goStep(step - 1); });
  nextBtn.addEventListener("click", function () {
    if (!canLeave(step)) { refreshNext(); return; }
    if (step < TOTAL) { goStep(step + 1); return; }
    var success = document.querySelector(".join-success");
    var nameEl = success.querySelector("[data-success-name]");
    if (nameEl && state.first) nameEl.textContent = "Welcome to the Forma Family, " + state.first + ".";
    success.classList.add("is-open");
    document.body.style.overflow = "hidden";
  });

  renderSummary();
  refreshNext();
})();
