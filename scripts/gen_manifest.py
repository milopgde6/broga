#!/usr/bin/env python3
"""Build manifests for all sets (or one)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data.models import Set
from app.data.db import SessionLocal
from app.catalog.manifest import build_manifest


def main():
    args = sys.argv[1:]
    with SessionLocal() as db:
        ids = [int(args[0])] if args else [s.id for s in db.query(Set).all()]
    for sid in ids:
        try:
            p = build_manifest(sid)
            print(f"✅ set {sid} → {p}")
        except Exception as e:
            print(f"❌ set {sid}: {e}")


if __name__ == "__main__":
    main()