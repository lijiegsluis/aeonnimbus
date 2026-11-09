# aeonnimbus.com: UI/UX and backend audit

Scope note: the live domain is blocked in the analysis sandbox (proxy returns 403), so this audit reads the deployed source in this repo (`index.html`, `products/`, `.github/`, JSON snapshots). `CNAME` points the domain at this repo, so the two should match. Anything about runtime behaviour (live quotes loading, CORS proxies answering) is inferred from code, not observed.

## 1. What the site is

One 1.2 MB static `index.html` (CSS, JS, six languages and all page content inline) plus a separate React app at `/products/`. Hosted from GitHub Pages. "Pages" are `div#pg-*` blocks toggled by `sp(id)`; the URL never changes.

| Page | Contents | Controls |
|---|---|---|
| Home | Hero ("Macro & equity research, published before the outcome"), call table, stat counters, portfolio simulation, philosophy, bio | AI Pitcher CTA, AUM and allocation inputs, subscribe |
| About | Career timeline, education, "how I build a thesis" | 2 buttons |
| Research | Substack feed rendered from `research-feed.json`, category filter, RSS badge | 5 filter buttons, 1 input |
| Track Record | KPI row, cumulative P&L chart with 5D/1M/6M/YTD/1Y/All, alpha-by-call table, footnotes, Q2 investor letter PDF | 6 buttons |
| Tools | 12 cards: 7 open-source calculators that run in-browser with Excel export (quant models, DCF engine, portfolio construction, position sizing, cross-asset correlation, idea screener, SOTP), 3 cards that deep-link to Markets, and 2 "new" tools (analyst alpha, trade exposure) | about 68 buttons and 120 inputs |
| Strategies | The main tables list 12 strategies (7 equity, 5 FX/gold) plus 3 Tenkai index/gold models, with Sharpe-vs-drawdown scatter, correlation matrix, annual-return tables, 70/30 out-of-sample check, per-strategy report PDFs and dashboards in `/reports/` | suite tabs, portfolio builder |
| Fund Lab | Paper "Asset Allocation Dynamic Fund" (NAV, performance, holdings, risk) | tabs |
| Markets | Overview, heatmap, earnings, economic calendar, IPO pipeline, congress trades, options flow | 49 buttons |
| Services / Contact / AI Pitcher | Four service cards, mailto form, invite-gated AI report generator | form, ticker input |

Global UI: dark/light toggle, 6-language switcher (EN/ES/FR/DE/IT/CN), dropdown for Research Lab, Subscribe CTA, GitHub and LinkedIn links, market-open status bar, scroll progress bar, back-to-top, page loader, grain overlay.

## 2. Backend reality

There is no server. Everything is client-side plus two scheduled GitHub Actions:

- `refresh-feed.yml` (every 6 h) pulls the Substack RSS into `research-feed.json` (about 930 KB, full post bodies).
- `refresh-market-data.yml` (weekdays 16:41 and 21:41 UTC) uses yfinance and House Clerk PDFs to build `market-data.json` (options flow, congress trades).
- The call registry (`KNOWN_CALLS`, entry/stop/target/size/exit) is hard-coded in the page script. Live P&L comes from the browser calling Finnhub directly.
- AI Pitcher calls the Gemini API straight from the browser.
- Contact form builds a `mailto:` link.

The sibling repos `aeon-platform` / `aeon-ai` already contain a Cloudflare Worker (`worker/src/finnhub.ts`, `gemini.ts`, `edgar.ts`, `cerebras.ts`, `cohere.ts`) and a FastAPI analytics service. That is a ready-made place to move every key-bearing call.

## 3. Problems found (ranked)

**P0, fix now**

1. **API keys ship to every visitor.** A Finnhub token is written inline in three `fetch` calls and again as variables for the calendar and quote code, an FMP key is in the page, and the Gemini key is only hidden behind `atob(...)`, which is not protection. Rotate all of them and move calls behind a Worker. Anyone can run up your quota or abuse the Gemini key.
2. **The contact form sends nothing.** `submitContact` opens `mailto:?subject=...` with an empty recipient, then shows "Message composed". The visitor's mail client opens with no "To" address. Visitors with webmail never get a mail client at all.
3. **Markets page is stale and partly labelled "illustrative".** Earnings filters say "Oct 14–17 / 21–24 / 28–31", the "AN Market View" is dated Sep 15 2026, and the heatmap, earnings, economic and IPO panels carry "Illustrative sample data, not a live feed" while the tab shows a LIVE badge. Only options flow and congress come from the refreshed JSON.

**P1, credibility and consistency**

4. **Numbers disagree across the page.** Home says "9 for 9" while the same section says eleven closed calls; the track-record stats table says "Losing trades: 0 of 8"; the tools page says "Six analyst tools" above twelve cards; strategies are "12", "13", "15" and "16" in different places; the FAQ structured data says "as of October 2026". For a site whose whole pitch is verifiability, internal contradictions cost trust. I recomputed from `KNOWN_CALLS`: 11 closed calls average +34.1%, matching the headline, so the data is fine and only the copy is stale. Drive every count from the registry.
5. **AI Pitcher sample contradicts the record.** The sample card shows MRVL entry $57.82 / exit $74.30, while the registry has entry $245.05 / exit $323.26 for the same +31.9% call.
6. **No real URLs.** Every view lives at `/`. Nothing can be linked, bookmarked, indexed or shared ("send me your Track Record page"), and the back button leaves the site. The sitemap lists `/#about`, `/#track` and similar fragment URLs, which search engines treat as the same page as `/`, so only one page is really indexable.
7. **1.2 MB single file.** Everything parses before first paint, hence the loader. Split data from markup.
8. **Fragile data sources.** `allorigins.win` and `corsproxy.io` are public CORS proxies, the Yahoo `query1` endpoint is unofficial, and Alpha Vantage is called with `apikey=demo`. Any of them can rate-limit or disappear and the panel silently stays empty.
9. **Unverifiable claims.** "Read by analysts at hedge funds · asset managers · family offices", "Audited performance" (the track page header; the chart note says alpha is "unverified"), and "100% hit rate" lead the page without third-party proof.
10. **Stale internal docs.** `AEONNIMBUS.md` describes a `D:/` Windows workflow, Vercel deploy and a different GitHub handle.

**P2, polish**

11. Contact form, filters and calculators have few ARIA attributes (about a dozen in the whole file). Tabs and sort controls are `div`s or untagged buttons.
12. Translation covers 104 `data-i18n` nodes; long-form content (thesis, strategy text) is English only, so the switcher over-promises.
13. No analytics, no on-site newsletter capture (it sends people to Substack), no site search, no per-call permalink.
14. Heavy decoration (grain overlay, page loader, scroll bar, back-to-top, Space Mono plus serif plus gold-on-black) competes with the data. The most valuable object on the site is the call, and it is just a table row.

## 4. Reference sites and what to borrow

Search results here were thin and some were aggregator pages, so each row says what is sourced and what is general knowledge.

| Reference | What to borrow | Basis |
|---|---|---|
| [TipRanks](https://alternativeto.net/software/tipranks/?p=5) and Fiorillo-style analyst pages | Third-party-audited hit rate for each analyst; one profile page per analyst with every call. An independent audit beats a self-reported 100%. | Search result (one analyst site cites TipRanks ranking as its verification; the 78% figure there is self-published) |
| [Koyfin](https://costbench.com/software/financial-data-terminals/koyfin/free-plan/) | A free tier with real dashboards and charting, plus watchlists. Power with a clean default. | Search result (free plan: advanced charting, dashboards, 2 watchlists, 2 screens; sources conflict on screener) |
| [Net Interest](https://sidestack.io/directory/substack/netinterest) | Free public posts, paid archive and weekly issues; the tier structure is explicit. | Search result (directory listing, figures approximate) |
| [Quantpedia](https://www.luxalgo.com/blog/quantpedia-strategy-research-guide/) | Strategy pages that separate in-sample from out-of-sample results with an equity curve, stats and code. Your 70/30 split table is the right idea; give each strategy its own page. | Search result |
| Portfolio Visualizer | Backtests with shareable parameters in the URL. | Search result mention only |
| Finviz | Treemap heatmap that actually updates. | General knowledge |
| Stratechery, Damodaran | Archive search, reading-time and a methodology page that explains how to read the numbers. | General knowledge |
| Authory and analyst-portfolio guidance | Curate best work, explain process as much as results ("why should I trust you?"). | [Search result](https://authory.com/use-cases/portfolio-for-analyst), vendor material |

## 5. What to implement

Ordered by value for the effort.

1. **Rotate keys and add a Worker proxy** for Finnhub and Gemini (reuse `aeon-ai/worker`). Add per-IP rate limits and allow-list the origin.
2. **Real contact endpoint** (Formspree or the Worker), honeypot, confirmation state. Until then show the email address as text.
3. **Per-call permalink page** (`/calls/orcl-2026-04-08`): thesis, catalyst, risks, entry/stop/target/size, live mark price, status, post-mortem on close, link to the dated Substack post, and a timestamp proof (git commit of the registry, or an archive link). This turns "published before the outcome" from a claim into something checkable. Add the registry fields that are missing: 8 open lots have no thesis text.
4. **Move the registry to `calls.json`** and generate every count, stat and the structured data from it; delete the hard-coded copy. This fixes finding 4 for good.
5. **Benchmark overlay**: add a daily S&P 500 series to the market-data job so alpha is computed, not "unverified".
6. **Real routes** (`/track`, `/research`, `/tools`, ...) from a static generator such as Astro or 11ty; drops the page to well under 200 KB and gives the sitemap real, indexable entries.
7. **Live P&L** from a scheduled `quotes.json` (same pattern as `market-data.json`) so the table needs no browser-side API calls.
8. **Freshness badges everywhere** ("Snapshot 2 days ago"). Remove the LIVE label and the illustrative panels until they are real, or hide them.
9. **Research search, tags and reading time**, saved-for-later, on-site subscribe form (Substack embed), site-wide search / command palette.
10. **Strategy pages** with equity curve, drawdown chart, annual table and CSV, plus a compare view.
11. **Privacy-friendly analytics** (Plausible or Cloudflare) to learn which pages convert to subscribers.
12. **Accessibility pass** (real tabs and sort semantics, focus states, contrast), and either translate the long-form or label the switcher "UI only".
13. **Legal check**: for UK/EU audiences confirm disclaimers and financial-promotion rules with a professional; not covered here.

## 6. The redesign demo

`redesign-demo/index.html` is a self-contained preview of a different design language, built from real data in this repo (call registry, feed, market snapshot, strategy table). It changes:

- **Layout**: sticky left rail instead of a top bar; wide content column.
- **Language**: cool grey paper and ink with one ultramarine accent; grotesque UI type, a reading serif for theses and a mono face for every number. Gold-on-black, grain, loader and scroll bar are gone.
- **Signature object**: each call is a dated "receipt" with a stop to entry to target range bar, shown on home, in the table dialog and ready for per-call pages.
- **Features added**: hash routes for every view, Ctrl+K command palette, sortable and filterable call table with drawer, copy-as-CSV, cumulative-contribution chart with a portfolio-size input, research search / sort / saved, working position-sizing and Black-Scholes tools, sortable strategy table with scatter, options-flow and congress filters with a freshness badge, light/dark/system theme.
- **Not done in the demo**: live quotes, S&P overlay, real form submission, six-language support, the Tenkai strategies, the fund page. Everything shown is static data and the demo says so.
