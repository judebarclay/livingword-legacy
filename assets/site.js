/* ============================================================
   SITE CONFIG. Everything brand-specific lives here.
   livingwordchurch.com shows Living Word; legacychurchmidland.com
   shows Legacy. Anywhere else (previews) add ?brand=legacy or
   ?brand=livingword, or use the switch in the corner.
   ============================================================ */

/* Subsplash live player: paste the iframe "src" from Subsplash
   (Dashboard > Live > Embed). Leave "" to show YouTube + app buttons. */
var LIVE = {
  subsplashEmbed: "",
  timezone: "America/Detroit",
  /* day: 0 = Sunday ... 4 = Thursday. 24h times, local to timezone. */
  services: [
    { day: 0, start: "09:55", end: "11:45", name: "Sunday Morning Service" },
    { day: 0, start: "17:55", end: "19:45", name: "Sunday Night Service" },
    { day: 4, start: "18:55", end: "20:45", name: "Thursday Night Service" }
  ]
};

var BRANDS = {
  livingword: {
    domain: "livingwordchurch.com",
    name: "Living Word Church",
    tagline: "Experience Jesus"
  },
  legacy: {
    domain: "legacychurchmidland.com",
    name: "Legacy Church",
    tagline: "Faith for generations"
  }
};

(function () {
  var html = document.documentElement;
  var brand = html.getAttribute("data-brand") || "livingword";
  var host = location.hostname.replace(/^www\./, "");
  var onLiveDomain = false;
  for (var k in BRANDS) if (host === BRANDS[k].domain) onLiveDomain = true;
  var forceLive = /[?&]live=1/.test(location.search);

  function all(s, root) { return Array.prototype.slice.call((root || document).querySelectorAll(s)); }

  /* Keep ?brand= on internal links while previewing */
  if (!onLiveDomain) {
    all("a[href]").forEach(function (a) {
      var h = a.getAttribute("href");
      if (/^(https?:|mailto:|tel:|#)/.test(h)) return;
      a.setAttribute("href", h + (h.indexOf("?") > -1 ? "&" : "?") + "brand=" + brand);
    });
  }

  /* Brand text */
  var b = BRANDS[brand];
  all("[data-b]").forEach(function (el) { var f = el.getAttribute("data-b"); if (b[f]) el.textContent = b[f]; });
  document.title = document.title.replace(/Living Word Church|Legacy Church/g, b.name);
  all("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* Menu */
  var menu = document.querySelector("[data-menu]");
  all("[data-menu-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var open = menu.hasAttribute("hidden");
      if (open) menu.removeAttribute("hidden"); else menu.setAttribute("hidden", "");
      html.classList.toggle("menu-open", open);
      all("[data-menu-toggle]").forEach(function (x) { x.setAttribute("aria-expanded", String(open)); });
    });
  });

  /* Nav background after scrolling past the hero */
  var nav = document.querySelector(".nav");
  function onScroll() { nav.classList.toggle("scrolled", window.scrollY > 40); }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* Reveal on scroll (Legacy photos turn from black and white to color) */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.25 });
    all(".reveal").forEach(function (el) { io.observe(el); });
  } else all(".reveal").forEach(function (el) { el.classList.add("in"); });

  /* FAQ: only one open at a time */
  all(".faq details").forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (d.open) all(".faq details").forEach(function (o) { if (o !== d) o.open = false; });
    });
  });

  /* Preview switch (hidden on the real domains) */
  var sw = document.querySelector("[data-switch]");
  if (sw && !onLiveDomain) {
    sw.hidden = false;
    all("[data-sw]", sw).forEach(function (btn) {
      btn.setAttribute("aria-pressed", String(btn.getAttribute("data-sw") === brand));
      btn.addEventListener("click", function () {
        var u = new URL(location.href); u.searchParams.set("brand", btn.getAttribute("data-sw")); location.href = u.toString();
      });
    });
    var lb = sw.querySelector("[data-sw-live]");
    lb.setAttribute("aria-pressed", String(forceLive));
    lb.addEventListener("click", function () {
      var u = new URL(location.href);
      if (forceLive) u.searchParams.delete("live"); else u.searchParams.set("live", "1");
      location.href = u.toString();
    });
  }

  /* ---------- Live service popup ---------- */
  function nowParts() {
    var fmt = new Intl.DateTimeFormat("en-US", { timeZone: LIVE.timezone, weekday: "short", hour: "2-digit", minute: "2-digit", hourCycle: "h23" });
    var p = {}; fmt.formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
    var days = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
    return { day: days[p.weekday], mins: parseInt(p.hour, 10) * 60 + parseInt(p.minute, 10) };
  }
  function toMins(t) { var a = t.split(":"); return +a[0] * 60 + +a[1]; }
  function currentService() {
    if (forceLive) return LIVE.services[0];
    var n = nowParts();
    for (var i = 0; i < LIVE.services.length; i++) {
      var s = LIVE.services[i];
      if (s.day === n.day && n.mins >= toMins(s.start) && n.mins <= toMins(s.end)) return s;
    }
    return null;
  }

  var modal = document.querySelector("[data-modal]");
  var player = document.querySelector("[data-player]");
  var fallbackHTML = player.innerHTML;
  var autoShown = false;

  function openLive() {
    var s = currentService();
    if (LIVE.subsplashEmbed) {
      player.innerHTML = '<iframe src="' + LIVE.subsplashEmbed + '" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen title="Live service"></iframe>';
    } else {
      player.innerHTML = fallbackHTML;
      player.querySelector("[data-fallback-title]").textContent = s ? s.name + " is live now" : "Watch the latest service";
    }
    modal.querySelector("[data-live-pill]").hidden = !s;
    modal.hidden = false;
    html.classList.add("modal-open");
  }
  function closeLive() { modal.hidden = true; player.innerHTML = fallbackHTML; html.classList.remove("modal-open"); }

  function refreshLive() {
    var s = currentService();
    var bar = document.querySelector("[data-live-bar]");
    bar.hidden = !s;
    html.classList.toggle("is-live", !!s);
    if (!s) return;
    all("[data-live-name]").forEach(function (el) { el.textContent = s.name; });
    var key = "live-popup-" + s.name, seen = false;
    try { seen = sessionStorage.getItem(key) === "1"; } catch (e) {}
    if (!seen && !autoShown) {
      autoShown = true;
      try { sessionStorage.setItem(key, "1"); } catch (e) {}
      openLive();
    }
  }

  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-open-live]")) { e.preventDefault(); openLive(); }
    if (e.target.closest("[data-close]") || e.target === modal) closeLive();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    if (!modal.hidden) closeLive();
    else if (!menu.hasAttribute("hidden")) document.querySelector("[data-menu-toggle]").click();
  });

  refreshLive();
  setInterval(refreshLive, 60000);
})();
