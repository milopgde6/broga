# app/catalog/studios.py
from app.data.models import Studio
from app.data.db import SessionLocal

def all_studios():
    with SessionLocal() as db:
        return db.query(Studio).order_by(Studio.name).all()