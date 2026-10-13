#!/usr/bin/env sh
# Regenera los recursos minificados y las páginas legales.
# Requiere Node (npx) y Python 3. Uso: sh scripts/build.sh
set -e
cd "$(dirname "$0")/.."
npx --yes esbuild@0.24.2 css/styles.css --minify --outfile=css/styles.min.css --log-level=warning
npx --yes esbuild@0.24.2 js/main.js --minify --target=es2017 --outfile=js/main.min.js --log-level=warning
python3 scripts/build_legal.py .
echo "OK"
