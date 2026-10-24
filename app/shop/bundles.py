# app/shop/bundles.py
# STUB: bundle = list of set_ids sold together at a discount
BUNDLES = {
    "starter_pack": {"sets": [1, 2, 3], "discount": 0.15},
}

def get(bundle_id: str):
    return BUNDLES.get(bundle_id)

def price(bundle_id: str, set_prices: list) -> float:
    b = BUNDLES.get(bundle_id)
    if not b:
        return 0.0
    total = sum(set_prices)
    return round(total * (1 - b["discount"]), 2)