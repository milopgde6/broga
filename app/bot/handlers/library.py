# app/bot/handlers/library.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config.emoji_map import E
from app.access.entitlements import owned_set_ids
from app.data.models import Set
from app.data.db import SessionLocal

router = Router()

@router.callback_query(F.data == "library")
async def show_library(cb: CallbackQuery):
    ids = owned_set_ids(cb.from_user.id)
    if not ids:
        await cb.message.edit_text(
            f"{E['library']} *Your library is empty.*",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f"{E['browse']} Browse", callback_data="browse")],
                [InlineKeyboardButton(text=f"{E['back']} Menu", callback_data="menu")],
            ]), parse_mode="Markdown")
        await cb.answer(); return

    db = SessionLocal()
    try:
        sets = db.query(Set).filter(Set.id.in_(ids)).all()
    finally:
        db.close()

    rows = [[InlineKeyboardButton(text=f"{E['owned']} {s.title[:40]}",
             callback_data=f"open:{s.id}")] for s in sets]
    rows.append([InlineKeyboardButton(text=f"{E['back']} Menu", callback_data="menu")])
    await cb.message.edit_text(
        f"{E['library']} *Your Library* — {len(sets)} sets",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        parse_mode="Markdown")
    await cb.answer()