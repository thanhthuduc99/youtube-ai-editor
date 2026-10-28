# Moves edit-plan.json times after the cut changed (render_cut.py keeps the previous cut as work/keep.prev.json), or
# from raw-video times onto the cut video (--from-raw). Overlay "at", section "start" and zoom "at" go cut(old) -> raw ->
# cut(new); durations follow the speed change. A moment whose speech was cut snaps to the next kept moment and is
# reported, so the overlay can be deleted or re-placed.
# Usage: python cut/scripts/shift_plan.py            (keep.prev.json -> keep.json)
#        python cut/scripts/shift_plan.py --from-raw (plan written on the raw video's timeline)
import argparse, json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
P = R.parent
ap = argparse.ArgumentParser()
ap.add_argument('--from-raw', action='store_true')
args = ap.parse_args()
new = json.loads((R/'work'/'keep.json').read_text(encoding='utf-8'))
old = None if args.from_raw else json.loads((R/'work'/'keep.prev.json').read_text(encoding='utf-8'))


def to_raw(t):
    if old is None:
        return t
    sp = old['speed']
    for r in old['segments']:
        if r['out_start'] <= t < r['out_start'] + (r['raw_end'] - r['raw_start'])/sp + 1e-6:
            return r['raw_start'] + (t - r['out_start'])*sp
    return old['segments'][-1]['raw_end']


def to_new(t):
    sp = new['speed']
    for r in new['segments']:
        if r['raw_start'] <= t < r['raw_end']:
            return r['out_start'] + (t - r['raw_start'])/sp, False
    nxt = next((r for r in new['segments'] if r['raw_start'] >= t), new['segments'][-1])
    return nxt['out_start'], nxt['raw_start'] - t > 0.6  # a shortened pause is not worth reporting, lost speech is


plan_f = P/'edit-plan.json'
plan = json.loads(plan_f.read_text(encoding='utf-8'))
scale = (old['speed'] if old else 1.0)/new['speed']  # durations were measured on the old timeline
for o in plan.get('overlays', []) + plan.get('zooms', []):
    if 'dur' in o:
        o['dur'] = round(o['dur']*scale, 2)
moved = []
for kind, items, key in (('overlay', plan.get('overlays', []), 'at'), ('section', plan.get('sections', []), 'start'),
                         ('zoom', plan.get('zooms', []), 'at')):
    for k, it in enumerate(items):
        t, lost = to_new(to_raw(it[key]))
        if lost:
            moved.append(f"{kind} #{k+1} {it.get('type', it.get('title', ''))}: speech at {it[key]:.2f}s was cut, moved to {t:.2f}s")
        it[key] = round(t, 3)
plan_f.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding='utf-8')
print(f"edit-plan.json re-timed ({'raw' if old is None else 'previous cut'} -> current cut), durations x{scale:.3f}")
print('\n'.join(moved) + '\n-> delete or re-place these, then build.py reports any overlap' if moved else 'every moment still exists')
