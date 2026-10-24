# app/bot/handlers/rare.py
from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.catalog.sets import rare
from app.bot.keyboards.catalog_kb import set_list_kb

router = Router(name="rare")


@router.callback_query(F.data == "rare")
async def rare_cb(cb: CallbackQuery):
    sets = rare(limit=50)
    if not sets:
        await cb.message.edit_text("No rare sets yet.")
        return await cb.answer()
    await cb.message.edit_text(
        "💎 RARE\n\nHard to find. Grab them before they're gone.",
        reply_markup=set_list_kb(sets, prefix="view"),
    )
    await cb.answer()