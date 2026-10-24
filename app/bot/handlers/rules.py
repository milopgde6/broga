# app/bot/handlers/rules.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name="rules")


@router.message(Command("rules"))
async def rules_cmd(message: Message):
    await message.answer(
        "📖 RULES\n\n"
        "1. Pay via the listed rails only.\n"
        "2. Keep your order ref — it's your receipt.\n"
        "3. No refunds after delivery unless the file is corrupt.\n"
        "4. Don't reshare purchased sets publicly.\n"
        "5. Report scams with a screenshot."
    )