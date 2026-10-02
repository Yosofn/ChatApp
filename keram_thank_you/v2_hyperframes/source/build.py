#!/usr/bin/env python3
"""Generates index.html + compositions/s*.html from timing-map.json and the verified caption plan.
Re-run after any timing change:  python3 build.py && npx hyperframes lint"""
import json, html, os

ROOT = os.path.dirname(os.path.abspath(__file__))
TM = json.load(open(os.path.join(ROOT, "timing-map.json")))
FPS = 25
CTA_END = 49.6         # last word ends ~48.9 s; CTA card holds ~0.7 s (≈17 frames)
OUTRO = ("assets/media/keram_outro.mp4", 3.0)   # supplied KERAM logo outro, cut in after the CTA hold
TOTAL = round(CTA_END + OUTRO[1], 2)
CAM_ORIGIN = "570px 1500px"   # measured: face x≈570; origin below the face so zooming lifts the face

# ---------------------------------------------------------------- scenes (World B)
# Display rows carry data-layout-allow-overlap: Cairo's ascender/descender boxes (≈1.9em) overlap in tight
# line-height:1 editorial stacks even though the glyphs never touch — verified on zoomed snapshots.
SCENES = [  # id, start, end
    ("s1-hadith",   1.20,  5.92),
    ("s2-bridge",   7.74, 10.20),
    ("s3-hear",    13.86, 17.30),
    ("s4-see",     21.68, 24.64),
    ("s5-examples",28.40, 33.24),
    ("s6-loves",   37.20, 41.28),
    ("s7-cta",     47.96, CTA_END),
]

# ---------------------------------------------------------------- crop ladder (World A)
M, E, C = 1.00, 1.08, 1.15
CROPS = [  # (time, scale, kind)  kind: set = hard punch at a cut / scene return
    (5.92, E, "set"), (10.20, M, "set"), (13.28, C, "set"), (17.30, M, "set"), (18.96, E, "set"),
    (24.64, E, "set"), (33.24, M, "set"), (41.28, E, "set"), (44.36, C, "set"),
]

# ---------------------------------------------------------------- captions (A-roll only)
# (start, end, [(word, t, flag)])  flag: 1 = warm accent, 2 = cool accent ; times = verified output seconds
CAPS = [
    (0.00, 0.82, [("مَنْ", 0.00, 0), ("لَا", 0.22, 0), ("يَشْكُرِ", 0.38, 0)]),
    (0.82, 1.20, [("النَّاسَ", 0.82, 1)]),
    (5.92, 6.72, [("Whoever", 5.92, 0), ("doesn't", 6.08, 0)]),
    (6.72, 7.74, [("thank", 6.72, 1), ("the", 7.02, 0), ("people,", 7.40, 0)]),
    (10.20, 11.12, [("So", 10.20, 0), ("how", 10.42, 0), ("do", 10.80, 0), ("you", 10.96, 0)]),
    (11.12, 12.04, [("teach", 11.12, 1), ("your", 11.46, 0), ("children", 11.58, 0)]),
    (12.04, 13.20, [("to", 12.04, 0), ("thank", 12.40, 0), ("you?", 12.76, 0)]),
    (13.28, 13.86, [("First,", 13.28, 1)]),
    (17.30, 18.80, [("say", 17.30, 0), ("“thank", 17.86, 1), ("you.”", 18.42, 0)]),
    (18.96, 19.86, [("When", 18.96, 0), ("they", 19.10, 0), ("help", 19.26, 2), ("you,", 19.52, 0)]),
    (19.88, 20.76, [("say", 19.88, 0), ("“thank", 20.26, 0), ("you", 20.62, 0)]),
    (20.78, 21.68, [("for", 20.78, 0), ("helping", 20.92, 1), ("me.”", 21.20, 0)]),
    (24.64, 25.46, [("Then", 24.64, 0), ("teach", 24.86, 0), ("them", 25.18, 0)]),
    (25.48, 25.96, [("to", 25.48, 0), ("notice", 25.72, 1)]),
    (25.98, 26.90, [("when", 25.98, 0), ("someone", 26.30, 0), ("makes", 26.60, 0)]),
    (26.92, 27.68, [("something", 26.92, 0), ("kind", 27.24, 1)]),
    (27.70, 28.40, [("for", 27.70, 0), ("them.", 27.92, 0)]),
    (33.24, 34.02, [("And", 33.24, 0), ("remind", 33.38, 1), ("them,", 33.64, 0)]),
    (34.04, 34.96, [("when", 34.04, 0), ("you", 34.34, 0), ("thank", 34.46, 0), ("the", 34.72, 0)]),
    (34.98, 35.46, [("people", 34.98, 0)]),
    (35.48, 36.22, [("for", 35.22, 0), ("something", 35.48, 0), ("good", 35.84, 1)]),
    (36.24, 37.20, [("they", 36.24, 0), ("do", 36.46, 0), ("for", 36.68, 0), ("you,", 36.92, 0)]),
    (41.28, 41.80, [("doing", 41.28, 0), ("what", 41.58, 0)]),
    (41.82, 42.16, [("the", 41.82, 0), ("Prophet", 42.00, 0)]),
    (42.18, 43.40, [("صَلَّى", 42.18, 2), ("اللَّهُ", 42.40, 2), ("عَلَيْهِ", 42.78, 2), ("وَسَلَّمَ", 43.02, 2)]),
    (43.42, 44.34, [("taught", 43.42, 0), ("us", 43.62, 0), ("to", 43.82, 0), ("do.", 44.00, 0)]),
    (44.36, 45.00, [("So", 44.36, 0), ("today,", 44.58, 1)]),
    (45.00, 46.32, [("don't", 45.00, 0), ("just", 45.58, 0), ("ask", 45.82, 1)]),
    (46.34, 46.80, [("your", 46.34, 0), ("child", 46.54, 0)]),
    (46.82, 47.96, [("to", 46.82, 0), ("say", 47.04, 0), ("“thank", 47.24, 1), ("you.”", 47.56, 0)]),
]
# 1-frame gap to the next cue keeps every caption a clean hard replacement
SFX = [  # (file, time, volume)  subtle marks on graphic cuts / locks only
    ("tick.wav", 1.20, 0.10), ("tick.wav", 7.74, 0.10), ("pop.wav", 8.74, 0.07), ("tick.wav", 13.86, 0.10),
    ("tick.wav", 21.68, 0.10), ("tick.wav", 28.40, 0.10), ("pop.wav", 31.00, 0.06), ("tick.wav", 37.20, 0.10),
    ("pop.wav", 38.62, 0.06), ("tick.wav", 47.96, 0.10), ("chime.wav", 48.60, 0.05),
]

SFX_LEN = {"tick.wav": 0.05, "pop.wav": 0.12, "chime.wav": 1.40}

def is_ar(s): return any("؀" <= ch <= "ۿ" or "ﷰ" <= ch <= "﷿" for ch in s)

FONT_FACE = """@font-face{font-family:"Cairo";src:url("assets/fonts/Cairo.ttf") format("truetype");font-weight:200 1000;font-display:block}"""
FONT_FACE_SUB = FONT_FACE

# KERAM brand tokens (sampled from the KERAM outro + logo cards): cream paper, navy ink, gold-brown + blue accents
TOKENS = """--paper:#F3E4D0;--paper-dark:#E4CFB3;--paper-light:#FAF2E6;--cream:#FFFAF2;--ink:#142E43;--ink-soft:#3D566C;
--accent-warm:#A7712F;--accent-warm-dark:#8A5A22;--accent-cool:#2C6CAF;--accent-cool-dark:#1F4A75;--accent-gold:#DFA962;"""
BLUE = """--paper:#2C6CAF;--paper-light:#3A7CC0;--paper-dark:#142E43;--cream:#1F4A75;--ink:#FFFFFF;--ink-soft:#D9E6F3;
--accent-warm:#E3B374;--accent-warm-dark:#C08847;--accent-cool:#9CCBF2;"""
GRAIN = ("url(\"data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E"
         "%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E"
         "%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")")

# ======================================================================= index.html
def build_index():
    vids, caps, sfx = [], [], []
    for i, r in enumerate(TM["ranges"]):
        vids.append(f'''      <video id="ar-{i:02d}" class="ar-vid" src="assets/media/rawreel_dialogue.mp4" data-start="{r['out_start']:.2f}" data-duration="{r['dur']:.2f}" data-media-start="{r['src_start']:.2f}" data-track-index="0" playsinline data-has-audio="true"></video>''')
    capsub = build_captions()
    for i, (f, t, v) in enumerate(SFX):
        sfx.append(f'''    <audio id="sfx-{i:02d}" src="assets/sfx/{f}" data-start="{t:.2f}" data-duration="{SFX_LEN[f]:.2f}" data-track-index="{4 + i % 2}" data-volume="{v}"></audio>''')
    scenes = [f'''    <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{s:.2f}" data-duration="{e - s:.2f}" data-track-index="2" data-width="1080" data-height="1920"></div>''' for sid, s, e in SCENES]

    js = []
    js.append(f'tl.fromTo("#cam",{{scale:1}},{{scale:1.12,duration:0.70,ease:"expo.out"}},0);')
    for t, sc, kind in CROPS:
        js.append(f'tl.set("#cam",{{scale:{sc}}},{t:.2f});')
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Say it to them first — reel</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      {FONT_FACE}
      :root{{{TOKENS}}}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:#142E43; }}
      #root {{ position:relative; width:100%; height:100%; overflow:hidden; background:#142E43; font-family:"Cairo", sans-serif; }}
      #cam {{ position:absolute; inset:0; transform-origin:{CAM_ORIGIN}; }}
      .outro-vid {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
      .ar-vid {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{TOTAL}" data-fps="{FPS}">
    <div id="cam">
{chr(10).join(vids)}
    </div>
{chr(10).join(scenes)}
    <video id="outro" class="outro-vid" src="{OUTRO[0]}" data-start="{CTA_END:.2f}" data-duration="{OUTRO[1]:.2f}" data-media-start="0" data-track-index="1" playsinline data-has-audio="true"></video>
    <div id="captions" data-track-kind="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-width="1080" data-height="1920"></div>
{chr(10).join(sfx)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join('      ' + l for l in js).lstrip()}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''

RTL = ' dir="rtl"'

def build_captions():
    caps, js = [], []
    for i, (s, e, words) in enumerate(CAPS):
        ar = all(is_ar(w) for w, _, _ in words)
        spans = "".join(f'<span class="w{" ar" if is_ar(w) else ""}" id="cw-{i:02d}-{j}">{html.escape(w)}</span>' for j, (w, _, _) in enumerate(words))
        caps.append(f'''        <div id="cap-{i:02d}" class="clip cap" data-start="{s:.2f}" data-duration="{e - s:.2f}" data-track-index="0"><div class="cap-in" id="capin-{i:02d}"{RTL if ar else ""}>{spans}</div></div>''')
        js.append(f'tl.fromTo("#capin-{i:02d}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.12,ease:"power2.out"}},{s:.2f});')
        for j, (w, t, flag) in enumerate(words):
            col = {1: "#E8B26A", 2: "#9CCBF2"}.get(flag)
            tt = max(t, s)
            js.append(f'tl.fromTo("#cw-{i:02d}-{j}",{{opacity:0.6}},{{opacity:1,duration:0.08,ease:"none"}},{tt:.2f});')
            if col:
                js.append(f'tl.fromTo("#cw-{i:02d}-{j}",{{color:"#FFFDF8"}},{{color:"{col}",duration:0.08,ease:"none",immediateRender:false}},{tt:.2f});')
    src = f'''<!doctype html>
<html lang="en">
  <head><meta charset="UTF-8" /><title>captions</title></head>
  <body>
    <template>
      <style>
        {FONT_FACE}
        #root {{ position:absolute; inset:0; pointer-events:none; }}
        .cap {{ position:absolute; left:80px; right:80px; top:1236px; height:132px; display:flex; align-items:center; justify-content:center; }}
        .cap-in {{ display:flex; flex-wrap:wrap; justify-content:center; align-items:baseline; gap:0 18px; max-width:920px; text-align:center;
                  font-family:"Cairo", sans-serif; font-weight:700; font-size:60px; line-height:1.15; color:#FFFDF8;
                  text-shadow:0 2px 3px rgba(27,29,30,.55), 0 6px 22px rgba(27,29,30,.45); }}
        .cap-in .w {{ display:inline-block; }}
        .cap-in .w.ar {{ font-size:66px; font-weight:800; line-height:1.6; }}
      </style>
      <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(caps)}
      </div>
      <script>
        (function () {{
          const tl = gsap.timeline({{ paused: true }});
          {chr(10).join('          ' + l for l in js).lstrip()}
          window.__timelines["captions"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
'''
    open(os.path.join(ROOT, "compositions", "captions.html"), "w").write(src)

# ======================================================================= scene helpers
def page(sid, body, script, extra_css="", dy=0, theme="cream"):
    return f'''<!doctype html>
<html lang="en">
  <head><meta charset="UTF-8" /><title>{sid}</title></head>
  <body>
    <template>
      <style>
        {FONT_FACE_SUB}
        #root {{ position:absolute; inset:0; overflow:hidden; {TOKENS} background:var(--paper); font-family:"Cairo", sans-serif; color:var(--ink); }}
        {"#root { " + BLUE + " }" if theme == "blue" else ""}
        #{sid}-bg {{ position:absolute; inset:0; background:{"linear-gradient(180deg, #2C6CAF 0%, #23578E 45%, #142E43 100%)" if theme == "blue" else "radial-gradient(120% 80% at 50% 42%, var(--paper-light) 0%, var(--paper) 58%, var(--paper-dark) 100%)"}; }}
        #{sid}-logo {{ position:absolute; right:80px; top:{150 - dy}px; width:118px; height:auto; }}
        #{sid}-grain {{ position:absolute; inset:0; background:{GRAIN}; background-size:256px 256px; opacity:{".06" if theme == "blue" else ".10"}; mix-blend-mode:{"soft-light" if theme == "blue" else "multiply"}; }}
        #{sid}-label {{ position:absolute; left:80px; top:{176 - dy}px; font-weight:700; font-size:30px; letter-spacing:.32em; color:var(--ink-soft); }}
        #{sid}-label b {{ color:var(--accent-warm); font-weight:800; }}
        .{sid}-svg {{ position:absolute; overflow:visible; }}
        .{sid}-svg .ink {{ fill:none; stroke:var(--ink); stroke-width:7; stroke-linecap:round; stroke-linejoin:round; }}
        .{sid}-row {{ position:absolute; left:80px; right:80px; display:flex; justify-content:center; align-items:baseline; flex-wrap:wrap; text-align:center; }}
        .{sid}-row .t {{ display:inline-block; }}
        .{sid}-mask {{ margin-top:28px; }}
        {extra_css}
      </style>
      <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
        <div id="{sid}-bg"></div>
        <div id="{sid}-grain"></div>
        <div id="{sid}-stage" data-layout-allow-overflow style="position:absolute;inset:0;transform:translateY({dy}px)">
        <img id="{sid}-logo" src="assets/keram_logo_{"white" if theme == "blue" else "gold"}.png" alt="KERAM" />
{body}
        </div>
      </div>
      <script>
        (function () {{
          const tl = gsap.timeline({{ paused: true }});
          const draw = (sel, at, dur) => {{
            document.querySelectorAll(sel).forEach((p) => {{
              const L = p.getTotalLength();
              tl.fromTo(p, {{ strokeDasharray: L, strokeDashoffset: L }}, {{ strokeDashoffset: 0, duration: dur, ease: "power2.inOut" }}, at);
            }});
          }};
          const rise = (sel, at, d = 0.32, y = 70) => tl.fromTo(sel, {{ yPercent: y, opacity: 0 }}, {{ yPercent: 0, opacity: 1, duration: d, ease: "power3.out" }}, at);
          const settle = (sel, at, d = 0.36) => tl.fromTo(sel, {{ scale: 1.18, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: d, ease: "expo.out" }}, at);
{script}
          window.__timelines["{sid}"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
'''

def T(t, s0): return round(t - s0, 2)   # output time → scene-local time

def s1():
    sid, s0 = "s1-hadith", 1.20
    body = f'''        <div id="{sid}-label">HADITH <b>·</b> THE PROPHET ﷺ</div>
        <svg class="{sid}-svg" style="left:300px;top:330px;width:480px;height:300px" viewBox="0 0 480 300">
          <path class="ink" d="M240 70 C190 40 110 34 30 50 L30 250 C110 234 190 240 240 270 C290 240 370 234 450 250 L450 50 C370 34 290 40 240 70 Z"/>
          <path class="ink" d="M240 70 L240 270"/>
          <path class="ink" style="stroke-width:4;opacity:.55" d="M80 110 C130 102 180 104 210 116 M80 150 C130 142 180 144 210 156 M270 116 C300 104 350 102 400 110 M270 156 C300 144 350 142 400 150"/>
        </svg>
        <div data-layout-allow-overlap class="{sid}-row {sid}-mask" id="{sid}-l1" dir="rtl" style="top:700px">
          <span class="t" style="font-weight:800;font-size:112px;line-height:1.55">مَنْ لَا <span style="color:var(--accent-warm)">يَشْكُرِ</span> النَّاسَ</span>
        </div>
        <div data-layout-allow-overlap class="{sid}-row {sid}-mask" dir="rtl" style="top:900px;gap:0 34px">
          <span data-layout-allow-overlap class="t" id="{sid}-w1" style="font-weight:800;font-size:112px;line-height:1.55">لَا</span>
          <span data-layout-allow-overlap class="t" id="{sid}-w2" style="font-weight:800;font-size:112px;line-height:1.55;color:var(--accent-warm)">يَشْكُرِ</span>
          <span data-layout-allow-overlap class="t" id="{sid}-w3" style="font-weight:800;font-size:112px;line-height:1.55">اللَّهَ</span>
        </div>
        <div id="{sid}-rule" style="position:absolute;left:390px;top:1150px;width:300px;height:8px;border-radius:8px;background:var(--accent-warm);transform-origin:50% 50%"></div>
        <div data-layout-allow-overlap class="{sid}-row" id="{sid}-attr" style="top:1220px;font-weight:600;font-size:50px;color:var(--ink-soft)">That’s what the Prophet ﷺ said</div>'''
    script = f'''          draw("#root svg .ink", 0, 0.55);
          rise("#{sid}-l1 .t", 0, 0.30, 60);
          rise("#{sid}-w1", {T(1.24, s0)});
          rise("#{sid}-w2", {T(1.74, s0)});
          rise("#{sid}-w3", {T(2.12, s0)});
          tl.fromTo("#{sid}-rule", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4, ease: "power3.out" }}, {T(2.56, s0)});
          rise("#{sid}-attr", {T(3.62, s0)}, 0.34, 40);'''
    return sid, page(sid, body, script, dy=150, theme="blue")

def s2():
    sid, s0 = "s2-bridge", 7.74
    body = f'''        <div id="{sid}-label">WHAT IT MEANS</div>
        <div data-layout-allow-overlap class="{sid}-row" id="{sid}-ctx" style="top:330px;font-weight:600;font-size:50px;color:var(--ink-soft)">Whoever doesn’t thank</div>
        <div id="{sid}-people" style="position:absolute;left:290px;top:430px;width:500px;height:150px;border:7px solid var(--ink);border-radius:80px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:84px;letter-spacing:.06em;background:var(--cream)">PEOPLE</div>
        <svg class="{sid}-svg" style="left:500px;top:600px;width:80px;height:340px" viewBox="0 0 80 340">
          <path class="ink" d="M40 0 L40 320"/><path class="ink" d="M12 290 L40 322 L68 290"/>
        </svg>
        <div id="{sid}-verb" style="position:absolute;left:600px;top:720px;font-weight:700;font-size:48px;color:var(--ink-soft)">doesn’t thank</div>
        <div data-layout-allow-overlap class="{sid}-row" id="{sid}-allah" style="top:960px;font-weight:900;font-size:220px;line-height:1;color:var(--accent-warm);letter-spacing:.02em">ALLAH</div>
        <div data-layout-allow-overlap class="{sid}-row" id="{sid}-swt" dir="rtl" style="top:1210px;font-weight:800;font-size:84px;line-height:1.6;color:var(--accent-cool)">سُبْحَانَهُ وَتَعَالَى</div>'''
    script = f'''          rise("#{sid}-ctx", 0, 0.28, 40);
          settle("#{sid}-people", 0, 0.32);
          draw("#root svg .ink", 0.24, 0.5);
          rise("#{sid}-verb", {T(8.36, s0)}, 0.28, 40);
          settle("#{sid}-allah", {T(8.74, s0)}, 0.4);
          rise("#{sid}-swt", {T(9.00, s0)}, 0.32, 50);'''
    return sid, page(sid, body, script, dy=120)

def s3():
    sid, s0 = "s3-hear", 13.86
    body = f'''        <div id="{sid}-label"><b>01</b> &nbsp;STEP ONE</div>
        <svg class="{sid}-svg" style="left:250px;top:300px;width:580px;height:400px" viewBox="0 0 580 400">
          <path class="ink" d="M70 40 H470 a40 40 0 0 1 40 40 V230 a40 40 0 0 1 -40 40 H230 L140 340 L160 270 H70 a40 40 0 0 1 -40 -40 V80 a40 40 0 0 1 40 -40 Z"/>
          <path class="ink arc" style="stroke:var(--accent-warm)" d="M540 120 q24 35 0 70"/><path class="ink arc" style="stroke:var(--accent-warm)" d="M566 92 q44 63 0 126"/>
        </svg>
        <div id="{sid}-quote" style="position:absolute;left:280px;top:378px;width:480px;text-align:center;font-weight:700;font-size:62px;color:var(--ink)">“Thank you.”</div>
        <div data-layout-allow-overlap class="{sid}-row {sid}-mask" style="top:760px"><span data-layout-allow-overlap class="t" id="{sid}-let" style="font-weight:600;font-size:64px;color:var(--ink-soft)">let them</span></div>
        <div data-layout-allow-overlap class="{sid}-row {sid}-mask" style="top:850px;gap:0 36px"><span data-layout-allow-overlap class="t" id="{sid}-hear" style="font-weight:900;font-size:200px;line-height:1;color:var(--accent-warm)">HEAR</span><span data-layout-allow-overlap class="t" id="{sid}-it" style="font-weight:900;font-size:200px;line-height:1">IT</span></div>
        <div data-layout-allow-overlap class="{sid}-row {sid}-mask" style="top:1100px"><span data-layout-allow-overlap class="t" id="{sid}-us" style="font-weight:800;font-size:92px">from us.</span></div>
        <div id="{sid}-mod" style="position:absolute;left:110px;right:110px;top:1350px;height:170px;border:5px solid var(--ink);border-radius:36px;background:var(--cream);display:flex;align-items:center;gap:30px;padding:0 40px">
          <svg style="width:110px;height:110px;flex:none;overflow:visible" viewBox="0 0 110 110"><g fill="none" stroke="#142E43" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"><rect x="10" y="44" width="90" height="58" rx="6"/><rect x="4" y="28" width="102" height="20" rx="5"/><path d="M55 28 V102"/><path d="M55 28 C40 4 16 12 28 24 C34 30 55 28 55 28 Z M55 28 C70 4 94 12 82 24 C76 30 55 28 55 28 Z" stroke="#A7712F"/></g></svg>
          <div style="font-weight:700;font-size:50px;line-height:1.15;color:var(--ink)">When your child brings something…</div>
        </div>'''
    script = f'''          draw("#root svg .ink:not(.arc)", 0, 0.5);
          rise("#{sid}-quote", 0.28, 0.3, 40);
          rise("#{sid}-let", 0, 0.28);
          rise("#{sid}-hear", {T(14.38, s0)}, 0.32, 80);
          rise("#{sid}-it", {T(14.60, s0)}, 0.28, 80);
          draw("#root svg .arc", {T(14.38, s0)}, 0.4);
          rise("#{sid}-us", {T(14.74, s0)}, 0.3);
          tl.fromTo("#{sid}-mod", {{ y: 120, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.36, ease: "power3.out" }}, {T(15.38, s0)});'''
    return sid, page(sid, body, script, dy=70)

def s4():
    sid, s0 = "s4-see", 21.68
    body = f'''        <div id="{sid}-label">HOW CHILDREN LEARN</div>
        <svg class="{sid}-svg" style="left:240px;top:330px;width:600px;height:300px" viewBox="0 0 600 300">
          <path class="ink" d="M20 150 C130 20 470 20 580 150 C470 280 130 280 20 150 Z"/>
          <g id="{sid}-iris"><circle class="ink" cx="300" cy="150" r="78"/><circle cx="300" cy="150" r="34" fill="#142E43"/></g>
        </svg>
        <div data-layout-allow-overlap class="{sid}-row" style="top:720px;gap:0 22px;font-weight:700;font-size:70px">
          <span data-layout-allow-overlap class="t" id="{sid}-a">Children</span><span data-layout-allow-overlap class="t" id="{sid}-b">learn</span><span data-layout-allow-overlap class="t" id="{sid}-c">a lot</span>
        </div>
        <div data-layout-allow-overlap class="{sid}-row" style="top:830px;font-weight:600;font-size:66px;color:var(--ink-soft)"><span data-layout-allow-overlap class="t" id="{sid}-d">from what they</span></div>
        <div data-layout-allow-overlap class="{sid}-row {sid}-mask" style="top:930px"><span data-layout-allow-overlap class="t" id="{sid}-see" style="font-weight:900;font-size:270px;line-height:1;color:var(--accent-warm)">SEE</span></div>
        <div data-layout-allow-overlap class="{sid}-row {sid}-mask" style="top:1220px"><span data-layout-allow-overlap class="t" id="{sid}-usdo" style="font-weight:900;font-size:170px;line-height:1">US DO.</span></div>'''
    script = f'''          draw("#root svg .ink", 0, 0.55);
          tl.fromTo("#{sid}-iris", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 0.3);
          rise("#{sid}-a", 0, 0.26, 50);
          rise("#{sid}-b", {T(22.02, s0)}, 0.26, 50);
          rise("#{sid}-c", {T(22.52, s0)}, 0.26, 50);
          rise("#{sid}-d", {T(23.18, s0)}, 0.26, 50);
          rise("#{sid}-see", {T(23.66, s0)}, 0.3, 90);
          tl.to("#{sid}-iris", {{ x: 0, y: -10, scale: 1.12, transformOrigin: "300px 150px", duration: 0.3, ease: "power3.out" }}, {T(23.66, s0)});
          rise("#{sid}-usdo", {T(23.92, s0)}, 0.28, 90);'''
    return sid, page(sid, body, script, dy=170)

def s5():
    sid, s0 = "s5-examples", 28.40
    mod = lambda n, top, icon, q: f'''        <div id="{sid}-m{n}" class="{sid}-mod" style="top:{top}px">
          <div class="{sid}-ic">{icon}</div>
          <div><div class="{sid}-q">{q}</div><div class="{sid}-a" id="{sid}-a{n}">“Thank you.”</div></div>
        </div>'''
    bowl = '<svg viewBox="0 0 140 140" style="width:140px;height:140px;overflow:visible"><g fill="none" stroke="#142E43" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 66 H128 C126 104 100 124 70 124 C40 124 14 104 12 66 Z"/><path d="M46 52 c-8 -14 8 -20 0 -34 M70 52 c-8 -14 8 -20 0 -34 M94 52 c-8 -14 8 -20 0 -34" stroke="#A7712F"/></g></svg>'
    hands = '<svg viewBox="0 0 140 140" style="width:140px;height:140px;overflow:visible"><g fill="none" stroke="#142E43" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"><rect x="34" y="42" width="72" height="56" rx="6"/><path d="M34 62 H106"/><path d="M8 110 C22 98 30 96 34 96 M132 110 C118 98 110 96 106 96"/><path d="M70 30 c-10 -8 -16 -13 -16 -19 a7 7 0 0 1 16 -3 a7 7 0 0 1 16 3 c0 6 -6 11 -16 19 z" stroke="#A7712F"/></g></svg>'
    css = f'''.{sid}-mod {{ position:absolute; left:90px; right:90px; height:400px; border:6px solid var(--ink); border-radius:44px; background:var(--cream);
             display:flex; align-items:center; gap:40px; padding:0 54px; transform-origin:50% 50%; }}
        .{sid}-ic {{ flex:none; width:150px; height:150px; display:grid; place-items:center; }}
        .{sid}-q {{ font-weight:800; font-size:72px; line-height:1.1; }}
        .{sid}-a {{ font-weight:900; font-size:86px; line-height:1.3; color:var(--accent-warm); }}'''
    body = f'''        <div id="{sid}-label">NOTICE <b>·</b> THEN SAY IT</div>
{mod(1, 330, bowl, "Mum made your food?")}
{mod(2, 830, hands, "Dad helped you?")}'''
    script = f'''          tl.fromTo("#{sid}-m1", {{ y: 160, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.36, ease: "power3.out" }}, 0);
          rise("#{sid}-a1", {T(30.20, s0)}, 0.28, 60);
          tl.fromTo("#{sid}-m2", {{ y: 160, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.36, ease: "power3.out" }}, {T(31.00, s0)});
          tl.to("#{sid}-m1", {{ scale: 0.94, borderColor: "#3D566C", duration: 0.3, ease: "power2.out" }}, {T(31.00, s0)});
          tl.to("#{sid}-a1", {{ color: "#2C6CAF", duration: 0.3 }}, {T(31.00, s0)});
          tl.to("#{sid}-m2", {{ borderColor: "#A7712F", duration: 0.2 }}, {T(31.20, s0)});
          rise("#{sid}-a2", {T(32.44, s0)}, 0.28, 60);'''
    return sid, page(sid, body, script, css, dy=90)

def s6():
    sid, s0 = "s6-loves", 37.20
    body = f'''        <div id="{sid}-label"><b>03</b> &nbsp;REMIND THEM</div>
        <div id="{sid}-p1" style="position:absolute;inset:0">
          <svg class="{sid}-svg" style="left:380px;top:320px;width:320px;height:290px" viewBox="0 0 320 290">
            <path id="{sid}-heart" class="ink" d="M160 270 C60 200 16 150 16 96 a72 72 0 0 1 144 -18 a72 72 0 0 1 144 18 c0 54 -44 104 -144 174 z"/>
          </svg>
          <div data-layout-allow-overlap class="{sid}-row" id="{sid}-allah" style="top:690px;font-weight:800;font-size:110px;line-height:1">Allah</div>
          <div data-layout-allow-overlap class="{sid}-row" id="{sid}-swt" dir="rtl" style="top:820px;font-weight:800;font-size:88px;line-height:1.6;color:var(--accent-cool)">سُبْحَانَهُ وَتَعَالَى</div>
          <div data-layout-allow-overlap class="{sid}-row {sid}-mask" style="top:990px"><span data-layout-allow-overlap class="t" id="{sid}-loves" style="font-weight:900;font-size:240px;line-height:1;color:var(--accent-warm)">LOVES</span></div>
          <div data-layout-allow-overlap class="{sid}-row" id="{sid}-that" style="top:1300px;font-weight:700;font-size:70px">that from you</div>
        </div>
        <div id="{sid}-p2" style="position:absolute;inset:0;opacity:0">
          <svg class="{sid}-svg" style="left:410px;top:330px;width:260px;height:340px" viewBox="0 0 260 340">
            <circle class="ink p2" cx="130" cy="120" r="100"/><path class="ink p2" d="M130 62 l17 35 38 5 -28 26 7 38 -34 -18 -34 18 7 -38 -28 -26 38 -5 z" style="stroke:var(--accent-warm)"/>
            <path class="ink p2" d="M78 205 L50 330 L100 300 L130 336 M182 205 L210 330 L160 300 L130 336"/>
          </svg>
          <div data-layout-allow-overlap class="{sid}-row" id="{sid}-you" style="top:760px;font-weight:700;font-size:74px;color:var(--ink-soft)">and you are</div>
          <div data-layout-allow-overlap class="{sid}-row {sid}-mask" style="top:850px"><span data-layout-allow-overlap class="t" id="{sid}-rew" style="font-weight:900;font-size:176px;line-height:1;color:var(--accent-warm)">REWARDED</span></div>
        </div>'''
    script = f'''          draw("#{sid}-heart", 0, 0.55);
          rise("#{sid}-allah", 0, 0.28, 40);
          rise("#{sid}-swt", {T(38.04, s0)}, 0.3, 50);
          tl.to("#{sid}-heart", {{ fill: "#DFA962", stroke: "#C08847", duration: 0.25, ease: "power2.out" }}, {T(38.62, s0)});
          rise("#{sid}-loves", {T(38.62, s0)}, 0.3, 90);
          rise("#{sid}-that", {T(38.92, s0)}, 0.26, 40);
          tl.to("#{sid}-p1", {{ yPercent: -6, opacity: 0, duration: 0.2, ease: "power2.in" }}, {T(39.66, s0)});
          tl.to("#{sid}-p2", {{ opacity: 1, duration: 0.04 }}, {T(39.82, s0)});
          draw("#root .p2", {T(39.86, s0)}, 0.5);
          rise("#{sid}-you", {T(39.86, s0)}, 0.26, 40);
          rise("#{sid}-rew", {T(40.32, s0)}, 0.3, 90);'''
    return sid, page(sid, body, script, dy=130, theme="blue")

def s7():
    sid, s0 = "s7-cta", 47.96
    body = f'''        <div id="{sid}-label">TODAY</div>
        <svg class="{sid}-svg" style="left:300px;top:330px;width:480px;height:330px" viewBox="0 0 480 330">
          <path class="ink" d="M60 30 H420 a40 40 0 0 1 40 40 V200 a40 40 0 0 1 -40 40 H200 L110 310 L130 240 H60 a40 40 0 0 1 -40 -40 V70 a40 40 0 0 1 40 -40 Z"/>
          <path class="ink" style="stroke:var(--accent-warm)" d="M150 135 h180"/>
        </svg>
        <div data-layout-allow-overlap class="{sid}-row" id="{sid}-say" style="top:760px;font-weight:800;font-size:96px;line-height:1">Say it to them</div>
        <div data-layout-allow-overlap class="{sid}-row {sid}-mask" style="top:860px"><span data-layout-allow-overlap class="t" id="{sid}-first" style="font-weight:900;font-size:250px;line-height:1;color:var(--accent-warm)">FIRST.</span></div>
        <div data-layout-allow-overlap class="{sid}-row" id="{sid}-ar" dir="rtl" style="top:1200px;font-weight:800;font-size:80px;line-height:1.6;color:var(--accent-cool)">قُلْهَا لَهُمْ أَوَّلًا</div>'''
    script = f'''          draw("#root svg .ink", 0, 0.4);
          rise("#{sid}-say", 0, 0.24, 40);
          settle("#{sid}-first", {T(48.56, s0)}, 0.36);
          rise("#{sid}-ar", {T(48.90, s0)}, 0.3, 50);'''
    return sid, page(sid, body, script, dy=120)

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    open(os.path.join(ROOT, "index.html"), "w").write(build_index())
    for fn in (s1, s2, s3, s4, s5, s6, s7):
        sid, src = fn()
        open(os.path.join(ROOT, "compositions", f"{sid}.html"), "w").write(src)
    a = sum(e - s for _, s, e in SCENES)
    a2=0
    print(f"built: {len(TM['ranges'])} A-roll ranges, {len(SCENES)} scenes ({a:.2f}s = {a / TOTAL * 100:.0f}% graphic), {len(CAPS)} caption cues")
