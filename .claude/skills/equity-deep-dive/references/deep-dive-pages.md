# Skill: Aeon Nimbus Equity Deep Dive (document-style pages)

A single-company initiation, written as fixed-size pages (like the IREN and FN deep dives). It shares the Aeon Nimbus style with the weekly deck (see SKILL.md): cream ground, gold rules, Inter 800 headlines, Newsreader italic asides, red/green for negative/positive only.

## When to use which
- **Weekly deck (8 slides, 1920×1080):** market note, catalyst, positions, calendar. Broad and fast.
- **Deep dive (about 12 pages):** one stock, one thesis, with valuation. Dense and evidence-led, printable to PDF.
- Both use the same palette, type scale, stat blocks, callouts and footer logic. A deep dive is read, so it can carry more text per page than a slide, but never below 12pt in print.

## Page set (12 pages, each `.page` with `data-screen-label`)
1. **Cover:** ticker, date, price → target, rating, 4 headline stats.
2. **Thesis:** one-sentence variant view ("the gap is in the...") plus 3 supporting numbers.
3. **Business model:** why the core asset is the moat; how it earns money.
4. **Financial overview:** revenue, margin, cash, debt; one table, one chart.
5. **WACC and DCF:** construction of the discount rate, the cash-flow build, the resulting value.
6. **Sensitivity and peers:** WACC × growth grid, peer multiples, unit economics.
7. **Three pillars:** the thesis in three evidence blocks.
8. **CapEx coverage and 2030 model:** can funding cover the plan; the target-year bridge.
9. **Variant views and reverse DCF:** what the market is pricing, three places we differ.
10. **Payoff and ownership:** bull/base/bear payoff and who owns it.
11. **Risks and catalysts:** ranked risks, dated catalyst watchlist.
12. **Position and references:** entry, target, stop, size, ledger, sources.

Narrative: what we think → why the asset is special → numbers → valuation → what could go wrong → what we do.

## Running elements
- **Header on every page:** `Aeon Nimbus Research · [Company] · [section]` on the left, `Long [TICKER] · $entry → $target` on the right.
- **Footer:** sources and page number.
- **Headline = conclusion**, not a topic ("Why power is the actual constraint", not "Business model").

## Rules
- Every number is sourced (filing, call, data vendor) or labelled as our estimate.
- State entry, target, stop and position size. Show the downside case with the same weight as the upside.
- A valuation page must show the inputs, not only the answer. Include a sensitivity grid.
- Variant view: say what the market believes and why we differ, with the evidence that would prove us wrong.
- Simulated AUM and "not investment advice" disclaimer on the cover and last page.
- Build on `doc-page.js` with explicit pagination (one `.page` per section) so it exports to PDF without extra work. Check each page for overflow.

## Companion outputs
- **Slide version:** compress to 6–8 slides (Thesis, Business, Financials, Valuation, Variant view and payoff, Risks and catalysts, Position). One idea per slide, 24px minimum text.
- **LinkedIn post (250–300 words):** hook with the variant view, three evidence points, valuation in one line (target, upside, downside), the risk that would make us wrong, entry/target/stop, "full report attached", disclaimer. Attach the PDF as a carousel.
