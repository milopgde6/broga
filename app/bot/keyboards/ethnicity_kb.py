# app/bot/keyboards/ethnicity_kb.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as B
from config.emoji_map import E

ETHNICITIES = ["asian", "euro", "latina", "mixed", "other"]


def ethnicity_kb():
    rows, row = [], []
    for eth in ETHNICITIES:
        row.append(B(text=eth.title(), callback_data=f"eth:{eth}"))
        if len(row) == 2:
            rows.append(row); row = []
    if row:
        rows.append(row)
    rows.append([B(text=f"{E['back']} Back", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)