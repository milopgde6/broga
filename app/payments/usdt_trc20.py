# app/payments/usdt_trc20.py
import uuid
from config.settings import USDT_TRC20_ADDR
from app.data.models import Order
from app.data.db import SessionLocal

def create_order(user_id: int, set_id: int, amount_usd: float) -> Order:
    db = SessionLocal()
    try:
        ref = f"THZ-{uuid.uuid4().hex[:10].upper()}"
        order = Order(user_id=user_id, set_id=set_id,
                      amount=amount_usd, rail="usdt", ref=ref)
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    finally:
        db.close()

def payment_instructions(order: Order) -> str:
    return (
        f"💎 *USDT (TRC20) payment*\n\n"
        f"Amount: `{order.amount}` USDT\n"
        f"Address: `{USDT_TRC20_ADDR}`\n"
        f"Ref: `{order.ref}`\n\n"
        f"⚡ Send exact amount. Include the ref in the memo if your wallet allows.\n"
        f"🛡 Access unlocks automatically once confirmed."
    )