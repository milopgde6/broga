# app/admin/upload.py
"""Admin: register a new set from uploaded files."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from app.bot.filters.is_admin import IsAdmin
from app.catalog.ingest import ingest_set
from app.catalog.manifest import build_manifest
from app.bot.states.admin_states import AdminStates

router = Router(name="admin_upload")
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.callback_query(F.data == "adm:upload")
async def upload_start(cb: CallbackQuery, state):
    await state.set_state(AdminStates.uploading)
    await cb.message.edit_text(
        "📤 UPLOAD SET\n\n"
        "Send the encoded file(s) as video/document.\n"
        "Then reply with metadata as:\n"
        "`title | studio | girl | age | ethnicity | era | quality | price`"
    )
    await cb.answer()


@router.message(AdminStates.uploading)
async def upload_receive(message: Message, state):
    text = (message.text or "").strip()
    if "|" not in text:
        await message.answer("Send metadata: title | studio | girl | age | ethnicity | era | quality | price")
        return
    parts = [p.strip() for p in text.split("|")]
    if len(parts) != 8:
        await message.answer("Need exactly 8 fields separated by |")
        return
    title, studio, girl, age, eth, era, quality, price = parts
    try:
        age_i = int(age)
        price_f = float(price)
    except ValueError:
        await message.answer("age must be int, price must be float")
        return
    set_id = ingest_set(
        title=title, studio_name=studio, girl_name=girl,
        age=age_i, ethnicity=eth, era=era,
        quality=quality, price=price_f, files=[],
    )
    await state.clear()
    await message.answer(f"✅ Set #{set_id} registered.\nBuild manifest with /manifest {set_id}")


@router.message(F.text.regexp(r"^/manifest (\d+)$"))
async def build_manifest_cmd(message: Message):
    set_id = int(message.text.split()[1])
    try:
        path = build_manifest(set_id)
        await message.answer(f"🛡 Manifest built:\n{path}")
    except Exception as e:
        await message.answer(f"❌ {e}")