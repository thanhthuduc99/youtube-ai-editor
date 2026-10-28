# Cut pass: renders cut/renders/cut.mp4 from work/utterances.json + work/cuts.json (Claude's decision). Drops and trims
# utterances, shortens long pauses to the creator's own rhythm, cuts at the quietest 10 ms frame, speeds up like his
# manual edit (raw x1.1). Also writes:
#   work/keep.json      kept raw ranges + where each starts in the output (the previous one is kept as keep.prev.json)
#   work/jumps.json     visible jump cuts (stumble removed, or 2 s+ of silence), for jump_fx.py
#   cut-report.md       every cut with its text and reason, for the approval stop
#   ../assets/transcript.json + .txt   the edit stage's transcript on the cut timeline, so edit-long skips whisper
# Usage: python cut/scripts/render_cut.py [--speed 1.1]
import argparse, json, re, shutil, subprocess
from pathlib import Path
import numpy as np

R = Path(__file__).resolve().parents[1]
WK, P = R/'work', R.parent
ap = argparse.ArgumentParser()
ap.add_argument('--speed', type=float, default=1.1)
SPEED = ap.parse_args().speed
# Editor's rhythm (measured on the REA video, 16/10/2026, 300+ pauses): gaps under 0.4 s kept as they are, 0.4 s and
# longer come out at ~0.25 s, even scene changes (3 s+) only keep ~0.4 s.
KEEP_GAP, PAD, LONG, PAD_LONG, FPS, FADE = 0.4, 0.13, 3.0, 0.2, 30, 0.008

U = json.loads((WK/'utterances.json').read_text(encoding='utf-8'))
cuts = json.loads((WK/'cuts.json').read_text(encoding='utf-8'))
rms = np.load(WK/'rms.npy')
utts = {u['id']: u for u in U['utterances']}
order = [u['id'] for u in U['utterances']]


def quietest(a, b):
    i0 = min(max(0, int(a*100)), len(rms)-1)
    i1 = max(i0+1, int(b*100))
    return (i0+int(np.argmin(rms[i0:i1])))/100 + 0.005


def norm(s):
    return re.sub(r'[^\w\s]', '', s.lower()).split()


dropped = {i for d in cuts.get('drop', []) for i in d['ids']}
unknown = dropped - set(order)
assert not unknown, f'unknown ids in cuts.json: {unknown}'
for k, i in enumerate(order):
    if utts[i].get('marker'):
        dropped.add(i)
        if k and order[k-1] not in dropped:
            print(f'WARNING: {order[k-1]} right before cut command {i} is kept, check the bad take was dropped')

# pieces: (start, end, hard_start, hard_end); hard = boundary is already a cut point inside speech (trim)
pieces = {i: [(utts[i]['start'], utts[i]['end'], False, False)] for i in order if i not in dropped}
trim_spans = []
for t in cuts.get('trim', []):
    u = utts[t['id']]; ws = u['words']; want = norm(t['text'])
    flat = [(k, x) for k, w in enumerate(ws) for x in norm(w['w'])]
    n = len(want)
    hit = next((j for j in range(len(flat)-n+1) if [x for _, x in flat[j:j+n]] == want), None)
    assert hit is not None, f"trim text not found in {t['id']}: {t['text']!r}"
    k0, k1 = flat[hit][0], flat[hit+n-1][0]
    s = u['start'] if k0 == 0 else quietest(ws[k0]['s']-0.08, ws[k0]['s']+0.08)
    e = u['end'] if k1 == len(ws)-1 else quietest(ws[k1+1]['s']-0.08, ws[k1+1]['s']+0.08)
    trim_spans.append((s, e))
    new = []
    for a, b, ha, hb in pieces[t['id']]:
        if e <= a or s >= b:
            new.append((a, b, ha, hb)); continue
        if s > a: new.append((a, s, ha, True))
        if e < b: new.append((e, b, True, hb))
    pieces[t['id']] = new

seq, gap_dropped = [], False  # (start, end, hard_start, hard_end, dropped_before)
for i in order:
    if i in dropped:
        gap_dropped = True; continue
    for a, b, ha, hb in pieces[i]:
        seq.append([a, b, ha, hb, gap_dropped]); gap_dropped = False

starts = sorted(u['start'] for u in U['utterances'])
ends = sorted(u['end'] for u in U['utterances'])


def end_cut(e):
    nxt = next((s for s in starts if s >= e-1e-3), U['to'])
    pad = PAD_LONG if nxt - e >= LONG else PAD
    hi = min(e+pad, (e+nxt)/2)
    return quietest(min(e+max(0.04, pad-0.08), hi), hi)


def start_cut(a):
    prv = max([x for x in ends if x <= a+1e-3], default=0.0)
    pad = PAD_LONG if a - prv >= LONG else PAD
    lo = max(a-pad, (prv+a)/2)
    return 0.0 if a < 0.05 else quietest(lo, max(lo, a-max(0.04, pad-0.08)))


segs = []  # [start, end, end_is_hard]
for a, b, ha, hb, dropped_before in seq:
    if segs and not dropped_before and not ha and not segs[-1][2] and a-segs[-1][1] <= KEEP_GAP:
        segs[-1][1] = b; segs[-1][2] = hb; continue
    segs.append([a if ha else start_cut(a), b, hb])
for s in segs:
    if not s[2]:
        s[1] = end_cut(s[1])

keep = []
for a, b, _ in segs:
    a, b = round(a*FPS)/FPS, round(b*FPS)/FPS
    if keep: a = max(a, keep[-1][1])
    if b-a >= 2/FPS:
        keep.append((a, b))

out_t, rows = 0.0, []
for a, b in keep:
    rows.append({'raw_start': round(a, 4), 'raw_end': round(b, 4), 'out_start': round(out_t/SPEED, 3)})
    out_t += b-a
if (WK/'keep.json').exists():
    shutil.copy(WK/'keep.json', WK/'keep.prev.json')
(WK/'keep.json').write_text(json.dumps({'source': U['source'], 'speed': SPEED, 'segments': rows}, indent=1), encoding='utf-8')


# jump cuts the viewer will see: where a stumble was removed, or where 2 s+ of silence went (the face jumps)
drop_spans = [(utts[i]['start'], utts[i]['end']) for i in dropped]
jumps = []
for pr, nx in zip(rows, rows[1:]):
    gap = nx['raw_start'] - pr['raw_end']
    stumble = any(pr['raw_end'] - 1e-3 <= (a+b)/2 <= nx['raw_start'] + 1e-3 for a, b in drop_spans + trim_spans)
    if stumble or gap >= 2.0:
        jumps.append({'at': nx['out_start'], 'removed': round(gap, 2), 'stumble': stumble})
(WK/'jumps.json').write_text(json.dumps(jumps, indent=1), encoding='utf-8')


def to_out(t):
    """Raw time -> time in cut.mp4, or None when that moment was cut."""
    for r in rows:
        if r['raw_start'] <= t < r['raw_end']:
            return r['out_start'] + (t - r['raw_start'])/SPEED
    return None


def land(t):
    """Where a cut made at raw time t shows up in cut.mp4 (start of the next kept range)."""
    nxt = next((r for r in rows if r['raw_start'] >= t - 1e-3), None)
    return nxt['out_start'] if nxt else round(out_t/SPEED, 3)


# ---- edit stage transcript (edit-long format), remapped to the cut timeline
fixes = {}
if (P/'project.json').exists():
    fixes = json.loads((P/'project.json').read_text(encoding='utf-8')).get('fixes', {})

def _fix(s):
    for k, v in fixes.items():
        s = s.replace(k, v)
    return s


segments = []
for i in order:
    if i in dropped:
        continue
    ws, u0, u1 = [], utts[i]['start'], utts[i]['end'] - 1e-3
    clamp = lambda t: min(max(t, u0), u1)  # whisper word times spill past the utterance edges found in the audio
    for w in utts[i]['words']:
        mid = clamp((w['s'] + w['e'])/2)
        if any(a <= mid < b for a, b in trim_spans) or to_out(mid) is None:
            continue
        s, e = to_out(clamp(w['s'])) or to_out(mid), to_out(clamp(w['e'])) or to_out(mid)
        ws.append({'word': ' ' + _fix(w['w']), 'start': round(s, 3), 'end': round(max(s, e), 3)})
    if not ws:
        continue
    if segments and ws[0]['start'] - segments[-1]['end'] < 0.45 and ws[-1]['end'] - segments[-1]['start'] < 12:
        segments[-1]['words'] += ws; segments[-1]['end'] = ws[-1]['end']
    else:
        segments.append({'start': ws[0]['start'], 'end': ws[-1]['end'], 'words': ws})
for sg in segments:
    sg['text'] = ''.join(w['word'] for w in sg['words']).strip()
A = P/'assets'; A.mkdir(exist_ok=True)
(A/'transcript.json').write_text(json.dumps([{k: s[k] for k in ('start', 'end', 'text', 'words')} for s in segments],
                                            ensure_ascii=False, indent=1), encoding='utf-8')
(A/'transcript.txt').write_text('\n'.join(f"[{int(s['start']//60)}:{s['start'] % 60:05.2f}] {s['text']}" for s in segments), encoding='utf-8')

# ---- render
g = []
for k, (a, b) in enumerate(keep):
    d = b-a
    g.append(f'[0:v]trim=start={a:.4f}:end={b:.4f},setpts=PTS-STARTPTS[v{k}];'
             f'[0:a]atrim=start={a:.4f}:end={b:.4f},asetpts=PTS-STARTPTS,'
             f'afade=t=in:d={FADE},afade=t=out:st={d-FADE:.4f}:d={FADE}[a{k}];')
g.append(''.join(f'[v{k}][a{k}]' for k in range(len(keep))) + f'concat=n={len(keep)}:v=1:a=1[vc][ac];')
g.append(f'[vc]setpts=PTS/{SPEED},fps={FPS}[v];[ac]atempo={SPEED}[a]')
(WK/'cut.filter').write_text('\n'.join(g), encoding='utf-8')
(R/'renders').mkdir(exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', U['source'], '-filter_complex_script', str(WK/'cut.filter'),
                '-map', '[v]', '-map', '[a]', '-c:v', 'h264_nvenc', '-preset', 'p5', '-rc', 'vbr', '-cq', '19', '-b:v', '0',
                '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(R/'renders'/'cut.mp4')],
               check=True)

# ---- report
raw_kept = sum(b-a for a, b in keep)
mm = lambda t: f'{int(t//60)}:{t % 60:04.1f}'
lines = [f'# Cắt vấp', '',
         f'- Raw {mm(U["to"])} → cut.mp4 {mm(raw_kept/SPEED)} (tốc độ ×{SPEED:g}).',
         f'- Bỏ {len(dropped)} đoạn, cắt chữ {len(cuts.get("trim", []))} chỗ, {len(keep)} đoạn giữ lại.',
         f'- Khoảng lặng: dưới {KEEP_GAP}s giữ nguyên, dài hơn rút về khoảng {2*PAD:.2f}s; im từ {LONG:g}s (chuyển cảnh) giữ khoảng {2*PAD_LONG:.1f}s.', '',
         '| Ở cut.mp4 | Raw | Bỏ | Lý do |', '|---|---|---|---|']
for d in cuts.get('drop', []):
    us = [utts[i] for i in d['ids']]
    txt = ' / '.join((u.get('text') or '[không rõ]') for u in us)
    lines.append(f"| {mm(land(us[0]['start']))} | {mm(us[0]['start'])}-{mm(us[-1]['end'])} | {txt[:140]} | {d.get('why', '')} |")
listed = {i for d in cuts.get('drop', []) for i in d['ids']}
for i in order:
    if utts[i].get('marker') and i not in listed:
        lines.append(f"| {mm(land(utts[i]['start']))} | {mm(utts[i]['start'])} | {utts[i].get('text', '')} | lệnh cắt bằng giọng |")
for t in cuts.get('trim', []):
    u = utts[t['id']]
    lines.append(f"| {mm(to_out(u['start']) or land(u['start']))} | {mm(u['start'])} | (trong câu) {t['text']} | {t.get('why', '')} |")
(R/'cut-report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'{len(keep)} segments, raw kept {raw_kept:.1f}s of {U["to"]:.0f}s -> cut.mp4 {raw_kept/SPEED:.1f}s, '
      f'dropped {len(dropped)} utterances, {len(cuts.get("trim", []))} trims, {len(segments)} transcript segments -> ../assets/transcript.*')
