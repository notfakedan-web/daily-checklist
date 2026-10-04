"""Wrap index.html (which is written as a Claude artifact body) into a standalone page in docs/.

The artifact runtime supplies the document skeleton and a small reset; GitHub Pages does not,
so this adds them, plus the manifest, icons and service worker that make it installable on a phone.
Run: python3 tools/build.py
"""
import hashlib, pathlib, re

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "index.html").read_text()

# The source is head-ish tags (title, fonts, style) followed by the page itself.
split = src.index('<div class="wrap">')
head, body = src[:split].strip(), src[split:].strip()

version = hashlib.sha256(src.encode()).hexdigest()[:10]

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Tap a day, tick off what's due.">
<meta name="robots" content="noindex">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#eef0f4" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#101217" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Checklist">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/icon-180.png">
<link rel="icon" href="icons/icon-192.png" type="image/png">
{head}
<style>
  /* The skeleton the artifact runtime would otherwise provide. */
  html {{ -webkit-text-size-adjust: 100%; background: var(--bg); }}
  body {{ margin: 0; -webkit-tap-highlight-color: transparent; }}
  img {{ max-width: 100%; }}
  [hidden] {{ display: none !important; }}
  button, .task {{ -webkit-user-select: none; user-select: none; touch-action: manipulation; }}
  /* Installed on a phone there are no browser bars, so keep clear of the notch and home bar. */
  .wrap {{
    padding-left: max(20px, env(safe-area-inset-left));
    padding-right: max(20px, env(safe-area-inset-right));
    padding-bottom: calc(48px + env(safe-area-inset-bottom));
    min-height: 100svh;
  }}
  @media (display-mode: standalone) {{
    .wrap {{ padding-top: max(20px, env(safe-area-inset-top)); }}
  }}
</style>
</head>
<body>
{body}
<script>
// Keep a copy of the app on the phone so it opens offline, and pick up new builds quietly.
if ("serviceWorker" in navigator) {{
  window.addEventListener("load", () => {{
    const had = !!navigator.serviceWorker.controller;
    let reloading = false;
    navigator.serviceWorker.addEventListener("controllerchange", () => {{
      if (had && !reloading) {{ reloading = true; location.reload(); }}
    }});
    navigator.serviceWorker.register("sw.js").catch(e => console.error(e));
  }});
}}
</script>
</body>
</html>
"""

(root / "docs" / "index.html").write_text(page)

sw = (root / "docs" / "sw.js").read_text()
sw = re.sub(r'daily-checklist-[0-9a-f]{10}|daily-checklist-__VERSION__', f"daily-checklist-{version}", sw, count=1)
(root / "docs" / "sw.js").write_text(sw)

print(f"docs/index.html written (cache daily-checklist-{version})")
