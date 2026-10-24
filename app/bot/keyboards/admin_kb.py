# app/bot/keyboards/admin_kb.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as B


def admin_home_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [B(text="📤 Upload set", callback_data="adm:upload")],
        [B(text="🏷 Tag editor", callback_data="adm:tags")],
        [B(text="💲 Pricing", callback_data="adm:pricing")],
        [B(text="🎟 Promos", callback_data="adm:promos")],
        [B(text="⭐️ Reviews mod", callback_data="adm:reviews")],
        [B(text="📣 Broadcast", callback_data="adm:broadcast")],
        [B(text="📊 Stats", callback_data="adm:stats")],
        [B(text="👥 Users", callback_data="adm:users")],
        [B(text="💾 Backups", callback_data="adm:backups")],
        [B(text="📜 Manifest admin", callback_data="adm:manifest")],
    ])


def confirm_kb(action: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [B(text="✅ Yes", callback_data=f"adm_ok:{action}"),
         B(text="❌ No", callback_data="adm:home")],
    ])