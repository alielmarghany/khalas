#!/usr/bin/env bash
# Rebuild ../out/skit.mp4: npm i && ./build.sh
set -euo pipefail
cd "$(dirname "$0")"
TMP=$(mktemp -d)
node render.js "$TMP/frames"
./audio.sh "$TMP/audio.m4a"
mkdir -p ../out
ffmpeg -loglevel error -y -framerate 30 -i "$TMP/frames/f%04d.png" -i "$TMP/audio.m4a" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -profile:v high -r 30 -c:a copy -shortest -movflags +faststart ../out/skit.mp4
ffmpeg -loglevel error -y -ss 9.2 -i ../out/skit.mp4 -frames:v 1 ../out/preview.png
rm -rf "$TMP"
