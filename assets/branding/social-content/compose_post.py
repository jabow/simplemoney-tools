"""Instagram feed post (1080x1350) featuring 3D Hazel. Text set as outlined paths (Spectral / Libre Franklin)."""
from lib import *
from PIL import ImageFilter, ImageDraw
import sys

TEAL = "#2E7F8C"; TEAL_D = "#256A76"

def text_png(lines, face, size, fill, wght=600, width=1000, align="left", leading=1.12):
    """Render lines of text to a transparent PNG via SVG paths."""
    parts = []; y = size * 0.78; maxw = 0
    for ln in lines:
        d, adv, bb = spectral(ln, size) if face == "spectral" else franklin(ln, size, wght)
        x = 0 if align == "left" else (width - adv) / 2 if align == "center" else width - adv
        parts.append(f'<path d="{d}" fill="{fill}" transform="translate({x:.1f} {y:.1f})"/>'); y += size * leading; maxw = max(maxw, adv)
    H = int(y - size * leading + size * 0.35)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {H}" width="{width}" height="{H}">{"".join(parts)}</svg>'
    return svg_to_png(svg)

def soft_shadow(size, alpha=110, blur=40):
    w, h = size; im = Image.new("RGBA", (w + blur*4, h + blur*4), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse((blur*2, blur*2, blur*2 + w, blur*2 + h), fill=(19, 36, 64, alpha))
    return im.filter(ImageFilter.GaussianBlur(blur))

def post(pose_png, out, headline, sub, bullets, dark=False):
    W, H = 1080, 1350
    bg = NAVY if dark else PAPER; ink = CREAM if dark else INK_TYPE; muted = SLATE if dark else "#4A6A84"
    can = Image.new("RGBA", (W, H), hexrgb(bg))
    dr = ImageDraw.Draw(can)
    # teal ground disc behind Hazel, offset low
    disc_r = 400; cx, cy = 600, 800
    dr.ellipse((cx - disc_r, cy - disc_r, cx + disc_r, cy + disc_r), fill=hexrgb(TEAL))
    # headline (top)
    hl = text_png(headline, "spectral", 66, ink, width=960)
    can.alpha_composite(hl, (60, 72))
    y = 72 + hl.height + 14
    sb = text_png(sub, "franklin", 30, muted, wght=500, width=960)
    can.alpha_composite(sb, (60, y))
    # Hazel with soft contact shadow
    hz = Image.open(pose_png).convert("RGBA")
    scale = 820 / hz.height; hz = hz.resize((int(hz.width*scale), 820), Image.LANCZOS)
    bbox = hz.getchannel("A").getbbox(); hz = hz.crop(bbox)
    hx = cx - hz.width // 2 + 10; hy = H - hz.height - 180
    sh = soft_shadow((int(hz.width*0.6), 70)); can.alpha_composite(sh, (hx + hz.width//5 - 80, H - 180 - 50 - 80))
    can.alpha_composite(hz, (hx, hy))
    # bullets (bottom-left strip on a cream/navy card)
    card_w, card_h = 540, 40 + 44*len(bullets); card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((0, 0, card_w-1, card_h-1), radius=22, fill=hexrgb(NAVY if not dark else "#1E3354"))
    can.alpha_composite(card, (60, H - card_h - 70))
    bl = text_png(bullets, "franklin", 28, CREAM, wght=600, width=500, leading=1.55)
    can.alpha_composite(bl, (90, H - card_h - 70 + 20))
    # footer handle
    ft = text_png(["simplemoney-tools.co.uk"], "franklin", 24, muted, wght=500, width=400, align="right")
    can.alpha_composite(ft, (W - 60 - 400, H - 52))
    can.convert("RGB").save(out, quality=95)
    return can

if __name__ == "__main__":
    pose = sys.argv[1]; out = sys.argv[2]
    post(pose, out,
         ["Your budget shouldn't", "cost a monthly fee", "to make sense."],
         ["Meet Hazel. She looks after the tools at Simple Money Tools."],
         ["•  Free Excel budget tracker", "•  Chrome extension for your new tab", "•  Your data stays on your computer"])
