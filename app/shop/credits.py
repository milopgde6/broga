# app/shop/credits.py
from app.data.models import User
from app.data.db import SessionLocal

def balance(user_id: int) -> int:
    db = SessionLocal()
    try:
        u = db.query(User).get(user_id)
        return u.credits if u else 0
    finally:
        db.close()

def add(user_id: int, amount: int) -> int:
    db = SessionLocal()
    try:
        u = db.query(User).get(user_id)
        if not u:
            return 0
        u.credits += amount
        db.commit()
        return u.credits
    finally:
        db.close()

def spend(user_id: int, amount: int) -> bool:
    db = SessionLocal()
    try:
        u = db.query(User).get(user_id)
        if not u or u.credits < amount:
            return False
        u.credits -= amount
        db.commit()
        return True
    finally:
        db.close()