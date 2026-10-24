# app/admin/backups.py
"""Admin: trigger DB backup."""
import subprocess
import os
from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.bot.filters.is_admin import IsAdmin

router = Router(name="admin_backups")
router.callback_query.filter(IsAdmin())

BACKUP_SCRIPT = os.path.join("scripts", "backup.sh")


@router.callback_query(F.data == "adm:backups")
async def backups_cb(cb: CallbackQuery):
    await cb.answer("Running backup…")
    try:
        out = subprocess.check_output(["bash", BACKUP_SCRIPT],
                                      stderr=subprocess.STDOUT, timeout=120)
        text = out.decode()[-1000:]
    except subprocess.CalledProcessError as e:
        text = f"❌ backup failed:\n{e.output.decode()[-1000:]}"
    except Exception as e:
        text = f"❌ {e}"
    await cb.message.edit_text(f"💾 BACKUP\n\n{text}")