#!/usr/bin/env python3
"""Generate public search engine discovery links for German shopping sources (no scraping)."""
import argparse
import json
from pathlib import Path
from urllib.parse import quote_plus, urlsplit

ROOT = Path(__file__).resolve().parent.parent
CATEGORIES = ("all", "phones", "tablets", "laptops", "pc", "apple", "gaming", "cameras", "audio")
SIMPLE = {"idealo": ("Idealo", "https://www.idealo.de/"), "geizhals": ("Geizhals", "https://geizhals.de/")}

def build_entries(product, sources, category="all", limit=None):
    if not product.strip():
        raise ValueError("Specify a product")
    providers = json.loads((ROOT / "data/refurbishers_de.json").read_text(encoding="utf-8"))["providers"]
    results = []
    for source in dict.fromkeys(sources):
        if source == "refurb":
            selected = [p for p in providers if category == "all" or category in p["categories"]]
        else:
            name, url = SIMPLE[source]
            selected = [{"id": source, "name": name, "url": url, "kind": "comparison"}]
        for p in selected:
            domain = urlsplit(p["url"]).hostname.removeprefix("www.")
            phrase = product.replace('"', " ")
            query = f'site:{domain} "{phrase}"' + (" refurbished" if source == "refurb" else "")
            results.append({"source": source, "id": p["id"], "name": p["name"], "kind": p["kind"], "shop_url": p["url"], "search_query": query, "google_url": "https://www.google.com/search?q=" + quote_plus(query), "bing_url": "https://www.bing.com/search?q=" + quote_plus(query), "status": "not checked"})
    return results[:limit] if limit is not None else results

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product")
    parser.add_argument("--sources", nargs="+", choices=["refurb", "idealo", "geizhals"], default=["idealo","geizhals","refurb"])
    parser.add_argument("--category", choices=CATEGORIES, default="all")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--format", choices=["text","json"], default="text")
    a = parser.parse_args()
    if a.limit < 1: parser.error("--limit must be positive")
    providers = build_entries(a.product, a.sources, a.category, None if a.all else a.limit)
    if a.format == "json":
        print(json.dumps({"product": a.product, "category": a.category, "generated": len(providers), "providers": providers}, indent=2, ensure_ascii=False))
    else:
        for item in providers: print(f'{item["name"]} [{item["kind"]}]: {item["google_url"]}')

if __name__ == "__main__":
    main()
