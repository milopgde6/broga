import json
import os

from app.data.models import Set
from app.data.db import SessionLocal
from app.storage import files
from app.storage.layout import manifest_path


def build_manifest(set_id: int) -> str:
    """Write a hash manifest for a set. Returns the storage key."""
    with SessionLocal() as db:
        s = db.query(Set).get(set_id)
        if not s:
            raise ValueError("set not found")
        entries = []
        for c in s.clips:
            key = files.key_for(c.path)
            if files.exists(key):
                entries.append({
                    "file": os.path.basename(key),
                    "sha256": files.sha256(key),
                    "bytes": files.size(key),
                })
        manifest = {
            "set_id": s.id,
            "title": s.title,
            "era": s.era,
            "quality": s.quality,
            "clips": entries,
        }
    return files.write_text(manifest_path(set_id), json.dumps(manifest, indent=2))


def verify_manifest(set_id: int) -> bool:
    """Re-hash and compare against stored manifest."""
    path = manifest_path(set_id)
    if not files.exists(path):
        return False
    manifest = json.loads(files.read_text(path))
    with SessionLocal() as db:
        s = db.query(Set).get(set_id)
        for entry, clip in zip(manifest["clips"], s.clips):
            key = files.key_for(clip.path)
            if not files.exists(key):
                return False
            if files.sha256(key) != entry["sha256"]:
                return False
    return True
