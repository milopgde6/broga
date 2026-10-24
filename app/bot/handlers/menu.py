# app/bot/handlers/menu.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from config.branding import BRAND
from app.bot.keyboards.main_menu import main_menu_kb

router = Router()

@router.callback_query(F.data == "menu")
async def show_menu(cb: CallbackQuery):
    header = BRAND["header"].format(sets=0, clips=0)
    text = (
        f"{BRAND['emoji']} *{BRAND['name']}*\n"
        f"_{BRAND['tagline']}_\n\n"
        f"{header}"
    )
    await cb.message.edit_text(text, reply_markup=main_menu_kb(), parse_mode="Markdown")
    await cb.answer()


@router.callback_query(F.data == "browse")
async def show_browse(cb: CallbackQuery):
    await show_menu(cb)