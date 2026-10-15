# ORCL: Full Technical Read

**Aeon Nimbus Research** · NYSE: ORCL · Oracle Corporation · Daily chart, as of Jul 27, 2026

**Price: \$119.61** (+4.6% on the day)

| Off ATH | vs 200-SMA | vs 50-SMA | RSI (14) | MACD hist | 20d avg vol |
|---|---|---|---|---|---|
| −65.4% | −35.9% | −29.7% | 32.4 | +0.32 | 39.2M |

Moving averages: 50-day SMA \$170.14 · 200-day SMA \$186.58. All-time high \$345.72 (Sep 2025); 52-week low \$114.75 (Jul 24, 2026). Volume peak 131.6M on the Sep 2025 gap.

## The full probability tree, by time horizon

Everything below is built from the same bootstrap Monte Carlo (ORCL's own trailing-90-day returns, 20,000–50,000 trials per estimate) plus a discretionary overlay for known catalysts and news. Where the two differ, both are shown — raw stat is the model alone; adjusted folds in that there's no scheduled Oracle-negative catalyst until Sep 14, that Wed/Thu's Big Tech earnings are a two-sided volatility event, and that Monday's bounce has a real fundamental driver. Ranges reflect two model variants (drift-persisting vs. zero-drift), not error bars.

### ① This week (Tue–Fri, 4 sessions left)

| Outcome                                              | Raw stat | Adjusted       |
|------------------------------------------------------|----------|----------------|
| Touches ≥ \$128 at any point                         | 30–33%   | 40–48%         |
| Friday *closes* ≥ \$128                              | 16–18%   | 20–28%         |
| Weekly candle green (Fri close \> Mon open \$118)    | 50–54%   | ≈ same         |
| Up week-over-week (Fri close \> last Fri's \$114.99) | 63–67%   | ≈ same         |
| Retests/breaks \$114.75 intraday this week           | 61–66%\* | slightly lower |

\*Implied from the 5-session floor-hold figure below. Wed (MSFT/META) and Thu (AAPL/AMZN) earnings widen both tails — they don't pick a direction on their own.

### ② Which comes first — next 3 weeks (15 sessions)

| Path                                                            | Raw stat | Adjusted |
|-----------------------------------------------------------------|----------|----------|
|  Drops to/through \$114.75 **first**, never having tagged \$128 | 63–68%   | 45–55%   |
|  Tags \$128 first, then later reverses through \$114.75         | ~15%     | 25–30%   |
|  Tags \$128 first and it holds, no retest of \$114.75           | 17–22%   | ≈ same   |
| Chops between the two, touching neither                         | ~0%      | ~0%      |

### ③ Floor-hold: \$114.75 never breaks on a closing basis

| By                                     | P(holds) |
|----------------------------------------|----------|
| 1 week                                 | 46–51%   |
| 2 weeks                                | 31–36%   |
| 3 weeks                                | 24–30%   |
| ~1 month                               | 20–25%   |
| Through Sep 14 earnings (~33 sessions) | 14–20%   |

### ④ Into and through Sep 14 earnings — fundamentals-weighted scenarios

**Downtrend continuation — new low made: 48%**

**Relief bounce inside the downtrend, ultimately sold into: 34%**

**Durable reversal — 200-SMA reclaim, credit story stabilizes: 18%**

### ⑤ Long horizon (6–9 months) — qualitative, not statistical

| Outcome                                                                                                    | Estimate |
|------------------------------------------------------------------------------------------------------------|----------|
| Recovers into the \$200–250 zone (38.2–61.8% fib) if Sep 14 goes well                                      | 20–30%   |
| New all-time high (\>\$345.72)                                                                             | 5–10%    |
| Full compound path: bounces to \$128 → fades → \$114.75 holds all summer → grinds to new ATH within months | 1–2%     |

That last row is the reminder worth keeping: each individual step is plausible on its own, but multiplying several sub-50% events together compounds fast. Building a specific multi-step narrative and pricing it like a single coin-flip is the mistake to avoid here.

## Fully bearish moving-average stack — a death cross already in place

20-day (\$132.96) sits below the 50-day (\$170.14), which sits below the 200-day (\$186.58). That ordering — short below medium below long — is the textbook signature of an established downtrend, not a pullback inside an uptrend. The 50/200 death cross happened weeks ago as the average of the last 50 sessions was dragged down through the 200-day by the June-July collapse; there's been no attempt to reclaim it since. Price is **29.7% below the 50-day** and **35.9% below the 200-day** — both stretched well past the point where a "normal" pullback usually resolves, which cuts both ways: it raises the odds of a mean-reversion bounce, but it's also exactly what persistent, trending selling looks like.

## Oversold, with a very early stabilization tell in MACD

| Indicator               |                                          | Reading    | Signal                      |
|-------------------------|------------------------------------------|------------|-----------------------------|
| RSI (14, Wilder)        |                                          | 32.4       | Oversold zone               |
| MACD (12,26,9)          | line −13.99 / signal −14.31              | hist +0.32 | Momentum flattening         |
| Bollinger (20, 2σ)      | lower 112.88 / mid 132.96 / upper 153.05 | 17th pct.  | Walking the lower band      |
| Volume (20d vs 60d avg) | 39.2M vs 30.3M                           | +30%       | Distribution, not drying up |

The MACD histogram ticked from +0.02 to +0.32 over the last two sessions — momentum is decelerating, not accelerating, to the downside. That's worth flagging, but it's two data points against months of trend; it is not yet a crossover or a confirmed bottoming signal. Price has been riding the lower Bollinger Band for over a week rather than spiking through it and snapping back, which is the more bearish of the two patterns — a "walk down the band" reflects sustained selling pressure, not a single capitulation flush.

## ADX confirms this is a strong trend, not a chop — that matters for how much to trust "oversold"

| Signal                    |                                 | Reading                      | Read                          |
|---------------------------|---------------------------------|------------------------------|-------------------------------|
| ADX (14)                  | +DI 11.4 / −DI 35.7             | 41.2                         | Strong trend (\>40)           |
| Stochastic (14,3,3)       | %K / %D                         | 5.6 / 9.5                    | Deeply oversold               |
| OBV (on-balance volume)   | now vs. 20d ago vs. Jun high    | −882M / −524M / −188M        | Confirms distribution         |
| Ichimoku                  | Tenkan 124.3 / Kijun 151.4      | below cloud                  | Bearish TK, price under cloud |
| 60-day regression channel | slope −\$1.44/day, fit \$130.18 | −0.46σ                       | On-trend, not stretched       |
| Volume Profile (180d)     | POC / value area                | \$144.00 / \$138.84–\$200.78 | Magnet zone \$138–153         |

Two things worth separating. First, **ADX at 41** with −DI more than 3x +DI says this downtrend has real directional conviction by trend-strength standards — strong trends can and do keep oversold oscillators pinned for extended stretches, so RSI/Stochastic being deep in oversold territory is a reason to *watch* for a bounce, not to assume one is imminent. Second, there's a faint **momentum divergence** building underneath the last three closing lows: RSI printed 26.9 at \$131.54, 27.1 at \$121.38, and 27.4 at \$114.75 — each new price low came with RSI essentially flat-to-marginally-higher instead of making a fresh extreme. That's the early shape of bullish divergence, but it's small (half a point at a time) and unconfirmed — not something to lean on by itself.

Two independent methods land on the same overhead zone: the **Ichimoku cloud that will exist 26 sessions from now has its lower edge at \$137.85**, and the **180-day Volume Profile's point-of-control is \$144.00** with a value area floor at \$138.84. \$138–144 is a genuine confluence — the first real structural ceiling above current price, well before the \$169–170 Fibonacci/50-SMA level called out below.

## Fibonacci retracement, high (\$345.72) to low (\$114.75)

100% — **\$345.72** Sep '25 ATH

78.6% — **\$296.29**

61.8% — **\$257.49**

50.0% — **\$230.24** psychological half-back

38.2% — **\$202.98** ≈ near 200-SMA

23.6% — **\$169.26** ≈ confluent w/ 50-SMA \$170

0% — **\$114.75** Jul '26 low

The single most important confluence on this chart: **\$169–170** is simultaneously the 23.6% Fibonacci retracement and the declining 50-day SMA. That's the first level any real bounce needs to clear — and the level bears would want to see hold as resistance. \$203 (38.2% fib) roughly lines up with the 200-day SMA; a close above that would meaningfully change the technical picture. Below current price, \$114.75 is the only reference low — a break there has no chart-based support until round-number levels near \$100.

## This is a fundamentals-driven crash, not a technical air-pocket

### Pressuring the stock

**S&P cut Oracle to BBB−** (Jul 13) on AI-infrastructure debt — one notch above junk. S&P / Benzinga

**FY26 capex hit \$55.7B** vs. \$50B guided; free cash flow swung to **−\$23.7B**; total debt reached \$156.2B, up from ~\$87B a year earlier — disclosed at the Jun 10 print, triggering the worst weekly decline since 2001 (−19%). CNBC

Plans to raise **~\$40B in FY27** via debt and equity, including a **\$20B share sale** — real dilution risk on top of the leverage. CNBC

Wisconsin regulators upheld collateral rules that could force **\>\$7B posted collateral** for an AI data center, adding \>\$100M/yr in financing cost; New Mexico separately rejected a gas-pipeline permit for another Oracle site. 247wallst

5-yr CDS trading near multi-year highs — it's become the market's go-to proxy for AI-capex financing stress, and IBM's post-earnings −25% added sector contagion. CNBC / 247wallst

CLSA opened coverage at **Hold, \$145 PT**; Melius cut to **Hold, \$160 PT**, questioning the multiple given no positive free cash flow expected until "the 2030s." 247wallst / TipRanks

Michael Burry publicly flagged the Nvidia–OpenAI financing as **circular** — Nvidia guaranteeing the spending that flows back to Nvidia for chips — the same "AI capex funded by leverage, not cash flow" critique already reflected in Oracle's own BBB− downgrade. X / 24/7 Wall St.

**Iran conflict / Strait of Hormuz:** strikes paused again Jul 27 (Brent −6.7%, WTI −6.1% same day) — but Iran's Foreign Ministry denies active negotiations, contradicting the US framing; Trump declared the ceasefire "over" as recently as Jul 8 and reinstated shipping-blockade rhetoric around Jul 23, which spiked oil and dropped stocks that day (S&P −1.2%, Nasdaq −2.2%). This is a disputed, reversible pause, not a resolution. CNBC / CNN / Washington Post

Broader Trump-news backdrop has been a net headwind this month, not a tailwind: AAII bullish sentiment fell to 29.6% (from 44.9% the week before) — lowest since last September — and new tariffs (Canada, effective Aug 19; a Section 301 forced-labor tariff on 80+ countries) add inflation and margin risk. The Fed explicitly cited tariffs, energy costs, and AI-infrastructure spending together as inflation drivers this spring — a combination that raises the cost of exactly the debt Oracle needs to refinance and the \$40B FY27 raise it's planning. CNBC / U.S. Bank / Fed commentary

### Supporting the stock

**Nvidia reportedly in talks to backstop ~\$250B** of financing for OpenAI's 10-gigawatt Ohio data-center project (WSJ, Sun Jul 26 night), plus discussions on up to \$350B more for chip purchases. This is **today's actual catalyst**: ORCL jumped as much as +4.95% Monday morning because OpenAI is Oracle's largest new customer — de-risking OpenAI's ability to fund and perform on its existing \$300B Oracle cloud commitment. Yahoo Finance / Bloomberg / WSJ

**\$638B remaining performance obligations** — a multi-year revenue backlog that's the fundamental counterweight to the debt story. CNBC

10-year, **~\$7B** enterprise deal with the U.S. Department of War, plus a 5-year Navy IDIQ worth **\$3.3–7.0B**. 247wallst

Reportedly the frontrunner for Japan's air-gapped government cloud, ahead of AWS/Azure/Google Cloud. 247wallst

Mizuho reiterated **Outperform, \$320 PT** (~164% upside from here); DA Davidson upgraded to **Buy, \$180**; Barclays trimmed to **\$202** but kept **Overweight**. TheStreet / Nasdaq / TipRanks

Consensus across 35 analysts is still nominally **Buy**, average target revised **+3%** over the past 3 months — though target dispersion (\$145–\$320) shows the Street is genuinely split. public.com

\$300B, 5-year OpenAI cloud commitment (announced 2025, capacity online 2027) remains intact and underpins the infrastructure buildout thesis. MLQ

## What got it here, and what's next

- **Sep '25:** Q1 FY26 print: cloud backlog blowout, RPO surges — stock gaps +36% in a day to an all-time high of \$345.72.

- **Jun 10 '26:** Q4/FY26 results: revenue record, but capex of \$55.7B blows through guidance and FCF goes deeply negative.

- **Jun 26 '26:** Worst week since the 2001 dot-com bust, −19%, as investors digest the debt load.

- **Jul 13 '26:** S&P downgrades credit rating to BBB− on AI-infrastructure leverage.

- **Jul 24 '26:** Stock prints a fresh low of \$114.75 (close \$114.99) into month-end, capping a ~65% drawdown from the ATH.

- **Jul 26–27 '26:** WSJ reports Nvidia in talks to backstop ~\$250B of OpenAI's data-center buildout. ORCL gaps up and rallies as much as +4.95% Monday — this report captures that bounce, at \$119.61.

- **Jul 28 '26:** Oracle AI Data Platform product roadmap webinar (vector search, hardware scalability) — developer/customer audience, not an IR event. Same series ran in April '26 with no notable price reaction. Watch mainly for whether "hardware scalability constraints" language gets picked up as a standalone headline.

- **Jul 29 '26:** **Microsoft & Meta earnings** (after close) — not Oracle, but the same AI-capex-sustainability debate. Azure growth and capex commentary are a direct sentiment read-through for ORCL. The dominant risk event of the week.

- **Jul 30 '26:** **Apple & Amazon earnings** (after close) — AWS growth/capex commentary is the other half of the sector read-through. Two-sided: reassuring prints support the bounce case, capex-fatigue signals reinforce the credit overhang. Oracle's Fusion Data Intelligence roadmap webinar (localized-LLM data integration) also runs this day — product-audience event, low direct market impact.

- **Sep 14 '26:** **Next earnings (FY27 Q1)** — the next Oracle-specific catalyst. Watch capex trajectory vs. the \$40B FY27 raise, FCF path, and whether the credit narrative stabilizes or deteriorates further.

## Next 4–8 weeks, into the September print

**Downtrend continuation: 48%**

MA stack stays bearish, bounces keep getting sold, and price breaks the \$114.75 low toward \$100 — or lower — if the September print shows capex still outrunning guidance, FCF still negative, or another credit action. Base case given the trend, the stacked MAs, and volume still expanding on down days.

*Target zone: \$95–110*

**Relief bounce within the downtrend: 34%**

Today's bounce isn't generic technical noise — it's specifically the Nvidia/OpenAI financing report de-risking Oracle's largest customer, on top of an RSI of 32 and a flattening MACD histogram that already argued for a snap-back. This name also has precedent for violent counter-trend rallies — it ran from a ~\$136 low in March to \$248 in June before fully round-tripping. A move toward the \$150 mid-Bollinger area, and possibly the \$169–170 confluence zone, is plausible without the primary trend actually changing — especially if the fragile Iran de-escalation holds and keeps risk appetite supportive.

*Target zone: \$150–170, likely sold into*

**Durable reversal: 18%**

Requires the credit narrative to actually stabilize — no further downgrade, a clean FY27 raise, visible RPO-to-revenue conversion — reclaiming the 200-day SMA (~\$187) and holding it. This is the setup Mizuho's \$320 target implies, but it needs the September earnings print to go right and a multi-month base to repair the moving-average structure. Lowest-probability outcome on this time horizon.

*Target zone: \$187 reclaim → \$230 (50% fib) on follow-through*

## Next 20 trading days (~1 month), simulated

Bootstrapped 20,000 times off ORCL's own trailing 90-day daily returns and intraday high-extension ratios (not a Gaussian assumption — this carries forward the real fat tails this stock has actually printed). Two variants: one lets the current negative drift persist, one demeans it and carries forward only the elevated volatility. The shaded bands below are the zero-drift (no persistent bias) version; the dashed line is where the median path sits if the recent downward momentum continues.

| Level                                | Touch prob. (zero-drift) | Touch prob. (drift-persisting) |
|--------------------------------------|--------------------------|--------------------------------|
| ≥ \$128                              | 64.7%                    | 57.2%                          |
| ≥ \$138 (Ichimoku/volume confluence) | 36.9%                    | 29.9%                          |
| ≥ \$144 (volume POC)                 | 25.6%                    | 19.9%                          |
| ≥ \$169.26 (major fib/50-SMA)        | 4.3%                     | 2.7%                           |
| ≤ \$114.75 (revisit the low)         | 74.5%                    | 80.7%                          |
| ≤ \$100                              | 27.8%                    | 36.0%                          |

The single most useful number in this table isn't upside — it's that **both scenarios put the odds of retesting \$114.75 sometime in the next month at 75–81%**. At this realized volatility (~4%/day), the "low is in" narrative doesn't hold much statistical water yet; round-tripping back toward the recent low is closer to the base case than the exception. \$169–170 staying out of reach for a month (95–97% odds) is consistent with everything else in this report: that level is a multi-week objective, not a near-term one.

### Sequencing: which happens first?

Endpoints don't tell you the route, so this reruns the same bootstrap as a race between two barriers — \$128 up vs. \$114.75 down — tracking whichever gets touched first over the next 15 sessions (~3 weeks):

| Path                                                                  | Probability |
|-----------------------------------------------------------------------|-------------|
|  Drops to/through \$114.75 **first**, before ever tagging \$128       | 63–68%      |
|  Tags \$128 first, then later reverses back through \$114.75          | ~15%        |
|  Tags \$128 first and it holds — no retest of \$114.75 within 3 weeks | 17–22%      |
| Chops between the two, touching neither                               | ~0%         |

Timing: in the simulations that do touch \$128, the **median time-to-touch is ~4 sessions out (around Friday)**, not this Tue–Thu. In the simulations that touch \$114.75, the median time is ~2 sessions (Wednesday) — it's simply closer (−4.1% away vs. +7.0% for \$128), so at ~4%/day volatility the nearer barrier tends to get tagged first, and faster. Only ~23–26% of paths reach \$128 specifically within Tue–Thu *as the first thing that happens*. The base case this simulation actually favors is closer to "chop or dip toward \$114.75 within the next couple of sessions," not "grind up to \$128 by Thursday and then roll over."

### Does \$114.75 hold as the floor?

Getting wicked and getting broken are different questions. "Touch" (above) counts any intraday low that dips to \$114.75. "Floor holds" means the *close* never goes below it — a brief undercut that closes back above is a failed breakdown, not a broken floor.

| By                     | P(close breaks floor) | P(floor holds, closing basis) |
|------------------------|-----------------------|-------------------------------|
| 1 week (5 sessions)    | 50–54%                | 46–51%                        |
| 2 weeks (10 sessions)  | 64–69%                | 31–36%                        |
| 3 weeks (15 sessions)  | 71–76%                | 24–30%                        |
| ~1 month (20 sessions) | 75–80%                | 20–25%                        |

Purely by the numbers, this floor is closer to a coin-flip over the next week and a clear underdog by a month out — which is a colder read than "it held once, so it's support." One thing the model can't price in: the shape of the last two sessions is itself a recognizable pattern — Thursday closed almost exactly at the session low (\$114.99 vs. a \$114.75 low), and Monday reversed hard on real news. That "test-and-reverse" candle sequence is the kind of thing technicians read as a tentative failed-breakdown / bear-trap signal, which argues the near-term (1-week) odds are probably a bit better than the raw 46–51% — but there's no fresh catalyst behind that read the way there was behind Monday's bounce, so don't overweight it. Net: call it roughly a coin-flip for the floor holding through this week, worse than even odds by two weeks, and a genuine minority outcome (1-in-4 to 1-in-5) by the time September 14 earnings actually arrives.

## Bottom line

Every trend and momentum measure here — the MA stack, the death cross, ADX at 41 with −DI dominant, the Bollinger walk, 65% off the high — describes a stock in a real, fundamentals-driven downtrend with genuine directional conviction, not a stretched pullback in a healthy uptrend. Today's bounce has a real, identifiable cause (the Nvidia/OpenAI financing report reducing counterparty risk on Oracle's biggest contract) and lines up with oversold technicals and a faint, unconfirmed RSI divergence, so it's a more credible relief rally than a random up day — but nothing here has flipped bullish yet: no moving-average reclaim, no MACD crossover, price still under the Ichimoku cloud, and the same debt-fueled-capex critique that hit Oracle's own credit rating (echoed today in Burry's "circular financing" comment on the Nvidia deal) is still fully intact. The simulation above agrees: the most probable next move is chop between roughly \$105–130 with a real chance (75–81%) of retesting \$114.75 before a good chance (95%+) of seeing \$169. Treat this as "watch for a tradeable bounce toward \$138–170," not "trend has turned." The next real verdict arrives September 14 — and if you're tracking a specific pair of Oracle events before month-end, tell me what they are; I could only confirm generic community webinars and the Nvidia/OpenAI report for this week, not two distinct Oracle corporate events.

Data: TradingView (BATS/Cboe One feed), 250 daily bars through Jul 27, 2026. Indicators computed directly from OHLCV (SMA/EMA/RSI-Wilder/MACD/Bollinger/ATR/Stochastic/ADX/OBV/Ichimoku/linear regression/volume profile); TradingView's own indicator overlay was unavailable at capture time. The 20-day probability map is a bootstrap Monte Carlo (20,000 trials/scenario) drawn from ORCL's own trailing 90-day return distribution, not a Gaussian model — it reflects this stock's actual recent fat tails, not a textbook assumption. Scenario probabilities and the fan chart are a statistical/technical synthesis for informational purposes only — not investment advice, not a guarantee, and not personalized to any portfolio. Past volatility does not guarantee future volatility.
