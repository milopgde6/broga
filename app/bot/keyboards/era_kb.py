# app/bot/keyboards/era_kb.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as B
from app.catalog.eras import all_eras
from config.emoji_map import E


def eras_kb():
    eras = all_eras()
    rows, row = [], []
    for era in eras:
        row.append(B(text=era, callback_data=f"era:{era}"))
        if len(row) == 3:
            rows.append(row); row = []
    if row:
        rows.append(row)
    rows.append([B(text=f"{E['back']} Back", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)