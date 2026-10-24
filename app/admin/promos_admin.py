# app/admin/promos_admin.py
"""Admin: create/toggle promo codes."""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from app.bot.filters.is_admin import IsAdmin
from app.shop.promos import CODES
from app.bot.states.admin_states import AdminStates

router = Router(name="admin_promos")
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.callback_query(F.data == "adm:promos")
async def promos_start(cb: CallbackQuery, state):
    await state.set_state(AdminStates.creating_promo)
    await cb.message.edit_text("🎟 Send: `CODE | pct`  (pct = 0.10 for 10% off)")
    await cb.answer()


@router.message(AdminStates.creating_promo)
async def promo_create(message: Message, state):
    text = (message.text or "").strip()
    if "|" not in text:
        await message.answer("Format: CODE | pct")
        return
    code, pct_s = text.split("|", 1)
    code = code.strip().upper()
    try:
        pct = float(pct_s.strip())
    except ValueError:
        await message.answer("pct must be float like 0.10")
        return
    CODES[code] = {"pct": pct, "active": True}
    await state.clear()
    await message.answer(f"✅ Promo {code} = {int(pct*100)}% off (active)")