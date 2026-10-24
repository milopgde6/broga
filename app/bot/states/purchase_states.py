# app/bot/states/purchase_states.py
from aiogram.fsm.state import State, StatesGroup


class PurchaseStates(StatesGroup):
    choosing_set = State()
    confirming = State()
    choosing_rail = State()
    awaiting_payment = State()
    applying_code = State()