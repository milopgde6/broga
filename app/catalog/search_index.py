# app/catalog/search_index.py
from app.data.models import Set, Girl, Studio
from app.data.db import SessionLocal

def search(query: str, limit: int = 20) -> list:
    db = SessionLocal()
    try:
        q = f"%{query.lower()}%"
        return (db.query(Set)
                  .join(Girl, Set.girl_id == Girl.id, isouter=True)
                  .join(Studio, Set.studio_id == Studio.id, isouter=True)
                  .filter(
                      Set.title.ilike(q) |
                      Girl.name.ilike(q) |
                      Studio.name.ilike(q) |
                      Set.era.ilike(q)
                  )
                  .limit(limit).all())
    finally:
        db.close()

def by_age(lo: int, hi: int, limit: int = 50) -> list:
    db = SessionLocal()
    try:
        return (db.query(Set)
                  .join(Girl, Set.girl_id == Girl.id)
                  .filter(Girl.age >= lo, Girl.age <= hi)
                  .limit(limit).all())
    finally:
        db.close()

def by_studio(name: str, limit: int = 50) -> list:
    db = SessionLocal()
    try:
        return (db.query(Set)
                  .join(Studio, Set.studio_id == Studio.id)
                  .filter(Studio.name == name)
                  .limit(limit).all())
    finally:
        db.close()

def by_era(era: str, limit: int = 50) -> list:
    db = SessionLocal()
    try:
        return db.query(Set).filter(Set.era == era).limit(limit).all()
    finally:
        db.close()