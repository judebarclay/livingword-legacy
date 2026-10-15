/* ------------------------------------------------------------------
   EDIT HERE: worship nights, links and videos.
   Each night: date (YYYY-MM-DD), time, church, city, register (URL).
   Leave date empty to show "Date coming"; leave register empty to
   send people to the host form until registration opens.
------------------------------------------------------------------- */
var INVASION = {
  nights: [
    { date: "2026-11-11", time: "7 PM", church: "Covenant of Peace International", city: "Dayton, OH", register: "" },
    { date: "2026-11-12", time: "7 PM", church: "Lake Michigan Christian Center", city: "Bridgman, MI", register: "" },
    { date: "2026-11-13", time: "7 PM", church: "Resurrection Life Church", city: "Clarksville, IN", register: "" }
  ],
  links: {
    youtube: "https://www.youtube.com/@InvasionMinistries",
    instagram: "https://instagram.com/invasionministries",
    facebook: "https://www.facebook.com/InvasionMinistries",
    email: "information@invasion.net",
    phone: "989-832-7547",
    give: "https://pushpay.com/g/marktbarclay?fnd=Invasion%20Youth%20%26%20Young%20Adults%20Conference"
  },
  testimonies: [
    { id: "onCNPrUt8Uw", clip: "test-glasses", q: "I came here wearing glasses, and I don't need them anymore." },
    { id: "onCNPrUt8Uw", clip: "test-anxiety", q: "The morning of Invasion I got set free. I haven't had an anxiety attack since." },
    { id: "onCNPrUt8Uw", clip: "test-chains", q: "Come to Invasion so God can break your chains and you can find His purpose for you." },
    { id: "onCNPrUt8Uw", clip: "test-joy", q: "I got freed from a generational curse, and the Lord filled me with His joy." },
    { id: "onCNPrUt8Uw", clip: "test-saved", q: "I gave my heart to Jesus, and today I got baptized." }
  ],
  moments: [
    { id: "rE1CzPh3_bY", clip: "inv-wed-band", t: "Nightly worship", p: "Every night at 7 PM the whole room comes together." },
    { id: "onCNPrUt8Uw", clip: "inv-fri-baptism", t: "Baptisms", p: "Young people going public with their faith." },
    { id: "gTwzLdiZFq0", clip: "inv-rev-fri", t: "Encounter", p: "Every service ends with space to respond and meet God." },
    { link: "https://instagram.com/invasionministries", clip: "inv-thu-sports", t: "Sports and tournaments", p: "Volleyball, basketball, eSports and more, with real trophies." }
  ],
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
      a.href = n.register || "mailto:" + L.email + "?subject=" + encodeURIComponent("Register: " + n.city + " worship night");
      if (n.register) { a.target = "_blank"; a.rel = "noopener"; }
      list.appendChild(li);
    });
  }

  // Video cards: the clip loops on the page; tapping plays the full video right there
  var playIcon = '<span class="play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>';
  // Full videos are hosted with the site and play in a native player
  function embed(id, start, muted) {
    return '<video class="full" controls playsinline autoplay' + (muted ? " muted loop" : "") +
      ' preload="auto" poster="assets/full/' + id + '.jpg"><source src="assets/full/' + id + '.mp4' + (start ? "#t=" + start : "") + '" type="video/mp4"></video>';
  }
  function stopOthers(keep) {
    document.querySelectorAll("video.full").forEach(function (v) { if (v !== keep) v.pause(); });
  }
  function playIn(box, id, start) {
    box.querySelectorAll("video").forEach(function (v) { v.pause(); });
    box.innerHTML = embed(id, start);
    box.classList.add("playing");
    var v = box.querySelector("video");
    stopOthers(v);
    v.play().catch(function () { v.muted = true; v.play().catch(function () {}); });
  }
  var loops = [];
  function loopVideo(clip, poster) {
    if (!clip) return '<img src="' + poster + '" alt="" loading="lazy">';
    return '<video muted loop playsinline preload="none" poster="' + (poster || "assets/clips/" + clip + ".jpg") + '"><source src="assets/clips/' + clip + '.mp4" type="video/mp4"></video>';
  }
  function card(v, big) {
    var a = document.createElement("a");
    a.className = "vcard" + (big ? " big" : "");
    a.href = "https://www.youtube.com/watch?v=" + v.id;
    a.innerHTML = '<div class="vthumb">' + loopVideo(v.clip, v.poster) + playIcon + '</div>' +
      '<div class="vmeta"><h3></h3>' + (v.where ? "<p></p>" : "") + "</div>";
    a.querySelector("h3").textContent = v.title;
    if (v.where) a.querySelector("p").textContent = v.where;
    a.addEventListener("click", function (e) {
      if (a.dataset.on) return;
      if (e.metaKey || e.ctrlKey) return;
      e.preventDefault();
      a.dataset.on = 1; a.removeAttribute("href");
      playIn(a.querySelector(".vthumb"), v.id);
    });
    return a;
  }
  document.querySelectorAll(".video-feature").forEach(function (box) {
    var d = box.dataset;
    box.appendChild(card({ id: d.video, clip: d.clip, poster: d.poster, title: d.title, where: d.where }, true));
  });
  document.querySelectorAll("[data-videos]").forEach(function (box) {
    (INVASION.videos[box.dataset.videos] || []).forEach(function (v) { box.appendChild(card(v)); });
  });

  // Testimonies: each card plays the testimony video in the player above
  var tGrid = document.querySelector("[data-testimonies]");
  if (tGrid) INVASION.testimonies.forEach(function (t) {
    var a = document.createElement("a");
    a.className = "tcard"; a.href = "https://www.youtube.com/watch?v=" + t.id + (t.at ? "&t=" + t.at + "s" : "");
    a.innerHTML = '<div class="tvid">' + loopVideo(t.clip) + playIcon + '</div><p></p>';
    a.querySelector("p").textContent = "“" + t.q + "”";
    a.addEventListener("click", function (e) {
      if (e.metaKey || e.ctrlKey) return;
      e.preventDefault();
      var box = document.querySelector("#testi-player .vthumb");
      playIn(box, t.id, t.at);
      box.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "center" });
    });
    tGrid.appendChild(a);
  });

  // Moments: looping tiles, each plays its video
  var bento = document.querySelector("[data-moments]");
  if (bento) INVASION.moments.forEach(function (m) {
    var a = document.createElement("a");
    a.className = "bento-item"; a.href = m.link || "https://www.youtube.com/watch?v=" + m.id;
    a.innerHTML = loopVideo(m.clip) + '<span class="bento-in"><b></b><span></span></span>' + (m.id ? playIcon : "");
    a.querySelector("b").textContent = m.t;
    a.querySelector(".bento-in span").textContent = m.p;
    if (m.id) a.addEventListener("click", function (e) {
      if (a.dataset.on) return;
      if (e.metaKey || e.ctrlKey) return;
      e.preventDefault();
      a.dataset.on = 1; a.removeAttribute("href");
      a.classList.add("playing");
      playIn(a, m.id);
    });
    else { a.target = "_blank"; a.rel = "noopener"; }
    bento.appendChild(a);
  });

  // Every loop on the page plays while it's on screen
  var vids = document.querySelectorAll(".vthumb video, .tvid video, .bento-item video, .feature-media");
  if (!reduce && "IntersectionObserver" in window) {
    var vio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.target.isConnected) return;
        if (e.isIntersecting) { inView.add(e.target); e.target.play().catch(function () {}); }
        else { inView.delete(e.target); e.target.pause(); }
      });
    }, { rootMargin: "200px" });
    vids.forEach(function (v) { v.muted = true; vio.observe(v); });
  }
  // iPhones in Low Power Mode block autoplay; the first tap or scroll touch starts the loops
  var inView = new Set();
  var hero = document.querySelector(".hero-video");
  if (hero) inView.add(hero);
  function kick() {
    inView.forEach(function (v) { if (v.isConnected && v.paused) v.play().catch(function () {}); });
  }
  ["touchend", "click", "keydown"].forEach(function (ev) { document.addEventListener(ev, kick, { passive: true }); });

  // Tribute: plays on its own (muted) as soon as it scrolls into view
  document.querySelectorAll("[data-autoplay-video]").forEach(function (box) {
    var id = box.getAttribute("data-autoplay-video"), started = false;
    function go() {
      if (started) return; started = true;
      box.innerHTML = embed(id, 0, true);
      var v = box.querySelector("video");
      v.play().catch(function () {});
    }
    box.innerHTML = '<img src="' + (box.dataset.poster || "assets/full/" + id + ".jpg") + '" alt="">';
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es, o) { if (es[0].isIntersecting) { go(); o.disconnect(); } }, { rootMargin: "300px" }).observe(box);
    } else go();
  });

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
  var targets = document.querySelectorAll(".section-head,.tcard,.bento-item,.year,.night,.vcard,.mosaic img,.team-hero,.team-copy,.team-photos,.thirty-grid > *,.host-grid > *,.follow h2,.follow-link,.story > *,.timeline li");
  targets.forEach(function (t) { t.classList.add("reveal"); });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    targets.forEach(function (t) { io.observe(t); });
  } else targets.forEach(function (t) { t.classList.add("in"); });
})();
