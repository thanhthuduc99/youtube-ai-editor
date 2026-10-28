# Renders every overlay composition with HyperFrames as an RGBA PNG sequence (exact colours, no ProRes matrix issue),
# packs it into cache/<id>.<hash>.mkv (FFV1 RGBA for corner overlays, H.264 4:4:4 for opaque full-frame ones),
# deletes the PNGs. Cached by content hash: only changed overlays re-render.
# Usage: python scripts/render_overlays.py [ov-003 ov-007 ...]
import re, shutil, subprocess, sys, time
from common import R, HF, CACHE, FPS, ff, load_json

OV = load_json('overlays.json')['overlays']
only = set(sys.argv[1:])
CACHE.mkdir(exist_ok=True)
todo = [o for o in OV if (not only or o['id'] in only) and not o.get('prerendered') and not (CACHE/f"{o['id']}.{o['hash']}.mkv").exists()]
print(f'{len(todo)} of {len(OV)} overlays to render', flush=True)
for k, o in enumerate(todo, 1):
    t0 = time.time()
    out = CACHE/f"{o['id']}.{o['hash']}.mkv"
    seq = CACHE/f"_{o['id']}"
    for attempt in range(3):  # Windows sometimes holds the fresh PNG folder (indexer/AV): HyperFrames' final rename fails EPERM
        shutil.rmtree(seq, ignore_errors=True)
        r = subprocess.run([*HF, 'render', '.', '-c', o['file'], '--format', 'png-sequence', '--fps', str(FPS),
                            '--workers', '2', '--quiet', '-o', str(seq)], cwd=R, shell=False)
        if r.returncode == 0:
            break
        print(f"{o['id']}: render failed (attempt {attempt+1}), retrying", flush=True); time.sleep(5)
    else:
        raise SystemExit(f"{o['id']}: render failed 3 times")
    pngs = sorted(seq.rglob('*.png'))
    if len(pngs) != o['frames']:
        raise SystemExit(f"{o['id']}: {len(pngs)} frames rendered, expected {o['frames']}")
    first = pngs[0]
    m = re.match(r'(.*?)(\d+)\.png$', first.name)
    pattern = f'{m.group(1)}%0{len(m.group(2))}d.png'
    src = ['-framerate', FPS, '-start_number', int(m.group(2)), '-i', first.parent/pattern]
    if o['full']:  # opaque cut-in: visually lossless H.264 4:4:4, BT.709
        ff(*src, '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv444p', '-c:v', 'libx264', '-preset', 'medium',
           '-crf', '12', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', out)
    else:          # corner overlay: lossless RGBA, tiny because most of the frame is transparent
        ff(*src, '-c:v', 'ffv1', '-level', '3', '-pix_fmt', 'bgra', '-g', '1', out)
    shutil.rmtree(seq)
    for old in CACHE.glob(f"{o['id']}.*.mkv"):
        if old != out:
            old.unlink()
    print(f"[{k}/{len(todo)}] {o['id']} {o['frames']} frames {time.time()-t0:.0f}s -> {out.name}", flush=True)
