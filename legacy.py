"""Legacy Church site (legacychurchmidland.com), built for the people who use it.

Jude, 2026-10-12: flow better, better media, less based on the old site, built
for visitors and church members. So Legacy has its own pages and layout:
  Visit       - everything a first-timer needs on one page
  Watch       - live and past services
  Ministries  - kids, youth, young adults
  Church family - what members do every week: give, events, prayer, app, next steps
  About       - thank-you story, beliefs, leadership (names and titles only)
Standing rules: no Living Word mentions, no photos of Mark or Marty Barclay,
feature Josh Barclay, younger faces with some older ones, white on black.
build.py imports this module and calls pages()/layout().
"""
import html
import os

from build import (FAQ, ICON_ARROW, ICON_OUT, L, LOCAL, ROOT, STEPS, VALUES, BELIEFS,
                   faq, img, live_modal, src)

NAME = "Legacy Church"
TAGLINE = "Faith for generations."
ADDR = "2010 N Stark Rd, Midland, MI 48642"
TIMES = "Sundays 10 AM &amp; 6 PM · Thursdays 7 PM"

NAV = [("plan-a-visit.html", "Visit"), ("watch.html", "Watch"), ("ministries.html", "Ministries"),
       ("family.html", "Church Family"), ("about.html", "About")]

# Old addresses keep working
REDIRECTS = {
    "new-here": "plan-a-visit.html", "next-steps": "family.html#grow", "prayer": "family.html#prayer",
    "calendar": "family.html#this-week", "kids": "ministries.html#kids", "youth": "ministries.html#youth",
    "young-adults": "ministries.html#young-adults", "our-story": "about.html",
    "leadership": "about.html#leadership",
}


def pic(key, fallback, alt, w=1600, pos=None, eager=False):
    """A photo of Jude's kept in assets/photos, or a library photo until it's committed."""
    if key in LOCAL and os.path.exists(os.path.join(ROOT, LOCAL[key])):
        return img(key, alt, w, pos=pos, eager=eager)
    return img(fallback, fallback_alt(fallback), w, pos=pos, eager=eager)


ALTS = {
    "hands": "Hands raised in worship on a Sunday", "smoke": "A full room at a worship night",
    "crowd": "The church worshipping together", "kneel": "Praying at the altar",
    "youth_circle": "Students praying together", "worship": "The church worshipping with hands raised",
}


def fallback_alt(key):
    return ALTS.get(key, "Worship at Legacy Church")


# The shared FAQ, with Legacy names and links
LX_FAQ = [(q, a.replace("Life Kids", "Legacy Kids").replace("Life Youth", "Legacy Youth")
           .replace("BASE app", "Legacy App").replace('href="kids.html"', 'href="ministries.html#kids"')
           .replace('href="youth.html"', 'href="ministries.html#youth"').replace('href="new-here.html"', 'href="about.html"')
           .replace('href="prayer.html"', 'href="family.html#prayer"').replace('href="next-steps.html"', 'href="family.html#grow"'))
          for q, a in FAQ]


def btn(href, label, solid=False):
    tgt = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
    icon = ICON_OUT if href.startswith("http") else ICON_ARROW
    return f'<a class="btn{" btn-solid" if solid else ""}" href="{href}"{tgt}>{label}{icon}</a>'


def row(href, title, note=""):
    """One line in an action list: big title, short note, arrow."""
    ext = href.startswith("http")
    tgt = ' target="_blank" rel="noopener"' if ext else ""
    return (f'<a class="lx-row" href="{href}"{tgt}><span class="lx-row-t">{title}</span>'
            f'<span class="lx-row-n">{note}</span>{ICON_OUT if ext else ICON_ARROW}</a>')


def week():
    rows = [
        ("Sunday", "10 AM", "Morning service", "Kids classes and nursery"),
        ("Sunday", "5:30 PM", "Legacy Youth", "Middle and high school"),
        ("Sunday", "6 PM", "Night service", "Kids classes and nursery"),
        ("Thursday", "7 PM", "Midweek service", "Kids classes and nursery"),
    ]
    items = "".join(f'<li><span class="lx-day">{d}</span><span class="lx-time">{t}</span>'
                    f'<span class="lx-what">{w}<small>{n}</small></span></li>' for d, t, w, n in rows)
    return f'<ol class="lx-week">{items}</ol>'


def app_links(cls="btn"):
    return (f'<a class="{cls}" href="{L["appstore"]}" target="_blank" rel="noopener">App Store{ICON_OUT}</a>'
            f'<a class="{cls}" href="{L["play"]}" target="_blank" rel="noopener">Google Play{ICON_OUT}</a>')


def head(eyebrow, title, lede, btns=""):
    return f"""<section class="lx-head wrap">
  <p class="eyebrow">{eyebrow}</p>
  <h1>{title}</h1>
  <p class="lede">{lede}</p>
  {f'<div class="btns">{btns}</div>' if btns else ''}
</section>"""


def wide(photo, cls=""):
    return f'<figure class="lx-wide {cls} reveal">{photo}</figure>'


# ================================================================ pages
def pages():
    P = {}

    # ------------------------------------------------------------ home
    P["index"] = ("Home", f"{NAME} in Midland, Michigan. {TIMES.replace('&amp;', 'and')}.", f"""
<section class="lx-hero">
  <figure>{img('smoke', 'A full room at a Legacy Church worship night', 2400, eager=True)}</figure>
  <div class="lx-hero-text wrap">
    <h1>{TAGLINE}</h1>
    <p class="lx-hero-info">{TIMES}<br>{ADDR}</p>
    <div class="btns">{btn('plan-a-visit.html', 'Plan your visit', True)}<a class="btn" href="watch.html" data-open-live>Watch live{ICON_ARROW}</a></div>
  </div>
</section>

<section class="lx-doors wrap">
  <a class="lx-door reveal" href="plan-a-visit.html">
    {img('crowd', 'The church worshipping together on a Sunday', 1600)}
    <div><p class="eyebrow">New here</p><h2>Plan your first Sunday.</h2>
    <p>Times, parking, what to expect and where the kids go.</p><span class="link">Start here{ICON_ARROW}</span></div>
  </a>
  <a class="lx-door reveal" href="family.html">
    {img('elder_mic', 'A longtime member sharing with the church', 1600, pos='50% 30%')}
    <div><p class="eyebrow">Church family</p><h2>Everything for the week.</h2>
    <p>Give, events, prayer, the Legacy App and your next step.</p><span class="link">Open{ICON_ARROW}</span></div>
  </a>
</section>

<section class="lx-split wrap" id="this-week">
  <div>
    <p class="eyebrow">This week</p>
    <h2>Join us in person.</h2>
    <p class="lx-mute">{ADDR}. Free parking right out front.</p>
    <div class="btns">{btn(L['map'], 'Get directions')}{btn(L['calendar'], 'All events')}</div>
  </div>
  {week()}
</section>

{wide(pic('josh_preach', 'hands', 'Josh Barclay preaching on a Sunday', 2400))}

<section class="lx-statement wrap reveal">
  <h2>Worship, the Word, and room for God to move. <span>Every service streams live, so you never miss one.</span></h2>
  <div class="btns">{btn('watch.html', 'Watch', True)}{btn(L['youtube_streams'], 'Past services')}</div>
</section>

<section class="lx-ministries wrap">
  <header class="lx-sec"><p class="eyebrow">Ministries</p><h2>A place for every age.</h2></header>
  <div class="lx-tiles">
    <a class="lx-tile reveal" href="ministries.html#kids">{img('kids', 'A child worshipping with hands raised', 1200)}<div><h3>Legacy Kids</h3><p>Infants through 5th grade, every service</p></div></a>
    <a class="lx-tile reveal" href="ministries.html#youth">{img('youth_room', 'Students worshipping at Legacy Youth', 1200)}<div><h3>Legacy Youth</h3><p>Sundays 5:30 PM</p></div></a>
    <a class="lx-tile reveal" href="ministries.html#young-adults">{img('ya', 'Young adults worshipping together', 1200)}<div><h3>Legacy Young Adults</h3><p>The Living Room</p></div></a>
  </div>
</section>

<section class="lx-band">
  <div class="wrap lx-band-grid">
    <div><p class="eyebrow">The Legacy App</p><h2>Church in your pocket.</h2>
    <p class="lx-mute">Watch live, see events and give from your phone.</p></div>
    <div class="btns">{app_links()}</div>
  </div>
</section>
""")

    # ------------------------------------------------------------ visit
    P["plan-a-visit"] = ("Plan a Visit", "Service times, directions, kids, parking and answers to common questions.", f"""
{head('Plan a visit', 'We saved you a seat.', f'Everything you need for your first Sunday at {NAME}, in one place.', btn(L['connect'], 'Let us know you’re coming', True) + btn(L['map'], 'Get directions'))}

<section class="lx-facts wrap">
  <div><p class="eyebrow">When</p><p>Sundays 10 AM &amp; 6 PM<br>Thursdays 7 PM</p></div>
  <div><p class="eyebrow">Where</p><p>2010 N Stark Rd<br>Midland, MI</p></div>
  <div><p class="eyebrow">How long</p><p>About 90 minutes</p></div>
  <div><p class="eyebrow">Kids</p><p>Classes and nursery<br>every service</p></div>
</section>

{wide(pic('josh_smile', 'crowd', 'Josh Barclay welcoming everyone on a Sunday', 2400))}

<section class="wrap">
  <header class="lx-sec"><p class="eyebrow">What to expect</p><h2>Your first Sunday.</h2></header>
  <ol class="lx-steps">
    <li class="reveal"><span>1</span><h3>Park out front</h3><p>Pull into the lot off North Stark Road and head for the main doors.</p></li>
    <li class="reveal"><span>2</span><h3>Say hi</h3><p>Our friendship team will welcome you and show you where the kids go.</p></li>
    <li class="reveal"><span>3</span><h3>Worship</h3><p>Heartfelt worship and practical teaching from the Bible. Come as you are.</p></li>
    <li class="reveal"><span>4</span><h3>Stay connected</h3><p>Fill out a connect card so we can say thanks and help with your next step.</p></li>
  </ol>
</section>

<section class="lx-split wrap reveal">
  <figure class="lx-photo">{img('kids', 'A child worshipping with hands raised', 1600)}</figure>
  <div>
    <p class="eyebrow">Your kids</p>
    <h2>Made for them.</h2>
    <p class="lx-mute">Nursery and kids classes run during every service, so your kids learn about Jesus at their level while you worship. Students have their own night, Sundays at 5:30 PM.</p>
    <div class="btns">{btn('ministries.html#kids', 'Legacy Kids')}{btn('ministries.html#youth', 'Legacy Youth')}</div>
  </div>
</section>

<section class="wrap lx-map reveal">
  <iframe title="Map to {ADDR}" src="{L['map_embed']}" loading="lazy"></iframe>
  <div><p class="eyebrow">Find us</p><p>{ADDR}</p>{btn(L['map'], 'Open in Maps')}</div>
</section>

<section class="wrap lx-faq" id="faq">
  <header class="lx-sec"><p class="eyebrow">Questions</p><h2>Good questions.</h2></header>
  {faq(LX_FAQ)}
</section>

<section class="lx-end wrap reveal">
  <h2>See you Sunday.</h2>
  <p class="lx-mute">Questions first? Call <a href="tel:+19898327547">989-832-7547</a> or email <a href="mailto:info@mbmmail.com">info@mbmmail.com</a>.</p>
  <div class="btns center">{btn(L['connect'], 'Let us know you’re coming', True)}</div>
</section>
""")

    # ------------------------------------------------------------ watch
    P["watch"] = ("Watch", f"Watch {NAME} live on Sundays and Thursdays, or catch up on past services.", f"""
{head('Watch', 'Watch live.', f'Every service streams live. {TIMES}.')}
<section class="wrap">
  <button type="button" class="video-card lx-player" data-open-live aria-label="Open the live player">
    {pic('josh_conference', 'hands', 'Josh Barclay preaching', 2400, eager=True)}
    <span class="play" aria-hidden="true"></span>
    <span class="video-label"><span class="live-only"><span class="dot"></span><span data-live-name>Live now</span></span><span class="offline-only">Open the player</span></span>
  </button>
</section>
<section class="wrap lx-list">
  {row(L['youtube_live'], 'YouTube Live', 'The live stream on YouTube')}
  {row(L['youtube_streams'], 'Past services', 'Catch up on recent Sundays and Thursdays')}
  {row(L['youtube'], 'Subscribe', 'Never miss a service')}
</section>
<section class="lx-band">
  <div class="wrap lx-band-grid">
    <div><p class="eyebrow">The Legacy App</p><h2>Watch anywhere.</h2>
    <p class="lx-mute">Services, events and giving in one app.</p></div>
    <div class="btns">{app_links()}</div>
  </div>
</section>
""")

    # ------------------------------------------------------------ ministries
    P["ministries"] = ("Ministries", "Legacy Kids, Legacy Youth and Legacy Young Adults.", f"""
{head('Ministries', 'A place for every age.', 'From the nursery to young adults, there is a place to grow with people your age.')}

<section class="lx-min wrap" id="kids">
  <figure class="lx-photo reveal">{img('kids', 'A child worshipping with hands raised', 1600)}</figure>
  <div>
    <p class="eyebrow">Infants–5th grade</p>
    <h2>Legacy Kids</h2>
    <p class="lx-mute">Nursery and kids classes during every service, with worship, Bible lessons and fun made for kids. Arrive a few minutes early on your first visit and we will show you where to go.</p>
    <dl class="lx-dl"><div><dt>When</dt><dd>Every service</dd></div><div><dt>Where</dt><dd>2010 N Stark Rd</dd></div></dl>
    <div class="btns">{btn('plan-a-visit.html', 'Plan a visit', True)}</div>
  </div>
</section>

<section class="lx-min wrap flip" id="youth">
  <figure class="lx-photo reveal">{img('youth_room', 'Students worshipping at Legacy Youth', 1600)}</figure>
  <div>
    <p class="eyebrow">Middle and high school</p>
    <h2>Legacy Youth</h2>
    <p class="lx-mute">Worship, the Word and real friendships. Every year students also head to Invasion, our youth conference.</p>
    <dl class="lx-dl"><div><dt>When</dt><dd>Sundays, 5:30 PM</dd></div><div><dt>Where</dt><dd>2010 N Stark Rd</dd></div></dl>
    <div class="btns">{btn(L['connect'], 'Get connected', True)}{btn(L['invasion'], 'Invasion')}</div>
  </div>
</section>
<section class="lx-strip wrap reveal">
  {img('youth_mic', 'A student leading worship', 900, pos='50% 25%')}
  {img('youth_circle', 'Students praying together', 900)}
  {img('youth_braid', 'A student worshipping', 900)}
</section>

<section class="lx-min wrap" id="young-adults">
  <figure class="lx-photo reveal">{img('ya', 'Young adults worshipping together', 1600)}</figure>
  <div>
    <p class="eyebrow">The Living Room</p>
    <h2>Legacy Young Adults</h2>
    <p class="lx-mute">A space for young adults to encounter Jesus, build real community and grow in their calling.</p>
    <div class="btns">{btn(L['ya_hang'], 'Wanna hang?', True)}</div>
  </div>
</section>
""")

    # ------------------------------------------------------------ church family
    P["family"] = ("Church Family", "Give, events, prayer, the Legacy App and next steps for the Legacy Church family.", f"""
{head('Church family', 'Welcome home.', 'The things you come back for every week, all in one place.')}

<section class="wrap lx-list">
  {row(L['give'], 'Give', 'Online, once or recurring')}
  {row(L['calendar'], 'Events', 'Everything coming up')}
  {row('#prayer', 'Prayer', 'Call, email or send a request')}
  {row(L['appstore'], 'Legacy App', 'Watch, events and giving on your phone')}
  {row(L['youtube_streams'], 'Past services', 'Catch up on YouTube')}
</section>

<section class="lx-split wrap" id="this-week">
  <div>
    <p class="eyebrow">This week</p>
    <h2>Every week.</h2>
    <p class="lx-mute">Special events, nights and classes are on the calendar.</p>
    <div class="btns">{btn(L['calendar'], 'All events', True)}</div>
  </div>
  {week()}
</section>

{wide(img('worship', 'The church worshipping with hands raised', 2400))}

<section class="wrap" id="grow">
  <header class="lx-sec"><p class="eyebrow">Next steps</p><h2>Take your next step.</h2></header>
  <div class="lx-list">
    {row(L['connect'], 'Connect card', 'New here? Tell us about you')}
    {row(L['baptism'], 'Get baptized', 'Go public with your faith')}
    {row(L['membership'], 'Membership class', 'Make Legacy your home')}
    {row(L['connect'], 'Serve', 'Worship, kids, hospitality, outreach and media')}
    {row('jesus.html', 'Know Jesus', 'Who He is and how to follow Him')}
    {row(L['smti'], 'SMTI', 'Ministry training at the Supernatural Ministry Training Institute')}
  </div>
</section>

<section class="lx-split wrap reveal" id="prayer">
  <figure class="lx-photo">{pic('josh_pray', 'kneel', 'Josh Barclay praying with the church', 1600)}</figure>
  <div>
    <p class="eyebrow">Prayer</p>
    <h2>You are not alone.</h2>
    <p class="lx-mute">Our prayer team listens, prays and stands in faith with you.</p>
    <dl class="lx-dl">
      <div><dt>Call</dt><dd><a href="tel:+19898354562">989-835-4562</a></dd></div>
      <div><dt>Email</dt><dd><a href="mailto:prayer@livingword.ws">prayer@livingword.ws</a></dd></div>
      <div><dt>Pastoral care</dt><dd>Ryan Schneider, <a href="tel:+19898598045">989-859-8045</a></dd></div>
    </dl>
    <div class="btns">{btn(L['prayer_form'], 'Request prayer', True)}</div>
  </div>
</section>

<section class="lx-band" id="give">
  <div class="wrap lx-band-grid">
    <div><p class="eyebrow">Give</p><h2>Build what lasts.</h2>
    <p class="lx-mute">Every gift fuels ministry in Midland and around the world.</p></div>
    <div class="btns">{btn(L['give'], 'Give now', True)}{btn('give.html', 'Where it goes')}</div>
  </div>
</section>
""")

    # ------------------------------------------------------------ give
    P["give"] = ("Give", f"Give online to {NAME}.", f"""
{head('Give', 'Build what lasts.', 'Every gift supports ministry here in Midland and reaches people around the world.', btn(L['give'], 'Give now', True))}
{wide(img('outreach_crowd', 'Serving families at a winter outreach', 2400))}
<section class="wrap">
  <ol class="lx-steps three">
    <li class="reveal"><span>1</span><h3>Every age</h3><p>Kids, youth, young adults, worship and care for every season of life.</p></li>
    <li class="reveal"><span>2</span><h3>Outreach</h3><p>Serving Midland and supporting missions beyond it, like Heart of Saginaw.</p></li>
    <li class="reveal"><span>3</span><h3>Our house</h3><p>Keeping the building ready to welcome people every week.</p></li>
  </ol>
</section>
<section class="wrap lx-list">
  {row(L['give'], 'Online', 'Give once or set up recurring giving')}
  {row(L['appstore'], 'In the Legacy App', 'Give from your phone')}
  <div class="lx-row"><span class="lx-row-t">In person</span><span class="lx-row-n">During any service at 2010 N Stark Rd</span></div>
</section>
""")

    # ------------------------------------------------------------ know jesus
    steps = "".join(f'<li class="reveal"><span>{i}</span><h3>{t}</h3><p class="lx-ref">{r}</p><p>{d}</p></li>'
                    for i, (t, r, d) in enumerate(STEPS, 1))
    P["jesus"] = ("Know Jesus", "Who is Jesus, and what does it mean to follow Him?", f"""
{head('Know Jesus', 'Who is Jesus?', 'Jesus is the Son of God. He lived a perfect life, died for our sins and rose again, so anyone who believes in Him can have forgiveness, freedom and eternal life.')}
<section class="wrap"><ol class="lx-steps">{steps}</ol></section>
<section class="lx-end wrap reveal">
  <h2>Made a decision?</h2>
  <p class="lx-mute">We want to celebrate with you and help with your next step.</p>
  <div class="btns center">{btn(L['decided'], 'I have decided', True)}{btn(L['question'], 'I have a question')}</div>
</section>
""")

    # ------------------------------------------------------------ about
    beliefs = "".join(f'<details><summary>{t}<span class="plus" aria-hidden="true"></span></summary><div><p>{d}</p></div></details>'
                      for t, d in BELIEFS)
    values = "".join(f'<li><b>{t}</b> {d}</li>' for t, d in VALUES)
    P["about"] = ("About", f"Who we are, what we believe and who leads {NAME}.", f"""
{head('About', 'Thank you.', 'To everyone who has prayed, served, given and worshipped in this house over the years: thank you. Every life touched and every step of faith is part of what God has done here, and He is not finished.')}
<section class="lx-strip wrap reveal">
  {img('youth_mic', 'A student leading worship', 900, eager=True, pos='50% 25%')}
  {img('elder_mic', 'A longtime member sharing with the church', 900, eager=True)}
  {img('kids', 'A child worshipping', 900, eager=True)}
</section>

<section class="lx-split wrap reveal">
  <div>
    <p class="eyebrow">Who we are</p>
    <h2>{TAGLINE}</h2>
    <p class="lx-mute">{NAME} is a Spirit-filled, non-denominational church in Midland with ministry for every age. Our mission is simple: love God, love others and share the good news.</p>
  </div>
  <figure class="lx-photo">{pic('josh_pulpit', 'crowd', 'Josh Barclay preaching', 1600)}</figure>
</section>

<section class="wrap lx-faq">
  <header class="lx-sec"><p class="eyebrow">Beliefs</p><h2>What we believe.</h2></header>
  <div class="faq">{beliefs}</div>
</section>

<section class="wrap">
  <header class="lx-sec"><p class="eyebrow">Values</p><h2>What matters to us.</h2></header>
  <ul class="lx-values">{values}</ul>
</section>

<section class="wrap" id="leadership">
  <header class="lx-sec"><p class="eyebrow">Leadership</p><h2>Our team.</h2></header>
  <div class="lx-list">
    <div class="lx-row"><span class="lx-row-t">Dr. Mark Barclay</span><span class="lx-row-n">Senior Pastor</span></div>
    <div class="lx-row"><span class="lx-row-t">Josh Barclay</span><span class="lx-row-n">Assistant Minister</span></div>
    <a class="lx-row" href="tel:+19898598045"><span class="lx-row-t">Ryan Schneider</span><span class="lx-row-n">Flock Care Minister · 989-859-8045</span>{ICON_ARROW}</a>
  </div>
</section>
""")
    return P


# ================================================================ layout
def wordmark():
    return '<span class="lx-wm">Legacy<span>Church</span></span>'


def layout(slug, title, desc, body):
    links = "".join(f'<a href="{h}"{" aria-current=page" if h == slug + ".html" else ""}>{t}</a>' for h, t in NAV)
    menu = "".join(f'<a href="{h}">{t}</a>' for h, t in [("index.html", "Home")] + NAV + [("give.html", "Give")])
    return f"""<!doctype html>
<html lang="en" data-brand="livingword" data-site="legacy">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · {NAME}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{title} · {NAME}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{src('smoke', 1200)}">
<meta name="theme-color" content="#000000">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.weserv.nl">
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/legacy.css">
</head>
<body class="lx p-{slug}">
<a class="skip" href="#main">Skip to content</a>
<div class="livebar" data-live-bar hidden>
  <span class="dot"></span><span><b>Live now</b> · <span data-live-name>Service</span></span>
  <button type="button" data-open-live>Watch</button>
</div>
<header class="nav">
  <a class="brand" href="index.html" aria-label="{NAME} home">{wordmark()}</a>
  <nav class="links" aria-label="Main">{links}</nav>
  <div class="nav-end">
    <a class="btn btn-sm btn-solid" href="{L['give']}" target="_blank" rel="noopener">Give</a>
    <button class="burger" type="button" data-menu-toggle aria-expanded="false" aria-label="Menu"><span></span><span></span></button>
  </div>
</header>
<div class="menu lx-menu" data-menu hidden>
  <nav class="lx-menu-links" aria-label="Menu">{menu}</nav>
  <div class="lx-menu-foot"><p>{TIMES}</p><p>{ADDR}</p></div>
</div>
<main id="main">
{body}
</main>
{footer()}
<nav class="lx-dock" aria-label="Quick links">
  <a href="plan-a-visit.html">Visit</a>
  <a href="watch.html" data-open-live>Watch</a>
  <a href="family.html">Family</a>
  <a href="{L['give']}" target="_blank" rel="noopener">Give</a>
</nav>
{live_modal().replace('BASE app', 'Legacy App')}
<script src="assets/site.js"></script>
</body>
</html>
"""


def footer():
    return f"""<footer class="lx-foot">
  <div class="wrap">
    <div class="lx-foot-top">
      <div><a class="brand" href="index.html">{wordmark()}</a><p class="lx-mute">{TAGLINE}</p></div>
      <div><p class="eyebrow">Services</p><p>Sundays 10 AM &amp; 6 PM<br>Thursdays 7 PM</p></div>
      <div><p class="eyebrow">Find us</p><p><a href="{L['map']}" target="_blank" rel="noopener">2010 N Stark Rd<br>Midland, MI 48642</a></p></div>
      <div><p class="eyebrow">Contact</p><p><a href="tel:+19898327547">989-832-7547</a><br><a href="mailto:info@mbmmail.com">info@mbmmail.com</a></p></div>
    </div>
    <div class="lx-foot-links">
      {''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)}
      <a href="give.html">Give</a><a href="jesus.html">Know Jesus</a>
      <a href="{L['instagram']}" target="_blank" rel="noopener">Instagram</a>
      <a href="{L['facebook']}" target="_blank" rel="noopener">Facebook</a>
      <a href="{L['youtube']}" target="_blank" rel="noopener">YouTube</a>
    </div>
    <p class="lx-foot-base">© <span data-year>2026</span> {NAME}</p>
  </div>
</footer>"""


def redirect(target):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{NAME}</title>
<meta http-equiv="refresh" content="0; url={target}"><link rel="canonical" href="{target}"></head>
<body style="background:#000;color:#fff;font-family:sans-serif"><a href="{target}" style="color:#fff">Continue</a></body></html>
"""
