# app/bot/handlers/tag_search.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from app.catalog.search_index import search
from app.bot.keyboards.catalog_kb import set_list_kb
from app.bot.states.search_states import SearchStates

router = Router(name="tag_search")


@router.callback_query(F.data == "tags")
async def search_cb(cb: CallbackQuery, state):
    await state.set_state(SearchStates.typing_query)
    await cb.message.edit_text("🔎 Type a search — title, girl, or studio.")
    await cb.answer()


@router.message(SearchStates.typing_query)
async def search_run(message: Message, state):
    q = (message.text or "").strip()
    if not q:
        await message.answer("Empty query. Try again.")
        return
    results = search(q, limit=30)
    await state.clear()
    if not results:
        await message.answer(f"🔎 No matches for '{q}'.")
        return
    await message.answer(
        f"🔎 {len(results)} result(s) for '{q}'.",
        reply_markup=set_list_kb(results, prefix="view"),
    )