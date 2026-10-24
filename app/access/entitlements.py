# app/access/entitlements.py
from app.data.models import Entitlement, Set
from app.data.db import SessionLocal

def owns(user_id: int, set_id: int) -> bool:
    db = SessionLocal()
    try:
        return db.query(Entitlement).filter_by(
            user_id=user_id, set_id=set_id).first() is not None
    finally:
        db.close()

def grant(user_id: int, set_id: int) -> Entitlement:
    db = SessionLocal()
    try:
        existing = db.query(Entitlement).filter_by(
            user_id=user_id, set_id=set_id).first()
        if existing:
            return existing
        ent = Entitlement(user_id=user_id, set_id=set_id)
        db.add(ent)
        db.commit()
        db.refresh(ent)
        return ent
    finally:
        db.close()

def owned_set_ids(user_id: int) -> list[int]:
    db = SessionLocal()
    try:
        rows = db.query(Entitlement.set_id).filter_by(user_id=user_id).all()
        return [r[0] for r in rows]
    finally:
        db.close()