# app/bot/middlewares/logging.py
"""Structured logging middleware for every update."""
import logging
import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

log = logging.getLogger("theez.updates")


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        uid = user.id if user else "?"
        uname = user.username if user else "?"
        start = time.perf_counter()
        try:
            result = await handler(event, data)
            return result
        except Exception:
            log.exception("handler error | user=%s(%s)", uid, uname)
            raise
        finally:
            ms = (time.perf_counter() - start) * 1000
            log.info("update | user=%s(%s) | %.1fms", uid, uname, ms)