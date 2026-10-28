# Example (2026-10-13, approved by the user): writes the edit-plan.json of projects/broll-lab-ai-edit, 10 sl-* slides fed with
# REAL material from the showroom 3D projects: raw + final video frames, utterances.json + cuts.json of the cut pass, the
# basic edit-plan, a rendered overlay with alpha pulled from cache/*.mkv, the review gallery, render logs, chapters.txt.
# Copy the pattern (where each prop comes from), not the paths. Output of this script: slides-example.json.
import json, subprocess
from pathlib import Path

PROJ = Path(r'C:/work/youtube/projects')
LAB = PROJ/'broll-lab-ai-edit'
YT = 'C:/work/youtube/videos/2026/showroom 3d'
RAW, SRC = f'{YT}/showroom 3d.mp4', f'{YT}/Final 3D.mp4'
ED = str(PROJ/'showroom-3d-basic'/'renders'/'final.mp4')
BF, AF = PROJ/'showroom-3d-basic'/'review'/'frames', PROJ/'showroom-3d-advanced'/'review'/'frames'
REAL = LAB/'assets'/'real'; REAL.mkdir(parents=True, exist_ok=True)


def ff(*a):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *map(str, a)], check=True)


# rendered keyword overlay with alpha (cache of the basic render) + the creator's face for the YouTube avatar
layer = REAL/'ov-020-keyword-alpha.png'
ff('-i', PROJ/'showroom-3d-basic'/'cache'/'ov-020.02a21b36da.mkv', '-vf', 'select=eq(n\\,18)', '-frames:v', 1, '-pix_fmt', 'rgba', layer)
avatar = REAL/'avatar.jpg'
ff('-ss', 30, '-i', SRC, '-frames:v', 1, '-vf', 'crop=164:164:96:858,scale=240:240', '-q:v', 2, avatar)

U = json.loads((PROJ/'showroom-3d-cut'/'work'/'utterances.json').read_text(encoding='utf-8'))['utterances']
ix = {u['id']: i for i, u in enumerate(U)}
a, b = 37.0, 55.0
words = [[u['start'], u['end'], u['text']] for u in U if u['end'] > a and u['start'] < b and not u['text'].startswith('[')]
lines = []
for uid in [f'U{k:03d}' for k in range(12, 26)]:
    i = ix[uid]; u = U[i]; prev = U[i-1]['end'] if i else 0
    lines.append([uid, u['start'], u['end'], round(u['start'] - prev, 2), u['text']])

ov = []
add = lambda t, d, props: ov.append({'type': t, 'at': float(sum(x['dur'] for x in ov)), 'dur': d, 'props': props, 'say': t})
add('sl-system', 6, {'title': 'Edit YouTube bằng *AI*', 'steps': [
    {'label': 'AI cut', 'icon': 'scissors', 'img': str(REAL/'sl-cut-timeline.jpg')},
    {'label': 'Tạo components', 'icon': 'layers', 'img': str(BF/'ov-006-hero.jpg')},
    {'label': 'AI edit', 'icon': 'wand', 'img': str(BF/'ov-017-hero.jpg')},
    {'label': 'Render', 'icon': 'play', 'img': f'{ED}@600.0', 'progress': True}]})
add('sl-cut', 5, {'title': '*AI cut*', 'file': RAW, 'a': a, 'b': b, 'clip_name': 'showroom 3d.mp4', 'words': words,
                  'cuts': [[39.733, 42.3, 'câu dở'], [50.0, 50.4, 'lặng'], [53.967, 54.4, 'lặng']],
                  'caption': 'bỏ câu dở, khoảng lặng'})
add('sl-transcript', 5, {'title': 'AI đọc *transcript*', 'file': 'utterances.txt', 'crumb': 'work', 'project': 'showroom-3d-cut',
                         'lines': lines, 'first_line': 32, 'strike': ['U017', 'U018'],
                         'reason': 'U017, U018: mở đầu dở *“Thì đầu tiên”*, nói lại trọn ở U019. Bỏ 2 dòng.'})
add('sl-stack', 5, {'title': 'Tạo *components*', 'base': f'{SRC}@670.01', 'layer': str(layer), 'file': 'ov-020.html', 'code': [
    '<div class="kw card" id="k">',
    '  Đổi <em class="acc">6 màu sơn</em> ngay trên web',
    '</div>',
    '<script>',
    "tl.fromTo('#k', {opacity:0, y:18, scale:.97},",
    "  {opacity:1, y:0, scale:1, duration:.34}, 0);",
    "tl.to('#k', {opacity:0, duration:.24}, D-.24);",
    '</script>']})
add('sl-fan', 5, {'title': 'Thư viện *components*', 'cards': [
    {'img': str(BF/'ov-006-hero.jpg'), 'label': 'chapter'}, {'img': str(AF/'ov-003-hero.jpg'), 'label': '3D'},
    {'img': str(AF/'ov-002-hero.jpg'), 'label': 'so sánh'}, {'img': str(AF/'ov-036-hero.jpg'), 'label': 'flow'},
    {'img': str(BF/'ov-001-hero.jpg'), 'label': 'b-roll'}]})
J = [['{', -1], ['  "overlays": [', -1],
     ['    {"type": "chapter", "at": 33.72,', -1], ['     "props": {"title": "Bản vẽ thành *3D*"}},', 0],
     ['    {"type": "keyword", "at": 193.8,', -1], ['     "props": {"text": "Toilet chỉ là *khối hộp*"}},', 1],
     ['    {"type": "lower-third", "at": 225.0,', -1], ['     "props": {"name": "Opus 5.5"}},', 2],
     ['    {"type": "keyword", "at": 669.41,', -1], ['     "props": {"text": "Đổi *6 màu sơn*…"}}', 3],
     ['  ]', -1], ['}', -1]]
add('sl-edit', 5, {'title': '*AI edit*',  'file': 'edit-plan.json', 'project': 'showroom-3d-basic', 'json': J, 'duration': 719.5,
                   'base': f'{SRC}@33.0', 'wave_file': str(PROJ/'showroom-3d-basic'/'assets'/'speech.wav'),
                   'strip': [f'{SRC}@{t}.0' for t in (30, 120, 210, 300, 390, 480, 570, 660)],
                   'blocks': [{'label': 'chapter', 'at': 33.72, 'img': str(BF/'ov-006-hero.jpg'), 'color': '#7B6CFF'},
                              {'label': 'keyword', 'at': 193.8, 'img': str(BF/'ov-011-hero.jpg'), 'color': '#E07A5F'},
                              {'label': 'lower-third', 'at': 225.0, 'img': str(BF/'ov-012-hero.jpg'), 'color': '#3B82F6'},
                              {'label': 'keyword', 'at': 669.41, 'img': str(BF/'ov-020-hero.jpg'), 'color': '#E07A5F'}]})
add('sl-terminal', 5, {'title': 'Claude Code *tự edit*', 'cwd': 'D:\\…\\projects\\showroom-3d-basic', 'prompt': 'edit video này theo style chuẩn',
                       'thinking': 'Đang đọc transcript…', 'steps': [
                           ['tool', 'Read(assets/transcript.txt)', 'Read 194 lines'],
                           ['tool', 'Write(edit-plan.json)', 'Wrote 20 overlays'],
                           ['tool', 'Bash(python scripts/build.py)', '20 overlays, 28 SFX cues -> overlays.json'],
                           ['tool', 'Bash(python scripts/preview.py)', '20 ảnh mẫu -> review/index.html'],
                           ['say', 'Xong ảnh mẫu. Mở *review/index.html* để duyệt.', '']]})
add('sl-approve', 5, {'title': 'Duyệt *ảnh mẫu* trước', 'page': str(PROJ/'showroom-3d-advanced'/'review'/'index.html'),
                      'url': 'D:/…/showroom-3d-advanced/review/index.html', 'tab': 'Duyệt mẫu Showroom 3D',
                      'reply': 'duyệt', 'done': 'Đã duyệt. Bắt đầu render video.'})
add('sl-render', 5, {'title': '*Render*', 'name': 'final.mp4', 'clip': [ED, 596.0],
                     'frames': [f'{ED}@{t}' for t in (6.0, 36.0, 136.5, 200.0, 249.0, 400.0, 583.0, 640.0)],
                     'log': [['cmd', 'python scripts/render_overlays.py'], ['out', '[1/18] ov-003  191 frames  111s'],
                             ['out', '[4/18] ov-006   96 frames   71s'], ['out', '[9/18] ov-011   30 frames   14s'],
                             ['out', '[18/18] ov-020  30 frames   14s'], ['cmd', 'python scripts/composite.py'],
                             ['bar', 'frame=21586 speed=2.43x'], ['ok', 'renders/final.mp4 · 1920×1080 · 11:59']]})
add('sl-publish', 5, {'title': 'Lên *YouTube*', 'clip': [ED, 34.0], 'time': '0:34 / 11:59', 'now': 1, 'progress': 0.047, 'search': 'Tìm kiếm',
                      'video_title': 'Tạo showroom 3D giống thật bằng AI', 'channel': 'Thành Vũ Đức', 'subs': '',
                      'avatar': str(avatar), 'url': 'youtube.com/watch?v=…',
                      'chapters': [['0:00', 'Intro', f'{ED}@1.5'], ['0:33', 'Bản vẽ thành 3D', f'{ED}@35.0'],
                                   ['2:15', 'Ảnh thành 3D', f'{ED}@137.0'], ['4:07', 'Căn hộ từ ảnh + bản vẽ', f'{ED}@249.0'],
                                   ['9:41', 'Showroom 3D', f'{ED}@583.0']]})

plan = {'style': 'basic', 'layout': {}, 'sections': [], 'zooms': [], 'overlays': ov}
(LAB/'edit-plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(ov), 'slides', sum(x['dur'] for x in ov), 's; words', len(words), 'lines', len(lines))
