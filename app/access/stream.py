# app/access/stream.py
from app.access.tokenize import verify
from app.access.entitlements import owns

def can_stream(token: str) -> bool:
    parsed = verify(token)
    if not parsed:
        return False
    user_id, set_id = parsed
    return owns(user_id, set_id)