/* Aeon Nimbus · doc-page.js
   - Fills running header/footer from <body data-*> and each page's data-section / data-sources.
   - Builds range bars and div bar charts from data attributes.
   - Checks every page for overflow and under-fill; result in window.__docPageReport.

   <body data-company="Fabrinet" data-ticker="FN" data-direction="Long"
         data-entry="405.33" data-target="580" data-currency="$">
   <section class="page" data-screen-label="02 Thesis" data-section="Thesis"
            data-sources="10-K FY26; Q4 FY26 call; Aeon Nimbus estimates">
     <div class="page-body">...</div>
   </section>
*/
(function () {
  const fmt = (v, cur) => {
    const n = Number(v);
    if (!isFinite(n)) return String(v);
    return (cur || "") + n.toLocaleString("en-US", { minimumFractionDigits: n % 1 ? 2 : 0, maximumFractionDigits: 2 });
  };

  function frame() {
    const b = document.body.dataset;
    const cur = b.currency || "$";
    const pages = [...document.querySelectorAll(".page")];
    const right = b.headerRight ||
      `${b.direction || "Long"} ${b.ticker || ""} · ${fmt(b.entry, cur)} → ${fmt(b.target, cur)}`;
    pages.forEach((pg, i) => {
      if (!pg.querySelector(":scope > .run-head") && !pg.hasAttribute("data-no-head")) {
        const h = document.createElement("header");
        h.className = "run-head";
        h.innerHTML = `<span class="rh-l">Aeon Nimbus Research · ${b.company || ""} · ${pg.dataset.section || ""}</span><span class="rh-r">${right}</span>`;
        pg.prepend(h);
      }
      if (!pg.querySelector(":scope > .run-foot")) {
        const f = document.createElement("footer");
        f.className = "run-foot";
        const src = pg.dataset.sources ? `Sources: ${pg.dataset.sources}` : "";
        f.innerHTML = `<span class="src">${src}</span><span class="pg">${i + 1} / ${pages.length}</span>`;
        pg.append(f);
      }
    });
  }

  function rangebars() {
    const cur = document.body.dataset.currency || "$";
    document.querySelectorAll(".rangebar").forEach((el) => {
      const d = el.dataset;
      const stop = +d.stop, target = +d.target, entry = +d.entry;
      const mark = d.mark !== undefined ? +d.mark : null;
      const lo = Math.min(stop, mark ?? stop), hi = Math.max(target, mark ?? target);
      const pct = (v) => ((v - lo) / (hi - lo)) * 100;
      const e = pct(entry);
      el.style.setProperty("--e", e + "%");
      let html = `<div class="track"></div>`;
      html += `<div class="tick" style="left:${e}%"></div>`;
      html += `<div class="lbl top l0" style="left:${pct(stop)}%">Stop ${fmt(stop, cur)}</div>`;
      html += `<div class="lbl top l1" style="left:${pct(target)}%">Target ${fmt(target, cur)}</div>`;
      html += `<div class="lbl bot" style="left:${e}%">Entry ${fmt(entry, cur)}</div>`;
      if (mark !== null) {
        html += `<div class="dot" style="left:${pct(mark)}%"></div>`;
        if (Math.abs(pct(mark) - e) > 18)
          html += `<div class="lbl bot" style="left:${pct(mark)}%">${d.markLabel || "Last"} ${fmt(mark, cur)}</div>`;
        else
          html += `<div class="lbl top" style="left:${pct(mark)}%;top:15.5mm;font-weight:700">${d.markLabel || "Last"} ${fmt(mark, cur)}</div>`;
      }
      el.innerHTML = html;
    });
  }

  function bars() {
    document.querySelectorAll(".hbars").forEach((g) => {
      const items = [...g.querySelectorAll(".hbar")];
      const max = +g.dataset.max || Math.max(...items.map((i) => Math.abs(+i.dataset.value)));
      items.forEach((i) => {
        const w = (Math.abs(+i.dataset.value) / max) * 100;
        i.innerHTML = `<span class="bl">${i.dataset.label || ""}</span><span class="bt"><span class="bf" style="width:${w}%"></span></span><span class="bv">${i.dataset.display ?? i.dataset.value}</span>`;
      });
    });
    document.querySelectorAll(".vbars").forEach((g) => {
      const items = [...g.querySelectorAll(".vbar")];
      const max = +g.dataset.max || Math.max(...items.map((i) => Math.abs(+i.dataset.value)));
      items.forEach((i) => {
        const h = (Math.abs(+i.dataset.value) / max) * 100;
        i.innerHTML = `<span class="vv">${i.dataset.display ?? i.dataset.value}</span><span class="vf" style="height:calc(${h}% - 6mm)"></span><span class="vl">${i.dataset.label || ""}</span>`;
      });
    });
  }

  function check() {
    const report = [];
    document.querySelectorAll(".page").forEach((pg, i) => {
      pg.removeAttribute("data-overflow");
      const body = pg.querySelector(".page-body");
      if (!body) return;
      const over = body.scrollHeight - body.clientHeight;
      // fill = space the content actually needs (children + gaps), not where spread pushes it
      const kids = [...body.children];
      const gap = parseFloat(getComputedStyle(body).rowGap) || 0;
      const need = kids.reduce((a, c) => a + c.getBoundingClientRect().height, 0) + gap * Math.max(0, kids.length - 1);
      const fill = need / body.clientHeight;
      let wide = 0;
      body.querySelectorAll("*").forEach((c) => {
        const d = c.scrollWidth - c.clientWidth;
        if (d > 2 && getComputedStyle(c).overflowX !== "visible") wide = Math.max(wide, d);
      });
      const small = [...body.querySelectorAll("*")].some((c) => {
        if (!c.childNodes.length || ![...c.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) return false;
        return parseFloat(getComputedStyle(c).fontSize) < 15.9; // 12pt = 16px
      });
      const entry = {
        page: i + 1,
        label: pg.dataset.screenLabel || "",
        overflowPx: Math.max(0, Math.round(over)),
        fill: Math.round(Math.min(fill, 1) * 100),
        clippedWidePx: Math.round(wide),
        textBelow12pt: small,
      };
      if (entry.overflowPx > 1) pg.setAttribute("data-overflow", entry.overflowPx);
      report.push(entry);
    });
    window.__docPageReport = report;
    const bad = report.filter((r) => r.overflowPx > 1 || r.textBelow12pt || r.clippedWidePx);
    if (bad.length) console.warn("doc-page issues", bad);
    return report;
  }

  function run() {
    frame();
    rangebars();
    bars();
    window.__docPageCheck = check;
    const done = () => { check(); window.__docPageReady = true; };
    (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(() => setTimeout(done, 50));
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();
})();
