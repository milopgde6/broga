# app/bot/handlers/browse_studio.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config.emoji_map import E
from app.data.models import Studio
from app.data.db import SessionLocal

router = Router()

@router.callback_query(F.data == "browse:studio")
async def list_studios(cb: CallbackQuery):
    db = SessionLocal()
    try:
        studios = db.query(Studio).limit(30).all()
    finally:
        db.close()

    rows = [[InlineKeyboardButton(f"{E['studio']} {s.name}",
             callback_data=f"studio:{s.name}")] for s in studios]
    rows.append([InlineKeyboardButton(f"{E['back']} Back", callback_data="menu")])
    await cb.message.edit_text(
        f"{E['studio']} *Studios*",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        parse_mode="Markdown")
    await cb.answer()