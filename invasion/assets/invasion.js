/* ------------------------------------------------------------------
   EDIT HERE: worship nights, links and videos.
   Each night: date (YYYY-MM-DD), time, church, city, register (URL).
   Leave date empty to show "Date coming"; leave register empty to
   send people to the host form until registration opens.
------------------------------------------------------------------- */
var INVASION = {
  nights: [
    { date: "", time: "7 PM", church: "[Church Name]", city: "[City, State]", register: "" },
    { date: "", time: "7 PM", church: "[Church Name]", city: "[City, State]", register: "" },
    { date: "", time: "7 PM", church: "[Church Name]", city: "[City, State]", register: "" }
  ],
  links: {
    youtube: "https://www.youtube.com/@InvasionMinistries",
    instagram: "https://instagram.com/invasionministries",
    facebook: "https://www.facebook.com/InvasionMinistries",
    email: "information@invasion.net",
    phone: "989-832-7547",
    give: "https://pushpay.com/g/marktbarclay?fnd=Invasion%20Youth%20%26%20Young%20Adults%20Conference"
  },
  videos: {
    "2026": [
      { id: "rE1CzPh3_bY", poster: "assets/clips/inv-wed.jpg", title: "Wednesday Night" },
      { id: "5No-xuEA0T0", clip: "inv-thu-worship", title: "Thursday Night" },
      { id: "yqpDQKF01e8", clip: "inv-fri-worship", title: "Friday Night" },
      { id: "onCNPrUt8Uw", clip: "inv-fri-baptism", title: "Testimonies" }
    ],
    past: [
      { id: "gTwzLdiZFq0", clip: "inv-rev-fri", title: "Friday Night", where: "Revolution 2025" },
      { id: "9pANd2JE7Jo", clip: "inv-rev-thu", title: "Thursday Night", where: "Revolution 2025" },
      { id: "OwJDddSvsp8", clip: "inv-free-crowd", title: "Conference Opener", where: "Freedom 2024" },
      { id: "rOewvj6FCJE", clip: "inv-wholeroom", title: "Whole Room (Live)", where: "Invasion Worship" }
    ]
  }
};

(function () {
  var L = INVASION.links;
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Nav turns solid after the hero (or right away on inner pages)
  var nav = document.querySelector("[data-nav]");
  var solidAt = document.querySelector(".hero") ? window.innerHeight * 0.6 : 10;
  function onScroll() { nav.classList.toggle("solid", window.scrollY > solidAt); }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  // Links
  var hrefs = {
    youtube: L.youtube, instagram: L.instagram, facebook: L.facebook, give: L.give,
    email: "mailto:" + L.email, phone: "tel:" + L.phone.replace(/\D/g, "")
  };
  document.querySelectorAll("[data-link]").forEach(function (a) {
    var k = a.getAttribute("data-link");
    a.href = hrefs[k];
    if (k === "email" && !a.textContent.trim()) a.textContent = L.email;
    if (k === "phone" && !a.textContent.trim()) a.textContent = L.phone;
    if (/^https?:/.test(a.href)) { a.target = "_blank"; a.rel = "noopener"; }
  });

  // Social icons
  var icons = {
    youtube: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12 31 31 0 0 0 1 16.8a3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .5-4.8 31 31 0 0 0-.5-4.8zM9.7 15.1V8.9l5.8 3.1z"/></svg>',
    instagram: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 3.3.1 4.8 1.7 4.9 4.9.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 3.2-1.7 4.8-4.9 4.9-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-3.3-.1-4.8-1.7-4.9-4.9C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8C2.4 3.9 3.9 2.4 7.2 2.3c1.2-.1 1.6-.1 4.8-.1zM12 0C8.7 0 8.3 0 7.1.1 2.7.3.3 2.7.1 7.1 0 8.3 0 8.7 0 12s0 3.7.1 4.9c.2 4.4 2.6 6.8 7 7 1.2.1 1.6.1 4.9.1s3.7 0 4.9-.1c4.4-.2 6.8-2.6 7-7 .1-1.2.1-1.6.1-4.9s0-3.7-.1-4.9c-.2-4.4-2.6-6.8-7-7C15.7 0 15.3 0 12 0zm0 5.8a6.2 6.2 0 1 0 0 12.4 6.2 6.2 0 0 0 0-12.4zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-11.8a1.4 1.4 0 1 0 0 2.9 1.4 1.4 0 0 0 0-2.9z"/></svg>',
    facebook: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M24 12a12 12 0 1 0-13.9 11.9v-8.4h-3V12h3V9.4c0-3 1.8-4.7 4.5-4.7 1.3 0 2.7.2 2.7.2v3h-1.5c-1.5 0-2 .9-2 1.9V12h3.4l-.5 3.5h-2.9v8.4A12 12 0 0 0 24 12z"/></svg>'
  };
  var names = { youtube: "YouTube", instagram: "Instagram", facebook: "Facebook" };
  var handles = { youtube: "@InvasionMinistries", instagram: "@invasionministries", facebook: "InvasionMinistries" };
  document.querySelectorAll("[data-social-icons]").forEach(function (box) {
    ["youtube", "instagram", "facebook"].forEach(function (k) {
      var a = document.createElement("a");
      a.href = L[k]; a.target = "_blank"; a.rel = "noopener"; a.setAttribute("aria-label", names[k]);
      a.innerHTML = icons[k]; box.appendChild(a);
    });
  });
  document.querySelectorAll("[data-social-big]").forEach(function (box) {
    ["youtube", "instagram", "facebook"].forEach(function (k) {
      var a = document.createElement("a");
      a.className = "follow-link"; a.href = L[k]; a.target = "_blank"; a.rel = "noopener";
      a.innerHTML = icons[k] + "<span><strong>" + names[k] + "</strong><small>" + handles[k] + "</small></span><i aria-hidden=\"true\">↗</i>";
      box.appendChild(a);
    });
  });

  // Worship nights
  var list = document.querySelector("[data-nights]");
  if (list) {
    var months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
    var days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    INVASION.nights.forEach(function (n) {
      var li = document.createElement("li");
      var d = n.date ? new Date(n.date + "T12:00:00") : null;
      li.className = "night";
      li.innerHTML = '<div class="night-date">' + (d
        ? months[d.getMonth()] + " " + d.getDate() + "<small>" + days[d.getDay()] + " · " + n.time + "</small>"
        : "Soon<small>Date coming</small>") + '</div>' +
        '<div class="night-where"><h3></h3><p></p></div>' +
        '<a class="btn">Register</a>';
      li.querySelector("h3").textContent = n.church;
      li.querySelector("p").textContent = n.city;
      var a = li.querySelector("a");
      a.href = n.register || "#host";
      if (n.register) { a.target = "_blank"; a.rel = "noopener"; }
      list.appendChild(li);
    });
  }

  // Video cards: local muted loop on hover, full YouTube video on click
  function card(v, big) {
    var a = document.createElement("a");
    a.className = "vcard" + (big ? " big" : "");
    a.href = "https://www.youtube.com/watch?v=" + v.id;
    a.setAttribute("data-yt", v.id);
    a.innerHTML =
      '<div class="vthumb"><img src="' + (v.poster || "assets/clips/" + v.clip + ".jpg") + '" alt="" loading="lazy">' +
      (v.clip ? '<video muted loop playsinline preload="none"><source src="assets/clips/' + v.clip + '.mp4" type="video/mp4"></video>' : "") +
      '<span class="play" aria-hidden="true"></span></div>' +
      '<div class="vmeta"><h3></h3>' + (v.where ? "<p></p>" : "") + "</div>";
    a.querySelector("h3").textContent = v.title;
    if (v.where) a.querySelector("p").textContent = v.where;
    var vid = a.querySelector("video");
    if (vid && !reduce) {
      a.addEventListener("mouseenter", function () { vid.play().catch(function () {}); });
      a.addEventListener("mouseleave", function () { vid.pause(); });
    }
    return a;
  }
  document.querySelectorAll(".video-feature").forEach(function (box) {
    var v = { id: box.dataset.video, clip: box.dataset.clip, poster: box.dataset.poster, title: box.dataset.title };
    var c = card(v, true);
    box.appendChild(c);
    // Big feature cards play their loop whenever they're on screen
    var vid = c.querySelector("video");
    if (vid && !reduce && "IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) vid.play().catch(function () {}); else vid.pause(); });
      }, { threshold: 0.4 }).observe(c);
    }
  });
  document.querySelectorAll("[data-videos]").forEach(function (box) {
    (INVASION.videos[box.dataset.videos] || []).forEach(function (v) { box.appendChild(card(v)); });
  });

  // Player modal
  var player = document.querySelector("[data-player]");
  if (player) {
    var frame = player.querySelector("[data-player-frame]"), yt = player.querySelector("[data-player-yt]");
    function close() { player.hidden = true; frame.innerHTML = ""; document.body.style.overflow = ""; }
    document.addEventListener("click", function (e) {
      var a = e.target.closest("[data-yt]");
      if (!a || e.metaKey || e.ctrlKey) return;
      e.preventDefault();
      var id = a.getAttribute("data-yt");
      frame.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen title="Video"></iframe>';
      yt.href = "https://www.youtube.com/watch?v=" + id;
      player.hidden = false; document.body.style.overflow = "hidden";
    });
    player.querySelector("[data-player-close]").addEventListener("click", close);
    player.addEventListener("click", function (e) { if (e.target === player) close(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !player.hidden) close(); });
  }

  // Host form opens an email until a form service is connected
  var host = document.querySelector("[data-host-form]");
  if (host) host.addEventListener("submit", function (e) {
    e.preventDefault();
    var body = [];
    new FormData(host).forEach(function (v, k) { body.push(k + ": " + v); });
    location.href = "mailto:" + L.email + "?subject=" + encodeURIComponent("Host an Invasion Worship Night") + "&body=" + encodeURIComponent(body.join("\n"));
    host.innerHTML = '<p class="done">Thank you. We\'ll be in touch.</p>';
  });

  document.querySelectorAll("[data-year]").forEach(function (s) { s.textContent = new Date().getFullYear(); });

  // Reveal on scroll
  var targets = document.querySelectorAll(".section-head,.night,.vcard,.mosaic img,.team-hero,.team-copy,.team-photos,.thirty-grid > *,.host-grid > *,.follow h2,.follow-link,.story > *,.timeline li");
  targets.forEach(function (t) { t.classList.add("reveal"); });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    targets.forEach(function (t) { io.observe(t); });
  } else targets.forEach(function (t) { t.classList.add("in"); });
})();
