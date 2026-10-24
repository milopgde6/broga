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


import asyncio
import logging
import aiohttp

from app.shop import orders
from app.payments.webhooks import _settle
from config.settings import USDT_WATCHER_URL, USDT_TRC20_ADDR

log = logging.getLogger("theez.reconcile")


async def _rail_says_paid(rail: str, ref: str) -> bool:
    if rail == "usdt" and USDT_WATCHER_URL:
        url = f"{USDT_WATCHER_URL}?address={USDT_TRC20_ADDR}&ref={ref}"
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(url, timeout=10) as r:
                    data = await r.json()
                    return bool(data.get("paid"))
        except Exception as e:
            log.warning("usdt watcher error: %s", e)
    return False  # shipstars settles via webhook


async def reconcile_once():
    for o in orders.pending_for_user_all() if hasattr(orders, "pending_for_user_all") else []:
        if await _rail_says_paid(o.rail, o.ref):
            await _settle(o.ref, o.rail)


async def reconcile_loop(interval: int = 300):
    while True:
        try:
            await reconcile_once()
        except Exception:
            log.exception("reconcile failed")
        await asyncio.sleep(interval)
