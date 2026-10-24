# app/bot/dispatcher.py
import asyncio
import logging

from aiogram import Dispatcher
from aiogram.exceptions import (
    TelegramRetryAfter, TelegramConflictError, TelegramForbiddenError,
)

from app.bot.middlewares.auth import AuthMiddleware
from app.bot.middlewares.rate_limit import RateLimitMiddleware

from app.bot.handlers import (
    start, menu, browse_age, browse_studio, browse_era, browse_ethnicity,
    search, tag_search, trust, purchase, library, credits, admin, provenance,
    new_arrivals, top_selling, quality_filter, promos,
    featured, full_sets, rare, refer,
)
from app.admin import upload as admin_upload, manifest_admin

log = logging.getLogger("theez.errors")


def build_dispatcher() -> Dispatcher:
    dp = Dispatcher()

    @dp.error()
    async def on_error(event):
        exc = event.exception
        if isinstance(exc, TelegramRetryAfter):
            log.warning("floodwait %ss — backing off", exc.retry_after)
            await asyncio.sleep(exc.retry_after + 1)
        elif isinstance(exc, TelegramConflictError):
            log.warning("409 conflict — another instance was polling")
        elif isinstance(exc, TelegramForbiddenError):
            log.info("user blocked the bot")
        else:
            log.exception("unhandled", exc_info=exc)

    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())
    dp.message.middleware(RateLimitMiddleware())
    dp.callback_query.middleware(RateLimitMiddleware())

    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(browse_age.router)
    dp.include_router(browse_studio.router)
    dp.include_router(browse_era.router)
    dp.include_router(browse_ethnicity.router)
    dp.include_router(search.router)
    dp.include_router(tag_search.router)
    dp.include_router(trust.router)
    dp.include_router(purchase.router)
    dp.include_router(library.router)
    dp.include_router(credits.router)
    dp.include_router(admin.router)
    dp.include_router(admin_upload.router)
    dp.include_router(manifest_admin.router)
    dp.include_router(provenance.router)
    dp.include_router(new_arrivals.router)
    dp.include_router(top_selling.router)
    dp.include_router(quality_filter.router)
    dp.include_router(promos.router)
    dp.include_router(featured.router)
    dp.include_router(full_sets.router)
    dp.include_router(rare.router)
    dp.include_router(refer.router)

    return dp