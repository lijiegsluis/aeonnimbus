---
name: equity-deep-dive
description: Aeon Nimbus equity research automation. Use whenever the user sends a stock ticker on its own (e.g. "NVDA", "$IREN", "MELI"), or asks for a deep dive, initiation, equity research or "análisis" of a company. Researches live data, builds the WACC/DCF/blend valuation, writes the research note under the Aeon Nimbus master prompt, lays it out as the 12-page Claude Design deep dive (cream/gold, Inter + Newsreader) and renders a PDF to reports/.
argument-hint: TICKER [es] [entry=PRICE] [watching]
---

# Aeon Nimbus · Equity Deep Dive (ticker → PDF)

One ticker in, one printable 12-page deep dive out, plus the full research note behind it.

**Arguments:** `TICKER` (required). Optional: `es` (write in Spanish; default English, like the FN report), `entry=123.45` (use this entry instead of the last close), `watching` (publish as a pre-entry call).

## Sources of truth (read before writing; in this order)

| File | Governs |
|---|---|
| `references/master-prompt.md` | **Content**: voice ("We believe / We note"), banned phrases, the 23-element deep-dive structure, WACC rules, sizing, the 7-row valuation blend, variant-view format, position statement, the 10 questions. Its "OUTPUT FORMAT" block (Cormorant/Crimson, 900px HTML, Chart.js) is **superseded** by the two design files below for this PDF. |
| `references/deep-dive-pages.md` | **The PDF**: 12-page set, running header/footer, headline = conclusion, sensitivity grid, downside at equal weight. |
| `references/aeon-nimbus-style.md` | **Visual language**: palette, type, stat blocks, callouts, range bar, tables. Also the weekly-deck and LinkedIn rules for companion outputs. |
| `references/examples/FN_Fabrinet_Deep_Dive_2026-10-02.md` | **Quality bar** for the research note: depth, sourcing, honesty about where the evidence is weaker. Match it. |
| `references/examples/MRVL_*`, `ORCL_*` | Risk-score and technical-read formats; use their method for the entry-timing/technicals section. |
| `assets/template-deep-dive.html` | Worked 12-page example (FN). Copy it; never start the layout from scratch. |
| `../../../research/positions.json` | Open book and closed calls, for the position statement and portfolio fit. |

## Paths

`T` = ticker in upper case, `t` = lower case, `D` = today's date (YYYY-MM-DD). Work folder: `research/T/D/`.

- `research/T/D/sources.md`: every fact used, with source and date
- `research/T/D/inputs.json` → `valuation.json` / `valuation.md`
- `research/T/D/T_<Company>_Deep_Dive_D.md`: the research note (master-prompt structure)
- `research/T/D/deep-dive.src.html`: the 12-page source
- `reports/t-deep-dive.pdf` and `reports/t-deep-dive.html`: the deliverable (same naming as the other reports in `reports/`)

Scripts run from the repo root: `S=.claude/skills/equity-deep-dive`.

## Workflow

Track the steps with the task list. Do not stop between steps to ask for approval: the user typed a ticker because they want the PDF. Ask only for the open book (step 1), and only when it is unconfirmed.

### 1. Book check (parallel with step 2)
Read `research/positions.json`. If `open_book_confirmed` is false or `as_of` is more than 14 days old, ask the user once, in one short message, for the open positions (ticker, entry, date, target, stop, size), and continue researching while you wait. If you get no answer, write the position statement with the closed-call record only, and flag it in the final message. Never invent open positions.

### 2. Research: data first, writing second
Search the live web. Never use numbers from memory. Run the searches in parallel batches. At minimum, cover the master prompt's 8 searches plus:
- Price at the latest close, 52-week range, shares diluted, market cap, net debt or net cash → EV
- Latest 10-K/20-F and 10-Q, plus the latest earnings release and call: segments, top customers, guidance, capex, cash flow, working capital
- Five-year history (revenue, growth, net income or EBITDA, margin, EPS, one sector KPI)
- Your own historical multiples: 4–5-year average EV/EBITDA, EV/Sales and P/E, with the matching average metric
- At least 5 peers with forward EV/EBITDA, EV/Sales and P/E, growth and margin, each with a dated price
- 10Y Treasury on the day; beta (TradingView 3-year, cross-checked with a second vendor); ERP 5.5%; CRP if more than 50% of revenue is EM; a size premium for small caps
- Named sell-side ratings and targets with dates; the strongest named bear case
- Ownership (13F/13G), insider holdings, short interest
- Technicals: 50/200-day averages, supports and resistances, the last gaps (ORCL example method)
- Dated catalysts for the next 6–12 months; news since the last print

Log each fact in `sources.md` as `metric | value | source | date`. If you cannot verify a number from a primary or reputable source, say so in the note. Do not fill the gap.

### 3. Valuation
Copy `assets/valuation-inputs.example.json` to `research/T/D/inputs.json` and fill it in. Run:
`python3 $S/scripts/valuation.py research/T/D/inputs.json research/T/D/valuation`.

The script outputs the WACC build, the DCF (explicit years; Gordon anchor plus exit multiple), the WACC × exit and WACC × g grids, the reverse DCF, the 7-row blend (negative or n/m peers excluded and listed), the scenarios, the payoff and half-Kelly. Use its numbers verbatim; never retype a computed number by hand.

Setting the call:
- **Target:** by default, the blended target price (master prompt). If you use another anchor (for example, the scenario median or a forward multiple roll, as FN did), the note must say so and show the blend next to it.
- **Stop:** a structural level, such as below the 52-week low or the support that breaks the thesis. State the reason.
- **Size:** 3% standard, up to 4% for highest conviction, 3% cap for EM, 2% planned when watching. Never above half-Kelly.
- **Direction:** Long only if upside to target is at least about 15% and payoff is at least 2:1. Otherwise publish as **Watching**, with the entry level at which it becomes a buy. Saying "not now" is a valid result.
- Scenario weights follow the master-prompt bands (bear 15–25%, base 50–55%, bull 25–30%).

### 4. Research note
Write `T_<Company>_Deep_Dive_D.md` with the master prompt's mandatory structure, in FN's register:
- Standfirst with the number that proves the mispricing
- The ten-questions table
- Business model before any number
- The financial table (at least 10 rows)
- WACC, then DCF, then the sensitivity grid, then peers, then the blend table
- 3 pillars, the institutional case, 3+ variant views (each with a named consensus bank or analyst and a falsifiable condition), the reverse DCF, payoff, risks (5–6), catalysts (5–6, dated)
- LinkedIn variants (3), the exact position statement listing all open positions, 10+ dated references

Run `python3 $S/scripts/lint_note.py <note.md>` and fix every error.

### 5. The 12-page PDF
Copy `assets/template-deep-dive.html` to `research/T/D/deep-dive.src.html`. Replace the content page by page, following `deep-dive-pages.md`:
1. Cover (dark)
2. Thesis
3. Business model
4. Financial overview
5. WACC and DCF
6. Sensitivity and peers
7. Three pillars
8. CapEx coverage and the target or 2030 bridge
9. Variant views and reverse DCF
10. Payoff and ownership
11. Risks and catalysts
12. Position and references (dark)

Layout rules:
- Set `<body data-company data-ticker data-direction data-entry data-target>`, and give every `.page` a `data-section` and `data-sources`. The header and footer are generated from these.
- Each headline is the conclusion. The text is condensed from the note: no new numbers appear in the PDF.
- Charts are divs (`.vbars`, `.hbars`, `.share`, `.rangebar`). Grids use `table.sens` with the `.base` cell outlined. Use `.pos`/`.neg` colours only for positive and negative values.
- All text is at least 12pt (the builder flags anything smaller).

Build and inspect:
```
node $S/scripts/build.mjs research/T/D/deep-dive.src.html reports t-deep-dive --png <scratchpad>/T-png
```
The build fails on overflow. Read every PNG, fix overflow, clipping, empty bands and orphan lines, then rebuild until it is clean with no warnings. Run `lint_note.py` on the `.src.html` too. Check the result with `pdfinfo reports/t-deep-dive.pdf`: 12 pages, A4.

### 6. Deliver
- Send `reports/t-deep-dive.pdf` with SendUserFile.
- In chat, answer in the user's language (Spanish if they wrote in Spanish) with:
  - the verdict strip (direction, entry, target, stop, size, horizon)
  - the thesis in one line
  - the blend versus target, and the main risk
  - anything you could not verify
- Offer, in one line each: (a) commit and push the report, note and inputs; (b) add the call to `research/positions.json` and the site's track record; (c) a 6–8-slide version or the LinkedIn carousel (`aeon-nimbus-style.md`).
- Do not edit `index.html`, `research-feed.json` or the ledger unless the user asks.

## Notes
- If Playwright is missing on another machine: `npm i -D playwright && npx playwright install chromium`. Fonts load from Google Fonts; offline, the page falls back to local Inter and Georgia.
- Non-US listings: use local currency (`"currency": "€"` in the inputs and `data-currency` on `<body>`), the local 10Y as Rf plus CRP per the master prompt, and the local exchange in the kicker.
- Pre-profit companies: set `"pre_profit": true` in the blend, which swaps the P/E rows for EV/Revenue. Do not use a Gordon anchor on negative terminal cash flow; use the exit multiple (`"anchor": "exit"`) and say why.
