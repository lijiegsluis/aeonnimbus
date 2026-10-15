# Aeon Nimbus · Claude Code notes

- Website: single-file `index.html` (see `AEONNIMBUS.md`). Reports live in `reports/` (`<ticker>-report.pdf`, `<ticker>-dashboard.html`, `<ticker>-deep-dive.pdf`).
- **Ticker → equity research PDF:** when the user sends a ticker on its own (e.g. `NVDA`, `$IREN`, `deep dive MELI`, `MRVL es`), run the `equity-deep-dive` skill (`.claude/skills/equity-deep-dive/SKILL.md`) end to end: live research → valuation (`scripts/valuation.py`) → research note under the master prompt → 12-page Claude Design deep dive → `reports/<ticker>-deep-dive.pdf`. A `UserPromptSubmit` hook (`.claude/hooks/ticker-trigger.py`) flags these messages.
- Research working files go to `research/<TICKER>/<YYYY-MM-DD>/`. The position ledger is `research/positions.json`.
- Do not edit `index.html`, `research-feed.json` or `market-data.json` as part of a deep dive unless asked; the last two are refreshed by GitHub Actions.
