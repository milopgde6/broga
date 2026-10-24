# 🛡 TRUST — Theez

> Scammers copy the menu. They can't copy a hash-matched master archive.

## The two folders that matter

| Folder            | Role              | Who sees it |
|-------------------|-------------------|-------------|
| `trust/`          | Public promise    | buyers      |
| `storage/originals/` | Private proof  | you only    |

## What "verified source" means here

1. Every set is ingested once, hashed with SHA-256, and logged.
2. A per-set manifest (`storage/manifests/set_<id>.json`) records
   filename → hash → byte size for every clip.
3. `verify_manifest()` re-hashes on demand and compares. A mismatch
   means tampering or corruption, and it shows.
4. Originals are never re-encoded from a copy — encoders read from
   `originals/`, never from `encoded/`.

## The public trust surface

- **📜 SOURCES** — provenance per set (studio, era, quality, clip count).
- **🛡 TRUST** — how verification works, plainly stated.
- **⚡️ HOW IT WORKS** — kills the "wait 24h" scammer delay.
- **🧾 order log** — recent paid sales, anonymized, as social proof.
- **🎬 proof clips** — a real clip from the set, shown before you buy.

## The seller's checklist (every set)

- [ ] ingested via `ingest_set`
- [ ] manifest built via `build_manifest`
- [ ] `verify_manifest` returns True
- [ ] proof clip present in `storage/proof/`
- [ ] price set, quality tagged

## Delivery promise

Payment confirmed → entitlement granted → token minted → instant.
No manual "send me your receipt and wait."

## Rails

- ⭐️ ShipStars
- 💵 USDT (TRC20)
- 🪙 Credits

Refund policy: corrupt file = refund + entitlement revoked.