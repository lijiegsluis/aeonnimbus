# Aeon Nimbus Research — website notes

Static site for **LiJie Guo / Aeon Nimbus Research**, served from this repo by GitHub Pages (`CNAME` → aeonnimbus.com). Pushing to `main` deploys.

## Layout

| Path | What it is |
|---|---|
| `index.html` | The whole main site: CSS, JS, six languages and every page inline |
| `products/` | Separate built React app (product suite) |
| `reports/` | Per-strategy dashboards and PDF reports |
| `research-feed.json` | Substack snapshot, refreshed every 6 h by `.github/workflows/refresh-feed.yml` |
| `market-data.json` | Options flow + Congress trades, refreshed on US trading days by `refresh-market-data.yml` |
| `redesign-demo/` | Alternative design preview and the original audit (`AUDIT.md`) |

## Pages and routing

Pages are `<div class="pg" id="pg-<id>">` blocks; `sp(id)` shows one. The v3 layer at the end of `index.html` (`<script id="an-v3-js">`) wraps `sp` so that every page has a URL (`/#track`, `/#research`, `/#legal` …), the back button works, the tab title follows the page, and the nav highlight is derived from each button's own `sp('…')` target.

Ids: `home about track research tools strats portfolios services contact pitcher markets legal`.

Adding a page: add the `pg-<id>` block, a title in `TITLES` in the v3 script, and a nav button with `onclick="sp('<id>')"`.

## Things to keep in sync by hand

- **Call registry**: `KNOWN_CALLS` in `index.html` is the source of truth for the track record. Headline copy (`11 for 11`, `0 of 11`, meta description, JSON-LD FAQ) is static text and must be updated when a call closes.
- **Strategy count** is 16 (7 equity, 6 FX/commodity, 3 Tenkai). The portfolio builder covers 13 of them.
- **Disclosures page** (`pg-legal`) describes how each figure is calculated and where data comes from. Update it when a calculation or data source changes.

## Configuration (top of the main `<script>`)

```js
const SUBSTACK_URL     = 'https://aeonnimbus.substack.com';
const GITHUB_URL       = 'https://github.com/lijiegsluis?tab=repositories';
const CONTACT_ENDPOINT = '';   // form backend URL (JSON POST) — set this to make the contact form deliver
const CONTACT_EMAIL    = '';   // or an address for a mailto: fallback
```

With both contact values empty the form copies the message to the clipboard and points to LinkedIn.

## Known gaps

- API keys for the quote and AI services are embedded in `index.html` and visible to visitors. They should be rotated and the calls moved behind a server-side proxy (the `aeon-ai/worker` Cloudflare Worker already wraps the same providers).
- Heatmap, earnings, economic and IPO panels are illustrative and labelled as such.
- Track-record alpha needs an S&P 500 price series in `market-data.json` to be computed without a browser-side fetch.

## Branding

Gold `#C8830A` on near-black, light theme on warm paper; Georgia for display, Space Mono for data. LinkedIn: https://www.linkedin.com/in/lijieguo-es/ · Substack: https://aeonnimbus.substack.com
