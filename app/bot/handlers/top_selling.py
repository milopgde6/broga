# app/bot/handlers/top_selling.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import func

from app.data.models import Order, Set
from app.data.db import SessionLocal
from app.bot.keyboards.catalog_kb import set_list_kb

router = Router(name="top_selling")


@router.callback_query(F.data == "top")
async def top_selling_cb(cb: CallbackQuery):
    with SessionLocal() as db:
        rows = (
            db.query(Set)
            .join(Order, Order.set_id == Set.id)
            .filter(Order.status == "paid")
            .group_by(Set.id)
            .order_by(func.count(Order.id).desc())
            .limit(30)
            .all()
        )
    if not rows:
        await cb.message.edit_text("No sales yet.")
        return await cb.answer()
    await cb.message.edit_text(
        "🔥 TOP SELLING\n\nWhat everyone's buying.",
        reply_markup=set_list_kb(rows, prefix="view"),
    )
    await cb.answer()