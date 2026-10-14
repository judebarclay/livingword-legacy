/* ------------------------------------------------------------------
   EDIT HERE: worship nights and contact details.
   Each night: date (YYYY-MM-DD), time, church, city, register (URL).
   Leave date empty to show a "date coming soon" row.
------------------------------------------------------------------- */
var INVASION = {
  nights: [
    { date: "", time: "7 PM", church: "[Church Name]", city: "[City, State]", register: "" },
    { date: "", time: "7 PM", church: "[Church Name]", city: "[City, State]", register: "" },
    { date: "", time: "7 PM", church: "[Church Name]", city: "[City, State]", register: "" }
  ],
  contactEmail: "[email]",   // host requests and updates go here
  instagram: ""              // full Instagram URL
};

(function () {
  // Nav turns solid after the hero
  var nav = document.querySelector("[data-nav]");
  function onScroll() { nav.classList.toggle("solid", window.scrollY > window.innerHeight * 0.6); }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  // Rotating word
  var words = ["Revival.", "Breakthrough.", "Healing.", "Freedom."];
  var el = document.querySelector("[data-rotate]"), i = 0;
  if (el && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    setInterval(function () {
      el.classList.add("out");
      setTimeout(function () { i = (i + 1) % words.length; el.textContent = words[i]; el.classList.remove("out"); }, 450);
    }, 2200);
  }

  // Nights list
  var list = document.querySelector("[data-nights]");
  var months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  var days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
  INVASION.nights.forEach(function (n) {
    var li = document.createElement("li");
    var d = n.date ? new Date(n.date + "T12:00:00") : null;
    li.className = "night reveal" + (d ? "" : " tba");
    var dateHtml = d
      ? months[d.getMonth()] + " " + d.getDate() + "<small>" + days[d.getDay()] + " · " + n.time + "</small>"
      : "Soon<small>Date coming</small>";
    var href = n.register || "#updates";
    var label = n.register ? "Register" : "Get notified";
    li.innerHTML = '<div class="night-date">' + dateHtml + '</div>' +
      '<div class="night-where"><h3></h3><p></p></div>' +
      '<a class="btn" href="' + href + '">' + label + '</a>';
    li.querySelector("h3").textContent = n.church;
    li.querySelector("p").textContent = n.city;
    list.appendChild(li);
  });

  // Film tabs
  var video = document.querySelector("[data-film-video]");
  document.querySelectorAll("[data-film]").forEach(function (b) {
    b.addEventListener("click", function () {
      document.querySelectorAll("[data-film]").forEach(function (x) { x.setAttribute("aria-selected", x === b); });
      var k = b.getAttribute("data-film");
      video.pause();
      video.poster = "assets/img/" + k + "-poster.jpg";
      video.querySelector("source").src = "assets/video/" + k + ".mp4";
      video.load();
    });
  });

  // Forms open an email until a form service is connected
  function mailForm(form, subject) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = new FormData(form), body = [];
      data.forEach(function (v, k) { body.push(k + ": " + v); });
      if (INVASION.contactEmail.indexOf("@") > 0) {
        location.href = "mailto:" + INVASION.contactEmail + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body.join("\n"));
      }
      form.innerHTML = '<p class="done">Thank you. We\'ll be in touch.</p>';
    });
  }
  var host = document.querySelector("[data-host-form]"); if (host) mailForm(host, "Host an Invasion worship night");
  var upd = document.querySelector("[data-updates-form]"); if (upd) mailForm(upd, "Invasion updates");

  if (INVASION.instagram) document.querySelectorAll('[data-social="instagram"]').forEach(function (a) { a.href = INVASION.instagram; });
  document.querySelectorAll("[data-year]").forEach(function (s) { s.textContent = new Date().getFullYear(); });

  // Reveal on scroll
  var targets = document.querySelectorAll(".section-head,.card,.team-copy,.team-photos,.mosaic img,.next,.host-grid > *,.updates h2,.night");
  targets.forEach(function (t) { t.classList.add("reveal"); });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    targets.forEach(function (t) { io.observe(t); });
  } else targets.forEach(function (t) { t.classList.add("in"); });
})();
