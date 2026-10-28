// Shared kit for the extra scenes (s11+). Loaded after the base script (IC, LOGOS, BG, title, rise, pop, move, CARD, FULL, chars).
const DOTS = '<i style="position:static;width:11px;height:11px;border-radius:50%;background:var(--ink-faint)"></i>'.repeat(3);
const WIN = (cls, x, y, w, h, inner = '', bar = '') => `<div class="paper ${cls}" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;border-radius:22px;overflow:hidden">
  <div style="left:0;right:0;top:0;height:46px;border-bottom:1px solid var(--line);background:var(--ivory);display:flex;align-items:center;gap:8px;padding:0 18px">${DOTS}${bar ? `<span style="position:static;margin-left:12px;font:600 16px Body;color:var(--ink-muted)">${bar}</span>` : ''}</div>${inner}</div>`;
const LN = (x, y, w, c = 'rgba(23,19,13,.1)', h = 12, cls = '') => `<i class="${cls}" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;border-radius:${h/2}px;background:${c}"></i>`;
const LINE = (cls, x1, y1, x2, y2, c = 'var(--ink-faint)', w = 3) => {
  const d = Math.hypot(x2 - x1, y2 - y1), a = Math.atan2(y2 - y1, x2 - x1)*180/Math.PI;
  return `<i class="${cls}" style="left:${x1}px;top:${y1 - w/2}px;width:${d}px;height:${w}px;border-radius:${w}px;background:${c};transform-origin:0 50%;rotate:${a}deg"></i>`;
};
const MAP = ['...XXXXXX...', '..XXXXXXXX..', 'XXX.XXXX.XXX', 'XXXXXXXXXXXX', '..XXXXXXXX..', '..X.X..X.X..'];
const MASC = (cls, x, y, px = 14, col = '#4A3AE0', hat = '') => `<div class="${cls}" style="left:${x}px;top:${y}px;width:${12*px}px;height:${(hat ? 8 : 6)*px}px">
  <svg viewBox="0 0 12 ${hat ? 8 : 6}" shape-rendering="crispEdges" style="width:100%;height:100%">${hat ? `<rect x="3" y="0" width="6" height="2" fill="${hat}"/>` : ''}
  ${MAP.map((r, j) => [...r].map((c, i) => c == 'X' ? `<rect x="${i}" y="${j + (hat ? 2 : 0)}" width="1.02" height="1.02" fill="${col}"/>` : '').join('')).join('')}</svg></div>`;
const CUR = (cls, x, y) => `<div class="${cls}" style="left:${x}px;top:${y}px;width:34px;height:44px;z-index:40"><svg viewBox="0 0 24 30" style="width:100%;height:100%"><path d="M2 2v22l6-5.5 4 9 4-1.8-4-8.7h8z" fill="#17130D" stroke="#fff" stroke-width="1.8" stroke-linejoin="round"/></svg></div>`;
const TILE = (cls, x, y, sz, inner, lab = '', col = 'var(--ink-muted)') => `<div class="${cls}" style="left:${x}px;top:${y}px;width:${sz}px;text-align:center">
  <div class="tb" style="position:relative;width:${sz}px;height:${sz}px;border-radius:${sz*.26}px;border:2.5px solid var(--line-strong);background:rgba(255,255,255,.75);display:grid;place-items:center;color:${col}">${inner}</div>
  ${lab ? `<div class="tl2" style="position:relative;margin-top:12px;font:800 24px Disp;letter-spacing:-.02em;white-space:nowrap;left:50%;translate:-50% 0;display:inline-block">${lab}</div>` : ''}</div>`;
const PILL = (cls, x, y, txt, ico = '') => `<div class="${cls}" style="left:${x}px;top:${y}px;display:flex;align-items:center;gap:10px;padding:12px 22px;border-radius:999px;background:#fff;border:1.5px solid var(--line-strong);font:700 22px Body;white-space:nowrap">${ico ? IC(ico, 22) : ''}${txt}</div>`;
const lit = (tl, el, t, col = '#4A3AE0', fill = 'rgba(183,168,255,.3)') => {
  const b = el.querySelector('.tb') || el;
  tl.to(b, {borderColor: col, backgroundColor: fill, color: col, duration: .25}, t);
  tl.fromTo(b, {scale: 1.12}, {scale: 1, duration: .45, ease: 'back.out(2)'}, t);
};
const dim = (tl, els, t, o = .3) => tl.to(els, {opacity: o, duration: .3}, t);
const hop = (tl, el, t, h = 34) => { tl.to(el, {y: -h, duration: .18, ease: 'power2.out'}, t); tl.to(el, {y: 0, duration: .3, ease: 'bounce.out'}, t + .18); };
const draw = (tl, el, t, d = .4) => tl.fromTo(el, {scaleX: 0}, {scaleX: 1, duration: d, ease: 'power2.inOut'}, t);
const type = (tl, sel, t0, t1) => { const ks = $$(sel); tl.set(ks, {display: 'none'}, 0); ks.forEach((k, j) => tl.set(k, {display: 'inline-block'}, t0 + j*(t1 - t0)/ks.length)); };
const click = (tl, el, t) => { tl.to(el, {scale: .84, duration: .08}, t); tl.to(el, {scale: 1, duration: .18, ease: 'back.out(3)'}, t + .08); };
const glide = (tl, el, t, x, y, d = .6) => tl.to(el, {left: x, top: y, duration: d, ease: 'power2.inOut'}, t);
// Claude Code desktop frame (brand-tinted), content goes in .main (1070 x 702 before the 1.3 scale)
const CLAUDE = (inner, title = 'edit whole youtube video') => `<div class="cw paper" style="left:70px;top:46px;width:1370px;height:762px;border-radius:24px;overflow:hidden;transform-origin:0 0;scale:1.3">
  <div style="left:0;top:0;bottom:0;width:300px;background:var(--ivory);border-right:1px solid var(--line)">
   <div style="left:20px;top:18px;display:flex;gap:7px">${DOTS}</div>
   <div style="left:20px;right:20px;top:60px;display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:12px;border:1px solid var(--line-strong);background:#fff;font:700 17px Body">${IC('plus', 18)} Phiên mới</div>
   <div style="left:34px;top:130px;font:700 12px Body;letter-spacing:.16em;color:var(--ink-muted)">GẦN ĐÂY</div>
   <div style="left:20px;right:20px;top:156px;display:flex;flex-direction:column;gap:2px">${['he-thong-youtube-ai', 'capcut-ai-yt', 'topview-final', 'rea-yt'].map((s, j) =>
     `<div style="position:static;padding:10px 14px;border-radius:10px;font-size:16px;${j ? 'color:var(--ink-soft)' : 'background:rgba(183,168,255,.3);font-weight:700'}">${s}</div>`).join('')}</div></div>
  <div style="left:300px;right:0;top:0;height:60px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:12px;padding:0 28px;font:700 18px Body">${title}
   <span style="position:static;font:600 13px Body;color:var(--plum);background:rgba(183,168,255,.3);padding:3px 10px;border-radius:999px">Code</span></div>
  <div class="main" style="left:300px;right:0;top:60px;bottom:0">${inner}</div></div>`;
const INPUT = (cls, top, inner = '') => `<div class="${cls}" style="left:60px;right:60px;top:${top}px;height:120px;border-radius:20px;border:2px solid var(--line-strong);background:#fff;box-shadow:var(--shadow)">${inner}
  <div style="left:22px;bottom:12px;display:flex;gap:8px;font:600 14px Body;color:var(--ink-muted)"><span style="position:static;border:1px solid var(--line);border-radius:8px;padding:4px 10px">Opus 5.5</span></div>
  <div class="snd" style="right:14px;bottom:12px;width:42px;height:42px;border-radius:13px;background:var(--ink-faint);display:grid;place-items:center;color:#fff">${IC('up', 22)}</div></div>`;
const CLAUDEMSG = (cls, top, html) => `<div class="${cls}" style="left:60px;right:60px;top:${top}px;display:flex;gap:12px;align-items:flex-start;font-size:18px;line-height:1.5"><div style="position:static;flex:none;width:24px;height:24px;margin-top:2px">${LOGOS.claude}</div><div style="position:static">${html}</div></div>`;
