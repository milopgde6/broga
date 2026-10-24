# tests/test_bot.py
"""Keyboard contract tests. These catch the #1 bot bug: callback drift."""
from app.bot.keyboards.main_menu import main_menu
from app.bot.keyboards.age_kb import age_bands_kb
from config.age_bands import AGE_BANDS


def _flat(kb):
    return [b.callback_data for row in kb.inline_keyboard for b in row]


def test_menu_has_core_buttons():
    cbs = _flat(main_menu())
    for must in ("browse", "library", "search", "sources", "trust", "how"):
        assert must in cbs


def test_menu_callback_data_unique():
    cbs = _flat(main_menu())
    assert len(cbs) == len(set(cbs)), "duplicate callback_data in main menu"


def test_menu_callback_within_telegram_limit():
    for cb in _flat(main_menu()):
        if cb is None:  # URL buttons carry no callback_data
            continue
        assert len(cb.encode("utf-8")) <= 64


def test_age_kb_covers_all_bands():
    cbs = _flat(age_bands_kb())
    for band in AGE_BANDS:
        assert f"age:{band}" in cbs


def test_age_kb_has_back():
    assert "menu" in _flat(age_bands_kb())