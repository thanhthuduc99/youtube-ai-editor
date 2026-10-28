# edit-plan.json -> one standalone HyperFrames composition per overlay (compositions/ov-*.html), the sped-up B-roll
# clips they play (assets/broll/), source frames they show (assets/img/), overlays.json (frame timing, hold loops,
# content hashes, absolute SFX cues) and chapters.txt for the YouTube description.
# Long corner overlays (section chips) render only entrance + exit; composite.py loops the settled frame in between.
import hashlib, json, re, shutil, subprocess, sys, urllib.request
from pathlib import Path
from common import R, P, FPS, W, H, CACHE, frame, ff, video, load_json, save_json, sfx_dir
import components as C

plan = load_json('edit-plan.json')
NF = frame(P['duration'])
LIB = sfx_dir()
errors, warnings = [], []
A = R/'assets'
SFX_OK = ({f.stem for f in LIB.glob('*.mp3')} if LIB else set()) | {f.stem for f in (A/'sfx').glob('*') if f.suffix.lower() in ('.mp3', '.wav')}
# overlays that keep the face on screen: no "switch" sound when they start
FACE_STAYS = {'th-text', 'th-chips', 'th-lower', 'th-side', 'th-column'}
for d in ('broll', 'img', 'models', 'logos'):
    (A/d).mkdir(parents=True, exist_ok=True)
(R/'compositions').mkdir(exist_ok=True)
ICONS = 'https://cdn.jsdelivr.net/npm/simple-icons@16.20.0/icons/{}.svg'


def logo(slug):
    """simple-icons slug (cached in assets/logos) or a local .svg/.png path; None -> letter tile."""
    if Path(slug).suffix.lower() in ('.svg', '.png', '.jpg') and Path(slug).exists():
        dst = A/'logos'/Path(slug).name
        if not dst.exists():
            shutil.copy(slug, dst)
        return f'<img src="../assets/logos/{dst.name}" style="width:52px;height:52px;object-fit:contain">'
    f = A/'logos'/f'{slug}.svg'
    if not f.exists():
        try:
            f.write_bytes(urllib.request.urlopen(ICONS.format(slug), timeout=20).read())
        except Exception:
            f.write_text('')
            warnings.append(f'logo "{slug}" not in simple-icons -> letter tile')
    s = f.read_text(encoding='utf-8').strip()
    return re.sub(r'<title>.*?</title>', '', s) or None


def _tag(*parts):
    return hashlib.sha1('|'.join(map(str, parts)).encode()).hexdigest()[:8]


def _safe(name):
    return re.sub(r'[^\w.-]+', '-', name)


def img(spec, w=None):
    """Real pictures for overlays. 'src:<s>' = frame of the source video (clip_crop applied); '<video file>@<s>' = frame
    of any other video (raw footage, a finished render); 'shot:<html file or url>' = page screenshot; else an image file.
    w = downscale to this width (thumbnails)."""
    spec = str(spec)
    if spec.startswith('shot:'):
        return shot(spec[5:])['src']
    m = re.match(r'(.+\.(?:mp4|mov|mkv|webm|m4v))@([\d.]+)$', spec, re.I)
    if spec.startswith('src:') or m:
        f, t = (video(), float(spec[4:])) if spec.startswith('src:') else (m[1], float(m[2]))
        crop = plan.get('layout', {}).get('clip_crop') if spec.startswith('src:') else None
        dst = A/'img'/f"{'src' if spec.startswith('src:') else _safe(Path(f).stem)[:24]}-{t:08.2f}-{_tag(f, crop, w)}.jpg"
        if not dst.exists():
            vf = ([f'crop={crop[2]}:{crop[3]}:{crop[0]}:{crop[1]}'] if crop else []) + ([f'scale={w}:-2:flags=lanczos'] if w else [])
            ff('-ss', f'{t:.3f}', '-i', f, '-frames:v', '1', '-q:v', '2', *(['-vf', ','.join(vf)] if vf else []), dst)
    else:
        src = Path(spec)
        dst = A/'img'/f'{_tag(src.resolve(), w)}-{_safe(src.name)}'
        if not dst.exists():
            if w:
                from PIL import Image
                im = Image.open(src); im.thumbnail((w, 10**5), Image.LANCZOS)
                im.save(dst, quality=90) if dst.suffix.lower() in ('.jpg', '.jpeg') else im.save(dst)
            else:
                shutil.copy(src, dst)
    return f'../assets/img/{dst.name}'


def shot(target, w=1440, h=900, sel=None, max_h=2600):
    """Screenshot of a local .html file or a URL (Playwright, page width w) -> {'src', 'w', 'h', 'boxes'}.
    boxes = [x, y, w, h] of every element matching sel, in screenshot pixels (e.g. thumbnails to tick)."""
    dst = A/'img'/f'shot-{_tag(target, w, h, sel, max_h)}.png'; meta = dst.with_suffix('.json')
    if not dst.exists() or not meta.exists():
        from playwright.sync_api import sync_playwright
        url = target if re.match(r'https?://', target) else Path(target).resolve().as_uri()
        with sync_playwright() as pw:
            b = pw.chromium.launch(); pg = b.new_page(viewport={'width': w, 'height': h})
            pg.goto(url, wait_until='networkidle', timeout=90000)
            pg.evaluate("""async () => { document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager');
              await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })));
              await document.fonts.ready; }""")
            full = pg.evaluate('[document.documentElement.scrollWidth, document.documentElement.scrollHeight]')
            H = min(full[1], max_h)
            boxes = pg.evaluate("""s => [...document.querySelectorAll(s)].map(e => { const r = e.getBoundingClientRect();
              return [r.x + scrollX, r.y + scrollY, r.width, r.height].map(Math.round); })""", sel) if sel else []
            pg.screenshot(path=str(dst), full_page=True, clip={'x': 0, 'y': 0, 'width': w, 'height': H})
            b.close()
        meta.write_text(json.dumps({'w': w, 'h': H, 'boxes': [b for b in boxes if b[1] + b[3] <= H]}))
    return {'src': f'../assets/img/{dst.name}', **json.loads(meta.read_text())}


def wave(f, a, b, n):
    """n peak levels (0..1) of the sound of media file f between a and b seconds, for drawing a real waveform."""
    import numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{a:.3f}', '-t', f'{b-a:.3f}', '-i', str(f), '-ac', '1', '-ar', '8000',
                          '-f', 's16le', '-'], capture_output=True, check=True).stdout
    x = np.abs(np.frombuffer(raw, np.int16).astype(np.float32))
    pk = np.array([c.max() if len(c) else 0 for c in np.array_split(x, n)])
    ref = np.percentile(pk, 98) or 1
    return [round(float(min(1, v/ref)), 3) for v in pk]


def vclip(f, a, n, speed=1.0, w=1920, vf=''):
    """n frames of any video file from a seconds (sped up by speed), muted, for <video> inside slides.
    vf = extra ffmpeg filters after scaling (e.g. 'boxblur=12:2' for a blurred background copy)."""
    dst = A/'broll'/f'v-{_safe(Path(f).stem)[:20]}-{_tag(f, a, n, speed, w, vf)}.mp4'
    if not dst.exists():
        ff('-ss', f'{a:.3f}', '-t', f'{n/FPS*speed+1:.3f}', '-i', f, '-an', '-vf',
           f'scale={w}:-2:flags=lanczos,{vf + "," if vf else ""}setpts=(PTS-STARTPTS)/{speed},fps={FPS}',
           '-frames:v', n, '-c:v', 'h264_nvenc', '-preset', 'p5', '-rc', 'vbr', '-cq', '18', '-b:v', '0', '-g', FPS,
           '-pix_fmt', 'yuv420p', '-movflags', '+faststart', dst)
    return f'../assets/broll/{dst.name}'


def model(path):
    dst = A/'models'/Path(path).name
    if not dst.exists():
        shutil.copy(path, dst)
    return f'../assets/models/{dst.name}'


def clip(o, n):
    c = o['clip']; sp = float(c.get('speed', 1))
    crop = c.get('crop', plan.get('layout', {}).get('clip_crop'))  # [x, y, w, h] in source pixels, e.g. drop browser bar + taskbar
    vf = (f'crop={crop[2]}:{crop[3]}:{crop[0]}:{crop[1]},scale=1920:1080,' if crop else '') + f'setpts=(PTS-STARTPTS)/{sp},fps={FPS}'
    dst = A/'broll'/f"{o['id']}-{c['src']:.2f}-x{sp:g}-{n}{'-c' if crop else ''}.mp4"
    if not dst.exists():
        for old in (A/'broll').glob(f"{o['id']}-*.mp4"):
            old.unlink()
        ff('-ss', f"{c['src']:.3f}", '-t', f'{n/FPS*sp+1:.3f}', '-i', video(), '-an',
           '-vf', vf, '-frames:v', n, '-c:v', 'h264_nvenc', '-preset', 'p5',
           '-rc', 'vbr', '-cq', '18', '-b:v', '0', '-g', FPS, '-pix_fmt', 'yuv420p', '-movflags', '+faststart', dst)
    return f'../assets/broll/{dst.name}'


def dur(n):
    """Composition length for exactly n frames. Never rounds up: HyperFrames renders ceil(D*fps) frames."""
    d = round(n/FPS, 4)
    return round(d - .0001, 4) if d*FPS > n else d


def fingerprint(html):
    h = hashlib.sha1(html.encode('utf-8'))
    for ref in sorted(set(re.findall(r'\.\./(assets/[^"\')\s]+)', html))):
        f = R/ref
        if f.is_file():
            st = f.stat(); h.update(f'{ref}:{st.st_size}:{st.st_mtime_ns}'.encode())
    return h.hexdigest()[:10]


records, cues = [], []
for i, o in enumerate(plan['overlays']):
    o.setdefault('id', f'ov-{i+1:03d}'); o.setdefault('props', {})
    if o['type'] not in C.BUILDERS:
        errors.append(f"{o['id']}: unknown type {o['type']}"); continue
    F = frame(o['at']); n = max(1, frame(o['dur']))
    if F + n > NF:
        warnings.append(f"{o['id']}: trimmed to video end"); n = NF - F

    def make(nr):
        ctx = dict(D=dur(nr), logo=logo, img=img, model=model, clip=lambda ov: clip(ov, nr), shot=shot, wave=wave,
                   vclip=lambda f, a, speed=1.0, w=1920, n=None, vf='': vclip(f, a, n or nr, speed, w, vf), video=video(), F=F)
        return C.BUILDERS[o['type']](o, ctx)

    c = make(n)
    nr, loop = n, None
    if c.get('holdable') and o.get('hold', True) and n/FPS > c['enter'] + c['exit'] + 1.5:
        nr = frame(c['enter'] + .25 + c['exit'])
        c = make(nr)
        loop = {'start': frame(c['enter'] + .1), 'count': n - nr}
    D = dur(nr)
    html = C.page(o, c, D)
    (R/'compositions'/f"{o['id']}.html").write_text(html, encoding='utf-8')
    hero = min(c['hero'], D - c['exit'] - .05) if loop is None else min(c['hero'], c['enter'] + .1)
    sfx = [(s['at'], s['name'], s.get('gain', -16)) for s in o['sfx']] if 'sfx' in o else c.get('sfx', [])
    sw = plan.get('switch_sfx')  # sound when the picture switches away from the face to a B-roll source
    if sw and c.get('full') and o['type'] not in FACE_STAYS and 'sfx' not in o:
        sfx = [(0, sw['name'], sw.get('gain', 0))] + [x for x in sfx if x[0] > .15]
    for rel, name, gain in sfx:
        if name not in SFX_OK:
            errors.append(f"{o['id']}: SFX '{name}' not in {LIB}")
        cues.append({'t': round(F/FPS + rel, 3), 'name': name, 'gain': gain, 'from': o['id']})
    records.append({'id': o['id'], 'type': o['type'], 'file': f"compositions/{o['id']}.html", 'at': round(F/FPS, 3),
                    'frame': F, 'frames': nr, 'total': n, 'loop': loop, 'hash': fingerprint(html),
                    'hero': round(hero, 3), 'entrance': round(c['enter']*.45, 3), 'full': bool(c.get('full')),
                    'pos': o['props'].get('pos', 'center' if c.get('full') else None), 'say': o.get('say', '')})

# transitions over jump cuts (face -> face): pre-rendered alpha layers, peak frame on the cut, with their own sound
def burn_alpha(src, dst):
    """Light leak / film burn shot on black -> RGBA (alpha = brightest channel), so a plain overlay ~ screen blend."""
    import numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(src), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-'],
                         capture_output=True, check=True).stdout
    f = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.float32)
    a = f.max(axis=3, keepdims=True)
    rgba = np.concatenate([np.where(a > 0, f/np.maximum(a, 1)*255, 0), a], axis=3).clip(0, 255).astype(np.uint8)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                    '-c:v', 'ffv1', '-level', '3', '-pix_fmt', 'bgra', '-g', '1', str(dst)], input=rgba.tobytes(), check=True)
    return len(f)


CACHE.mkdir(exist_ok=True)
TR = A/'transitions'
for k, t in enumerate(plan.get('transitions', [])):
    src = TR/f"{t.get('kind', 'filmburn-01')}.mp4"
    if not src.exists():
        errors.append(f"transition {k+1}: {src} missing"); continue
    meta = json.loads(src.with_suffix('.json').read_text(encoding='utf-8'))
    tid = f'tr-{k+1:02d}'
    F = max(0, frame(t['at'] - meta['peak']))
    h = hashlib.sha1(f"{src.name}:{src.stat().st_size}:{src.stat().st_mtime_ns}".encode()).hexdigest()[:10]
    out = CACHE/f'{tid}.{h}.mkv'
    if not out.exists():
        for old in CACHE.glob(f'{tid}.*.mkv'):
            old.unlink()
        burn_alpha(src, out)
    n = int(subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames',
                            '-of', 'csv=p=0', str(out)], capture_output=True, text=True).stdout.strip())
    n = min(n, NF - F)
    records.append({'id': tid, 'type': 'transition', 'file': None, 'prerendered': True, 'at': round(F/FPS, 3), 'frame': F,
                    'frames': n, 'total': n, 'loop': None, 'hash': h, 'hero': meta['peak'], 'entrance': round(meta['peak']*.6, 3),
                    'full': False, 'pos': 'transition', 'say': t.get('say', f"cut at {t['at']:.2f}s")})
    cues.append({'t': round(F/FPS, 3), 'name': meta['sfx'], 'gain': t.get('gain', -6), 'from': tid})

# conflicts: two full-frame overlays at once, or two corner overlays in the same slot at once
for a in records:
    for b in records:
        if a['id'] < b['id'] and a['frame'] < b['frame'] + b['total'] and b['frame'] < a['frame'] + a['total']:
            if a['full'] and b['full']:
                errors.append(f"{a['id']} and {b['id']}: two full-frame overlays overlap")
            elif not a['full'] and not b['full'] and a['pos'] == b['pos']:
                errors.append(f"{a['id']} and {b['id']}: both at {a['pos']} at the same time")

if plan.get('style') == 'advanced':
    ev = sorted((r['frame'], r['frame'] + r['total']) for r in records if r['type'] != 'section-chip')
    ev += [(frame(z['at']), frame(z['at'] + z['dur'])) for z in plan.get('zooms', [])]
    ev.sort(); end = ev[0][1] if ev else 0
    for s, e in ev[1:]:
        if (s - end)/FPS > 15:
            warnings.append(f'advanced: {(s-end)/FPS:.1f}s with no visual from {end/FPS:.1f}s')
        end = max(end, e)

cues.sort(key=lambda c: c['t'])
kept = []
for c in cues:
    if c['t'] < 0 or c['t'] >= P['duration']:
        continue
    if kept and c['t'] - kept[-1]['t'] < .25:
        warnings.append(f"SFX {c['name']} at {c['t']}s dropped (<0.25s after {kept[-1]['name']})"); continue
    kept.append(c)

zooms = [{'f0': frame(z['at']), 'f1': frame(z['at'] + z['dur']), 'scale': z.get('scale', 1.12),
          'cx': z.get('cx', .5), 'cy': z.get('cy', .5)} for z in plan.get('zooms', [])]

live = {f"{r['id']}.html" for r in records}
for f in (R/'compositions').glob('ov-*.html'):
    if f.name not in live:
        f.unlink()

if errors:
    print('ERRORS:\n  ' + '\n  '.join(errors)); sys.exit(1)
save_json('overlays.json', {'fps': FPS, 'duration': P['duration'], 'frames': NF, 'style': plan.get('style'),
                            'overlays': records, 'zooms': zooms, 'sfx': kept})

mmss = lambda t: f'{int(t//60)}:{int(t % 60):02d}'
chap = ['0:00 Intro'] + [f"{mmss(s['start'])} {s.get('chapter') or s['title']}" for s in plan.get('sections', [])]
(R/'chapters.txt').write_text('\n'.join(chap) + '\n', encoding='utf-8')
for w in warnings:
    print('warning:', w)
held = sum(1 for r in records if r['loop'])
print(f"{len(records)} overlays ({held} held), {len(zooms)} zooms, {len(kept)} SFX cues, "
      f"{sum(r['frames'] for r in records)} frames to render -> overlays.json, chapters.txt")
