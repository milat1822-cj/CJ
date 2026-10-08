#!/usr/bin/env python3
"""語音轉文字，輸出含逐字時間碼的 JSON。
用法: transcribe.py <影片/音檔> <輸出.json> [模型=small] [語言=zh]
"""
import json, sys
from faster_whisper import WhisperModel

src, out = sys.argv[1], sys.argv[2]
model_name = sys.argv[3] if len(sys.argv) > 3 else "small"
lang = sys.argv[4] if len(sys.argv) > 4 else "zh"

model = WhisperModel(model_name, compute_type="int8")
segments, info = model.transcribe(src, language=lang, word_timestamps=True, vad_filter=False)

result = {"language": info.language, "duration": info.duration, "segments": []}
for s in segments:
    result["segments"].append({
        "start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(),
        "words": [{"w": w.word, "start": round(w.start, 2), "end": round(w.end, 2)} for w in (s.words or [])],
    })
with open(out, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print(f"完成：{len(result['segments'])} 段，總長 {info.duration:.1f} 秒 -> {out}")
