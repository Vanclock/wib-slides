#!/bin/sh
# One-time setup in a fresh container (run from the repo root)
pip install --break-system-packages fonttools cairosvg pillow
cd "$(dirname "$0")" && npm init -y >/dev/null && npm i @fontsource/unifrakturcook @fontsource/old-standard-tt
