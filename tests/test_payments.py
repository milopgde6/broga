# tests/test_payments.py
import pytest
from app.data.db import SessionLocal, Base, engine
from app.data.models import User, Set
from app.shop import orders
from app.payments.refunds import refund
from app.access.entitlements import owns
from app.access.grant import grant


@pytest.fixture(autouse=True)
def fresh_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def _seed():
    with SessionLocal() as db:
        u = User(username="buyer", credits=0)
        s = Set(title="S1", price=5.0)
        db.add_all([u, s]); db.commit()
        return u.id, s.id


def test_order_create_and_pay():
    uid, sid = _seed()
    o = orders.create(uid, sid, 5.0, "usdt")
    assert o.status == "pending"
    orders.mark_paid(o.ref)
    assert orders.get(o.ref).status == "paid"


def test_refund_revokes():
    uid, sid = _seed()
    o = orders.create(uid, sid, 5.0, "usdt")
    orders.mark_paid(o.ref)
    grant(uid, sid)
    assert owns(uid, sid)
    refund(o.ref)
    assert not owns(uid, sid)
    assert orders.get(o.ref).status == "refunded"