# app/trust/badges.py
from config.emoji_map import E

def set_badges(set_row) -> str:
    b = []
    if set_row.is_rare:  b.append(f"{E['rare']} RARE")
    if set_row.is_full:  b.append(f"{E['full_sets']} FULL SET")
    if set_row.quality == "remaster":
        b.append(f"{E['quality']} REMASTER")
    elif set_row.quality == "hd":
        b.append(f"{E['quality']} HD")
    return "  ".join(b)

def trust_line() -> str:
    return f"{E['trust']} verified source  ·  {E['how']} instant delivery"