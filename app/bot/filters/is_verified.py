# app/bot/filters/is_verified.py
"""Filter: only verified users (has purchased at least once) pass."""
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from app.data.models import Entitlement
from app.data.db import SessionLocal


class IsVerified(BaseFilter):
    async def __call__(self, event) -> bool:
        user = getattr(event, "from_user", None)
        if user is None:
            return False
        with SessionLocal() as db:
            return (
                db.query(Entitlement)
                .filter(Entitlement.user_id == user.id)
                .first()
                is not None
            )