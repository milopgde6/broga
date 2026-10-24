# app/shop/pricing.py
CREDIT_PACKS = {
    "p100":  {"credits": 100,  "price_usd": 5},
    "p300":  {"credits": 300,  "price_usd": 13},
    "p700":  {"credits": 700,  "price_usd": 28},
    "p2000": {"credits": 2000, "price_usd": 75},
}

def set_price_credits(set_row) -> int:
    """Convert a set's USD price into credits (1 credit = $0.05)."""
    return max(1, int(round(set_row.price / 0.05)))

def bundle_discount(n_sets: int) -> float:
    """Multiplier applied to a bundle total. Bigger bundle = deeper cut."""
    if n_sets >= 10: return 0.70
    if n_sets >= 5:  return 0.80
    if n_sets >= 3:  return 0.90
    return 1.0