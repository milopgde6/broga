# app/bot/handlers/purchase.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config.emoji_map import E
from app.data.models import Set
from app.data.db import SessionLocal
from app.shop.pricing import set_price_credits
from app.shop import credits as credit_svc
from app.shop import orders as order_svc
from app.access.entitlements import grant, owns

router = Router()


@router.callback_query(F.data == "purchases")
async def purchases_cb(cb: CallbackQuery):
    rows = order_svc.for_user(cb.from_user.id)
    if not rows:
        text = f"{E['purchases']} No purchases yet."
    else:
        lines = [f"{E['purchases']} *Purchases*", ""]
        for o in rows[:20]:
            lines.append(f"`{o.ref}` — ${o.amount:.2f} — {o.status}")
        text = "\n".join(lines)
    await cb.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(f"{E['back']} Menu", callback_data="menu")],
        ]),
        parse_mode="Markdown",
    )
    await cb.answer()


@router.callback_query(F.data.startswith("buy:"))
async def buy_set(cb: CallbackQuery):
    set_id = int(cb.data.split(":")[1])
    db = SessionLocal()
    try:
        s = db.query(Set).get(set_id)
        if not s:
            await cb.answer("Set not found"); return
        price = set_price_credits(s)
        title = s.title
    finally:
        db.close()

    user_id = cb.from_user.id
    if owns(user_id, set_id):
        await cb.answer("Already owned")
        return

    bal = credit_svc.balance(user_id)
    if bal >= price:
        credit_svc.spend(user_id, price)
        grant(user_id, set_id)
        await cb.message.edit_text(
            f"{E['owned']} *Unlocked:* {title}\n{E['credits']} −{price} credits",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(f"{E['library']} Open Library", callback_data="library")],
                [InlineKeyboardButton(f"{E['back']} Menu", callback_data="menu")],
            ]), parse_mode="Markdown")
    else:
        short = price - bal
        await cb.message.edit_text(
            f"{E['credits']} *Need {short} more credits*\n\n"
            f"Set: {title}\nPrice: {price} credits\nBalance: {bal}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(f"{E['credits']} Top up", callback_data="credits")],
                [InlineKeyboardButton(f"{E['back']} Back", callback_data="menu")],
            ]), parse_mode="Markdown")
    await cb.answer()