# Living Word Church / Legacy Church

One static site that serves both brands:

- **livingwordchurch.com** shows Living Word Church (white, bold type).
- **legacychurchmidland.com** shows Legacy Church (black, cinematic, photos bloom into color).

Anywhere else (previews), add `?brand=legacy` or `?brand=livingword` to any page, or use the switch in the corner. `?live=1` previews the live-service popup.

## Editing

- Page content: `build.py`, then run `python3.12 build.py` to regenerate the `.html` files.
- Look and feel: `assets/site.css`.
- Live popup, service times, brand names/taglines: top of `assets/site.js`.
  Paste the Subsplash embed URL into `LIVE.subsplashEmbed` to play the stream inside the popup.

Photos come from the current livingwordchurch.com media library, resized on the fly by images.weserv.nl.
