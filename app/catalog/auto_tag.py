# app/catalog/auto_tag.py
"""Heuristic tagger. Cheap, deterministic, expandable."""
import re
from typing import List

_RULES = [
    (re.compile(r"\bremaster", re.I), "remaster"),
    (re.compile(r"\bfull\b", re.I), "full-set"),
    (re.compile(r"\bhd\b", re.I), "hd"),
    (re.compile(r"\b4k\b", re.I), "4k"),
    (re.compile(r"\bclassic\b", re.I), "classic"),
    (re.compile(r"\bnew\b", re.I), "new"),
    (re.compile(r"\brare\b", re.I), "rare"),
]


def suggest_tags(title: str) -> List[str]:
    if not title:
        return []
    tags = []
    for rx, tag in _RULES:
        if rx.search(title):
            tags.append(tag)
    return tags


def apply_tags(title: str, existing: str = "") -> str:
    """Merge suggested tags with existing comma string, dedup, sorted."""
    current = {t.strip() for t in (existing or "").split(",") if t.strip()}
    current.update(suggest_tags(title))
    return ",".join(sorted(current))