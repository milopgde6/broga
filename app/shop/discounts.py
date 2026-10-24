# app/shop/discounts.py
def bundle_discount(pct: float, amount: float) -> float:
    return round(amount * (1 - pct), 2)

def stack(*amounts) -> float:
    """Apply sequential discounts."""
    total = amounts[0]
    for pct in amounts[1:]:
        total = round(total * (1 - pct), 2)
    return total