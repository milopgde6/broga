# app/shop/wallet.py
from app.shop import credits

def topup(user_id: int, amount: int):
    credits.add(user_id, amount)

def pay(user_id: int, amount: int) -> bool:
    return credits.spend(user_id, amount)