# app/bot/handlers/search.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config.emoji_map import E
from app.catalog.search_index import search

router = Router()

class SearchState(StatesGroup):
    waiting = State()

@router.callback_query(F.data == "search")
async def ask_query(cb: CallbackQuery, state: FSMContext):
    await state.set_state(SearchState.waiting)
    await cb.message.edit_text(f"{E['search']} Send your search query:")
    await cb.answer()

@router.message(SearchState.waiting)
async def run_search(msg: Message, state: FSMContext):
    results = search(msg.text or "")
    await state.clear()
    rows = [[InlineKeyboardButton(text=f"{E['avail']} {s.title[:40]}",
             callback_data=f"set:{s.id}")] for s in results]
    rows.append([InlineKeyboardButton(text=f"{E['back']} Back", callback_data="menu")])
    await msg.answer(
        f"{E['search']} *{len(results)} results* for `{msg.text}`",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        parse_mode="Markdown")