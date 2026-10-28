# Full-frame B-roll slides for the middle of a section (about 1 every 2 minutes). Every slide shows REAL material:
# frames and clips of the actual videos, real transcript lines, real code and logs, real page screenshots, inside
# faithful app frames (Chrome, VS Code, terminal, YouTube) with real icons (Material Symbols, codicons), a real 3D
# MacBook (GLB, pmndrs examples, MIT) and the Contentta 3D pieces (extruded logo tiles, Claude Code voxel mascot).
# Few words, no big numbers: the motion carries the idea. Same return dict as components.py (full=True).
import json, math, re
from pathlib import Path
from common import R
from components import esc, rich, _titles, TITLES_IN

MASCOT = (Path(__file__).resolve().parent/'elements'/'claude-code-mascot.html').read_text(encoding='utf-8')

ICONS = {
    'scissors': '<circle cx="6" cy="6" r="3"/><path d="M8.12 8.12 12 12"/><path d="M20 4 8.12 15.88"/><circle cx="6" cy="18" r="3"/><path d="M14.8 14.8 20 20"/>',
    'layers': '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
    'wand': '<path d="m21.64 3.64-1.28-1.28a1.21 1.21 0 0 0-1.72 0L2.36 18.64a1.21 1.21 0 0 0 0 1.72l1.28 1.28a1.2 1.2 0 0 0 1.72 0L21.64 5.36a1.2 1.2 0 0 0 0-1.72"/><path d="m14 7 3 3"/><path d="M5 6v4"/><path d="M19 14v4"/><path d="M10 2v2"/><path d="M7 8H3"/><path d="M21 16h-4"/><path d="M11 3H9"/>',
    'play': '<polygon points="6 3 20 12 6 21 6 3"/>',
    'check': '<path d="M20 6 9 17l-5-5"/>',
}

KIT = """
@font-face{font-family:UI;src:url('../assets/fonts/ui.ttf')}@font-face{font-family:UIB;src:url('../assets/fonts/ui-bold.ttf')}
@font-face{font-family:YT;src:url('../assets/fonts/yt.ttf')}@font-face{font-family:YTM;src:url('../assets/fonts/yt-medium.ttf')}
.scene{position:absolute;inset:0;perspective:2200px;perspective-origin:50% 42%;transform-style:preserve-3d}
.t3{position:absolute;transform-style:preserve-3d}.t3 .ly,.t3 .fc{position:absolute;inset:0;border-radius:inherit}
.t3 .fc{display:grid;place-items:center;border:1px solid rgba(23,19,13,.08);box-shadow:inset 0 3px 0 rgba(255,255,255,.55),inset 0 -10px 24px rgba(0,0,0,.06)}
.t3 .fc svg{width:56%;height:56%}.t3 .fc svg.ico{width:50%;height:50%}
.shd{position:absolute;border-radius:50%;background:radial-gradient(ellipse,rgba(23,19,13,.30),rgba(23,19,13,0) 70%);filter:blur(8px)}
.lbl{position:absolute;text-align:center;font-family:BodyBold;font-size:28px;color:var(--soft);white-space:nowrap}
.pill{position:absolute;display:flex;align-items:center;gap:12px;padding:12px 26px;border-radius:999px;background:#fff;border:1px solid var(--line);
 box-shadow:0 14px 30px -14px rgba(23,19,13,.35);font-family:BodyBold;font-size:26px;white-space:nowrap}
.ico{fill:none;stroke:currentColor;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}
.mwrap,.mhop{position:absolute;width:0;height:0;transform-style:preserve-3d}
.mscale{position:absolute;left:-286px;top:-312px;width:572px;height:312px;transform-origin:50% 100%;transform-style:preserve-3d}
.mascot{position:absolute;inset:0;transform-style:preserve-3d}.vx-l{position:absolute;inset:0;transform-style:preserve-3d}
.vx-l i{position:absolute;left:0;top:0;width:52px;height:52px}
.ui{display:block;flex:none}
.cur{position:absolute;filter:drop-shadow(0 3px 5px rgba(0,0,0,.25))}
.mw{position:absolute;border-radius:14px;background:#fff;overflow:hidden;
 box-shadow:0 0 0 1px rgba(23,19,13,.14),0 2px 6px rgba(23,19,13,.06),0 28px 60px -16px rgba(23,19,13,.42),0 70px 120px -40px rgba(23,19,13,.30)}
.mw.dk{background:#1A1816;box-shadow:0 0 0 1px rgba(0,0,0,.6),inset 0 0 0 1px rgba(255,255,255,.07),0 28px 60px -16px rgba(23,19,13,.55),0 70px 120px -40px rgba(23,19,13,.35)}
.tl3{display:flex;gap:8px;flex:none}.tl3 i{width:13px;height:13px;border-radius:50%;background:#FF5F57;box-shadow:inset 0 0 0 .6px rgba(0,0,0,.22)}
.tl3 i+i{background:#FEBC2E}.tl3 i+i+i{background:#28C840}
.cr-tabs{height:44px;background:#DFE3E7;display:flex;align-items:flex-end;padding:0 10px 0 18px;gap:10px}
.cr-tabs .tl3{align-self:center;margin-right:10px}
.cr-tab{height:36px;width:270px;background:#fff;border-radius:10px 10px 0 0;display:flex;align-items:center;gap:9px;padding:0 10px 0 12px;font:13px/1 UI;color:#1F1F1F}
.cr-tab span{flex:1;white-space:nowrap;overflow:hidden}.cr-tab img,.cr-tab svg.fav{width:16px;height:16px}
.cr-plus{align-self:center}
.cr-bar{height:46px;background:#fff;display:flex;align-items:center;gap:14px;padding:0 14px;border-bottom:1px solid #E6E6E6}
.cr-omni{flex:1;height:34px;border-radius:17px;background:#EDF0F3;display:flex;align-items:center;gap:10px;padding:0 14px;font:14px/1 UI;color:#1F1F1F}
.cr-omni span{flex:1;white-space:nowrap;overflow:hidden}
.cr-av{width:26px;height:26px;border-radius:50%;background:#C9D7F2 center/cover;flex:none}
.cr-page{position:absolute;left:0;right:0;top:90px;bottom:0;overflow:hidden;background:#fff}
.tm-top{position:relative;height:40px;display:flex;align-items:center;padding:0 16px;background:#24211E;border-bottom:1px solid rgba(255,255,255,.06);font:13px/1 UI;color:#A9A39A}
.tm-top span{position:absolute;left:0;right:0;text-align:center}
.tm-body{position:absolute;left:0;right:0;top:40px;bottom:0;padding:22px 30px;font:500 21px/1.6 Mono;color:#E9E4DC;white-space:pre;overflow:hidden}
.cc-o{color:#D97757}.cc-g{color:#4EBA65}.cc-d{color:#8F8981}.cc-w{color:#F4F0EA}.cc-r{color:#FF6B6B}.cc-b{font-weight:700;color:#F4F0EA}
.lnk{position:absolute;inset:0;width:1920px;height:1080px}.lnk path{fill:none;stroke:var(--plum2);stroke-width:4;stroke-dasharray:3 12;stroke-linecap:round}
.vframe{position:absolute;border-radius:16px;overflow:hidden;background:#111;border:7px solid #fff;
 box-shadow:0 0 0 1px rgba(23,19,13,.12),0 30px 60px -22px rgba(23,19,13,.5),0 6px 14px rgba(23,19,13,.08)}
.vframe img,.vframe video{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;display:block}
.chip{position:absolute;padding:7px 16px;border-radius:999px;background:rgba(255,255,255,.94);font:600 19px/1 UIB;color:var(--ink);
 box-shadow:0 6px 16px -6px rgba(23,19,13,.4);white-space:nowrap}
"""

TL3 = '<div class="tl3"><i></i><i></i><i></i></div>'


def mix(c1, c2, f):
    a = [int(c1[k:k+2], 16) for k in (1, 3, 5)]; b = [int(c2[k:k+2], 16) for k in (1, 3, 5)]
    return '#' + ''.join(f'{round(x+(y-x)*f):02X}' for x, y in zip(a, b))


def tile3d(tid, x, y, size, inner, face='#FFFFFF', side=('#98948A', '#CDC7BA'), depth=24, n=10, extra=''):
    lays = ''.join(f'<div class="ly" style="transform:translateZ({-depth+2*depth*k/(n-1):.1f}px);background:{mix(side[0], side[1], k/(n-1))}"></div>' for k in range(n))
    return (f'<div class="t3" id="{tid}" style="left:{x:.0f}px;top:{y:.0f}px;width:{size}px;height:{size}px;border-radius:{round(size*.26)}px">'
            f'{lays}<div class="fc" style="transform:translateZ({depth}px);background:{face}">{inner}{extra}</div></div>')


def icon(name, color='#4A3AE0'):
    return f'<svg class="ico" viewBox="0 0 24 24" style="color:{color}">{ICONS[name]}</svg>'


def ui(name, size=20, color='currentColor'):
    """A real app icon from assets/ui/icons (m-* Material Symbols, c-* VS Code codicons)."""
    f = R/'assets'/'ui'/'icons'/f'{name}.svg'
    if not f.exists():
        return ''
    head, rest = f.read_text(encoding='utf-8').split('>', 1)
    head = re.sub(r'\s(width|height|fill|class|style)="[^"]*"', '', head)
    return f'{head} class="ui" style="width:{size}px;height:{size}px;fill:{color}">{rest}'


def logo(ctx, slug, color):
    svg = ctx['logo'](slug) or ''
    return svg.replace('<svg ', f'<svg fill="{color}" ', 1)


def shadow(x, y, w, h=70, sid=''):
    return f'<div class="shd"{f" id={chr(34)}{sid}{chr(34)}" if sid else ""} style="left:{x:.0f}px;top:{y:.0f}px;width:{w}px;height:{h}px"></div>'


def mascot(mid, x, y, scale=.4):
    """Claude Code voxel mascot standing with its feet centred on (x, y)."""
    return (f'<div class="mwrap" id="{mid}" style="left:{x:.0f}px;top:{y:.0f}px"><div class="mhop" id="{mid}h">'
            f'<div class="mscale" style="transform:scale({scale})"><div class="mascot" id="{mid}v">{MASCOT}</div></div></div></div>')


CUR = {'cursor': (84, 48), 'hand': (92, 42)}  # hotspot in the 256 px apple_cursor artwork


def cursor(cid, x, y, size=60, kind='cursor'):
    """macOS pointer whose tip sits on (x, y); move it with GSAP x/y."""
    k = size/256; tx, ty = CUR[kind]
    return f'<img class="cur" id="{cid}" src="../assets/ui/{kind}.svg" style="left:{x-tx*k:.0f}px;top:{y-ty*k:.0f}px;width:{size}px;height:{size}px">'


def chrome(wid, x, y, w, h, url, inner, tab, fav=''):
    """Chrome window (light) with a real tab strip and omnibox; inner fills the page area (top 90 px is chrome)."""
    g = '#5F6368'
    return (f'<div class="mw" id="{wid}" style="left:{x:.0f}px;top:{y:.0f}px;width:{w}px;height:{h}px">'
            f'<div class="cr-tabs">{TL3}<div class="cr-tab">{fav}<span>{esc(tab)}</span>{ui("m-close", 16, g)}</div>'
            f'<div class="cr-plus">{ui("m-add", 20, g)}</div></div>'
            f'<div class="cr-bar">{ui("m-arrow_back", 22, g)}{ui("m-arrow_forward", 22, "#C4C7C5")}{ui("m-refresh", 22, g)}'
            f'<div class="cr-omni">{ui("m-tune", 18, g)}<span>{esc(url)}</span>{ui("m-star", 20, g)}</div>'
            f'<i class="cr-av"></i>{ui("m-more_vert", 22, g)}</div><div class="cr-page">{inner}</div></div>')


def term(wid, x, y, w, h, title, inner, extra=''):
    return (f'<div class="mw dk" id="{wid}" style="left:{x:.0f}px;top:{y:.0f}px;width:{w}px;height:{h}px">'
            f'<div class="tm-top">{TL3}<span>{esc(title)}</span></div><div class="tm-body">{inner}</div>{extra}</div>')


def enter3d(sel, t, ry=-70, rx=14, to_ry=-16, to_rx=10, dur=.9, spin=False):
    fr = -376 if spin else ry
    return (f"tl.fromTo('{sel}',{{opacity:0,scale:.55,rotationY:{fr},rotationX:{rx}}},"
            f"{{opacity:1,scale:1,rotationY:{to_ry},rotationX:{to_rx},duration:{dur},ease:'{'power3.out' if spin else 'back.out(1.4)'}'}},{t:.2f});")


def win_in(sel, t=.1, ry=-12, rx=6, to_ry=-5, to_rx=4, end_ry=5, end_rx=3, D=5.0):
    """A window floats in tilted, then turns slowly the other way until the end."""
    return (f"tl.fromTo('{sel}',{{opacity:0,y:60,rotationY:{ry},rotationX:{rx}}},{{opacity:1,y:0,rotationY:{to_ry},rotationX:{to_rx},duration:.75,ease:'power3.out'}},{t:.2f});"
            f"tl.to('{sel}',{{rotationY:{end_ry},rotationX:{end_rx},duration:{max(.5, D-t-.75):.2f},ease:'sine.inOut'}},{t+.75:.2f});")


def drift(sel, t, until, ry=16, rx=6):
    return f"tl.to('{sel}',{{rotationY:{ry},rotationX:{rx},duration:{max(.4, until-t):.2f},ease:'sine.inOut'}},{t:.2f});"


def floaty(sel, t, until, amp=-12, period=1.4):
    n = max(0, int((until-t)//period)-1)
    return f"tl.fromTo('{sel}',{{y:0}},{{y:{amp},duration:{period},ease:'sine.inOut',yoyo:true,repeat:{n}}},{t:.2f});"


def pop(sel, t, frm=.6):
    return f"tl.fromTo('{sel}',{{opacity:0,scale:{frm}}},{{opacity:1,scale:1,duration:.45,ease:'back.out(1.6)'}},{t:.2f});"


def show(sel, t, y=14):
    return f"tl.fromTo('{sel}',{{opacity:0,y:{y}}},{{opacity:1,y:0,duration:.38,ease:'power3.out'}},{t:.2f});"


def hop(mid, t, x0, x1, h=110, d=.5):
    # immediateRender:false on every hop: a later fromTo would otherwise paint its start state at frame 0
    return (f"tl.fromTo('#{mid}',{{x:{x0:.0f}}},{{x:{x1:.0f},duration:{d},ease:'power1.inOut',immediateRender:false}},{t:.2f});"
            f"tl.fromTo('#{mid}h',{{y:0}},{{y:{-h},duration:{d/2},ease:'power2.out',immediateRender:false}},{t:.2f});"
            f"tl.fromTo('#{mid}h',{{y:{-h}}},{{y:0,duration:{d/2},ease:'power2.in',immediateRender:false}},{t+d/2:.2f});")


def sway(mid, t, D):
    return f"tl.fromTo('#{mid}v',{{rotationY:-28,rotationX:8}},{{rotationY:24,rotationX:6,duration:{max(.5, D-t):.2f},ease:'sine.inOut'}},{t:.2f});"


def typed(sel, n, t, cps=22):
    """Type n characters into an element styled .ty (inline-block, overflow hidden, width 0)."""
    return f"tl.fromTo('{sel}',{{width:'0ch'}},{{width:'{n}ch',duration:{max(.2, n/cps):.2f},ease:'steps({n})'}},{t:.2f});"


def full(html, css, js, enter, hero, sfx, **kw):
    return dict(html=f'<div class="canvas" id="cv"></div><div class="stage" id="st">{html}</div>', css=KIT + css, js=js,
                enter=enter, exit=0, hero=hero, sfx=sfx, full=True, **kw)


def _hl(line, rules):
    """Colour code tokens (VS Code Dark+) in one left-to-right pass, escaping everything else."""
    rx = re.compile('|'.join(f'({r})' for r, _ in rules)); out, pos = [], 0
    for m in rx.finditer(line):
        out.append(esc(line[pos:m.start()]))
        out.append(f'<b style="color:{rules[m.lastindex-1][1]};font-weight:500">{esc(m.group())}</b>'); pos = m.end()
    return ''.join(out) + esc(line[pos:])


CODE_RULES = [(r"'[^']*'|\"[^\"]*\"", '#CE9178'), (r'</?[a-z]+', '#569CD6'), (r'\btl\.\w+', '#DCDCAA'), (r'(?<=[:(,\s-])-?\d*\.?\d+(?!\w)', '#B5CEA8')]
JSON_RULES = [(r'"[^"]*"(?=\s*:)', '#9CDCFE'), (r'"[^"]*"', '#CE9178'), (r'-?\d+\.?\d*', '#B5CEA8')]
hl_code = lambda line: _hl(line, CODE_RULES)
hl_json = lambda line: _hl(line, JSON_RULES)


# ------------------------------------------------------------------ 1. the whole system: 4 real screens, mascot hops across

def sl_system(o, ctx):
    """props: title, steps [{label, img, icon (scissors|layers|wand|play), progress?}]: img = a real frame of each step."""
    p = o['props']; D = ctx['D']
    steps = p['steps']; n = len(steps)
    w = 360; h = round(w*9/16) + 30; gap = 84; top = 470
    x0 = (1920 - (n*w + (n-1)*gap))/2
    xs = [x0 + i*(w+gap) for i in range(n)]; cy = top + h/2
    seg = gap - 28
    lines = ''.join(f'<path class="base" d="M{xs[i]+w+14:.0f},{cy:.0f} H{xs[i+1]-14:.0f}"/><path class="prog" id="pg{i}" d="M{xs[i]+w+14:.0f},{cy:.0f} H{xs[i+1]-14:.0f}"/>' for i in range(n-1))
    html = _titles(p) + f'<svg class="sl-path" viewBox="0 0 1920 1080">{lines}</svg><div class="scene">'
    for i, s in enumerate(steps):
        bar = '<i class="rbar" id="rb"></i>' if s.get('progress') else ''
        html += shadow(xs[i]+30, top+h+2, w-60, 44)
        html += (f'<div class="cw" id="k{i}" style="left:{xs[i]:.0f}px;top:{top}px;width:{w}px;height:{h}px">'
                 f'<i class="ring" id="kL{i}"></i><div class="mw sc"><div class="sc-bar">{TL3}</div>'
                 f'<div class="sc-img"><img id="ki{i}" src="{ctx["img"](s["img"], 960)}">{bar}</div></div>'
                 + tile3d(f't{i}', -34, h-66, 96, icon(s['icon']), depth=14, n=8) + '</div>')
        html += f'<div class="lbl" id="kl{i}" style="left:{xs[i]-30:.0f}px;width:{w+60}px;top:{top+h+46}px;font-size:34px">{rich(s["label"])}</div>'
    html += mascot('m', xs[0]+w/2, top+1, .34) + '</div>'
    css = ('.sl-path{position:absolute;inset:0;width:1920px;height:1080px}.sl-path path{fill:none;stroke-width:6;stroke-linecap:round}'
           f'.sl-path .base{{stroke:rgba(23,19,13,.16);stroke-dasharray:3 13}}.sl-path .prog{{stroke:var(--plum);stroke-dasharray:{seg};stroke-dashoffset:{seg}}}'
           '.cw{position:absolute;transform-style:preserve-3d}.sc{inset:0}'
           '.sc-bar{height:30px;background:#ECE8E2;display:flex;align-items:center;padding:0 12px}.sc-bar .tl3{gap:6px}.sc-bar .tl3 i{width:10px;height:10px}'
           '.sc-img{position:absolute;left:0;right:0;top:30px;bottom:0;overflow:hidden;background:#111}.sc-img img{width:100%;height:100%;object-fit:cover;display:block}'
           '.rbar{position:absolute;left:0;bottom:0;height:6px;width:100%;background:#FF0033;transform-origin:0 50%}'
           '.ring{position:absolute;inset:-10px;border-radius:22px;border:5px solid var(--plum);box-shadow:0 0 0 10px rgba(74,58,224,.14);opacity:0}')
    js = TITLES_IN
    for i in range(n):
        js += enter3d(f'#k{i}', .15+.1*i, ry=-50, rx=10, to_ry=-8, to_rx=8, dur=.8) + drift(f'#k{i}', .95+.1*i, D, ry=8, rx=6)
        js += show(f'#kl{i}', .45+.1*i) + f"tl.fromTo('#ki{i}',{{scale:1}},{{scale:1.08,duration:{D:.2f},ease:'none'}},0);"
    js += pop('#m', 1.0, .5) + sway('m', 1.0, D) + "tl.to('#kL0',{opacity:1,duration:.25},1.1);"
    sfx = [(0, 'whoosh', -17), (1.0, 'pop', -18)]
    t = 1.55
    for i in range(1, n):
        t = 1.55 + (i-1)*.8
        js += hop('m', t, xs[i-1]-xs[0], xs[i]-xs[0])
        js += f"tl.to('#pg{i-1}',{{strokeDashoffset:0,duration:.4,ease:'power1.inOut'}},{t:.2f});"
        js += f"tl.to('#kL{i}',{{opacity:1,duration:.2}},{t+.45:.2f});tl.fromTo('#k{i}',{{y:0}},{{y:10,duration:.12,yoyo:true,repeat:1,ease:'power2.out',immediateRender:false}},{t+.5:.2f});"
        sfx.append((round(t+.5, 2), 'pop', -18))
    if any(s.get('progress') for s in steps):
        js += f"tl.fromTo('#rb',{{scaleX:0}},{{scaleX:1,duration:{max(.4, D-t-.5):.2f},ease:'none'}},{t+.5:.2f});"
    end = t + .6
    sfx.append((round(end+.35, 2), 'sparkle', -19))
    return full(html, css, js, end, min(D-.2, end+.3), sfx)


# ------------------------------------------------------------------ 2. AI cut: a real timeline (frames, waveform, words), the cuts ripple out

def sl_cut(o, ctx):
    """props: title, file (raw video, default source), a, b (window, s), cuts [[start, end, label]], words [[start, end, text]],
    clip_name, caption. Cuts and words come from the real cut pass (utterances + cuts)."""
    p = o['props']; D = ctx['D']
    f = p.get('file') or ctx['video']; a, b = float(p['a']), float(p['b'])
    cuts = sorted(p['cuts']); words = p.get('words', [])
    WX, WY, W, H = 150, 316, 1620, 446
    hd = 92; TW = W - hd - 22; k = TW/(b-a)
    X = lambda t: (min(max(t, a), b) - a)*k
    RY, RH, TY, TH, VY, VH, AY, AH = 50, 34, 96, 52, 158, 128, 296, 118
    tw = round(VH*16/9); nth = math.ceil(TW/tw) + 1
    srcs = [ctx['img'](f'{f}@{a + (j*tw + tw/2)/k:.2f}', 320) for j in range(nth)]
    thumbs = ''.join(f'<img src="{s}" style="left:{j*tw}px;width:{tw}px">' for j, s in enumerate(srcs))
    nb = int(TW//4); pk = ctx['wave'](f, a, b, nb)
    wave = '<svg class="wv" width="%d" height="%d"><path d="%s"/></svg>' % (TW, AH, ''.join(
        f'M{i*4+2},{AH/2-hh:.1f}V{AH/2+hh:.1f}' for i, v in enumerate(pk) for hh in [max(1.2, v*AH*.42)]))
    chips = ''.join(f'<span class="wd" style="left:{X(s):.1f}px;width:{max(10, X(e)-X(s)-3):.1f}px">{esc(t)}</span>'
                    for s, e, t in words if e > a and s < b)
    bounds, t = [], a
    for cs, ce, lab in cuts:
        bounds += [(t, cs, None), (cs, ce, lab)]; t = ce
    bounds.append((t, b, None))
    name = esc(p.get('clip_name', Path(f).name))
    segs, tags = '', ''
    for j, (s, e, lab) in enumerate(bounds):
        x, wd = X(s), X(e) - X(s)
        trk = lambda cls, top, hh, inner, extra='': (f'<div class="tk {cls}" style="top:{top}px;height:{hh}px">'
                                                     f'<div class="in" style="left:{-x:.1f}px">{inner}</div>{extra}</div>')
        segs += (f'<div class="seg{" cut" if lab else ""}" id="sg{j}" style="left:{x:.1f}px;width:{wd:.1f}px">'
                 + trk('tT', TY, TH, chips) + trk('tV', VY, VH, thumbs, f'<b class="cn">{name}</b>' if not lab and wd > 170 else '') + trk('tA', AY, AH, wave)
                 + (f'<i class="cfx" id="cf{j}" style="top:{TY-4}px;height:{AY+AH-TY+8}px"></i>' if lab else '') + '</div>')
        if lab:
            tags += f'<div class="ctw" style="left:{x+wd/2:.1f}px;top:{VY+VH/2-14:.0f}px"><span class="ctag" id="ct{j}">{esc(lab)}</span></div>'
    ticks = ''
    for sec in range(math.ceil(a), int(b)+1):
        big = sec % 2 == 0
        ticks += f'<i class="tick{" big" if big else ""}" style="left:{X(sec):.1f}px"></i>'
        if big:
            ticks += f'<span class="tlab" style="left:{X(sec)+6:.1f}px">{sec//60:02d}:{sec % 60:02d}</span>'
    area = (f'<div class="area" style="left:{hd}px;width:{TW}px"><div class="ruler" style="top:{RY}px;height:{RH}px">{ticks}</div>'
            f'{segs}{tags}<div id="scan" style="top:{RY}px;height:{AY+AH-RY}px"><i></i></div></div>')
    heads = ''.join(f'<div class="th" style="top:{y}px;height:{hh}px">{lab}</div>' for y, hh, lab in ((TY, TH, 'Lời'), (VY, VH, 'V1'), (AY, AH, 'A1')))
    win = term('nle', WX, WY, W, H, p.get('bar', f'Timeline · {Path(f).name}'), '', f'<div class="hdr">{heads}</div>{area}')
    cap = f'<div class="pill" id="cap" style="left:0;right:0;margin:0 auto;width:max-content;top:{WY+H+54}px">{rich(p.get("caption", "bỏ câu dở, khoảng lặng"))}</div>'
    html = (_titles(p) + '<div class="scene">' + win + shadow(1645, 378, 150, 30)
            + tile3d('cl', 1650, 226, 140, logo(ctx, 'claude', '#D97757')) + '</div>' + cap)
    css = ('#nle .tm-body{display:none}.hdr{position:absolute;left:0;top:0;width:%dpx;bottom:0;background:#201E1B;border-right:1px solid rgba(255,255,255,.06)}'
           '.th{position:absolute;left:0;right:0;display:flex;align-items:center;padding-left:22px;font:600 17px UIB;color:#A39C92;background:#272420;border-radius:0 8px 8px 0;margin-right:10px}'
           '.area{position:absolute;top:0;bottom:0}.ruler{position:absolute;left:0;right:0;border-bottom:1px solid rgba(255,255,255,.10)}'
           '.tick{position:absolute;bottom:0;width:1px;height:9px;background:rgba(255,255,255,.28)}.tick.big{height:16px;background:rgba(255,255,255,.5)}'
           '.tlab{position:absolute;top:2px;font:500 14px Mono;color:#9C958B}'
           '.seg{position:absolute;top:0;bottom:0}.tk{position:absolute;left:1px;right:1px;overflow:hidden;border-radius:7px}.in{position:absolute;top:0;bottom:0;width:%dpx}'
           '.tT{background:#2B2824}.wd{position:absolute;top:9px;height:34px;border-radius:6px;background:#3D3832;color:#EEE8DF;font:500 17px/34px Body;padding:0 8px;white-space:nowrap;overflow:hidden}'
           '.tV{background:#2A2648;box-shadow:inset 0 0 0 2px #7366F0}.tV img{position:absolute;top:0;height:100%%;object-fit:cover;opacity:.92}'
           '.cn{position:absolute;left:6px;top:6px;padding:3px 8px;border-radius:5px;background:rgba(32,28,60,.85);font:600 13px UIB;color:#E6E2FF;white-space:nowrap}'
           '.tA{background:#173A2B;box-shadow:inset 0 0 0 2px #2F9E6E}.wv{position:absolute;left:0;top:0}.wv path{stroke:#4FE0A0;stroke-width:2.6;stroke-linecap:round}'
           '.cfx{position:absolute;left:0;right:0;border-radius:9px;background:rgba(255,86,86,.30);box-shadow:inset 0 0 0 3px #FF6B6B;opacity:0}'
           '.ctw{position:absolute;width:0;display:flex;justify-content:center}.ctag{display:block;padding:7px 14px;border-radius:999px;background:#FF5A5A;color:#fff;font:700 18px/1 BodyBold;box-shadow:0 6px 16px -4px rgba(0,0,0,.5);white-space:nowrap;opacity:0}'
           '#scan{position:absolute;left:0;width:3px;margin-left:-1px;background:#A99BFF;box-shadow:0 0 0 3px rgba(123,108,255,.25),0 0 24px rgba(123,108,255,.9)}'
           '#scan i{position:absolute;left:-8px;top:-2px;width:19px;height:22px;border-radius:5px 5px 9px 9px;background:#A99BFF}') % (hd, TW)
    t0, sweep = .6, 2.4
    js = TITLES_IN + win_in('#nle', .1, ry=0, rx=16, to_ry=0, to_rx=12, end_ry=0, end_rx=9, D=D)
    js += enter3d('#cl', .35, ry=-60, to_ry=-12) + drift('#cl', 1.25, D, ry=14) + show('#cap', 1.0)
    js += f"tl.fromTo('#scan',{{x:0}},{{x:{TW},duration:{sweep},ease:'none'}},{t0});tl.to('#scan',{{opacity:0,duration:.25}},{t0+sweep:.2f});"
    sfx = [(0, 'whoosh', -17)]
    for j, (s, e, lab) in enumerate(bounds):
        if lab:
            tk = t0 + (X(s)+X(e))/2/TW*sweep
            js += f"tl.to('#cf{j}',{{opacity:1,duration:.15}},{tk:.2f});" + pop(f'#ct{j}', tk, .5)
            sfx.append((round(tk, 2), 'click', -15))
    tr = t0 + sweep + .25; shift = 0.0
    for j, (s, e, lab) in enumerate(bounds):
        if lab:
            js += f"tl.to('#sg{j}',{{y:-30,opacity:0,duration:.32,ease:'power2.in'}},{tr:.2f});tl.to('#ct{j}',{{opacity:0,duration:.2}},{tr:.2f});"
            shift += X(e) - X(s)
        elif shift:
            js += f"tl.to('#sg{j}',{{x:{-shift:.1f},duration:.45,ease:'power3.inOut'}},{tr+.22:.2f});"
    sfx.append((round(tr+.2, 2), 'whoosh-short', -17))
    return full(html, css, js, tr+.7, min(D-.2, tr-.15), sfx)


# ------------------------------------------------------------------ 3. AI reads the real transcript file, the stumble lines go red and collapse

def sl_transcript(o, ctx):
    """props: title, file (tab name), crumb, lines [[id, start, end, gap, text]], first_line, strike [ids], reason, who."""
    p = o['props']; D = ctx['D']
    rows = p['lines']; strike = set(p['strike']); n0 = int(p.get('first_line', 1))
    WX, WY, W, H, LH = 130, 250, 1100, 660, 38
    body = ''
    for i, (uid, s, e, g, txt) in enumerate(rows):
        body += (f'<div class="ln{" del" if uid in strike else ""}" id="ln{i}"><span class="gn">{n0+i}</span><span class="cd">'
                 f'<b class="c-id">{esc(uid)}</b>  <b class="c-t">{s:7.2f}-{e:7.2f}</b>  <b class="c-g">(+{g:.2f})</b>  {esc(txt)}</span>'
                 f'<i class="stk" id="sk{i}"></i></div>')
    first = next(i for i, r in enumerate(rows) if r[0] in strike)
    dels = [i for i, r in enumerate(rows) if r[0] in strike]
    act = ''.join(ui(f'c-{n}', 26, '#1F1F1F' if n == 'files' else '#7A7A7A') for n in ('files', 'search', 'source-control', 'debug-alt', 'extensions'))
    ed = (f'<div class="mw" id="ed" style="left:{WX}px;top:{WY}px;width:{W}px;height:{H}px">'
          f'<div class="vs-top">{TL3}<span>{esc(p.get("file", "utterances.txt"))} — {esc(p.get("project", "edit"))}</span></div>'
          f'<div class="vs-act">{act}<i class="vs-on"></i></div>'
          f'<div class="vs-main"><div class="vs-tabs"><div class="vs-tab">{ui("c-file", 16, "#6C6C6C")}<span>{esc(p.get("file", "utterances.txt"))}</span>{ui("c-close", 15, "#6C6C6C")}</div></div>'
          f'<div class="vs-crumb">{esc(p.get("crumb", "work"))} {ui("c-chevron-right", 14, "#8A8A8A")} {esc(p.get("file", "utterances.txt"))}</div>'
          f'<div class="vs-code"><i class="rh" id="rh"></i>{body}</div></div></div>')
    cl = logo(ctx, 'claude', '#D97757')
    card = (f'<div class="rc" id="rc"><div class="rc-h"><span class="rc-av">{cl}</span><b>{esc(p.get("who", "Claude"))}</b></div>'
            f'<div class="rc-t">{rich(p["reason"])}</div></div>')
    html = (_titles(p) + '<div class="scene">' + ed + shadow(1405, 452, 230, 40) + tile3d('cl', 1430, 268, 180, cl, depth=24) + card + '</div>')
    css = ('.vs-top{position:relative;height:40px;background:#F8F8F8;border-bottom:1px solid #E5E5E5;display:flex;align-items:center;padding:0 16px;font:13px/1 UI;color:#3B3B3B}'
           '.vs-top span{position:absolute;left:0;right:0;text-align:center}'
           '.vs-act{position:absolute;left:0;top:40px;bottom:0;width:56px;background:#F8F8F8;border-right:1px solid #E5E5E5;display:flex;flex-direction:column;align-items:center;gap:26px;padding-top:16px}'
           '.vs-on{position:absolute;left:0;top:14px;width:3px;height:32px;background:#005FB8}'
           '.vs-main{position:absolute;left:56px;right:0;top:40px;bottom:0;background:#fff}'
           '.vs-tabs{height:38px;background:#F8F8F8;border-bottom:1px solid #E5E5E5;display:flex}'
           '.vs-tab{height:38px;display:flex;align-items:center;gap:8px;padding:0 14px;background:#fff;border-top:2px solid #005FB8;border-right:1px solid #E5E5E5;font:14px/1 UI;color:#1F1F1F}'
           '.vs-crumb{height:30px;display:flex;align-items:center;gap:4px;padding:0 18px;font:13px/1 UI;color:#6C6C6C}'
           f'.vs-code{{position:absolute;left:0;right:0;top:82px;bottom:0;padding-top:14px}}.ln{{position:relative;height:{LH}px;display:flex;align-items:center;overflow:hidden}}'
           '.gn{width:58px;text-align:right;padding-right:22px;font:500 17px Mono;color:#9AA0A6;flex:none}'
           ".cd{font:500 19px Mono;color:#2B2B2B;white-space:pre}.cd b{font-weight:500}.c-id{color:#0000FF}.c-t{color:#098658}.c-g{color:#A31515}"
           f'.rh{{position:absolute;left:0;right:0;top:14px;height:{LH}px;background:#E9EEFF;box-shadow:inset 3px 0 0 #7B6CFF;opacity:0}}'
           '.stk{position:absolute;left:58px;right:24px;top:50%;height:3px;margin-top:-1px;background:#E5484D;transform-origin:0 50%;transform:scaleX(0)}'
           '.rc{position:absolute;left:1290px;top:520px;width:520px;padding:24px 28px;border-radius:22px;background:#fff;border:1px solid var(--line);'
           'box-shadow:0 30px 60px -24px rgba(23,19,13,.42)}.rc-h{display:flex;align-items:center;gap:12px;font:700 22px BodyBold}'
           '.rc-av{width:38px;height:38px;border-radius:10px;background:#F5EEE6;display:grid;place-items:center}.rc-av svg{width:24px;height:24px}'
           '.rc-t{margin-top:14px;font:500 24px/1.5 Body;color:var(--soft)}')
    js = TITLES_IN + win_in('#ed', .1, ry=14, rx=6, to_ry=8, to_rx=4, end_ry=3, end_rx=3, D=D)
    js += f"tl.fromTo('.ln',{{opacity:0,x:-12}},{{opacity:1,x:0,duration:.28,stagger:.035,ease:'power2.out'}},.35);"
    js += "tl.to('#rh',{opacity:1,duration:.15},.75);"
    step = .9/max(1, first)
    for i in range(1, first+1):
        js += f"tl.set('#rh',{{y:{i*LH}}},{.75+i*step:.2f});"
    ts = .75 + .9 + .1
    js += f"tl.to('#rh',{{opacity:0,duration:.15}},{ts:.2f});"
    for i in dels:
        js += f"tl.to('#ln{i}',{{backgroundColor:'#FFE5E5',duration:.15}},{ts:.2f});tl.to('#sk{i}',{{scaleX:1,duration:.3,ease:'power2.out'}},{ts+.05:.2f});"
    js += enter3d('#cl', .45, ry=60, to_ry=14) + drift('#cl', 1.35, D, ry=-12) + floaty('#cl', 1.4, D)
    js += show('#rc', ts+.25, 24)
    tc = ts + 1.25
    for i in dels:
        js += f"tl.to('#ln{i}',{{height:0,opacity:0,duration:.4,ease:'power2.inOut'}},{tc:.2f});"
    sfx = [(0, 'whoosh', -17), (.45, 'pop', -18), (round(ts, 2), 'click', -15), (round(ts+.3, 2), 'pop', -19), (round(tc, 2), 'whoosh-short', -18)]
    return full(html, css, js, tc+.5, min(D-.2, ts+.9), sfx)


# ------------------------------------------------------------------ 4. components: exploded view of a real frame, overlay layer and its code, then merge

def sl_stack(o, ctx):
    """props: title, base (img spec: the real frame), layer (PNG with alpha: the real rendered overlay), code [lines], labels."""
    p = o['props']; D = ctx['D']
    labels = p.get('labels') or ['video gốc', 'component', 'code']
    code = ''.join(f'<div class="cl" id="cl{i}">{hl_code(l) or "&nbsp;"}</div>' for i, l in enumerate(p['code']))
    html = (_titles(p) + '<div class="scene"><div id="stk">'
            f'<div class="lyr" id="L0"><img class="lv" src="{ctx["img"](p["base"])}"><span class="lt" id="lt0">{esc(labels[0])}</span></div>'
            f'<div class="lyr ov" id="L1"><img src="{ctx["img"](p["layer"])}"><span class="lt" id="lt1">{esc(labels[1])}</span></div>'
            f'<div class="lyr cdl" id="L2"><div class="code-h">{TL3}<span>{esc(p.get("file", "ov-020.html"))}</span></div><div class="code">{code}</div>'
            f'<span class="lt" id="lt2">{esc(labels[2])}</span></div></div></div>')
    css = ('#stk{position:absolute;left:520px;top:330px;width:960px;height:540px;transform-style:preserve-3d}'
           '.lyr{position:absolute;inset:0;border-radius:18px;transform-style:preserve-3d}.lyr img{position:absolute;inset:0;width:100%;height:100%;border-radius:18px;display:block}'
           '.lv{box-shadow:0 0 0 1px rgba(23,19,13,.12),0 40px 80px -30px rgba(23,19,13,.55)}'
           '.ov{box-shadow:inset 0 0 0 3px rgba(123,108,255,.75);background:rgba(183,168,255,.07)}'
           '.cdl{left:-110px;top:30px;right:auto;bottom:auto;width:600px;height:330px;background:rgba(24,22,20,.9);border-radius:16px;'
           'box-shadow:0 0 0 1px rgba(0,0,0,.4),0 30px 60px -20px rgba(23,19,13,.6)}'
           '.code-h{position:relative;height:36px;display:flex;align-items:center;padding:0 14px;border-bottom:1px solid rgba(255,255,255,.08);font:13px/1 UI;color:#A9A39A}'
           '.code-h span{position:absolute;left:0;right:0;text-align:center}.code-h .tl3 i{width:11px;height:11px}'
           '.code{padding:14px 18px;font:500 16px/1.62 Mono;color:#D4D4D4;white-space:pre}'
           '.lt{position:absolute;left:0;top:-58px;padding:9px 20px;border-radius:999px;background:#fff;font:700 22px/1 BodyBold;color:var(--ink);'
           'box-shadow:0 10px 24px -10px rgba(23,19,13,.4);white-space:nowrap}#lt1{background:var(--plum);color:#fff}#lt2{background:#24211E;color:#F4F0EA}'
           '#lt0{top:auto;bottom:-58px;left:auto;right:0}#lt1{left:auto;right:0}#lt2{top:auto;bottom:-56px}')
    js = TITLES_IN + "tl.set('#stk',{rotationY:-30,rotationX:14},0);"
    js += "tl.fromTo('#L0',{opacity:0,y:80,z:0},{opacity:1,y:0,z:0,duration:.6,ease:'power3.out'},.1);"
    js += "tl.fromTo('#L1',{opacity:0,z:640},{opacity:1,z:190,duration:.65,ease:'power3.out'},.45);"
    js += "tl.fromTo('#L2',{opacity:0,z:860},{opacity:1,z:380,duration:.65,ease:'power3.out'},.8);"
    js += pop('#lt0', 1.0, .6) + pop('#lt1', 1.15, .6) + pop('#lt2', 1.3, .6)
    js += "tl.fromTo('.cl',{opacity:0,x:-10},{opacity:1,x:0,duration:.22,stagger:.09,ease:'power2.out'},1.05);"
    js += "tl.to('#stk',{rotationY:-22,rotationX:12,duration:1.9,ease:'sine.inOut'},1.1);"
    js += ("tl.to('#L2',{z:820,opacity:0,duration:.4,ease:'power2.in'},3.0);tl.to(['#lt0','#lt1'],{opacity:0,duration:.25},3.0);"
           "tl.to('#L1',{z:0,duration:.6,ease:'power3.inOut'},3.15);"
           "tl.to('#stk',{rotationY:0,rotationX:0,scale:1.12,duration:.8,ease:'power3.inOut'},3.15);tl.to('.ov',{boxShadow:'inset 0 0 0 0px rgba(123,108,255,0)',backgroundColor:'rgba(183,168,255,0)',duration:.4},3.5);")
    sfx = [(0, 'whoosh', -17), (.5, 'pop', -19), (.85, 'pop', -19), (1.3, 'typing', -21), (3.1, 'whoosh-short', -17), (3.95, 'sparkle', -19)]
    return full(html, css, js, 3.95, min(D-.2, 2.6), sfx)


# ------------------------------------------------------------------ 5. component library: real rendered components fan out

def sl_fan(o, ctx):
    """props: title, cards [{img, label}] x5: real frames of rendered components."""
    p = o['props']; D = ctx['D']
    cards = p['cards'][:5]
    xs, ys, rz, ry = [-600, -300, 0, 300, 600], [86, 22, 0, 22, 86], [-12, -6, 0, 6, 12], [16, 8, 0, -8, -16]
    order = [0, 4, 1, 3, 2]
    html = (_titles(p) + '<div class="scene">' + shadow(560, 850, 800, 110) + '<div id="fan">'
            + ''.join(f'<div class="fc5 vframe" id="c{k}"><img src="{ctx["img"](cards[k]["img"], 1100)}">'
                      f'<span class="chip">{esc(cards[k].get("label", ""))}</span></div>' for k in order) + '</div></div>')
    css = ('#fan{position:absolute;left:702px;top:384px;width:516px;height:297px;transform-style:preserve-3d}'
           '.fc5{inset:0;transform-style:preserve-3d}.fc5 .chip{left:14px;bottom:14px;top:auto}')
    js = TITLES_IN + "tl.fromTo('.fc5',{opacity:0,y:70,scale:.9},{opacity:1,y:0,scale:1,duration:.5,stagger:.06,ease:'power3.out'},.1);"
    for k in range(len(cards)):
        js += (f"tl.fromTo('#c{k}',{{x:0,y:0,rotation:0,rotationY:0}},{{x:{xs[k]},y:{ys[k]},rotation:{rz[k]},rotationY:{ry[k]},"
               f"duration:.85,ease:'back.out(1.2)',immediateRender:false}},.75);")
    js += f"tl.fromTo('#fan',{{rotationX:8}},{{rotationX:2,duration:{D:.2f},ease:'sine.inOut'}},0);" + floaty('#fan', 1.65, D, amp=-14, period=1.5)
    js += f"tl.fromTo('.fc5 img',{{scale:1}},{{scale:1.06,duration:{D:.2f},ease:'none'}},0);"
    return full(html, css, js, 1.65, min(D-.2, 2.1), [(0, 'whoosh', -17), (.75, 'whoosh-short', -16), (1.55, 'sparkle', -19)])


# ------------------------------------------------------------------ 6. AI edit: a real 3D MacBook opens, the plan types itself, the edit fills in

LAPTOP_MODULE = r"""
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { CSS3DRenderer, CSS3DObject } from 'three/addons/renderers/CSS3DRenderer.js';
const CFG = __CFG__;
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('gl'), alpha: true, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(1920, 1080, false); renderer.setPixelRatio(1); renderer.setClearColor(0x000000, 0);
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.outputColorSpace = THREE.SRGBColorSpace;
const css = new CSS3DRenderer({ element: document.getElementById('css3d') }); css.setSize(1920, 1080);
const scene = new THREE.Scene();
scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture;
const camera = new THREE.PerspectiveCamera(CFG.fov, 1920/1080, 0.1, 200);
camera.position.set(0, CFG.camY, CFG.camZ); camera.lookAt(0, CFG.lookY, 0); camera.updateMatrixWorld();
scene.add(new THREE.HemisphereLight(0xffffff, 0xe8e0ff, 0.7));
const key = new THREE.DirectionalLight(0xffffff, 1.4); key.position.set(4, 9, 7); scene.add(key);
const pivot = new THREE.Group(); scene.add(pivot);
const scr = document.getElementById('scr');
let hinge = null;
const clamp = x => Math.min(1, Math.max(0, x));
const ease = x => 1 - Math.pow(1 - clamp(x), 3);
function build() {
  const draco = new DRACOLoader().setDecoderPath('../assets/vendor/three/draco/');
  return new GLTFLoader().setDRACOLoader(draco).loadAsync(CFG.model).then(g => {
    const m = g.scene; const holder = new THREE.Group(); holder.add(m); pivot.add(holder);
    hinge = m.getObjectByName('screenflip');
    let screen = null; m.traverse(o => { if (o.isMesh && o.material && o.material.name === 'screen.001') screen = o; });
    screen.material = new THREE.MeshBasicMaterial({ color: 0x080808 });  // the GLB ships a desktop wallpaper there
    hinge.rotation.x = CFG.open; holder.updateMatrixWorld(true);
    const box = new THREE.Box3().setFromObject(holder); const size = box.getSize(new THREE.Vector3()); const c = box.getCenter(new THREE.Vector3());
    const s = CFG.width / size.x; holder.scale.setScalar(s);
    holder.position.set(-c.x * s, -box.min.y * s, -c.z * s); pivot.updateMatrixWorld(true);
    screen.geometry.computeBoundingBox(); const bb = screen.geometry.boundingBox;
    const ext = bb.getSize(new THREE.Vector3()); const ctr = bb.getCenter(new THREE.Vector3());
    const ax = ['x', 'y', 'z'].sort((p, q) => ext[p] - ext[q]);
    const mw = screen.matrixWorld; const m3 = new THREE.Matrix3().setFromMatrix4(mw);
    const dir = (a, len) => { const v = new THREE.Vector3(); v[a] = len; return v.applyMatrix3(m3); };
    let [u, v] = [ax[1], ax[2]];
    if (Math.abs(dir(u, 1).normalize().x) < Math.abs(dir(v, 1).normalize().x)) [u, v] = [v, u];
    const wW = dir(u, ext[u]).length(), wH = dir(v, ext[v]).length();
    const cW = ctr.clone().applyMatrix4(mw);
    const xw = dir(u, 1).normalize(); if (xw.x < 0) xw.negate();
    const zw = dir(ax[0], 1).normalize(); if (zw.dot(camera.position.clone().sub(cW)) < 0) zw.negate();
    const yw = new THREE.Vector3().crossVectors(zw, xw);
    const M = new THREE.Matrix4().makeBasis(xw, yw, zw).scale(new THREE.Vector3(wW * CFG.inset / CFG.px[0], wH * CFG.inset / CFG.px[1], 1))
      .setPosition(cW.addScaledVector(zw, 0.004 * CFG.width));
    const obj = new CSS3DObject(scr); new THREE.Matrix4().copy(mw).invert().multiply(M).decompose(obj.position, obj.quaternion, obj.scale);
    screen.add(obj);
  });
}
function renderAt(t) {
  if (!hinge) return;
  const k = ease((t - CFG.t0) / CFG.td);
  hinge.rotation.x = CFG.closed + (CFG.open - CFG.closed) * k;
  const q = clamp(t / CFG.D);
  pivot.rotation.y = CFG.ry0 + (CFG.ry1 - CFG.ry0) * (0.5 - 0.5 * Math.cos(Math.PI * q));
  pivot.rotation.x = CFG.rx; pivot.position.y = CFG.py + Math.sin(t * 1.3) * 0.04 * CFG.width;
  scr.style.opacity = clamp((k - 0.8) / 0.2);
  renderer.render(scene, camera); css.render(scene, camera);
}
const ready = build().then(() => { renderAt(window.__hfThreeTime || 0); window.__three_ok = true; });
window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {}; window.__hf.buildReady.scene3d = ready;
window.__ready3d = ready;
window.addEventListener('hf-seek', e => renderAt(e.detail.time));
"""


def sl_edit(o, ctx):
    """props: title, file (tab), json [[html-escaped-free text line, block index or -1]], blocks [{label, at, img}], duration
    (of the edited video, for block positions), strip [img specs] (timeline thumbnails), left/right logos, left_name/right_name."""
    p = o['props']; D = ctx['D']
    PX = (1440, 900)
    blocks = p['blocks']; vd = float(p.get('duration', 720))
    jl = ''.join(f'<div class="jl" id="jl{i}"><span class="jn">{i+1}</span><span class="jc">{hl_json(t)}</span></div>' for i, (t, _) in enumerate(p['json']))
    pv = ''.join(f'<img id="pv{i}" src="{ctx["img"](b["img"], 1280)}">' for i, b in enumerate(blocks))
    pv0 = f'<img id="pvb" src="{ctx["img"](p["base"], 1280)}">' if p.get('base') else ''
    strip = ''.join(f'<img src="{ctx["img"](s, 320)}">' for s in p['strip'])
    TLW = 1440 - 120 - 24
    obs = ''.join(f'<span class="ob" id="ob{i}" style="left:{b["at"]/vd*TLW:.0f}px;top:{2 + 36*(i % 2)}px;background:{b.get("color", "#7B6CFF")}">{esc(b["label"])}</span>' for i, b in enumerate(blocks))
    pk = ctx['wave'](p.get('wave_file') or ctx['video'], 0, vd, 300) if p.get('wave_file') else [0.3]*300
    wave = '<svg class="lx-wv" viewBox="0 0 %d 60" preserveAspectRatio="none"><path d="%s"/></svg>' % (
        TLW, ''.join(f'M{i*TLW/300:.1f},{30-v*26:.1f}V{30+v*26:.1f}' for i, v in enumerate(pk)))
    screen = (f'<div id="scr"><div class="lx"><div class="lx-top">{TL3}<span>{esc(p.get("file", "edit-plan.json"))} — {esc(p.get("project", "showroom-3d"))}</span></div>'
              f'<div class="lx-code">{jl}</div>'
              f'<div class="lx-pv"><div class="lx-pvh">{ui("m-play_arrow-fill", 20, "#CCCCCC")}<span>Preview</span></div><div class="lx-pvi">{pv0}{pv}</div></div>'
              f'<div class="lx-tl"><div class="lx-hd"><b>OV</b><b>V1</b><b>A1</b></div><div class="lx-tr">'
              f'<div class="lx-ov">{obs}</div><div class="lx-v">{strip}</div><div class="lx-a">{wave}</div><i id="ph"></i></div></div>'
              f'<i class="glare"></i></div></div>')
    a, b2 = logo(ctx, p.get('left', 'claude'), p.get('left_color', '#D97757')), logo(ctx, p.get('right', 'openai'), p.get('right_color', '#17130D'))
    html = (shadow(560, 900, 800, 90) + f'<div id="lpw"><canvas id="gl" width="1920" height="1080"></canvas><div id="css3d">{screen}</div></div>'
            + '<div class="scene">' + shadow(170, 600, 230, 40) + tile3d('ta', 190, 400, 190, a) + shadow(1520, 600, 230, 40) + tile3d('tb', 1540, 400, 190, b2) + '</div>'
            + f'<div class="lbl" id="na" style="left:135px;width:300px;top:650px">{esc(p.get("left_name", "Claude"))}</div>'
            + f'<div class="lbl" id="nb" style="left:1485px;width:300px;top:650px">{esc(p.get("right_name", "ChatGPT"))}</div>'
            + '<svg class="lnk" viewBox="0 0 1920 1080"><path id="la" d="M392 495 C470 495 500 450 600 450"/><path id="lb" d="M1528 495 C1450 495 1420 450 1320 450"/></svg>' + _titles(p))
    css = ('#lpw{position:absolute;inset:0}#gl,#css3d{position:absolute;left:0;top:0;width:1920px;height:1080px}'
           f'#scr{{width:{PX[0]}px;height:{PX[1]}px;opacity:0;backface-visibility:hidden}}'
           '.lx{position:absolute;inset:0;background:#1F1F1F;overflow:hidden;font-family:UI;color:#CCCCCC}'
           '.lx-top{position:relative;height:38px;background:#181818;border-bottom:1px solid #2B2B2B;display:flex;align-items:center;padding:0 14px;font:14px/1 UI;color:#9D9D9D}'
           '.lx-top span{position:absolute;left:0;right:0;text-align:center}'
           '.lx-code{position:absolute;left:0;top:38px;width:620px;height:500px;padding:16px 0;background:#1F1F1F;border-right:1px solid #2B2B2B}'
           '.jl{display:flex;height:31px;align-items:center;font:500 18px Mono;color:#D4D4D4;white-space:pre;opacity:0}.jn{width:52px;text-align:right;padding-right:18px;color:#6E7681;flex:none}.jc{white-space:pre}'
           '.lx-pv{position:absolute;left:620px;right:0;top:38px;height:500px;background:#181818;padding:12px 24px}'
           '.lx-pvh{display:flex;align-items:center;gap:8px;height:30px;font:600 15px UIB;color:#CCCCCC}'
           '.lx-pvi{position:relative;width:772px;height:434px;margin-top:10px;border-radius:8px;overflow:hidden;background:#000}.lx-pvi img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}'
           '.lx-tl{position:absolute;left:0;right:0;top:538px;bottom:0;background:#181818;border-top:1px solid #2B2B2B}'
           '.lx-hd{position:absolute;left:0;top:18px;width:120px;display:flex;flex-direction:column;gap:12px}.lx-hd b{height:70px;display:flex;align-items:center;padding-left:26px;font:600 15px UIB;color:#9D9D9D}'
           '.lx-hd b+b{height:124px}.lx-hd b+b+b{height:84px}'
           '.lx-tr{position:absolute;left:120px;right:24px;top:18px;bottom:16px}'
           '.lx-ov{position:relative;height:70px}.ob{position:absolute;height:32px;padding:0 14px;border-radius:7px;font:600 15px/32px UIB;color:#fff;white-space:nowrap;'
           'box-shadow:inset 0 0 0 2px rgba(255,255,255,.25);opacity:0}'
           '.lx-v{display:flex;height:124px;margin-top:12px;border-radius:8px;overflow:hidden;box-shadow:inset 0 0 0 2px #7366F0}.lx-v img{height:100%;flex:1;min-width:0;object-fit:cover}'
           '.lx-a{height:84px;margin-top:12px;border-radius:8px;background:#173A2B;box-shadow:inset 0 0 0 2px #2F9E6E;overflow:hidden}.lx-wv{width:100%;height:100%}.lx-wv path{stroke:#4FE0A0;stroke-width:2.2}'
           '#ph{position:absolute;left:0;top:-6px;bottom:-6px;width:3px;background:#F2F2F2;box-shadow:0 0 10px rgba(255,255,255,.6)}'
           '.glare{position:absolute;inset:0;background:linear-gradient(118deg,rgba(255,255,255,.10),rgba(255,255,255,0) 38%);pointer-events:none}')
    cfg = dict(model=ctx['model'](p.get('model') or str(R/'assets'/'models'/'macbook.glb')), px=PX, inset=.972, width=10.0, fov=26,
               camY=float(p.get('camY', 16)), camZ=float(p.get('camZ', 30)), lookY=float(p.get('lookY', 1.45)),
               closed=1.52, open=float(p.get('open', -.30)), t0=.12, td=.85, ry0=-.28, ry1=.22, rx=float(p.get('rx', 0)), py=float(p.get('py', -1.2)), D=D)
    module = LAPTOP_MODULE.replace('__CFG__', json.dumps(cfg))
    js = TITLES_IN + "tl.fromTo('#lpw',{opacity:0,y:60},{opacity:1,y:0,duration:.6,ease:'power3.out'},.05);"
    js += enter3d('#ta', .45, ry=-60, to_ry=-14) + enter3d('#tb', .55, ry=60, to_ry=14) + drift('#ta', 1.35, D, ry=10) + drift('#tb', 1.45, D, ry=-10)
    js += show('#na', .8) + show('#nb', .9) + "tl.fromTo(['#la','#lb'],{opacity:0},{opacity:1,duration:.4},1.0);"
    t = 1.05; step = min(.16, (D - 1.6 - t)/max(1, len(p['json'])))
    sfx = [(0, 'whoosh', -17), (.5, 'pop', -18), (1.1, 'typing', -21)]
    done = {}
    for i, (_, blk) in enumerate(p['json']):
        js += f"tl.set('#jl{i}',{{opacity:1}},{t:.2f});"
        if blk >= 0:
            done[blk] = t
        t += step
    for i in range(len(blocks)):
        tb = done.get(i, t) + .05
        js += f"tl.fromTo('#pv{i}',{{opacity:0}},{{opacity:1,duration:.25}},{tb:.2f});" + pop(f'#ob{i}', tb, .6)
        sfx.append((round(tb, 2), 'click-soft', -16))
    js += f"tl.fromTo('#ph',{{x:0}},{{x:{TLW},duration:{D-1.1:.2f},ease:'none'}},1.1);"
    end = max(done.values() or [t]) + .5
    return full(html, css, js, end, min(D-.2, end+.2), sfx, module=module)


# ------------------------------------------------------------------ 7. Claude Code in a terminal: the real session, mascot on top

def sl_terminal(o, ctx):
    """props: title, cwd, prompt, steps [[kind, text, result]]: kind tool|say; model."""
    p = o['props']; D = ctx['D']
    prompt = p['prompt']; steps = p['steps']
    head = (f'<div class="cc-box" id="cb"><b class="cc-o">✻</b> <b class="cc-b">Welcome to Claude Code!</b>\n\n'
            f'  <span class="cc-d">/help for help, /status for your current setup</span>\n\n  <span class="cc-d">cwd: {esc(p.get("cwd", "~"))}</span></div>')
    body = head + f'<div class="tl" id="tp"><span class="cc-d">&gt;</span> <span class="ty" id="ty">{esc(prompt)}</span><i id="cur"></i></div>'
    for k, (kind, txt, res) in enumerate(steps):
        if kind == 'tool':
            body += f'<div class="tl" id="s{k}"><b class="cc-g">●</b> <b class="cc-b">{esc(txt)}</b></div>'
            if res:
                body += f'<div class="tl" id="r{k}"><span class="cc-d">  ⎿  {esc(res)}</span></div>'
        else:
            body += f'<div class="tl" id="s{k}"><b class="cc-w">●</b> <span class="cc-w">{rich(txt)}</span></div>'
    body += f'<div class="tl" id="spin"><b class="cc-o" id="sst">✻</b> <span class="cc-o">{esc(p.get("thinking", "Đang làm…"))}</span> <span class="cc-d">(esc to interrupt)</span></div>'
    W, H, X0, Y0 = 1240, 640, 340, 300
    html = (_titles(p) + '<div class="scene">' + shadow(420, Y0+H-20, 1080, 90)
            + term('tm', X0, Y0, W, H, p.get('bar', 'claude — edit-long'), body) + mascot('m', X0+W-150, Y0+4, .34) + '</div>')
    css = ('.tl{opacity:0}.cc-box{display:block;margin-bottom:18px;padding:14px 22px;border:2px solid #D97757;border-radius:12px;width:max-content;min-width:760px;line-height:1.35}'
           '.ty{display:inline-block;overflow:hidden;vertical-align:bottom;width:0;color:#F4F0EA}'
           '#cur{display:inline-block;width:12px;height:26px;background:#E9E4DC;vertical-align:-5px;margin-left:4px}'
           '#tm .tm-body{line-height:1.5}')
    js = TITLES_IN + win_in('#tm', .1, ry=12, rx=6, to_ry=6, to_rx=4, end_ry=-5, end_rx=3, D=D)
    js += "tl.fromTo('#cb',{opacity:0},{opacity:1,duration:.3},.3);tl.set('#tp',{opacity:1},.5);" + typed('#ty', len(prompt), .55, 30)
    t = .55 + len(prompt)/30 + .2
    js += f"tl.set('#cur',{{opacity:0}},{t:.2f});tl.set('#spin',{{opacity:1}},{t:.2f});"
    k_spin = t
    sfx = [(0, 'whoosh', -17), (.45, 'pop', -19), (.6, 'typing', -20)]
    gap = (D - .7 - t)/max(1, len(steps))
    for k, (kind, txt, res) in enumerate(steps):
        t += gap
        js += f"tl.set('#s{k}',{{opacity:1}},{t:.2f});"
        if kind == 'tool' and res:
            js += f"tl.set('#r{k}',{{opacity:1}},{t+gap*.45:.2f});"
        sfx.append((round(t, 2), 'click-soft' if kind == 'tool' else 'ping', -18 if kind == 'tool' else -16))
    js += f"tl.set('#spin',{{opacity:0}},{t:.2f});"
    rot = k_spin
    while rot < t:
        js += f"tl.fromTo('#sst',{{rotation:0}},{{rotation:180,duration:.4,ease:'none',immediateRender:false}},{rot:.2f});"; rot += .4
    js += pop('#m', .5, .5) + sway('m', .5, D) + hop('m', k_spin, 0, 0, 80, .45) + hop('m', (k_spin+t)/2, 0, 0, 80, .45)
    return full(html, css, js, t, min(D-.15, t+.1), sfx)


# ------------------------------------------------------------------ 8. approve the samples: the real gallery page, "duyệt" typed in Claude Code, ticks

def sl_approve(o, ctx):
    """props: title, page (the real review/index.html), url, tab, reply (what the user types), done (Claude's answer)."""
    p = o['props']; D = ctx['D']
    WX, WY, W, H = 210, 240, 1500, 760
    sh = ctx['shot'](p['page'], w=W, h=H-90, sel=p.get('sel', 'article img'), max_h=3000)
    boxes = sh['boxes']; scroll = max(0, min(sh['h'] - (H-90), (boxes[0][1] - 40) if boxes else 0))
    vis = [b for b in boxes if b[1] - scroll > -20 and b[1] + b[3] - scroll < H - 90 + 40][:9]
    ticks = ''.join(f'<span class="tk" id="tk{i}" style="left:{bx+bw-56}px;top:{by+14}px">{ui("m-check_circle-fill", 44, "#22A559")}</span>' for i, (bx, by, bw, bh) in enumerate(vis))
    page = f'<div id="pg"><img src="{sh["src"]}" style="width:{sh["w"]}px">{ticks}</div>'
    win = chrome('ap', WX, WY, W, H, p.get('url', 'review/index.html'), page, p.get('tab', 'Duyệt mẫu'))
    cc = (f'<div class="mw dk" id="cc"><div class="cc-in"><span class="cc-d">&gt;</span> <span class="ty" id="ty">{esc(p.get("reply", "duyệt"))}</span></div>'
          f'<div class="cc-out" id="co"><b class="cc-g">●</b> <span class="cc-w">{esc(p.get("done", "Đã duyệt. Bắt đầu render video."))}</span></div></div>')
    tx, ty = 900, 600
    if vis:
        bx, by, bw, bh = vis[min(4, len(vis)-1)]
        tx, ty = WX + bx + bw*.6, WY + 90 + by - scroll + bh*.55
    html = _titles(p) + '<div class="scene">' + win + '</div>' + cc + cursor('cu', 1180, 520, 62)
    css = ('#pg{position:absolute;left:0;top:0}#pg img{display:block}.tk{position:absolute;width:44px;height:44px;border-radius:50%;background:#fff;'
           'box-shadow:0 6px 14px -4px rgba(0,0,0,.35);transform:scale(0)}'
           '#cc{left:1180px;top:820px;width:600px;height:150px;padding:26px 30px;font:500 24px/1.6 Mono;color:#E9E4DC;white-space:pre}'
           '.ty{display:inline-block;overflow:hidden;vertical-align:bottom;width:0;color:#F4F0EA}.cc-out{opacity:0}')
    js = TITLES_IN + win_in('#ap', .1, ry=-10, rx=6, to_ry=-4, to_rx=3, end_ry=4, end_rx=2, D=D)
    js += f"tl.fromTo('#pg',{{y:0}},{{y:{-scroll},duration:1.1,ease:'power2.inOut'}},.7);"
    js += f"tl.fromTo('#cu',{{x:0,y:0,opacity:0}},{{x:{tx-1180:.0f},y:{ty-520:.0f},opacity:1,duration:1.0,ease:'power2.inOut'}},.8);"
    js += "tl.fromTo('#cc',{opacity:0,y:40},{opacity:1,y:0,duration:.45,ease:'power3.out'},1.85);" + typed('#ty', len(p.get('reply', 'duyệt')), 2.25, 12)
    t = 2.25 + len(p.get('reply', 'duyệt'))/12 + .1
    js += ''.join(f"tl.to('#tk{i}',{{scale:1,duration:.3,ease:'back.out(2.2)'}},{t+.08*i:.2f});" for i in range(len(vis)))
    js += f"tl.to('#co',{{opacity:1,duration:.2}},{t+.08*len(vis)+.1:.2f});"
    sfx = [(0, 'whoosh', -17), (2.3, 'typing', -20), (round(t, 2), 'pop', -18), (round(t+.4, 2), 'pop', -19), (round(t+.08*len(vis)+.1, 2), 'chime', -16)]
    end = t + .08*len(vis) + .4
    return full(html, css, js, end, min(D-.2, end), sfx)


# ------------------------------------------------------------------ 9. render: the real render log runs, real frames of the final video stack up, then it plays

def sl_render(o, ctx):
    """props: title, log [[kind, text]] (cmd|out|ok|bar), frames [img specs of the finished video], clip [file, start], name."""
    p = o['props']; D = ctx['D']
    lines = p['log']
    body = ''
    for k, (kind, txt) in enumerate(lines):
        if kind == 'cmd':
            body += f'<div class="tl" id="l{k}"><span class="cc-o">$</span> <span class="cc-w">{esc(txt)}</span></div>'
        elif kind == 'ok':
            body += f'<div class="tl" id="l{k}"><b class="cc-g">✓</b> <span class="cc-w">{esc(txt)}</span></div>'
        elif kind == 'bar':
            body += f'<div class="tl" id="l{k}"><span class="pb"><i id="pbf"></i></span> <span class="cc-d">{esc(txt)}</span></div>'
        else:
            body += f'<div class="tl" id="l{k}"><span class="cc-d">{esc(txt)}</span></div>'
    fr = p['frames'][:8]
    GX, GY, gw, gh = 1010, 300, 200, 113
    frames = ''.join(f'<div class="vframe fr" id="f{k}" style="left:{GX + (k % 4)*(gw+16)}px;top:{GY + (k//4)*(gh+16)}px;width:{gw}px;height:{gh}px">'
                     f'<img src="{ctx["img"](s, 400)}"></div>' for k, s in enumerate(fr))
    cf, cs = p['clip']
    vid = f'<video src="{ctx["vclip"](cf, float(cs))}" data-start="0" data-duration="{D}" muted playsinline></video>'
    player = (f'<div class="vframe" id="pl" style="left:{GX}px;top:{GY}px;width:{4*gw+48}px;height:{round((4*gw+48)*9/16)}px">{vid}'
              f'<span class="chip" id="nm" style="left:16px;top:16px">{esc(p.get("name", "final.mp4"))}</span></div>')
    html = (_titles(p) + '<div class="scene">' + shadow(160, 860, 760, 80) + term('tm', 110, 300, 840, 560, p.get('bar', 'render — edit-long'), body)
            + player + frames + '</div>')
    css = ('.tl{opacity:0}#tm .tm-body{font-size:19px;line-height:1.75}.pb{display:inline-block;width:300px;height:16px;border-radius:4px;background:rgba(255,255,255,.12);vertical-align:-1px;overflow:hidden}'
           '#pbf{display:block;height:100%;width:100%;background:#D97757;transform-origin:0 50%;transform:scaleX(0)}'
           '.fr{border-width:4px;border-radius:10px}#pl{opacity:0}')
    js = TITLES_IN + win_in('#tm', .1, ry=14, rx=5, to_ry=8, to_rx=3, end_ry=2, end_rx=2, D=D)
    t = .45; gap = 2.4/max(1, len(lines))
    sfx = [(0, 'whoosh', -17)]
    for k, (kind, _) in enumerate(lines):
        js += f"tl.set('#l{k}',{{opacity:1}},{t:.2f});"
        if kind == 'bar':
            js += f"tl.to('#pbf',{{scaleX:1,duration:{gap*2.2:.2f},ease:'power1.inOut'}},{t:.2f});"
        t += gap
    for k in range(len(fr)):
        tk = .6 + k*.27
        js += (f"tl.fromTo('#f{k}',{{opacity:0,x:{-260 - (k % 4)*80},y:{120 - (k//4)*60},scale:.4,rotation:{-10 if k % 2 else 8}}},"
               f"{{opacity:1,x:0,y:0,scale:1,rotation:0,duration:.5,ease:'power3.out'}},{tk:.2f});")
        if k % 2 == 0:
            sfx.append((round(tk, 2), 'click-soft', -17))
    tp = max(t, .6 + len(fr)*.27 + .3)
    js += f"tl.to('.fr',{{opacity:0,scale:.9,duration:.3,stagger:.03,ease:'power2.in'}},{tp:.2f});"
    js += f"tl.fromTo('#pl',{{opacity:0,scale:.92}},{{opacity:1,scale:1,duration:.45,ease:'power3.out'}},{tp+.25:.2f});" + pop('#nm', tp+.55)
    sfx += [(round(tp+.25, 2), 'whoosh-short', -17), (round(tp+.6, 2), 'sparkle', -18)]
    return full(html, css, js, tp+.7, min(D-.15, tp+.9), sfx)


# ------------------------------------------------------------------ 10. publish: a real YouTube watch page with the finished video playing

def sl_publish(o, ctx):
    """props: title, clip [file, start], video_title, channel, subs, avatar (img), chapters [[mm:ss, title, img]], views."""
    p = o['props']; D = ctx['D']
    WX, WY, W, H = 150, 200, 1620, 820
    cf, cs = p['clip']
    vid = f'<video src="{ctx["vclip"](cf, float(cs))}" data-start="0" data-duration="{D}" muted playsinline></video>'
    g = '#0F0F0F'; wt = '#FFFFFF'
    ctrl = (f'<div class="yt-ctl"><div class="yt-prog"><i class="yt-pl" id="yp"></i><i class="yt-dot" id="yd"></i></div>'
            f'<div class="yt-row">{ui("m-pause-fill", 34, wt)}{ui("m-skip_next-fill", 32, wt)}{ui("m-volume_up-fill", 30, wt)}'
            f'<span class="yt-time">{esc(p.get("time", "0:12 / 11:59"))}</span><span class="yt-ch">• {esc(p["chapters"][int(p.get("now", 0))][1] if p.get("chapters") else "")}</span>'
            f'<i style="flex:1"></i>{ui("m-closed_caption", 30, wt)}{ui("m-settings", 30, wt)}{ui("m-fullscreen", 32, wt)}</div></div>')
    av = ctx['img'](p['avatar'], 160) if p.get('avatar') else ''
    chap = ''.join(f'<div class="yt-c" id="yc{i}"><img src="{ctx["img"](im, 320)}"><div><b>{esc(tt)}</b><span>{esc(ts)}</span></div></div>'
                   for i, (ts, tt, im) in enumerate(p.get('chapters', [])))
    page = (f'<div class="yt"><div class="yt-hd">{ui("m-menu", 26, g)}<span class="yt-logo">{logo(ctx, "youtube", "#FF0000")}<b>YouTube</b></span>'
            f'<div class="yt-sr"><span>{esc(p.get("search", ""))}</span><i>{ui("m-search", 24, g)}</i></div><span class="yt-mic">{ui("m-mic-fill", 22, g)}</span>'
            f'<i style="flex:1"></i>{ui("m-video_call", 28, g)}{ui("m-notifications", 28, g)}<span class="yt-me" style="background-image:url({av})"></span></div>'
            f'<div class="yt-main"><div class="yt-pv">{vid}{ctrl}</div>'
            f'<div class="yt-t">{esc(p.get("video_title", ""))}</div>'
            f'<div class="yt-own"><span class="yt-av" style="background-image:url({av})"></span><div class="yt-cn"><b>{esc(p.get("channel", ""))}</b><span>{esc(p.get("subs", ""))}</span></div>'
            f'<span class="yt-sub" id="ys">Đăng ký</span><i style="flex:1"></i><span class="yt-btn">{ui("m-thumb_up", 22, g)}<b>{esc(p.get("likes", ""))}</b><em></em>{ui("m-thumb_down", 22, g)}</span>'
            f'<span class="yt-btn">{ui("m-share", 22, g)}<b>Chia sẻ</b></span><span class="yt-btn">{ui("m-more_horiz", 22, g)}</span></div></div>'
            f'<div class="yt-side"><div class="yt-sh">Chương</div>{chap}</div></div>')
    win = chrome('yt', WX, WY, W, H, p.get('url', 'youtube.com/watch'), page, p.get('video_title', 'YouTube'), f'<span class="fav">{logo(ctx, "youtube", "#FF0000")}</span>')
    html = (_titles(p) + '<div class="scene">' + win + shadow(1640, 990, 220, 40) + tile3d('ytt', 1660, 800, 180, logo(ctx, 'youtube', '#FF0000'), depth=26) + '</div>'
            + cursor('cu', 760, 1000, 58, 'hand'))
    css = ('.fav svg{width:16px;height:16px;display:block}.yt{position:absolute;inset:0;background:#fff;font-family:YT;color:#0F0F0F}'
           '.yt-hd{height:56px;display:flex;align-items:center;gap:22px;padding:0 22px}.yt-logo{display:flex;align-items:center;gap:3px;margin-left:4px}.yt-logo svg{width:34px;height:24px}'
           '.yt-logo b{font:700 22px/1 YTM;letter-spacing:-1.2px}'
           '.yt-sr{margin-left:150px;width:520px;height:40px;border:1px solid #D3D3D3;border-radius:20px;display:flex;align-items:center;overflow:hidden;font:16px YT;color:#606060}'
           '.yt-sr span{flex:1;padding:0 16px}.yt-sr i{width:64px;height:100%;display:grid;place-items:center;background:#F8F8F8;border-left:1px solid #D3D3D3}'
           '.yt-mic{width:40px;height:40px;border-radius:50%;background:#F2F2F2;display:grid;place-items:center;margin-left:-10px}'
           '.yt-me,.yt-av{border-radius:50%;background:#ddd center/cover;flex:none}.yt-me{width:34px;height:34px}'
           '.yt-main{position:absolute;left:24px;top:64px;width:1000px}.yt-pv{position:relative;width:1000px;height:562px;border-radius:12px;overflow:hidden;background:#000}'
           '.yt-pv video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}'
           '.yt-ctl{position:absolute;left:0;right:0;bottom:0;height:110px;padding:0 18px;background:linear-gradient(transparent,rgba(0,0,0,.65))}'
           '.yt-prog{position:absolute;left:18px;right:18px;bottom:62px;height:5px;background:rgba(255,255,255,.3)}.yt-pl{position:absolute;left:0;top:0;bottom:0;width:100%;background:#FF0033;transform-origin:0 50%}'
           '.yt-dot{position:absolute;top:-5px;left:0;width:15px;height:15px;border-radius:50%;background:#FF0033;margin-left:-7px}'
           '.yt-row{position:absolute;left:18px;right:18px;bottom:12px;height:44px;display:flex;align-items:center;gap:22px;color:#fff}'
           '.yt-time{font:16px YT;color:#fff}.yt-ch{font:500 16px YTM;color:#fff;margin-left:-8px}'
           '.yt-t{margin-top:14px;font:700 24px/1.3 YTM;white-space:nowrap;overflow:hidden}'
           '.yt-own{display:flex;align-items:center;gap:14px;margin-top:12px}.yt-av{width:44px;height:44px}.yt-cn b{display:block;font:500 17px YTM}.yt-cn span{font:13px YT;color:#606060}'
           '.yt-sub{margin-left:12px;height:38px;padding:0 18px;border-radius:19px;background:#0F0F0F;color:#fff;font:500 15px/38px YTM}'
           '.yt-btn{display:flex;align-items:center;gap:8px;height:38px;padding:0 16px;border-radius:19px;background:#F2F2F2;font:500 15px YTM}.yt-btn em{width:1px;height:24px;background:#CFCFCF}'
           '.yt-side{position:absolute;left:1050px;right:24px;top:64px}.yt-sh{font:700 20px YTM;margin-bottom:12px}'
           '.yt-c{display:flex;gap:12px;padding:8px;border-radius:12px;margin-bottom:6px}.yt-c img{width:168px;height:94px;border-radius:8px;object-fit:cover;flex:none}'
           '.yt-c b{display:block;font:500 16px/1.35 YTM}.yt-c span{display:inline-block;margin-top:8px;padding:2px 8px;border-radius:4px;background:#E5F0FF;color:#065FD4;font:500 13px YTM}')
    js = TITLES_IN + win_in('#yt', .1, ry=-10, rx=6, to_ry=-4, to_rx=3, end_ry=4, end_rx=2, D=D)
    pr = float(p.get('progress', .05)); PW = 1000 - 36
    js += f"tl.fromTo('#yp',{{scaleX:{pr:.4f}}},{{scaleX:{pr + D/720:.4f},duration:{D:.2f},ease:'none'}},0);tl.fromTo('#yd',{{x:{pr*PW:.0f}}},{{x:{(pr + D/720)*PW:.0f},duration:{D:.2f},ease:'none'}},0);"
    js += "tl.fromTo('.yt-c',{opacity:0,x:20},{opacity:1,x:0,duration:.3,stagger:.08,ease:'power2.out'},.6);"
    js += enter3d('#ytt', .9, spin=True, dur=1.1, to_ry=-14) + drift('#ytt', 2.0, D, ry=14) + floaty('#ytt', 2.0, D)
    sub_x, sub_y = WX + 24 + 44 + 14 + 130 + 12 + 46, WY + 90 + 64 + 562 + 14 + 31 + 12 + 19
    js += f"tl.fromTo('#cu',{{x:0,y:0,opacity:0}},{{x:{sub_x-760},y:{sub_y-1000},opacity:1,duration:.9,ease:'power2.inOut'}},1.6);"
    js += ("tl.to('#ys',{scale:.92,duration:.08},2.55);tl.to('#ys',{scale:1,backgroundColor:'#F2F2F2',color:'#0F0F0F',duration:.2},2.63);"
           "tl.set('#ys',{innerText:'Đã đăng ký'},2.63);")
    sfx = [(0, 'whoosh', -17), (.9, 'whoosh-cinematic', -18), (2.55, 'click', -15), (2.9, 'sparkle', -18)]
    return full(html, css, js, 2.9, min(D-.2, 3.2), sfx)


SLIDES = {'sl-system': sl_system, 'sl-cut': sl_cut, 'sl-transcript': sl_transcript, 'sl-stack': sl_stack, 'sl-fan': sl_fan,
          'sl-edit': sl_edit, 'sl-terminal': sl_terminal, 'sl-approve': sl_approve, 'sl-render': sl_render, 'sl-publish': sl_publish}
