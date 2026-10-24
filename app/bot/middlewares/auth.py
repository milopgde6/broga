# app/bot/middlewares/auth.py
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Awaitable, Any
from app.data.models import User
from app.data.db import SessionLocal

class AuthMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict) -> Any:
        user = data.get("event_from_user")
        if user:
            db = SessionLocal()
            try:
                u = db.query(User).filter_by(tg_id=user.id).first()
                if not u:
                    u = User(tg_id=user.id, username=user.username)
                    db.add(u); db.commit()
                data["db_user"] = u
            finally:
                db.close()
        return await handler(event, data)