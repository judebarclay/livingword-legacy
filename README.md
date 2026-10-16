# Living Word Church + Legacy Church

Two separate websites, built from one shared set of content:

| Folder | Domain | Look |
| --- | --- | --- |
| `livingword/` | livingwordchurch.com | White, bold grotesque type |
| `legacy/` | legacychurchmidland.com | Black, cinematic serif, photos bloom into color |

Each folder is self-contained (pages plus its own `assets/`), so either one can be deployed to its own domain on its own.
Add `?live=1` to any page to preview the live-service popup.

## Editing

- Page content: `build.py`, then run `python3.12 build.py` to regenerate both folders. Don't edit the generated `.html` files by hand.
- Look and feel: `assets/site.css`.
- Live popup and service times: top of `assets/site.js`. Paste the Subsplash embed URL into `LIVE.subsplashEmbed` to play the stream inside the popup.

Photos come from the current livingwordchurch.com media library, resized on the fly by images.weserv.nl.

## Invasion (`invasion/`)

Site for invasion.net: Invasion Worship Nights, Invasion 2026 and past-year recaps, the 30-year tribute, and an About page (`about.html`). Plain static files, no build step.
Edit worship night dates, churches, registration links, social links and the YouTube recap list at the top of `invasion/assets/invasion.js`. Video cards open the YouTube video in a popup; the short muted loops in `assets/clips/` play on hover.
Photos and video are Jude's own (Invasion 26 film, Invasion Worship studio sessions, 2024 worship night selects).
