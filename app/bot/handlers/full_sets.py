# app/bot/handlers/full_sets.py
from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.catalog.sets import featured
from app.bot.keyboards.catalog_kb import set_list_kb

router = Router(name="full_sets")


@router.callback_query(F.data == "full_sets")
async def full_sets_cb(cb: CallbackQuery):
    sets = featured(limit=50)
    if not sets:
        await cb.message.edit_text("No full sets yet.")
        return await cb.answer()
    await cb.message.edit_text(
        "🎞 FULL SETS\n\nComplete archives — nothing missing.",
        reply_markup=set_list_kb(sets, prefix="view"),
    )
    await cb.answer()