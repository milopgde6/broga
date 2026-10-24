# app/admin/users.py
"""Admin: user lookup and credit grant."""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from app.bot.filters.is_admin import IsAdmin
from app.data.models import User, Order
from app.data.db import SessionLocal
from app.shop import credits

router = Router(name="admin_users")
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.callback_query(F.data == "adm:users")
async def users_cb(cb: CallbackQuery):
    await cb.message.edit_text(
        "👥 USERS\n\n"
        "Send: `user_id` to inspect\n"
        "Send: `user_id | +credits` to grant"
    )
    await cb.answer()


@router.message(F.text.regexp(r"^\d+(\s*\|\s*[+-]?\d+)?$"))
async def user_lookup(message: Message):
    text = message.text.strip()
    if "|" in text:
        uid_s, amt_s = text.split("|", 1)
        uid = int(uid_s.strip())
        amt = int(amt_s.strip())
        credits.add(uid, amt)
        await message.answer(f"✅ {uid} credits {amt:+d} → now {credits.balance(uid)}")
        return
    uid = int(text)
    with SessionLocal() as db:
        u = db.query(User).get(uid)
        if not u:
            await message.answer("No such user.")
            return
        orders = db.query(Order).filter_by(user_id=uid).count()
        paid = db.query(Order).filter_by(user_id=uid, status="paid").count()
    await message.answer(
        f"👤 {uid}\n"
        f"username: {u.username or '—'}\n"
        f"credits: {u.credits}\n"
        f"orders: {orders} ({paid} paid)"
    )