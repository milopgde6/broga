# app/payments/addresses.py
"""Payment rail addresses and ref encoding."""
from config.settings import USDT_TRC20_ADDR


def usdt_address(ref: str) -> str:
    """Return the USDT address (ref is tracked off-chain)."""
    return USDT_TRC20_ADDR


def payment_instructions(rail: str, ref: str, amount: float) -> str:
    if rail == "usdt":
        return (
            "💵 USDT (TRC20)\n\n"
            f"Send ${amount:.2f} to:\n`{USDT_TRC20_ADDR}`\n\n"
            f"Ref: `{ref}`\n"
            "Include the ref in the memo/note if your wallet allows."
        )
    if rail == "shipstars":
        return (
            "⭐️ ShipStars\n\n"
            f"Send ${amount:.2f} to @TheezStore\n"
            f"Ref: `{ref}`"
        )
    if rail == "credits":
        return f"🪙 Paying ${amount:.2f} from your credits balance."
    return "Unknown rail."