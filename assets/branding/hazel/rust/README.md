# Hazel — current mark (rust on night navy), chosen 26 September 2026

James's pick from round 7 ("for now"). Hazel is a red squirrel in profile facing right, holding
a pound coin to her chest, tail rising behind her; on a night-navy disc. Flat fills, no strokes,
no gradients. The £ is a Nunito ExtraBold glyph outlined (cap height 80 on the 512 grid ≈ 6 px at
40 px) on a coin with a thin knockout ring so it separates from the body at small sizes.

| File | Use |
|---|---|
| `svg/hazel-rust-night.svg` | **Master.** Faces right (toward the username on Instagram). |
| `svg/hazel-rust-night-left.svg` | Mirrored, for placements where the mark sits right of text. |
| `svg/hazel-rust-mark-nodisc.svg` | Transparent, no disc — site header, wordmark lockup, light grounds. |
| `instagram/hazel-avatar-rust-night-{1080,320}.png` | Instagram avatar (upload the 1080). Left-facing alternates alongside. |
| `png/hazel-rust-night-{512,256,180,128,96,48,32,16}.png` | Icon and apple-touch-icon sizes from the master. Don't use the 16/32 here for favicons — use `favicon/`. |
| `favicon/hazel-rust-favicon.svg`, `favicon/hazel-rust-favicon-{16,32,48}.png`, `favicon/favicon.ico` | **Favicon.** The SVG is a heavier small-size redraw (navy disc, rust head + body, dark-rust tail, brass coin dot, no £); the .ico holds 16 + 32 from it and 48 from the master. |
| `extension/icon-{16,32,48,128}.png` | Chrome extension icon set — 16/32 from the favicon redraw, 48/128 from the master. Copy into the extension repo. |
| `lockup/hazel-lockup-{horizontal,stacked}-{light,dark}.svg` (+ `-1200.png`) | Hazel + wordmark. "Simple Money Tools" in Spectral SemiBold outlined to paths; light = ink `#103A55` type, dark = cream type. Disc-less Hazel in both. Minimum 120 px wide (horizontal). |
| `social/og-image-hazel.{svg,png}` | Open Graph 1200×630, Daylight palette. |
| `social/chrome-store-tile-440x280`, `social/chrome-store-marquee-1400x560` | Chrome Web Store promo images (Personal Dashboard Pro). |
| `social/gumroad-cover-1280x720`, `social/gumroad-thumbnail-600x600` | Gumroad cover (Daylight) and square thumbnail (night) for Budget Tracker Pro. |
| `png/hazel-rust-mark-nodisc-{512,256}.png` | Disc-less rasters. |
| `size-check-dark.png` | Old avatar vs Hazel at 320/110/40/32/16 px on a dark ground. |
| `variants.png` | Right / left / no-disc side by side. |

## Palette

| Token | Hex | Use |
|---|---|---|
| Night navy | `#132440` | Disc, £ glyph, knockout ring around the coin |
| Rust | `#C8693A` | Body, ear, paws |
| Tail | `#A24E2A` | Tail outer half (the silhouette) |
| Tail light | `#E0925F` | Tail inner half |
| Cream | `#F1EADC` | Muzzle, eye ring, inner ear |
| Ink | `#0F1F33` | Pupil, nose |
| Brass | `#C9A45E` | Coin face |
| Brass dark | `#B5762F` | Coin rim (8 px) |

Earlier rounds are kept beside this folder for reference: the round-5 set at the `hazel/` root,
`round6-silhouette/` (rejected), `round7-night/` (the four colourways this was chosen from).
Generator: `hazel5.py` for the mark; `build_lockup.py` / `build_favicon.py` / `build_social.py` for the 26 Sep additions (session scratch; the SVGs are the source of truth).

Text in the social images is outlined too (Spectral SemiBold + Libre Franklin 500/600), so nothing here depends on installed fonts.
