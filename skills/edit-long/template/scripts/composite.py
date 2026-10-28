# One ffmpeg pass: source video + punch-in zooms + every overlay (FFV1 alpha) + SFX bed -> renders/final.mp4.
# Layers enter through lazy movie= sources (one decoded frame each in RAM), never split/trim of the main input.
# Usage: python scripts/composite.py                  full video
#        python scripts/composite.py --range 95,140   draft of one stretch -> renders/range-95-140.mp4
import subprocess, sys
from common import R, FPS, W, H, CACHE, frame, video, load_json, P

O = load_json('overlays.json')
N = frame(P['duration'])
a, b = 0, N
out = R/'renders'/'final.mp4'
if '--range' in sys.argv:
    s0, s1 = map(float, sys.argv[sys.argv.index('--range')+1].split(','))
    a, b = frame(s0), min(N, frame(s1))
    out = R/'renders'/f'range-{s0:g}-{s1:g}.mp4'
bed = R/'assets'/'sfx-bed.wav'

g = []
z = [x for x in O['zooms'] if x['f1'] > a and x['f0'] < b]
if z:
    on = lambda x: f"between(in+{a},{x['f0']},{x['f1']-1})"
    Z = '1' + ''.join(f"+{x['scale']-1:.4f}*{on(x)}" for x in z)
    CX = '0.5' + ''.join(f"+{x['cx']-.5:.4f}*{on(x)}" for x in z)
    CY = '0.5' + ''.join(f"+{x['cy']-.5:.4f}*{on(x)}" for x in z)
    g.append(f"[0:v]zoompan=z='{Z}':x='(iw-iw/zoom)*({CX})':y='(ih-ih/zoom)*({CY})':d=1:s={W}x{H}:fps={FPS}[v0]")
else:
    g.append('[0:v]null[v0]')

k = 0
for o in sorted(O['overlays'], key=lambda o: o['frame']):
    F, n = o['frame'], o['total']
    if F+n <= a or F >= b:
        continue
    path = f"cache/{o['id']}.{o['hash']}.mkv"
    if not (R/path).exists():
        raise SystemExit(f'missing {path}: run render_overlays.py first')
    skip = max(0, a-F)
    chain = f"movie='{path}'"
    if o['loop']:
        chain += f",loop=loop={o['loop']['count']}:size=1:start={o['loop']['start']}"
    if skip:
        chain += f',trim=start_frame={skip}'
    chain += f',setpts=PTS-STARTPTS+{F+skip-a}/{FPS}/TB'
    chain += ',format=yuv444p' if o['full'] else ',scale=out_color_matrix=bt709:out_range=tv,format=yuva444p'
    g.append(f'{chain}[l{k}]')
    g.append(f'[v{k}][l{k}]overlay=eof_action=pass:format=yuv444[v{k+1}]')
    k += 1
g.append(f'[v{k}]format=yuv420p[v]')
if bed.exists():
    g.append('[0:a]aresample=48000[a0];[1:a][a0]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95:level=false[a]')
(R/'renders').mkdir(exist_ok=True)
(R/'renders'/'graph.txt').write_text(';\n'.join(g), encoding='utf-8')

seek = ['-ss', f'{a/FPS:.4f}', '-to', f'{b/FPS:.4f}'] if (a, b) != (0, N) else []
cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-stats_period', '10', '-stats', '-y', *seek, '-i', str(video())]
if bed.exists():
    cmd += [*seek, '-i', str(bed)]
cmd += ['-/filter_complex', str(R/'renders'/'graph.txt'), '-map', '[v]', '-map', '[a]' if bed.exists() else '0:a',
        '-c:v', 'h264_nvenc', '-preset', 'p5', '-tune', 'hq', '-rc', 'vbr', '-cq', '19', '-b:v', '0', '-g', '60',
        '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
        '-fps_mode', 'cfr', '-frames:v', str(b-a), '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(out)]
print(f'{k} layers, {len(z)} zooms, frames {a}-{b}', flush=True)
subprocess.run(cmd, cwd=R, check=True)
print('->', out)
