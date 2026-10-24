# app/bot/handlers/cart.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

from app.shop import cart as cart_mod
from app.shop.pricing import set_price
from app.data.models import Set
from app.data.db import SessionLocal
from app.bot.keyboards.cart_kb import cart_kb, empty_cart_kb

router = Router(name="cart")


def _render(user_id: int):
    ids = cart_mod.items(user_id)
    if not ids:
        return "🛒 Your cart is empty.", empty_cart_kb()
    with SessionLocal() as db:
        rows = []
        for sid in ids:
            s = db.query(Set).get(sid)
            if s:
                rows.append((s.id, s.title, s.price))
    total = sum(r[2] for r in rows)
    text = "🛒 CART\n\n" + "\n".join(f"• {t} — ${p:.2f}" for _, t, p in rows)
    text += f"\n\nTotal: ${total:.2f}"
    return text, cart_kb(rows)


@router.message(Command("cart"))
async def cart_cmd(message: Message):
    text, kb = _render(message.from_user.id)
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == "cart_show")
async def cart_show(cb: CallbackQuery):
    text, kb = _render(cb.from_user.id)
    await cb.message.edit_text(text, reply_markup=kb)
    await cb.answer()


@router.callback_query(F.data.startswith("uncart:"))
async def uncart(cb: CallbackQuery):
    sid = int(cb.data.split(":")[1])
    cart_mod.remove(cb.from_user.id, sid)
    text, kb = _render(cb.from_user.id)
    await cb.message.edit_text(text, reply_markup=kb)
    await cb.answer("Removed")


@router.callback_query(F.data == "cart_clear")
async def cart_clear(cb: CallbackQuery):
    cart_mod.clear(cb.from_user.id)
    text, kb = _render(cb.from_user.id)
    await cb.message.edit_text(text, reply_markup=kb)
    await cb.answer("Cleared")