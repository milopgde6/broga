# app/bot/handlers/browse_era.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config.emoji_map import E
from app.catalog.search_index import by_era

router = Router()

@router.callback_query(F.data == "browse:era")
async def list_eras(cb: CallbackQuery):
    eras = [str(y) for y in range(1995, 2015)]
    rows, row = [], []
    for e in eras:
        row.append(InlineKeyboardButton(text=e, callback_data=f"era:{e}"))
        if len(row) == 4:
            rows.append(row); row = []
    if row: rows.append(row)
    rows.append([InlineKeyboardButton(text=f"{E['back']} Back", callback_data="menu")])
    await cb.message.edit_text(
        f"{E['era']} *By Era*",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        parse_mode="Markdown")
    await cb.answer()