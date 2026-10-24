# app/bot/filters/is_admin.py
"""Filter: only admins pass."""
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from config.settings import ADMIN_IDS


class IsAdmin(BaseFilter):
    async def __call__(self, event) -> bool:
        user = None
        if isinstance(event, Message):
            user = event.from_user
        elif isinstance(event, CallbackQuery):
            user = event.from_user
        if user is None:
            return False
        return user.id in ADMIN_IDS