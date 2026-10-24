# app/bot/handlers/quality_filter.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as B

from app.catalog.quality import by_quality, QUALITIES
from app.bot.keyboards.catalog_kb import set_list_kb

router = Router(name="quality_filter")


def quality_kb():
    rows = [[B(text=q.upper(), callback_data=f"qual:{q}")] for q in QUALITIES]
    rows.append([B(text="⬅️ Back", callback_data="catalog")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


@router.callback_query(F.data == "quality")
async def quality_cb(cb: CallbackQuery):
    await cb.message.edit_text("🎚 FILTER BY QUALITY", reply_markup=quality_kb())
    await cb.answer()


@router.callback_query(F.data.startswith("qual:"))
async def qual_pick(cb: CallbackQuery):
    q = cb.data.split(":")[1]
    sets = by_quality(q)
    if not sets:
        await cb.message.edit_text(f"No {q.upper()} sets.")
        return await cb.answer()
    await cb.message.edit_text(
        f"🎚 {q.upper()}\n\n{len(sets)} set(s).",
        reply_markup=set_list_kb(sets, prefix="view"),
    )
    await cb.answer()