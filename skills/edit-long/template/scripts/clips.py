# One review clip per overlay (with its SFX) so the user can judge the motion of each effect on its own.
# Full-frame overlays: exactly their window. Corner overlays: 1 s of context before and after.
# Needs render_overlays.py + sound_mix.py first. Usage: python scripts/clips.py [ov-003 ...] -> review/clips/<id>-<type>.mp4
import shutil, subprocess, sys
from common import R, P, load_json

only = set(sys.argv[1:])
out = R/'review'/'clips'; out.mkdir(parents=True, exist_ok=True)
for o in load_json('overlays.json')['overlays']:
    if only and o['id'] not in only:
        continue
    pad = 0 if o['full'] else 1.0
    a = max(0.0, o['at'] - pad); b = min(P['duration'], o['at'] + o['total']/30 + pad)
    a, b = round(a, 3), round(b, 3)
    subprocess.run([sys.executable, str(R/'scripts'/'composite.py'), '--range', f'{a},{b}'], cwd=R, check=True,
                   stdout=subprocess.DEVNULL)
    src = R/'renders'/f'range-{a:g}-{b:g}.mp4'  # composite.py's own naming
    dst = out/f"{o['id']}-{o['type']}.mp4"
    shutil.move(str(src), dst)
    print(dst.name, f'{b-a:.1f}s', flush=True)
subprocess.run([sys.executable, str(R/'scripts'/'preview.py'), '--gallery'], cwd=R, check=True)
print('gallery: review/index.html')
