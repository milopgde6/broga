#!/usr/bin/env python3
"""Bulk import sets from a folder tree.

Layout expected:
  <root>/<set_title>/<files...>
  <root>/<set_title>/meta.txt   (optional: studio|girl|age|eth|era|quality|price)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.catalog.ingest import ingest_set
from app.catalog.manifest import build_manifest


def parse_meta(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        line = f.read().strip()
    parts = [p.strip() for p in line.split("|")]
    if len(parts) != 7:
        return {}
    studio, girl, age, eth, era, quality, price = parts
    return {
        "studio_name": studio, "girl_name": girl, "age": int(age),
        "ethnicity": eth, "era": era, "quality": quality,
        "price": float(price),
    }


def main():
    if len(sys.argv) < 2:
        print("usage: import_bulk.py <root>")
        sys.exit(1)
    root = sys.argv[1]
    for name in sorted(os.listdir(root)):
        d = os.path.join(root, name)
        if not os.path.isdir(d):
            continue
        files = [os.path.join(d, f) for f in os.listdir(d) if not f.startswith("meta")]
        meta = parse_meta(os.path.join(d, "meta.txt"))
        if not meta:
            print(f"⚠️  {name}: no meta.txt, skipping")
            continue
        try:
            sid = ingest_set(title=name, files=files, **meta)
            build_manifest(sid)
            print(f"✅ {name} → set {sid}")
        except Exception as e:
            print(f"❌ {name}: {e}")


if __name__ == "__main__":
    main()