# app/bot/keyboards/purchase_kb.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as B
from config.emoji_map import E


def confirm_kb(set_id: int, price: float):
    return InlineKeyboardMarkup(inline_keyboard=[
        [B(text=f"✅ Confirm ${price:.2f}", callback_data=f"confirm:{set_id}")],
        [B(text="🎟 Apply code", callback_data=f"code:{set_id}")],
        [B(text=f"{E['back']} Back", callback_data=f"view:{set_id}")],
    ])


def rail_kb(set_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [B(text="⭐️ ShipStars", callback_data=f"rail:shipstars:{set_id}")],
        [B(text="💵 USDT (TRC20)", callback_data=f"rail:usdt:{set_id}")],
        [B(text="🪙 Credits", callback_data=f"rail:credits:{set_id}")],
        [B(text=f"{E['back']} Back", callback_data=f"buy:{set_id}")],
    ])


def awaiting_kb(set_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [B(text="🔄 Check payment", callback_data=f"checkpay:{set_id}")],
        [B(text="❌ Cancel", callback_data=f"cancelpay:{set_id}")],
    ])