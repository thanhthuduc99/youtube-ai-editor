# Word-timestamped transcript with local faster-whisper (no API key) -> assets/transcript.json + transcript.txt.
# No hotwords/initial_prompt: they make whisper paraphrase ("mình" -> "tôi"); fix terms with project.json "fixes".
# Long audio is split into ~8 min chunks at silences; each chunk is saved so a crash resumes where it stopped.
import json, re, subprocess
from faster_whisper import WhisperModel
from common import R, P, ff

A = R/'assets'; C = A/'chunks'; C.mkdir(exist_ok=True)
DUR = P['duration']; TARGET = 480

log = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(A/'speech.wav'), '-af', 'silencedetect=noise=-35dB:d=0.4',
                      '-f', 'null', '-'], capture_output=True, text=True, errors='replace').stderr
starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
mids = [(a+b)/2 for a, b in zip(starts, ends)]
cuts = [0.0]
while DUR - cuts[-1] > TARGET*1.4:
    want = cuts[-1] + TARGET
    near = [m for m in mids if abs(m-want) < 60]
    cuts.append(min(near, key=lambda m: abs(m-want)) if near else want)
cuts.append(DUR)

model = None
out = []
for i, (a, b) in enumerate(zip(cuts, cuts[1:])):
    cj = C/f'{i:02}-{a:.2f}.json'
    if not cj.exists():
        if model is None:
            model = WhisperModel(P.get('whisper_model', 'medium'), device='cpu', compute_type='int8', cpu_threads=8)
        wav = C/f'{i:02}.wav'
        ff('-ss', f'{a:.3f}', '-to', f'{b:.3f}', '-i', A/'speech.wav', wav)
        segs, _ = model.transcribe(str(wav), language=P.get('language', 'vi'), word_timestamps=True, beam_size=5,
                                   vad_filter=True, condition_on_previous_text=False)
        rows = []
        for s in segs:
            rows.append({'start': round(s.start+a, 3), 'end': round(s.end+a, 3), 'text': s.text.strip(),
                         'words': [{'word': w.word, 'start': round(w.start+a, 3), 'end': round(w.end+a, 3)} for w in s.words]})
            print(f'{s.start+a:7.2f} {s.text.strip()}', flush=True)
        cj.write_text(json.dumps(rows, ensure_ascii=False), encoding='utf-8'); wav.unlink()
    out += json.loads(cj.read_text(encoding='utf-8'))


def fix(text):
    for k, v in P.get('fixes', {}).items():
        text = text.replace(k, v)
    return text


for s in out:
    s['text'] = fix(s['text'])
    for w in s['words']:
        w['word'] = fix(w['word'])
(A/'transcript.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
(A/'transcript.txt').write_text('\n'.join(f"[{int(s['start']//60)}:{s['start'] % 60:05.2f}] {s['text']}" for s in out), encoding='utf-8')
print(f'{len(out)} segments, {len(cuts)-1} chunks -> assets/transcript.json, transcript.txt')
