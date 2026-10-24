import os

from app.access.tokenize import mint
from app.storage import files


def build_links(user_id: int, set_id: int, clips: list) -> list[dict]:
    """Return per-clip delivery payloads.

    With R2 configured these are short-lived presigned URLs; otherwise they
    fall back to the signed local ``/stream`` path.
    """
    token = mint(user_id, set_id)
    out = []
    for c in clips:
        key = files.key_for(c.path)
        fname = os.path.basename(key)
        url = files.url(key) or f"/stream/{token}/{fname}"
        out.append({
            "clip_id": c.id,
            "filename": fname,
            "token": token,
            "url": url,
        })
    return out
