"""Chỉnh da kiểu CapCut (bảng Skin) cho video talking-head: MediaPipe FaceLandmarker + OpenCV.
Thang 0-100 giống CapCut. Mặc định = bộ Thanh chốt 20/10/2026: clear 29, smooth 29, blemish 14,
facelift 12, even 11, KHÔNG làm trắng, KHÔNG đổi tông da (bản trắng + hồng bị chê "da ghê").
Không chỉnh sáng cả khung. Cần: pip install mediapipe + model ~/.cache/mediapipe/face_landmarker.task
  python beauty.py in.mp4 out.mp4 [--workers 6] [--ss 8 --t 8] [--side]
  python beauty.py in.png out.png
"""
import argparse
import os
import subprocess
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions, vision

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("dst")
ap.add_argument("--ss", type=float, default=0)
ap.add_argument("--t", type=float, default=0)
ap.add_argument("--side", action="store_true")
ap.add_argument("--workers", type=int, default=max(1, min(6, (os.cpu_count() or 2) // 2)))
ap.add_argument("--chunk", default="", help="nội bộ: start_frame:n_frames, ghi video không tiếng")
for k, v in dict(clear=29, smooth=29, whitening=0, blemish=14, facelift=12, even=11, pink=0).items():
    ap.add_argument(f"--{k}", type=float, default=v)
a = ap.parse_args()

MODEL = os.path.join(os.path.expanduser("~"), ".cache", "mediapipe", "face_landmarker.task")
C = vision.FaceLandmarksConnections
idx = lambda conns: sorted({c.start for c in conns} | {c.end for c in conns})
OVAL, LEYE, REYE = idx(C.FACE_LANDMARKS_FACE_OVAL), idx(C.FACE_LANDMARKS_LEFT_EYE), idx(C.FACE_LANDMARKS_RIGHT_EYE)
LBROW, RBROW, LIPS = idx(C.FACE_LANDMARKS_LEFT_EYEBROW), idx(C.FACE_LANDMARKS_RIGHT_EYEBROW), idx(C.FACE_LANDMARKS_LIPS)
NOSTRIL = [97, 2, 326, 327, 294, 278, 48, 64, 98, 240, 460]
# Cặp điểm má/hàm 2 bên dùng cho facelift (kéo vào trong theo chiều ngang).
JAW_L = [234, 93, 132, 58, 172, 136, 150]
JAW_R = [454, 323, 361, 288, 397, 365, 379]

video = a.src.lower().endswith((".mp4", ".mov", ".mkv"))
lm_opts = vision.FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL),
    running_mode=vision.RunningMode.VIDEO if video else vision.RunningMode.IMAGE, num_faces=1)
landmarker = vision.FaceLandmarker.create_from_options(lm_opts)
skin_mean = None  # trung bình LAB của da, làm mượt theo thời gian


def hull_mask(shape, pts, ids, dilate=0):
    m = np.zeros(shape, np.uint8)
    cv2.fillConvexPoly(m, cv2.convexHull(pts[ids].astype(np.int32)), 255)
    if dilate:
        m = cv2.dilate(m, np.ones((dilate, dilate), np.uint8))
    return m


def beautify(img, ts_ms=0):
    global skin_mean
    H, W = img.shape[:2]
    rgb = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    res = landmarker.detect_for_video(rgb, ts_ms) if video else landmarker.detect(rgb)
    if not res.face_landmarks:
        return img
    pts = np.array([(p.x * W, p.y * H) for p in res.face_landmarks[0]], np.float32)
    fw = pts[OVAL, 0].max() - pts[OVAL, 0].min()

    # Chỉ xử lý vùng quanh mặt + cổ.
    x0, y0 = int(max(0, pts[:, 0].min() - fw * 0.4)), int(max(0, pts[:, 1].min() - fw * 0.3))
    x1, y1 = int(min(W, pts[:, 0].max() + fw * 0.4)), int(min(H, pts[:, 1].max() + fw * 0.9))
    full, img = img, img[y0:y1, x0:x1].astype(np.float32)
    pts = pts - (x0, y0)
    shp = img.shape[:2]

    # Mask da: oval mặt trừ mắt, lông mày, môi, lỗ mũi. Cổ: màu da bên dưới cằm.
    face = hull_mask(shp, pts, OVAL)
    feats = np.zeros(shp, np.uint8)
    d = max(3, int(fw * 0.03)) | 1
    for ids in (LEYE, REYE, LBROW, RBROW, LIPS):
        feats |= hull_mask(shp, pts, ids, d)
    feats |= hull_mask(shp, pts, NOSTRIL, d)
    ycc = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2YCrCb)
    skin_col = cv2.inRange(ycc, (35, 130, 77), (255, 180, 135))
    chin_y = int(pts[OVAL, 1].max())
    neck = np.zeros(shp, np.uint8)
    cx = int(pts[OVAL, 0].mean())
    cv2.rectangle(neck, (cx - int(fw * 0.42), chin_y - int(fw * 0.1)), (cx + int(fw * 0.42), shp[0]), 255, -1)
    # Trán sát chân tóc nằm ngoài oval của MediaPipe: lấy thêm theo màu da phía trên lông mày.
    top_y = int(pts[OVAL, 1].min())
    brow_y = int(pts[LBROW + RBROW, 1].min())
    fore = np.zeros(shp, np.uint8)
    cv2.rectangle(fore, (cx - int(fw * 0.38), max(0, top_y - int(fw * 0.25))), (cx + int(fw * 0.38), brow_y), 255, -1)
    skin = (face | ((neck | fore) & skin_col)) & ~feats
    skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    soft = cv2.GaussianBlur(skin, (0, 0), fw * 0.015 + 2).astype(np.float32) / 255.0
    feat_soft = cv2.GaussianBlur(feats, (0, 0), 3).astype(np.float32) / 255.0
    s3 = soft[..., None]

    out = img.copy()

    # 1. Clear blemishes: chấm nhỏ tối/đỏ hơn da quanh nó -> vá.
    if a.blemish > 0:
        core = cv2.erode(skin, np.ones((d * 3, d * 3), np.uint8)) & face
        lab = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
        r = fw / 25
        dark = cv2.GaussianBlur(lab[..., 0], (0, 0), r) - lab[..., 0]
        red = lab[..., 1] - cv2.GaussianBlur(lab[..., 1], (0, 0), r)
        k = a.blemish / 100
        spots = (((dark > 9 - 5 * k) | (red > 5 - 2 * k)) & (core > 0)).astype(np.uint8) * 255
        n, lbl, st, _ = cv2.connectedComponentsWithStats(spots)
        big = [i for i in range(1, n) if not (3 <= st[i, cv2.CC_STAT_AREA] <= fw * fw * 0.002)]
        spots[np.isin(lbl, big)] = 0
        spots = cv2.dilate(spots, np.ones((5, 5), np.uint8))
        if spots.any():
            healed = cv2.inpaint(out.astype(np.uint8), spots, 5, cv2.INPAINT_TELEA).astype(np.float32)
            km = cv2.GaussianBlur(spots, (0, 0), 1.5).astype(np.float32)[..., None] / 255.0 * min(1, 0.5 + k * 3)
            out = out * (1 - km) + healed * km

    # 2. Smooth: tách tần số, giữ lại vân da để không thành da nhựa.
    if a.smooth > 0:
        sm = a.smooth / 100
        q = cv2.resize(out.astype(np.uint8), (shp[1] // 3, shp[0] // 3), interpolation=cv2.INTER_AREA)
        base = cv2.bilateralFilter(q, 0, 25, max(2, fw / 90))
        base = cv2.resize(base, (shp[1], shp[0]), interpolation=cv2.INTER_LINEAR).astype(np.float32)
        base = cv2.GaussianBlur(base, (0, 0), fw / 200 + 1)
        high = out - cv2.GaussianBlur(out, (0, 0), 1.4)
        smooth = base + high * (1 - sm)
        out = out * (1 - s3 * min(1, sm * 2.2)) + smooth * s3 * min(1, sm * 2.2)

    # 3. Even + whitening + skin tone hồng: làm trong LAB.
    lab = cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
    if a.even > 0:
        # Đều màu: kéo chroma về trung bình vùng lớn (bớt mảng đỏ, thâm).
        ev = a.even / 100 * 2.2
        for c in (1, 2):
            big = cv2.GaussianBlur(lab[..., c], (0, 0), fw / 12)
            lab[..., c] += (big - lab[..., c]) * ev * soft
    m = skin > 0
    cur = lab[m].mean(0)
    skin_mean = cur if skin_mean is None or not video else skin_mean * 0.85 + cur * 0.15
    wl = a.whitening / 100
    # Whitening: nâng sáng da theo đường cong (vùng tối lên nhiều hơn vùng đã sáng).
    lab[..., 0] += (255 - lab[..., 0]) * wl * 0.55 * soft
    # Skin tone hồng nhạt: b (vàng) về gần trung tính, a (hồng) nhích lên nhẹ.
    pk = a.pink / 100
    lab[..., 2] -= (skin_mean[2] - 129) * pk * soft
    lab[..., 1] += (140 - skin_mean[1]) * pk * 0.6 * soft
    out = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)

    # 4. Clear: làm nét mắt, lông mày, môi + chút tương phản cục bộ.
    if a.clear > 0:
        cl = a.clear / 100
        blur = cv2.GaussianBlur(out, (0, 0), 1.6)
        sharp = out + (out - blur) * (cl * 2.5)
        fm = np.clip(feat_soft + 0.25 * soft * cl, 0, 1)[..., None]
        out = out * (1 - fm) + sharp * fm

    out = np.clip(out, 0, 255).astype(np.uint8)

    # 5. Facelift: kéo má/hàm vào trong theo chiều ngang, mờ dần ra xa.
    if a.facelift > 0:
        fl = a.facelift / 100 * fw * 0.06
        gx, gy = np.meshgrid(np.arange(shp[1], dtype=np.float32), np.arange(shp[0], dtype=np.float32))
        mapx = gx.copy()
        sig = fw * 0.12
        for ids, sign in ((JAW_L, -1), (JAW_R, 1)):
            for i in ids:
                px, py = pts[i]
                wgt = np.exp(-((gx - px) ** 2 + (gy - py) ** 2) / (2 * sig * sig))
                mapx += sign * fl * wgt / len(ids) * 3
        out = cv2.remap(out, mapx, gy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

    res_img = full.copy()
    res_img[y0:y1, x0:x1] = out
    return res_img


if not video:
    cv2.imwrite(a.dst, beautify(cv2.imread(a.src)))
    raise SystemExit

pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate",
                     "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", a.src], capture_output=True, text=True).stdout.split()
W, H, fps, dur = int(pr[0]), int(pr[1]), eval(pr[2]), float(pr[3])


def run(cut, dst, with_audio, t0=0, limit=()):
    """Đọc khung từ ffmpeg, chỉnh, ghi ra ffmpeg. t0 = mốc thời gian (ms) của khung đầu, cho landmarker VIDEO."""
    rd = subprocess.Popen(["ffmpeg", "-v", "error", *cut, "-i", a.src, *limit, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                          stdout=subprocess.PIPE)
    oW = W * 2 if a.side else W
    audio = [*cut, "-i", a.src, "-map", "0:v", "-map", "1:a?", "-c:a", "aac", "-b:a", "192k", "-shortest"] if with_audio else ["-an"]
    wr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{oW}x{H}", "-r", str(fps),
                           "-i", "-", *audio, "-c:v", "libx264", "-crf", "15", "-preset", "fast", "-pix_fmt", "yuv420p",
                           "-g", "30", dst], stdin=subprocess.PIPE)
    size, n = W * H * 3, 0
    while True:
        buf = rd.stdout.read(size)
        if len(buf) < size:
            break
        fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        o = beautify(fr, t0 + int(n * 1000 / fps))
        wr.stdin.write((np.hstack([fr, o]) if a.side else o).tobytes())
        n += 1
    wr.stdin.close()
    wr.wait()
    return n


if a.chunk:
    start, count = (int(v) for v in a.chunk.split(":"))
    # Cắt theo SỐ KHUNG bằng trim, không dùng -ss: seek theo giây làm lệch 1-2 khung ở mỗi chỗ nối.
    run([], a.dst, False, int(start * 1000 / fps),
        ["-vf", f"trim=start_frame={start}:end_frame={start + count},setpts=PTS-STARTPTS"])
    raise SystemExit

if a.ss or a.t or a.side or a.workers <= 1:
    cut = (["-ss", str(a.ss)] if a.ss else []) + (["-t", str(a.t)] if a.t else [])
    print("frames", run(cut, a.dst, True))
    raise SystemExit

# Chia video thành nhiều đoạn chạy song song (mỗi khung ~1 giây trên 1 nhân), rồi nối lại + lấy tiếng gốc.
import sys
import tempfile
total = int(round(dur * fps))
per = -(-total // a.workers)
tmp = tempfile.mkdtemp(prefix="beauty-", dir=os.path.dirname(os.path.abspath(a.dst)))
parts, procs = [], []
for k in range(a.workers):
    st = k * per
    if st >= total:
        break
    part = os.path.join(tmp, f"p{k:02d}.mp4")
    parts.append(part)
    procs.append(subprocess.Popen([sys.executable, os.path.abspath(__file__), a.src, part, "--chunk", f"{st}:{min(per, total - st)}",
                                   *sum(([f"--{k_}", str(getattr(a, k_))] for k_ in
                                         ("clear", "smooth", "whitening", "blemish", "facelift", "even", "pink")), [])]))
if any(p.wait() for p in procs):
    raise SystemExit("beauty: 1 đoạn bị lỗi")
lst = os.path.join(tmp, "list.txt")
with open(lst, "w", encoding="utf-8") as f:
    f.writelines(f"file '{p}'\n" for p in parts)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", a.src, "-map", "0:v", "-map", "1:a?",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", a.dst], check=True)
for p in parts + [lst]:
    os.remove(p)
os.rmdir(tmp)
print("frames", total, "workers", len(parts))
