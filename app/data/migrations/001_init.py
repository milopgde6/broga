# app/data/migrations/001_init.py
from app.data.db import Base, engine
from app.data import models  # noqa: F401

def up():
    Base.metadata.create_all(engine)