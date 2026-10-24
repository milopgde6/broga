# app/access/revoke.py
from app.data.models import Entitlement
from app.data.db import SessionLocal

def revoke(user_id: int, set_id: int):
    with SessionLocal() as db:
        db.query(Entitlement).filter_by(
            user_id=user_id, set_id=set_id).delete()
        db.commit()