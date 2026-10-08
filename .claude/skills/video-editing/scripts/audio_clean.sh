#!/usr/bin/env bash
# 降噪 + 響度統一(-16 LUFS)。畫面不重新編碼。
# 用法: audio_clean.sh <輸入> <輸出.mp4>
set -euo pipefail
in="$1"; out="$2"
ffmpeg -y -i "$in" -c:v copy \
  -af "highpass=f=80,afftdn=nr=12:nf=-30,loudnorm=I=-16:TP=-1.5:LRA=11" \
  -c:a aac -b:a 192k -movflags +faststart "$out"
