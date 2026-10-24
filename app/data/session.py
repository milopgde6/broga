# app/data/session.py
from app.data.db import SessionLocal

def session():
    return SessionLocal()