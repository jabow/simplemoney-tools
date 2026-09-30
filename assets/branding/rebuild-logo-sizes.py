"""Re-cut every size the site uses from logo/hazel-3d-1080.png. Run from this folder."""
from PIL import Image, ImageDraw

src = Image.open("logo/hazel-3d-1080.png").convert("RGBA")
for s in (512, 320, 256, 192, 180, 128, 96, 64, 48, 32):
    src.resize((s, s), Image.LANCZOS).save(f"logo/hazel-3d-{s}.png", optimize=True)

night = Image.open("logo/hazel-3d-night-1080.png").convert("RGBA")
night.resize((320, 320), Image.LANCZOS).save("logo/hazel-3d-night-320.png", optimize=True)

# Circle-masked set (transparent corners) for the tab icon and the nav/footer mark.
mask = Image.new("L", (4320, 4320), 0)
ImageDraw.Draw(mask).ellipse((0, 0, 4319, 4319), fill=255)
mask = mask.resize((1080, 1080), Image.LANCZOS)
circle = src.copy()
circle.putalpha(mask)
for s in (512, 256, 192, 128, 96, 64, 48, 32, 16):
    circle.resize((s, s), Image.LANCZOS).save(f"logo/circle/hazel-3d-circle-{s}.png", optimize=True)
circle.resize((48, 48), Image.LANCZOS).save("logo/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
print("done")
