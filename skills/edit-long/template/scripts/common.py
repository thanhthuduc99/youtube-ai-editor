# Shared project settings for every script: project root, project.json, frame helpers, HyperFrames command.
from pathlib import Path
import json, os, subprocess, sys

R = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding='utf-8')
P = json.loads((R/'project.json').read_text(encoding='utf-8'))
FPS = 30
W, H = 1920, 1080
HF = ['npx.cmd' if os.name == 'nt' else 'npx', '--yes', 'hyperframes@0.8.143']
CACHE = R/'cache'
SKILL = Path.home()/'.claude'/'skills'/'edit-long'


def frame(t):
    return int(round(t*FPS))


def snap(t):
    return frame(t)/FPS


def video():
    """Video used for frames and compositing: the prepared mezzanine if prepare.py made one, else the original."""
    return Path(P.get('video') or P['source'])


def probe_duration(path):
    out = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', str(path)])
    return float(json.loads(out)['format']['duration'])


def ff(*args):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *map(str, args)], check=True)


def sfx_dir():
    for cand in [P.get('sfx_dir'), str(Path.home()/'.claude'/'skills'/'media-use'/'audio'/'assets'/'sfx')]:
        if cand and Path(cand).is_dir():
            return Path(cand)
    return None


def load_json(name):
    return json.loads((R/name).read_text(encoding='utf-8'))


def save_json(name, data):
    (R/name).parent.mkdir(parents=True, exist_ok=True)
    (R/name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def save_project():
    save_json('project.json', P)
