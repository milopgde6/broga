# app/bot/handlers/promos.py
from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.shop.promos import CODES

router = Router(name="promos")


@router.callback_query(F.data == "codes")
async def promos_cb(cb: CallbackQuery):
    active = [c for c, v in CODES.items() if v.get("active")]
    if not active:
        await cb.message.edit_text("🎟 No active promos.")
        return await cb.answer()
    lines = ["🎟 ACTIVE PROMOS", ""]
    for c in active:
        lines.append(f"• {c} — {int(CODES[c]['pct']*100)}% off")
    await cb.message.edit_text("\n".join(lines))
    await cb.answer()