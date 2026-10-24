# app/catalog/stats.py
from app.data.models import Set, Clip
from app.data.db import SessionLocal

def counts():
    with SessionLocal() as db:
        return {
            "sets": db.query(Set).count(),
            "clips": db.query(Clip).count(),
        }