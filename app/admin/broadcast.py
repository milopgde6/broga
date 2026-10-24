# app/admin/broadcast.py
"""Admin: broadcast a message to all users."""
import asyncio
from aiogram import Router, F
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from aiogram.types import CallbackQuery, Message

from app.bot.filters.is_admin import IsAdmin
from app.data.models import User
from app.data.db import SessionLocal
from app.bot.states.admin_states import AdminStates

router = Router(name="admin_broadcast")
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.callback_query(F.data == "adm:broadcast")
async def broadcast_start(cb: CallbackQuery, state):
    await state.set_state(AdminStates.broadcasting)
    await cb.message.edit_text("📣 Send the message to broadcast.")
    await cb.answer()


@router.message(AdminStates.broadcasting)
async def broadcast_send(message: Message, state):
    with SessionLocal() as db:
        ids = [u.tg_id for u in db.query(User).all()]
    await state.clear()
    sent, failed = 0, 0
    for uid in ids:
        try:
            await message.bot.send_message(uid, message.text or message.caption or "")
            sent += 1
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after + 1)
            failed += 1
        except TelegramForbiddenError:
            failed += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)  # ~20/s, under Telegram limits
    await message.answer(f"📣 Done. sent={sent} failed={failed}")