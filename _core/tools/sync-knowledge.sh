#!/usr/bin/env bash
# Mirror the auto-memory (deep topic notes) into this folder so the Drive
# folder stays the only source of truth. Run at every loop close.
set -euo pipefail
SRC="$HOME/.claude/projects/-Users-bam-Library-CloudStorage-GoogleDrive-we-therum-studio-My-Drive-Therum-Projects-TSC-BETA/memory"
DST="$(cd "$(dirname "$0")/.." && pwd)/knowledge"
mkdir -p "$DST"
rsync -a --delete --exclude '.DS_Store' "$SRC/" "$DST/"
echo "knowledge synced: $(ls "$DST"/*.md | wc -l | tr -d ' ') files → $DST"
