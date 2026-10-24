# app/bot/handlers/channel.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config.branding import BRAND

router = Router(name="channel")


@router.message(Command("channel"))
async def channel_cmd(message: Message):
    await message.answer(
        f"📡 {BRAND['channel_name']}\n"
        f"{BRAND['channel_url']}\n\n"
        "New drops posted there first."
    )