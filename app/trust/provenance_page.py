# app/trust/provenance_page.py
from config.branding import BRAND

def sources_page() -> str:
    return (
        "📜 SOURCES\n"
        "Every set is sourced, hashed, and logged.\n"
        "Originals kept in trust/originals — never re-encoded from a copy.\n"
        "Scammers copy the menu; they can't copy a hash-matched master archive."
    )

def trust_page() -> str:
    return (
        "🛡 TRUST\n"
        "• verified source\n"
        "• hash manifest per set\n"
        "• instant delivery\n"
        "• public order log\n"
        f"Questions → {BRAND['support_handle']}"
    )