# app/utils/formatting.py
def money(x: float) -> str:
    return f"${x:,.2f}"

def clip_count(n: int) -> str:
    return f"{n} clip" + ("s" if n != 1 else "")