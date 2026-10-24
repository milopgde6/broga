# app/payments/shipstars.py
import uuid
from app.data.models import Order
from app.data.db import SessionLocal

def create_order(user_id: int, set_id: int, amount_usd: float) -> Order:
    db = SessionLocal()
    try:
        ref = f"THZ-{uuid.uuid4().hex[:10].upper()}"
        order = Order(user_id=user_id, set_id=set_id,
                      amount=amount_usd, rail="shipstars", ref=ref)
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    finally:
        db.close()

def invoice_payload(order: Order) -> dict:
    return {
        "title": "THEEZ · set unlock",
        "description": f"Set #{order.set_id}",
        "payload": order.ref,
        "currency": "USD",
        "prices": [{"label": "unlock", "amount": int(order.amount * 100)}],
    }