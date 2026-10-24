# app/bot/handlers/new_arrivals.py
from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.data.models import Set
from app.data.db import SessionLocal
from app.bot.keyboards.catalog_kb import set_list_kb

router = Router(name="new_arrivals")


@router.callback_query(F.data == "new")
async def new_arrivals_cb(cb: CallbackQuery):
    with SessionLocal() as db:
        sets = db.query(Set).order_by(Set.created_at.desc()).limit(30).all()
    if not sets:
        await cb.message.edit_text("No sets yet.")
        return await cb.answer()
    await cb.message.edit_text(
        "🆕 NEW ARRIVALS\n\nFresh in the archive.",
        reply_markup=set_list_kb(sets, prefix="view"),
    )
    await cb.answer()