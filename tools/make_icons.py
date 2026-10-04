"""Generate the home-screen icons: a red tick on near-black, matching the app's on-air palette."""
from PIL import Image, ImageDraw

INK = (21, 23, 28)        # --ink
LIVE = (224, 50, 47)      # --live

def tick(size, inset):
    """inset: how much of the square the mark leaves empty (0.0 = full bleed mark)."""
    S = 1024
    img = Image.new("RGB", (S, S), INK)
    d = ImageDraw.Draw(img)
    span = S * (1 - 2 * inset)
    x0, y0 = S * inset, S * inset
    pts = [(x0 + span * 0.08, y0 + span * 0.52),
           (x0 + span * 0.38, y0 + span * 0.82),
           (x0 + span * 0.92, y0 + span * 0.18)]
    d.line(pts, fill=LIVE, width=int(span * 0.155), joint="curve")
    for p in pts:                                  # round the caps
        r = span * 0.0775
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=LIVE)
    return img.resize((size, size), Image.LANCZOS)

# iOS applies its own rounded mask, so these are full-bleed squares.
tick(180, 0.20).save("docs/icons/icon-180.png")
tick(192, 0.20).save("docs/icons/icon-192.png")
tick(512, 0.20).save("docs/icons/icon-512.png")
# Maskable: content pulled into the inner safe zone so Android can crop to a circle.
tick(512, 0.30).save("docs/icons/icon-maskable-512.png")
print("icons written")
