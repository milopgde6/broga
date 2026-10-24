#!/usr/bin/env python3
"""Transcode raw clips to H.264/AAC MP4 with faststart."""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data.models import Clip
from app.data.db import SessionLocal


def transcode(src: str, dst: str):
    subprocess.run([
        "ffmpeg", "-y", "-i", src,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart", dst,
    ], check=True)


def main():
    args = sys.argv[1:]
    if len(args) == 2:
        transcode(args[0], args[1])
        print("✅ done")
        return
    with SessionLocal() as db:
        for c in db.query(Clip).all():
            if not os.path.exists(c.path):
                continue
            base, _ = os.path.splitext(c.path)
            dst = base + ".mp4"
            if os.path.exists(dst):
                continue
            try:
                transcode(c.path, dst)
                print(f"✅ {c.id} → {dst}")
            except subprocess.CalledProcessError as e:
                print(f"❌ {c.id}: {e}")


if __name__ == "__main__":
    main()