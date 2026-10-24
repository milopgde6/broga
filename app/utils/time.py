# app/utils/time.py
from datetime import datetime

def now_utc():
    return datetime.utcnow()

def fmt(dt) -> str:
    return dt.strftime("%Y-%m-%d %H:%M") if dt else "-"