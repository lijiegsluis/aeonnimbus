"""Snapshot the Substack RSS feed into research-feed.json (rss2json-compatible shape)."""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from datetime import timezone

RSS = "https://aeonnimbus.substack.com/feed"
OUT = "research-feed.json"
NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
}


def text(el, path):
    found = el.find(path, NS)
    return (found.text or "").strip() if found is not None else ""


def main():
    req = urllib.request.Request(RSS, headers={"User-Agent": "Mozilla/5.0 (aeonnimbus feed snapshot)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        root = ET.fromstring(r.read())
    ch = root.find("channel")

    items = []
    for it in ch.findall("item"):
        raw_date = text(it, "pubDate")
        try:
            pub = parsedate_to_datetime(raw_date).astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        except (TypeError, ValueError):
            pub = raw_date
        enc = it.find("enclosure")
        items.append({
            "title": text(it, "title"),
            "pubDate": pub,
            "link": text(it, "link"),
            "guid": text(it, "guid"),
            "author": text(it, "dc:creator"),
            "thumbnail": "",
            "description": text(it, "description"),
            "content": text(it, "content:encoded"),
            "enclosure": dict(enc.attrib) if enc is not None else {},
            "categories": [c.text for c in it.findall("category") if c.text],
        })

    if not items:
        sys.exit("Feed returned no items; keeping existing snapshot.")

    data = {
        "status": "ok",
        "feed": {
            "url": RSS,
            "title": text(ch, "title"),
            "link": text(ch, "link"),
            "author": text(ch, "dc:creator") or "Aeon Nimbus Research",
            "description": text(ch, "description"),
            "image": text(ch, "image/url"),
        },
        "items": items,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f"Wrote {len(items)} items; newest: {items[0]['pubDate']} {items[0]['title']}")


if __name__ == "__main__":
    main()
