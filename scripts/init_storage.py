#!/usr/bin/env python3
"""Create + pin the full storage tree. Safe to run any time."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.storage.layout import ensure_layout


def main():
    dirs = ensure_layout()
    print(f"✅ {len(dirs)} dirs ensured + .gitkeep pinned:")
    for d in dirs:
        print(f"   {d}")


if __name__ == "__main__":
    main()