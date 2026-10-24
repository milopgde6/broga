# app/trust/order_log.py
"""Public-facing order log. Buyers see recent sales as social proof."""
from datetime import datetime, timedelta
from typing import List

from app.data.models import Order, User, Set
from app.data.db import SessionLocal


def recent(limit: int = 10) -> List[dict]:
    """Last N paid orders, anonymized for public display."""
    with SessionLocal() as db:
        rows = (
            db.query(Order)
            .filter(Order.status == "paid")
            .order_by(Order.created_at.desc())
            .limit(limit)
            .all()
        )
        out = []
        for o in rows:
            user = db.query(User).get(o.user_id)
            s = db.query(Set).get(o.set_id)
            handle = user.username if user and user.username else f"user{o.user_id}"
            out.append({
                "handle": handle,
                "set_title": s.title if s else "—",
                "amount": o.amount,
                "rail": o.rail,
                "when": o.created_at,
            })
        return out


def log_line(limit: int = 5) -> str:
    """Compact text block for the trust page."""
    rows = recent(limit)
    if not rows:
        return "🧾 No sales yet — be the first."
    lines = ["🧾 RECENT SALES"]
    for r in rows:
        lines.append(f"• {r['handle']} bought {r['set_title']} ({r['rail']})")
    return "\n".join(lines)


def sales_last_24h() -> int:
    cutoff = datetime.utcnow() - timedelta(hours=24)
    with SessionLocal() as db:
        return (
            db.query(Order)
            .filter(Order.status == "paid", Order.created_at >= cutoff)
            .count()
        )