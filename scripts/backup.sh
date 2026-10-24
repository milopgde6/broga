#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DB="${ROOT}/theez.db"
KIND="${1:-daily}"
case "$KIND" in daily|weekly) ;; *) echo "usage: backup.sh [daily|weekly]"; exit 1;; esac

OUT="${ROOT}/app/data/backups/${KIND}"
KEEP=$([ "$KIND" = "weekly" ] && echo 12 || echo 20)
STAMP="$(date +%Y%m%d_%H%M%S)"

mkdir -p "$OUT"; touch "$OUT/.gitkeep"
[ -f "$DB" ] || { echo "no db at $DB"; exit 1; }

if command -v sqlite3 >/dev/null 2>&1; then
  sqlite3 "$DB" ".backup '${OUT}/theez_${STAMP}.db'"
else
  cp "$DB" "${OUT}/theez_${STAMP}.db"
fi
echo "db backed up → ${OUT}/theez_${STAMP}.db"

ls -1t "$OUT"/theez_*.db 2>/dev/null | tail -n +$((KEEP + 1)) | xargs -r rm --
echo "kept last $KEEP in $OUT"
