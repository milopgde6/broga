# app/catalog/quality.py
from app.data.models import Set
from app.data.db import SessionLocal

QUALITIES = ["sd", "hd", "remaster"]

def by_quality(q: str):
    with SessionLocal() as db:
        return db.query(Set).filter(Set.quality == q).all()