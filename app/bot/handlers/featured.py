# app/bot/handlers/featured.py
from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.catalog.sets import featured
from app.bot.keyboards.catalog_kb import set_list_kb

router = Router(name="featured")


@router.callback_query(F.data == "featured")
async def featured_cb(cb: CallbackQuery):
    sets = featured(limit=20)
    if not sets:
        await cb.message.edit_text("No featured sets yet.")
        return await cb.answer()
    await cb.message.edit_text(
        "⭐️ FEATURED\n\nHand-picked full sets.",
        reply_markup=set_list_kb(sets, prefix="view"),
    )
    await cb.answer()