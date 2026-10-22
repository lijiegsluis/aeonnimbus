---
name: anatomy
description: Explain a technical concept by building a small interactive simulation instead of writing prose. Use when asked "how does X work", for pricing models, algorithms, protocols, or any mechanism with parameters worth playing with.
---

# Anatomy

Explain by building a machine the user can operate.

## Procedure
1. **Pick the mechanism**: the 1-3 variables that actually drive behavior (e.g. for Black-Scholes: spot, vol, time).
2. **Build one self-contained HTML file** (no build step, vanilla JS, inline CSS, canvas or SVG). Sliders/toggles for each variable; the output (chart, state diagram, numbers) updates live.
3. **Show the real mechanism**, not decoration: label the parts, show intermediate values, let the user break it (extreme inputs) and see why.
4. **Add a "what to try" panel** with 3 guided experiments and what each reveals.
5. **Verify** the math against a known case before delivering; state the case in a comment.
6. Save to `intelligence/anatomies/<topic>.html` (or publish as an Artifact when available). Reply with the path and a 2-sentence summary, not an essay.

## Rules
- Text explanation is a caption, not the product.
- Defaults must start in an interesting, non-degenerate state.
- Keep the file under ~300 lines; one concept per machine.
