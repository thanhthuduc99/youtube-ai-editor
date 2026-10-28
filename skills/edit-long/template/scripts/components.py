# Overlay component library (light luxe). Each builder returns a dict:
#   html, css, js (GSAP on `tl`, uses D = render duration), enter (s, entrance settled), exit (s, length of exit),
#   hero (s, frame shown for approval), sfx [(t, name, gain_db)], full (opaque full frame), holdable (may loop the
#   settled frame for long durations), module (optional ES module for Three.js).
# Text overlays default to pos 'bottom' (centred above the bottom UI bar). Text: "*word*" marks the accent word (plum). Times inside a component are relative to the overlay start.
import html as _h
import json
import re

TOKENS = """
:root{--ivory:#FAF6EF;--ivory2:#F3ECE0;--paper:#FFFFFF;--ink:#17130D;--soft:#4A4339;--muted:#8A8073;
--line:rgba(23,19,13,.09);--plum:#4A3AE0;--plum2:#7B6CFF;--lav:#B7A8FF;--peach:#FFB39C;--sky:#9AD0FF;--sage:#A9E0C2;--gold:#E6B45A}
@font-face{font-family:Display;src:url('../assets/fonts/display.ttf')}
@font-face{font-family:Body;src:url('../assets/fonts/body.ttf')}
@font-face{font-family:BodyBold;src:url('../assets/fonts/body-bold.ttf')}
@font-face{font-family:Mono;src:url('../assets/fonts/mono.ttf')}
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;background:transparent;overflow:hidden}
#root{position:relative;width:100%;height:100%;overflow:hidden;font-family:Body;color:var(--ink)}
.layer{position:absolute;inset:0}
.d{font-family:Display;font-weight:800;letter-spacing:-.02em;line-height:1.1}
.bb{font-family:BodyBold}
em.acc{font-style:normal;color:var(--plum)}
.card{background:rgba(255,255,255,.97);border:1px solid var(--line);border-radius:26px;
 box-shadow:0 34px 70px -26px rgba(23,19,13,.42),0 4px 14px rgba(23,19,13,.08)}
.pos{position:absolute;inset:0;display:flex;padding:110px}
.pos-right{align-items:center;justify-content:flex-end}
.pos-left{align-items:center;justify-content:flex-start;padding-left:120px}
.pos-center{align-items:center;justify-content:center}
.pos-top{align-items:flex-start;justify-content:center;padding-top:104px}
.pos-top-right{align-items:flex-start;justify-content:flex-end;padding-top:112px;padding-right:72px}
.pos-top-left{align-items:flex-start;justify-content:flex-start;padding-top:112px;padding-left:72px}
.pos-bottom-right{align-items:flex-end;justify-content:flex-end;padding-bottom:116px;padding-right:72px}
.pos-bottom{align-items:flex-end;justify-content:center;padding-bottom:170px}
.tile{width:84px;height:84px;border-radius:22px;background:var(--ivory);border:1px solid var(--line);display:grid;place-items:center;flex:none}
.tile svg{width:46px;height:46px;fill:var(--ink)}
.tile .letter{font-family:Display;font-size:40px;color:var(--plum)}
.num{width:44px;height:44px;border-radius:50%;background:var(--plum);color:#fff;display:grid;place-items:center;font-family:BodyBold;font-size:24px;flex:none}
.canvas{position:absolute;inset:0;background:
 radial-gradient(900px 640px at 16% 18%,rgba(183,168,255,.55),transparent 62%),
 radial-gradient(860px 620px at 86% 84%,rgba(154,208,255,.50),transparent 62%),
 radial-gradient(600px 400px at 70% 10%,rgba(255,179,156,.22),transparent 60%),var(--ivory)}
.canvas::after{content:'';position:absolute;inset:0;background-image:radial-gradient(rgba(23,19,13,.07) 1.3px,transparent 1.4px);background-size:30px 30px}
.stage{position:absolute;inset:0}
.ftitle{position:absolute;left:0;right:0;top:92px;text-align:center;font-size:58px}
.fsub{position:absolute;left:0;right:0;top:172px;text-align:center;font-size:28px;color:var(--soft)}
.glass{background:rgba(255,255,255,.78);border:1px solid rgba(255,255,255,.95);border-radius:30px;
 box-shadow:0 30px 60px -30px rgba(40,30,120,.35),inset 0 1px 0 rgba(255,255,255,.9)}
"""


def esc(s):
    return _h.escape(str(s), quote=True)


def rich(s):
    return re.sub(r'\*(.+?)\*', r'<em class="acc">\1</em>', esc(s))


def tile(ctx, logo, name=''):
    svg = ctx['logo'](logo) if logo else None
    inner = svg or f'<span class="letter">{esc((name or logo or "?")[:1].upper())}</span>'
    return f'<div class="tile">{inner}</div>'


def _exit_fade(sel, X=.24):
    return f"tl.to('{sel}',{{opacity:0,duration:{X},ease:'power2.in'}},D-{X});"


# ---------------------------------------------------------------- basic: corner / inline overlays

def keyword(o, ctx):
    p = o['props']; pos = p.get('pos', 'bottom')
    logo = tile(ctx, p['logo'], p.get('text')) if p.get('logo') else ''
    sub = f'<div class="kws">{rich(p["sub"])}</div>' if p.get('sub') else ''
    html = f'<div class="pos pos-{pos}"><div class="kw card" id="k">{logo}<div><div class="d kwt">{rich(p["text"])}</div>{sub}</div></div></div>'
    n = len(re.sub(r'\*', '', p['text']))
    size = p.get('size') or (62 if n <= 22 else 54 if n <= 28 else 46)
    css = '.kw{display:flex;align-items:center;gap:22px;padding:24px 36px;max-width:1000px}.kwt{font-size:%dpx;white-space:nowrap}.kws{font-size:27px;color:var(--soft);margin-top:8px}' % size
    js = ("tl.fromTo('#k',{opacity:0,y:18,scale:.97},{opacity:1,y:0,scale:1,duration:.34,ease:'power3.out'},0);"
          + ("tl.fromTo('#k .tile',{opacity:0,scale:.6},{opacity:1,scale:1,duration:.42,ease:'back.out(1.7)'},.08);" if logo else '')
          + _exit_fade('#k'))
    return dict(html=html, css=css, js=js, enter=.5, exit=.24, hero=.7, sfx=[(0, 'pop', -19)], holdable=True)


def lower(o, ctx):
    p = o['props']; pos = p.get('pos', 'bottom')
    html = (f'<div class="pos pos-{pos}"><div class="lt card" id="lt">{tile(ctx, p.get("logo"), p["name"])}'
            f'<div><div class="d ltn">{rich(p["name"])}</div><div class="ltd">{rich(p.get("desc", ""))}</div></div></div></div>')
    css = '.lt{display:flex;align-items:center;gap:20px;padding:18px 32px 18px 18px}.ltn{font-size:40px}.ltd{font-size:24px;color:var(--soft);margin-top:4px}'
    js = ("tl.fromTo('#lt',{opacity:0,x:34},{opacity:1,x:0,duration:.4,ease:'power3.out'},0);"
          "tl.fromTo('#lt .tile',{opacity:0,scale:.6},{opacity:1,scale:1,duration:.4,ease:'back.out(1.7)'},.1);" + _exit_fade('#lt'))
    return dict(html=html, css=css, js=js, enter=.55, exit=.24, hero=.8, sfx=[(0, 'pop', -19)], holdable=True)


def chips(o, ctx):
    p = o['props']; items = p['items']; pos = p.get('pos', 'bottom')
    times = p.get('times') or [.1 + i*.38 for i in range(len(items))]
    cs = ''.join(f'<div class="chip card" id="c{i}"><span class="num">{i+1}</span><span>{rich(t)}</span></div>' for i, t in enumerate(items))
    css = ('.chips{position:absolute;left:0;right:0;display:flex;justify-content:center;gap:18px;flex-wrap:wrap;padding:0 140px}'
           '.chips-top{top:118px}.chips-bottom{bottom:170px;padding:0 380px}.chips-center{top:50%;transform:translateY(-50%)}'
           '.chip{display:flex;align-items:center;gap:14px;padding:14px 28px 14px 14px;border-radius:999px;font-family:BodyBold;font-size:32px}')
    js = ''.join(f"tl.fromTo('#c{i}',{{opacity:0,y:16,scale:.95}},{{opacity:1,y:0,scale:1,duration:.32,ease:'power3.out'}},{t});" for i, t in enumerate(times))
    js += _exit_fade('.chip')
    return dict(html=f'<div class="chips chips-{pos}">{cs}</div>', css=css, js=js, enter=times[-1]+.35, exit=.24,
                hero=times[-1]+.5, sfx=[(t, 'click-soft', -15) for t in times], holdable=True)


def banner(o, ctx):
    p = o['props']; pos = p.get('pos', 'top-right')
    metas = ''.join(f'<span class="meta">{rich(m)}</span>' for m in p.get('meta', []))
    eyebrow = p.get('eyebrow') or f'PHẦN {int(p["n"]):02d}'
    html = (f'<div class="pos pos-{pos}"><div class="ban card" id="b"><div class="bar" id="bbar"></div>'
            f'<div class="eyebrow bb" id="be">{esc(eyebrow)}</div><div class="d bant" id="bt">{rich(p["title"])}</div>'
            f'<div class="metas" id="bm">{metas}</div></div></div>')
    css = ('.ban{width:800px;padding:34px 44px 38px 52px;position:relative;overflow:hidden}'
           '.bar{position:absolute;left:0;top:0;bottom:0;width:12px;background:var(--plum)}'
           '.eyebrow{font-size:22px;letter-spacing:.2em;color:var(--plum)}.bant{font-size:64px;margin:12px 0 22px}'
           '.metas{display:flex;gap:12px;flex-wrap:wrap}.meta{font-family:BodyBold;font-size:24px;padding:10px 20px;border-radius:999px;background:var(--ivory);border:1px solid var(--line)}')
    js = ("tl.fromTo('#b',{opacity:0,x:70},{opacity:1,x:0,duration:.48,ease:'power3.out'},0);"
          "tl.fromTo('#bbar',{scaleY:0,transformOrigin:'50% 0%'},{scaleY:1,duration:.45,ease:'power3.out'},.12);"
          "tl.fromTo(['#be','#bt','#bm'],{opacity:0,y:16},{opacity:1,y:0,duration:.36,stagger:.09,ease:'power3.out'},.16);"
          "tl.to('#b',{opacity:0,x:44,duration:.3,ease:'power2.in'},D-.3);")
    return dict(html=html, css=css, js=js, enter=.75, exit=.3, hero=1.2, sfx=[(-.05, 'whoosh-short', -17), (.3, 'pop', -20)], holdable=True)


def chapter(o, ctx):
    """Full-frame section opener: big number, title, fact chips, progress through the video's parts."""
    p = o['props']; n = int(p['n']); total = int(p.get('total', n))
    metas = ''.join(f'<span class="meta">{rich(m)}</span>' for m in p.get('meta', []))
    parts = p.get('parts') or [''] * total
    prog = ''.join(f'<div class="seg{" done" if i < n-1 else (" cur" if i == n-1 else "")}"><i></i><span>{rich(t)}</span></div>' for i, t in enumerate(parts))
    pic = f'<div class="chimg glass" id="chi"><img src="{ctx["img"](p["img"])}"></div>' if p.get('img') else ''
    plain = re.sub(r'\*', '', p['title'])
    size = (84 if len(plain) <= 14 else 70) if pic else (98 if len(plain) <= 18 else 82)
    html = (f'<div class="canvas" id="cv"></div><div class="stage" id="st"><div class="chw{" withimg" if pic else ""}">'
            f'<div class="d chn" id="chn">{n:02d}</div><div class="chr"><div class="eyebrow bb" id="che">PHẦN {n} / {total}</div>'
            f'<div class="d cht" id="cht">{rich(p["title"])}</div><div class="metas" id="chm">{metas}</div></div></div>'
            f'{pic}<div class="prog" id="prog">{prog}</div></div>')
    css = ('.chw{position:absolute;left:150px;right:150px;top:0;bottom:120px;display:flex;align-items:center;gap:70px}'
           '.chw.withimg{right:800px;gap:48px}.withimg .chn{font-size:250px}'
           '.chimg{position:absolute;left:1180px;top:250px;width:600px;height:420px;padding:12px;border-radius:30px}'
           '.chimg img{width:100%;height:100%;object-fit:cover;border-radius:20px;display:block}'
           '.chn{font-size:330px;line-height:.85;color:var(--plum);letter-spacing:-.05em}'
           f'.eyebrow{{font-size:24px;letter-spacing:.22em;color:var(--plum)}}.cht{{font-size:{size}px;margin:14px 0 30px;max-width:1000px}}'
           '.metas{display:flex;gap:14px;flex-wrap:wrap}.meta{font-family:BodyBold;font-size:28px;padding:12px 24px;border-radius:999px;background:#fff;border:1px solid var(--line);box-shadow:0 10px 24px -16px rgba(23,19,13,.4)}'
           '.prog{position:absolute;left:150px;right:150px;bottom:110px;display:flex;gap:14px}'
           '.seg{flex:1;display:flex;flex-direction:column;gap:12px}.seg i{display:block;height:8px;border-radius:9px;background:rgba(23,19,13,.1)}'
           '.seg span{font-family:BodyBold;font-size:22px;color:var(--muted)}.seg.done i{background:var(--lav)}.seg.cur i{background:var(--plum)}.seg.cur span{color:var(--ink)}')
    js = _full("tl.fromTo('#chn',{opacity:0,x:-60},{opacity:1,x:0,duration:.5,ease:'power3.out'},.05);"
               "tl.fromTo(['#che','#cht','#chm'],{opacity:0,y:22},{opacity:1,y:0,duration:.42,stagger:.1,ease:'power3.out'},.15);"
               "tl.fromTo('#chm .meta',{opacity:0,scale:.9},{opacity:1,scale:1,duration:.3,stagger:.08,ease:'back.out(1.6)'},.45);"
               "tl.fromTo('#prog .seg',{opacity:0,y:10},{opacity:1,y:0,duration:.3,stagger:.06},.3);"
               "tl.fromTo('#prog .cur i',{scaleX:0,transformOrigin:'0% 50%'},{scaleX:1,duration:.6,ease:'power2.out'},.55);"
               + ("tl.fromTo('#chi',{opacity:0,x:60,rotation:2},{opacity:1,x:0,rotation:0,duration:.6,ease:'power3.out'},.2);" if pic else ''))
    return dict(html=html, css=css, js=js, enter=1.1, exit=0, hero=1.5,
                sfx=[(0, 'whoosh', -16), (.45, 'pop', -19)], full=True)


def section_chip(o, ctx):
    p = o['props']; pos = p.get('pos', 'top-right')
    html = f'<div class="pos pos-{pos}" style="padding-top:88px"><div class="sch" id="sc"><span class="num">{esc(p["n"])}</span><span>{rich(p["title"])}</span></div></div>'
    css = ('.sch{display:flex;align-items:center;gap:12px;padding:9px 24px 9px 9px;border-radius:999px;font-family:BodyBold;font-size:26px;'
           'background:rgba(255,255,255,.93);border:1px solid var(--line);box-shadow:0 12px 30px -12px rgba(23,19,13,.38)}.sch .num{width:38px;height:38px;font-size:20px}')
    js = "tl.fromTo('#sc',{opacity:0,x:30},{opacity:1,x:0,duration:.4,ease:'power3.out'},0);tl.to('#sc',{opacity:0,x:20,duration:.3,ease:'power2.in'},D-.3);"
    return dict(html=html, css=css, js=js, enter=.45, exit=.3, hero=.7, sfx=[(0, 'click-soft', -17)], holdable=True)


# ---------------------------------------------------------------- B-roll (sped-up source clips)

def broll(o, ctx):
    """Full frame: ivory canvas, label left, sped-up clip in a card on the right (Ben AI intro card)."""
    p = o['props']
    eyebrow = f'<div class="beb bb">{rich(p["eyebrow"])}</div>' if p.get('eyebrow') else ''
    sub = f'<div class="bsub">{rich(p["sub"])}</div>' if p.get('sub') else ''
    badge = f'<div class="speed bb" id="spd">tua nhanh ×{o["clip"]["speed"]:g}</div>' if p.get('badge', True) else ''
    html = (f'<div class="canvas"></div><div class="cshadow" id="cs"></div>'
            f'<div class="blab" id="bl">{eyebrow}<div class="d blt">{rich(p["label"])}</div>{sub}</div>{badge}')
    video = f'<div class="vw" id="vw"><video src="{ctx["clip"](o)}" data-start="0" data-duration="{ctx["D"]}" muted playsinline></video></div>'
    css = ('.cshadow,.vw{position:absolute;left:840px;top:262px;width:960px;height:540px;border-radius:24px}'
           '.cshadow{background:#fff;box-shadow:0 44px 90px -30px rgba(23,19,13,.5),0 0 0 10px rgba(255,255,255,.9)}'
           '.vw{overflow:hidden;z-index:2}.vw video{width:100%;height:100%;object-fit:cover;display:block}'
           '.blab{position:absolute;left:120px;top:0;bottom:0;width:640px;display:flex;flex-direction:column;justify-content:center}'
           '.beb{font-size:24px;letter-spacing:.18em;color:var(--plum);margin-bottom:16px}.blt{font-size:78px}.bsub{font-size:30px;color:var(--soft);margin-top:20px;line-height:1.4}'
           '.speed{position:absolute;left:864px;top:826px;padding:8px 18px;border-radius:999px;background:var(--ink);color:#fff;font-size:20px;z-index:3}')
    js = ("tl.fromTo(['#cs','#vw'],{opacity:0,y:44,scale:.94},{opacity:1,y:0,scale:1,duration:.5,ease:'power3.out'},0);"
          "tl.fromTo('#bl > *',{opacity:0,y:22},{opacity:1,y:0,duration:.38,stagger:.08,ease:'power3.out'},.1);"
          + ("tl.fromTo('#spd',{opacity:0},{opacity:1,duration:.3},.4);" if badge else ''))
    return dict(html=html, css=css, js=js, video=video, enter=.6, exit=0, hero=min(1.4, ctx['D']*.6),
                sfx=[(0, 'whoosh-short', -16)], full=True)


def broll_full(o, ctx):
    """Full frame sped-up clip with a small label chip (hard cut in and out)."""
    p = o['props']
    lab = f'<div class="pos pos-top-left"><div class="bfl card bb" id="bf">{rich(p["label"])}</div></div>' if p.get('label') else ''
    video = f'<div class="vf"><video src="{ctx["clip"](o)}" data-start="0" data-duration="{ctx["D"]}" muted playsinline></video></div>'
    css = '.vf{position:absolute;inset:0}.vf video{width:100%;height:100%;object-fit:cover;display:block}.bfl{padding:18px 34px;font-size:44px;border-radius:999px;position:relative;z-index:3}'
    js = "tl.fromTo('#bf',{opacity:0,y:12},{opacity:1,y:0,duration:.32,ease:'power3.out'},.15);" if lab else ''
    return dict(html=lab, css=css, js=js, video=video, video_below=True, enter=.5, exit=0, hero=min(1.2, ctx['D']*.5),
                sfx=[(0, 'whoosh-short', -17)], full=True)


# ---------------------------------------------------------------- advanced: full-frame motion graphics

def _full(js_body):
    """Full-frame cut-ins are opaque from frame 0 to the last frame (hard cut in and out, like both reference
    channels), so render_overlays.py can store them as small H.264 instead of lossless alpha."""
    return js_body


def _titles(p):
    t = f'<div class="d ftitle" id="ft">{rich(p["title"])}</div>' if p.get('title') else ''
    s = f'<div class="fsub" id="fs">{rich(p["sub"])}</div>' if p.get('sub') else ''
    return t + s


TITLES_IN = "tl.fromTo(['#ft','#fs'],{opacity:0,y:18},{opacity:1,y:0,duration:.4,stagger:.08,ease:'power3.out'},.08);"


def _fmt_js(decimals):
    return "v=>{const s=(+v).toFixed(%d);return s.replace('.',',')}" % decimals


def stat(o, ctx):
    p = o['props']; dec = int(p.get('decimals', 0))
    final = json.dumps(f"{float(p['value']):.{dec}f}".replace('.', ','))
    html = (f'<div class="canvas" id="cv"></div><div class="stage" id="st">{_titles(p)}<div class="sbox" id="sb">'
            f'<div class="d sv"><span>{esc(p.get("prefix", ""))}</span><span id="n">0</span><span class="suf">{esc(p.get("suffix", ""))}</span></div>'
            f'<div class="sl bb">{rich(p.get("label", ""))}</div>'
            + (f'<div class="sn">{rich(p["note"])}</div>' if p.get('note') else '') + '</div></div>')
    css = ('.sbox{position:absolute;left:0;right:0;top:0;bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding-top:60px}'
           '.sv{font-size:250px;color:var(--plum);line-height:1;font-variant-numeric:tabular-nums;display:flex;align-items:baseline;gap:10px}'
           '.suf{font-size:120px;color:var(--ink)}.sl{font-size:42px;margin-top:26px}.sn{font-size:28px;color:var(--soft);margin-top:14px}')
    run = float(p.get('count', 1.1))
    js = _full(TITLES_IN +
               "tl.fromTo('#sb',{opacity:0,scale:.92},{opacity:1,scale:1,duration:.45,ease:'power3.out'},.12);"
               f"tl.fromTo('#n',{{innerText:{p.get('from', 0)}}},{{innerText:{p['value']},duration:{run},ease:'power2.out',modifiers:{{innerText:{_fmt_js(dec)}}}}},.2);"
               f"tl.set('#n',{{innerText:{final}}},{.2+run});")
    return dict(html=html, css=css, js=js, enter=.2+run+.1, exit=0, hero=.2+run+.3,
                sfx=[(0, 'whoosh', -17), (.2+run, 'sparkle', -19)], full=True)


def tiles(o, ctx):
    """Tool tiles around an optional center node, joined by lines (Liam tool map)."""
    p = o['props']; items = p['items']; n = len(items)
    import math
    cx, cy = 960, 660
    if p.get('center'):
        angles = [math.pi*(1 - i/(n-1)) for i in range(n)] if n > 1 else [math.pi/2]
        pos = [(cx + 620*math.cos(a), cy - 330*math.sin(a)) for a in angles]
    else:
        gap = min(300, 1500/max(n, 1))
        pos = [(cx - gap*(n-1)/2 + gap*i, 590) for i in range(n)]
    nodes = ''
    for i, (it, (x, y)) in enumerate(zip(items, pos)):
        nodes += (f'<div class="tl2 glass{" hot" if it.get("hot") else ""}" id="t{i}" style="left:{x-112:.0f}px;top:{y-112:.0f}px">'
                  f'{tile(ctx, it.get("logo"), it["name"])}<div class="tn bb">{rich(it["name"])}</div></div>')
    lines = ''
    if p.get('center'):
        c = p['center']
        nodes += (f'<div class="tl2 glass core" id="tc" style="left:{cx-135}px;top:{cy-135}px;width:270px;height:270px">'
                  f'{tile(ctx, c.get("logo"), c["name"])}<div class="tn bb">{rich(c["name"])}</div></div>')
        for i, (x, y) in enumerate(pos):
            lines += f'<line id="l{i}" x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}"/>'
    else:
        for i in range(n-1):
            lines += f'<line id="l{i}" x1="{pos[i][0]+100:.0f}" y1="590" x2="{pos[i+1][0]-100:.0f}" y2="590"/>'
    html = (f'<div class="canvas" id="cv"></div><div class="stage" id="st">{_titles(p)}'
            f'<svg class="lines" viewBox="0 0 1920 1080">{lines}</svg>{nodes}</div>')
    css = ('.lines{position:absolute;inset:0;width:1920px;height:1080px}.lines line{stroke:var(--plum2);stroke-width:3;stroke-dasharray:2 12;stroke-linecap:round;opacity:.8}'
           '.tl2{position:absolute;width:224px;height:224px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px}'
           '.tl2 .tile{background:#fff;width:100px;height:100px;border-radius:26px}.tl2 .tile svg{width:56px;height:56px}.tl2 .tile .letter{font-size:50px}'
           '.tn{font-size:26px;text-align:center;padding:0 12px;line-height:1.2}'
           '.tl2.hot{outline:3px solid var(--plum);outline-offset:4px}.core .tile{width:120px;height:120px}.core .tn{font-size:30px}')
    st = .3
    js = TITLES_IN
    if p.get('center'):
        js += "tl.fromTo('#tc',{opacity:0,scale:.7},{opacity:1,scale:1,duration:.5,ease:'back.out(1.5)'},.2);"; st = .45
    js += f"tl.fromTo('.tl2:not(.core)',{{opacity:0,scale:.75}},{{opacity:1,scale:1,duration:.45,stagger:.11,ease:'back.out(1.6)'}},{st});"
    js += f"tl.fromTo('.lines line',{{opacity:0}},{{opacity:.85,duration:.3,stagger:.08}},{st+.25});"
    end = st + .11*(n-1) + .5
    return dict(html=html, css=css, js=_full(js), enter=end, exit=0, hero=end+.3,
                sfx=[(0, 'whoosh', -17), (st, 'pop', -18), (end-.1, 'click-soft', -18)], full=True)


def flow(o, ctx):
    p = o['props']; steps = p['steps']; n = len(steps)
    cards = ''
    for i, s in enumerate(steps):
        if i:
            cards += f'<div class="arr" id="a{i}"><div class="dot" id="d{i}"></div></div>'
        ico = tile(ctx, s.get('logo'), s['t']) if s.get('logo') else f'<span class="num">{i+1}</span>'
        if s.get('img'):
            ico = f'<div class="simg"><img src="{ctx["img"](s["img"])}"></div>' + ico
        cards += (f'<div class="step glass{" hot" if s.get("hot") else ""}" id="s{i}">{ico}<div class="d stt">{rich(s["t"])}</div>'
                  + (f'<div class="sts">{rich(s["s"])}</div>' if s.get('s') else '') + '</div>')
    html = f'<div class="canvas" id="cv"></div><div class="stage" id="st">{_titles(p)}<div class="flow"><div class="frow">{cards}</div></div></div>'
    w = min(340, int(1500/n) - 40)
    css = ('.flow{position:absolute;left:0;right:0;top:0;bottom:0;display:flex;align-items:center;justify-content:center;gap:0;padding-top:80px}'
           '.frow{display:flex;align-items:stretch}'
           f'.step{{width:{w}px;padding:30px 26px;display:flex;flex-direction:column;align-items:flex-start;gap:14px}}'
           '.simg{width:100%;height:200px;border-radius:18px;overflow:hidden;background:#fff}.simg img{width:100%;height:100%;object-fit:cover;display:block}'
           '.step.hot{outline:3px solid var(--plum);outline-offset:4px}.stt{font-size:38px}.sts{font-size:23px;color:var(--soft);line-height:1.4}'
           '.arr{width:84px;height:4px;align-self:center;background:repeating-linear-gradient(90deg,var(--plum2) 0 6px,transparent 6px 14px);position:relative}'
           '.dot{position:absolute;left:0;top:-7px;width:18px;height:18px;border-radius:50%;background:var(--plum);box-shadow:0 0 0 6px rgba(74,58,224,.18)}')
    gap = float(p.get('gap', .45))
    js = TITLES_IN
    for i in range(n):
        t0 = .25 + i*gap
        js += f"tl.fromTo('#s{i}',{{opacity:0,y:28,scale:.94}},{{opacity:1,y:0,scale:1,duration:.42,ease:'power3.out'}},{t0:.2f});"
        if i:
            js += f"tl.fromTo('#a{i}',{{opacity:0}},{{opacity:1,duration:.2}},{t0-.2:.2f});tl.fromTo('#d{i}',{{x:0}},{{x:66,duration:.5,ease:'power1.inOut'}},{t0-.2:.2f});"
    end = .25 + (n-1)*gap + .45
    return dict(html=html, css=css, js=_full(js), enter=end, exit=0, hero=end+.3,
                sfx=[(0, 'whoosh', -17)] + [(.25+i*gap, 'pop', -19) for i in range(n)], full=True)


def compare(o, ctx):
    p = o['props']; L, Rr = p['left'], p['right']
    def card(side, it):
        return (f'<div class="cmp {side}" id="{side}"><div class="cimg glass"><img src="{ctx["img"](it["img"])}"></div>'
                f'<div class="clab bb">{rich(it["label"])}</div></div>')
    mid = esc(p.get('mid', '→'))
    html = (f'<div class="canvas" id="cv"></div><div class="stage" id="st">{_titles(p)}'
            f'<div class="cmpw">{card("cl", L)}<div class="mid d" id="mid">{mid}</div>{card("cr", Rr)}</div></div>')
    css = ('.cmpw{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:40px;padding-top:90px}'
           '.cmp{display:flex;flex-direction:column;align-items:center;gap:22px}.cimg{width:760px;height:460px;padding:12px;border-radius:28px}'
           '.cimg img{width:100%;height:100%;object-fit:cover;border-radius:18px;display:block}.clab{font-size:30px;padding:10px 24px;border-radius:999px;background:#fff;border:1px solid var(--line)}'
           '.mid{width:96px;height:96px;border-radius:50%;background:var(--plum);color:#fff;display:grid;place-items:center;font-size:48px;flex:none}')
    js = _full(TITLES_IN + "tl.fromTo('#cl',{opacity:0,x:-70},{opacity:1,x:0,duration:.5,ease:'power3.out'},.15);"
               "tl.fromTo('#cr',{opacity:0,x:70},{opacity:1,x:0,duration:.5,ease:'power3.out'},.35);"
               "tl.fromTo('#mid',{opacity:0,scale:.5},{opacity:1,scale:1,duration:.4,ease:'back.out(1.8)'},.6);")
    return dict(html=html, css=css, js=js, enter=1.0, exit=0, hero=1.4,
                sfx=[(0, 'whoosh', -17), (.6, 'pop', -18)], full=True)


def image(o, ctx):
    p = o['props']
    cap = f'<div class="icap bb" id="ic">{rich(p["caption"])}</div>' if p.get('caption') else ''
    html = (f'<div class="canvas" id="cv"></div><div class="stage" id="st">{_titles(p)}<div class="iw">'
            f'<div class="ibox glass" id="ib"><img id="im" src="{ctx["img"](p["img"])}"></div>{cap}</div></div>')
    top = 120 if p.get('title') else 0
    css = (f'.iw{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;padding-top:{top}px}}'
           '.ibox{width:1240px;height:698px;padding:14px;border-radius:32px;overflow:hidden}.ibox img{width:100%;height:100%;object-fit:cover;border-radius:20px;display:block}'
           '.icap{font-size:30px;padding:10px 26px;border-radius:999px;background:#fff;border:1px solid var(--line)}')
    js = _full(TITLES_IN + "tl.fromTo('#ib',{opacity:0,y:40,scale:.94},{opacity:1,y:0,scale:1,duration:.5,ease:'power3.out'},.1);"
               "tl.fromTo('#im',{scale:1},{scale:1.05,duration:D,ease:'none'},0);"
               + ("tl.fromTo('#ic',{opacity:0,y:12},{opacity:1,y:0,duration:.3},.45);" if cap else ''))
    return dict(html=html, css=css, js=js, enter=.8, exit=0, hero=1.2, sfx=[(0, 'whoosh', -17)], full=True)


def journey(o, ctx):
    """Recurring section map: nodes on a path, done ones ticked, current one lit (Liam 'Business Map')."""
    p = o['props']; items = p['items']; cur = int(p['current']); n = len(items)
    xs = [260 + i*(1400/(n-1)) for i in range(n)]
    ys = [640 + (60 if i % 2 else -40) for i in range(n)]
    d = 'M' + ' L'.join(f'{x:.0f},{y:.0f}' for x, y in zip(xs, ys))
    nodes = ''
    for i, (x, y, it) in enumerate(zip(xs, ys, items)):
        st = 'done' if i < cur else ('cur' if i == cur else 'todo')
        mark = '✓' if st == 'done' else str(i+1)
        nodes += (f'<div class="jn {st}" id="j{i}" style="left:{x-64:.0f}px;top:{y-64:.0f}px"><div class="jc d">{mark}</div>'
                  f'<div class="jl bb">{rich(it)}</div></div>')
    html = (f'<div class="canvas" id="cv"></div><div class="stage" id="st">{_titles(p)}'
            f'<svg class="jp" viewBox="0 0 1920 1080"><path id="jpath" d="{d}"/></svg>{nodes}</div>')
    css = ('.jp{position:absolute;inset:0;width:1920px;height:1080px}.jp path{fill:none;stroke:var(--plum2);stroke-width:5;stroke-linecap:round;stroke-linejoin:round}'
           '.jn{position:absolute;width:128px;display:flex;flex-direction:column;align-items:center}'
           '.jc{width:128px;height:128px;border-radius:50%;display:grid;place-items:center;font-size:54px;background:#fff;border:2px solid var(--line);box-shadow:0 20px 40px -20px rgba(23,19,13,.35)}'
           '.jl{position:absolute;top:150px;width:320px;text-align:center;font-size:30px;line-height:1.25}'
           '.done .jc{background:var(--sage);color:var(--ink)}.todo .jc{color:var(--muted)}.todo .jl{color:var(--muted)}'
           '.cur .jc{background:var(--plum);color:#fff;border-color:var(--plum);box-shadow:0 0 0 14px rgba(74,58,224,.16),0 24px 50px -18px rgba(74,58,224,.6)}')
    js = TITLES_IN + ("tl.fromTo('#jpath',{strokeDasharray:2400,strokeDashoffset:2400},{strokeDashoffset:0,duration:.9,ease:'power2.inOut'},.15);"
                      "tl.fromTo('.jn',{opacity:0,y:20},{opacity:1,y:0,duration:.4,stagger:.12,ease:'power3.out'},.3);")
    hi = .3 + .12*(n-1) + .45
    js += f"tl.fromTo('#j{cur} .jc',{{scale:.8}},{{scale:1,duration:.5,ease:'back.out(2)'}},{hi:.2f});"
    return dict(html=html, css=css, js=_full(js), enter=hi+.5, exit=0, hero=hi+.7,
                sfx=[(-.8, 'riser', -20), (0, 'whoosh', -17), (hi, 'sparkle', -18)], full=True)


def units(o, ctx):
    """Unit grid: one square per item, coloured by group (e.g. 34 objects: 32 code, 1 AI, 1 Poly Haven)."""
    p = o['props']; groups = p['groups']
    total = sum(g['n'] for g in groups)
    cols = p.get('cols') or min(17, total)
    sq = min(70, int(1400/cols) - 12)
    cells = ''; k = 0
    for gi, g in enumerate(groups):
        for _ in range(g['n']):
            cells += f'<div class="u g{gi}" style="background:var(--{g.get("color", "lav")})"></div>'; k += 1
    legend = ''.join(f'<div class="lg"><span class="sw" style="background:var(--{g.get("color", "lav")})"></span><span class="d lgn">{g["n"]}</span><span class="lgl">{rich(g["label"])}</span></div>' for g in groups)
    html = (f'<div class="canvas" id="cv"></div><div class="stage" id="st">{_titles(p)}<div class="uw">'
            f'<div class="ug" style="grid-template-columns:repeat({cols},{sq}px)">{cells}</div><div class="lgs" id="lgs">{legend}</div></div></div>')
    css = (f'.uw{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:56px;padding-top:110px}}'
           f'.ug{{display:grid;gap:12px}}.u{{width:{sq}px;height:{sq}px;border-radius:16px;box-shadow:0 10px 20px -12px rgba(23,19,13,.4)}}'
           '.lgs{display:flex;gap:56px}.lg{display:flex;align-items:center;gap:14px}.sw{width:30px;height:30px;border-radius:9px}.lgn{font-size:54px}.lgl{font-size:28px;color:var(--soft)}')
    run = min(1.4, .03*total + .4)
    js = _full(TITLES_IN + f"tl.fromTo('.u',{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.3,stagger:{run/total:.4f},ease:'back.out(1.8)'}},.2);"
               f"tl.fromTo('#lgs .lg',{{opacity:0,y:14}},{{opacity:1,y:0,duration:.35,stagger:.12}},{.2+run:.2f});")
    end = .2 + run + .12*len(groups) + .35
    return dict(html=html, css=css, js=js, enter=end, exit=0, hero=end+.3,
                sfx=[(0, 'whoosh', -17), (.2, 'typing', -22), (.2+run, 'sparkle', -19)], full=True)


def three(o, ctx):
    """Three.js scene on the canvas. mode 'model': a GLB on a turntable (optional paint swatches);
    mode 'orb': a pearl orb on a lit ring with DOM step labels around it (Liam '8-step' sphere)."""
    p = o['props']; mode = p.get('mode', 'orb')
    labels = ''
    if mode == 'orb':
        import math
        L = p.get('labels', []); cur = p.get('current', -1)
        for i, t in enumerate(L):
            a = math.pi*(1.08 - 1.16*i/max(len(L)-1, 1))
            x, y = 960 + 600*math.cos(a), 640 - 300*math.sin(a)
            labels += f'<div class="ol bb{" on" if i == cur else ""}" id="ol{i}" style="left:{x-150:.0f}px;top:{y-28:.0f}px">{rich(t)}</div>'
    sw = ''
    if p.get('swatches'):
        sw = '<div class="sws" id="sws">' + ''.join(
            f'<div class="swc" id="sw{i}"><i class="ring" id="sr{i}"></i><span style="background:{s["hex"]}"></span><em>{esc(s["name"])}</em></div>' for i, s in enumerate(p['swatches'])) + '</div>'
    cap = f'<div class="tcap bb" id="tcap">{rich(p["caption"])}</div>' if p.get('caption') else ''
    html = (f'<div class="canvas" id="cv"></div><div class="stage" id="st"><div class="shadow3"></div><canvas id="gl" width="1920" height="1080"></canvas>'
            f'{_titles(p)}{labels}{sw}{cap}</div>')
    css = ('#gl{position:absolute;inset:0;width:1920px;height:1080px}'
           '.shadow3{position:absolute;left:560px;top:780px;width:800px;height:150px;border-radius:50%;background:radial-gradient(closest-side,rgba(23,19,13,.32),transparent)}'
           '.ol{position:absolute;width:300px;text-align:center;font-size:26px;padding:10px 16px;border-radius:999px;background:rgba(255,255,255,.9);border:1px solid var(--line)}'
           '.ol.on{background:var(--plum);color:#fff;border-color:var(--plum)}'
           '.sws{position:absolute;left:0;right:0;bottom:84px;display:flex;justify-content:center;gap:14px}'
           '.swc{display:flex;align-items:center;gap:10px;padding:8px 18px 8px 8px;border-radius:999px;background:rgba(255,255,255,.9);border:1px solid var(--line);font-family:BodyBold;font-size:20px}'
           '.swc{position:relative}.swc span{width:34px;height:34px;border-radius:50%;box-shadow:inset 0 0 0 2px rgba(255,255,255,.7)}.swc em{font-style:normal}'
           '.ring{position:absolute;inset:-5px;border-radius:999px;border:3px solid var(--plum);opacity:0}'
           '.tcap{position:absolute;left:0;right:0;top:172px;text-align:center;font-size:28px;color:var(--soft)}')
    js = TITLES_IN + "tl.fromTo('#gl',{opacity:0,y:30},{opacity:1,y:0,duration:.6,ease:'power3.out'},.1);"
    if labels:
        js += "tl.fromTo('.ol',{opacity:0,scale:.85},{opacity:1,scale:1,duration:.35,stagger:.07,ease:'back.out(1.6)'},.5);"
    if sw:
        n = len(p['swatches']); step = float(p.get('swatch_step', .5))
        js += f"tl.fromTo('.swc',{{opacity:0,y:14}},{{opacity:1,y:0,duration:.3,stagger:.06}},.4);"
        for i in range(n):
            js += f"tl.set('#sr{i}',{{opacity:1}},{.9+i*step:.2f});"
            if i < n-1:
                js += f"tl.set('#sr{i}',{{opacity:0}},{.9+(i+1)*step:.2f});"
    if cap:
        js += "tl.fromTo('#tcap',{opacity:0,y:12},{opacity:1,y:0,duration:.3},.6);"
    cfg = dict(mode=mode, model=ctx['model'](p['model']) if p.get('model') else None, spin=float(p.get('spin', .35)),
               start=float(p.get('angle', -.6)), scale=float(p.get('scale', 1)), y=float(p.get('y', 0)))
    module = THREE_MODULE.replace('__CFG__', json.dumps(cfg))
    return dict(html=html, css=css, js=_full(js), module=module, enter=1.0, exit=0, hero=min(2.0, ctx['D']*.5),
                sfx=[(-.8, 'riser', -20), (0, 'whoosh-cinematic', -18)], full=True)


THREE_MODULE = r"""
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
const CFG = __CFG__;
const canvas = document.getElementById('gl');
const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(1920, 1080, false); renderer.setPixelRatio(1); renderer.setClearColor(0x000000, 0);
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.outputColorSpace = THREE.SRGBColorSpace;
const scene = new THREE.Scene();
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
const camera = new THREE.PerspectiveCamera(30, 1920/1080, 0.1, 100);
camera.position.set(0, 1.5, 7.9); camera.lookAt(0, 0.35, 0);
scene.add(new THREE.HemisphereLight(0xffffff, 0xe8e0ff, 1.2));
const key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(3, 5, 4); scene.add(key);
const pivot = new THREE.Group(); scene.add(pivot);
function build() {
  if (CFG.mode === 'model') {
    const draco = new DRACOLoader().setDecoderPath('../assets/vendor/three/draco/');
    return new GLTFLoader().setDRACOLoader(draco).loadAsync(CFG.model).then(g => {
      const m = g.scene; const box = new THREE.Box3().setFromObject(m); const size = box.getSize(new THREE.Vector3());
      const s = 3.4 / Math.max(size.x, size.y, size.z) * CFG.scale; m.scale.setScalar(s);
      const c = new THREE.Box3().setFromObject(m).getCenter(new THREE.Vector3()); const b = new THREE.Box3().setFromObject(m);
      m.position.set(-c.x, -b.min.y - 0.55 + CFG.y, -c.z); pivot.add(m);
      const disc = new THREE.Mesh(new THREE.CylinderGeometry(2.3, 2.3, 0.08, 96), new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.35, clearcoat: 1 }));
      disc.position.y = -0.6; pivot.add(disc);
      const ring = new THREE.Mesh(new THREE.TorusGeometry(2.32, 0.025, 16, 160), new THREE.MeshStandardMaterial({ color: 0x4A3AE0, emissive: 0x4A3AE0, emissiveIntensity: 1.4 }));
      ring.rotation.x = Math.PI/2; ring.position.y = -0.56; pivot.add(ring);
    });
  }
  const orb = new THREE.Mesh(new THREE.SphereGeometry(1.05, 96, 64), new THREE.MeshPhysicalMaterial({ color: 0xF6F1FF, roughness: 0.18, metalness: 0.1, clearcoat: 1, sheen: 1, sheenColor: new THREE.Color(0xB7A8FF), iridescence: 0.6 }));
  orb.position.y = 0.55; pivot.add(orb);
  for (let i = 0; i < 3; i++) {
    const r = new THREE.Mesh(new THREE.TorusGeometry(1.5 + i*0.32, 0.012, 12, 200), new THREE.MeshStandardMaterial({ color: 0x7B6CFF, emissive: 0x7B6CFF, emissiveIntensity: 0.9 - i*0.25 }));
    r.rotation.x = Math.PI/2; r.position.y = -0.45; pivot.add(r);
  }
  const base = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.4, 0.18, 96), new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.3, clearcoat: 1 }));
  base.position.y = -0.5; pivot.add(base);
  return Promise.resolve();
}
function renderAt(t) { pivot.rotation.y = CFG.start + t * CFG.spin; renderer.render(scene, camera); }
const ready = build().then(() => { renderAt(window.__hfThreeTime || 0); window.__three_ok = true; });
window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {}; window.__hf.buildReady.scene3d = ready;
window.__ready3d = ready;
window.addEventListener('hf-seek', e => renderAt(e.detail.time));
"""

BUILDERS = {'keyword': keyword, 'lower-third': lower, 'chips': chips, 'banner': banner, 'chapter': chapter, 'section-chip': section_chip,
            'broll': broll, 'broll-full': broll_full, 'stat': stat, 'tiles': tiles, 'flow': flow, 'compare': compare,
            'image': image, 'journey': journey, 'units': units, 'three': three}


from slides import SLIDES  # noqa: E402  (slides.py imports helpers defined above)
BUILDERS.update(SLIDES)
from talking import TALKING  # noqa: E402
BUILDERS.update(TALKING)


def page(o, c, D):
    """Standalone HyperFrames composition for one overlay."""
    importmap = ''
    module = ''
    if c.get('module'):
        importmap = ('<script type="importmap">{"imports":{"three":"../assets/vendor/three/three.module.js",'
                     '"three/addons/":"../assets/vendor/three/addons/"}}</script>')
        module = f'<script type="module">{c["module"]}</script>'
    video = c.get('video', '')
    body = (video if c.get('video_below') else '') + \
        f'<div class="layer clip" data-start="0" data-duration="{D}" data-track-index="1">{c["html"]}</div>' + \
        ('' if c.get('video_below') else video)
    return f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=1920, height=1080"><title>{o['id']}</title>
<style>{TOKENS}{c.get('css', '')}</style>
<script src="../assets/vendor/gsap.min.js"></script>{importmap}
</head><body>
<div id="root" data-composition-id="{o['id']}" data-duration="{D}" data-width="1920" data-height="1080">{body}</div>
<script>
const D={D};
const tl=gsap.timeline({{paused:true}});
{c['js']}
window.__timelines["{o['id']}"]=tl;
</script>{module}
</body></html>
"""
