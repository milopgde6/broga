# app/shop/orders.py
"""Order lifecycle: create, mark paid, fetch."""
import secrets
from typing import Optional, List

from app.data.models import Order
from app.data.db import SessionLocal


def _new_ref() -> str:
    return secrets.token_hex(6)  # 12 hex chars


def create(user_id: int, set_id: int, amount: float, rail: str) -> Order:
    ref = _new_ref()
    with SessionLocal() as db:
        o = Order(ref=ref, user_id=user_id, set_id=set_id,
                  amount=amount, rail=rail, status="pending")
        db.add(o)
        db.commit()
        db.refresh(o)
        return o


def get(ref: str) -> Optional[Order]:
    with SessionLocal() as db:
        return db.query(Order).filter_by(ref=ref).first()


def mark_paid(ref: str, rail: Optional[str] = None) -> Optional[Order]:
    with SessionLocal() as db:
        o = db.query(Order).filter_by(ref=ref).first()
        if not o or o.status == "paid":
            return o
        o.status = "paid"
        if rail:
            o.rail = rail
        db.commit()
        db.refresh(o)
        return o


def mark_failed(ref: str) -> Optional[Order]:
    with SessionLocal() as db:
        o = db.query(Order).filter_by(ref=ref).first()
        if not o:
            return None
        o.status = "failed"
        db.commit()
        return o


def for_user(user_id: int) -> List[Order]:
    with SessionLocal() as db:
        return (db.query(Order)
                  .filter_by(user_id=user_id)
                  .order_by(Order.created_at.desc())
                  .all())


def pending_for_user(user_id: int) -> List[Order]:
    with SessionLocal() as db:
        return (db.query(Order)
                  .filter_by(user_id=user_id, status="pending")
                  .all())


def pending_for_user_all():
    with SessionLocal() as db:
        return db.query(Order).filter_by(status="pending").all()
