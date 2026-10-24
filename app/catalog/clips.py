# app/catalog/clips.py
from app.data.models import Clip
from app.data.db import SessionLocal

def for_set(set_id: int):
    with SessionLocal() as db:
        return db.query(Clip).filter_by(set_id=set_id).all()