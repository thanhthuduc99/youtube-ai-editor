# Editor notes "che mờ ..." (cuts.json notes): blur rectangles over a raw time range, mapped onto cut.mp4 through keep.json.
# Claude picks each rectangle by looking at full-res frames with a grid (customer names, phones, prices, emails...).
# work/blur.json: [{"raw": [757.5, 827.0], "rect": [x, y, w, h], "why": "tên khách trên bảng CRM"}]
# Usage: python cut/scripts/blur.py [--range a,b]   (cut timeline; --range renders only that window for a quick check)
import argparse, json, subprocess
from pathlib import Path

R = Path(__file__).resolve().parents[1]; WK = R/'work'
ap = argparse.ArgumentParser(); ap.add_argument('--range', default='')
args = ap.parse_args()
K = json.loads((WK/'keep.json').read_text(encoding='utf-8')); SP = K['speed']
B = json.loads((WK/'blur.json').read_text(encoding='utf-8'))


def to_cut(lo, hi):
    """Cut-timeline windows covering raw [lo, hi]."""
    out = []
    for s in K['segments']:
        a, b = max(lo, s['raw_start']), min(hi, s['raw_end'])
        if b > a:
            o = s['out_start']
            out.append((o+(a-s['raw_start'])/SP, o+(b-s['raw_start'])/SP))
    return out


t0 = float(args.range.split(',')[0]) if args.range else 0.0   # input seek: filter time starts at 0
chains, last = [], '0:v'
for i, b in enumerate(B):
    x, y, w, h = b['rect']
    win = to_cut(*b['raw'])
    if not win:
        continue
    en = '+'.join(f'between(t,{a-t0:.3f},{c-t0:.3f})' for a, c in win)
    chains.append(f'[0:v]crop={w}:{h}:{x}:{y},boxblur=20:3[b{i}];[{last}][b{i}]overlay={x}:{y}:enable=\'{en}\'[v{i}]')
    last = f'v{i}'
    print(f"blur {b.get('why', '')}: raw {b['raw']} -> cut " + ', '.join(f'{a:.1f}-{c:.1f}' for a, c in win))
src = R/'renders'/'cut.mp4'
seek = ['-ss', f'{t0:.3f}', '-t', f'{float(args.range.split(",")[1])-t0:.3f}'] if args.range else []
dst = R/'renders'/('cut-blur-check.mp4' if args.range else 'cut-blur.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *seek, '-i', str(src), '-filter_complex', ';'.join(chains), '-map', f'[{last}]', '-map', '0:a',
                '-c:v', 'h264_nvenc', '-cq', '19', '-c:a', 'copy', '-movflags', '+faststart', str(dst)], check=True)
print('->', dst)
