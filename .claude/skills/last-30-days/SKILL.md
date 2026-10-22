---
name: last-30-days
description: Research what people said about a topic in the last 30 days across Reddit, X, YouTube and TikTok and report the consensus, disagreements, and notable posts. Use for sentiment, trends, "what is the chatter on X", pre-research for a market note.
---

# Last 30 Days

## Procedure
1. Fix the topic and the window (today minus 30 days). Generate 4-6 query variants (name, ticker/aliases, common complaints, "vs" comparisons).
2. Search each source with whatever tools are available (WebSearch/WebFetch with `site:reddit.com`, `site:x.com`, `site:youtube.com`, `site:tiktok.com`, or the Hermes web/social tools). Record URL, date, author handle, and engagement for each item. Drop anything outside the window.
3. Cluster into themes. For each: sentiment, representative quotes (short, attributed), and volume.
4. Report:
   - **Consensus** (what most agree on)
   - **Disagreements** (strongest opposing views)
   - **Rising / fading** (vs earlier in the window)
   - **Notable posts** (with links and dates)
   - **Confidence & gaps** (which sources were unreachable, sample size)

## Rules
- Distinguish verified facts from claims; social posts are evidence of opinion, not of truth.
- Never invent posts or numbers. If a platform blocks access, say so and report what you could reach.
- No personal data beyond public handles; no targeting of private individuals.
