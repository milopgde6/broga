# app/bot/states/search_states.py
from aiogram.fsm.state import State, StatesGroup


class SearchStates(StatesGroup):
    typing_query = State()
    filtering = State()