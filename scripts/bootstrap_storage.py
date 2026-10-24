#!/usr/bin/env python3
"""Bootstrap the Theez storage + backup tree.

Pure stdlib — no app imports, no dotenv, no DB. Run it any time; idempotent.
Creates each dir, pins it with .gitkeep, and drops a README so no folder
is ever empty on disk.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --- directories that must exist ---
DIRS = [
    "app/data/backups/daily",
    "app/data/backups/weekly",
    "app/storage/originals",
    "app/storage/encoded",
    "app/storage/previews",
    "app/storage/proof",
    "app/storage/thumbs",
    "app/storage/posters",
    "app/storage/manifests",
    "app/storage/temp",
    "app/storage/by_studio",
]

# --- README per dir so it's never "empty" ---
READMES = {
    "app/storage/originals":  "# originals\nMaster files. Never re-encoded from a copy.\n",
    "app/storage/encoded":    "# encoded\nDelivery copies. Regenerable from originals.\n",
    "app/storage/previews":   "# previews\nShort teaser clips for the card view.\n",
    "app/storage/proof":      "# proof\nOne real clip per set, shown before purchase.\n",
    "app/storage/thumbs":     "# thumbs\nGenerated thumbnails (clip_<id>.jpg).\n",
    "app/storage/posters":    "# posters\nCover art per set.\n",
    "app/storage/manifests":  "# manifests\nSHA-256 hash manifest per set (set_<id>.json).\n",
    "app/storage/temp":       "# temp\nScratch space. Safe to wipe.\n",
    "app/storage/by_studio":  (
        "# by_studio\n\nHuman-browsable mirror of the archive.\n\n"
        "Shape: `by_studio/<studio>/<year>/<girl>/<set>/`\n\n"
        "`<studio>` etc. are placeholders — real folders are created as sets\n"
        "are ingested. See the `_demo` path for a concrete example.\n"
    ),
    "app/data/backups/daily":  "# daily\nNightly DB snapshots.\n",
    "app/data/backups/weekly": "# weekly\nWeekly DB snapshots.\n",
}

# --- one concrete example so the by_studio shape is visible ---
DEMO_SET = "app/storage/by_studio/_demo/2004/Demo_Girl/Set_01"


def main() -> None:
    made = 0

    for d in DIRS:
        p = ROOT / d
        p.mkdir(parents=True, exist_ok=True)

        keep = p / ".gitkeep"
        if not keep.exists():
            keep.touch()

        if d in READMES:
            rd = p / "README.md"
            if not rd.exists():
                rd.write_text(READMES[d], encoding="utf-8")

        made += 1
        print(f"  ok  {d}")

    # concrete demo path
    demo = ROOT / DEMO_SET
    demo.mkdir(parents=True, exist_ok=True)
    (demo / ".gitkeep").touch()
    print(f"  ok  {DEMO_SET}")

    print(f"\n✅ {made + 1} directories present, pinned, and documented.")


if __name__ == "__main__":
    main()