# app/utils/validation.py
"""Input validation helpers. Fail loud, fail early."""
import re
from typing import Optional

_REF_RE = re.compile(r"^[a-f0-9]{12}$")
_USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,32}$")


class ValidationError(ValueError):
    """Raised when an input fails validation."""


def valid_age_band(band: str, bands: dict) -> bool:
    if not isinstance(band, str):
        return False
    return band in bands


def valid_ref(ref: str) -> bool:
    return bool(ref) and bool(_REF_RE.match(ref))


def valid_username(name: str) -> bool:
    return bool(name) and bool(_USERNAME_RE.match(name))


def valid_amount(amount: float, minimum: float = 0.0) -> bool:
    try:
        return float(amount) >= minimum
    except (TypeError, ValueError):
        return False


def require(condition: bool, msg: str) -> None:
    if not condition:
        raise ValidationError(msg)


def parse_age_band(band: str, bands: dict) -> tuple[int, int]:
    """Return (lo, hi) for a band key, raising if unknown."""
    require(band in bands, f"unknown age band: {band}")
    return bands[band]


def sanitize_text(s: Optional[str], max_len: int = 200) -> str:
    if not s:
        return ""
    s = s.strip()
    return s if len(s) <= max_len else s[:max_len - 1] + "…"