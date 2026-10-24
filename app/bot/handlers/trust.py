# app/bot/handlers/trust.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from config.emoji_map import E
from app.bot.keyboards.shared_kb import back_kb

router = Router()

TRUST_TEXT = (
    f"{E['trust']} *TRUST & PROVENANCE*\n\n"
    f"Every set on THEEZ is hash-matched against a master archive.\n\n"
    f"• {E['sources']} Source logged per set\n"
    f"• {E['trust']} SHA-256 manifest published\n"
    f"• {E['how']} Instant delivery, no waiting\n"
    f"• {E['owned']} You only see what you own\n\n"
    f"Scammers copy the menu. They can't copy the paper trail."
)

@router.callback_query(F.data == "trust")
async def show_trust(cb: CallbackQuery):
    await cb.message.edit_text(TRUST_TEXT, reply_markup=back_kb(), parse_mode="Markdown")
    await cb.answer()

@router.callback_query(F.data == "sources")
async def show_sources(cb: CallbackQuery):
    await cb.message.edit_text(
        f"{E['sources']} *SOURCES*\n\nEvery set links to its origin studio + era. Full provenance on request.",
        reply_markup=back_kb(), parse_mode="Markdown")
    await cb.answer()

@router.callback_query(F.data == "how")
async def show_how(cb: CallbackQuery):
    await cb.message.edit_text(
        f"{E['how']} *HOW IT WORKS*\n\n1. Pick a set\n2. Pay (USDT or Stars)\n3. Access unlocks instantly\n4. Stream or download — forever.",
        reply_markup=back_kb(), parse_mode="Markdown")
    await cb.answer()