# app/bot/keyboards/catalog_kb.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as B
from config.emoji_map import E


def set_card_kb(set_id: int, owned: bool = False, in_cart: bool = False):
    rows = []
    if owned:
        rows.append([B(text=f"{E['owned']} Open", callback_data=f"open:{set_id}")])
    elif in_cart:
        rows.append([B(text=f"{E['cart']} In cart", callback_data=f"uncart:{set_id}")])
    else:
        rows.append([
            B(text=f"{E['cart']} Add", callback_data=f"cart:{set_id}"),
            B(text=f"{E['purchases']} Buy", callback_data=f"buy:{set_id}"),
        ])
    rows.append([
        B(text=f"{E['sources']} Source", callback_data=f"src:{set_id}"),
        B(text=f"{E['trust']} Proof", callback_data=f"proof:{set_id}"),
    ])
    rows.append([B(text=f"{E['back']} Back", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def set_list_kb(sets, page: int = 1, per_page: int = 5, prefix: str = "view"):
    start = (page - 1) * per_page
    chunk = sets[start:start + per_page]
    rows = [[B(text=s.title, callback_data=f"{prefix}:{s.id}")] for s in chunk]
    nav = []
    if page > 1:
        nav.append(B(text="⬅️", callback_data=f"{prefix}_page:{page-1}"))
    if start + per_page < len(sets):
        nav.append(B(text="➡️", callback_data=f"{prefix}_page:{page+1}"))
    if nav:
        rows.append(nav)
    rows.append([B(text=f"{E['back']} Back", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)