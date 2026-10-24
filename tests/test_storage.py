import hashlib

from app.storage import files


def test_key_for_normalises(tmp_path, monkeypatch):
    monkeypatch.setattr(files, "STORAGE_ROOT", str(tmp_path))
    assert files.key_for(str(tmp_path / "encoded" / "a.mp4")) == "encoded/a.mp4"
    assert files.key_for("encoded/a.mp4") == "encoded/a.mp4"
    assert files.key_for("./encoded/a.mp4") == "encoded/a.mp4"


def test_local_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(files, "STORAGE_ROOT", str(tmp_path))
    monkeypatch.setattr(files.r2, "enabled", lambda: False)

    key = files.write_text("manifests/set_1.json", '{"ok": true}')
    assert key == "manifests/set_1.json"
    assert files.exists(key)
    assert files.read_text(key) == '{"ok": true}'
    assert files.url(key) is None

    data = b"hello"
    files.write_bytes("encoded/x.bin", data)
    assert files.size("encoded/x.bin") == len(data)
    assert files.sha256("encoded/x.bin") == hashlib.sha256(data).hexdigest()
