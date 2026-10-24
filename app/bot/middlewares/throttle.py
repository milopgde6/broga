# app/bot/middlewares/throttle.py
"""Per-user rate limiter. Drops updates that exceed the limit."""
import time
from collections import defaultdict
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from config.limits import RATE_LIMIT_PER_MIN


class ThrottleMiddleware(BaseMiddleware):
    def __init__(self, per_min: int = RATE_LIMIT_PER_MIN):
        self.per_min = per_min
        self._hits: Dict[int, list] = defaultdict(list)

    def _allowed(self, user_id: int) -> bool:
        now = time.time()
        window = self._hits[user_id]
        # drop hits older than 60s
        cutoff = now - 60
        while window and window[0] < cutoff:
            window.pop(0)
        if len(window) >= self.per_min:
            return False
        window.append(now)
        return True

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user and not self._allowed(user.id):
            # silently drop — Telegram will retry, or user just waits
            return None
        return await handler(event, data)