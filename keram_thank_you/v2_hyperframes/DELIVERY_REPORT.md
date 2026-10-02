# Delivery report — KERAM "Say it to them first" (HyperFrames v0.8.111)

## Output
| | |
|---|---|
| File | `final_reel.mp4` — 1080×1920, 25 fps (source native), H.264 + AAC 48 kHz stereo, 38.4 MB |
| Duration | **52.60 s** = 49.24 s edited dialogue + 0.36 s CTA hold + 3.00 s KERAM outro (matches root `data-duration`) |
| Original | 181.92 s raw take → 49.24 s of kept speech (73 % removed) |
| Loudness | −14.0 LUFS integrated, −1.1 dBFS peak (dialogue master −13.9 LUFS / −1.6 dBTP) |
| Black frames | 0 (blackdetect) · re-transcribed render: every word present, nothing clipped |

## Removed source ranges (s)
0.00–0.40 · 6.32–6.68 · 10.96–15.84 · 18.92–21.20 · 23.48–27.84 · 31.24–36.48 · 39.20–74.88 · 77.84–95.20 · 98.96–105.56 · 108.16–111.28 · 113.52–120.16 · 126.80–137.60 · 142.08–168.76 · 172.36–172.80 · 174.08–181.92
Retake decisions (last complete take kept) are listed in `source-analysis.md`; all 14 kept ranges with output mapping are in `timing-map.json`.

**Cut changes vs v1:** cuts now use energy onsets at −45 dBFS instead of silence midpoints (0.08 s head / 0.10 s tail room). Internal pauses ≥ 0.26 s are removed, and splits that would remove < 0.2 s are merged, so there are no micro jump cuts. Every visible jump cut is covered by a crop punch (5.92, 13.28, 18.96, 44.36 s) or hidden under an interlude.

**Mouth rule (your note):** mouth measured at y≈1020 and chin at y≈1160. Captions sit at y 1236–1368, and punch-ins zoom from an origin below the face (570, 1500), so the face moves up and away from the caption band. No text overlays the face anywhere; the interludes are full-screen.

## Structure
- **7 semantic interludes**: hadith · meaning bridge · step 01 hear it · see us do · Mum/Dad examples · Allah loves / rewarded · CTA "FIRST."
- **A-roll / graphic ratio**: talking head 25.46 s (52 % of the 49.6 s edit) · interludes 24.14 s (48 %) · + 3.0 s outro
- Crop ladder 1.00 / 1.08 / 1.15, plus an opening push 1.00→1.12 over 0.70 s (expo.out)
- 30 word-timed caption cues, 1–4 words, one accent word max; Arabic cues RTL

## Branding (KERAM)
Tokens sampled from the supplied outro and logo cards: cream `#F3E4D0` (the outro background, so the CTA→outro cut is seamless), navy `#142E43`, gold-brown `#A7712F`, blue `#2C6CAF`, light gold `#DFA962`/`#E3B374` on blue.
Blue gradient scenes: hadith and "Allah loves". KERAM logo mark top-right on every interlude, gold on cream and white on blue (extracted from the outro).
Outro: the supplied `KERAM - Logo Outro Vertical 9x16.mp4`, used unaltered with its own audio.

## Fonts
**Cairo** (variable 200–1000; first available family in the prompt's preference list, verified with `fc-list`), shipped locally as `assets/fonts/Cairo.ttf`.
Weights: 900 display · 800 Arabic display / sub-heads · 700 captions & labels · 600 supporting copy. Arabic shaping and tashkeel were checked in snapshots.

## Dependencies & provenance
- Registry: `grain-overlay` (its noise texture is used **statically**; the component's infinite CSS animation was dropped per the determinism rules) and `svg-stroke-trace` (measured-length stroke-draw technique applied inline to brand-coloured icons).
- GSAP 3.14.2 vendored locally (`assets/vendor/gsap.min.js`); no render-time network requests.
- SFX `tick/pop/chime.wav`: generated locally by synthesis (no third-party audio), 11 marks at 5–10 % volume on graphic cuts and locks.
- Icons and illustrations: hand-authored SVG (book, eye, speech bubbles, gift, bowl, helping hands, heart, ribbon).
- Transcription: faster-whisper large-v3 (local), cross-checked against waveform energy and the contact sheet.

## Validation
- `hyperframes lint`: 0 errors, 1 warning (`timeline_track_too_dense` on the caption sub-composition; Studio's one-caption-track convention keeps all 30 cues there)
- `hyperframes check`: **passed**. Runtime 0 errors · layout 0 issues · motion 0 · contrast 18/18 WCAG AA.
  Display rows carry `data-layout-allow-overlap`: Cairo's tall ascender/descender boxes intersect in line-height-1 stacks, and zoomed snapshots verified that no glyphs touch.
- `hyperframes keyframes`: opening push and 9 crop states verified. Boundary snapshots ±1 frame at all 16 world switches, plus push 0/25/50/75/100 %, CTA hold and final frame.
- Animation map reviewed: motion clusters at entrances and builds, with readable holds and no continuous motion.

## Needs your review
1. Hadith pronunciation: one ASR pass heard «يَشْكُرُ … اللَّهِ». The on-screen text uses the canonical tashkeel «يَشْكُرِ … اللَّهَ», so check it by ear.
2. Spoken slip "That's what **was** the Prophet ﷺ said": the on-screen text and SRT drop "was".
3. "Mom" is spelled "Mum" (your script). ASR misheard "loves **that**" as "death"; it is corrected.
4. The Studio preview runs only inside the cloud container (`http://localhost:3002`), so this MP4 is the approval copy.
