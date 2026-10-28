# Smooths the jump cuts left by the cut pass (work/jumps.json), the user's rule:
#   - a B-roll that hides the face already sits on the cut -> nothing to add, the face -> B-roll switch gets the click
#     (plan "switch_sfx", added by build.py at the start of every overlay that replaces the face);
#   - face -> face -> only listed. User 21/10/2026: no film burn on every cut ("nhìn kì"); burn only the few cuts that
#     really need it, chosen with the user (--at), or all of them with --burn (old behaviour).
# Re-run after every plan change: it replaces the transitions it added before.
# Usage: python cut/scripts/jump_fx.py [--at 57.5,120.3] [--burn] [--kind filmburn-01]
import argparse, json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
P = R.parent
ap = argparse.ArgumentParser()
ap.add_argument('--kind', default='filmburn-01')
ap.add_argument('--burn', action='store_true', help='film burn on every uncovered face -> face cut')
ap.add_argument('--at', default='', help='comma list of jump times (s) that get a film burn')
args = ap.parse_args()
picked = [float(x) for x in args.at.split(',') if x.strip()]
FACE_STAYS = {'th-text', 'th-chips', 'th-lower', 'th-side', 'th-column', 'keyword', 'lower-third', 'chips', 'banner', 'section-chip'}
jumps = json.loads((R/'work'/'jumps.json').read_text(encoding='utf-8'))
plan_f = P/'edit-plan.json'
plan = json.loads(plan_f.read_text(encoding='utf-8'))
plan.setdefault('switch_sfx', {'name': 'mouse-click', 'gain': 0})
tr = [t for t in plan.get('transitions', []) if not t.get('auto')]
for j in jumps:
    cover = next((o for o in plan['overlays'] if o['type'] not in FACE_STAYS and o['at'] - .4 <= j['at'] <= o['at'] + o['dur']), None)
    if cover:
        print(f"{j['at']:7.2f}s  covered by {cover['type']} at {cover['at']:.2f}s -> click on the switch")
        continue
    if not (args.burn or any(abs(j['at'] - t) < .3 for t in picked)):
        print(f"{j['at']:7.2f}s  face -> face, {j['removed']:.1f}s removed -> left as is (burn candidate)")
        continue
    tr.append({'at': j['at'], 'kind': args.kind, 'auto': True, 'say': f"jump cut, {j['removed']:.1f}s removed"})
    near = [o for o in plan['overlays'] if 0 <= o['at'] - j['at'] < 1.0]
    print(f"{j['at']:7.2f}s  face -> face -> {args.kind}" + (f"  (move {near[0]['type']} at {near[0]['at']:.2f}s to >= {j['at']+.9:.2f}s)" if near else ''))
plan['transitions'] = sorted(tr, key=lambda t: t['at'])
plan_f.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding='utf-8')
print(f"{len(plan['transitions'])} transitions, switch sound: {plan['switch_sfx']['name']}")
