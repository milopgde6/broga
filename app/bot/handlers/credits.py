# app/bot/handlers/credits.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config.emoji_map import E
from app.shop import credits as credit_svc
from app.shop.pricing import CREDIT_PACKS

router = Router()

@router.callback_query(F.data == "credits")
async def show_credits(cb: CallbackQuery):
    bal = credit_svc.balance(cb.from_user.id)
    rows = []
    for pid, pack in CREDIT_PACKS.items():
        rows.append([InlineKeyboardButton(
            f"{E['credits']} {pack['credits']} credits — ${pack['price_usd']}",
            callback_data=f"topup:{pid}")])
    rows.append([InlineKeyboardButton(f"{E['back']} Menu", callback_data="menu")])
    await cb.message.edit_text(
        f"{E['credits']} *Balance:* {bal} credits\n\nChoose a top-up:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        parse_mode="Markdown")
    await cb.answer()

@router.callback_query(F.data.startswith("topup:"))
async def topup(cb: CallbackQuery):
    pid = cb.data.split(":")[1]
    pack = CREDIT_PACKS.get(pid)
    if not pack:
        await cb.answer("Unknown pack"); return
    rows = [
        [InlineKeyboardButton(f"{E['credits']} USDT (TRC20)", callback_data=f"pay:usdt:{pid}")],
        [InlineKeyboardButton(f"⭐ ShipStars", callback_data=f"pay:stars:{pid}")],
        [InlineKeyboardButton(f"{E['back']} Back", callback_data="credits")],
    ]
    await cb.message.edit_text(
        f"{E['credits']} *{pack['credits']} credits* — ${pack['price_usd']}\n\nChoose payment rail:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        parse_mode="Markdown")
    await cb.answer()