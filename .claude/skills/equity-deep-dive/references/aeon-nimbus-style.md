# Skill: Aeon Nimbus Weekly Deck + LinkedIn Post

Turn a weekly market note into a dense, editorial 8-slide deck (1920×1080) and a LinkedIn post, in the Aeon Nimbus style.

## Style language
- **Palette:** cream `#f6f4f0` ground, near-black `#0a0a0a` dark slides, gold `#c9962a` (deep `#a77c1d` on cream) for rules and accents, red `#c1141a` / green `#16863f` for negative / positive only.
- **Type:** Inter 800 for headlines and big numbers (tight tracking), Inter 700 uppercase tracked for eyebrows and labels, Newsreader italic for editorial asides and "vs".
- **Minimum text size:** 24px everywhere, including footers and chart labels.
- **Structure per slide:** gold eyebrow, 52–60px headline stating the conclusion, 2px gold rule, content, footer with source line and page number.
- **Components:** stat block (3px top rule, 60px number, 24px caption); callout (white box, gold left border); range bar (stop → target, entry tick, mark dot); waffle (10×10 grid); bar pairs; tables with black header row.
- **Rhythm:** dark cover, light body, one dark slide in the middle for exits if needed, dark close.
- Charts are simple divs, not images. Columns must fill the slide: use `justify-content:space-between` and verify nothing sits above empty space or under the footer.

## Slide order (8 slides)
1. **Cover:** title, subtitle, 4 headline stats (average return, win rate, NAV, key macro number).
2. **The catalyst:** the week's one news event; what circulated vs. what was confirmed; market reaction.
3. **Fundamentals and risk:** demand evidence, then who funds it (FCF, debt, capex).
4. **Macro:** rates scale, jobs, CPI, hike probability.
5. **Positions:** recent exits (left, with return, dates, reason) and open book (right: range bar, return, one-line thesis).
6. **Allocation:** waffle S&P 500 vs our book, return bars, concentration comparison, capital-protection callout with the Munger quote.
7. **Calendar and probabilities:** dated events table; 3 own probability estimates labelled as estimates.
8. **Signals and close:** more cautious / more constructive lists, then tagline and open/closed tickers.

Narrative: what happened → why it matters → macro backdrop → what we did → how we are positioned → what's next → what changes our mind.

## Rules
- Every number comes from the source note. Label own estimates as estimates. Footer states the source.
- One idea per slide; the headline is the conclusion, not the topic.
- Publish losses with the wins. Say what was right to do and what was not.
- Simulated AUM and "not investment advice" disclaimer on the close and in footers.
- Build with `deck-stage.js`, sections labelled with `data-label`. Check every slide for overflow against the footer.

## Principle (recurring close)
Protecting capital matters more than chasing returns. A 50% loss needs a 100% gain to break even. Munger: "It is remarkable how much long-term advantage people like us have gotten by trying to be consistently not stupid, instead of trying to be very intelligent."

## LinkedIn post
- **Hook (first two lines):** the single surprising fact, bold. No preamble.
- **Body:** 3 short blocks with bold lead-ins (Demand / Risk / What we did), arrows for lists, max 4 items each.
- **Proof:** one line of track record with the benchmark.
- **Principle:** the capital-protection line and the Munger quote.
- **Next:** dated events and what would change our stance.
- **Close:** the transparency line (every position published before the result), "Full deck attached", disclaimer in italics.
- 2–3 hashtags. Attach the deck as a PDF carousel. Target 250–300 words.
