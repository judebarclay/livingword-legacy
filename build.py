#!/usr/bin/env python3.12
"""Builds two separate websites from one set of content:
livingword/  ->  livingwordchurch.com   (white, bold grotesque)
legacy/      ->  legacychurchmidland.com (black, cinematic serif)


Run:  python3.12 build.py   (needs Python 3.12+)
Each site folder is self-contained (its own pages and assets/ copy) so it
can be deployed to its own domain. Edit shared look in assets/site.css and
the live popup in assets/site.js, then rebuild.
"""
import html
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- links
L = {
    "connect": "https://livingwordmi.churchcenter.com/people/forms/965780",
    "membership": "https://livingwordmi.churchcenter.com/people/forms/988734",
    "baptism": "https://livingwordmi.churchcenter.com/people/forms/955187",
    "prayer_form": "https://livingwordmi.churchcenter.com/people/forms/750697",
    "decided": "https://livingwordmi.churchcenter.com/people/forms/990118",
    "question": "https://livingwordmi.churchcenter.com/people/forms/990128",
    "calendar": "https://livingwordmi.churchcenter.com/calendar",
    "give": "https://pushpay.com/g/livingwordchurchmi",
    "smti": "https://www.smtionline.com",
    "invasion": "https://invasion.net",
    "ya_hang": "https://launcher.nucleus.church/launcher/4df88bb03231e4f1aacf?nucleuslauncher=open&nlinfocard=infocard_eaeffbfe31d341c19741eaa900fdfafe",
    "youtube": "https://www.youtube.com/@LivingWordChurchMidland",
    "youtube_streams": "https://www.youtube.com/@LivingWordChurchMidland/streams",
    "youtube_live": "https://www.youtube.com/@LivingWordChurchMidland/live",
    "appstore": "https://apps.apple.com/us/app/base-by-mark-t-barclay/id631514907",
    "play": "https://play.google.com/store/apps/details?id=com.marktbarclay.markbarclayministries199app",
    "instagram": "https://www.instagram.com/livingwordchurchmidland/",
    "facebook": "https://www.facebook.com/livingwordchurchmidland",
    "map": "https://maps.google.com/?q=2010+N+Stark+Rd+Midland+MI+48642",
    "map_embed": "https://maps.google.com/maps?q=2010%20N%20Stark%20Rd%2C%20Midland%2C%20MI%2048642&z=14&output=embed",
}

# ---------------------------------------------------------------- photos
# All from the current livingwordchurch.com media library.
# Served resized through images.weserv.nl so phones don't download 8K originals.
NUC = "cdn1.nucleus-cdn.church/church_64c360e7eb284f29be806893ed84daff/"
IMG = {
    "hands": "file_171be67154f94b81ac461ff12ccb1770/2025-03-07T16:07:58.425Z/0F7A0657.jpg",
    "crowd": "file_0e5c261711d54737a3ad544d117f8153/2025-06-26T23:29:04.071Z/0F7A7996-2.jpg",
    "welcome": "file_34a5fd01d6734be8b906e47906b5adc0/2025-06-12T22:06:53.714Z/0F7A0091.jpg",
    "smoke": "file_26b54d6541c24756b5acf4795824a3e4/2025-01-12T22:14:47.208Z/IMGC6608.jpg",
    "kids": "file_8cf076061bea4e33ba2e495d00f00474/2025-01-12T16:00:20.950Z/Untitled-39.jpg",
    "youth_room": "file_e78f58de79f74219b3d7d0ed1025bda1/2025-06-12T20:03:20.797Z/0F7A8440.jpg",
    "youth_braid": "file_4151fade796e4dccbdec081650fdae95/2025-06-12T19:51:30.296Z/0F7A8474.jpg",
    "youth_mic": "file_200abcaf19df43ccbd885e08c919b42b/2025-06-12T19:51:20.657Z/0F7A8424.jpg",
    "youth_circle": "file_63f00376b3c6485f8fc6f03e0a053869/2025-06-12T20:05:32.708Z/0F7A8523.jpg",
    "ya": "file_d89d489a0ddc4229b7de27a1d4583391/2025-06-12T21:06:18.845Z/0F7A8911.jpg",
    "prayer": "file_20110bae743d4a4e8c79aeab8681fa17/2025-06-16T21:02:50.402Z/0F7A0031.jpg",
    "kneel": "file_046f8474632841f4acdd36bc2f40765a/2025-06-13T18:34:41.432Z/0F7A1473.jpg",
    "baptism": "file_7eb50be9c6584735a5366c580a0b7069/2025-04-23T22:44:03.519Z/0F7A8838.jpg",
    "building": "file_893e28c8e38d4f7183f571cf948d16d8/2025-03-24T21:44:33.967Z/LIVING_WORD_CHURCH_OUTSIDE_ROAD_.jpg",
    "outreach": "file_d7139930b6ca4b19a3cff92a7409b23c/2024-12-22T20:45:20.514Z/Untitled-2595.jpg",
    "outreach_crowd": "file_818336e49b874847a3d5f1ba61ae5a6c/2024-12-22T20:43:28.559Z/Untitled-2583.jpg",
    "heart": "file_83b84c252df34868a50a00cceab21666/2024-12-22T20:43:39.358Z/Untitled-2602.jpg",
    "missions": "file_ea3d06991f694661831889bd7a202b71/2024-12-22T20:46:23.487Z/0F7A0489.jpg",
    "hall": "file_d01d03400f6d4e26a36274cd49eaedf1/2025-06-12T23:31:45.304Z/LWOC_Jaycee_Hall_B_W_1.jpg",
    "dedication": "file_4f5fd551edb24811a7bdbfc7ac57f5b1/2025-06-13T00:04:39.864Z/Church_Dedication_May__1981_Congregation_4.jpg",
    "frame": "file_6b472f13503b416ba60bb493817f9944/2025-06-13T00:02:22.785Z/LWC_Building_Frame.jpg",
    "lake": "file_070a1acd93974e348eaf0795937c8543/2025-06-13T00:00:57.208Z/Dawn_R_Lake_Baptism_MTB_1980_1.jpg",
    "cali": "file_d86c4a5bd7dd4a759a58d2ca21f243fe/2025-06-12T23:49:41.348Z/Cali_MTB_Preaching_1__5_-2.jpg",
    # Mark T. Barclay on stage with WELCOME on the screen, cropped in around him
    "grandpa_welcome": "file_2c3af27266584ac59f76d542b9ef1aa2/2025-06-13T00:22:55.665Z/IMG_3248.jpg&cx=0&cy=1350&cw=2900&ch=1450&precrop",
    "baptism_practice": "file_f5ab36f40d32454ba092768e9c58b24e/2025-06-13T00:00:23.831Z/SMTI_Baptism_Practice_1.jpg",
    "bensch_family": "file_75ae3a4e8f454fd2bce13f5be6f29e6d/2025-06-13T00:00:32.270Z/Ray_Bensch___Family_1.jpg",
    "seminar": "file_7cd9df32e3894236bbc79069393bf2ee/2025-06-13T00:00:39.967Z/MTB_Teaching_SMTI_H._S._Seminar__2.jpg",
    "gathering": "file_9c0d5454e7cc45b9b2ce6baf12d470e8/2025-06-12T23:52:04.123Z/Misc._1.jpg",
}


def src(key, w=1600):
    return f"https://images.weserv.nl/?url={NUC}{IMG[key]}&w={w}&output=jpg&q=80"


def img(key, alt, w=1600, cls="", pos=None, eager=False):
    srcset = ", ".join(f"{src(key, x)} {x}w" for x in (800, 1600, 2400) if x <= max(w, 800) * 1.5)
    style = f' style="object-position:{pos}"' if pos else ""
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{src(key, w)}" srcset="{srcset}" sizes="100vw" alt="{html.escape(alt)}" '
            f'{loading} decoding="async"{style}>')


NAME = '<span data-b="name">Living Word Church</span>'
TIMES = "Sundays 10 AM &amp; 6 PM · Thursdays 7 PM"

# ---------------------------------------------------------------- navigation
NAV = [("new-here.html", "New Here"), ("next-steps.html", "Next Steps"), ("watch.html", "Watch"),
       ("our-story.html", "Our Story")]
MENU = [
    ("Visit", [("index.html", "Home"), ("new-here.html", "New Here"), ("plan-a-visit.html", "Visit + FAQ"),
               ("calendar.html", "Calendar")]),
    ("Grow", [("next-steps.html", "Next Steps"), ("jesus.html", "Know Jesus"), ("prayer.html", "Prayer"),
              ("watch.html", "Watch")]),
    ("Family", [("kids.html", "Life Kids"), ("youth.html", "Life Youth"), ("young-adults.html", "Young Adults")]),
    ("About", [("our-story.html", "Our Story"), ("leadership.html", "Leadership"), ("give.html", "Give")]),
]

ICON_ARROW = '<svg class="i" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
ICON_OUT = '<svg class="i" viewBox="0 0 16 16" aria-hidden="true"><path d="M5 11 11 5M6 5h5v5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'


def a(href, label, cls="btn"):
    ext = href.startswith("http")
    tgt = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="{cls}" href="{href}"{tgt}>{label}{ICON_OUT if ext else ICON_ARROW}</a>'


BRAND = {"key": "livingword"}
SITES = {
    "livingword": {"name": "Living Word Church", "tagline": "Experience Jesus", "og": "hands"},
    "legacy": {"name": "Legacy Church", "tagline": "Faith for generations.", "og": "smoke"},
}


def wordmark():
    if BRAND["key"] == "legacy":
        return '<span class="wm wm-lg"><b>Legacy</b> <small>Church</small></span>'
    return '<span class="wm wm-lw"><b>Living Word</b> <i>Church</i></span>'



def layout(slug, title, desc, body):
    links = "".join(f'<a href="{h}"{" aria-current=page" if h == slug + ".html" else ""}>{t}</a>' for h, t in NAV)
    menu = "".join(
        f'<div class="menu-col"><p class="eyebrow">{g}</p>' +
        "".join(f'<a href="{h}">{t}</a>' for h, t in items) + "</div>" for g, items in MENU)
    site = SITES[BRAND["key"]]
    return f"""<!doctype html>
<html lang="en" data-brand="{BRAND['key']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · {site['name']}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{src(site['og'], 1200)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.weserv.nl">
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
</head>
<body class="p-{slug}">
<a class="skip" href="#main">Skip to content</a>
<div class="livebar" data-live-bar hidden>
  <span class="dot"></span><span><b>Live now</b> · <span data-live-name>Service</span></span>
  <button type="button" data-open-live>Watch</button>
</div>
<header class="nav">
  <a class="brand" href="index.html" aria-label="Home">{wordmark()}</a>
  <nav class="links" aria-label="Main">{links}</nav>
  <div class="nav-end">
    <a class="btn btn-sm btn-solid" href="give.html">Give</a>
    <button class="burger" type="button" data-menu-toggle aria-expanded="false" aria-label="Menu"><span></span><span></span></button>
  </div>
</header>
<div class="menu" data-menu hidden>
  <div class="menu-inner">{menu}</div>
  <div class="menu-foot"><p>{TIMES}</p><p>2010 N Stark Rd, Midland, MI</p></div>
</div>
<main id="main">
{body}
</main>
{footer()}
{live_modal()}
<script src="assets/site.js"></script>
</body>
</html>
"""


def footer():
    cols = "".join(
        f'<div><p class="eyebrow">{g}</p>' + "".join(f'<a href="{h}">{t}</a>' for h, t in items) + "</div>"
        for g, items in MENU)
    return f"""<footer class="foot">
  <div class="wrap">
    <div class="foot-top">
      <a class="brand big" href="index.html">{wordmark()}</a>
      <div class="foot-cta">
        <p class="foot-times">{TIMES}</p>
        <p>2010 N Stark Rd<br>Midland, MI 48642</p>
        <p><a href="tel:+19898327547">989-832-7547</a><br><a href="mailto:info@mbmmail.com">info@mbmmail.com</a></p>
      </div>
    </div>
    <div class="foot-cols">{cols}
      <div><p class="eyebrow">Follow</p>
        <a href="{L['instagram']}" target="_blank" rel="noopener">Instagram</a>
        <a href="{L['facebook']}" target="_blank" rel="noopener">Facebook</a>
        <a href="{L['youtube']}" target="_blank" rel="noopener">YouTube</a>
        <a href="{L['appstore']}" target="_blank" rel="noopener">BASE app</a>
      </div>
    </div>
    <div class="foot-base">
      <p>© <span data-year>2026</span> {SITES[BRAND['key']]['name']}.{' Formerly Living Word Church.' if BRAND['key'] == 'legacy' else ''}</p>
      <p class="foot-tag">{SITES[BRAND['key']]['tagline']}</p>
    </div>
  </div>
</footer>"""


def live_modal():
    return f"""<div class="modal" data-modal hidden role="dialog" aria-modal="true" aria-label="Live service">
  <div class="modal-box">
    <div class="modal-head">
      <span class="pill" data-live-pill hidden><span class="dot"></span>Live</span>
      <button type="button" class="x" data-close aria-label="Close">×</button>
    </div>
    <div class="player" data-player>
      <div class="player-fallback">
        <h3 data-fallback-title>Watch the latest service</h3>
        <p>Stream live on YouTube or in the BASE app.</p>
        <div class="btns center">
          <a class="btn btn-solid" href="{L['youtube_live']}" target="_blank" rel="noopener">Watch on YouTube{ICON_OUT}</a>
          <a class="btn" href="{L['appstore']}" target="_blank" rel="noopener">App Store{ICON_OUT}</a>
          <a class="btn" href="{L['play']}" target="_blank" rel="noopener">Google Play{ICON_OUT}</a>
        </div>
      </div>
    </div>
  </div>
</div>"""


def phero(eyebrow, caps, accent, lede, photo, alt, btns="", pos=None):
    return f"""<section class="phero">
  <div class="phero-text wrap">
    <p class="eyebrow">{eyebrow}</p>
    <h1><span class="caps">{caps}</span> <em>{accent}</em></h1>
    <p class="lede">{lede}</p>
    {f'<div class="btns">{btns}</div>' if btns else ''}
  </div>
  <figure class="phero-media reveal">{img(photo, alt, 2400, pos=pos, eager=True)}</figure>
</section>"""


def times_band():
    return f"""<section class="band wrap">
  <div class="times">
    <div><p class="eyebrow">Sunday</p><p class="big">10 AM</p><p>Morning service</p></div>
    <div><p class="eyebrow">Sunday</p><p class="big">6 PM</p><p>Night service</p></div>
    <div><p class="eyebrow">Thursday</p><p class="big">7 PM</p><p>Midweek service</p></div>
    <div class="times-where"><p class="eyebrow">Where</p><p>2010 N Stark Rd<br>Midland, MI 48642</p>
      <a class="link" href="{L['map']}" target="_blank" rel="noopener">Get directions{ICON_OUT}</a></div>
  </div>
</section>"""


def app_block():
    return f"""<section class="app wrap reveal">
  <div class="app-text">
    <p class="eyebrow">The BASE app</p>
    <h2>Church in your pocket.</h2>
    <p>Watch sermons, view upcoming events, give online and find resources, all in one place.</p>
    <div class="btns">
      <a class="btn btn-solid" href="{L['appstore']}" target="_blank" rel="noopener">App Store{ICON_OUT}</a>
      <a class="btn" href="{L['play']}" target="_blank" rel="noopener">Google Play{ICON_OUT}</a>
    </div>
  </div>
  <div class="app-phone" aria-hidden="true">
    <div class="phone"><div class="phone-screen">{img('hands', '', 800)}<span>BASE</span></div></div>
  </div>
</section>"""


def cta(title, text, btns):
    return f"""<section class="cta wrap reveal">
  <h2>{title}</h2>
  <p>{text}</p>
  <div class="btns center">{btns}</div>
</section>"""


def faq(items):
    rows = "".join(f'<details><summary>{q}<span class="plus" aria-hidden="true"></span></summary><div>{ans}</div></details>'
                   for q, ans in items)
    return f'<div class="faq">{rows}</div>'


# ================================================================ PAGES
PAGES = {}

# ---------------------------------------------------------------- home
PAGES["index"] = ("Home", "Living Word Church in Midland, Michigan. Sundays 10 AM and 6 PM, Thursdays 7 PM.", f"""
<div class="lw-only">
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Midland, Michigan · Since 1981</p>
    <h1><span class="caps">Experience</span><em>Jesus.</em></h1>
    <p class="lede">A Spirit-filled church family on North Stark Road. Come as you are. We saved you a seat.</p>
    <div class="btns">
      <a class="btn btn-solid" href="plan-a-visit.html">Plan a visit{ICON_ARROW}</a>
      <a class="btn" href="watch.html">Watch online{ICON_ARROW}</a>
    </div>
  </div>
  <figure class="hero-media reveal">{img('hands', 'Hands raised in worship under stage lights', 2400, eager=True, pos='50% 40%')}</figure>
</section>

<nav class="quick wrap" aria-label="Start here">
  <a href="new-here.html"><span>01</span>New Here</a>
  <a href="next-steps.html"><span>02</span>Next Steps</a>
  <a href="watch.html"><span>03</span>Watch</a>
  <a href="give.html"><span>04</span>Give</a>
  <a href="our-story.html"><span>05</span>Our Story</a>
</nav>

{times_band()}

<section class="split wrap reveal">
  <figure>{img('prayer', 'People praying together after a service', 1600, pos='50% 30%')}</figure>
  <div>
    <p class="eyebrow">First time?</p>
    <h2>Come as you are.</h2>
    <p>Services run about 90 minutes with worship and practical teaching from the Bible. Your kids have their own classes, there's plenty of parking, and someone will be at the door to say hi.</p>
    {a('plan-a-visit.html', 'Everything to know before you come', 'link')}
  </div>
</section>

<section class="tiles wrap">
  <header class="sec-head"><p class="eyebrow">For every age</p><h2>There's a place for your whole family.</h2></header>
  <div class="tiles-grid">
    <a class="tile reveal" href="kids.html">{img('kids', 'A child with hands raised during worship', 1200)}<div><p class="eyebrow">Infants–5th grade</p><h3>Life Kids</h3></div></a>
    <a class="tile reveal" href="youth.html">{img('youth_mic', 'A student leading worship', 1200, pos='50% 25%')}<div><p class="eyebrow">Sundays 5:30 PM</p><h3>Life Youth</h3></div></a>
    <a class="tile reveal" href="young-adults.html">{img('ya', 'Young adults worshipping in The Living Room', 1200)}<div><p class="eyebrow">The Living Room</p><h3>Young Adults</h3></div></a>
  </div>
</section>

<section class="dark-band">
  <div class="wrap watch-grid reveal">
    <div>
      <p class="eyebrow">Watch</p>
      <h2>Can't make it in? Join us online.</h2>
      <p>Every service streams live. When we're on, this site pops the stream up for you.</p>
      <div class="btns">
        <a class="btn btn-solid" href="watch.html">Watch live{ICON_ARROW}</a>
        <a class="btn" href="{L['youtube_streams']}" target="_blank" rel="noopener">Past services{ICON_OUT}</a>
      </div>
    </div>
    <a class="video-card" href="watch.html">{img('grandpa_welcome', 'Mark T. Barclay on stage on a Sunday morning', 1600)}<span class="play" aria-hidden="true"></span></a>
  </div>
</section>

<section class="steps wrap">
  <header class="sec-head"><p class="eyebrow">Next steps</p><h2>Ready for more?</h2></header>
  <div class="step-list">
    <a href="{L['connect']}" target="_blank" rel="noopener"><span>Fill out a connect card</span>{ICON_OUT}</a>
    <a href="{L['baptism']}" target="_blank" rel="noopener"><span>Get baptized</span>{ICON_OUT}</a>
    <a href="{L['membership']}" target="_blank" rel="noopener"><span>Take the membership class</span>{ICON_OUT}</a>
    <a href="prayer.html"><span>Ask for prayer</span>{ICON_ARROW}</a>
    <a href="jesus.html"><span>Know Jesus</span>{ICON_ARROW}</a>
  </div>
</section>

<section class="split wrap reveal flip">
  <figure class="archive">{img('dedication', 'The congregation at the church dedication in May 1981', 1200)}</figure>
  <div>
    <p class="eyebrow">Our story</p>
    <h2>Four decades of faith in Midland.</h2>
    <p>{NAME} was planted in 1981. Same Word, same Spirit, a new generation filling the room.</p>
    {a('our-story.html', 'Read our story', 'link')}
  </div>
</section>

{app_block()}
{cta('Give', 'Your generosity fuels ministry here in Midland and around the world.', f'<a class="btn btn-solid" href="give.html">Ways to give{ICON_ARROW}</a>')}
</div>

<div class="lg-only">
<section class="lg-hero">
  <figure class="lg-hero-media">{img('smoke', 'Worship night with stage haze and a full room', 2400, eager=True)}</figure>
  <div class="lg-hero-text">
    <p class="eyebrow">Midland, Michigan</p>
    <h1>Legacy</h1>
    <p class="lg-tag">Faith for generations.</p>
    <div class="btns center">
      <a class="btn btn-solid" href="plan-a-visit.html">Plan a visit{ICON_ARROW}</a>
      <a class="btn" href="watch.html">Watch live{ICON_ARROW}</a>
    </div>
  </div>
  <p class="lg-scroll" aria-hidden="true">Scroll</p>
</section>

<div class="marquee" aria-label="Service times"><div><span>Sundays 10 AM</span><span>Sundays 6 PM</span><span>Thursdays 7 PM</span><span>2010 N Stark Rd</span><span>Sundays 10 AM</span><span>Sundays 6 PM</span><span>Thursdays 7 PM</span><span>2010 N Stark Rd</span></div></div>

<section class="lg-intro wrap reveal">
  <p class="eyebrow">A new name</p>
  <h2>Same family. Same Word.<br><em>A new chapter.</em></h2>
  <p>For more than forty years this house was Living Word Church. Now we're Legacy Church, carrying everything God built here into the next generation.</p>
  {a('our-story.html', 'Our story', 'link')}
</section>

<section class="lg-mosaic wrap">
  <figure class="m1 reveal">{img('hands', 'Hands raised in worship', 1600)}</figure>
  <figure class="m2 reveal">{img('youth_braid', 'A student worshipping', 1200)}</figure>
  <figure class="m3 reveal">{img('prayer', 'Praying for someone after service', 1200)}</figure>
  <figure class="m4 reveal">{img('baptism', 'A baptism', 1600)}</figure>
</section>

<section class="lg-index wrap">
  <p class="eyebrow">Start here</p>
  <a class="reveal" href="new-here.html"><span class="n">01</span><span class="t">New here</span>{ICON_ARROW}</a>
  <a class="reveal" href="plan-a-visit.html"><span class="n">02</span><span class="t">Plan a visit</span>{ICON_ARROW}</a>
  <a class="reveal" href="next-steps.html"><span class="n">03</span><span class="t">Next steps</span>{ICON_ARROW}</a>
  <a class="reveal" href="watch.html"><span class="n">04</span><span class="t">Watch</span>{ICON_ARROW}</a>
  <a class="reveal" href="give.html"><span class="n">05</span><span class="t">Give</span>{ICON_ARROW}</a>
</section>

<section class="lg-panels">
  <a class="lg-panel reveal" href="kids.html">{img('kids', 'A child worshipping', 2000)}<div><p class="eyebrow">Life Kids</p><h3>Faith that starts young.</h3></div></a>
  <a class="lg-panel reveal" href="youth.html">{img('youth_room', 'Life Youth worship night', 2000)}<div><p class="eyebrow">Life Youth · Sundays 5:30 PM</p><h3>A generation on fire.</h3></div></a>
  <a class="lg-panel reveal" href="young-adults.html">{img('ya', 'Young adults in The Living Room', 2000)}<div><p class="eyebrow">Young Adults</p><h3>The Living Room.</h3></div></a>
</section>

{app_block()}
{cta('Build what lasts.', 'Every gift fuels ministry in Midland and around the world.', f'<a class="btn btn-solid" href="give.html">Give{ICON_ARROW}</a>')}
</div>
""")

# ---------------------------------------------------------------- new here
VALUES = [
    ("Love", "We're committed to loving God and loving others, and to being known for our love for one another."),
    ("Worship", "We glorify God through worship rooted in Scripture that draws us closer to Him."),
    ("Service", "We serve our community and those in need through physical and spiritual acts of love and kindness."),
    ("Evangelism", "We spread the good news of Jesus Christ to all people, through both deed and word."),
    ("Discipleship", "We prioritize discipling others, helping them grow in their understanding of the Bible and their relationship with God."),
    ("Stewardship", "We're wise stewards of the resources God has given us, to meet the needs of the church and community."),
    ("Unity", "We foster unity in diversity, standing together as a church family united in sharing God's love."),
    ("Holiness", "We aim to be a holy people, living in obedience to God's Word and surrendered to the transforming power of the Holy Spirit."),
    ("Mission", "We fulfill the Great Commission, making disciples of Jesus Christ in our region and beyond."),
]
BELIEFS = [
    ("The Trinity", "There is one God, eternally existing as Father, Son and Holy Spirit."),
    ("The Bible", "The Bible is the true and inspired Word of God, our final authority for faith and life."),
    ("Jesus", "Jesus Christ is the Son of God. He died for our sins, rose again and is coming back."),
    ("Salvation", "Salvation is a gift, received by grace through faith in Jesus Christ."),
    ("Baptism", "Water baptism is a public declaration of new life in Christ."),
    ("The Holy Spirit", "The Holy Spirit lives in every believer and empowers us to live for God today."),
    ("The Church", "The Church is the body of Christ, a family of believers called to worship, grow and serve together."),
    ("Prayer", "Prayer changes things. We bring everything to God with faith."),
]


def numbered(items, cls="values"):
    return f'<ol class="{cls}">' + "".join(
        f'<li class="reveal"><span class="n">{i:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(items, 1)) + "</ol>"


PAGES["new-here"] = ("New Here", "Looking for a church in Midland? Here's what to expect at Living Word Church.", f"""
{phero('New here', 'Looking for', 'a church?', f'You\'re in the right place. {NAME} is a Spirit-filled, non-denominational church family in Midland, Michigan. Our mission is simple: love God, love others, and share the good news.', 'crowd', 'The congregation worshipping', btns=a('plan-a-visit.html', 'Plan a visit', 'btn btn-solid') + a('jesus.html', 'Know Jesus'))}

{times_band()}

<section class="expect wrap">
  <header class="sec-head"><p class="eyebrow">What to expect</p><h2>Your first Sunday.</h2></header>
  <div class="expect-grid">
    <div class="reveal"><span class="n">01</span><h3>Pull in</h3><p>Park anywhere in our on-site lot off North Stark Road and head to the main doors.</p></div>
    <div class="reveal"><span class="n">02</span><h3>Say hi</h3><p>Our friendship team will welcome you and help you find your way, including where to take the kids.</p></div>
    <div class="reveal"><span class="n">03</span><h3>Worship</h3><p>Expect heartfelt worship and practical, Bible-based teaching. About 90 minutes in all.</p></div>
    <div class="reveal"><span class="n">04</span><h3>Stay connected</h3><p>Fill out a connect card so we can say thanks for coming and help with your next step.</p></div>
  </div>
  <div class="btns">{a(L['connect'], 'Connect card', 'btn btn-solid')}{a('plan-a-visit.html', 'Read the FAQ')}</div>
</section>

<section class="wrap">
  <header class="sec-head"><p class="eyebrow">Our values</p><h2>What matters to us.</h2></header>
  {numbered(VALUES)}
</section>

<section class="dark-band">
  <div class="wrap">
    <header class="sec-head"><p class="eyebrow">Our beliefs</p><h2>What we believe.</h2></header>
    {numbered(BELIEFS, 'values beliefs')}
  </div>
</section>

{app_block()}

<section class="wrap more-links">
  <p class="eyebrow">Keep exploring</p>
  <div class="step-list">
    <a href="next-steps.html"><span>Next steps</span>{ICON_ARROW}</a>
    <a href="leadership.html"><span>Leadership</span>{ICON_ARROW}</a>
    <a href="our-story.html"><span>Our story</span>{ICON_ARROW}</a>
  </div>
</section>
""")

# ---------------------------------------------------------------- plan a visit
FAQ = [
    ("When are services?", f"<p>Sundays at 10 AM and 6 PM, and Thursdays at 7 PM. Life Youth meets Sundays at 5:30 PM.</p>"),
    ("Where are you, and where do I park?", f"<p>2010 N Stark Rd, Midland, MI 48642. We have a large on-site parking lot right in front of the building. <a href=\"{L['map']}\" target=\"_blank\" rel=\"noopener\">Open in Maps</a>.</p>"),
    ("How long is a service?", "<p>About 90 minutes, with worship and a message from the Bible.</p>"),
    ("What should I wear?", "<p>We love to dress up for worship, but we want you to feel comfortable. Come as you are.</p>"),
    ("What about my kids?", "<p>Children's classes and nursery run during each service, so your kids learn about Jesus at their level while you worship. See <a href=\"kids.html\">Life Kids</a>.</p>"),
    ("Is there something for teens?", "<p>Yes. Life Youth meets Sundays at 5:30 PM for worship, fellowship and fun. See <a href=\"youth.html\">Life Youth</a>.</p>"),
    ("Is the building accessible?", "<p>Yes, the building is wheelchair accessible.</p>"),
    ("What kind of church is this?", "<p>We're a Spirit-filled, non-denominational Word of Faith church. Read <a href=\"new-here.html\">what we believe</a>.</p>"),
    ("Can I watch online?", f"<p>Every service streams live on <a href=\"{L['youtube']}\" target=\"_blank\" rel=\"noopener\">YouTube</a> and in the BASE app. When a service is live, this site pops the stream up for you. See <a href=\"watch.html\">Watch</a>.</p>"),
    ("Can I talk to a pastor?", "<p>Yes. Our Flock Care Minister, Ryan Schneider, is here for you: <a href=\"tel:+19898598045\">989-859-8045</a>.</p>"),
    ("How do I ask for prayer?", "<p>Call the prayer line at <a href=\"tel:+19898354562\">989-835-4562</a> and leave a voicemail, email <a href=\"mailto:prayer@livingword.ws\">prayer@livingword.ws</a>, or use the <a href=\"prayer.html\">prayer request form</a>.</p>"),
    ("How do I get baptized or become a member?", f"<p>Sign up for <a href=\"{L['baptism']}\" target=\"_blank\" rel=\"noopener\">water baptism</a> or the <a href=\"{L['membership']}\" target=\"_blank\" rel=\"noopener\">membership class</a>. Both are listed on <a href=\"next-steps.html\">Next Steps</a>.</p>"),
    ("How can I give?", f"<p>Give online any time through <a href=\"{L['give']}\" target=\"_blank\" rel=\"noopener\">Pushpay</a>, in the BASE app, or during any service. See <a href=\"give.html\">Give</a>.</p>"),
    ("Who do I contact with other questions?", "<p>Call the office at <a href=\"tel:+19898327547\">989-832-7547</a> or email <a href=\"mailto:info@mbmmail.com\">info@mbmmail.com</a>.</p>"),
]

PAGES["plan-a-visit"] = ("Plan a Visit", "Service times, directions, kids, parking and everything else to know before you visit.", f"""
{phero('Plan a visit', 'We saved', 'you a seat.', 'Here\'s everything you need to know to plan your visit.', 'building', 'The church building on North Stark Road at dusk', btns=a(L['map'], 'Get directions', 'btn btn-solid') + a(L['connect'], 'Let us know you\'re coming'))}

{times_band()}

<section class="wrap faq-wrap">
  <header class="sec-head"><p class="eyebrow">FAQ</p><h2>Good questions.</h2></header>
  {faq(FAQ)}
</section>

<section class="wrap map-wrap reveal">
  <iframe title="Map to 2010 N Stark Rd, Midland, MI" src="{L['map_embed']}" loading="lazy"></iframe>
</section>

{cta('Still have a question?', 'We\'d love to hear from you.', f'<a class="btn btn-solid" href="tel:+19898327547">Call 989-832-7547{ICON_ARROW}</a><a class="btn" href="mailto:info@mbmmail.com">Email us{ICON_ARROW}</a>')}
""")

# ---------------------------------------------------------------- next steps
PAGES["next-steps"] = ("Next Steps", "Connect, get baptized, join the membership class, get prayer and start serving.", f"""
{phero('Next steps', 'Take your', 'next step.', 'Wherever you are with God, there\'s a next step for you here.', 'grandpa_welcome', 'Mark T. Barclay on stage with WELCOME on the screen', pos='50% 50%')}

<section class="wrap">
  <div class="cards">
    <a class="card reveal" href="{L['connect']}" target="_blank" rel="noopener"><span class="n">01</span><h3>Connect card</h3><p>New here? Tell us a little about you so we can help you get connected.</p><span class="link">Fill it out{ICON_OUT}</span></a>
    <a class="card reveal" href="{L['membership']}" target="_blank" rel="noopener"><span class="n">02</span><h3>Membership class</h3><p>Learn who we are and what it means to call this church home.</p><span class="link">Sign up{ICON_OUT}</span></a>
    <a class="card reveal" href="{L['baptism']}" target="_blank" rel="noopener"><span class="n">03</span><h3>Get baptized</h3><p>Make a public declaration of your faith in Jesus.</p><span class="link">Sign up{ICON_OUT}</span></a>
    <a class="card reveal" href="prayer.html"><span class="n">04</span><h3>Get prayer</h3><p>Whatever you're facing, our prayer team stands in faith with you.</p><span class="link">Request prayer{ICON_ARROW}</span></a>
    <a class="card reveal" href="{L['smti']}" target="_blank" rel="noopener"><span class="n">05</span><h3>SMTI</h3><p>Go deeper with ministry training at the Supernatural Ministry Training Institute.</p><span class="link">Learn more{ICON_OUT}</span></a>
    <a class="card reveal" href="jesus.html"><span class="n">06</span><h3>Know Jesus</h3><p>Find out who Jesus is and what it means to follow Him.</p><span class="link">Start here{ICON_ARROW}</span></a>
  </div>
</section>

<section class="split wrap reveal">
  <figure>{img('baptism', 'A woman being baptized', 1600)}</figure>
  <div>
    <p class="eyebrow">Baptism</p>
    <h2>Go public with your faith.</h2>
    <p>Water baptism is an outward sign of an inward change. If you've decided to follow Jesus, this is your next step.</p>
    {a(L['baptism'], 'Sign up for baptism', 'btn btn-solid')}
  </div>
</section>

<section class="dark-band">
  <div class="wrap">
    <header class="sec-head"><p class="eyebrow">Serve</p><h2>How to get involved.</h2><p>Use your gifts to make a difference. Areas include worship, kids, hospitality, outreach and media.</p></header>
    <ol class="path">
      <li class="reveal"><span class="n">01</span><h3>Visit</h3><p>Come to a service and meet our friendship team.</p></li>
      <li class="reveal"><span class="n">02</span><h3>Coffee</h3><p>Grab coffee with a ministry leader and find your fit.</p></li>
      <li class="reveal"><span class="n">03</span><h3>Workers School</h3><p>Learn how we serve and why it matters.</p></li>
      <li class="reveal"><span class="n">04</span><h3>Shadow</h3><p>Serve alongside an experienced team member.</p></li>
      <li class="reveal"><span class="n">05</span><h3>Train</h3><p>Get equipped for your area.</p></li>
      <li class="reveal"><span class="n">06</span><h3>Serve</h3><p>Join the team and start making a difference.</p></li>
      <li class="reveal"><span class="n">07</span><h3>Stay connected</h3><p>Grow with your team and the church family.</p></li>
    </ol>
    <div class="btns">{a(L['connect'], 'I want to serve', 'btn btn-solid')}</div>
  </div>
</section>

<section class="tiles wrap">
  <header class="sec-head"><p class="eyebrow">Ministries</p><h2>Find your people.</h2></header>
  <div class="tiles-grid">
    <a class="tile reveal" href="kids.html">{img('kids', 'Life Kids', 1200)}<div><h3>Life Kids</h3></div></a>
    <a class="tile reveal" href="youth.html">{img('youth_circle', 'Life Youth small group', 1200)}<div><h3>Life Youth</h3></div></a>
    <a class="tile reveal" href="young-adults.html">{img('ya', 'Young adults', 1200)}<div><h3>Young Adults</h3></div></a>
  </div>
</section>

{times_band()}
""")

# ---------------------------------------------------------------- watch
PAGES["watch"] = ("Watch", "Watch Living Word Church live on Sundays and Thursdays, or catch up on past services.", f"""
<section class="watch-hero">
  <div class="wrap">
    <p class="eyebrow">Watch</p>
    <h1><span class="caps">Watch</span> <em>live.</em></h1>
    <p class="lede">Every service streams live. {TIMES}.</p>
  </div>
  <div class="wrap">
    <button type="button" class="video-card big" data-open-live aria-label="Open the live player">
      {img('hands', 'Worship at a Sunday service', 2400, eager=True)}
      <span class="play" aria-hidden="true"></span>
      <span class="video-label"><span class="live-only"><span class="dot"></span><span data-live-name>Live now</span></span><span class="offline-only">Open the player</span></span>
    </button>
  </div>
</section>

<section class="wrap">
  <div class="cards three">
    <a class="card reveal" href="{L['youtube_live']}" target="_blank" rel="noopener"><h3>YouTube Live</h3><p>Watch the live stream on YouTube.</p><span class="link">Open{ICON_OUT}</span></a>
    <a class="card reveal" href="{L['youtube_streams']}" target="_blank" rel="noopener"><h3>Past services</h3><p>Catch up on recent Sundays and Thursdays.</p><span class="link">Browse{ICON_OUT}</span></a>
    <a class="card reveal" href="{L['youtube']}" target="_blank" rel="noopener"><h3>Our channel</h3><p>Subscribe so you never miss a service.</p><span class="link">Subscribe{ICON_OUT}</span></a>
  </div>
</section>

{app_block()}
""")

# ---------------------------------------------------------------- give
PAGES["give"] = ("Give", "Give online to Living Word Church through Pushpay.", f"""
{phero('Give', 'The power of', 'generosity.', 'Every gift supports ministry here in Midland and reaches people around the world.', 'outreach', 'Volunteers praying with people at an outreach', btns=a(L['give'], 'Give now', 'btn btn-solid'))}

<section class="wrap">
  <header class="sec-head"><p class="eyebrow">Why we give</p><h2>Where your gift goes.</h2></header>
  <ol class="values three">
    <li class="reveal"><span class="n">01</span><h3>Supporting ministries</h3><p>Kids, youth, young adults, worship and care for every age and stage.</p></li>
    <li class="reveal"><span class="n">02</span><h3>Empowering outreach</h3><p>Serving our community and supporting missions beyond Midland.</p></li>
    <li class="reveal"><span class="n">03</span><h3>Equipping our house</h3><p>Keeping our place of worship ready to welcome people every week.</p></li>
  </ol>
</section>

<section class="split wrap reveal">
  <figure>{img('heart', 'The Heart of Saginaw sign', 1600)}</figure>
  <div>
    <p class="eyebrow">Giving highlight</p>
    <h2>Heart of Saginaw.</h2>
    <p>A faith-based non-profit serving children and teens in inner-city Saginaw. Part of what you give helps them reach the next generation.</p>
  </div>
</section>

<section class="duo wrap">
  <figure class="reveal">{img('outreach_crowd', 'A winter outreach serving families', 1600)}</figure>
  <figure class="reveal">{img('missions', 'A missions team', 1600)}</figure>
</section>

<section class="wrap">
  <header class="sec-head"><p class="eyebrow">Ways to give</p><h2>Simple and secure.</h2></header>
  <div class="cards three">
    <a class="card reveal" href="{L['give']}" target="_blank" rel="noopener"><h3>Online</h3><p>Give once or set up recurring giving with Pushpay.</p><span class="link">Give now{ICON_OUT}</span></a>
    <a class="card reveal" href="{L['appstore']}" target="_blank" rel="noopener"><h3>In the app</h3><p>Give from the BASE app on your phone.</p><span class="link">Get the app{ICON_OUT}</span></a>
    <div class="card reveal"><h3>In person</h3><p>Give during any service at 2010 N Stark Rd.</p></div>
  </div>
</section>
""")

# ---------------------------------------------------------------- our story
PAGES["our-story"] = ("Our Story", "Living Word Church was planted in Midland, Michigan in 1981.", f"""
<section class="phero">
  <div class="phero-text wrap">
    <p class="eyebrow">Our story</p>
    <h1><span class="caps">God is</span> <em>faithful.</em></h1>
    <p class="lede">From a small rented hall to a home of our own, this is the story of what God has done since 1981.</p>
  </div>
  <div class="collage reveal">
    {img('lake', 'A lake baptism in 1980', 900, eager=True)}
    {img('dedication', 'The congregation at the 1981 church dedication', 900, eager=True)}
    {img('frame', 'The church building frame going up', 900, eager=True)}
    {img('crowd', 'A Sunday service today', 900, eager=True)}
  </div>
</section>

<section class="story wrap">
  <article class="chapter reveal">
    <p class="year">The call</p>
    <div><h2>It started far from Michigan.</h2>
    <p>While serving in Vietnam, Mark T. Barclay answered God's call to ministry. He went on to Bible college in California, preaching wherever doors opened, before returning to Michigan to plant a church.</p></div>
    <div class="chap-gallery">{img('cali', 'Preaching in California in the early years', 1000)}{img('seminar', 'Mark T. Barclay teaching a seminar', 700)}</div>
  </article>
  <article class="chapter reveal">
    <p class="year">1980</p>
    <div><h2>Before the building.</h2>
    <p>Before there was a building there were people hungry for the Word, and new believers baptized in Michigan lakes.</p></div>
    <div class="chap-gallery">{img('lake', 'A lake baptism in 1980', 1000)}{img('baptism_practice', 'Teaching on baptism', 700)}</div>
  </article>
  <article class="chapter reveal">
    <p class="year">1981</p>
    <div><h2>A church is born.</h2>
    <p>The church was planted in 1981, and those early services met in a rented hall. In May 1981 the congregation gathered to dedicate the church to God.</p></div>
    <div class="chap-gallery">{img('hall', 'The rented hall where the church first met', 1000)}{img('dedication', 'The congregation at the 1981 dedication', 700)}{img('gathering', 'An early church gathering outdoors', 700)}</div>
  </article>
  <article class="chapter reveal">
    <p class="year">Building</p>
    <div><h2>Room to grow.</h2>
    <p>As the family grew, so did the vision, and the church built a home of its own.</p></div>
    <div class="chap-gallery">{img('frame', 'The church building frame going up', 1000)}{img('bensch_family', 'A church family in the early years', 700)}{img('building', 'The church building today', 700)}</div>
  </article>
  <article class="chapter reveal">
    <p class="year">Today</p>
    <div><h2>Who we are today.</h2>
    <p>Today {NAME} is a Spirit-filled, non-denominational Word of Faith church with ministry for every age, from infants through high school, young adults and beyond.</p></div>
    <div class="chap-gallery">{img('crowd', 'A Sunday service today', 1000)}{img('kneel', 'Praying at the altar', 700)}{img('baptism', 'A baptism today', 700)}</div>
  </article>
</section>

<section class="dark-band lg-only">
  <div class="wrap lg-intro">
    <p class="eyebrow">2027</p>
    <h2>Living Word becomes <em>Legacy.</em></h2>
    <p>A new name for the same family, carrying more than forty years of faithfulness into the next generation.</p>
  </div>
</section>

<section class="wrap more-links">
  <p class="eyebrow">More about us</p>
  <div class="step-list">
    <a href="leadership.html"><span>Leadership</span>{ICON_ARROW}</a>
    <a href="new-here.html"><span>Values and beliefs</span>{ICON_ARROW}</a>
  </div>
</section>
""")

# ---------------------------------------------------------------- leadership
PAGES["leadership"] = ("Leadership", "Meet the ministry leaders of Living Word Church.", f"""
<section class="simple-hero wrap">
  <p class="eyebrow">Leadership</p>
  <h1><span class="caps">Meet our</span> <em>leaders.</em></h1>
  <p class="lede">The ministry team serving our church family.</p>
</section>
<section class="wrap">
  <div class="leaders">
    <div class="leader reveal"><p class="eyebrow">Senior Pastor</p><h3>Dr. Mark Barclay</h3></div>
    <div class="leader reveal"><p class="eyebrow">Assistant Minister</p><h3>Josh Barclay</h3></div>
    <div class="leader reveal"><p class="eyebrow">Flock Care Minister</p><h3>Ryan Schneider</h3><p><a href="tel:+19898598045">989-859-8045</a></p></div>
  </div>
</section>
{cta('Need someone to talk to?', 'Our Flock Care Minister is here for you.', f'<a class="btn btn-solid" href="tel:+19898598045">Call 989-859-8045{ICON_ARROW}</a>')}
""")

# ---------------------------------------------------------------- calendar
PAGES["calendar"] = ("Calendar", "Weekly services and upcoming events at Living Word Church.", f"""
<section class="simple-hero wrap">
  <p class="eyebrow">Calendar</p>
  <h1><span class="caps">See what's</span> <em>happening.</em></h1>
  <p class="lede">Our weekly rhythm, plus every upcoming event.</p>
  <div class="btns">{a(L['calendar'], 'All upcoming events', 'btn btn-solid')}{a(L['instagram'], 'Follow for updates')}</div>
</section>
<section class="wrap">
  <div class="week">
    <div class="day reveal"><p class="eyebrow">Sunday</p>
      <div class="ev"><b>10:00 AM</b><span>Morning service</span><small>Life Kids classes and nursery</small></div>
      <div class="ev"><b>5:30 PM</b><span>Life Youth</span><small>Students</small></div>
      <div class="ev"><b>6:00 PM</b><span>Night service</span></div>
    </div>
    <div class="day reveal"><p class="eyebrow">Thursday</p>
      <div class="ev"><b>7:00 PM</b><span>Midweek service</span></div>
    </div>
    <div class="day reveal muted"><p class="eyebrow">Online</p>
      <div class="ev"><b>Every service</b><span>Live on YouTube and BASE</span><small><a href="watch.html">Watch</a></small></div>
    </div>
  </div>
</section>
{app_block()}
""")

# ---------------------------------------------------------------- prayer
PAGES["prayer"] = ("Prayer", "Request prayer from the Living Word Church prayer team.", f"""
{phero('Prayer', 'Prayer', 'changes things.', 'You\'re not alone. Our prayer team listens, prays and stands in faith with you. Whatever you\'re facing, we\'re here.', 'prayer', 'Praying for someone at the altar', btns=a(L['prayer_form'], 'Request prayer', 'btn btn-solid') + '<a class="btn" href="tel:+19898354562">Call 989-835-4562' + ICON_ARROW + '</a>', pos='50% 30%')}

<section class="wrap">
  <div class="cards three">
    <a class="card reveal" href="tel:+19898354562"><h3>Call</h3><p>Leave a voicemail with your request on the prayer line.</p><span class="link">989-835-4562{ICON_ARROW}</span></a>
    <a class="card reveal" href="mailto:prayer@livingword.ws"><h3>Email</h3><p>Send your request to the prayer team.</p><span class="link">prayer@livingword.ws{ICON_ARROW}</span></a>
    <a class="card reveal" href="{L['prayer_form']}" target="_blank" rel="noopener"><h3>Online</h3><p>Fill out the prayer request form.</p><span class="link">Open form{ICON_OUT}</span></a>
  </div>
</section>

<section class="split wrap reveal flip">
  <figure>{img('kneel', 'A worship leader kneeling in prayer', 1200)}</figure>
  <div>
    <p class="eyebrow">Pastoral care</p>
    <h2>We're here for you.</h2>
    <p>If you need someone to talk to, our Flock Care Minister, Ryan Schneider, is available.</p>
    <a class="btn btn-solid" href="tel:+19898598045">Call 989-859-8045{ICON_ARROW}</a>
  </div>
</section>
""")

# ---------------------------------------------------------------- know jesus
STEPS = [
    ("Acknowledge", "Romans 3:23", "We have all sinned and fall short of God's glory. Admit your need for Him."),
    ("Believe", "John 3:16", "God loved the world so much that He gave His Son. Believe that Jesus died and rose again for you."),
    ("Repent &amp; confess", "Acts 3:19", "Turn from sin and turn to God, so your sins can be wiped away."),
    ("Receive", "Revelation 3:20", "Jesus is knocking. Open the door and invite Him into your life."),
    ("Follow", "Luke 9:23", "Follow Jesus every day. You don't have to do it alone; we'd love to walk with you."),
]
PAGES["jesus"] = ("Know Jesus", "Who is Jesus, and what does it mean to follow Him?", f"""
<section class="simple-hero wrap">
  <p class="eyebrow">Know Jesus</p>
  <h1><span class="caps">Who is</span> <em>Jesus?</em></h1>
  <p class="lede">Jesus is the Son of God. He lived a perfect life, died for our sins and rose again, so that anyone who believes in Him can have forgiveness, freedom and eternal life.</p>
</section>

<section class="wrap">
  <header class="sec-head"><p class="eyebrow">Why follow Jesus</p><h2>Five steps to a new life.</h2></header>
  <ol class="values">{''.join(f'<li class="reveal"><span class="n">{i:02d}</span><h3>{t}</h3><p class="ref">{r}</p><p>{d}</p></li>' for i, (t, r, d) in enumerate(STEPS, 1))}</ol>
</section>

{cta('Made a decision?', 'We want to celebrate with you and help you take your next step.', a(L['decided'], 'I have decided!', 'btn btn-solid') + a(L['question'], 'I have a question'))}

<section class="split wrap reveal">
  <figure>{img('baptism', 'A baptism', 1600)}</figure>
  <div>
    <p class="eyebrow">Next step</p>
    <h2>Water baptism.</h2>
    <p>Baptism is how you show the world that you belong to Jesus.</p>
    {a(L['baptism'], 'Sign up for baptism', 'btn btn-solid')}
  </div>
</section>
""")

# ---------------------------------------------------------------- kids
PAGES["kids"] = ("Life Kids", "Life Kids: children's ministry and nursery during every service.", f"""
{phero('Life Kids', 'Kids in our', 'community.', 'Kids are at the core of who we are. During each service, children\'s classes and nursery help your kids learn about Jesus at their level.', 'kids', 'A child with hands raised during worship', btns=a('plan-a-visit.html', 'Plan a visit', 'btn btn-solid'))}

<section class="wrap">
  <header class="sec-head"><p class="eyebrow">Where do kids fit in?</p><h2>Right in the middle.</h2></header>
  <ol class="values three">
    <li class="reveal"><span class="n">01</span><h3>Nursery</h3><p>A safe, caring room for the little ones during every service.</p></li>
    <li class="reveal"><span class="n">02</span><h3>Kids classes</h3><p>Worship, Bible lessons and fun, made for kids, every service.</p></li>
    <li class="reveal"><span class="n">03</span><h3>Special nights</h3><p>Events like the Life Kids Glow Party throughout the year.</p></li>
  </ol>
</section>

<section class="wrap faq-wrap">
  <header class="sec-head"><p class="eyebrow">Parents</p><h2>Questions parents ask.</h2></header>
  {faq([
      ("When do kids classes meet?", "<p>During each service: Sundays at 10 AM and 6 PM, and Thursdays at 7 PM.</p>"),
      ("What should I do on my first visit?", "<p>Arrive a few minutes early and our friendship team will show you where kids go and introduce you to the team.</p>"),
      ("What about middle and high school?", "<p>Students have their own night: <a href=\"youth.html\">Life Youth</a>, Sundays at 5:30 PM.</p>"),
  ])}
</section>
""")

# ---------------------------------------------------------------- youth
PAGES["youth"] = ("Life Youth", "Life Youth meets Sundays at 5:30 PM at 2010 N Stark Rd.", f"""
{phero('Life Youth', 'Life', 'Youth.', 'Sundays at 5:30 PM. Worship, fellowship and fun for students, right here at 2010 N Stark Rd.', 'youth_room', 'Students worshipping at Life Youth', btns=a(L['connect'], 'Get connected', 'btn btn-solid'))}

<section class="gallery wrap">
  <figure class="g1 reveal">{img('youth_mic', 'A student leading worship', 1200, pos='50% 25%')}</figure>
  <figure class="g2 reveal">{img('youth_circle', 'A Life Youth small group', 1600)}</figure>
  <figure class="g3 reveal">{img('youth_braid', 'A student worshipping', 1200)}</figure>
</section>

<section class="split wrap reveal">
  <div>
    <p class="eyebrow">Every year</p>
    <h2>Invasion.</h2>
    <p>Our annual youth conference. Students from all over come together for worship, the Word and encounters with God.</p>
    {a(L['invasion'], 'invasion.net', 'btn btn-solid')}
  </div>
  <div class="facts">
    <p><b>When</b> Sundays, 5:30 PM</p>
    <p><b>Where</b> 2010 N Stark Rd, Midland</p>
    <p><b>Who</b> Middle and high school students</p>
  </div>
</section>
""")

# ---------------------------------------------------------------- young adults
PAGES["young-adults"] = ("Young Adults", "The Living Room: young adults at Living Word Church.", f"""
{phero('Young Adults', 'The Living', 'Room.', 'A space for young adults to encounter Jesus, build real community and grow in their calling. Raw, real and full of life.', 'ya', 'Young adults worshipping in The Living Room', btns=a(L['ya_hang'], 'Wanna hang?', 'btn btn-solid'))}

<section class="wrap">
  <ol class="values three">
    <li class="reveal"><span class="n">01</span><h3>Encounter Jesus</h3><p>Worship and the Word, with room for God to move.</p></li>
    <li class="reveal"><span class="n">02</span><h3>Build community</h3><p>Real friendships with people in the same season of life.</p></li>
    <li class="reveal"><span class="n">03</span><h3>Grow your calling</h3><p>Discover what God has put in you and step into it.</p></li>
  </ol>
</section>

{cta('Wanna hang?', 'Tell us a little about you and we\'ll reach out.', a(L['ya_hang'], 'Get in touch', 'btn btn-solid'))}
""")


def for_brand(html_text, key):
    """Drop the other brand's blocks and bake in this brand's name."""
    other = "lw" if key == "legacy" else "lg"
    html_text = re.sub(r'<div class="%s-only">\n.*?\n</div>\n' % other, "", html_text, flags=re.S)
    html_text = re.sub(r'<section class="([^"]*) %s-only">.*?</section>\n' % other, "", html_text, flags=re.S)
    return html_text.replace(NAME, SITES[key]["name"])


def main():
    for key in SITES:
        BRAND["key"] = key
        out = os.path.join(ROOT, key)
        shutil.rmtree(out, ignore_errors=True)
        shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(out, "assets"))
        for slug, (title, desc, body) in PAGES.items():
            desc = desc.replace("Living Word Church", SITES[key]["name"])
            with open(os.path.join(out, slug + ".html"), "w") as f:
                f.write(for_brand(layout(slug, title, desc, body), key))
        print("built", key, len(PAGES), "pages")


if __name__ == "__main__":
    main()
