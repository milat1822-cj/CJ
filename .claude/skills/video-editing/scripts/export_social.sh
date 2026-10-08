#!/usr/bin/env bash
# 輸出 IG/FB 版本。mode: reels(9:16 1080x1920 置中裁切) | feed(4:5 1080x1350)
# 用法: export_social.sh <輸入> <輸出.mp4> reels|feed
set -euo pipefail
in="$1"; out="$2"; mode="${3:-reels}"
case "$mode" in
  reels) w=1080; h=1920 ;;
  feed)  w=1080; h=1350 ;;
  *) echo "mode 只能是 reels 或 feed"; exit 1 ;;
esac
ffmpeg -y -i "$in" \
  -vf "scale=${w}:${h}:force_original_aspect_ratio=increase,crop=${w}:${h},fps=30,format=yuv420p" \
  -c:v libx264 -crf 20 -preset medium -profile:v high \
  -c:a aac -b:a 160k -ar 48000 -movflags +faststart "$out"
