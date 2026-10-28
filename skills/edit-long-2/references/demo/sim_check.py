# Screenshot sim.html at given cut-video times -> ../screenshots/edit2/sim-<t>.jpg + sim-sheet.jpg. Needs serve.py on :8765.
# Usage: python sim_check.py [t1 t2 ...]
import sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent/'screenshots'/'edit2'; OUT.mkdir(parents=True, exist_ok=True)
TIMES = [float(x) for x in sys.argv[1:]] or [630, 633.8, 638.8, 643.6, 646, 658.8, 671.5, 675.8, 678.5, 688.9, 695, 703.8, 712, 724.5, 742,
                                             757.5, 767, 773.9, 781, 791.5, 799, 821.8, 836.8, 848.5, 858, 865.5, 875, 903.5, 910, 923.5, 930]
shots = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://localhost:8765/sim.html'); pg.wait_for_function("document.querySelector('#v').readyState >= 2", timeout=60000)
    for t in TIMES:
        pg.evaluate("""async t => { const v = document.querySelector('#v'); v.currentTime = t - 629.4;
            await new Promise(r => v.addEventListener('seeked', r, {once: true})); document.querySelector('#rng').value = t - 629.4;
            document.querySelector('#rng').dispatchEvent(new Event('input')); }""", t)
        pg.wait_for_timeout(200)
        f = OUT/f'sim-{t:06.1f}.jpg'; pg.locator('#fr').screenshot(path=str(f), type='jpeg', quality=85); shots.append((t, f))
    b.close()
print('errors:', errs[:5])
cols, tw, th = 3, 640, 360
sheet = Image.new('RGB', (cols*tw, ((len(shots) + cols - 1)//cols)*th), 'white')
for k, (t, f) in enumerate(shots):
    sheet.paste(Image.open(f).convert('RGB').resize((tw, th)), ((k % cols)*tw, (k//cols)*th))
sheet.save(OUT/'sim-sheet.jpg', quality=80); print(OUT/'sim-sheet.jpg', len(shots))
