# Talking-head templates (Ben AI style) for footage where the creator faces the camera: the frame slides left or right
# to make room, a dark blurred copy of the shot fills the space, text and real visuals (screenshots, sped-up source
# clips, thumbnails) come in on the free side, then everything returns so the cut back to the raw shot is invisible.
# Full-frame types embed the same seconds of the source video (frame exact, the original audio keeps playing under
# them). Text-only types are transparent overlays. Same return dict as components.py.
from components import esc, rich
from slides import KIT, tile3d, logo, pop, show

DARK = """
.fv,.fb{position:absolute;left:0;top:0;width:1920px;height:1080px}.fb,.fv.clip{overflow:hidden}
.fv video,.fb video{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover}
.fb{transform:scale(1.08)}.blk{position:absolute;inset:0;background:#07060A}
.fv.fadeR{--fade:0px;-webkit-mask-image:linear-gradient(90deg,#000 calc(100% - var(--fade)),transparent);mask-image:linear-gradient(90deg,#000 calc(100% - var(--fade)),transparent)}
.fv.fadeL{--fade:0px;-webkit-mask-image:linear-gradient(270deg,#000 calc(100% - var(--fade)),transparent);mask-image:linear-gradient(270deg,#000 calc(100% - var(--fade)),transparent)}
.tw{position:absolute;color:#fff;font-family:BodyBold;text-shadow:0 4px 30px rgba(0,0,0,.45)}
.tw em.acc{color:#A99BFF}.tw .l1{font-size:70px;line-height:1.08;letter-spacing:-.01em}.tw .l2{font-size:34px;color:rgba(255,255,255,.8);margin-top:14px;font-family:Body}
.dcard{position:absolute;border-radius:18px;overflow:hidden;background:#111;box-shadow:0 0 0 1px rgba(255,255,255,.14),0 40px 90px -20px rgba(0,0,0,.8)}
.dcard img,.dcard video{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover}
.badge{position:absolute;padding:8px 16px;border-radius:999px;background:rgba(10,9,14,.78);color:#fff;font:600 20px/1 UIB;border:1px solid rgba(255,255,255,.18);white-space:nowrap}
.dpill{position:absolute;padding:18px 34px;border-radius:999px;background:rgba(12,11,18,.86);border:1px solid rgba(255,255,255,.16);color:#fff;font-family:BodyBold;
 font-size:44px;white-space:nowrap;box-shadow:0 30px 60px -20px rgba(0,0,0,.8)}.dpill em.acc{color:#A99BFF}
"""


def face(ctx, fid='fv', extra='', cls=''):
    """The same seconds of the source video, frame exact (speed 1): ctx F is the overlay's first frame in the composite."""
    return (f'<div class="fv {cls}" id="{fid}"><video src="{ctx["vclip"](ctx["video"], ctx["F"]/30)}" data-start="0" data-duration="{ctx["D"]}" muted playsinline></video>'
            f'{extra}</div>')


def blurred(ctx, bid='fb'):
    """A soft, low-res blurred copy of the same seconds (cheap: blurred by ffmpeg at 480 px, upscaled by the browser)."""
    return (f'<div class="fb" id="{bid}"><video src="{ctx["vclip"](ctx["video"], ctx["F"]/30, w=480, vf="boxblur=10:2")}" data-start="0" '
            f'data-duration="{ctx["D"]}" muted playsinline></video></div>')


def lines(p, cls='tw', style=''):
    l2 = f'<div class="l2" id="tl2">{rich(p["sub"])}</div>' if p.get('sub') else ''
    return f'<div class="{cls}" id="tx" style="{style}"><div class="l1" id="tl1">{rich(p["text"])}</div>{l2}</div>'


def full(html, css, js, enter, hero, sfx):
    return dict(html=html, css=KIT + DARK + css, js=js, enter=enter, exit=0, hero=hero, sfx=sfx, full=True)


def text_in(t):
    return (f"tl.fromTo('#tl1',{{opacity:0,y:26,filter:'blur(10px)'}},{{opacity:1,y:0,filter:'blur(0px)',duration:.45,ease:'power3.out'}},{t:.2f});"
            f"tl.fromTo('#tl2',{{opacity:0,y:16}},{{opacity:1,y:0,duration:.4,ease:'power3.out'}},{t+.12:.2f});")


def shift(D, dx=-440, t0=.05, dur=.7):
    """Frame slides aside, its inner edge fades (CSS mask) into a dark blurred copy of the shot; all back at the end, so the
    first and last frames equal the raw shot and the cuts are invisible."""
    back = max(t0 + dur + .3, D - dur - .02)
    return (f"tl.fromTo('#fv',{{x:0,'--fade':'0px'}},{{x:{dx},'--fade':'340px',duration:{dur},ease:'power3.inOut'}},{t0:.2f});"
            f"tl.to('#fv',{{x:0,'--fade':'0px',duration:{dur},ease:'power3.inOut'}},{back:.2f});"
            f"tl.fromTo('#fb',{{opacity:0}},{{opacity:1,duration:{dur*.8:.2f},ease:'power2.out'}},{t0:.2f});"
            f"tl.fromTo('#bk',{{opacity:0}},{{opacity:.62,duration:{dur*.8:.2f},ease:'power2.out'}},{t0:.2f});"
            f"tl.to(['#fb','#bk'],{{opacity:0,duration:{dur*.8:.2f},ease:'power2.in'}},{back+dur*.2:.2f});"), back


# ------------------------------------------------------------------ transparent overlays (the shot stays as it is)

def th_text(o, ctx):
    """Big 2-line text on one side (same place as th-side's card, x 1200 / 110); the frame slides the face 300 px to the OTHER
    side and a dark gradient reaches from the text side up to the face edge, so there is no bright gap between them
    (Ben "Claude Motion" card, user rule 16/10/2026). Optional 3D logo tile above. props: text, sub, side (right|left), logo + logo_color, or logos [[slug, color], ...]."""
    p = o['props']; D = ctx['D']; side = p.get('side', 'right')
    dx = -300 if side == 'right' else 300
    x = 1200 if side == 'right' else 110
    grad = f"linear-gradient({'270deg' if side == 'right' else '90deg'},rgba(7,6,10,.84),rgba(7,6,10,.72) 30%,rgba(7,6,10,.42) 45%,rgba(7,6,10,0) 56%)"
    tiles = p.get('logos') or ([[p['logo'], p.get('logo_color', '#14A800')]] if p.get('logo') else [])
    size = 150 if len(tiles) == 1 else 116
    tile = ''.join(tile3d(f'lg{k}', x + k*(size+26), 270 + (150-size), size, logo(ctx, sl, col), depth=16, n=8) for k, (sl, col) in enumerate(tiles))
    html = (blurred(ctx) + '<div class="blk" id="bk" style="opacity:.55"></div>' + face(ctx, cls='fadeR' if side == 'right' else 'fadeL')
            + f'<div class="gr deco" id="gr" style="position:absolute;inset:0;background:{grad}"></div>'
            + f'<div class="scene">{tile}</div>' + lines(p, style=f'left:{x}px;top:{460 if tiles else 400}px;width:640px'))
    js, back = shift(D, dx)
    js += ("tl.fromTo('#gr',{opacity:0},{opacity:1,duration:.5,ease:'power2.out'},.05);"
           f"tl.to('#gr',{{opacity:0,duration:.5,ease:'power2.in'}},{back:.2f});") + text_in(.3)
    for k in range(len(tiles)):
        js += (f"tl.fromTo('#lg{k}',{{opacity:0,scale:.5,rotationY:-60}},{{opacity:1,scale:1,rotationY:-14,rotationX:10,duration:.7,ease:'back.out(1.5)'}},{.2+k*.12:.2f});"
               f"tl.to('#lg{k}',{{rotationY:12,rotationX:6,duration:{max(.3, back-1.1-k*.12):.2f},ease:'sine.inOut'}},{.9+k*.12:.2f});")
    js += f"tl.to(['#tx','.t3'],{{opacity:0,duration:.3,ease:'power2.in'}},{back-.1:.2f});"
    return full(html, '', js, .8 + .12*max(0, len(tiles)-1), min(back - .2, 1.6),
                [(0, 'whoosh-short', -18)] + [(round(.25 + k*.3, 2), 'pop', -18) for k in range(min(2, len(tiles)))])


def th_center(o, ctx):
    """Text centred under the chin over a dark gradient along the bottom; face and both sides stay untouched. Line 1 is
    revealed left to right like typing (Ben "I'm Ben | Three time founder", user rule 16/10/2026).
    props: text, sub, logos [[slug, color], ...] (small tiles in front of line 1), top (px, default 800)."""
    p = o['props']; D = ctx['D']; top = p.get('top', 800)
    tiles = ''.join(f'<span class="ctile" id="ct{k}">{logo(ctx, sl, col)}</span>' for k, (sl, col) in enumerate(p.get('logos', [])))
    sub = f'<div class="csub" id="tl2">{rich(p["sub"])}</div>' if p.get('sub') else ''
    html = (f'<div class="cgr deco" id="cgr"></div><div class="cwrap" style="top:{top}px"><div class="cline">{tiles}'
            f'<span class="ctx" id="tl1">{rich(p["text"])}</span></div>{sub}</div>')
    css = KIT + DARK + ('.cgr{position:absolute;left:0;right:0;bottom:0;height:540px;background:linear-gradient(0deg,rgba(7,6,10,.86),rgba(7,6,10,.55) 46%,rgba(7,6,10,0))}'
                        '.cwrap{position:absolute;left:0;right:0;margin:0 auto;width:max-content;text-align:center;color:#fff;text-shadow:0 4px 26px rgba(0,0,0,.5)}'
                        '.cline{display:inline-flex;align-items:center;gap:22px}.ctx{font:64px/1.1 BodyBold;white-space:nowrap}.ctx em.acc{color:#A99BFF}'
                        '.ctile{width:74px;height:74px;border-radius:20px;background:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -12px rgba(0,0,0,.6)}'
                        '.ctile svg,.ctile img{width:44px!important;height:44px!important}.csub{margin-top:14px;font:32px Body;color:rgba(255,255,255,.82)}')
    n = len(p.get('logos', []))
    js = ("tl.fromTo('#cgr',{opacity:0},{opacity:1,duration:.35,ease:'power2.out'},0);"
          + ''.join(pop(f'#ct{k}', .1 + k*.1, .5) for k in range(n))
          + f"tl.fromTo('#tl1',{{clipPath:'inset(-20% 100% -20% 0%)'}},{{clipPath:'inset(-20% 0% -20% 0%)',duration:.7,ease:'power1.inOut'}},{.15 + n*.1:.2f});"
          f"tl.fromTo('#tl2',{{opacity:0,y:12}},{{opacity:1,y:0,duration:.4,ease:'power3.out'}},{.75 + n*.1:.2f});"
          "tl.to(['#cgr','.cwrap'],{opacity:0,duration:.3,ease:'power2.in'},D-.32);")
    return dict(html=html, css=css, js=js, enter=1.1 + n*.1, exit=.32, hero=min(D - .45, 1.4 + n*.1), full=False,
                sfx=[(0, 'whoosh-short', -19), (round(.15 + n*.1, 2), 'typing', -21)])


def th_chips(o, ctx):
    """Pills flow in from the right one after another along the lower third, the row slides left and ends centred.
    props: items [str] (mark the key one with *word*)."""
    p = o['props']; D = ctx['D']; items = p['items']
    n = len(items); step = min(.75, (D - 1.2)/n)
    html = '<div class="lgr deco" id="lgr"></div><div id="row">' + ''.join(
        f'<span class="cp{" on" if "*" in it else ""}" id="c{k}">{rich(it)}</span>' for k, it in enumerate(items)) + '</div>'
    css = KIT + DARK + ('.lgr{position:absolute;left:0;right:0;bottom:0;height:420px;background:linear-gradient(0deg,rgba(7,6,10,.66),rgba(7,6,10,0))}'
                        '#row{position:absolute;left:0;top:820px;display:flex;gap:22px;white-space:nowrap}'
                        '.cp{display:inline-block;padding:20px 34px;border-radius:16px;background:rgba(14,12,20,.82);border:1px solid rgba(255,255,255,.16);'
                        'color:#fff;font:700 40px/1 BodyBold;box-shadow:0 20px 40px -16px rgba(0,0,0,.7)}.cp.on{background:#5B4BEA;border-color:#8E80FF}.cp em.acc{color:#fff}')
    js = "tl.fromTo('#lgr',{opacity:0},{opacity:1,duration:.3},0);"
    js += f"tl.set('#row',{{x:1300}},0);"
    sfx = []
    for k in range(n):
        t = .15 + k*step
        js += (f"tl.fromTo('#c{k}',{{opacity:0,x:260,filter:'blur(12px)'}},{{opacity:1,x:0,filter:'blur(0px)',duration:.45,ease:'power3.out'}},{t:.2f});")
        sfx.append((round(t, 2), 'click-soft', -17))
    js += (f"tl.to('#row',{{x:()=>(1920-document.getElementById('row').offsetWidth)/2,duration:{n*step:.2f},ease:'power1.inOut'}},.15);"
           "tl.to(['#row','#lgr'],{opacity:0,duration:.3,ease:'power2.in'},D-.32);")
    return dict(html=html, css=css, js=js, enter=.15 + n*step, exit=.32, hero=min(D - .45, .15 + n*step + .2), full=False, sfx=sfx)


def th_lower(o, ctx):
    """Name + role lower-left over the shot (Ben "I'm Ben, three-time founder"). props: name, role."""
    p = o['props']; D = ctx['D']
    html = ('<div class="lgr2 deco" id="lg2"></div><div class="nm" id="nm"><i class="bar" id="br"></i>'
            f'<div class="n1" id="n1">{rich(p["name"])}</div><div class="n2" id="n2">{rich(p["role"])}</div></div>')
    css = KIT + DARK + ('.lgr2{position:absolute;inset:0;background:radial-gradient(1200px 520px at 0% 100%,rgba(7,6,10,.7),rgba(7,6,10,0) 70%)}'
                        '.nm{position:absolute;left:120px;top:770px;color:#fff;text-shadow:0 4px 24px rgba(0,0,0,.5)}'
                        '.bar{position:absolute;left:-30px;top:8px;width:7px;height:120px;border-radius:4px;background:#8E80FF}'
                        '.n1{font:800 66px/1.05 BodyBold}.n2{margin-top:10px;font:500 32px Body;color:rgba(255,255,255,.82)}.n2 em.acc{color:#A99BFF}')
    js = ("tl.fromTo('#lg2',{opacity:0},{opacity:1,duration:.35},0);tl.fromTo('#br',{scaleY:0,transformOrigin:'50% 0%'},{scaleY:1,duration:.4,ease:'power3.out'},.05);"
          "tl.fromTo('#n1',{opacity:0,x:-30},{opacity:1,x:0,duration:.45,ease:'power3.out'},.12);tl.fromTo('#n2',{opacity:0,x:-20},{opacity:1,x:0,duration:.4,ease:'power3.out'},.26);"
          "tl.to(['#lg2','#nm'],{opacity:0,duration:.3,ease:'power2.in'},D-.32);")
    return dict(html=html, css=css, js=js, enter=.7, exit=.32, hero=min(1.5, D - .5), full=False, sfx=[(.05, 'whoosh-short', -19)])


# ------------------------------------------------------------------ full frame (the shot is embedded and moves)

def th_side(o, ctx):
    """Frame slides left (or right), a real visual comes in on the free side with a caption under it.
    props: img (screenshot / frame) or clip [file, start, speed], text, sub, side (right|left), badge."""
    p = o['props']; D = ctx['D']; side = p.get('side', 'right')
    dx = -440 if side == 'right' else 440
    cx = 1000 if side == 'right' else 80
    W, H = 840, 472
    if p.get('clip'):
        f, a, sp = (p['clip'] + [3])[:3]
        media = f'<video src="{ctx["vclip"](f, float(a), speed=float(sp))}" data-start="0" data-duration="{D}" muted playsinline></video>'
        badge = f'<span class="badge" id="bd" style="left:18px;top:18px">{esc(p.get("badge", f"tua nhanh ×{float(sp):g}"))}</span>'
    else:
        media = f'<img src="{ctx["img"](p["img"], 1600)}">'; badge = ''
    html = (blurred(ctx) + '<div class="blk" id="bk" style="opacity:.55"></div>'
            + face(ctx, cls='fadeR' if side == 'right' else 'fadeL')
            + f'<div class="dcard" id="cd" style="left:{cx}px;top:250px;width:{W}px;height:{H}px">{media}{badge}</div>'
            + lines(p, style=f'left:{cx}px;top:{250+H+40}px;width:{W}px;text-align:center'))
    css = '#tx .l1{font-size:54px}#tx .l2{font-size:30px}'
    js, back = shift(D, dx)
    js += (f"tl.fromTo('#cd',{{opacity:0,x:{-dx*.35:.0f},scale:.94}},{{opacity:1,x:0,scale:1,duration:.6,ease:'power3.out'}},.35);"
           + text_in(.6) + (pop('#bd', .8, .7) if badge else '')
           + f"tl.to(['#cd','#tx'],{{opacity:0,x:{-dx*.25:.0f},duration:.35,ease:'power2.in'}},{back-.1:.2f});")
    return full(html, css, js, 1.0, min(back - .2, 2.2), [(0, 'whoosh', -17), (.4, 'whoosh-short', -18), (round(back, 2), 'whoosh-short', -19)])


def th_blurcard(o, ctx):
    """Blur + black layer over the shot, text on the left, a sped-up source clip in a card on the right (Ben "How to set it up").
    props: text, sub, clip [file, start, speed], badge."""
    p = o['props']; D = ctx['D']
    f, a, sp = (p['clip'] + [3])[:3]
    W, H = 900, 506
    html = (face(ctx) + blurred(ctx) + '<div class="blk" id="bk"></div>'
            + f'<div class="dcard" id="cd" style="left:900px;top:287px;width:{W}px;height:{H}px">'
            f'<video src="{ctx["vclip"](f, float(a), speed=float(sp))}" data-start="0" data-duration="{D}" muted playsinline></video>'
            f'<span class="badge" id="bd" style="left:18px;top:18px">{esc(p.get("badge", f"tua nhanh ×{float(sp):g}"))}</span></div>'
            + lines(p, style='left:120px;top:400px;width:700px'))
    end = D - .45
    js = ("tl.fromTo('#fb',{opacity:0},{opacity:1,duration:.35,ease:'power2.out'},0);tl.fromTo('#bk',{opacity:0},{opacity:.55,duration:.35},0);"
          "tl.fromTo('#cd',{opacity:0,x:120,rotationY:-18},{opacity:1,x:0,rotationY:-6,duration:.65,ease:'power3.out'},.2);"
          f"tl.to('#cd',{{rotationY:-2,duration:{end-.85:.2f},ease:'sine.inOut'}},.85);" + text_in(.35) + pop('#bd', .7, .7)
          + f"tl.to(['#cd','#tx'],{{opacity:0,duration:.3,ease:'power2.in'}},{end:.2f});tl.to(['#fb','#bk'],{{opacity:0,duration:.35,ease:'power2.in'}},{end+.08:.2f});")
    return full(html, '', js, 1.0, min(end - .2, 2.4), [(0, 'whoosh', -17), (.2, 'whoosh-short', -18), (round(end, 2), 'whoosh-short', -20)])


def th_pip(o, ctx):
    """The face shrinks into a picture-in-picture corner while a sped-up source clip fills the frame, then grows back.
    props: clip [file, start, speed], label, corner (br|bl)."""
    p = o['props']; D = ctx['D']
    f, a, sp = (p['clip'] + [3])[:3]
    s = .27; br = p.get('corner', 'bl') == 'br'; m = 30
    tx = (1920 - 1920*s - m) if br else m; ty = 1080 - 1080*s - m
    html = (f'<div class="fv" id="src"><video src="{ctx["vclip"](f, float(a), speed=float(sp))}" data-start="0" data-duration="{D}" muted playsinline></video></div>'
            + f'<span class="badge" id="bd" style="{'left:48px' if br else 'right:48px'};top:44px">{esc(p.get("label", f"tua nhanh ×{float(sp):g}"))}</span>'
            + face(ctx, cls='clip'))
    css = '#fv{transform-origin:0 0;border-radius:0}'
    end = D - .6
    js = (f"tl.fromTo('#fv',{{x:0,y:0,scale:1,borderRadius:0}},{{x:{tx:.0f},y:{ty:.0f},scale:{s},borderRadius:70,duration:.7,ease:'power3.inOut'}},.05);"
          "tl.fromTo('#fv',{boxShadow:'0 0 0 0px rgba(255,255,255,0)'},{boxShadow:'0 0 0 12px rgba(255,255,255,.9), 0 60px 120px rgba(0,0,0,.6)',duration:.5},.3);"
          + pop('#bd', .6, .7)
          + f"tl.to('#fv',{{x:0,y:0,scale:1,borderRadius:0,boxShadow:'0 0 0 0px rgba(255,255,255,0)',duration:.6,ease:'power3.inOut'}},{end:.2f});"
          f"tl.to('#bd',{{opacity:0,duration:.2}},{end:.2f});")
    return full(html, css, js, .8, min(end - .2, 2.4), [(0, 'whoosh', -17), (round(end, 2), 'whoosh-short', -19)])


def _wall_rows(ctx, imgs, rows, w, h, gap):
    out = []
    for r in range(rows):
        seq = imgs[r::rows] or imgs
        seq = (seq*4)[:max(8, len(seq)*2)]
        out.append(''.join(f'<div class="wc" style="width:{w}px;height:{h}px"><img src="{ctx["img"](s, 640)}"></div>' for s in seq))
    return out


def th_wall(o, ctx):
    """Tilted wall of real thumbnails / frames scrolling in alternating directions over the blurred dark shot,
    a headline pill in the middle (Ben's channel wall). props: imgs [specs], text, tilt."""
    p = o['props']; D = ctx['D']
    w, h, gap = 430, 242, 26
    rows = _wall_rows(ctx, p['imgs'], 4, w, h, gap)
    html = (face(ctx) + blurred(ctx) + '<div class="blk" id="bk"></div><div id="wall">'
            + ''.join(f'<div class="wr" id="wr{r}">{row}</div>' for r, row in enumerate(rows)) + '</div><div class="vig" id="vg"></div>'
            + f'<div class="dpill" id="hp" style="left:0;right:0;margin:0 auto;width:max-content;top:470px">{rich(p["text"])}</div>')
    css = (f'#wall{{position:absolute;left:-420px;top:-260px;width:2760px;height:1600px;transform:rotate({p.get("tilt", -9)}deg);display:flex;flex-direction:column;gap:{gap}px;justify-content:center}}'
           f'.wr{{display:flex;gap:{gap}px;width:max-content}}.wc{{position:relative;border-radius:16px;overflow:hidden;flex:none;box-shadow:0 20px 40px -12px rgba(0,0,0,.7)}}'
           '.wc img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}'
           '.vig{position:absolute;inset:0;background:radial-gradient(1100px 600px at 50% 50%,rgba(7,6,10,0),rgba(7,6,10,.75))}')
    end = D - .5
    js = "tl.fromTo('#fb',{opacity:0},{opacity:1,duration:.3},0);tl.fromTo('#bk',{opacity:0},{opacity:.6,duration:.3},0);"
    for r in range(4):
        d = 1 if r % 2 else -1
        x0 = -300 if d < 0 else -600
        js += (f"tl.fromTo('#wr{r}',{{x:{x0 + d*1400},opacity:0}},{{x:{x0},opacity:1,duration:.7,ease:'power3.out'}},{.05+r*.06:.2f});"
               f"tl.to('#wr{r}',{{x:'+={d*320}',duration:{end-.8:.2f},ease:'none'}},{.75+r*.06:.2f});")
    js += ("tl.fromTo('#vg',{opacity:0},{opacity:1,duration:.4},.1);" + pop('#hp', .7, .7)
           + f"tl.to(['#wall','#vg','#hp'],{{opacity:0,duration:.35,ease:'power2.in'}},{end:.2f});tl.to(['#fb','#bk'],{{opacity:0,duration:.4,ease:'power2.in'}},{end+.1:.2f});")
    return full(html, css, js, 1.1, min(end - .2, 2.2), [(0, 'whoosh', -17), (.1, 'whoosh-cinematic', -19), (.7, 'pop', -18)])


def th_column(o, ctx):
    """Frame slides left; on the right two tilted columns of real thumbnails run vertically in opposite directions,
    caption under them. props: imgs [specs], text, sub."""
    p = o['props']; D = ctx['D']
    imgs = p['imgs']; w, h, gap = 380, 214, 22
    cols = []
    for c in range(2):
        seq = imgs[c::2] or imgs; seq = (seq*4)[:10]
        cols.append(''.join(f'<div class="wc" style="width:{w}px;height:{h}px"><img src="{ctx["img"](s, 640)}"></div>' for s in seq))
    html = (blurred(ctx) + '<div class="blk" id="bk" style="opacity:.55"></div>' + face(ctx, cls='fadeR')
            + '<div id="colw">' + ''.join(f'<div class="cl2" id="col{c}">{col}</div>' for c, col in enumerate(cols)) + '</div>'
            + '<div class="cvig" id="cvg"></div>' + lines(p, style='left:1010px;top:860px;width:820px;text-align:center'))
    css = (f'#colw{{position:absolute;left:1030px;top:-300px;width:800px;height:1700px;display:flex;gap:{gap}px;transform:rotate(8deg)}}'
           f'.cl2{{display:flex;flex-direction:column;gap:{gap}px}}.wc{{position:relative;border-radius:14px;overflow:hidden;flex:none;box-shadow:0 18px 36px -12px rgba(0,0,0,.7)}}'
           '.wc img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}'
           '.cvig{position:absolute;left:960px;top:0;right:0;bottom:0;background:linear-gradient(0deg,rgba(7,6,10,.92),rgba(7,6,10,0) 34%,rgba(7,6,10,0) 80%,rgba(7,6,10,.7))}'
           '#tx .l1{font-size:52px}#tx .l2{font-size:30px}')
    js, back = shift(D, -440)
    js += ("tl.fromTo('#colw',{opacity:0,x:200},{opacity:1,x:0,duration:.6,ease:'power3.out'},.3);tl.fromTo('#cvg',{opacity:0},{opacity:1,duration:.4},.3);"
           f"tl.fromTo('#col0',{{y:0}},{{y:-{(h+gap)*3}, duration:{D:.2f},ease:'none'}},0);tl.fromTo('#col1',{{y:-{(h+gap)*3}}},{{y:0,duration:{D:.2f},ease:'none'}},0);"
           + text_in(.7) + f"tl.to(['#colw','#cvg','#tx'],{{opacity:0,duration:.35,ease:'power2.in'}},{back-.1:.2f});")
    return full(html, css, js, 1.1, min(back - .2, 2.4), [(0, 'whoosh', -17), (.35, 'whoosh-short', -18), (round(back, 2), 'whoosh-short', -19)])


def th_page(o, ctx):
    """A real page screenshot tilted in 3D, slowly panning, over the blurred dark shot, headline pill below.
    props: img (screenshot), text, pan (px to travel)."""
    p = o['props']; D = ctx['D']
    html = (face(ctx) + blurred(ctx) + '<div class="blk" id="bk"></div><div class="scene"><div id="pgw"><div class="pgc" id="pgc">'
            f'<img src="{ctx["img"](p["img"])}"></div></div></div><div class="pvig" id="pvg"></div>'
            + f'<div class="dpill" id="hp" style="left:0;right:0;margin:0 auto;width:max-content;top:850px">{rich(p["text"])}</div>')
    css = ('#pgw{position:absolute;left:260px;top:120px;width:1400px;height:788px;transform-style:preserve-3d}'
           '.pgc{position:absolute;inset:0;border-radius:20px;overflow:hidden;box-shadow:0 0 0 1px rgba(255,255,255,.18),0 60px 120px -30px rgba(0,0,0,.9)}'
           '.pgc img{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;transform-origin:30% 20%}'
           '.pvig{position:absolute;inset:0;background:linear-gradient(0deg,rgba(7,6,10,.85),rgba(7,6,10,0) 36%)}')
    end = D - .5
    js = ("tl.fromTo('#fb',{opacity:0},{opacity:1,duration:.3},0);tl.fromTo('#bk',{opacity:0},{opacity:.6,duration:.3},0);"
          "tl.fromTo('#pgw',{opacity:0,y:120,rotationX:34,rotationZ:-8,scale:.9},{opacity:1,y:0,rotationX:20,rotationZ:-5,scale:1,duration:.8,ease:'power3.out'},.08);"
          f"tl.to('#pgw',{{rotationX:12,rotationZ:-3,duration:{end-.9:.2f},ease:'sine.inOut'}},.88);"
          f"tl.fromTo('.pgc img',{{scale:1.0,x:0,y:0}},{{scale:{p.get('zoom', 1.35)},x:-60,y:-40,duration:{end:.2f},ease:'sine.inOut'}},0);"
          "tl.fromTo('#pvg',{opacity:0},{opacity:1,duration:.4},.2);" + pop('#hp', .8, .7)
          + f"tl.to(['#pgw','#pvg','#hp'],{{opacity:0,duration:.35,ease:'power2.in'}},{end:.2f});tl.to(['#fb','#bk'],{{opacity:0,duration:.4,ease:'power2.in'}},{end+.1:.2f});")
    return full(html, css, js, 1.2, min(end - .2, 2.6), [(0, 'whoosh', -17), (.08, 'whoosh-cinematic', -19), (.8, 'pop', -18)])


def th_row(o, ctx):
    """Blur + black layer, an optional 3D logo tile on top, a row of real cards rising in, one line under them
    (Ben "Eight tips and techniques"). props: cards [{img, label}], logo, logo_color, text."""
    p = o['props']; D = ctx['D']; cards = p['cards'][:5]
    n = len(cards); w = 330 if n > 3 else 400; h = round(w*9/16); gap = 34
    x0 = (1920 - (n*w + (n-1)*gap))/2; y = 430
    tile = (tile3d('lg', 885, 190, 150, logo(ctx, p['logo'], p.get('logo_color', '#14A800')), depth=18, n=8) if p.get('logo') else '')
    row = ''.join(f'<div class="dcard rc" id="r{k}" style="left:{x0 + k*(w+gap):.0f}px;top:{y}px;width:{w}px;height:{h}px">'
                  f'<img src="{ctx["img"](c["img"], 800)}"><span class="badge" style="left:12px;bottom:12px;top:auto">{esc(c.get("label", ""))}</span></div>'
                  for k, c in enumerate(cards))
    html = (face(ctx) + blurred(ctx) + '<div class="blk" id="bk"></div>' + f'<div class="scene">{tile}</div>' + row
            + lines(p, style=f'left:0;right:0;top:{y + h + 60}px;text-align:center'))
    css = '#tx .l1{font-size:56px}.rc .badge{font-size:18px}'
    end = D - .5
    js = ("tl.fromTo('#fb',{opacity:0},{opacity:1,duration:.35,ease:'power2.out'},0);tl.fromTo('#bk',{opacity:0},{opacity:.66,duration:.35},0);"
          + ("tl.fromTo('#lg',{opacity:0,scale:.5,rotationY:-60},{opacity:1,scale:1,rotationY:-12,rotationX:10,duration:.7,ease:'back.out(1.5)'},.1);"
             f"tl.to('#lg',{{rotationY:14,duration:{end-.8:.2f},ease:'sine.inOut'}},.8);" if tile else '')
          + ''.join(f"tl.fromTo('#r{k}',{{opacity:0,y:80,rotation:{(k-(n-1)/2)*3:.1f}}},{{opacity:1,y:0,rotation:0,duration:.55,ease:'back.out(1.3)'}},{.35+k*.12:.2f});" for k in range(n))
          + text_in(.5 + n*.12)
          + f"tl.to(['.rc','#tx','#lg'],{{opacity:0,y:-20,duration:.3,ease:'power2.in'}},{end:.2f});tl.to(['#fb','#bk'],{{opacity:0,duration:.35,ease:'power2.in'}},{end+.08:.2f});")
    sfx = [(0, 'whoosh', -17)] + [(round(.35 + k*.24, 2), 'click-soft', -18) for k in range((n+1)//2)]
    return full(html, css, js, .9 + n*.12, min(end - .2, 1.6 + n*.12), sfx)


TALKING = {'th-text': th_text, 'th-chips': th_chips, 'th-lower': th_lower, 'th-side': th_side, 'th-blurcard': th_blurcard,
           'th-pip': th_pip, 'th-wall': th_wall, 'th-column': th_column, 'th-page': th_page, 'th-row': th_row, 'th-center': th_center}
