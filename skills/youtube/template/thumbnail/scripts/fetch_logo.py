"""Download a real brand logo for thumbnail references.

Sources, tried in this order (each only when its flag is given):
  --seller  App Store icon (iTunes Search API), 1024px. Seller must match, so knockoff apps never win.
  --wiki    Wikimedia Commons logo file (SVG rendered to 1024px PNG). Good for wordmarks.
  --domain  apple-touch-icon from the official site, then Google favicon. Small, last resort.

Always look at the result before feeding it to the image model.

Usage:
  python fetch_logo.py claude --term "Claude by Anthropic" --seller Anthropic
  python fetch_logo.py n8n --wiki "n8n logo" --domain n8n.io
  python fetch_logo.py upwork --wiki "Upwork logo" --out upwork-wordmark
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "logos"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "thumbnail-benai/1.0 (logo fetch)"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read(), r.headers.get("Content-Type", "")


def from_app_store(term, seller):
    q = urllib.parse.urlencode({"term": term, "entity": "software", "limit": 10})
    results = json.loads(get(f"https://itunes.apple.com/search?{q}")[0])["results"]
    for app in results:
        if seller.lower() in app["sellerName"].lower():
            url = app["artworkUrl512"].replace("512x512bb", "1024x1024bb")
            return get(url)[0], f"App Store: {app['trackName']} ({app['sellerName']})"
    return None, None


def from_commons(term, name):
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": term, "gsrlimit": 10, "prop": "imageinfo", "iiprop": "url", "iiurlwidth": 1024,
    })
    pages = json.loads(get(f"https://commons.wikimedia.org/w/api.php?{q}")[0]).get("query", {}).get("pages", {})
    files = [p for p in pages.values()
             if name.lower() in p["title"].lower() and p["title"].lower().endswith((".svg", ".png"))]
    files.sort(key=lambda p: (not p["title"].lower().endswith(".svg"), p.get("index", 99)))
    if not files:
        return None, None
    info = files[0]["imageinfo"][0]
    return get(info.get("thumburl") or info["url"])[0], f"Wikimedia Commons: {files[0]['title']}"


def from_domain(domain):
    try:
        data, ctype = get(f"https://{domain}/apple-touch-icon.png")
        if ctype.startswith("image/"):
            return data, f"apple-touch-icon: {domain}"
    except Exception:
        pass
    return get(f"https://www.google.com/s2/favicons?domain={domain}&sz=256")[0], f"favicon: {domain}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name", help="brand name (also the output file name), e.g. claude")
    ap.add_argument("--out", help="output file name when it differs from the brand, e.g. upwork-wordmark")
    ap.add_argument("--term", help="App Store search term (default: name)")
    ap.add_argument("--seller", help="App Store seller to match, e.g. OpenAI")
    ap.add_argument("--wiki", help="Wikimedia Commons search, e.g. 'n8n logo'")
    ap.add_argument("--domain", help="official website domain, e.g. n8n.io")
    args = ap.parse_args()

    data = source = None
    if args.seller:
        data, source = from_app_store(args.term or args.name, args.seller)
    if data is None and args.wiki:
        data, source = from_commons(args.wiki, args.name)
    if data is None and args.domain:
        data, source = from_domain(args.domain)
    if data is None:
        sys.exit(f"no logo found for {args.name}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{args.out or args.name}.png"
    img = Image.open(BytesIO(data)).convert("RGBA")
    img.save(out)
    warn = "  (small, may look blurry)" if max(img.size) < 256 else ""
    print(f"{out} | {img.size[0]}x{img.size[1]} | {source}{warn}")


if __name__ == "__main__":
    main()
