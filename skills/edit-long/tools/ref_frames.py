# Reference study: frames + contact sheets from downloaded YouTube videos (yt-dlp, 720p video-only).
# Per video, one decode pass: 1 fps for the first 45 s (intro), scene-change frames, 1 frame / 20 s.
# Usage: python -I ref_frames.py <out_dir> <video> [<video> ...]   -> <out_dir>/<stem>/ + stats.json
import json, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(sys.argv[1]); FONT = ImageFont.truetype('arial.ttf', 18)


def sheet(files, labels, path, cols, tw=320, th=180):
    rows = (len(files)+cols-1)//cols
    im = Image.new('RGB', (cols*tw, rows*(th+24)), '#111'); d = ImageDraw.Draw(im)
    for i, (f, lab) in enumerate(zip(files, labels)):
        x, y = i % cols*tw, i//cols*(th+24)
        im.paste(Image.open(f).convert('RGB').resize((tw, th)), (x, y)); d.text((x+6, y+th+2), lab, font=FONT, fill='white')
    im.save(path, quality=88)


def mmss(t):
    return f'{int(t//60)}:{t % 60:04.1f}'


stats = {}
for v in map(Path, sys.argv[2:]):
    o = OUT/v.stem
    for sub in ('intro', 'scene', 'every20'):
        (o/sub).mkdir(parents=True, exist_ok=True)
    dur = float(json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', str(v)]))['format']['duration'])
    fc = ("[0:v]scale=640:360,split=3[a][b][c];"
          "[a]select='gt(scene,0.30)',showinfo[sa];"
          r"[b]select='isnan(prev_selected_t)+gte(t-prev_selected_t\,20)'[sb];"
          "[c]trim=0:45,fps=1[sc]")
    log = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-y', '-i', str(v), '-filter_complex', fc,
                          '-map', '[sa]', '-fps_mode', 'vfr', '-q:v', '3', str(o/'scene/%04d.jpg'),
                          '-map', '[sb]', '-fps_mode', 'vfr', '-q:v', '3', str(o/'every20/%04d.jpg'),
                          '-map', '[sc]', '-q:v', '3', str(o/'intro/%04d.jpg')],
                         capture_output=True, text=True, errors='replace').stderr
    times = [float(t) for t in re.findall(r'pts_time:([\d.]+)', log)]
    scene = sorted((o/'scene').glob('*.jpg')); every = sorted((o/'every20').glob('*.jpg')); intro = sorted((o/'intro').glob('*.jpg'))
    sheet(intro, [f'{i}s' for i in range(len(intro))], o/'sheet-intro.jpg', 9)
    for k in range(0, len(every), 30):
        sheet(every[k:k+30], [mmss(20*(k+i)) for i in range(len(every[k:k+30]))], o/f'sheet-every20-{k//30+1}.jpg', 6)
    for k in range(0, len(scene), 48):
        sheet(scene[k:k+48], [mmss(t) for t in times[k:k+48]], o/f'sheet-scene-{k//48+1}.jpg', 8)
    early = [t for t in times if t < 60]
    stats[v.stem] = {'duration_s': round(dur, 1), 'scene_cuts': len(times), 'cuts_per_min': round(len(times)/dur*60, 2),
                     'cuts_first_60s': len(early), 'scene_times': [round(t, 2) for t in times]}
    print(v.stem, stats[v.stem]['cuts_per_min'], 'cuts/min', len(times), 'cuts', flush=True)
prev = json.loads((OUT/'stats.json').read_text()) if (OUT/'stats.json').exists() else {}
(OUT/'stats.json').write_text(json.dumps({**prev, **stats}, indent=1), encoding='utf-8')
