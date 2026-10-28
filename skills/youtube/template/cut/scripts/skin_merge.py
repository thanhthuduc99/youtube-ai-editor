# Take the skin from one render and everything else from another: out = base outside the skin, look on the skin.
# Skin mask = MediaPipe selfie segmenter (person) x skin colour (YCrCb) on the base frame, closed, feathered and smoothed
# over time so it does not flicker. Background, hair, shirt stay exactly as in base.
#   python skin_merge.py base.png look.png out.png [--mask mask.png]
#   python skin_merge.py base.mp4 look.mp4 out.mp4          (same frame count; audio from base)
import argparse, os, subprocess
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions, vision

ap = argparse.ArgumentParser()
ap.add_argument('base'); ap.add_argument('look'); ap.add_argument('out'); ap.add_argument('--mask', default='')
a = ap.parse_args()
video = a.base.lower().endswith(('.mp4', '.mov', '.mkv'))
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path=os.path.join(os.path.expanduser('~'), '.cache', 'mediapipe', 'selfie_segmenter.tflite')),
    running_mode=vision.RunningMode.VIDEO if video else vision.RunningMode.IMAGE, output_confidence_masks=True))
prev = None


def skin_mask(img, ts=0):
    global prev
    rgb = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    r = seg.segment_for_video(rgb, ts) if video else seg.segment(rgb)
    person = r.confidence_masks[0].numpy_view().astype(np.float32)
    person = cv2.resize(person, (img.shape[1], img.shape[0]))
    ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb).astype(np.float32)
    cr, cb = ycc[..., 1], ycc[..., 2]
    # soft skin range: full weight inside Cr 138-172 / Cb 90-128, fading 8 units outside
    w = lambda v, lo, hi, f=8: np.clip(np.minimum(v - (lo - f), (hi + f) - v) / f, 0, 1)
    skin = w(cr, 138, 172) * w(cb, 90, 128) * np.clip((ycc[..., 0] - 40) / 30, 0, 1)
    m = (skin * np.clip((person - 0.3) / 0.4, 0, 1)).astype(np.float32)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    m = cv2.GaussianBlur(m, (0, 0), 5)
    prev = m if prev is None or not video else prev * 0.5 + m * 0.5
    return prev


def merge(base, look, ts=0):
    m = skin_mask(base.astype(np.uint8), ts)[..., None]
    return (base * (1 - m) + look * m).clip(0, 255).astype(np.uint8), m


if not video:
    out, m = merge(cv2.imread(a.base).astype(np.float32), cv2.imread(a.look).astype(np.float32))
    cv2.imwrite(a.out, out)
    if a.mask:
        cv2.imwrite(a.mask, (m[..., 0] * 255).astype(np.uint8))
    raise SystemExit
pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate',
                     '-of', 'default=nw=1:nk=1', a.base], capture_output=True, text=True).stdout.split()
W, H, fps = int(pr[0]), int(pr[1]), eval(pr[2])
rd = lambda p: subprocess.Popen(['ffmpeg', '-v', 'error', '-i', p, '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
rb, rl = rd(a.base), rd(a.look)
wr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-',
                       '-i', a.base, '-map', '0:v', '-map', '1:a?', '-c:a', 'copy', '-c:v', 'libx264', '-crf', '15', '-preset', 'fast',
                       '-pix_fmt', 'yuv420p', a.out], stdin=subprocess.PIPE)
n, size = 0, W * H * 3
while True:
    b, l = rb.stdout.read(size), rl.stdout.read(size)
    if len(b) < size or len(l) < size:
        break
    out, _ = merge(np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32),
                   np.frombuffer(l, np.uint8).reshape(H, W, 3).astype(np.float32), int(n * 1000 / fps))
    wr.stdin.write(out.tobytes()); n += 1
wr.stdin.close(); wr.wait()
print('frames', n)
