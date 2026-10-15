#!/usr/bin/env python3
"""Aeon Nimbus valuation engine for equity deep dives.

Reads an inputs JSON (see ../assets/valuation-inputs.example.json) and writes:
  <out>.json  every computed number, for the HTML pages
  <out>.md    the same as markdown tables, for the research note

  python3 valuation.py inputs.json research/FN/valuation

Implements the master-prompt rules: WACC built from scratch (Rf + beta x ERP + CRP + size),
UFCF DCF with Gordon and exit-multiple terminal values, WACC x exit-multiple and WACC x g grids,
reverse DCF, the 7-row weighted valuation blend with outlier exclusion, scenario EV,
payoff asymmetry and half-Kelly sizing.
"""
import json
import statistics
import sys
from copy import deepcopy


def wacc_build(w):
    ke = w["rf"] + w["beta"] * w.get("erp", 0.055) + w.get("crp", 0.0) + w.get("size_premium", 0.0)
    e, d = w["equity_value"], w.get("debt_value", 0.0)
    v = e + d
    kd_after = w.get("kd", 0.0) * (1 - w.get("tax", 0.21))
    wacc = ke * e / v + kd_after * d / v
    return {"rf": w["rf"], "beta": w["beta"], "erp": w.get("erp", 0.055), "crp": w.get("crp", 0.0),
            "size_premium": w.get("size_premium", 0.0), "ke": ke, "kd_pre": w.get("kd", 0.0),
            "kd_after": kd_after, "e_weight": e / v, "d_weight": d / v, "wacc": wacc}


def project(d):
    """Explicit-period UFCF from revenue growth and margin paths."""
    rev = d["base_revenue"]
    rows = []
    n = len(d["growth"])
    for i in range(n):
        prev = rev
        rev = rev * (1 + d["growth"][i])
        ebit = rev * d["ebit_margin"][i]
        nopat = ebit * (1 - d["tax_rate"])
        da = rev * _at(d["da_pct"], i)
        capex = rev * _at(d["capex_pct"], i)
        dnwc = (rev - prev) * _at(d["nwc_pct_of_incr_rev"], i)
        ufcf = nopat + da - capex - dnwc
        rows.append({"year": d["first_year"] + i, "revenue": rev, "growth": d["growth"][i],
                     "ebit": ebit, "ebit_margin": d["ebit_margin"][i], "nopat": nopat, "da": da,
                     "capex": capex, "dnwc": dnwc, "ufcf": ufcf, "ebitda": ebit + da})
    return rows


def _at(x, i):
    return x[i] if isinstance(x, list) else x


def dcf(d, wacc, g=None, exit_mult=None, mid_year=None):
    if mid_year is None:
        mid_year = d.get("mid_year", False)  # house default: year-end discounting
    rows = project(d)
    pv = 0.0
    for i, r in enumerate(rows):
        t = i + (0.5 if mid_year else 1.0)
        r["df"] = 1 / (1 + wacc) ** t
        r["pv"] = r["ufcf"] * r["df"]
        pv += r["pv"]
    last = rows[-1]
    n = len(rows)
    if exit_mult is not None:
        tv = last["ebitda"] * exit_mult
    else:
        g = d["terminal_growth"] if g is None else g
        if wacc <= g:
            return None
        tv = last["ufcf"] * (1 + g) / (wacc - g)
    pv_tv = tv / (1 + wacc) ** n
    ev = pv + pv_tv
    equity = ev - d["net_debt"]
    return {"rows": rows, "pv_explicit": pv, "tv": tv, "pv_tv": pv_tv, "ev": ev,
            "equity": equity, "per_share": equity / d["diluted_shares"], "tv_share": pv_tv / ev}


def bisect(f, lo, hi, target, it=80):
    flo = f(lo) - target
    for _ in range(it):
        mid = (lo + hi) / 2
        fm = f(mid) - target
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def reverse_dcf(d, wacc, price):
    out = {}
    try:
        out["implied_wacc"] = bisect(lambda w: dcf(d, w)["per_share"], d["terminal_growth"] + 0.005, 0.40, price)
    except Exception:
        out["implied_wacc"] = None

    def margin_scale(k):
        dd = deepcopy(d)
        dd["ebit_margin"] = [m * k for m in d["ebit_margin"]]
        return dcf(dd, wacc)["per_share"]
    k = bisect(margin_scale, 0.05, 6.0, price)
    out["implied_terminal_ebit_margin"] = d["ebit_margin"][-1] * k

    def growth_shift(s):
        dd = deepcopy(d)
        dd["growth"] = [x + s for x in d["growth"]]
        return dcf(dd, wacc)["per_share"]
    s = bisect(growth_shift, -0.5, 1.0, price)
    out["implied_growth_shift"] = s
    dd = deepcopy(d)
    dd["growth"] = [x + s for x in d["growth"]]
    out["implied_final_year_revenue"] = project(dd)[-1]["revenue"]
    out["implied_revenue_cagr"] = (out["implied_final_year_revenue"] / d["base_revenue"]) ** (1 / len(d["growth"])) - 1
    out["implied_terminal_growth"] = None
    try:
        out["implied_terminal_growth"] = bisect(lambda g: dcf(d, wacc, g=g)["per_share"], -0.05, wacc - 0.002, price)
    except Exception:
        pass
    return out


def multiple_value(mult, metric, kind, net_debt, shares):
    if kind == "ev":
        return (mult * metric - net_debt) / shares
    return mult * metric  # P/E: metric is EPS


def blend(inp, dcf_ps):
    b = inp["blend"]
    nd, sh = inp["dcf"]["net_debt"], inp["dcf"]["diluted_shares"]
    peers = inp.get("peers", [])
    stat = statistics.median if b.get("peer_stat", "median") == "median" else statistics.mean
    excluded = {}

    def peer_mult(key):
        vals = []
        for p in peers:
            v = p.get(key)
            if v is None:
                continue  # not reported for this peer
            if v <= 0 or p.get("exclude", {}).get(key):
                excluded.setdefault(key, []).append(p["ticker"])  # negative / n/m: flag, never average
                continue
            vals.append(v)
        return stat(vals) if vals else None

    pe_key = "pe" if not b.get("pre_profit") else "ev_revenue"
    m = {
        "Comparable EV/EBITDA": (peer_mult("ev_ebitda"), b["fwd_ebitda"], "ev"),
        "Historical EV/EBITDA": (b["hist_ev_ebitda"], b["hist_avg_ebitda"], "ev"),
        "Comparable EV/Sales": (peer_mult("ev_sales"), b["fwd_revenue"], "ev"),
        "Comparable P/E": (peer_mult(pe_key), b["fwd_eps"] if pe_key == "pe" else b["fwd_revenue"],
                           "pe" if pe_key == "pe" else "ev"),
        "Historical EV/Sales": (b["hist_ev_sales"], b["hist_avg_revenue"], "ev"),
        "Historical P/E": (b["hist_pe"] if pe_key == "pe" else b.get("hist_ev_revenue"),
                           b["hist_avg_eps"] if pe_key == "pe" else b["hist_avg_revenue"],
                           "pe" if pe_key == "pe" else "ev"),
    }
    weights = b.get("weights", {"DCF": .50, "Comparable EV/EBITDA": .15, "Historical EV/EBITDA": .15,
                                 "Comparable EV/Sales": .05, "Comparable P/E": .05,
                                 "Historical EV/Sales": .05, "Historical P/E": .05})
    rows = [{"method": "DCF", "weight": weights["DCF"], "multiple": None, "value": dcf_ps}]
    for name, (mult, metric, kind) in m.items():
        label = name if pe_key == "pe" else name.replace("P/E", "EV/Revenue")
        val = multiple_value(mult, metric, kind, nd, sh) if mult else None
        rows.append({"method": label, "weight": weights[name], "multiple": mult, "value": val})
    live = [r for r in rows if r["value"] is not None]
    wsum = sum(r["weight"] for r in live)
    for r in rows:
        r["contribution"] = r["value"] * r["weight"] / wsum if r["value"] is not None else None
    return {"rows": rows, "blended": sum(r["contribution"] for r in live), "weight_used": wsum,
            "excluded_peers": excluded, "peer_stat": b.get("peer_stat", "median")}


def scenarios(inp):
    s = inp["scenarios"]
    entry = inp["position"]["entry"]
    price = inp["market"]["price"]
    for x in s:
        x["ret_entry"] = x["price"] / entry - 1
        x["ret_price"] = x["price"] / price - 1
    ev = sum(x["weight"] * x["price"] for x in s)
    return {"cases": s, "weighted": ev, "weighted_ret_entry": ev / entry - 1, "weighted_ret_price": ev / price - 1,
            "weights_sum": sum(x["weight"] for x in s)}


def payoff(inp):
    p = inp["position"]
    up = p["target"] / p["entry"] - 1
    dn = 1 - p["stop"] / p["entry"]
    b = up / dn
    q = p.get("p_win", 0.5)
    kelly = q - (1 - q) / b
    return {"upside": up, "downside": -dn, "ratio": b, "p_win": q, "kelly": kelly,
            "half_kelly": kelly / 2, "size": p["size"]}


def grid(d, waccs, cols, mode):
    out = []
    for w in waccs:
        row = []
        for c in cols:
            r = dcf(d, w, exit_mult=c) if mode == "exit" else dcf(d, w, g=c)
            row.append(None if r is None else r["per_share"])
        out.append(row)
    return out


def fmt_money(x, cur="$"):
    return "n/m" if x is None else f"{cur}{x:,.2f}"


def pct(x, d=1):
    return "n/m" if x is None else f"{x*100:+.{d}f}%"


def pl(x, d=1):
    return "n/m" if x is None else f"{x*100:.{d}f}%"


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    inp = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    cur = inp.get("currency", "$")
    d = inp["dcf"]
    w = wacc_build(inp["wacc"])
    W = inp["dcf"].get("wacc_override") or w["wacc"]
    gordon = dcf(d, W)
    exit_ = dcf(d, W, exit_mult=d["exit_multiple"]) if d.get("exit_multiple") else None
    dcf_ps = gordon["per_share"] if d.get("anchor", "gordon") == "gordon" else exit_["per_share"]
    step = inp.get("grid_wacc_step", 0.01)
    waccs = [round(W + k * step, 4) for k in (-2, -1, 0, 1, 2)]
    em = d.get("exit_multiple") or 15
    exits = [em - 4, em - 2, em, em + 2, em + 4]
    gs = [d["terminal_growth"] + k for k in (-0.01, -0.005, 0, 0.005, 0.01)]
    res = {
        "ticker": inp["ticker"], "as_of": inp["as_of"], "currency": cur,
        "market": inp["market"], "position": inp["position"],
        "wacc": w, "wacc_used": W,
        "dcf_gordon": gordon, "dcf_exit": exit_, "dcf_per_share": dcf_ps,
        "grid_wacc_exit": {"waccs": waccs, "cols": exits, "values": grid(d, waccs, exits, "exit")},
        "grid_wacc_g": {"waccs": waccs, "cols": gs, "values": grid(d, waccs, gs, "g")},
        "reverse_dcf": reverse_dcf(d, W, inp["market"]["price"]),
        "blend": blend(inp, dcf_ps) if inp.get("blend") else None,
        "scenarios": scenarios(inp) if inp.get("scenarios") else None,
        "payoff": payoff(inp),
    }
    json.dump(res, open(out + ".json", "w"), indent=2, default=float)

    # ---------- markdown ----------
    L = []
    L.append(f"# {inp['ticker']} valuation output · as of {inp['as_of']}\n")
    L.append("## Cost of capital\n\n| Input | Value |\n|---|---|")
    L += [f"| Risk-free (10Y) | {pl(w['rf'],2)} |", f"| Beta | {w['beta']:.2f} |", f"| ERP | {pl(w['erp'],2)} |",
          f"| CRP | {pl(w['crp'],2)} |", f"| Size premium | {pl(w['size_premium'],2)} |",
          f"| Cost of equity | {pl(w['ke'],2)} |", f"| After-tax cost of debt | {pl(w['kd_after'],2)} |",
          f"| E/V · D/V | {pl(w['e_weight'])} · {pl(w['d_weight'])} |", f"| **WACC** | **{pl(w['wacc'],2)}** |"]
    if W != w["wacc"]:
        L.append(f"\nWACC used in DCF (override): {pl(W,2)}")
    L.append(f"\n## DCF (UFCF, {'mid-year' if d.get('mid_year') else 'year-end'} discounting)\n")
    L.append("| Year | Revenue | Growth | EBIT margin | NOPAT | D&A | CapEx | ΔNWC | UFCF | PV |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in gordon["rows"]:
        L.append(f"| {r['year']} | {r['revenue']:,.0f} | {pl(r['growth'])} | {pl(r['ebit_margin'])} | {r['nopat']:,.0f} | "
                 f"{r['da']:,.0f} | {r['capex']:,.0f} | {r['dnwc']:,.0f} | {r['ufcf']:,.0f} | {r['pv']:,.0f} |")
    L.append(f"\nGordon (g = {pl(d['terminal_growth'])}): EV {gordon['ev']:,.0f} · equity {gordon['equity']:,.0f} · "
             f"**{fmt_money(gordon['per_share'], cur)}/share** · terminal value {pl(gordon['tv_share'])} of EV")
    if exit_:
        L.append(f"Exit multiple ({d['exit_multiple']}× EBITDA): **{fmt_money(exit_['per_share'], cur)}/share** · "
                 f"terminal value {pl(exit_['tv_share'])} of EV")
    for key, title, lab in (("grid_wacc_exit", "WACC × exit EV/EBITDA", lambda c: f"{c:.0f}×"),
                            ("grid_wacc_g", "WACC × terminal growth", lambda c: pl(c))):
        g = res[key]
        L.append(f"\n## Sensitivity: {title}\n")
        L.append("| WACC | " + " | ".join(lab(c) for c in g["cols"]) + " |")
        L.append("|---" * (len(g["cols"]) + 1) + "|")
        for wv, row in zip(g["waccs"], g["values"]):
            L.append(f"| {pl(wv)} | " + " | ".join(fmt_money(v, cur) for v in row) + " |")
    rd = res["reverse_dcf"]
    L.append(f"\n## Reverse DCF at {fmt_money(inp['market']['price'], cur)}\n\n| What must be true (one at a time) | Implied | Our base |\n|---|---|---|")
    L.append(f"| Discount rate | {pl(rd['implied_wacc'],2)} | {pl(W,2)} |")
    L.append(f"| Terminal EBIT margin | {pl(rd['implied_terminal_ebit_margin'])} | {pl(d['ebit_margin'][-1])} |")
    L.append(f"| Revenue CAGR | {pl(rd['implied_revenue_cagr'])} | {pl((gordon['rows'][-1]['revenue']/d['base_revenue'])**(1/len(d['growth']))-1)} |")
    L.append(f"| Final-year revenue | {rd['implied_final_year_revenue']:,.0f} | {gordon['rows'][-1]['revenue']:,.0f} |")
    L.append(f"| Terminal growth | {pl(rd['implied_terminal_growth'])} | {pl(d['terminal_growth'])} |")
    if res["blend"]:
        bl = res["blend"]
        L.append("\n## Weighted valuation blend\n\n| Valuation method | Weighting | Multiple | Valuation | Contribution |\n|---|---|---|---|---|")
        for r in bl["rows"]:
            mult = "" if r["multiple"] is None else f"{r['multiple']:.1f}×"
            L.append(f"| {r['method']} | {pl(r['weight'],0)} | {mult} | {fmt_money(r['value'], cur)} | {fmt_money(r['contribution'], cur)} |")
        L.append(f"| **Blended target price** | | | | **{fmt_money(bl['blended'], cur)}** |")
        if bl["excluded_peers"]:
            L.append("\nExcluded from peer " + bl["peer_stat"] + " (negative or n/m): " +
                     "; ".join(f"{k}: {', '.join(v)}" for k, v in bl["excluded_peers"].items()))
        if abs(bl["weight_used"] - 1) > 1e-9:
            L.append(f"\nWeights re-normalised over available methods ({pl(bl['weight_used'],0)} of 100%).")
    if res["scenarios"]:
        sc = res["scenarios"]
        L.append("\n## Scenarios\n\n| | " + " | ".join(c["name"] for c in sc["cases"]) + " |\n|---" + "|---" * len(sc["cases"]) + "|")
        L.append("| Weight | " + " | ".join(pl(c["weight"], 0) for c in sc["cases"]) + " |")
        L.append("| Price | " + " | ".join(fmt_money(c["price"], cur) for c in sc["cases"]) + " |")
        L.append("| Return from entry | " + " | ".join(pct(c["ret_entry"]) for c in sc["cases"]) + " |")
        L.append("| Multiple | " + " | ".join(c.get("multiple", "") for c in sc["cases"]) + " |")
        L.append(f"\nProbability-weighted value: **{fmt_money(sc['weighted'], cur)}** ({pct(sc['weighted_ret_entry'])} vs entry, "
                 f"{pct(sc['weighted_ret_price'])} vs price). Weights sum to {pl(sc['weights_sum'],0)}.")
    p = res["payoff"]
    L.append(f"\n## Payoff asymmetry\n\nUpside to target {pct(p['upside'])} · downside to stop {pct(p['downside'])} · "
             f"ratio **{p['ratio']:.2f} to 1** · p(win) {pl(p['p_win'],0)} · Kelly {pl(p['kelly'])} · "
             f"half-Kelly **{pl(p['half_kelly'])}** · position size **{pl(p['size'],1)}**")
    open(out + ".md", "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
