# Screenshot every demo scene at a few moments -> ../screenshots/edit2/edit2-<scene>-<t>.jpg + one contact sheet.
# Usage: python check.py [scene ids...]
import sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE.parent/'screenshots'/'edit2'; OUT.mkdir(parents=True, exist_ok=True)
TIMES = {'s01': [0.8, 2.4, 4.0], 's02': [0.8, 2.2, 6.6], 's03': [0.6, 5.0, 13.8], 's04': [3.0, 9.5, 12.8], 's05': [3.5, 8.9, 9.9],
         's06': [0.6, 5.5, 11.8], 's07': [1.3, 3.2, 5.4], 's08': [0.45, 2.5, 6.4], 's09': [2.5, 7.4, 9.6], 's10': [1.35, 2.2, 3.6]}

shots = []
with sync_playwright() as p:
    b = p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    pg = b.new_page(viewport={'width': 1280, 'height': 900})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
    pg.goto((HERE/'index.html').as_uri())

    meta = pg.evaluate("SCENES.map(s => [s.id, s.dur, s.poster])")
    want = sys.argv[1:] or [m[0] for m in meta]
    for i, (sid, dur, poster) in enumerate(meta):
        if sid not in want:
            continue
        for t in TIMES.get(sid, [round(dur*.3, 2), round(dur*.62, 2), poster]):
            pg.evaluate("""async ([i, t]) => { const s = SCENES[i]; s.box.scrollIntoView();
                if (!s.v.src) s.v.src = s.v.dataset.src; if (!s.ready) await new Promise(r => { const k = setInterval(() => { if (s.ready) { clearInterval(k); r(); } }, 50); });
                s.v.currentTime = t;
                await new Promise(r => s.v.addEventListener('seeked', r, {once: true})); s.show(t); }""", [i, t])
            pg.wait_for_timeout(250)
            f = OUT/f'edit2-{sid}-{t:05.2f}.jpg'
            pg.locator('.frame').nth(i).screenshot(path=str(f), type='jpeg', quality=85); shots.append(f)
    b.close()
print('errors:', errs[:5])
cols = 3; tw, th = 640, 360
sheet = Image.new('RGB', (cols*tw, ((len(shots)+cols-1)//cols)*th), 'white')
for k, f in enumerate(shots):
    sheet.paste(Image.open(f).convert('RGB').resize((tw, th)), ((k % cols)*tw, (k//cols)*th))
sheet.save(OUT/'edit2-sheet.jpg', quality=85)
print(OUT/'edit2-sheet.jpg', len(shots))
