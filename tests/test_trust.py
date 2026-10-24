# tests/test_trust.py
import pytest
from app.data.db import SessionLocal, Base, engine
from app.data.models import User, Set, Order
from app.trust import reviews as rev
from app.trust import order_log


@pytest.fixture(autouse=True)
def fresh_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def _seed():
    with SessionLocal() as db:
        u = User(username="rev", credits=0)
        s = Set(title="S1", price=5.0)
        db.add_all([u, s]); db.commit()
        return u.id, s.id


def test_review_add_and_avg():
    uid, sid = _seed()
    rev.add(uid, sid, 5, "great")
    rev.add(uid, sid, 3, "ok")
    assert rev.avg_stars(sid) == 4.0


def test_review_clamped():
    uid, sid = _seed()
    rev.add(uid, sid, 99)
    assert rev.for_set(sid)[0].stars == 5


def test_order_log_recent():
    uid, sid = _seed()
    with SessionLocal() as db:
        db.add(Order(user_id=uid, set_id=sid, amount=5.0, rail="usdt",
                     status="paid", ref="abc123abc123"))
        db.commit()
    rows = order_log.recent(5)
    assert len(rows) == 1
    assert rows[0]["amount"] == 5.0


def test_order_log_sales_24h():
    uid, sid = _seed()
    with SessionLocal() as db:
        db.add(Order(user_id=uid, set_id=sid, amount=5.0, rail="usdt",
                     status="paid", ref="def456def456"))
        db.commit()
    assert order_log.sales_last_24h() == 1