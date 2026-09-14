# Medallion mark — Simple Money Tools

Added 14 September 2026. These files sit alongside the existing branding assets and
nothing currently references them, so the live site is unchanged until you swap the
links below.

## Files

| File | Use |
|---|---|
| `logo-medallion.svg` | Master. Square 96×96 viewBox, transparent background. Use anywhere 48 px and above. |
| `logo-medallion-small.svg` | Simplified cut — no inner ring, two columns, heavier ribbon. Use at 32 px and below. |
| `logo-medallion-16.png` / `-32.png` | Rendered from the simplified cut. |
| `logo-medallion-48.png` / `-128.png` / `-180.png` / `-512.png` | Rendered from the master. |
| `favicon-medallion.ico` | 16 / 32 / 48 bundle for browsers that ignore the SVG favicon. |

## Palette

| Role | Hex |
|---|---|
| Coin | `#9DD7D9` |
| Coin inner ring | `#FFFFFF` at 50% |
| Columns | `#ACCF98` |
| Ribbon | `#71B096` |
| Ribbon shadow | `#4E8A66` |

## Construction

The columns are the area under the ribbon, clipped into three tracks — that is why the
column tops follow the line exactly. The shadow is the same ribbon path offset 3.6 units
down and drawn only inside the columns. Keep the ribbon at one stroke weight; do not add
a second colour to the coin.

## To switch the site over

In every page's `<head>`:

```html
<link rel="icon" type="image/svg+xml" href="assets/branding/logo-medallion.svg" />
<link rel="alternate icon" href="assets/branding/favicon-medallion.ico" />
<link rel="apple-touch-icon" href="assets/branding/logo-medallion-180.png" />
```

Then replace the `assets/branding/logo-mark.jpg` image sources — `index.html` uses it at
34 px (header), 136 px and 32 px — with `logo-medallion.svg`. The old JPEGs have a baked-in
background; the SVG is transparent, so check it against whatever sits behind it.

Still to make: the horizontal and stacked lockups with the wordmark, a replacement for
`logo-full.jpg` (og:image, 1200×630) and the Chrome Web Store tile.
