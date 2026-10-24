# app/admin/pricing.py
"""Admin: change a set's price."""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from app.bot.filters.is_admin import IsAdmin
from app.data.models import Set
from app.data.db import SessionLocal
from app.bot.states.admin_states import AdminStates

router = Router(name="admin_pricing")
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.callback_query(F.data == "adm:pricing")
async def pricing_start(cb: CallbackQuery, state):
    await state.set_state(AdminStates.editing_price)
    await cb.message.edit_text("💲 Send: `set_id | new_price`")
    await cb.answer()


@router.message(AdminStates.editing_price)
async def pricing_apply(message: Message, state):
    text = (message.text or "").strip()
    if "|" not in text:
        await message.answer("Format: set_id | price")
        return
    sid_s, price_s = text.split("|", 1)
    try:
        sid = int(sid_s.strip())
        price = float(price_s.strip())
    except ValueError:
        await message.answer("Bad numbers")
        return
    with SessionLocal() as db:
        s = db.query(Set).get(sid)
        if not s:
            await message.answer("Set not found")
            return
        old = s.price
        s.price = price
        db.commit()
    await state.clear()
    await message.answer(f"✅ #{sid} price: ${old:.2f} → ${price:.2f}")