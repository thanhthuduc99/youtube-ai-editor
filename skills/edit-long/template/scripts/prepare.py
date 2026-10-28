# Probes the source, makes a CFR 30 fps H.264 mezzanine only when needed (VFR, HEVC, odd size, start != 0),
# extracts 16 kHz speech for whisper, and writes review/source-grid.jpg (12 frames) to read the layout.
# Usage: python scripts/prepare.py "<video path>"   (path is saved to project.json "source")
import json, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
from common import R, P, W, H, ff, probe_duration, save_project, video

if len(sys.argv) > 1:
    P['source'] = sys.argv[1]
src = P['source']
A = R/'assets'; A.mkdir(exist_ok=True)
free_gb = shutil.disk_usage(R).free/1e9
if free_gb < 10:
    print(f'WARNING: only {free_gb:.1f} GB free on the project drive')

pr = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', src]))
v = next(s for s in pr['streams'] if s['codec_type'] == 'video')
ok = (v['codec_name'] == 'h264' and v['r_frame_rate'] == v['avg_frame_rate'] == '30/1'
      and (v['width'], v['height']) == (W, H) and float(pr['format'].get('start_time', 0)) == 0)
if ok:
    P.pop('video', None)
else:
    out = A/'source.mp4'
    ff('-i', src, '-vf', f'fps=30,scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:-1:-1', '-c:v', 'h264_nvenc',
       '-preset', 'p5', '-rc', 'vbr', '-cq', '17', '-b:v', '0', '-g', '30', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k',
       '-movflags', '+faststart', out)
    P['video'] = str(out)
P['duration'] = round(probe_duration(video()), 3)
save_project()

ff('-i', video(), '-vn', '-ac', '1', '-ar', '16000', A/'speech.wav')

Q = R/'review'; Q.mkdir(exist_ok=True)
font = ImageFont.truetype('arial.ttf', 22)
sheet = Image.new('RGB', (4*480, 3*290), '#111'); d = ImageDraw.Draw(sheet)
for i in range(12):
    t = P['duration']*(i+.5)/12
    f = Q/f'_grid{i}.jpg'
    ff('-ss', f'{t:.2f}', '-i', video(), '-frames:v', '1', '-vf', 'scale=480:270', f)
    sheet.paste(Image.open(f), (i % 4*480, i//4*290)); f.unlink()
    d.text((i % 4*480+8, i//4*290+270), f'{int(t//60)}:{t % 60:04.1f}', font=font, fill='white')
sheet.save(Q/'source-grid.jpg', quality=90)
print(f"video={video()} duration={P['duration']}s mezzanine={'no' if ok else 'yes'} free={free_gb:.1f}GB")
