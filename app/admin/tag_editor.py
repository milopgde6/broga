# app/admin/tag_editor.py
"""Admin: edit tags on a set."""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from app.bot.filters.is_admin import IsAdmin
from app.data.models import Set
from app.data.db import SessionLocal
from app.bot.states.admin_states import AdminStates

router = Router(name="admin_tags")
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.callback_query(F.data == "adm:tags")
async def tags_start(cb: CallbackQuery, state):
    await state.set_state(AdminStates.editing_tags)
    await cb.message.edit_text("🏷 Send: `set_id | tag1, tag2, tag3`")
    await cb.answer()


@router.message(AdminStates.editing_tags)
async def tags_apply(message: Message, state):
    text = (message.text or "").strip()
    if "|" not in text:
        await message.answer("Format: set_id | tag1, tag2")
        return
    sid_s, tags_s = text.split("|", 1)
    try:
        sid = int(sid_s.strip())
    except ValueError:
        await message.answer("set_id must be int")
        return
    tags = [t.strip() for t in tags_s.split(",") if t.strip()]
    with SessionLocal() as db:
        s = db.query(Set).get(sid)
        if not s:
            await message.answer("Set not found")
            return
        s.tags = ",".join(tags)
        db.commit()
    await state.clear()
    await message.answer(f"✅ Tags updated on #{sid}: {', '.join(tags)}")