# app/bot/handlers/admin.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config.settings import ADMIN_IDS
from config.emoji_map import E
from app.bot.keyboards.shared_kb import back_kb

router = Router()

def is_admin(tg_id: int) -> bool:
    return tg_id in ADMIN_IDS

@router.callback_query(F.data == "admin")
async def show_admin(cb: CallbackQuery):
    if not is_admin(cb.from_user.id):
        await cb.message.edit_text(
            f"{E['admin']} *Support*\n\nPing the admin for help.",
            reply_markup=back_kb(), parse_mode="Markdown")
        await cb.answer(); return

    rows = [
        [InlineKeyboardButton("📤 Upload set", callback_data="adm:upload")],
        [InlineKeyboardButton("🏷 Edit tags", callback_data="adm:tags")],
        [InlineKeyboardButton("💰 Pricing", callback_data="adm:pricing")],
        [InlineKeyboardButton("👥 Users", callback_data="adm:users")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="adm:broadcast")],
        [InlineKeyboardButton("📊 Stats", callback_data="adm:stats")],
        [InlineKeyboardButton("🧾 Manifest", callback_data="adm:manifest")],
        [InlineKeyboardButton(f"{E['back']} Menu", callback_data="menu")],
    ]
    await cb.message.edit_text(
        f"{E['admin']} *Admin panel*",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        parse_mode="Markdown")
    await cb.answer()