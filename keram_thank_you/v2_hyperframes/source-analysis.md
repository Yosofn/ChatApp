# Source analysis — rawreel.mp4

| Field | Value |
|---|---|
| Duration | 181.92 s |
| Video | H.264, 720×1280 (9:16), 25 fps CFR, yuvj420p |
| Audio | AAC, 48 kHz, stereo |
| Content | Single static talking head (green polo, warm beige wall, black chair), consistent framing for the whole take |

**Measured framing (1080×1920 canvas):** head top ≈ y540, eyes ≈ y840, mouth ≈ y1020, chin ≈ y1160, face centre x ≈ 570.
→ Captions live at y≈1240–1360 (below the chin). Punch-ins use transform-origin (570px, 1500px) so the face moves **up** when zooming and the mouth never meets the caption band.

**Audio:** speech median ≈ −22 dBFS; pauses are already gated to digital silence (−120 dB), so speech/silence was segmented at −45 dBFS on 10 ms frames and cross-checked with Whisper large-v3 word timings and the contact sheet (`analysis/contact_1fps.jpg`).

## Silence / outtake ranges removed (source seconds)
0.00–0.40 · 6.32–6.68 · 10.96–15.84 · 18.92–21.20 · 23.48–27.84 · 31.24–36.48 · 39.20–74.88 · 77.84–95.20 · 98.96–105.56 · 108.16–111.28 · 113.52–120.16 · 126.80–137.60 · 142.08–168.76 · 172.36–172.80 · 174.08–181.92

Within these: repeated takes and off-camera talk —
- "Children learn a lot…" attempts at 45.4, 48.3, 52.6, 68.4, 71.4 (+ off-camera pronunciation discussion 59.6–65.6) → **kept last complete take 74.88–77.84**
- "Then teach them to notice…" attempt 88.9 ("made") → **kept 95.20–98.96**
- "And you are rewarded for…" fragment 135.4, off-camera 130.1 → **kept 137.60–142.08**
- Closing line attempts 148.7 ("…thank you for you. Just do it"), 159.0, laughter 154.4, off-camera 142.6–147.4 → **kept 168.76–174.08**
- No deliberate teaching repetition exists; every repeat was a correction.

## Semantic beats (output time)
1. Hook — hadith in Arabic (0.0–2.5) + attribution "That's what the Prophet ﷺ said" (2.6–5.8)
2. Translation claim — "Whoever doesn't thank the people doesn't thank Allah ﷻ" (5.9–10.2)
3. Question — "So how do you teach your children to thank you?" (10.2–13.2)
4. Step 1 — "First, let them hear it from us. When your child brings something, say thank you. When they help you, say thank you for helping me." (13.2–21.7)
5. Thesis — "Children learn a lot from what they see us do." (21.7–24.6)
6. Step 2 — "Then teach them to notice when someone makes something kind for them." (24.6–28.4)
7. Examples — "Mum made your food? Say thank you. Dad helped you? Say thank you." (28.4–33.2)
8. Step 3 — "And remind them … Allah subhanahu wa ta'ala loves that from you, and you are rewarded for doing what the Prophet ﷺ taught us to do." (33.2–44.4)
9. CTA — "So today don't just ask your child to say thank you. Say it to them first." (44.4–49.2)
