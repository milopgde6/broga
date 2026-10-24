# app/admin/reviews_mod.py
"""Admin: list, inspect and delete reviews."""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from app.bot.filters.is_admin import IsAdmin
from app.data.models import Review, User, Set
from app.data.db import SessionLocal

router = Router(name="admin_reviews")
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())

PAGE = 20


@router.callback_query(F.data == "adm:reviews")
async def reviews_home(cb: CallbackQuery):
    with SessionLocal() as db:
        rows = (db.query(Review)
                  .order_by(Review.id.desc())
                  .limit(PAGE).all())
        if not rows:
            await cb.message.edit_text(
                "⭐️ REVIEWS MOD\n\nNo reviews yet.\n\n"
                "Delete one with `/delreview <id>`"
            )
            return await cb.answer()

        lines = [f"⭐️ LAST {len(rows)} REVIEWS", ""]
        for r in rows:
            u = db.query(User).get(r.user_id)
            s = db.query(Set).get(r.set_id)
            handle = u.username if u and u.username else f"u{r.user_id}"
            title = s.title if s else f"set{r.set_id}"
            body = (r.text or "")[:40].replace("\n", " ")
            lines.append(f"#{r.id} · {r.stars}⭐ · {handle} · {title}")
            if body:
                lines.append(f"    “{body}”")
        lines.append("")
        lines.append("Delete: `/delreview <id>`  ·  `/delreviews <set_id>`")
    await cb.message.edit_text("\n".join(lines))
    await cb.answer()


@router.message(F.text.regexp(r"^/delreview (\d+)$"))
async def delete_one(message: Message):
    rid = int(message.text.split()[1])
    with SessionLocal() as db:
        r = db.query(Review).get(rid)
        if not r:
            await message.answer("No such review.")
            return
        db.delete(r)
        db.commit()
    await message.answer(f"🗑 Deleted review #{rid}")


@router.message(F.text.regexp(r"^/delreviews (\d+)$"))
async def delete_all_for_set(message: Message):
    sid = int(message.text.split()[1])
    with SessionLocal() as db:
        n = db.query(Review).filter_by(set_id=sid).delete()
        db.commit()
    await message.answer(f"🗑 Deleted {n} review(s) for set {sid}")