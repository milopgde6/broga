# app/utils/text.py
def truncate(s: str, n: int = 60) -> str:
    return s if len(s) <= n else s[:n - 1] + "…"