# app/bot/handlers/help.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config.branding import BRAND

router = Router(name="help")


@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        f"{BRAND['name']} — HELP\n\n"
        "/start — main menu\n"
        "/catalog — browse sets\n"
        "/cart — your cart\n"
        "/purchases — your library\n"
        "/trust — how we verify\n"
        "/help — this message\n\n"
        f"Questions → {BRAND['support_handle']}"
    )