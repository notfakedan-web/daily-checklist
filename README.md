# Daily Checklist

A private habit calendar: tap a day to see what's due and tick it off.

- **Stream** every day (the main one, marked ON AIR, with a streak count)
- **Gym** every day
- **TRT** every other day, starting October 1, 2026 (Oct 1, 3, 5, ...)

Habits can be changed in the page under **Edit habits** (name, how often, start date).

## Where it runs

Two places, from the same source file.

**On the phone (home-screen app).** `docs/` is published with GitHub Pages. Open that link in Safari
on the iPhone, then Share → **Add to Home Screen**. It gets its own icon, opens fullscreen with no
browser bars, and works with no signal. Check-offs are saved on that device.

**In Claude (syncs between devices).** The same page is published as a private artifact:
https://claude.ai/artifact/7QRLKs5vi82R3Q6vEc3wav — opening it needs your Claude login, and
check-offs go to your own private space in the artifact's database, so they follow you between
phone and computer.

To carry days from one to the other, use **Copy backup** on one and **Restore backup** on the other
(under Edit habits).

## Working on it

`index.html` is the source, written as a Claude artifact body (no `<html>` / `<head>` wrapper, which
the artifact runtime supplies). After editing it:

```sh
python3 tools/build.py     # wraps it into docs/index.html with the manifest, icons and offline cache
```

Then commit and push, which updates the phone app. To update the Claude version, ask Claude to
republish `index.html` to the same artifact link.

`tools/make_icons.py` regenerates the home-screen icons.
