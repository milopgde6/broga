# app/catalog/manifest.py
import json, os
from app.utils.hashing import sha256_file
from app.data.models import Set
from app.data.db import SessionLocal
from app.storage.layout import MANIFESTS, manifest_path

def build_manifest(set_id: int) -> str:
    """Write a hash manifest for a set. Returns manifest path."""
    os.makedirs(MANIFESTS, exist_ok=True)
    with SessionLocal() as db:
        s = db.query(Set).get(set_id)
        if not s:
            raise ValueError("set not found")
        entries = []
        for c in s.clips:
            if os.path.exists(c.path):
                entries.append({
                    "file": os.path.basename(c.path),
                    "sha256": sha256_file(c.path),
                    "bytes": os.path.getsize(c.path),
                })
        manifest = {
            "set_id": s.id,
            "title": s.title,
            "era": s.era,
            "quality": s.quality,
            "clips": entries,
        }
    path = manifest_path(set_id)
    with open(path, "w") as f:
        json.dump(manifest, f, indent=2)
    return path

def verify_manifest(set_id: int) -> bool:
    """Re-hash and compare against stored manifest."""
    path = manifest_path(set_id)
    if not os.path.exists(path):
        return False
    with open(path) as f:
        manifest = json.load(f)
    with SessionLocal() as db:
        s = db.query(Set).get(set_id)
        for entry, clip in zip(manifest["clips"], s.clips):
            if not os.path.exists(clip.path):
                return False
            if sha256_file(clip.path) != entry["sha256"]:
                return False
    return True