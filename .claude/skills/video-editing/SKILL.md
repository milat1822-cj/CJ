---
name: video-editing
description: 將長影片/Podcast 原始檔自動剪輯：語音轉文字、刪除講錯與贅詞、降噪、統一音量、上字幕、輸出 IG / FB 規格短影音。當使用者提到剪片、字幕、降噪、Podcast、Reels、短影音、精華剪輯時使用。
---

# 影片剪輯流程

主要發布平台：**Instagram（Reels / 貼文）與 Facebook（Reels / 動態）**。規格見 `specs/platforms.md`。

## 原則
- **先產出清單，再動手剪。** 刪除清單（cutlist）必須讓使用者確認後才套用；原始檔永遠不覆蓋。
- 所有輸出放 `output/<專案名>/`，中間檔放 `work/`，兩者都不進 git。
- 我不能「看」影片時間軸，判斷依據是逐字稿 + 抽樣畫面 + ffprobe 數據。節奏好不好看，請使用者驗收。

## 流程
1. **環境檢查**：`bash scripts/check_env.sh`，缺什麼就告訴使用者怎麼裝，不要默默跳過。
2. **轉逐字稿**：`python3 scripts/transcribe.py <影片> work/transcript.json`（含逐字時間碼）。
3. **產生刪除清單**：讀逐字稿，找出
   - 講錯後重講（保留最後一次完整的版本）
   - 贅詞（呃、嗯、那個、就是說…過度密集時）
   - 超過 0.8 秒的停頓
   - 離題或與主題無關的段落
   輸出 `work/cutlist.json`，格式見下，並用白話列出每一筆「為什麼刪」給使用者確認。
4. **套用剪輯**：`python3 scripts/apply_cuts.py <影片> work/cutlist.json work/cut.mp4`
5. **音訊處理**：`bash scripts/audio_clean.sh work/cut.mp4 work/clean.mp4`（降噪 + 響度 -16 LUFS）
6. **字幕**：由逐字稿（需重新對齊剪後時間軸）產生 SRT，`bash scripts/burn_subs.sh work/clean.mp4 work/subs.srt work/subbed.mp4`。
7. **短影音精華**：從逐字稿挑 30–60 秒、開頭就有鉤子的片段，另外列清單給使用者選，再各自走 4→6。
8. **輸出平台版本**：`bash scripts/export_social.sh <輸入> <輸出> reels|feed`
9. **自我檢查**：ffprobe 確認解析度/長度/編碼，抽 3–5 張畫面看字幕有沒有被切到、有沒有黑畫面。

## cutlist.json 格式（保留片段）
```json
{
  "keep": [
    {"start": 0.0, "end": 12.4},
    {"start": 15.1, "end": 80.0}
  ],
  "removed": [
    {"start": 12.4, "end": 15.1, "reason": "講錯重講"}
  ]
}
```
`keep` 供程式使用，`removed` 供使用者審核。

## 尚未實作（之後依需求補）
- 動畫圖卡 / B-Roll：用 Remotion（Node），品牌字型與顏色先填 `specs/brand.md`。
- 背景音樂 ducking：ffmpeg `sidechaincompress`，音樂須是有授權的素材。
- 說話者辨識（多人 Podcast）。
