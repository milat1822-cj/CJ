#!/usr/bin/env python3
"""依 cutlist.json 的 keep 片段剪接影片（重新編碼，切點精準）。
用法: apply_cuts.py <輸入> <cutlist.json> <輸出.mp4>
"""
import json, subprocess, sys

src, cutlist, out = sys.argv[1:4]
keep = json.load(open(cutlist, encoding="utf-8"))["keep"]
if not keep:
    sys.exit("keep 為空，沒有可保留的片段")

parts, labels = [], []
for i, k in enumerate(keep):
    s, e = k["start"], k["end"]
    parts.append(f"[0:v]trim=start={s}:end={e},setpts=PTS-STARTPTS[v{i}];"
                 f"[0:a]atrim=start={s}:end={e},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={max(e-s-0.01,0)}:d=0.01[a{i}]")
    labels.append(f"[v{i}][a{i}]")
graph = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(keep)}:v=1:a=1[v][a]"

subprocess.run(["ffmpeg", "-y", "-i", src, "-filter_complex", graph, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
total = sum(k["end"] - k["start"] for k in keep)
print(f"完成：保留 {len(keep)} 段，共 {total:.1f} 秒 -> {out}")
