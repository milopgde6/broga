# app/bot/handlers/refer.py
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

router = Router(name="refer")


async def _send_refer(message: Message, user_id: int):
    me = await message.bot.get_me()
    link = f"https://t.me/{me.username}?start=ref_{user_id}"
    await message.answer(
        "🎁 REFER A FRIEND\n\n"
        "Share your link. When they buy, you get store credit.\n\n"
        f"Your link:\n{link}"
    )


@router.message(Command("refer"))
async def refer_cmd(message: Message):
    await _send_refer(message, message.from_user.id)


@router.callback_query(F.data == "refer")
async def refer_cb(cb: CallbackQuery):
    await _send_refer(cb.message, cb.from_user.id)
    await cb.answer()
