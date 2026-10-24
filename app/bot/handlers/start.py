# app/bot/handlers/start.py
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from config.branding import BRAND
from app.bot.keyboards.main_menu import main_menu_kb
from app.data.models import User
from app.data.db import SessionLocal

router = Router()

@router.message(CommandStart())
async def cmd_start(msg: Message):
    db = SessionLocal()
    try:
        u = db.query(User).filter_by(tg_id=msg.from_user.id).first()
        if not u:
            u = User(tg_id=msg.from_user.id, username=msg.from_user.username)
            db.add(u)
            db.commit()
    finally:
        db.close()

    header = BRAND["header"].format(sets=0, clips=0)
    text = (
        f"{BRAND['emoji']} *{BRAND['name']}*\n"
        f"_{BRAND['tagline']}_\n\n"
        f"{header}"
    )
    await msg.answer(text, reply_markup=main_menu_kb(), parse_mode="Markdown")