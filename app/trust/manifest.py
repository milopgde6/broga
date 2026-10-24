# app/trust/manifest.py
import hashlib, os, json
from datetime import datetime
from app.storage.layout import MANIFESTS, manifest_path

MANIFEST_DIR = MANIFESTS

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def build_manifest(set_row, clip_paths: list[str]) -> dict:
    os.makedirs(MANIFESTS, exist_ok=True)
    entries = []
    for p in clip_paths:
        entries.append({
            "file": os.path.basename(p),
            "sha256": sha256_file(p),
            "bytes": os.path.getsize(p),
        })
    manifest = {
        "set_id": set_row.id,
        "title": set_row.title,
        "built_at": datetime.utcnow().isoformat(),
        "clips": entries,
    }
    out = manifest_path(set_row.id)
    with open(out, "w") as f:
        json.dump(manifest, f, indent=2)
    return manifest