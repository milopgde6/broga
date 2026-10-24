# app/bot/states/admin_states.py
from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    uploading = State()
    upload_meta = State()
    editing_tags = State()
    editing_price = State()
    broadcasting = State()
    creating_promo = State()