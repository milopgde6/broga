# app/payments/webhooks.py
"""HTTP receiver for payment rail callbacks. Idempotent."""
import asyncio
import hmac
import logging

from aiohttp import web

from app.payments.verify import mark_paid
from app.access.entitlements import grant
from config.settings import WEBHOOK_SECRET, WEBHOOK_HOST, WEBHOOK_PORT

log = logging.getLogger("theez.webhooks")


def _authorized(req: web.Request) -> bool:
    if not WEBHOOK_SECRET:
        return True
    got = req.headers.get("X-Theez-Secret", "")
    return hmac.compare_digest(got, WEBHOOK_SECRET)


async def _settle(ref: str, rail: str) -> bool:
    order = await asyncio.to_thread(mark_paid, ref, rail)
    if not order:
        return False
    await asyncio.to_thread(grant, order.user_id, order.set_id)
    return True


async def _handle(req: web.Request, rail: str) -> web.Response:
    if not _authorized(req):
        return web.json_response({"ok": False, "reason": "unauthorized"}, status=401)
    try:
        data = await req.json()
    except Exception:
        return web.json_response({"ok": False, "reason": "bad_json"}, status=400)
    ref = data.get("ref") or data.get("order_ref") or data.get("memo")
    if not ref:
        return web.json_response({"ok": False, "reason": "no_ref"}, status=400)
    ok = await _settle(ref, rail)
    log.info("webhook %s ref=%s ok=%s", rail, ref, ok)
    return web.json_response({"ok": ok}, status=200 if ok else 404)


async def shipstars(req): return await _handle(req, "shipstars")
async def usdt(req):      return await _handle(req, "usdt")
async def health(req):    return web.json_response({"ok": True})


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_post("/webhook/shipstars", shipstars)
    app.router.add_post("/webhook/usdt", usdt)
    app.router.add_get("/health", health)
    return app


async def run_webhook_server():
    runner = web.AppRunner(create_app())
    await runner.setup()
    site = web.TCPSite(runner, WEBHOOK_HOST, WEBHOOK_PORT)
    await site.start()
    log.info("webhooks listening on %s:%s", WEBHOOK_HOST, WEBHOOK_PORT)
    while True:
        await asyncio.sleep(3600)
