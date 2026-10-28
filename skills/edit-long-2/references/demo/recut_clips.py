# Re-cut every demo clip from another render of the cut (e.g. the skin-retouched cut-skin.mp4). Ranges: clips1.txt + clips2.txt.
# Usage: python recut_clips.py ../cut/renders/cut-skin.mp4
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
src = sys.argv[1]
for f in ('clips1.txt', 'clips2.txt'):
    for line in (HERE/f).read_text().split('\n'):
        if not line.strip():
            continue
        n, a, b = line.split()
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-ss', a, '-to', b, '-i', src, '-vf', 'scale=1280:-2', '-c:v', 'h264_nvenc', '-cq', '24',
                        '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-y', str(HERE/'clips'/f'{n}.mp4')], check=True)
        print(n)
