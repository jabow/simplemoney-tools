# Simple Money Tools branding — start here

**The logo is `logo/hazel-3d-1080.png`.** Hazel, the 3D rust squirrel holding a pound coin, on a
teal ground (chosen 29 Sep 2026). Everything the site shows is cut from that file.

| Folder | What is in it | Use it for |
|---|---|---|
| `logo/` | **Current logo.** `hazel-3d-{1080…32}.png` square; `circle/hazel-3d-circle-{512…16}.png` circle-masked with transparent corners; `favicon.ico` (16/32/48); `hazel-3d-night-*.png` navy-ground alternate. | Site header and footer (`circle/…-128`), favicon (`favicon.ico` + `circle/…-32`), apple-touch-icon (`hazel-3d-180`), founder avatar and About page (`hazel-3d-512`), Instagram avatar (`hazel-3d-1080`). |
| `social/` | Open Graph image, Chrome Web Store tile and marquee, Gumroad cover and thumbnail. | Link previews, store listings. `og-image-hazel.png` is the live OG image (3D Hazel); `-flat.png` is the previous one. |
| `social-content/` | Pose library (`poses/`, `poses-teal/`), Instagram post composites (`posts/`), the Blender script (`hazel3d.py`) and post composer. See `README-3D.md`. | Making new posts, Reel covers, tutorial thumbnails. Not used by the site. |
| `hazel-flat/` | The flat vector Hazel (26 Sep 2026): SVG master, lockups with the wordmark, small-size favicon SVG, Chrome extension icon set, flat Instagram avatar. See its `README.md`. | Anywhere a vector or a wordmark lockup is needed. The Personal Dashboard Pro extension icons still come from here. |
| `archive/` | Every earlier mark, oldest first: chart-arrow, Medallion, pastel squirrel v1, the Hazel design rounds. See `ARCHIVE-README.md`. | Reference only. |

To re-cut the logo sizes from the master, run `python rebuild-logo-sizes.py` in this folder (needs Pillow).

History: chart-arrow → Medallion (14 Sep 2026) → pastel squirrel (15 Sep) → flat Hazel (26 Sep) → 3D Hazel (29 Sep, site-wide from 30 Sep).
