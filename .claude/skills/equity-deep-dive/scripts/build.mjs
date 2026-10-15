#!/usr/bin/env node
// Aeon Nimbus · deep-dive builder
// Inlines doc-page.css/js into a source page, renders it in Chromium, checks every page
// for overflow / sub-12pt text, and prints an A4 PDF.
//
//   node build.mjs <source.html> <out-dir> <basename> [--png <dir>] [--allow-overflow]
//
// Writes <out-dir>/<basename>.html (self-contained) and <out-dir>/<basename>.pdf.
// Exit code 2 when a page overflows (unless --allow-overflow).

import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { dirname, resolve, join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createRequire } from "node:module";

const here = dirname(fileURLToPath(import.meta.url));
const assets = resolve(here, "../assets");
const args = process.argv.slice(2);
const flag = (n) => args.includes(n);
const opt = (n) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : null; };
const pos = args.filter((a, i) => !a.startsWith("--") && !(i > 0 && args[i - 1] === "--png"));
const [src, outDir, base] = pos;
if (!src || !outDir || !base) {
  console.error("usage: node build.mjs <source.html> <out-dir> <basename> [--png <dir>] [--allow-overflow]");
  process.exit(1);
}

// ---- load playwright from wherever it is installed
function loadPlaywright() {
  const req = createRequire(import.meta.url);
  const tries = ["playwright", "playwright-core", "@playwright/test"];
  const roots = [process.cwd(), here, ...(process.env.NODE_PATH || "").split(":").filter(Boolean)];
  for (const name of tries) {
    for (const root of roots) {
      try { return req(req.resolve(name, { paths: [root] })); } catch {}
    }
  }
  console.error("Playwright not found. Install it with:  npm i -D playwright  (then: npx playwright install chromium)");
  process.exit(1);
}
const { chromium } = loadPlaywright();

// ---- inline assets
let html = readFileSync(src, "utf8");
const css = readFileSync(join(assets, "doc-page.css"), "utf8");
const js = readFileSync(join(assets, "doc-page.js"), "utf8");
const block = `<style>\n${css}\n</style>\n<script>\n${js}\n</script>`;
if (html.includes("<!-- DOC-PAGE -->")) html = html.replace("<!-- DOC-PAGE -->", block);
else html = html.replace("</head>", `${block}\n</head>`);

mkdirSync(outDir, { recursive: true });
const htmlOut = resolve(outDir, `${base}.html`);
const pdfOut = resolve(outDir, `${base}.pdf`);
writeFileSync(htmlOut, html);

// ---- render (bundled Playwright browser first, then explicit paths)
let browser;
try { browser = await chromium.launch(); }
catch (err) {
  const exe = [process.env.CHROMIUM_PATH, "/opt/pw-browsers/chromium"].find((p) => p && existsSync(p));
  if (!exe) throw err;
  browser = await chromium.launch({ executablePath: exe });
}
const page = await browser.newPage({ viewport: { width: 900, height: 1200 } });
page.on("console", (m) => { if (m.type() === "error") console.error("[page]", m.text()); });
await page.goto(pathToFileURL(htmlOut).href, { waitUntil: "networkidle", timeout: 60000 });
await page.emulateMedia({ media: "print" });
await page.waitForFunction(() => window.__docPageReady === true, null, { timeout: 30000 });
const report = await page.evaluate(() => window.__docPageCheck());

const fonts = await page.evaluate(() => ({
  inter: document.fonts.check('800 20px "Inter"'),
  newsreader: document.fonts.check('italic 400 20px "Newsreader"'),
}));

console.log("page  label                          fill  overflow  wide  <12pt");
for (const r of report) {
  console.log(
    String(r.page).padStart(4), " ", (r.label || "").padEnd(30).slice(0, 30),
    String(r.fill + "%").padStart(5), String(r.overflowPx).padStart(8),
    String(r.clippedWidePx).padStart(5), r.textBelow12pt ? "  YES" : "   no",
  );
}
if (!fonts.inter || !fonts.newsreader) console.warn("WARN fonts not loaded:", fonts, "(falls back to local/system fonts)");

const png = opt("--png");
if (png) {
  mkdirSync(png, { recursive: true });
  const n = await page.locator(".page").count();
  for (let i = 0; i < n; i++) {
    await page.locator(".page").nth(i).screenshot({ path: join(png, `page-${String(i + 1).padStart(2, "0")}.png`) });
  }
  console.log(`PNG previews: ${png}`);
}

await page.pdf({ path: pdfOut, preferCSSPageSize: true, printBackground: true });
await browser.close();
console.log(`HTML: ${htmlOut}\nPDF:  ${pdfOut}`);

const overflow = report.filter((r) => r.overflowPx > 1);
const small = report.filter((r) => r.textBelow12pt);
const thin = report.filter((r) => r.fill < 65);
if (thin.length) console.warn(`WARN under-filled pages (<65%): ${thin.map((r) => r.page).join(", ")}`);
if (small.length) console.warn(`WARN text below 12pt on pages: ${small.map((r) => r.page).join(", ")}`);
if (overflow.length && !flag("--allow-overflow")) {
  console.error(`FAIL overflow on pages: ${overflow.map((r) => `${r.page} (+${r.overflowPx}px)`).join(", ")}`);
  process.exit(2);
}
