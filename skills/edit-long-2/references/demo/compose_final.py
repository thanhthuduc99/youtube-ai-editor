# Builds the final: the timeline is split into pieces (plain cut, a rendered scene, a scene tail), each piece encoded alike,
# then joined without re-encoding (keeps RAM low with 80+ scenes). Audio = the cut's voice (user dropped the intro music 30/10).
# Usage: python compose_final.py  ->  ../renders/final-edit2.mp4
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent/'cut/renders/cut.mp4'
OUT = HERE.parent/'renders/final-edit2.mp4'
FPS = 30
WORK = HERE/'renders/pieces'
WORK.mkdir(exist_ok=True)
plan = json.loads((HERE/'final_plan.json').read_text(encoding='utf-8'))
total = int(subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v', '-show_entries', 'stream=nb_read_packets',
                            '-of', 'csv=p=0', str(SRC)], capture_output=True, text=True).stdout.strip(' ,\n'))

layers = [(p['from'], p['frames'], f"{p['id']}.mp4") for p in plan]
layers += [(p['from'] + p['frames'], p['tail'], f"{p['id']}-tail.mp4") for p in plan if p.get('tail')]
pieces, t = [], 0
for at, n, f in sorted(layers):
    if at > t:
        pieces.append((t, at - t, None))
    pieces.append((at, n, f))
    t = at + n
if t < total:
    pieces.append((t, total - t, None))

ENC = ['-an', '-c:v', 'h264_nvenc', '-cq', '18', '-preset', 'p5', '-g', '60', '-pix_fmt', 'yuv420p', '-r', str(FPS),
       '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709']
lst = []
for k, (at, n, f) in enumerate(pieces):
    dst = WORK/f'{k:03d}.mp4'
    if f is None:
        src = ['-ss', f'{at/FPS:.4f}', '-i', str(SRC)]
        vf = 'null'
    else:
        src = ['-i', str(HERE/'renders'/f)]
        vf = 'scale=in_range=pc:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', *src, '-frames:v', str(n), '-vf', vf, *ENC, '-y', str(dst)], check=True)
    lst.append(f"file '{dst.as_posix()}'")
(WORK/'list.txt').write_text('\n'.join(lst), encoding='utf-8')
video = WORK/'video.mp4'
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(WORK/'list.txt'), '-c', 'copy', '-y', str(video)], check=True)

subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', str(video), '-i', str(SRC), '-map', '0:v', '-map', '1:a', '-c', 'copy',
                '-movflags', '+faststart', '-y', str(OUT)], check=True)
print(OUT, len(pieces), 'pieces')
