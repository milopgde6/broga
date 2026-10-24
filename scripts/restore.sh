#!/usr/bin/env bash
set -euo pipefail
[ $# -lt 1 ] && { echo "usage: restore.sh <backup.db>"; exit 1; }
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$1"; DST="${ROOT}/theez.db"
[ -f "$SRC" ] || { echo "no such file: $SRC"; exit 1; }
[ -f "$DST" ] && cp "$DST" "${DST}.pre_restore"
cp "$SRC" "$DST"
echo "restored $SRC → $DST (previous saved as ${DST}.pre_restore)"
