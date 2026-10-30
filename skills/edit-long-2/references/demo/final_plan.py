# Picks the scenes that go into the final and cuts a full-res face clip for each from the cut video.
# Scene ranges: every clips*.txt ("<id> <start> <end>" in seconds of the cut). One file per agent avoids write clashes.
# Overlaps: the earlier scene ends where the next one starts. A scene with id 'sim' (screen simulation) runs to its end alone.
# Usage: python final_plan.py  ->  final_plan.json + clips-hd/<id>.mp4
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent/'cut/renders/cut.mp4'
FPS, TAIL = 30, 18

rows = []  # (start, end, id)
for f in sorted(HERE.glob('clips*.txt')):
    for line in f.read_text().split('\n'):
        if line.strip():
            n, a, b = line.split()
            rows.append((float(a), float(b), n))
sim = next((r for r in rows if r[2] == 'sim'), None)
rows = sorted(r for r in rows if r[2] != 'sim' and (sim is None or r[0] < sim[0]))
plan = []
for i, (a, b, n) in enumerate(rows):
    if i + 1 < len(rows):
        b = min(b, rows[i + 1][0])
    plan.append({'id': n, 'a': a, 'b': b})
if sim:
    plan.append({'id': 'sim', 'a': sim[0], 'b': sim[1]})
for p in plan:
    p['from'] = round(p['a']*FPS)            # first frame in the cut
    p['frames'] = round((p['b'] - p['a'])*FPS)
# a scene that ends on plain face gets TAIL frames where the face card grows back to full frame (no hard jump)
for p, q in zip(plan, plan[1:]):
    p['tail'] = TAIL if q['from'] - (p['from'] + p['frames']) >= TAIL else 0
plan[-1]['tail'] = 0
tmp = HERE/f'final_plan.{subprocess.os.getpid()}.tmp'  # several agents run this at once
tmp.write_text(json.dumps(plan, indent=1), encoding='utf-8')
tmp.replace(HERE/'final_plan.json')
total = sum(p['frames'] for p in plan)
print(len(plan), 'scenes,', total, 'frames to render')

out = HERE/'clips-hd'
out.mkdir(exist_ok=True)
for p in plan:
    dst = out/f"{p['id']}.mp4"
    if dst.exists() and int(subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v', '-show_entries', 'stream=nb_read_packets',
                                           '-of', 'csv=p=0', str(dst)], capture_output=True, text=True).stdout.strip(' ,\n')) >= p['frames'] + p['tail']:
        continue
    # the browser seeks every frame, so keep keyframes close (-g 10)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-ss', f"{p['from']/FPS:.4f}", '-i', str(SRC), '-frames:v', str(p['frames'] + p['tail'] + 2),
                    '-an', '-c:v', 'h264_nvenc', '-cq', '17', '-g', '10', '-bf', '0', '-movflags', '+faststart', '-y', str(dst)], check=True)
    print(p['id'], p['from'], p['frames'])
