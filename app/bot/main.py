import asyncio
import fcntl
import logging
import os
import tempfile

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramRetryAfter

from config.settings import BOT_TOKEN
from app.bot.dispatcher import build_dispatcher
from app.data.db import Base, engine
from app.payments.webhooks import start_webhook_server
from app.storage.layout import ensure_layout

log = logging.getLogger("theez.boot")


def _acquire_single_instance():
    path = os.getenv(
        "THEEZ_LOCK_FILE",
        os.path.join(tempfile.gettempdir(), "theez-bot.lock"),
    )
    fh = open(path, "w")
    try:
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        log.error("Another THEEZ instance is already running; exiting.")
        fh.close()
        raise SystemExit(1)
    fh.write(str(os.getpid()))
    fh.flush()
    return fh


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    lock = _acquire_single_instance()
    try:
        if not BOT_TOKEN:
            raise RuntimeError("BOT_TOKEN is required to start the bot")

        ensure_layout()
        Base.metadata.create_all(bind=engine)
        bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
        dp = build_dispatcher()

        try:
            webhook_runner = await start_webhook_server()
        except Exception:
            await bot.session.close()
            raise

        reconcile_task = None
        try:
            try:
                await bot.delete_webhook(drop_pending_updates=True)
            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after + 1)
                await bot.delete_webhook(drop_pending_updates=True)
            except Exception as e:
                log.warning("delete_webhook failed: %s", e)

            me = await bot.get_me()
            print(f"🧀 THEEZ up as @{me.username}")

            from app.payments.reconciliation import reconcile_loop

            reconcile_task = asyncio.create_task(
                reconcile_loop(), name="payment-reconciliation"
            )
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        finally:
            if reconcile_task is not None:
                reconcile_task.cancel()
                await asyncio.gather(reconcile_task, return_exceptions=True)
            await webhook_runner.cleanup()
            await bot.session.close()
    finally:
        lock.close()


if __name__ == "__main__":
    asyncio.run(main())
