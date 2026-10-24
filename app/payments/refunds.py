# app/payments/reconciliation.py
from app.data.models import Order
from app.data.db import SessionLocal

def pending_orders():
    with SessionLocal() as db:
        return db.query(Order).filter_by(status="pending").all()

def stale_orders(older_than_sec: int = 3600):
    import time
    cutoff = time.time() - older_than_sec
    with SessionLocal() as db:
        return [o for o in db.query(Order).filter_by(status="pending").all()
                if o.created_at.timestamp() < cutoff]