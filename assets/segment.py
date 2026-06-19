"""Split the scattered-petals PNG into individual petal/flower pieces via connected components."""
import os, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

BASE = r"C:\Users\renay\Documents\claude\assets"
OUT = os.path.join(BASE, "petals")
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith(".png"):
        os.remove(os.path.join(OUT, f))

im = Image.open(os.path.join(BASE, "petals-src.png")).convert("RGBA")
arr = np.asarray(im)
alpha = arr[..., 3]
mask = alpha > 40
mask = ndimage.binary_dilation(mask, iterations=1)
labels, n = ndimage.label(mask)

pieces = []
idx = 0
for lab in range(1, n + 1):
    comp = labels == lab
    if comp.sum() < 350:
        continue
    ys, xs = np.where(comp)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    sub = arr[y0:y1, x0:x1].copy()
    sc = comp[y0:y1, x0:x1]
    sa = sub[..., 3]; sa[~sc] = 0; sub[..., 3] = sa
    idx += 1
    Image.fromarray(sub, "RGBA").save(os.path.join(OUT, f"petal-{idx:02d}.png"))
    pieces.append((idx, x1 - x0, y1 - y0))

print("saved", idx, "pieces")
for p in pieces:
    print("petal-%02d  %dx%d" % p)

# montage on washi for review
cell, cols = 170, 5
rows = (idx + cols - 1) // cols
sheet = Image.new("RGBA", (cols * cell, rows * cell), (251, 244, 242, 255))
dr = ImageDraw.Draw(sheet)
for i, (n_, w, h) in enumerate(pieces):
    pc = Image.open(os.path.join(OUT, f"petal-{n_:02d}.png")).convert("RGBA")
    s = min((cell - 30) / pc.width, (cell - 30) / pc.height, 1.0)
    pc = pc.resize((max(1, round(pc.width * s)), max(1, round(pc.height * s))), Image.LANCZOS)
    cx, cy = (i % cols) * cell, (i // cols) * cell
    sheet.alpha_composite(pc, (cx + (cell - pc.width) // 2, cy + (cell - pc.height) // 2))
    dr.text((cx + 6, cy + 6), f"{n_:02d}", fill=(150, 90, 120))
sheet.convert("RGB").save(os.path.join(BASE, "petals-montage.png"))
print("saved montage")
