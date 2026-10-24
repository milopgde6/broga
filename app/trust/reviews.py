# app/trust/reviews.py
from app.data.models import Review
from app.data.db import SessionLocal

def add(user_id: int, set_id: int, stars: int, text: str = ""):
    with SessionLocal() as db:
        db.add(Review(user_id=user_id, set_id=set_id,
                      stars=max(1, min(5, stars)), text=text))
        db.commit()

def for_set(set_id: int):
    with SessionLocal() as db:
        return db.query(Review).filter_by(set_id=set_id).all()

def avg_stars(set_id: int) -> float:
    rows = for_set(set_id)
    return round(sum(r.stars for r in rows) / len(rows), 2) if rows else 0.0