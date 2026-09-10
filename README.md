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
| Contact email `SimpleMoneyTools1@gmail.com` | `contact.html`, `js/main.js`, `contact.php` | Confirmed live by the project owner 2026-09-10. Replaced an earlier generic address on this domain that was never actually created, so mail sent to it went nowhere. Also hard-coded in the Personal Dashboard Pro extension (`config.js`'s `SUPPORT_EMAIL`, a separate repository) — change all four together. |
| Contact form submission | `contact.php` | **Wired up** — posts to `contact.php`, which emails the address above. See below. |
| Newsletter/"register interest" form | `index.html`, `contact.html` | No backend connected — see below |
| Production URLs (canonical, Open Graph, sitemap) | all pages, `sitemap.xml`, `robots.txt` | Use the real domain `https://simplemoney-tools.co.uk/` already, but assume the site is deployed there — update if that changes |

To update a social link: edit every `data-placeholder-link="instagram"` (or
`"tiktok"`) anchor's `href`, and remove the `data-placeholder-link` attribute
and the "coming soon" wording once the account is live.

### The contact form

`contact.html` posts to **`contact.php`**, the one server-side file on this
otherwise-static site. It validates the submission, applies a light per-IP
rate limit, and emails the result to `SimpleMoneyTools1@gmail.com` via PHP's
`mail()`. Nothing is stored anywhere — there is no database.

`js/main.js`'s `initContactForm()` intercepts the submit and posts via
`fetch`, so the page doesn't navigate. That is progressive enhancement, not
the only route: the `<form>` keeps a real `action`/`method`, and `contact.php`
answers a non-JSON request with a 303 redirect back to
`contact.html?sent=…`, which `showRedirectOutcome()` then renders. So the
form works with JavaScript off, or if `main.js` fails to load.

**The success message is never shown unless the server actually confirmed
delivery.** Every failure path names the email address instead. Keep it that
way — a message silently lost is worse than a visible error.

#### Deliverability — read this before debugging "the form is broken"

`mail()` hands off to the host's local MTA, so:

- `From:` **must** be an address on this domain (`FROM_ADDRESS` in
  `contact.php`). It doesn't need a real inbox, but the domain's **SPF record
  must authorise Hostinger's mail servers**, or Gmail will spam-file or
  silently drop the message.
- The visitor's address goes in `Reply-To:`, never `From:`. Putting it in
  `From:` is the single most common reason these forms stop being delivered.
- If mail stops arriving, check SPF/DMARC in hPanel **first**, before
  anything in the PHP.

Send a real test message through the live form after any change here — a
200 from `contact.php` only means `mail()` accepted it for delivery, not
that it landed in the inbox.

### The newsletter form

`initNewsletterForm()` is still client-side only — no email service is
connected, and the `.form-note` next to it says so plainly. If you wire it
up, update that note and the "This website" section of `privacy.html` at
the same time.

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

## The two privacy policies

There are deliberately **two** separate privacy pages, and they are not
interchangeable:

| Page | Covers | Indexed? |
|---|---|---|
| `privacy.html` | The website, the free Budget Tracker, the free Personal Dashboard extension | No — `robots` `noindex` |
| `personal-dashboard-pro-privacy.html` | The **Personal Dashboard Pro Chrome extension only** | Yes — in `sitemap.xml`, deliberately crawlable |

`https://simplemoney-tools.co.uk/personal-dashboard-pro-privacy.html` is the
URL given to the **Chrome Web Store** as Personal Dashboard Pro's privacy
policy, and it is referenced from inside the extension itself (a separate
repository: `index.html`'s footer link and
`src/components/settings/pro-settings-panel.js`). **Do not rename, move or
delete that file** — a dead privacy-policy URL is grounds for the listing
being taken down. Each page links to the other.

Every factual claim on the Pro page was checked against the extension's
actual source, not its marketing copy. If you change what the extension
does, change that page in the same commit. In particular it currently
asserts, and these must stay true:

- Trading 212: exactly two read-only calls (account summary, open
  positions), credential local-only and never exported, no write capability
  anywhere in the code, Invest/Stocks ISA only — **no SIPP or CFD support**,
  because that API doesn't expose them.
- Strava: OAuth with `activity:read` and `profile:read_all` only, no write
  scope, password never seen by the extension.
- The Strava fitness estimate, activity streak and the weekly trend rows
  (Activities, **Activity time**, Swim, Bike, Run) are the extension's own
  calculations and must never be described as official Strava metrics. The
  metric is called "Activity time", not "Training time".
- **Garmin is not mentioned at all**, and must not be — it has no UI in the
  product, not even Demo. Don't reintroduce it as a feature or a "coming
  soon", on this page or on `tools.html`.
- Weather coordinates are rounded to 2 decimal places **in the browser**
  (`roundCoord()` in the extension's `utils.js`) before the request leaves
  the device.
- The "delete all local data" control is free for every user and is
  deliberately not paywalled.

## Deploying the site

**Live host: Hostinger**, deploying from this GitHub repository. Pushing to
`main` is what ships — there is no build step (the site is plain
HTML/CSS/JS), and no separate upload.

Two things follow from being on Hostinger specifically:

- **PHP is available**, which is what `contact.php` relies on. A purely
  static host (GitHub Pages, Cloudflare Pages) would break the contact form.
- **The repo root is the web root.** Every file committed here is publicly
  fetchable, including this README — `/README.md` returned HTTP 200 before
  `.htaccess` was added to block it. Don't put anything in this repo you
  wouldn't publish.

After a deploy, confirm the change is actually live rather than trusting the
push. The `Last-Modified` header is unreliable here (it reflects the file's
mtime on Hostinger's disk), so check for a string you know you changed:

```sh
curl -s https://simplemoney-tools.co.uk/tools.html | grep -c "one-time"
```

Also re-check `robots.txt`, `sitemap.xml` and every `canonical`/`og:url` tag
still match the live domain.

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
- **Contact email** (`SimpleMoneyTools1@gmail.com`) — real and confirmed
  live by the project owner, 2026-09-10.
- **Contact form** — wired up and delivering via `contact.php`. See
  "The contact form" above, including the SPF caveat.
- **Newsletter form** — still client-side only, no backend, and the form
  says so on the page. See "The newsletter form" above.
- **Favicon** — hand-authored SVG placeholder in brand colours, not derived
  from the real logo file (no image-editing tool was available in this
  environment to crop/export one — see Known limitations). Swap in a real
  exported favicon set (16×16, 32×32, apple-touch-icon) when available.
- **Personal Dashboard Pro pricing** — set: £5, one-time, lifetime. Shown
  on `tools.html`'s Pro card. The amount actually charged is whatever the
  ExtensionPay dashboard says for the `personal-dashboard-pro` extension
  id, so change it there first and mirror it on the site.
- **Chrome Web Store URL for Pro** — still a placeholder
  (`data-placeholder-link="webstore-pro"` on `tools.html`). Pro is a
  separate extension from the free Personal Dashboard, so it gets its own
  store id once the submission is approved. See the HTML comment on that
  card for why it must **not** link straight to ExtensionPay.
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
