# app/admin/manifest_admin.py
"""Admin: build/verify manifests."""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from app.bot.filters.is_admin import IsAdmin
from app.catalog.manifest import build_manifest, verify_manifest

router = Router(name="admin_manifest")
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.callback_query(F.data == "adm:manifest")
async def manifest_cb(cb: CallbackQuery):
    await cb.message.edit_text(
        "📜 MANIFEST ADMIN\n\n"
        "`/buildmanifest <set_id>` — build\n"
        "`/verifymanifest <set_id>` — verify"
    )
    await cb.answer()


@router.message(F.text.regexp(r"^/buildmanifest (\d+)$"))
async def build_cmd(message: Message):
    sid = int(message.text.split()[1])
    try:
        path = build_manifest(sid)
        await message.answer(f"🛡 Built: {path}")
    except Exception as e:
        await message.answer(f"❌ {e}")


@router.message(F.text.regexp(r"^/verifymanifest (\d+)$"))
async def verify_cmd(message: Message):
    sid = int(message.text.split()[1])
    ok = verify_manifest(sid)
    await message.answer(f"{'✅ verified' if ok else '❌ tampered/missing'} — set {sid}")