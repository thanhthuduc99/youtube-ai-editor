# QA of renders/final.mp4 without loading the video into memory: stream info, full decode, faststart, new black frames,
# loudness, audio alignment vs the source speech, and every overlay's hero frame compared with the approved preview.
# Writes renders/qa-report.json and renders/frames/FINAL-heroes-*.jpg.
import json, struct, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from common import R, P, FPS, video, load_json

F = R/'renders'/'final.mp4'
Q = R/'renders'/'frames'; Q.mkdir(parents=True, exist_ok=True)
O = load_json('overlays.json')


def run(args):
    return subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')


probe = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(F)]).stdout)
v = next(s for s in probe['streams'] if s['codec_type'] == 'video')
a = next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)

atoms = []
with open(F, 'rb') as fh:
    pos, size = 0, F.stat().st_size
    while pos < size and len(atoms) < 8:
        fh.seek(pos); n, typ = struct.unpack('>I4s', fh.read(8))
        if n == 1:
            n = struct.unpack('>Q', fh.read(8))[0]
        atoms.append(typ.decode('latin1')); pos += n or size - pos
faststart = 'moov' in atoms and 'mdat' in atoms and atoms.index('moov') < atoms.index('mdat')

scan = run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(F), '-vf', 'blackdetect=d=0.1:pix_th=0.08',
            '-af', 'ebur128=peak=true', '-f', 'null', '-'])
black = [l.split('black_start:')[1].split()[0] for l in scan.stderr.splitlines() if 'black_start:' in l]
summ = scan.stderr[scan.stderr.rfind('Summary:'):]
lufs = next((float(l.split()[1]) for l in summ.splitlines() if l.strip().startswith('I:')), None)
peak = next((float(l.split()[1]) for l in summ.splitlines() if l.strip().startswith('Peak:')), None)
decode_err = [l for l in scan.stderr.splitlines() if 'error' in l.lower() and 'concealing' in l.lower()][:20]

run(['ffmpeg', '-v', 'error', '-y', '-i', str(F), '-vn', '-ac', '1', '-ar', '16000', str(R/'renders'/'final-audio.wav')])
with wave.open(str(R/'assets'/'speech.wav')) as w:
    x = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float32)
with wave.open(str(R/'renders'/'final-audio.wav')) as w:
    y = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float32)
lags = []
for s in sorted({int(P['duration']*f) for f in (.05, .3, .55, .8)} | {max(0, int(P['duration']) - 8)}):
    p_, q_ = x[s*16000:(s+5)*16000], y[s*16000:(s+5)*16000]
    if len(p_) < 16000 or len(q_) < 16000:
        continue
    c = np.fft.irfft(np.fft.rfft(q_, 2**18)*np.fft.rfft(p_[::-1], 2**18))
    lags.append({'at_s': s, 'lag_ms': round(float((np.argmax(c) - len(p_) + 1)/16), 1)})
del x, y

font = ImageFont.truetype('arial.ttf', 18)
diffs, shots = [], []
for o in O['overlays']:
    t = o['at'] + o['hero']; out = Q/f"{o['id']}.jpg"
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', str(F), '-frames:v', '1', '-q:v', '2', str(out)])
    ref = R/'review'/'frames'/f"{o['id']}-hero.jpg"
    if out.exists() and ref.exists():
        d = np.abs(np.asarray(Image.open(out).convert('RGB'), np.float32) - np.asarray(Image.open(ref).convert('RGB'), np.float32)).mean()
        # video inside the layer or motion that never stops: preview and render land a fraction of a frame apart
        moving = o['type'] in ('broll', 'broll-full') or (o['type'].startswith('th-') and o['full'])
        limit = 20 if o['type'] == 'transition' else 12 if moving else 4  # a film burn flashes frame to frame
        diffs.append({'id': o['id'], 'type': o['type'], 'mean_diff': round(float(d), 2), 'flag': bool(d > limit)})
        shots.append(out)
for k in range(0, len(shots), 12):
    chunk = shots[k:k+12]; rows = (len(chunk)+3)//4
    sheet = Image.new('RGB', (4*480, rows*296), '#17130D'); dr = ImageDraw.Draw(sheet)
    for j, f in enumerate(chunk):
        sheet.paste(Image.open(f).resize((480, 270)), (j % 4*480, j//4*296)); dr.text((j % 4*480+8, j//4*296+272), f.stem, font=font, fill='white')
    sheet.save(Q/f'FINAL-heroes-{k//12+1}.jpg', quality=88)

src_frames = int(round(P['duration']*FPS))
report = {
    'file': str(F), 'size_mb': round(F.stat().st_size/1e6, 1),
    'video': {k: v.get(k) for k in ('codec_name', 'width', 'height', 'pix_fmt', 'r_frame_rate', 'nb_frames', 'color_space')},
    'audio': {k: a.get(k) for k in ('codec_name', 'sample_rate', 'channels')} if a else None,
    'duration_s': float(probe['format']['duration']), 'frames_expected': src_frames,
    'frames_ok': abs(int(v.get('nb_frames') or 0) - src_frames) <= 1, 'faststart': faststart,
    'black_starts_s': black, 'loudness_lufs': lufs, 'true_peak_dbfs': peak, 'decode_errors': decode_err,
    'audio_lag_vs_source_ms': lags, 'hero_diffs': diffs, 'flagged': [d['id'] for d in diffs if d['flag']],
}
(R/'renders'/'qa-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps({k: report[k] for k in ('size_mb', 'duration_s', 'frames_ok', 'faststart', 'black_starts_s', 'loudness_lufs',
                                         'true_peak_dbfs', 'audio_lag_vs_source_ms', 'flagged')}, ensure_ascii=False, indent=1))
sys.exit(1 if report['flagged'] or not report['frames_ok'] or any(abs(l['lag_ms']) > 40 for l in lags) else 0)
