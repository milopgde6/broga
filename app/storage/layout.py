# app/storage/layout.py
"""Canonical storage layout. One place defines every path.

Nothing else in the codebase should string-join STORAGE_ROOT by hand —
import from here so a folder rename can't break four modules at once.
"""
import os
import re

from config.settings import STORAGE_ROOT

# --- fixed roots ---
ROOT      = STORAGE_ROOT
ORIGINALS = os.path.join(ROOT, "originals")   # master files, never re-encoded from
ENCODED   = os.path.join(ROOT, "encoded")     # delivery copies
PREVIEWS  = os.path.join(ROOT, "previews")
PROOF     = os.path.join(ROOT, "proof")       # proof clips shown pre-purchase
THUMBS    = os.path.join(ROOT, "thumbs")
POSTERS   = os.path.join(ROOT, "posters")
TEMP      = os.path.join(ROOT, "temp")
MANIFESTS = os.path.join(ROOT, "manifests")   # hash manifests per set
BY_STUDIO = os.path.join(ROOT, "by_studio")   # human-browsable mirror

STORAGE_DIRS = [
    ORIGINALS, ENCODED, PREVIEWS, PROOF,
    THUMBS, POSTERS, TEMP, MANIFESTS, BY_STUDIO,
]

# --- DB backups live beside the data package ---
BACKUP_DIRS = [
    os.path.join("app", "data", "backups", "daily"),
    os.path.join("app", "data", "backups", "weekly"),
]

_SLUG_RE = re.compile(r"[^A-Za-z0-9._-]+")


def slug(s: str) -> str:
    """Filesystem-safe segment. Collapses junk to single underscores."""
    s = (s or "unknown").strip()
    s = _SLUG_RE.sub("_", s)
    return s.strip("_") or "unknown"


def set_dir(studio: str, year: str | int, girl: str, set_title: str) -> str:
    """Path for one set: by_studio/<studio>/<year>/<girl>/<set>."""
    path = os.path.join(
        BY_STUDIO, slug(studio), slug(str(year)), slug(girl), slug(set_title)
    )
    os.makedirs(path, exist_ok=True)
    return path


def _pin(d: str) -> None:
    """Create dir + a .gitkeep so Git tracks the empty folder."""
    os.makedirs(d, exist_ok=True)
    keep = os.path.join(d, ".gitkeep")
    if not os.path.exists(keep):
        open(keep, "a").close()


def ensure_layout() -> list[str]:
    """Create every required dir and pin it. Idempotent. Returns what exists."""
    created = []
    for d in STORAGE_DIRS + BACKUP_DIRS:
        _pin(d)
        created.append(d)
    return created


def proof_path(set_id: int) -> str:
    return os.path.join(PROOF, f"set_{set_id}_proof.mp4")


def manifest_path(set_id: int) -> str:
    return os.path.join(MANIFESTS, f"set_{set_id}.json")


def thumb_path(clip_id: int) -> str:
    return os.path.join(THUMBS, f"clip_{clip_id}.jpg")