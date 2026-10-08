#!/usr/bin/env bash
# 燒錄字幕。用法: burn_subs.sh <影片> <字幕.srt> <輸出.mp4> [字型名稱]
set -euo pipefail
in="$1"; srt="$2"; out="$3"; font="${4:-Noto Sans CJK TC}"
style="FontName=${font},FontSize=14,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=60"
ffmpeg -y -i "$in" -vf "subtitles='${srt}':force_style='${style}'" -c:a copy -movflags +faststart "$out"
