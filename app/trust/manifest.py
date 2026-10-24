import json
import os
from datetime import datetime

from app.storage import files
from app.storage.layout import MANIFESTS, manifest_path
from app.utils.hashing import sha256_file  # re-exported for callers

MANIFEST_DIR = MANIFESTS


def build_manifest(set_row, clip_paths: list[str]) -> dict:
    entries = []
    for p in clip_paths:
        key = files.key_for(p)
        entries.append({
            "file": os.path.basename(key),
            "sha256": files.sha256(key),
            "bytes": files.size(key),
        })
    manifest = {
        "set_id": set_row.id,
        "title": set_row.title,
        "built_at": datetime.utcnow().isoformat(),
        "clips": entries,
    }
    files.write_text(manifest_path(set_row.id), json.dumps(manifest, indent=2))
    return manifest
