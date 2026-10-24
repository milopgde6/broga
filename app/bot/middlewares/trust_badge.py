# app/bot/middlewares/trust_badge.py
"""Injects a trust badge + verified flag into handler data for every update."""
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.data.models import Entitlement
from app.data.db import SessionLocal


class TrustBadgeMiddleware(BaseMiddleware):
    """Adds `is_verified` and `badge` to handler data so handlers don't re-query."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        verified = False
        if user:
            with SessionLocal() as db:
                verified = (
                    db.query(Entitlement)
                    .filter(Entitlement.user_id == user.id)
                    .first()
                    is not None
                )
        data["is_verified"] = verified
        data["badge"] = "🛡" if verified else ""
        return await handler(event, data)