# tests/test_access.py
import pytest
from app.data.db import SessionLocal, Base, engine
from app.data.models import User, Set, Entitlement
from app.access.grant import grant
from app.access.revoke import revoke
from app.access.entitlements import owns


@pytest.fixture(autouse=True)
def fresh_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def _seed():
    with SessionLocal() as db:
        u = User(username="tester", credits=0)
        s = Set(title="S1", price=5.0)
        db.add_all([u, s]); db.commit()
        return u.id, s.id


def test_grant_then_owns():
    uid, sid = _seed()
    grant(uid, sid)
    assert owns(uid, sid) is True


def test_revoke_removes():
    uid, sid = _seed()
    grant(uid, sid)
    revoke(uid, sid)
    assert owns(uid, sid) is False


def test_double_grant_idempotent():
    uid, sid = _seed()
    grant(uid, sid)
    grant(uid, sid)
    with SessionLocal() as db:
        assert db.query(Entitlement).filter_by(user_id=uid, set_id=sid).count() == 1