# app/shop/cart.py
from config.limits import MAX_CART_ITEMS

_carts = {}  # user_id -> [set_id, ...]   STUB: move to DB later

def add(user_id: int, set_id: int) -> bool:
    cart = _carts.setdefault(user_id, [])
    if set_id in cart:
        return False
    if len(cart) >= MAX_CART_ITEMS:
        return False
    cart.append(set_id)
    return True

def remove(user_id: int, set_id: int):
    _carts.get(user_id, []).remove(set_id) if set_id in _carts.get(user_id, []) else None

def items(user_id: int):
    return _carts.get(user_id, [])

def clear(user_id: int):
    _carts[user_id] = []