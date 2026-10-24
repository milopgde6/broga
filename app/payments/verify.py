# app/payments/verify.py
from typing import Optional

from app.data.models import Order
from app.data.db import SessionLocal


def mark_paid(ref: str, rail: Optional[str] = None) -> Optional[Order]:
    """Idempotent: mark order paid. Returns the order, or None if unknown."""
    db = SessionLocal()
    try:
        order = db.query(Order).filter_by(ref=ref).first()
        if not order:
            return None
        if order.status != "paid":
            order.status = "paid"
            if rail:
                order.rail = rail
            db.commit()
            db.refresh(order)
        return order
    finally:
        db.close()
