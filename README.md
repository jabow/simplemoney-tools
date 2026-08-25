# Simple Money Tools — website

A static, dependency-free website for the Simple Money Tools brand: a home page,
a full tools directory, tutorials/instructions, an about page, contact page, and
draft privacy/terms pages. Plain HTML, CSS and vanilla JavaScript — no build
step, no framework, no npm install required.

Design language is adapted from [james-bowen.co.uk](https://james-bowen.co.uk/)
(dark theme, card layouts, sticky nav, restrained motion), given its own
identity via the Simple Money Tools brand colours (green/blue, from the logo)
and a Sora/Inter type pairing.

## Project purpose

- Showcase the free and paid Simple Money Tools products
- Promote the Simple Money Tools Chrome extensions (Personal Dashboard, and
  the in-development Simple Money Tools Pro)
- Provide tutorials and setup instructions
- Link to the Simple Money Tools YouTube, Instagram and TikTok accounts
- Build trust in the brand with honest, non-hyped copy
- Act as a central platform that can grow as more tools ship

## File structure

```
simplemoney-tools/
├── index.html          Home page
├── tools.html           All tools, with category filters
├── tutorials.html       Written guides, video guides, search, troubleshooting, FAQ
├── about.html            Brand story + about the creator
├── contact.html          Contact form (placeholder) + social links
├── privacy.html           Draft privacy policy
├── terms.html             Draft terms of use
├── robots.txt
├── sitemap.xml
├── css/
│   └── styles.css        Single shared stylesheet (design tokens + components)
├── js/
│   └── main.js            Shared behaviour (nav, filters, forms, animations)
├── assets/
│   ├── branding/           Logo, favicon, brand marks
│   ├── icons/               Source SVG icons (also inlined directly in HTML)
│   ├── images/               (reserved for future page imagery)
│   └── screenshots/          Product screenshots used across tool cards
└── README.md
```

## Running it locally

No build step. Either:

- Open `index.html` directly in a browser, or
- Serve the folder so relative paths and `fetch`-based features (if added
  later) behave like production, e.g.:
  ```sh
  cd simplemoney-tools
  python -m http.server 8080
  # then visit http://localhost:8080
  ```

## Editing tools (`tools.html` / home page featured cards)

Each tool is a `<article class="tool-card">` block. To add a new one:

1. Copy an existing `.tool-card` block in `tools.html`.
2. Set a unique `id` (used for deep-linking, e.g. `tools.html#your-tool`).
3. Set `data-tags` to a space-separated list matching the filter buttons
   (`budgeting`, `chrome-extensions`, `dashboards`, `free`, `paid`,
   `coming-soon`) — add a new filter button in `.filter-bar` if you introduce
   a new category.
4. Update the screenshot, badges, feature list and action links.
5. If it should also appear on the home page, copy the relevant `.tool-card`
   into `index.html`'s "Featured tools" section too (kept separate
   deliberately, since the home page is a curated subset, not the full list).

Filtering is handled by `initToolFilters()` in `js/main.js` — it reads
`data-tags` on each card and toggles visibility; no changes needed there for
a new tool, only new filter categories.

## Adding tutorials

Tutorial cards live in `tutorials.html`. Each is an `article.tutorial-card`
with:

- `data-tags` — space-separated categories used by the filter buttons
- `data-search` — free-text keywords used by the search box (title +
  description + anything else worth matching on)

Written guide *content* (the actual instructions) lives further down the
same page in `<section>` blocks with `id`s that the card's "View Tutorial"
button links to (e.g. `#budget-tracker-guide`). Video cards link straight
out to YouTube instead.

To add a new tutorial: copy a card, give it a unique `data-search` string,
add it to an existing filter category (or add a new filter button), and
either add a written guide section or link out to a video.

## Replacing placeholder links

Search the codebase for `PLACEHOLDER` and `data-placeholder-link` — every
placeholder is commented in the HTML source at the point it's used. Current
placeholders:

| What | Where | Current state |
|---|---|---|
| Instagram URL | nav, footer, `index.html` social section | `href="#"`, `data-placeholder-link="instagram"` |
| TikTok URL | nav, footer, `index.html` social section | `href="#"`, `data-placeholder-link="tiktok"` |
| Contact email `hello@simplemoney-tools.co.uk` | `contact.html` | Real domain, but confirm the mailbox exists before publishing |
| Contact form submission | `contact.html` | No backend connected — see below |
| Newsletter/"register interest" form | `index.html`, `contact.html` | No backend connected — see below |
| Production URLs (canonical, Open Graph, sitemap) | all pages, `sitemap.xml`, `robots.txt` | Use the real domain `https://simplemoney-tools.co.uk/` already, but assume the site is deployed there — update if that changes |

To update a social link: edit every `data-placeholder-link="instagram"` (or
`"tiktok"`) anchor's `href`, and remove the `data-placeholder-link` attribute
and the "coming soon" wording once the account is live.

### Wiring up the contact / newsletter forms

Both forms in `js/main.js` (`initContactForm`, `initNewsletterForm`) currently
only run client-side validation and show a status message explaining that
nothing was actually sent — they intentionally do **not** claim to submit
anywhere. To make them real, pick one:

- A form backend (e.g. Formspree, Netlify Forms, Getform) — point the
  `<form>`'s `action`/`method` at their endpoint and remove the
  `e.preventDefault()` short-circuit (or call their API via `fetch`).
  Adjust the status message copy accordingly.
- A custom backend endpoint — same idea, `fetch()` your endpoint from
  `main.js` instead of showing the placeholder message.

Either way, update the `.notice-box` text in `contact.html` and the
`.form-note` text next to the newsletter form once it's live.

## Replacing screenshots

Screenshots live in `assets/screenshots/`. They're referenced directly by
filename in the HTML (`<img src="assets/screenshots/...">`), so:

1. Add the new image to `assets/screenshots/`.
2. Update the relevant `<img src>` and `alt` text.
3. Keep images reasonably sized/compressed before adding them — this
   environment didn't have an image-processing tool available when the site
   was built (see **Known limitations** below), so the screenshots currently
   in the repo are un-optimised copies of the originals.

## Branding assets

Copied from `BCA_TECH Dropbox\James Bowen\_James\Shared Personal\Simple Money
Tools\Branding` (originals untouched):

- `assets/branding/logo-mark.jpg` — icon-only mark (from `Logo1.jpg`), used
  in the nav, footer and as the source for `apple-touch-icon`.
- `assets/branding/logo-full.jpg` — icon + wordmark (from `ZMg5g.jpg`), used
  on the About page and as the Open Graph share image.
- `assets/branding/favicon.svg` — **hand-authored**, not from the branding
  folder. No transparent/square export of the real logo existed to use as a
  crisp favicon, so this is a simplified SVG recreation in the brand's
  accent colours. Replace with a proper exported favicon from the real logo
  when one is available (see **Known limitations**).
- `assets/branding/dashboard-extension-icon.png` — the real Personal
  Dashboard Chrome extension icon (from
  `Personal-Dashboard/icons/icon128.png`).
- `assets/screenshots/budget-tracker-dashboard*.png` — real Budget Tracker
  dashboard screenshots (from the Branding folder).
- `assets/screenshots/dashboard-pro-*.jpg` — real Personal Dashboard Pro
  Chrome Web Store screenshots (from `Personal-Dashboard-Pro/store-assets/`;
  these use placeholder demo data — "Alex", sample prices — not a real
  user's data).

The `You Tube Banner.png` and everything under the Branding folder's
`not used/` subfolder were deliberately **not** used, per their naming.

## Deploying the site

It's static HTML/CSS/JS — any static host works. For the `simplemoney-tools.co.uk`
domain, options include:

- **GitHub Pages**: push this repo, enable Pages on the `main` branch, point
  the domain's DNS at GitHub Pages, add a `CNAME` file with
  `simplemoney-tools.co.uk`.
- **Netlify / Vercel / Cloudflare Pages**: connect the repo, no build
  command needed (leave build command empty, publish directory = repo root).
- **Any traditional host**: upload the folder contents as-is via FTP/SFTP.

Once deployed, double-check `robots.txt`, `sitemap.xml` and every
`canonical`/`og:url` tag actually match the live domain.

## Git repository

A local Git repository was initialised in this folder with `main` as the
default branch, and an initial commit was made after the site was built and
checked. GitHub CLI (`gh`) was not installed in this environment, so no
remote repository was created automatically. To connect one manually:

```sh
# create the repo on GitHub first (via the web UI), then:
git remote add origin https://github.com/<your-username>/simplemoney-tools.git
git branch -M main
git push -u origin main
```

If you install GitHub CLI (`gh`) and authenticate it, you can instead run,
from inside this folder:

```sh
gh repo create simplemoney-tools --private --source=. --remote=origin --push
```

## Outstanding placeholders & decisions

- **Instagram and TikTok URLs** — not found anywhere in the branding folder
  or existing project files, so left as clearly labelled placeholders
  throughout (see table above). Do not invent handles; update once real
  URLs exist.
- **Contact email** (`hello@simplemoney-tools.co.uk`) — uses the real domain
  by convention, but the mailbox itself hasn't been confirmed to exist.
  Set it up (or change the address) before publishing.
- **Contact form and newsletter form** — client-side validated only, no
  backend. See "Wiring up the contact / newsletter forms" above.
- **Favicon** — hand-authored SVG placeholder in brand colours, not derived
  from the real logo file (no image-editing tool was available in this
  environment to crop/export one — see Known limitations). Swap in a real
  exported favicon set (16×16, 32×32, apple-touch-icon) when available.
- **Simple Money Tools Pro pricing** — intentionally not shown anywhere on
  the site, since Pro isn't released and no real price has been set. The
  site instead offers a "register interest" path. Add pricing once it's
  decided.
- **Screenshot optimisation** — screenshots are unmodified copies of the
  source files; no compression/resizing pass was possible in this
  environment (see below). Run them through an image optimiser before final
  production deploy.

## Known limitations

- **No image-processing tool was available** (no ImageMagick, no Python
  Pillow) when this site was built, so:
  - The favicon is a hand-drawn SVG rather than a proper export/crop of the
    real logo.
  - Screenshots and logo files were copied as-is, without resizing or
    compression.
- **No `gh` (GitHub CLI)** was installed, so a GitHub repository could not be
  created or pushed to automatically — only a local Git repo was set up.
  See "Git repository" above for the manual commands.
- This was built and reviewed in a headless browser check (console errors,
  broken links, responsive layout) rather than manual testing across every
  real device/browser — spot-check on an actual phone/tablet before launch.
