"""Build market-data.json: unusual options activity and House STOCK Act trades.

Runs in GitHub Actions (the static site can't call these sources directly).
Each section is kept from the previous snapshot if its source fails.
"""
import datetime as dt
import io
import json
import re
import sys
import time
import zipfile
import xml.etree.ElementTree as ET

import requests

OUT = "market-data.json"
UA = {"User-Agent": "Mozilla/5.0 (aeonnimbus market-data snapshot; github.com/lijiegsluis/aeonnimbus)"}
NOW = dt.datetime.now(dt.timezone.utc)

FLOW_TICKERS = ["SPY", "QQQ", "IWM", "NVDA", "AAPL", "MSFT", "AMZN", "META", "GOOGL", "TSLA",
                "AMD", "AVGO", "ORCL", "NFLX", "PLTR", "COIN", "MSTR", "JPM", "XOM", "SMCI"]
MIN_VOLUME, MIN_VOL_OI, MIN_PREMIUM, EXPIRIES = 500, 2.0, 250_000, 4


def money(v):
    return f"${v / 1e6:.1f}M" if v >= 1e6 else f"${v / 1e3:.0f}K"


def options_flow():
    import yfinance as yf

    items = []
    for sym in FLOW_TICKERS:
        try:
            tk = yf.Ticker(sym)
            for exp in list(tk.options)[:EXPIRIES]:
                chain = tk.option_chain(exp)
                for kind, df in (("call", chain.calls), ("put", chain.puts)):
                    for r in df.itertuples():
                        vol, oi, last = r.volume or 0, r.openInterest or 0, r.lastPrice or 0
                        if vol != vol or oi != oi or vol < MIN_VOLUME or last <= 0:  # NaN guards
                            continue
                        ratio = vol / oi if oi else float("inf")
                        prem = vol * last * 100
                        if ratio < MIN_VOL_OI or prem < MIN_PREMIUM:
                            continue
                        bid, ask = r.bid or 0, r.ask or 0
                        # Aggressor side from where the last print sat in the spread
                        if ask and last >= ask * 0.98:
                            side = "bought"
                        elif bid and last <= bid * 1.02:
                            side = "sold"
                        else:
                            side = "mid"
                        bias = "neutral" if side == "mid" else (
                            "bullish" if (kind == "call") == (side == "bought") else "bearish")
                        ts = r.lastTradeDate
                        items.append({
                            "tk": sym, "type": kind, "strike": f"${r.strike:g}",
                            "expiry": dt.date.fromisoformat(exp).strftime("%b %d"), "exp": exp,
                            "prem": money(prem), "premNum": round(prem), "volOI": "new OI" if not oi else f"{ratio:.1f}×",
                            "vol": int(vol), "oi": int(oi), "bias": bias, "side": side,
                            "time": ts.strftime("%b %d %H:%M UTC") if hasattr(ts, "strftime") else "",
                        })
            time.sleep(0.5)
        except Exception as e:  # one bad ticker shouldn't sink the snapshot
            print(f"flow: {sym} failed: {e}", file=sys.stderr)
    items.sort(key=lambda x: x["premNum"], reverse=True)
    return items[:60]


PTR_ROW = re.compile(
    r"\(([A-Z][A-Z.\-]{0,6})\)\s*\[(?:ST|OP)\].{0,160}?\b(P|S(?:\s*\(partial\))?|E)\s+"
    r"(\d{2}/\d{2}/\d{4})\s*(\d{2}/\d{2}/\d{4})\s*(\$[\d,]+\s*-\s*\$[\d,]+|Over\s*\$[\d,]+)",
    re.S)


def legislators():
    url = "https://unitedstates.github.io/congress-legislators/legislators-current.json"
    out = {}
    for p in requests.get(url, headers=UA, timeout=60).json():
        term = p["terms"][-1]
        if term["type"] != "rep":
            continue
        party = {"Democrat": "D", "Republican": "R"}.get(term.get("party"), "I")
        out[(p["name"]["last"].lower(), term["state"])] = party
    return out


def house_trades(max_filings=60):
    from pypdf import PdfReader

    parties = legislators()
    filings = []
    for year in {NOW.year, (NOW - dt.timedelta(days=45)).year}:
        z = requests.get(f"https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}FD.zip",
                         headers=UA, timeout=120)
        z.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(z.content)) as zf:
            xml_name = next(n for n in zf.namelist() if n.endswith(".xml"))
            for m in ET.fromstring(zf.read(xml_name)).iter("Member"):
                if (m.findtext("FilingType") or "") != "P":
                    continue
                filed = dt.datetime.strptime(m.findtext("FilingDate"), "%m/%d/%Y").date()
                filings.append({"last": m.findtext("Last") or "", "first": m.findtext("First") or "",
                                "prefix": m.findtext("Prefix") or "", "state": (m.findtext("StateDst") or "")[:2],
                                "filed": filed, "doc": m.findtext("DocID"), "year": year})
    filings.sort(key=lambda f: f["filed"], reverse=True)

    trades, parsed = [], 0
    for f in filings:
        if parsed >= max_filings:
            break
        url = f"https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{f['year']}/{f['doc']}.pdf"
        try:
            pdf = requests.get(url, headers=UA, timeout=60)
            if pdf.status_code != 200:
                continue
            text = " ".join((pg.extract_text() or "") for pg in PdfReader(io.BytesIO(pdf.content)).pages)
        except Exception as e:
            print(f"congress: {f['doc']} unreadable: {e}", file=sys.stderr)
            continue
        parsed += 1
        text = re.sub(r"\s+", " ", text)
        name = " ".join(x for x in (f["first"], f["last"]) if x).strip()
        party = parties.get((f["last"].lower(), f["state"]), "?")
        for tk, kind, tdate, _ndate, amount in PTR_ROW.findall(text):
            if kind == "E":
                continue
            traded = dt.datetime.strptime(tdate, "%m/%d/%Y").date()
            trades.append({
                "pol": name, "party": party, "state": f["state"], "tk": tk,
                "dir": "BUY" if kind == "P" else "SELL",
                "amt": re.sub(r"\s+", " ", amount).replace(" - ", "–"),
                "trdate": traded.strftime("%b %d, %Y"), "traded": traded.isoformat(),
                "disclosed": f["filed"].isoformat(), "delay": max(0, (f["filed"] - traded).days),
                "sector": "", "link": url,
            })
        time.sleep(0.3)
    trades.sort(key=lambda t: (t["disclosed"], t["traded"]), reverse=True)
    print(f"congress: parsed {parsed} PTR filings, {len(trades)} stock trades", file=sys.stderr)
    return trades[:150]


def add_sectors(trades, limit=60):
    import yfinance as yf

    cache = {}
    for t in trades:
        tk = t["tk"]
        if tk not in cache and len(cache) < limit:
            try:
                cache[tk] = yf.Ticker(tk).info.get("sector") or ""
            except Exception:
                cache[tk] = ""
        t["sector"] = cache.get(tk, "")


def main():
    try:
        with open(OUT, encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    stamp = NOW.strftime("%Y-%m-%dT%H:%M:%SZ")
    ok = False
    try:
        flow = options_flow()
        if flow:
            data["flow"] = {"as_of": stamp, "items": flow,
                            "criteria": f"volume ≥ {MIN_VOLUME}, volume ≥ {MIN_VOL_OI:g}× open interest, "
                                        f"premium ≥ {money(MIN_PREMIUM)}, nearest {EXPIRIES} expiries"}
            ok = True
        print(f"flow: {len(flow)} unusual contracts", file=sys.stderr)
    except Exception as e:
        print(f"flow: failed: {e}", file=sys.stderr)

    try:
        trades = house_trades()
        if trades:
            add_sectors(trades)
            data["congress"] = {"as_of": stamp, "items": trades,
                                "source": "U.S. House Clerk periodic transaction reports (electronic filings)"}
            ok = True
    except Exception as e:
        print(f"congress: failed: {e}", file=sys.stderr)

    if not ok:
        sys.exit("No section refreshed; keeping the previous snapshot.")
    data["generated_at"] = stamp
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    for k in ("flow", "congress"):
        if k in data:
            print(f"{k}: {len(data[k]['items'])} items; first: {json.dumps(data[k]['items'][0])[:200]}")


if __name__ == "__main__":
    main()
