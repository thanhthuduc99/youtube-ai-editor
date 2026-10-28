# Approval samples without rendering any video. Playwright opens each overlay composition over a local HTTP server,
# seeks the GSAP timeline (+ hf-seek for Three.js, + <video> currentTime), screenshots it with a transparent
# background and lays it over the real source frame at that moment. Checks fonts, JS errors, frame edges, webcam
# collisions and text overflow. Writes review/index.html, review/contact-*.jpg, review/preview-qa.json.
# Usage: python scripts/preview.py            (all overlays)
#        python scripts/preview.py --gallery  (rebuild the gallery only, e.g. after clips.py)
#        python scripts/preview.py ov-004 ...  (only these; the gallery keeps the others' previous frames)
import asyncio, functools, html, http.server, json, os, shutil, sys, threading
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
from common import R, P, FPS, SKILL, ff, video, load_json

O = load_json('overlays.json'); plan = load_json('edit-plan.json')
only = set(sys.argv[1:])
Q = R/'review'; FR = Q/'frames'; SRC = Q/'src'
for d in (FR, SRC):
    d.mkdir(parents=True, exist_ok=True)
FACE = plan.get('layout', {}).get('face')
SAFE = 24

SEEK = '''async ([id, t]) => {
  const tl = window.__timelines && window.__timelines[id]; if (tl) tl.seek(t);
  for (const v of document.querySelectorAll('video')) {
    const s = +(v.dataset.start || 0);
    await new Promise(r => { if (v.readyState >= 1) r(); else v.addEventListener('loadedmetadata', r, {once: true}); setTimeout(r, 5000); });
    await new Promise(r => { v.addEventListener('seeked', r, {once: true}); v.currentTime = Math.max(0, t - s) + 0.001; setTimeout(r, 5000); });
    // like the HyperFrames renderer: paint the decoded frame into an <img> next to the video (a <video> inside a 3D-transformed
    // layer otherwise keeps showing a stale frame in screenshots)
    const c = document.createElement('canvas'); c.width = v.videoWidth; c.height = v.videoHeight; c.getContext('2d').drawImage(v, 0, 0);
    let im = v.nextElementSibling;
    if (!im || !im.classList.contains('__pv_frame__')) { im = document.createElement('img'); im.className = '__pv_frame__'; v.after(im); }
    const cs = getComputedStyle(v);
    im.style.cssText = `position:absolute;left:${v.offsetLeft}px;top:${v.offsetTop}px;width:${v.offsetWidth}px;height:${v.offsetHeight}px;object-fit:${cs.objectFit};border-radius:${cs.borderRadius}`;
    im.src = c.toDataURL('image/jpeg', .92); await im.decode().catch(() => {}); v.style.visibility = 'hidden';
  }
  if (window.__ready3d) { await window.__ready3d; window.__hfThreeTime = t; window.dispatchEvent(new CustomEvent('hf-seek', {detail: {time: t}})); }
  await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
}'''
CHECK = '''([full, face, safe]) => {
  const eff = e => { let o = 1; for (let n = e; n && n.nodeType === 1; n = n.parentElement) o *= +getComputedStyle(n).opacity; return o; };
  const out = [];
  const els = [...document.querySelectorAll('#root *')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 2 && r.height > 2 && eff(e) > .05; });
  for (const e of els) {
    const txt = (e.innerText || '').trim().slice(0, 60);
    const isText = e.children.length === 0 && txt;
    let r = e.getBoundingClientRect();
    if (isText) { const rg = document.createRange(); rg.selectNodeContents(e); r = rg.getBoundingClientRect(); }  // glyph extents, not the block
    if (isText && (e.scrollWidth > e.clientWidth + 2)) out.push({kind: 'text-overflow', text: txt});
    if (full && !isText) continue;
    if (e.matches('.canvas,.stage,.layer,.pos,.chips,.sws,.scene,.deco,canvas,svg,svg *')) continue;
    if (r.left < safe || r.top < safe || r.right > 1920 - safe || r.bottom > 1080 - safe) out.push({kind: 'edge', text: txt || e.className, box: [r.left, r.top, r.right, r.bottom].map(Math.round)});
    if (!full && face && r.left < face[2] && r.right > face[0] && r.top < face[3] && r.bottom > face[1]) out.push({kind: 'covers-webcam', text: txt || e.className});
  }
  const used = new Set(els.filter(e => e.children.length === 0 && (e.innerText || '').trim()).map(e => getComputedStyle(e).fontFamily.split(',')[0].replace(/["']/g, '').trim()));
  const ok = new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/["']/g, '')));
  const fonts = [...used].filter(f => !ok.has(f)).map(f => [f, 'not loaded']);
  return {fails: out, fonts};
}'''


class Quiet(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, '.js': 'text/javascript', '.mjs': 'text/javascript',
                      '.wasm': 'application/wasm', '.glb': 'model/gltf-binary'}

    def log_message(self, *a):
        pass

    def send_head(self):  # byte ranges: without them Chrome cannot seek a <video> and every sample shows frame 0
        rng = self.headers.get('Range')
        if not rng or not rng.startswith('bytes='):
            return super().send_head()
        path = self.translate_path(self.path)
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404); return None
        size = os.fstat(f.fileno()).st_size
        a, _, b = rng[6:].partition('-')
        a = int(a or 0); b = min(int(b) if b else size - 1, size - 1)
        self.send_response(206)
        for k, v in (('Content-Type', self.guess_type(path)), ('Accept-Ranges', 'bytes'), ('Content-Range', f'bytes {a}-{b}/{size}'), ('Content-Length', str(b - a + 1))):
            self.send_header(k, v)
        self.end_headers()
        f.seek(a); self.left = b - a + 1
        return f

    def copyfile(self, src, dst):
        if getattr(self, 'left', None) is None:
            return super().copyfile(src, dst)
        while self.left > 0 and (chunk := src.read(min(1 << 16, self.left))):
            dst.write(chunk); self.left -= len(chunk)


def source_frame(t, name):
    f = SRC/f'{name}.jpg'
    ff('-ss', f'{t:.3f}', '-i', video(), '-frames:v', '1', '-q:v', '2', f)
    return Image.open(f).convert('RGBA')


async def main():
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(R)))
    srv.handle_error = lambda *a: None  # Chrome aborts video range requests mid-stream; not an error
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{srv.server_address[1]}/'
    qa = json.loads((Q/'preview-qa.json').read_text(encoding='utf-8')) if only and (Q/'preview-qa.json').exists() else {}
    async with async_playwright() as pw:
        b = await pw.chromium.launch(headless=True, args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        for o in O['overlays']:
            if only and o['id'] not in only:
                continue
            if o.get('prerendered'):
                for kind, t in (('hero', o['hero']), ('entrance', o['entrance'])):
                    shot = FR/f"{o['id']}-{kind}.png"
                    ff('-i', R/'cache'/f"{o['id']}.{o['hash']}.mkv", '-vf', f"select=eq(n\\,{round(t*FPS)})", '-frames:v', '1', '-pix_fmt', 'rgba', shot)
                    bg = source_frame(o['at'] + t, f"{o['id']}-{kind}")
                    Image.alpha_composite(bg, Image.open(shot).convert('RGBA')).convert('RGB').save(FR/f"{o['id']}-{kind}.jpg", quality=90)
                    shot.unlink()
                qa[o['id']] = {'errors': [], 'fails': [], 'fonts': []}
                print(f"{o['id']} {o['type']:<12} {o['at']:7.2f}s", flush=True)
                continue
            page = await b.new_page(viewport={'width': 1920, 'height': 1080})
            await page.add_init_script('window.__timelines = window.__timelines || {}')  # the HyperFrames runtime normally creates it
            errs = []; page.on('pageerror', lambda e: errs.append(str(e)))
            page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            await page.goto(base + o['file'], wait_until='load', timeout=60000)
            await page.evaluate('document.fonts.ready')
            await page.evaluate('''async () => { for (let k = 0; k < 3; k++) {  // a dropped local request leaves a broken image
              const bad = [...document.images].filter(i => i.complete && !i.naturalWidth && i.getAttribute('src')); if (!bad.length) break;
              await Promise.all(bad.map(i => new Promise(r => { i.onload = i.onerror = r; i.src = i.src.split('?')[0] + '?retry=' + k; }))); } }''')
            await page.wait_for_function(f'!!window.__timelines["{o["id"]}"]', timeout=20000)
            row = {'errors': errs, 'fails': [], 'fonts': []}
            for kind, t in (('hero', o['hero']), ('entrance', o['entrance'])):
                await page.evaluate(SEEK, [o['id'], t])
                shot = FR/f"{o['id']}-{kind}.png"
                await page.screenshot(path=str(shot), omit_background=True)
                if kind == 'hero':
                    res = await page.evaluate(CHECK, [o['full'], FACE, SAFE])
                    row['fails'] = res['fails']; row['fonts'] = res['fonts']
                bg = source_frame(o['at'] + t, f"{o['id']}-{kind}")
                Image.alpha_composite(bg, Image.open(shot).convert('RGBA')).convert('RGB').save(FR/f"{o['id']}-{kind}.jpg", quality=90)
                shot.unlink()
            qa[o['id']] = row
            await page.close()
            flag = ' FAIL' if (row['errors'] or row['fails'] or row['fonts']) else ''
            print(f"{o['id']} {o['type']:<12} {o['at']:7.2f}s{flag}", flush=True)
        await b.close()
    srv.shutdown()

    for k, z in enumerate(O['zooms']):
        t = (z['f0'] + z['f1'])/2/FPS
        im = source_frame(t, f'zoom-{k+1:02d}').convert('RGB')
        w, h = 1920/z['scale'], 1080/z['scale']
        x = min(max(0, z['cx']*1920 - w/2), 1920 - w); y = min(max(0, z['cy']*1080 - h/2), 1080 - h)
        im.crop((x, y, x + w, y + h)).resize((1920, 1080), Image.LANCZOS).save(FR/f'zoom-{k+1:02d}-hero.jpg', quality=90)
    (Q/'preview-qa.json').write_text(json.dumps(qa, ensure_ascii=False, indent=1), encoding='utf-8')
    gallery()
    bad = {k: v for k, v in qa.items() if v['errors'] or v['fails'] or v['fonts']}
    print(json.dumps({'overlays': len(qa), 'with_problems': len(bad), 'problems': bad}, ensure_ascii=False, indent=1)[:6000])


def mmss(t):
    return f'{int(t//60)}:{t % 60:04.1f}'


def gallery():
    style = O.get('style') or 'basic'
    refdir = SKILL/'references'/'screenshots'/('ben-ai' if style == 'basic' else 'liam-ottley')
    (Q/'ref').mkdir(exist_ok=True)
    refs = sorted(refdir.glob('*.jpg'))[:10] if refdir.is_dir() else []
    for f in refs:
        shutil.copy(f, Q/'ref'/f.name)
    secs = sorted(plan.get('sections', []), key=lambda s: s['start'])
    groups = [('Intro', 0, secs[0]['start'] if secs else 1e9)] + \
             [(f"Phần {s.get('n', i+1)} · {s['title']}", s['start'], secs[i+1]['start'] if i+1 < len(secs) else 1e9) for i, s in enumerate(secs)]
    cards = {g[0]: [] for g in groups}
    for o in O['overlays']:
        g = next(g for g in groups if g[1] <= o['at'] < g[2] or g is groups[-1])
        loop = f" · giữ {o['total']/FPS:.0f}s" if o['loop'] else ''
        clip = Q/'clips'/f'{o["id"]}-{o["type"]}.mp4'
        media = (f'<video src="clips/{clip.name}" poster="frames/{o["id"]}-hero.jpg" controls preload="none" playsinline></video>' if clip.exists() else
                 f'<a href="frames/{o["id"]}-hero.jpg"><img src="frames/{o["id"]}-hero.jpg" loading="lazy" alt="{o["id"]}"></a>')
        cards[g[0]].append(
            f'<article>{media}'
            f'<div class="meta"><strong>{o["id"]} · {o["type"]}</strong><span>{mmss(o["at"])} · {o["total"]/FPS:.1f}s{loop}</span>'
            f'<p>{html.escape(o["say"])}</p><a href="frames/{o["id"]}-entrance.jpg">Khung lúc đang vào</a></div></article>')
    for k, z in enumerate(O['zooms']):
        g = next(g for g in groups if g[1] <= z['f0']/FPS < g[2] or g is groups[-1])
        cards[g[0]].append(f'<article><a href="frames/zoom-{k+1:02d}-hero.jpg"><img src="frames/zoom-{k+1:02d}-hero.jpg" loading="lazy"></a>'
                           f'<div class="meta"><strong>zoom {k+1} · ×{z["scale"]}</strong><span>{mmss(z["f0"]/FPS)} · {(z["f1"]-z["f0"])/FPS:.1f}s</span></div></article>')
    body = ''.join(f'<h2>{html.escape(name)}</h2><div class="grid">{"".join(cards[name])}</div>' for name, _, _ in groups if cards[name])
    ref = ''.join(f'<img src="ref/{f.name}" title="{f.stem}">' for f in refs)
    n_full = sum(o['full'] for o in O['overlays'])
    doc = f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Duyệt mẫu {html.escape(P.get("name", P["id"]))}</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#FAF6EF;color:#17130D;font-family:system-ui,sans-serif}}main{{max-width:1500px;margin:auto;padding:40px 24px}}
.tag{{color:#4A3AE0;font-size:13px;letter-spacing:.08em;font-weight:700}}h1{{font-size:clamp(26px,4vw,44px);margin:10px 0 8px}}p{{line-height:1.6;color:#4A4339}}
h2{{margin:44px 0 16px;font-size:24px}}.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}}
article{{background:#fff;border:1px solid #17130d17;border-radius:16px;overflow:hidden}}article img,article video{{display:block;width:100%;height:auto}}
.meta{{padding:14px 16px;font-size:14px}}.meta span{{display:block;color:#8A8073;margin-top:4px}}.meta p{{margin:8px 0;font-size:13px}}a{{color:#4A3AE0;text-decoration:none}}
.ref{{display:flex;gap:10px;overflow-x:auto;padding:6px 0}}.ref img{{height:110px;border-radius:10px}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}</style></head><body><main>
<div class="tag">BẢN MẪU CHỜ DUYỆT · CHƯA RENDER VIDEO · STYLE {style.upper()}</div>
<h1>{html.escape(P.get("name", P["id"]))}</h1>
<p>{len(O["overlays"])} overlay ({n_full} toàn khung), {len(O["zooms"])} zoom, {len(O["sfx"])} SFX. Mỗi ảnh là overlay đặt lên đúng khung hình gốc tại giây đó. Bấm ảnh để xem 1920×1080.
Góp ý theo mã (ví dụ "ov-004 đổi chữ", "bỏ ov-010"), hoặc nói "duyệt" để render.</p>
<h2>Tham chiếu {"Ben AI" if style == "basic" else "Liam Ottley"}</h2><div class="ref">{ref}</div>{body}</main></body></html>'''
    (Q/'index.html').write_text(doc, encoding='utf-8')
    files = [FR/f"{o['id']}-hero.jpg" for o in O['overlays']] + sorted(FR.glob('zoom-*-hero.jpg'))
    files = [f for f in files if f.exists()]
    font = ImageFont.truetype('arial.ttf', 18)
    for old in Q.glob('contact-*.jpg'):
        old.unlink()
    for k in range(0, len(files), 12):
        chunk = files[k:k+12]; rows = (len(chunk)+3)//4
        sheet = Image.new('RGB', (4*480, rows*296), '#17130D'); d = ImageDraw.Draw(sheet)
        for j, f in enumerate(chunk):
            sheet.paste(Image.open(f).resize((480, 270)), (j % 4*480, j//4*296))
            d.text((j % 4*480+8, j//4*296+272), f.stem.replace('-hero', ''), font=font, fill='white')
        sheet.save(Q/f'contact-{k//12+1}.jpg', quality=88)
    (Q/'status.json').write_text(json.dumps({'status': 'awaiting_approval', 'video_rendered': False}), encoding='utf-8')


if '--gallery' in sys.argv:  # rebuild review/index.html only (clips.py calls this after exporting clips)
    gallery()
else:
    asyncio.run(main())
