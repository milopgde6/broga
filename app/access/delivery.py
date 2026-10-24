# app/access/delivery.py
import os
from app.access.tokenize import mint

def build_links(user_id: int, set_id: int, clips: list) -> list[dict]:
    """Return per-clip delivery payloads with signed tokens."""
    token = mint(user_id, set_id)
    out = []
    for c in clips:
        fname = os.path.basename(c.path)
        out.append({
            "clip_id": c.id,
            "filename": fname,
            "token": token,
            "url": f"/stream/{token}/{fname}",   # served by your web layer
        })
    return out