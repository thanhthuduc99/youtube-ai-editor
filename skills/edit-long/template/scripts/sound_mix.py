# Builds the SFX bed (assets/sfx-bed.wav, 48 kHz stereo, same length as the source) from the cue list in overlays.json.
# Written in 60 s blocks so memory stays flat on 40 min videos. composite.py mixes it under the original audio.
import json, subprocess, wave
import numpy as np
from common import R, P, sfx_dir, load_json

SR = 48000
cues = sorted(load_json('overlays.json')['sfx'], key=lambda c: c['t'])
LIB = sfx_dir()
clips = {}
for name in sorted({c['name'] for c in cues}):
    f = next((x for x in (R/'assets'/'sfx'/f'{name}.wav', R/'assets'/'sfx'/f'{name}.mp3', LIB/f'{name}.mp3') if x.exists()), None)
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(f), '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'])
    clips[name] = np.frombuffer(raw, dtype='<f4').reshape(-1, 2)

N = int(round(P['duration']*SR)); BLOCK = 60*SR
peak = 0.0
with wave.open(str(R/'assets'/'sfx-bed.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    for b0 in range(0, N, BLOCK):
        b1 = min(N, b0+BLOCK)
        buf = np.zeros((b1-b0, 2), dtype=np.float32)
        for c in cues:
            s0 = int(round(c['t']*SR)); x = clips[c['name']]
            if s0 >= b1 or s0+len(x) <= b0:
                continue
            a, z = max(s0, b0), min(s0+len(x), b1)
            buf[a-b0:z-b0] += x[a-s0:z-s0]*10**(c['gain']/20)
        peak = max(peak, float(np.abs(buf).max()) if len(buf) else 0)
        w.writeframes((np.clip(buf, -1, 1)*32767).astype('<i2').tobytes())
(R/'renders').mkdir(exist_ok=True)
(R/'renders'/'sfx-cues.json').write_text(json.dumps(cues, indent=1), encoding='utf-8')
print(f'sfx-bed.wav {N/SR:.2f}s, {len(cues)} cues from {len(clips)} files, bed peak {20*np.log10(max(peak, 1e-9)):.1f} dBFS')
