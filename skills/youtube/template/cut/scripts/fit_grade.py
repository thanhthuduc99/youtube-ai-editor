# Learn the creator's CapCut look from a pair: the raw clip and the SAME clip exported from CapCut with only the grade
# applied (no cut, no speed). Fits a 33^3 3D LUT (mean output colour per input colour bin, empty bins filled from
# neighbours), writes work/grade.cube, and reports how close raw+LUT gets to the CapCut frames plus how much fine detail
# CapCut removed (a smoothing/beauty filter is not a colour change and a LUT cannot copy it).
# Usage: python cut/scripts/fit_grade.py <raw clip> <capcut clip> [--frames 40]
import argparse, subprocess
from pathlib import Path
import numpy as np
from scipy.ndimage import uniform_filter

WK = Path(__file__).resolve().parents[1]/'work'
ap = argparse.ArgumentParser(); ap.add_argument('raw'); ap.add_argument('graded'); ap.add_argument('--frames', type=int, default=40)
args = ap.parse_args()
N = 33


def frames(src, n):
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src],
                               capture_output=True, text=True).stdout)
    out = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'fps={n/dur:.5f},scale=960:540', '-frames:v', str(n),
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(out, np.uint8).reshape(-1, 540, 960, 3).astype(np.float32)/255


A, B = frames(args.raw, args.frames), frames(args.graded, args.frames)
n = min(len(A), len(B)); A, B = A[:n], B[:n]
idx = np.clip(np.rint(A*(N-1)).astype(int), 0, N-1).reshape(-1, 3)
flat = idx[:, 0]*N*N + idx[:, 1]*N + idx[:, 2]
cnt = np.bincount(flat, minlength=N**3)
lut = np.stack([np.bincount(flat, B.reshape(-1, 3)[:, c], minlength=N**3) for c in range(3)], 1)
grid = np.stack(np.meshgrid(*[np.linspace(0, 1, N)]*3, indexing='ij'), -1).reshape(-1, 3)
lut = np.where(cnt[:, None] > 0, lut/np.maximum(cnt, 1)[:, None], np.nan)
known = ~np.isnan(lut[:, 0])
shift = np.nanmedian(lut[known]-grid[known], 0)                      # fill empty bins: identity + median shift, then smooth
filled = np.where(known[:, None], lut, grid+shift).reshape(N, N, N, 3)
w = np.where(known, np.minimum(cnt, 50)/50, 0.05).reshape(N, N, N, 1)
sm = uniform_filter(filled*w, size=(3, 3, 3, 1))/np.maximum(uniform_filter(w, size=(3, 3, 3, 1)), 1e-6)
final = np.where(w > 0.5, filled, sm).clip(0, 1)
with open(WK/'grade.cube', 'w') as f:
    f.write(f'TITLE "creator capcut look"\nLUT_3D_SIZE {N}\n')
    for b in range(N):          # .cube order: red fastest
        for g in range(N):
            for r in range(N):
                f.write('%.6f %.6f %.6f\n' % tuple(final[r, g, b]))
pred = final[idx[:, 0], idx[:, 1], idx[:, 2]].reshape(B.shape)
hf = lambda x: np.abs(x.mean(-1) - uniform_filter(x.mean(-1), size=(1, 5, 5))).mean()
print(f'frames {n}, bins used {known.sum()}/{N**3}')
print(f'mean abs error  raw vs capcut {np.abs(A-B).mean()*255:.2f}   raw+LUT vs capcut {np.abs(pred-B).mean()*255:.2f}  (0-255)')
print(f'fine detail     raw {hf(A)*255:.2f}  capcut {hf(B)*255:.2f}  -> capcut keeps {hf(B)/hf(A)*100:.0f}% of the detail')
print('->', WK/'grade.cube', '   apply: ffmpeg ... -vf lut3d=file=grade.cube')
