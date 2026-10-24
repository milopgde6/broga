# app/bot/handlers/provenance.py
from aiogram import Router, F
from aiogram.types import CallbackQuery
from config.emoji_map import E
from app.bot.keyboards.shared_kb import back_kb
from app.data.models import Set
from app.data.db import SessionLocal
from app.storage.layout import manifest_path
import os, json

router = Router()

@router.callback_query(F.data.startswith("prov:"))
async def show_provenance(cb: CallbackQuery):
    set_id = int(cb.data.split(":")[1])
    db = SessionLocal()
    try:
        s = db.query(Set).get(set_id)
        if not s:
            await cb.answer("Not found"); return
        title, era = s.title, s.era
        studio = s.studio.name if s.studio else "unknown"
        girl = s.girl.name if s.girl else "unknown"
    finally:
        db.close()

    mpath = manifest_path(set_id)
    hashes = "—"
    if os.path.exists(mpath):
        with open(mpath) as f:
            m = json.load(f)
        hashes = "\n".join(f"`{c['sha256'][:16]}…` {c['file']}" for c in m["clips"][:5])

    text = (
        f"{E['sources']} *PROVENANCE*\n\n"
        f"Title: {title}\n"
        f"Studio: {studio}\n"
        f"Girl: {girl}\n"
        f"Era: {era}\n\n"
        f"{E['trust']} *SHA-256 manifest:*\n{hashes}"
    )
    await cb.message.edit_text(text, reply_markup=back_kb(), parse_mode="Markdown")
    await cb.answer()