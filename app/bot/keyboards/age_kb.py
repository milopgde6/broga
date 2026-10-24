# app/bot/keyboards/age_kb.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as B
from config.age_bands import AGE_BANDS
from config.emoji_map import E


def age_bands_kb():
    rows, row = [], []
    for band in AGE_BANDS:
        row.append(B(text=band, callback_data=f"age:{band}"))
        if len(row) == 2:
            rows.append(row); row = []
    if row:
        rows.append(row)
    rows.append([B(text=f"{E['back']} Back", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)