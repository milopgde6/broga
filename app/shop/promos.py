# app/shop/promos.py
# STUB: promo codes — move to DB for real use
CODES = {
    "THEEZ10": {"pct": 0.10, "active": True},
    "WELCOME": {"pct": 0.05, "active": True},
}

def apply(code: str, amount: float) -> float:
    c = CODES.get(code.upper())
    if not c or not c["active"]:
        return amount
    return round(amount * (1 - c["pct"]), 2)