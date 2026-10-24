# app/catalog/eras.py
from app.data.models import Set
from app.data.db import SessionLocal

def all_eras():
    with SessionLocal() as db:
        rows = db.query(Set.era).distinct().all()
        return sorted([r[0] for r in rows if r[0]])