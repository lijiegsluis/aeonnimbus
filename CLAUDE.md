# Aeon Nimbus Research — Website Project

## Overview
Single-file portfolio website for **LiJie Guo / Aeon Nimbus Research**.
File: `D:/AeonNimbus/website_institutional_with tools.html`

---

## Key Architecture
- **Single HTML file** — all CSS, JS, and content in one file
- Pages switch via `sp(id)` — sets `display:block` on `#pg-<id>`, hides others
- CSS variables in `:root` for theming; dark mode via `html.dark` class
- **CRLF line endings** on Windows — always use Python `str.replace()` to edit, NOT the Edit tool

## CONFIG Block (top of `<script>`)
```javascript
const SUBSTACK_URL = ''; // ← fill when Substack is created
const GITHUB_URL   = 'https://github.com/LiJieGuo'; // ← update with real username
```

## How to Edit Safely (Windows CRLF rule)
The Edit tool WILL FAIL on this file due to Windows CRLF line endings.
Always use Python to make changes:
```python
f = open('D:/AeonNimbus/website_institutional_with tools.html', encoding='utf-8')
html = f.read(); f.close()
html = html.replace(OLD_STRING, NEW_STRING, 1)
with open('D:/AeonNimbus/website_institutional_with tools.html', 'w', encoding='utf-8') as f:
    f.write(html)
```

## Page IDs
| Page | ID |
|------|----|
| Home | `pg-home` |
| Research | `pg-research` |
| Track Record | `pg-track` |
| Tools | `pg-tools` |

## Tools Page Structure
- Each tool is a `.tc` card with `.tchd` header and `.tbody` collapsible panel
- Tabs inside panels use `vt('toolname', 'panelid')` to switch
- Quant tools: `#tc-quant` → BS, MC, Bond, Vol tabs
- DCF tool: `#tc-dcf`
- **Excel export**: SheetJS loaded from CDN. Buttons hidden until calculation runs.
  - `exportBSExcel()`, `exportMCExcel()`, `exportBondExcel()`, `exportDCFExcel()`

## Research Post HTML Structure
To add a new post, insert into `.plist` inside `#pg-research`:
```html
<div class="post" data-cat="equity">
  <div><div class="pdt">Mar 18, 2026</div></div>
  <div>
    <span class="pchip ce">Equity Deep Dive</span>
    <div class="ptt">TITLE</div>
    <div class="pex">Summary excerpt...</div>
    <div class="pmeta">
      <span class="read-time">12 min read</span>
      <a href="SUBSTACK_URL" target="_blank" class="prd">Read →</a>
    </div>
  </div>
</div>
```
Category classes: `ce` (equity), `cm` (macro), `cg` (geo), `cb` (central bank)
`data-cat` values: `equity`, `macro`, `geo`, `central-bank`

---

## Deployment Workflow (once GitHub repo exists)

### First-time setup
```bash
cd D:/AeonNimbus
git init
git remote add origin https://github.com/LiJieGuo/aeon-nimbus-website.git
git add .
git commit -m "Initial deploy"
git push -u origin main
# Then connect repo to Vercel at vercel.com — auto-deploys on every push
```

### After any change
```bash
cd D:/AeonNimbus
git add "website_institutional_with tools.html"
git commit -m "Update: <description>"
git push
# Vercel deploys automatically in ~30 seconds
```

### Can Claude Code still edit after the site is live?
**YES — completely.** This Claude Code instance always edits the local file at
`D:/AeonNimbus/website_institutional_with tools.html`.
After editing, run the git commands above to push → Vercel auto-deploys.
The live site updates in under 60 seconds.

---

## Sync from Substack / LinkedIn Agents
The two automation agents (`aeon-substack-agent`, `aeon-linkedin-agent`) sync back
to this repo via `website_sync/sync.py` in the substack agent.
That script:
1. Reads the new published post data
2. Inserts a new `.post` entry into `#pg-research` in this HTML file
3. Commits + pushes to GitHub → Vercel redeploys

---

## Branding
- **Name**: LiJie Guo · Aeon Nimbus Research
- **Tagline**: Spanish-born, Chinese. Global markets & technology. Investing since 18.
- **MSc**: emlyon (Finance/PGE) + Politecnico di Milano (Quant Finance & Fintech) + Bayes Business School (Finance)
- **Colors**: Gold `#8B6914`, Dark ink `#1A1814`, Paper `#F5F2EC`
- **Font**: `'EB Garamond'` (serif) + monospace system stack
- **LinkedIn**: https://www.linkedin.com/in/lijieguo-es/
- **Substack**: TBD — update `SUBSTACK_URL` in CONFIG when created
- **GitHub**: https://github.com/LiJieGuo — update `GITHUB_URL` in CONFIG
