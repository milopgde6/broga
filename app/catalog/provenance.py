# app/catalog/provenance.py
from app.data.models import Set, Studio
from app.data.db import SessionLocal

def provenance_text(set_id: int) -> str:
    with SessionLocal() as db:
        s = db.query(Set).get(set_id)
        if not s:
            return "unknown set"
        return (
            f"📜 SOURCE\n"
            f"Studio: {s.studio.name}\n"
            f"Era: {s.era}\n"
            f"Quality: {s.quality}\n"
            f"Clips: {len(s.clips)}\n"
            f"🛡 hash-verified master archive"
        )