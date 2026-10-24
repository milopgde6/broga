# app/trust/public_stats.py
from app.catalog.stats import counts

def trust_line() -> str:
    c = counts()
    return (f"📊 {c['sets']} sets · {c['clips']} clips\n"
            f"🛡 hash-verified · ⚡️ instant delivery")