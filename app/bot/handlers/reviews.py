# app/bot/handlers/reviews.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as B

from app.trust import reviews as rev
from app.access.entitlements import owns

router = Router(name="reviews")


def stars_kb(set_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [B(text=f"{'⭐️'*n} {n}", callback_data=f"rev:{set_id}:{n}") for n in (1, 2, 3)],
        [B(text=f"{'⭐️'*n} {n}", callback_data=f"rev:{set_id}:{n}") for n in (4, 5)],
    ])


@router.callback_query(F.data.startswith("reviews:"))
async def show_reviews(cb: CallbackQuery):
    set_id = int(cb.data.split(":")[1])
    rows = rev.for_set(set_id)
    avg = rev.avg_stars(set_id)
    if not rows:
        text = "⭐️ No reviews yet."
    else:
        text = f"⭐️ {avg}/5 ({len(rows)} reviews)\n\n"
        text += "\n".join(f"• {r.stars}⭐ {r.text[:60]}" for r in rows[:5])
    kb = None
    if owns(cb.from_user.id, set_id):
        kb = stars_kb(set_id)
    await cb.message.edit_text(text, reply_markup=kb)
    await cb.answer()


@router.callback_query(F.data.startswith("rev:"))
async def leave_review(cb: CallbackQuery, state):
    _, set_id, n = cb.data.split(":")
    set_id, n = int(set_id), int(n)
    if not owns(cb.from_user.id, set_id):
        await cb.answer("Buy first to review.", show_alert=True)
        return
    rev.add(cb.from_user.id, set_id, n)
    await cb.message.edit_text(f"Thanks! You rated {n}⭐")
    await cb.answer()