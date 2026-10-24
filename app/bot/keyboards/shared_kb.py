# app/bot/keyboards/shared_kb.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.emoji_map import E

def back_kb(target: str = "menu") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(f"{E['back']} Back", callback_data=target)]
    ])

def set_card_kb(set_id: int, owned: bool) -> InlineKeyboardMarkup:
    rows = []
    if owned:
        rows.append([InlineKeyboardButton(f"{E['owned']} Owned · Open", callback_data=f"open:{set_id}")])
    else:
        rows.append([
            InlineKeyboardButton(f"{E['cart']} Add", callback_data=f"cart:add:{set_id}"),
            InlineKeyboardButton(f"{E['credits']} Buy", callback_data=f"buy:{set_id}"),
        ])
    rows.append([InlineKeyboardButton(f"{E['back']} Back", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)