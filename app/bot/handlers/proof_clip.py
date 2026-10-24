# app/bot/handlers/proof_clip.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from app.trust.proof_clips import proof_path, has_proof

router = Router(name="proof_clip")


@router.callback_query(F.data.startswith("proof:"))
async def proof_cb(cb: CallbackQuery):
    set_id = int(cb.data.split(":")[1])
    if not has_proof(set_id):
        await cb.answer("No proof clip for this set.", show_alert=True)
        return
    await cb.message.answer_video(
        FSInputFile(proof_path(set_id)),
        caption="🎬 Proof clip — this is the actual file.",
    )
    await cb.answer()