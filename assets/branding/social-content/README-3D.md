# Hazel — 3D pose library and post composites, 29 Sep 2026

The avatar renders themselves (teal and night, all sizes) live in `../logo/` — that is the site logo now.

James wanted the Simple Money Tools avatar to compete with the Gran Haul Cards one: a 3D
toy-style character filling the circle, adult but not corporate. This folder is that.

| File | Use |
|---|---|
| `../logo/hazel-3d-1080.png` | **Instagram avatar** (upload this) and the site logo master. Teal ground, cat mouth, head tilt. |
| `../logo/hazel-3d-night-1080.png` | Night-navy ground alternate. |
| `poses/hazel-pose-<pose>-{1080,512}.png` | **Pose library**, transparent PNG: `coin wave thumbs point laptop chart sleep`. For post graphics, Reel covers, tutorial thumbnails, extension empty states. Add a soft ellipse shadow under her when compositing (see `compose_post.py`). |
| `hazel3d.py` | The whole scene as a script for Blender-as-a-Python-module (`pip install bpy`, Blender 5.0). |
| `compose_post.py` | 1080×1350 feed-post composer used for `posts/post-01-meet-hazel`. |

The OG image at `../social/og-image-hazel.png` now uses the 3D Hazel (`coin` pose); the flat
version is kept beside it as `og-image-hazel-flat.png`.

## Decisions along the way
- Flat/vector avatar options were shown first; James asked for a 3D style — "not childish in any
  way, target is adult investors, but not overly corporate".
- Expression: **cat/squirrel mouth** + slightly narrowed eyes + small head tilt. A single thin
  smile line was "a little creepy"; wink, open mouth and dimples were shown and not chosen.
- £ on the coin is **cream** so it pops at 40 px. Paws grip the coin rim.
- Ground tones tried: night, apricot, sage, teal, sky, holiday. **Teal** chosen — "teal looks good".
  Teal isn't in the Daylight palette yet; it's acting as the social accent.

## Rendering
```
python3 hazel3d.py out.png 1080 128 teal tilt coin
#                  ^file    ^px  ^samples ^ground ^expression ^pose
```
Grounds: `night apricot sage teal sky holiday clear` (`clear` = transparent, no floor; append
`-navyglyph` for a navy £). Expressions: `neutral cat tilt smile dimple cheek open wink`
(`tilt` = cat mouth + head tilt). Poses: `coin wave thumbs point laptop chart sleep`.
~4–5 min per 1080 render on CPU with a ground, ~1.5 min transparent.
