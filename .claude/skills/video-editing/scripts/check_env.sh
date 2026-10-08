#!/usr/bin/env bash
# 檢查剪輯所需工具
ok=1
chk() { if command -v "$1" >/dev/null 2>&1; then echo "OK   $1"; else echo "缺   $1  -> $2"; ok=0; fi; }
chk ffmpeg  "apt install ffmpeg / brew install ffmpeg"
chk ffprobe "隨 ffmpeg 安裝"
chk node    "安裝 Node 20+（Remotion 動畫用，選用）"
chk python3 "安裝 Python 3.9+"
python3 -c "import faster_whisper" 2>/dev/null && echo "OK   faster-whisper" || { echo "缺   faster-whisper -> pip install faster-whisper"; ok=0; }
[ $ok -eq 1 ] && echo "環境完整" || echo "請先補齊上面缺少的項目"
