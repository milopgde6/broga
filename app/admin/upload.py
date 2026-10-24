"""Admin: upload encoded files to R2 and register a new set."""
import os
import tempfile

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from app.bot.filters.is_admin import IsAdmin
from app.catalog.ingest import ingest_set
from app.catalog.manifest import build_manifest
from app.bot.states.admin_states import AdminStates
from app.storage import files
from app.storage.layout import slug

router = Router(name="admin_upload")
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())

MEDIA = F.video | F.document


@router.callback_query(F.data == "adm:upload")
async def upload_start(cb: CallbackQuery, state):
    await state.set_state(AdminStates.uploading)
    await state.update_data(uploads=[])
    await cb.message.edit_text(
        "📤 UPLOAD SET\n\n"
        "Send the encoded file(s) as video/document.\n"
        "When finished, send /done, then reply with metadata:\n"
        "`title | studio | girl | age | ethnicity | era | quality | price`"
    )
    await cb.answer()


@router.message(AdminStates.uploading, F.text == "/done")
async def upload_done(message: Message, state):
    data = await state.get_data()
    if not data.get("uploads"):
        await message.answer("Upload at least one file first.")
        return
    await state.set_state(AdminStates.upload_meta)
    await message.answer("Send metadata: title | studio | girl | age | ethnicity | era | quality | price")


@router.message(AdminStates.uploading, MEDIA)
async def upload_file(message: Message, state):
    media = message.video or message.document
    original = getattr(media, "file_name", None) or f"{media.file_unique_id}.mp4"
    safe = slug(os.path.basename(original))
    key = f"encoded/{media.file_unique_id}_{safe}"

    fd, tmp = tempfile.mkstemp(prefix="theez_upload_")
    try:
        with os.fdopen(fd, "wb") as fh:
            await message.bot.download(media, destination=fh)
        files.upload_file(tmp, key=key, content_type=getattr(media, "mime_type", None))
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

    data = await state.get_data()
    uploads = list(data.get("uploads", []))
    uploads.append(key)
    await state.update_data(uploads=uploads)
    await message.answer(
        f"✅ Uploaded `{safe}` ({len(uploads)} file(s)).\n"
        "Send more, or /done to finish."
    )


@router.message(AdminStates.upload_meta)
async def upload_receive(message: Message, state):
    text = (message.text or "").strip()
    parts = [p.strip() for p in text.split("|")]
    if len(parts) != 8:
        await message.answer("Need exactly 8 fields: title | studio | girl | age | ethnicity | era | quality | price")
        return
    title, studio, girl, age, eth, era, quality, price = parts
    try:
        age_i = int(age)
        price_f = float(price)
    except ValueError:
        await message.answer("age must be int, price must be float")
        return

    data = await state.get_data()
    uploads = list(data.get("uploads", []))
    set_id = ingest_set(
        title=title, studio_name=studio, girl_name=girl,
        age=age_i, ethnicity=eth, era=era,
        quality=quality, price=price_f, files=uploads,
    )
    try:
        build_manifest(set_id)
    except Exception:
        pass
    await state.clear()
    await message.answer(f"✅ Set #{set_id} registered with {len(uploads)} clip(s).")


@router.callback_query(F.data == "adm:uploadcancel")
async def upload_cancel(cb: CallbackQuery, state):
    await state.clear()
    await cb.message.edit_text("Upload cancelled.")
    await cb.answer()


@router.message(F.text.regexp(r"^/manifest (\d+)$"))
async def build_manifest_cmd(message: Message):
    set_id = int(message.text.split()[1])
    try:
        path = build_manifest(set_id)
        await message.answer(f"🛡 Manifest built: {path}")
    except Exception as e:
        await message.answer(f"❌ {e}")
