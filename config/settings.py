# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN       = os.getenv("BOT_TOKEN", "")
ADMIN_IDS       = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
DB_URL          = os.getenv("DB_URL", "sqlite:///theez.db")

# access token
TOKEN_SECRET    = os.getenv("TOKEN_SECRET", "change-me")
TOKEN_TTL_SEC   = int(os.getenv("TOKEN_TTL_SEC", "60"))

# payments
SHIPSTARS_KEY   = os.getenv("SHIPSTARS_KEY", "")
USDT_TRC20_ADDR = os.getenv("USDT_TRC20_ADDR", "")
USDT_WATCHER_URL= os.getenv("USDT_WATCHER_URL", "")
WEBHOOK_SECRET  = os.getenv("WEBHOOK_SECRET", "")
WEBHOOK_HOST    = os.getenv("WEBHOOK_HOST", "0.0.0.0")
WEBHOOK_PORT    = int(os.getenv("WEBHOOK_PORT", "8080"))

# storage roots
STORAGE_ROOT    = os.getenv("STORAGE_ROOT", "app/storage")
ORIGINALS_DIR   = os.path.join(STORAGE_ROOT, "originals")
ENCODED_DIR     = os.path.join(STORAGE_ROOT, "encoded")
PREVIEW_DIR     = os.path.join(STORAGE_ROOT, "previews")