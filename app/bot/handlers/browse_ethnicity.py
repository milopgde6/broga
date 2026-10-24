# app/bot/handlers/browse_ethnicity.py
from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.data.models import Set, Girl
from app.data.db import SessionLocal
from app.bot.keyboards.ethnicity_kb import ethnicity_kb
from app.bot.keyboards.catalog_kb import set_list_kb

router = Router(name="browse_ethnicity")


@router.callback_query(F.data == "browse:ethnicity")
async def browse_eth_cb(cb: CallbackQuery):
    await cb.message.edit_text("🌏 BROWSE BY ETHNICITY", reply_markup=ethnicity_kb())
    await cb.answer()


@router.callback_query(F.data.startswith("eth:"))
async def eth_pick(cb: CallbackQuery):
    eth = cb.data.split(":")[1]
    with SessionLocal() as db:
        sets = (
            db.query(Set).join(Girl)
            .filter(Girl.ethnicity == eth)
            .limit(50).all()
        )
    if not sets:
        await cb.message.edit_text(f"No sets for {eth}.")
        return await cb.answer()
    await cb.message.edit_text(
        f"🌏 {eth.upper()}\n\n{len(sets)} set(s).",
        reply_markup=set_list_kb(sets, prefix="view"),
    )
    await cb.answer()