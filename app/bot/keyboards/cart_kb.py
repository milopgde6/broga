# app/bot/keyboards/cart_kb.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as B
from config.emoji_map import E


def cart_kb(items: list):
    """items = list of (set_id, title, price)."""
    rows = []
    for set_id, title, price in items:
        rows.append([
            B(text=f"❌ {title} (${price:.2f})", callback_data=f"uncart:{set_id}"),
        ])
    if items:
        rows.append([B(text=f"{E['purchases']} Checkout", callback_data="checkout")])
        rows.append([B(text="🗑 Clear cart", callback_data="cart_clear")])
    rows.append([B(text=f"{E['back']} Back", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def empty_cart_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [B(text=f"{E['catalog']} Browse catalog", callback_data="catalog")],
        [B(text=f"{E['back']} Back", callback_data="menu")],
    ])