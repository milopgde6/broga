# app/catalog/ingest.py
import os
from app.utils.hashing import sha256_file
from app.data.models import Set, Clip, Girl, Studio
from app.data.db import SessionLocal

def ingest_set(title, studio_name, girl_name, age, ethnicity,
               era, quality, price, files):
    """Register a set + its clips. files = list of encoded paths."""
    with SessionLocal() as db:
        studio = db.query(Studio).filter_by(name=studio_name).first()
        if not studio:
            studio = Studio(name=studio_name)
            db.add(studio); db.flush()
        girl = db.query(Girl).filter_by(name=girl_name).first()
        if not girl:
            girl = Girl(name=girl_name, age=age, ethnicity=ethnicity)
            db.add(girl); db.flush()
        s = Set(title=title, studio_id=studio.id, girl_id=girl.id,
                era=era, quality=quality, price=price)
        db.add(s); db.flush()
        for p in files:
            db.add(Clip(set_id=s.id, path=p))
        db.commit()
        return s.id