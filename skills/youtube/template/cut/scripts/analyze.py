# Splits raw speech into utterances at real silences (RMS islands checked by Silero VAD), attaches faster-whisper
# words, puts each spoken cut command ("Hey Ryan, cắt đoạn này") on its own line, and writes work/utterances.txt
# (cut rules + transcript) for the cut decision. Word timestamps are only used for meaning; cut points come from RMS.
# Usage: python cut/scripts/analyze.py "<raw video>" [--to <seconds>]   (run in the background: whisper medium on CPU)
import argparse, json, re, subprocess
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel, decode_audio
from faster_whisper.vad import VadOptions, get_speech_timestamps
from marker import find_markers, find_edit_requests, fold

R = Path(__file__).resolve().parents[1]
WK = R/'work'; WK.mkdir(exist_ok=True)
SR = 16000

ap = argparse.ArgumentParser()
ap.add_argument('src')
ap.add_argument('--to', type=float)
args = ap.parse_args()

wav = WK/'speech.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + (['-t', str(args.to)] if args.to else []) +
               ['-i', args.src, '-vn', '-ac', '1', '-ar', str(SR), str(wav)], check=True)
audio = decode_audio(str(wav), sampling_rate=SR)
args.to = args.to or round(len(audio)/SR, 3)

frames = audio[:len(audio)//160*160].reshape(-1, 160)
rms = 20*np.log10(np.sqrt((frames**2).mean(1))+1e-7)
np.save(WK/'rms.npy', rms.astype(np.float32))

# Islands of sound split at >= 0.2 s below (speech level - 20 dB); keep the ones Silero calls speech (drops clicks, breaths)
MIN_SIL = 20
loud = rms > np.percentile(rms, 70)-20
islands, a, quiet = [], None, 0
for i, x in enumerate(loud):
    if x:
        if a is None: a = i
        quiet, last = 0, i
    elif a is not None:
        quiet += 1
        if quiet >= MIN_SIL:
            islands.append((a, last+1)); a = None
if a is not None:
    islands.append((a, last+1))
speech = np.zeros(len(rms), bool)
for v in get_speech_timestamps(audio, VadOptions(min_silence_duration_ms=100, speech_pad_ms=0)):
    speech[v['start']//160:v['end']//160] = True
islands = [(a, b) for a, b in islands if speech[a:b].mean() >= 0.3]
utts = [{'start': round(max(0, a-2)/100, 3), 'end': round((b+2)/100, 3), 'words': []} for a, b in islands]

model = WhisperModel('medium', device='cpu', compute_type='int8', cpu_threads=8)
cache = WK/'words.json'
key = {'source': args.src, 'to': args.to}
cached = json.loads(cache.read_text(encoding='utf-8')) if cache.exists() else {}
if {k: cached.get(k) for k in key} == key:
    words = cached['words']
else:
    segs, _ = model.transcribe(audio, language='vi', word_timestamps=True, beam_size=5, vad_filter=True,
                               condition_on_previous_text=False)
    words = []
    for s in segs:
        print(f'{s.start:7.2f} {s.text.strip()}', flush=True)
        words += [{'w': w.word.strip(), 's': round(w.start, 3), 'e': round(w.end, 3)} for w in s.words]
    cache.write_text(json.dumps({**key, 'words': words}, ensure_ascii=False), encoding='utf-8')


def dist(u, t):
    return 0 if u['start'] <= t <= u['end'] else min(abs(t-u['start']), abs(t-u['end']))


orphans = []
for w in words:
    mid = (w['s']+w['e'])/2
    u = min(utts, key=lambda u: dist(u, mid))
    (u['words'] if dist(u, mid) < 1.0 else orphans).append(w)

HALLU = re.compile(r'subscribe|ghiền mì gõ|cảm ơn các bạn đã (theo dõi|xem)', re.I)
for u in utts:
    dur = u['end']-u['start']
    if u['words'] or dur < 0.3:
        continue
    a, b = max(0, int((u['start']-0.2)*SR)), int((u['end']+0.2)*SR)
    ws = [w for s in model.transcribe(audio[a:b], language='vi', word_timestamps=True, beam_size=5, temperature=0, vad_filter=False,
                                      condition_on_previous_text=False)[0] for w in s.words]
    text = ' '.join(w.word.strip() for w in ws)
    if ws and len(ws)/dur < 6 and not HALLU.search(text):
        u['words'] = [{'w': w.word.strip(), 's': round(w.start+a/SR, 3), 'e': round(w.end+a/SR, 3)} for w in ws]
        u['retry'] = True

def quietest(a, b):
    i0 = min(max(0, int(a*100)), len(rms)-1)
    return (i0+int(np.argmin(rms[i0:max(i0+1, int(b*100))])))/100 + 0.005


def cut_out_marker(utts, ms, me, flag='marker'):
    hit = [u for u in utts if u['end'] > ms and u['start'] < me]
    if not hit:
        return utts
    a0, b0 = min(u['start'] for u in hit), max(u['end'] for u in hit)
    ms = a0 if ms-a0 < 0.15 else ms
    me = b0 if b0-me < 0.15 else me
    ws = [w for u in hit for w in u['words']]
    part = lambda a, b, **k: {'start': round(a, 3), 'end': round(b, 3), **k,
                              'words': [w for w in ws if a <= (w['s']+w['e'])/2 < b]}
    new = [part(ms, me, **{flag: True})] + ([part(a0, ms)] if ms > a0 else []) + ([part(me, b0)] if me < b0 else [])
    return sorted([u for u in utts if u not in hit]+new, key=lambda u: u['start'])


flat = sorted((w for u in utts for w in u['words']), key=lambda w: w['s'])
for i0, i1 in find_markers(flat):
    utts = cut_out_marker(utts, quietest(flat[i0]['s']-0.25, flat[i0]['s']+0.05), quietest(flat[i1]['e']-0.05, flat[i1]['e']+0.25))
# "Hey Claude, <edit request>": split it off from the start of the wake word to the end of its utterance
flat = sorted((w for u in utts for w in u['words']), key=lambda w: w['s'])
for i0 in find_edit_requests(flat):
    s0 = flat[i0]['s']
    host = next((u for u in utts if u['start'] - .05 <= s0 <= u['end']), None)
    if host:
        utts = cut_out_marker(utts, quietest(s0-0.25, s0+0.05), host['end'], flag='edit')
# Short form the speaker also uses: an utterance that is only "cắt" / "cắt cắt" / "cut" / "cái cut" (REA, 16/10/2026)
for u in utts:
    t = [fold(w['w']) for w in u['words']]
    if t and len(t) <= 3 and set(t) <= {'cat', 'cut', 'cai'} and set(t) & {'cat', 'cut'}:
        u['marker'] = True
for i, u in enumerate(utts):
    u['id'] = f'U{i+1:03}'

RULES = '''# LUẬT CẮT (đọc hết file trước khi quyết định, bản nói lại có thể nằm sau 1 khoảng lặng dài)
# Chữ do Whisper nhận dạng, có lỗi nghe nhầm. Phán đoán theo nghĩa và âm gần giống. Pause/im lặng script tự rút, không cần bỏ vì im lặng.
# 0. Dòng [LỆNH CẮT] = người nói ra lệnh cắt bản vừa nói hỏng (vd "Hey Ryan, cắt đoạn này"), rồi nói lại ngay sau đó.
#    Bỏ dòng lệnh. Quay ngược: xem câu ngay sau lệnh mở đầu bằng gì, tìm lần nói trước đó của câu đó (trước lệnh),
#    bỏ từ đó tới hết lệnh. Không tìm được câu khớp thì bỏ ngược về đầu câu đang nói dở (thường sau khoảng lặng dài gần nhất).
#    Thấy 1 câu giống lệnh cắt mà không có tag (Whisper nghe sai tên) thì xử y như lệnh.
# 1. Câu được nói lại (cùng ý, cùng cách mở đầu): giữ bản CUỐI CÙNG nói trọn, bỏ các bản trước và mọi đoạn ở giữa thuộc bản hỏng.
# 2. Câu bỏ dở rồi nói lại từ đầu: bỏ câu dở.
# 3. Lặp ngay trong 1 đoạn ("thì đầu tiên thì đầu tiên mình muốn..."): dùng trim bỏ bản đầu.
# 4. Tiếng đệm đứng riêng thành 1 đoạn (ờ, à, ừm, ê, vâng...): bỏ. Giữ "thì", "rồi", "ha", "này" khi nằm trong câu.
#    "này" đứng riêng 1 đoạn ngay sau 1 câu đã trọn: bỏ. "thì", "và", "rồi", "thì bạn" đứng riêng 1 đoạn giữa 2 câu: bỏ.
#    Nửa từ/nửa cụm bị ngắt ngay trước bản nói trọn (vd "Vậy bây" rồi "Vậy bây giờ bạn...", "phân tích cái đó" rồi nói lại cả câu): bỏ.
# 5. [không rõ] ngắn hơn 0.6s: bỏ (thường là tiếng ậm ừ). [không rõ] nằm sát 1 chỗ nói lại: bỏ. Dài hơn và đứng riêng: giữ.
# 6. Không bỏ nội dung chỉ vì thấy thừa hay dài dòng. Chỉ bỏ vấp. Không chắc thì giữ.
# 7. Câu dặn editor (gọi "ghi chú editor", "editor", "che lại...", "giúp tôi...", "cắt cái đoạn ... đi", "hết video"): bỏ khỏi video và chép yêu cầu vào "notes".
#    "Cắt (ở) đoạn X đi" nói ở cuối video = kết thúc video ngay sau X: GIỮ X, bỏ mọi thứ sau X.
# 8. Dòng [LỆNH EDIT] = người nói ra lệnh cho Claude edit ("Hey Claude, chèn ảnh chụp trang này", "quay màn hình đoạn này",
#    "thêm B-roll ... vào đây"). Bỏ dòng lệnh và các câu ngay sau còn thuộc lệnh đó (đọc theo nghĩa, lệnh hay kéo sang 1-2 dòng).
#    Chép vào notes với "kind": "edit", "at" = giờ raw bắt đầu lệnh, "ask" = yêu cầu đầy đủ, "for" = câu nội dung mà B-roll
#    phải minh hoạ (thường là câu ngay trước hoặc ngay sau lệnh). Thấy câu giống lệnh này mà không có tag thì xử y vậy.
# OUTPUT work/cuts.json:
#   {"drop": [{"ids": ["U040", "U041"], "why": "bản hỏng, nói lại ở U043"}],
#    "trim": [{"id": "U023", "text": "thì đầu tiên", "why": "lặp đầu câu"}],
#    "notes": [{"ids": ["U246"], "at": 789.8, "ask": "che mờ thông tin khách hàng trên bảng CRM đang hiện"},
#              {"ids": ["U300"], "at": 912.4, "kind": "edit", "ask": "chèn ảnh chụp trang GitHub repo", "for": "U299"}]}
#   drop.ids: bỏ nguyên đoạn, gom ID liền nhau cùng lý do. trim.text: các từ LIỀN NHAU chép y nguyên từ đoạn đó.
'''
lines = RULES.splitlines() + [
    '',
    '# Mỗi dòng: ID  start-end  (+im lặng trước đó)  chữ. Đoạn có tiếng nói, tách tại chỗ ngắt >= 0.2s. Giờ theo file raw (giây).',
    '# [không rõ Xs] = có tiếng nhưng Whisper không ra chữ. "~" = chữ từ lần nghe lại riêng đoạn đó, độ tin thấp hơn.', '']
prev = 0.0
for u in utts:
    gap = u['start']-prev
    if gap >= 3:
        lines.append(f'      ---- im lặng {gap:.1f}s ----')
    u['text'] = ' '.join(w['w'] for w in u['words'])
    shown = u['text'] or f"[không rõ {u['end']-u['start']:.1f}s]"
    tag = '[LỆNH CẮT] ' if u.get('marker') else '[LỆNH EDIT] ' if u.get('edit') else '~' if u.get('retry') else ''
    lines.append(f"{u['id']}  {u['start']:7.2f}-{u['end']:7.2f}  (+{gap:4.2f})  {tag}{shown}")
    prev = u['end']
(WK/'utterances.txt').write_text('\n'.join(lines), encoding='utf-8')
(WK/'utterances.json').write_text(json.dumps({'source': args.src, 'to': args.to, 'utterances': utts, 'orphans': orphans},
                                             ensure_ascii=False, indent=1), encoding='utf-8')
empty = sum(1 for u in utts if not u['text'])
marks = [u['id'] for u in utts if u.get('marker')]
edits = [u['id'] for u in utts if u.get('edit')]
print(f'{len(utts)} utterances, {empty} without text, {len(orphans)} orphan words, cut commands: {marks or "none"}, '
      f'edit requests: {edits or "none"} -> work/utterances.txt')
