#!/usr/bin/env python3
"""Generate a thumbnail per clip via ffmpeg."""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data.models import Clip
from app.data.db import SessionLocal
from config.settings import STORAGE_ROOT

THUMB_DIR = os.path.join(STORAGE_ROOT, "thumbs")


def main():
    os.makedirs(THUMB_DIR, exist_ok=True)
    with SessionLocal() as db:
        clips = db.query(Clip).all()
        for c in clips:
            if not os.path.exists(c.path):
                continue
            out = os.path.join(THUMB_DIR, f"clip_{c.id}.jpg")
            if os.path.exists(out):
                continue
            subprocess.run([
                "ffmpeg", "-y", "-ss", "00:00:02", "-i", c.path,
                "-frames:v", "1", "-vf", "scale=480:-1", out,
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ thumb {c.id}")


if __name__ == "__main__":
    main()