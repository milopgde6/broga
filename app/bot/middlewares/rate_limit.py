# app/bot/middlewares/rate_limit.py
import time
from collections import defaultdict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Any

_hits: dict[int, list[float]] = defaultdict(list)
WINDOW = 2.0
MAX = 8

class RateLimitMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict) -> Any:
        user = data.get("event_from_user")
        if user:
            now = time.time()
            hits = [t for t in _hits[user.id] if now - t < WINDOW]
            if len(hits) >= MAX:
                return None
            hits.append(now)
            _hits[user.id] = hits
        return await handler(event, data)