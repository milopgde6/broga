# app/access/tokenize.py
import hmac, hashlib, time, base64
from config.settings import TOKEN_SECRET, TOKEN_TTL_SEC

def _sig(payload: str) -> str:
    return hmac.new(TOKEN_SECRET.encode(), payload.encode(),
                    hashlib.sha256).hexdigest()[:16]

def mint(user_id: int, set_id: int) -> str:
    """Create a short-lived signed access token for a user+set."""
    exp = int(time.time()) + TOKEN_TTL_SEC
    payload = f"{user_id}:{set_id}:{exp}"
    token = f"{payload}:{_sig(payload)}"
    return base64.urlsafe_b64encode(token.encode()).decode()

def verify(token: str) -> tuple[int, int] | None:
    """Return (user_id, set_id) if valid & unexpired, else None."""
    try:
        raw = base64.urlsafe_b64decode(token.encode()).decode()
        user_id, set_id, exp, sig = raw.split(":")
        payload = f"{user_id}:{set_id}:{exp}"
        if not hmac.compare_digest(sig, _sig(payload)):
            return None
        if int(exp) < int(time.time()):
            return None
        return int(user_id), int(set_id)
    except Exception:
        return None