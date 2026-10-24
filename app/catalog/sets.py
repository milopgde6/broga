# app/catalog/sets.py
from app.data.models import Set
from app.data.db import SessionLocal

def by_age(lo: int, hi: int):
    from app.data.models import Girl
    with SessionLocal() as db:
        return (db.query(Set).join(Girl)
                  .filter(Girl.age >= lo, Girl.age <= hi).all())

def by_studio(name: str):
    from app.data.models import Studio
    with SessionLocal() as db:
        return (db.query(Set).join(Studio)
                  .filter(Studio.name == name).all())

def by_era(era: str):
    with SessionLocal() as db:
        return db.query(Set).filter(Set.era == era).all()

def featured(limit: int = 10):
    with SessionLocal() as db:
        return db.query(Set).filter(Set.is_full == True).limit(limit).all()

def rare(limit: int = 10):
    with SessionLocal() as db:
        return db.query(Set).filter(Set.is_rare == True).limit(limit).all()