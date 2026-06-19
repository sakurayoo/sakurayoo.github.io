"""Bake a soft left + bottom fade into the watercolour hero so it dissolves into the page."""
import numpy as np
from PIL import Image

BASE = r"C:\Users\renay\Documents\claude\assets"
im = Image.open(BASE + r"\hero-src.png").convert("RGB")
W, H = im.size
rgb = np.asarray(im).astype(np.float32) / 255.0
yy, xx = np.mgrid[0:H, 0:W]

# left fade: transparent at x=0 -> opaque by 45% width
lf = np.clip(xx / (0.45 * W), 0, 1)
lf = lf * lf * (3 - 2 * lf)
# bottom fade: opaque until 74% height -> transparent at bottom
bf = np.clip((H - yy) / (0.26 * H), 0, 1)
bf = bf * bf * (3 - 2 * bf)
alpha = lf * bf

out = Image.fromarray((np.dstack([rgb, alpha]) * 255).astype(np.uint8), "RGBA")
w = 1500
out = out.resize((w, round(H * w / W)), Image.LANCZOS)
out.save(BASE + r"\hero-bg2.png", optimize=True)
print("saved hero-bg2.png", out.size)

# preview on washi
bg = Image.new("RGBA", out.size, (251, 244, 242, 255))
bg.alpha_composite(out)
bg.convert("RGB").save(BASE + r"\hero-preview.png")
print("saved hero-preview.png")
