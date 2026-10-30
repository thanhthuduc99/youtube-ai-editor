# Renders demo scenes (index.html) and the screen sim (sim.html) to 1920x1080 30fps videos, frame by frame in Chrome:
# seek the clip, seek the GSAP timeline, screenshot, pipe to ffmpeg. Needs `python serve.py 8766` running and final_plan.py done.
# Usage: python render_scenes.py [ids...]   (no ids = every scene in final_plan.json not rendered yet)  ->  renders/<id>.mp4
#        the tail (face card growing back to full frame) goes to renders/<id>-tail.mp4
import json
import subprocess
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
URL, FPS = 'http://localhost:8766/', 30
plan = {p['id']: p for p in json.loads((HERE/'final_plan.json').read_text(encoding='utf-8'))}
jobs = [(i, '') for i in plan if not (HERE/'renders'/f'{i}.mp4').exists()]
jobs += [(i, '-tail') for i in plan if plan[i].get('tail') and not (HERE/'renders'/f'{i}-tail.mp4').exists()]
jobs = [(i, k) for i, k in jobs if i in sys.argv[1:]] if sys.argv[1:] else jobs
(HERE/'renders').mkdir(exist_ok=True)

# pull one scene's 1920x1080 stage out of the demo list, full size at the top-left corner
SETUP_SCENE = """async ([id, tail]) => {
  const s = SCENES.find(o => o.id === id), st = s.box.querySelector('.stage');
  document.body.appendChild(st); [...document.body.children].forEach(e => e !== st && e.tagName !== 'SCRIPT' && (e.style.display = 'none'));
  st.style.cssText += ';position:fixed;left:0;top:0;transform:none;margin:0';
  window.R = {tl: s.tl, v: s.v};
  if (tail) { const f = st.querySelector('.face'); move(s.tl, f, s.v, FULL, tail); s.tl.to(f, {opacity: 1, duration: .2}, tail); }
}"""
SETUP_SIM = """async () => {
  const st = document.getElementById('st'); document.body.appendChild(st);
  [...document.body.children].forEach(e => e !== st && e.tagName !== 'SCRIPT' && (e.style.display = 'none'));
  st.style.cssText += ';position:fixed;left:0;top:0;transform:none;margin:0';
  window.R = {tl, v: document.getElementById('v')};
}"""
LOAD = """async src => { const v = R.v; v.pause(); v.muted = true; v.removeAttribute('src'); v.src = src;
  await new Promise(r => v.addEventListener('loadeddata', r, {once: true})); }"""
SEEK = """async t => { const v = R.v;
  if (Math.abs(v.currentTime - t) > 1e-4) await new Promise(r => { v.addEventListener('seeked', r, {once: true}); v.currentTime = t; });
  R.tl.time(t); await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); }"""

with sync_playwright() as pw:
    br = pw.chromium.launch(channel='chrome', args=['--autoplay-policy=no-user-gesture-required'])
    for i, kind in jobs:
        p = plan[i]
        k0, k1 = (p['frames'], p['frames'] + p['tail']) if kind else (0, p['frames'])
        pg = br.new_page(viewport={'width': 1920, 'height': 1080})
        pg.route('**/clips/*.mp4', lambda r: r.abort())  # the demo's own 1280px clips: not needed, they eat RAM
        pg.goto(URL + ('sim.html' if i == 'sim' else 'index.html'), wait_until='load')
        pg.evaluate(SETUP_SIM) if i == 'sim' else pg.evaluate(SETUP_SCENE, [i, k0/FPS if kind else 0])
        pg.evaluate("document.fonts.ready.then(() => 1)")
        pg.evaluate(LOAD, f'clips-hd/{i}.mp4')
        tmp = HERE/'renders'/f'{i}{kind}.part.mp4'
        ff = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                               '-c:v', 'h264_nvenc', '-cq', '17', '-pix_fmt', 'yuv420p', '-y', str(tmp)], stdin=subprocess.PIPE)
        for k in range(k0, k1):
            pg.evaluate(SEEK, (k + .5)/FPS)
            for n in range(5):  # low RAM makes Chrome drop a capture now and then
                try:
                    shot = pg.screenshot(type='jpeg', quality=94)
                    break
                except Exception:
                    if n == 4:
                        raise
                    pg.wait_for_timeout(1000)
            ff.stdin.write(shot)
            if k % 300 == 0:
                print(i + kind, k, '/', k1, flush=True)
        ff.stdin.close()
        ff.wait()
        tmp.replace(HERE/'renders'/f'{i}{kind}.mp4')
        pg.close()
        print('done', i + kind, flush=True)
    br.close()
