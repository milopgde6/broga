# app/bot/handlers/browse_age.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from config.age_bands import AGE_BANDS
from config.emoji_map import E
from app.catalog.search_index import by_age
from app.bot.keyboards.age_kb import age_bands_kb

router = Router()

@router.callback_query(F.data == "browse:age")
async def list_age_bands(cb: CallbackQuery):
    await cb.message.edit_text(
        f"{E['age']} *By Age*",
        reply_markup=age_bands_kb(),
        parse_mode="Markdown")
    await cb.answer()


@router.callback_query(F.data.startswith("age:"))
async def show_age(cb: CallbackQuery):
    band = cb.data.split(":", 1)[1]
    lo, hi = AGE_BANDS.get(band, (0, 99))
    sets = by_age(lo, hi)

    rows = []
    for s in sets[:20]:
        label = f"{E['avail']} {s.title[:40]}"
        rows.append([InlineKeyboardButton(label, callback_data=f"set:{s.id}")])
    rows.append([InlineKeyboardButton(f"{E['back']} Back", callback_data="menu")])

    text = f"{E['age']} *Age {band}* — {len(sets)} sets"
    await cb.message.edit_text(
        text, reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        parse_mode="Markdown")
    await cb.answer()