"""Unified media storage.

Uses Cloudflare R2 when configured, otherwise falls back to the local
filesystem under STORAGE_ROOT. Keys are POSIX paths relative to STORAGE_ROOT
(e.g. ``encoded/clip_12.mp4``); legacy filesystem paths are normalised by
:func:`key_for`.
"""
import hashlib
import os
import shutil

from app.storage import r2
from app.utils.hashing import sha256_file
from config.settings import R2_URL_TTL_SEC, STORAGE_ROOT


def enabled() -> bool:
    return r2.enabled()


def key_for(path: str) -> str:
    """Normalise a key or legacy filesystem path to a storage key."""
    p = str(path).replace("\\", "/")
    root = STORAGE_ROOT.replace("\\", "/").rstrip("/")
    if p == root:
        return ""
    if p.startswith(root + "/"):
        p = p[len(root) + 1:]
    elif p.startswith("./"):
        p = p[2:]
    return p.lstrip("/")


def local_path(key: str) -> str:
    """Local filesystem path for a key (used in local mode / temp downloads)."""
    p = str(key)
    if not enabled() and os.path.isabs(p):
        return p
    return os.path.join(STORAGE_ROOT, key_for(p))


def exists(key: str) -> bool:
    k = key_for(key)
    if enabled():
        return r2.exists(k)
    return os.path.exists(local_path(k))


def size(key: str) -> int:
    k = key_for(key)
    if enabled():
        return r2.size(k)
    return os.path.getsize(local_path(k))


def sha256(key: str) -> str:
    k = key_for(key)
    if not enabled():
        return sha256_file(local_path(k))
    digest = hashlib.sha256()
    for chunk in r2.iter_chunks(k):
        digest.update(chunk)
    return digest.hexdigest()


def read_bytes(key: str) -> bytes:
    k = key_for(key)
    if enabled():
        return r2.get_bytes(k)
    with open(local_path(k), "rb") as f:
        return f.read()


def write_bytes(key: str, data: bytes, content_type: str | None = None) -> str:
    k = key_for(key)
    if enabled():
        r2.put_bytes(k, data, content_type)
        return k
    dest = local_path(k)
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)
    return k


def read_text(key: str) -> str:
    return read_bytes(key).decode("utf-8")


def write_text(key: str, text: str, content_type: str = "application/json") -> str:
    return write_bytes(key, text.encode("utf-8"), content_type)


def upload_file(local_file: str, key: str | None = None,
                content_type: str | None = None) -> str:
    """Upload a local file. In local mode, copies it under STORAGE_ROOT."""
    k = key_for(key or local_file)
    if enabled():
        r2.upload_file(local_file, k, content_type)
        return k
    dest = local_path(k)
    if os.path.abspath(local_file) != os.path.abspath(dest):
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        shutil.copyfile(local_file, dest)
    return k


def url(key: str, expires: int | None = None) -> str | None:
    """Short-lived presigned URL, or None when storage is local."""
    if not enabled():
        return None
    return r2.presigned_url(key_for(key), expires or R2_URL_TTL_SEC)
