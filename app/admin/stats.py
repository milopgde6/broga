# app/admin/stats.py
"""Admin: dashboard stats."""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import func

from app.bot.filters.is_admin import IsAdmin
from app.data.models import Set, Clip, Order, User, Entitlement
from app.data.db import SessionLocal

router = Router(name="admin_stats")
router.callback_query.filter(IsAdmin())


@router.callback_query(F.data == "adm:stats")
async def stats_cb(cb: CallbackQuery):
    with SessionLocal() as db:
        sets = db.query(Set).count()
        clips = db.query(Clip).count()
        users = db.query(User).count()
        paid = db.query(Order).filter_by(status="paid").count()
        revenue = db.query(func.coalesce(func.sum(Order.amount), 0.0)) \
                    .filter(Order.status == "paid").scalar()
        owned = db.query(Entitlement).count()
    await cb.message.edit_text(
        "📊 STATS\n\n"
        f"👥 Users: {users}\n"
        f"🎞 Sets: {sets}\n"
        f"🎬 Clips: {clips}\n"
        f"🧾 Paid orders: {paid}\n"
        f"💵 Revenue: ${revenue:.2f}\n"
        f"🔑 Entitlements: {owned}"
    )
    await cb.answer()