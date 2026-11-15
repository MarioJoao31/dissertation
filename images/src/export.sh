#!/bin/sh
# Export each images/src/<name>.svg to images/<name>.pdf (vector) with headless Chrome.
# Usage: ./export.sh [name ...]   (no args = all)
set -e
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP=$(mktemp -d)
names=${*:-$(ls *.svg | sed 's/\.svg$//')}
for n in $names; do
  vb=$(grep -o 'viewBox="[^"]*"' "$n.svg" | head -1 | tr -d '"' | cut -d= -f2)
  w=$(echo "$vb" | awk '{print $3}'); h=$(echo "$vb" | awk '{print $4}')
  { printf '<!doctype html><html><head><meta charset="utf-8"><style>@page{size:%spx %spx;margin:0}html,body{margin:0;padding:0}body>svg{width:%spx;height:%spx;display:block}</style></head><body>' "$w" "$h" "$w" "$h"
    sed '1{/^<?xml/d;}' "$n.svg"
    printf '</body></html>'; } > "$TMP/$n.html"
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer --virtual-time-budget=4000 \
    --print-to-pdf="$PWD/../$n.pdf" "file://$TMP/$n.html" 2>/dev/null
  "$CHROME" --headless --disable-gpu --hide-scrollbars --virtual-time-budget=4000 \
    --window-size="$w,$h" --screenshot="$TMP/$n.png" "file://$TMP/$n.html" 2>/dev/null
  cp "$TMP/$n.png" "${PREVIEW_DIR:-$TMP}/$n.png" 2>/dev/null || true
  echo "exported $n ($w x $h)"
done
