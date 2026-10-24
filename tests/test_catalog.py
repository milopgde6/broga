# tests/test_catalog.py
import pytest
from app.data.db import SessionLocal, Base, engine
from app.data.models import Set
from app.catalog.search_index import search
from app.catalog.auto_tag import suggest_tags, apply_tags


@pytest.fixture(autouse=True)
def fresh_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def test_search_by_title():
    with SessionLocal() as db:
        db.add(Set(title="Rare Classic HD", price=9.0))
        db.add(Set(title="New Drop", price=4.0))
        db.commit()
    assert len(search("classic")) == 1
    assert len(search("drop")) == 1
    assert len(search("zzz")) == 0


def test_auto_tag_rules():
    tags = suggest_tags("Rare Classic HD Remaster")
    assert "rare" in tags and "classic" in tags and "hd" in tags


def test_apply_tags_dedup():
    out = apply_tags("Rare HD", existing="hd,full-set")
    parts = set(out.split(","))
    assert "hd" in parts and "rare" in parts and "full-set" in parts
    assert len(parts) == len(out.split(","))