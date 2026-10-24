# app/bot/keyboards/studio_kb.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as B
from app.catalog.studios import all_studios
from config.emoji_map import E


def studios_kb(page: int = 1, per_page: int = 8):
    studios = all_studios()
    start = (page - 1) * per_page
    chunk = studios[start:start + per_page]
    rows = [[B(text=s.name, callback_data=f"studio:{s.id}")] for s in chunk]
    nav = []
    if page > 1:
        nav.append(B(text="⬅️", callback_data=f"studio_page:{page-1}"))
    if start + per_page < len(studios):
        nav.append(B(text="➡️", callback_data=f"studio_page:{page+1}"))
    if nav:
        rows.append(nav)
    rows.append([B(text=f"{E['back']} Back", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)