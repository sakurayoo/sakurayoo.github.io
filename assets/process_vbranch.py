"""Key the black background out of the vertical cherry branch -> transparent PNG."""
import numpy as np
from PIL import Image, ImageFilter

BASE = r"C:\Users\renay\Documents\claude\assets"
im = Image.open(BASE + r"\vbranch-src.png").convert("RGB")
a = np.asarray(im).astype(np.float32) / 255.0
val = a.max(-1)  # black bg = 0; branch/flowers > 0

# alpha ramp: transparent where near-black, opaque for the subject
alpha = np.clip((val - 0.05) / (0.18 - 0.05), 0, 1)
alpha = alpha * alpha * (3 - 2 * alpha)
alpha = np.asarray(
    Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
).astype(np.float32) / 255.0

# reduce dark fringe: lift RGB slightly where it's a partial edge
out = Image.fromarray((np.dstack([a, alpha]) * 255).astype(np.uint8), "RGBA")
m = alpha > 0.12
ys, xs = np.where(m)
out = out.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
out.save(BASE + r"\vbranch.png", optimize=True)
print("saved vbranch.png", out.size)

# preview on washi
bg = Image.new("RGBA", out.size, (251, 244, 242, 255))
bg.alpha_composite(out)
bg.convert("RGB").save(BASE + r"\vbranch-preview.png")
print("saved vbranch-preview.png")
