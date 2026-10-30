// Scenes s65-s67 (intro 64.1-80.0): 2 video trên 10.000 view, tỷ lệ view/sub 10x, đăng lại lên TikTok/Facebook rồi reach tăng.
const F2N = n => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
// running numbers computed from the timeline time, so any seek (forward or back) shows the right value
const F2COUNT = (tl, list) => tl.eventCallback('onUpdate', () => {
  const t = tl.time();
  list.forEach(([el, t0, t1, n]) => { const p = Math.min(1, Math.max(0, (t - t0)/(t1 - t0))); el.textContent = F2N(Math.round(n*(1 - Math.pow(1 - p, 3)))); });
});
const F2YT = (x, y) => `<div style="${x}px;${y}px;width:58px;height:42px;padding:8px 9px;border-radius:11px;background:#fff;box-shadow:0 4px 12px -4px rgba(23,19,13,.35)">${LOGOS.youtube}</div>`;
const F2VID = (cls, x, y, img, ttl, plus = '') => `<div class="paper ${cls}" style="left:${x}px;top:${y}px;width:450px;height:420px;border-radius:26px">
  <img src="img/${img}" style="left:16px;top:16px;width:418px;height:235px;border-radius:16px;object-fit:cover">
  <div style="left:22px;right:22px;top:266px;height:60px;overflow:hidden;font:700 22px/30px Body;white-space:normal">${ttl}</div>
  <div class="vr" style="left:16px;top:346px;display:flex;align-items:center;gap:10px;padding:8px 20px 8px 16px;border-radius:999px;background:var(--ivory-deep);font:800 30px Disp;white-space:nowrap">${IC('eye', 28)}<span class="n" style="position:static">0</span>${plus ? '<span class="pl" style="position:relative;margin-left:-8px">+</span>' : ''}<span style="position:static">view</span></div></div>`;
const F2C67 = () => card(960, 600, 400, 460);

SCENES.push(
{id: 's65', clip: 'clips/s65.mp4', dur: 3.9, poster: 3.6, name: '2 video <em>trên 10.000 view</em>',
 desc: '"2 cái video trên 10.000 view, ở trên cái kênh khoảng 1.000 subscriber": 2 thẻ video thật trượt vào, số view chạy tới 11.088 (REA) và 10.000+ (CapCut), rồi chip kênh chạy số subscriber tới 1.000.',
 html: () => BG + title(1345, 110, '2 video trên <em>10.000 view</em>') +
   F2VID('vc1', 880, 250, 'rea-t1.jpg', 'Reverse Engineer Anything: clone mọi phần mềm bằng AI') +
   F2VID('vc2', 1360, 250, 'cap-thumb.jpg', 'Claude Code tự dựng video trong CapCut', 1) +
   `<div class="chn paper" style="left:930px;top:715px;width:830px;height:130px;border-radius:30px">
     <img src="img/chan-avatar.png" style="left:26px;top:25px;width:80px;height:80px;border-radius:50%">
     <div style="left:128px;top:22px;font:800 34px Disp;letter-spacing:-.02em;white-space:nowrap">Thành Vũ Đức</div>
     <div style="left:128px;top:72px;display:flex;align-items:center;gap:10px;font:600 20px Body;color:var(--ink-muted);white-space:nowrap"><i style="position:static;display:block;width:30px;height:21px">${LOGOS.youtube}</i>kênh YouTube</div>
     <div style="right:32px;top:24px;display:flex;align-items:baseline;gap:12px;white-space:nowrap"><span class="ns" style="position:relative;display:inline-block;font:800 64px Disp;letter-spacing:-.03em;color:var(--plum)">0</span><span class="sl" style="position:static;font:700 26px Body;color:var(--ink-muted)">subscriber</span></div></div>`,
 anim(tl, $, f, v) {
   move(tl, f, v, CARD.L, 0, .45); rise(tl, $('.ttl'), .15);
   [['.vc1', .25], ['.vc2', .5]].forEach(([c, t]) => tl.fromTo($(c), {opacity: 0, x: 160, filter: 'blur(10px)'}, {opacity: 1, x: 0, filter: 'blur(0px)', duration: .5, ease: 'expo.out'}, t));
   [['.vc1', 1.0], ['.vc2', 1.15]].forEach(([c, t]) => { const r = $(c + ' .vr');
     tl.to(r, {backgroundColor: '#4A3AE0', color: '#fff', duration: .2}, t); tl.fromTo(r, {scale: 1.18}, {scale: 1, duration: .45, ease: 'back.out(2.4)', immediateRender: false}, t); });
   pop(tl, $('.vc2 .pl'), 1.15, .3);
   hop(tl, $('.vc1'), 1.35, 16); hop(tl, $('.vc2'), 1.45, 16);
   rise(tl, $('.chn'), 1.85, 34);
   tl.fromTo($('.ns'), {scale: 1.3}, {scale: 1, duration: .45, ease: 'back.out(2.2)', immediateRender: false}, 3.0);
   tl.to($('.sl'), {color: '#4A3AE0', duration: .2}, 3.3); hop(tl, $('.chn'), 3.3, 12);
   F2COUNT(tl, [[$('.vc1 .n'), .55, 1.05, 11088], [$('.vc2 .n'), .75, 1.15, 10000], [$('.ns'), 2.2, 3.0, 1000]]);
 }},

{id: 's66', clip: 'clips/s66.mp4', dur: 3.6, poster: 3.4, name: 'Tỷ lệ view trên sub <em>10x</em>',
 desc: '"tỷ lệ views trên subscriber gần như là 10x luôn": cột View mọc lên 10.000 ở chữ "views", cột Subscriber 1.000 ở chữ "subscriber", mũi tên vẽ từ cột thấp lên cột cao và nhãn "10x" bật ra đúng chữ "10x".',
 html: () => BG + title(615, 110, 'Tỷ lệ <em>view trên sub</em>') +
   `${LINE('bl', 170, 862, 1070, 862, 'var(--ink-faint)', 4)}
    <div class="b0" style="left:300px;top:818px;width:200px;height:42px;border-radius:14px 14px 4px 4px;background:var(--lav);transform-origin:50% 100%"></div>
    <div class="b1" style="left:700px;top:440px;width:200px;height:420px;border-radius:18px 18px 4px 4px;background:linear-gradient(180deg,#7B6CFF,#4A3AE0);transform-origin:50% 100%;box-shadow:0 24px 50px -24px rgba(74,58,224,.6)"></div>
    <div class="v0" style="left:250px;top:740px;width:300px;text-align:center;font:800 56px Disp;letter-spacing:-.03em">0</div>
    <div class="v1" style="left:650px;top:356px;width:300px;text-align:center;font:800 64px Disp;letter-spacing:-.03em;color:var(--plum)">0</div>` +
   [['Subscriber', 'user', 250], ['View', 'eye', 650]].map(([n, i, x], j) => `<div class="k${j}" style="left:${x}px;top:886px;width:300px;display:flex;justify-content:center;align-items:center;gap:10px;font:800 32px Disp;color:var(--ink-soft);white-space:nowrap">${IC(i, 30)}${n}</div>`).join('') +
   `<div class="ar" style="left:0;top:0;width:1920px;height:1080px"><svg viewBox="0 0 1920 1080">
      <path class="ap" d="M400 725 C 410 560, 520 470, 668 452" pathLength="1" fill="none" stroke="#4A3AE0" stroke-width="6" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>
      <path class="ah" d="M640 430 L672 452 L644 482" fill="none" stroke="#4A3AE0" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" opacity="0"/></svg></div>
    <div class="x10" style="left:925px;top:225px;width:200px;height:200px;border-radius:50%;background:var(--plum);color:#fff;display:grid;place-items:center;font:800 88px Disp;letter-spacing:-.04em;box-shadow:0 22px 44px -16px rgba(74,58,224,.65),0 0 0 8px rgba(183,168,255,.45)">10x</div>`,
 anim(tl, $, f, v) {
   tl.set(f, CARD.L.box, 0); tl.set(v, CARD.L.vid, 0); move(tl, f, v, CARD.R, .02, .5);
   draw(tl, $('.bl'), .3, .45); rise(tl, $('.ttl'), .45);
   [[1, 1.2, .5], [0, 1.8, .35]].forEach(([j, t, d]) => {
     rise(tl, $('.k' + j), t - .1, 14);
     tl.fromTo($('.b' + j), {scaleY: 0}, {scaleY: 1, duration: d, ease: 'power3.out'}, t);
     tl.fromTo($('.v' + j), {opacity: 0, y: j ? 420 : 42}, {opacity: 1, y: 0, duration: d, ease: 'power3.out'}, t);
   });
   tl.to($('.k1'), {color: '#4A3AE0', duration: .2}, 1.2); tl.to($('.k0'), {color: '#4A3AE0', duration: .2}, 1.8);
   tl.to($('.ap'), {attr: {'stroke-dashoffset': 0}, duration: .4, ease: 'power2.inOut'}, 2.7); tl.to($('.ah'), {attr: {opacity: 1}, duration: .1}, 3.05);
   tl.fromTo($('.x10'), {opacity: 0, scale: .2, rotate: -40}, {opacity: 1, scale: 1, rotate: -8, duration: .5, ease: 'back.out(2.2)'}, 3.1);
   tl.fromTo($('.b1'), {filter: 'brightness(1.5)'}, {filter: 'brightness(1)', duration: .5, immediateRender: false}, 3.1); hop(tl, $('.v1'), 3.1, 18);
   F2COUNT(tl, [[$('.v1'), 1.2, 1.7, 10000], [$('.v0'), 1.8, 2.15, 1000]]);
 }},

{id: 's67', clip: 'clips/s67.mp4', dur: 8.4, poster: 8.2, name: 'Đăng lại lên <em>mọi nền tảng</em>',
 desc: '"những cái video này mình đăng lên TikTok, Facebook, những nền tảng khác, thì nó cũng đạt được một cái lượng reach rất lớn": chấm tín hiệu chạy từ video tới từng nền tảng, logo bật đúng chữ TikTok, Facebook, "nền tảng khác"; tới chữ "reach" đồ thị vọt lên, "lớn" thì mũi tên bật.',
 html: () => BG + title(960, 80, 'Đăng lên <em>mọi nền tảng</em>') + title(960, 80, 'Reach <em>rất lớn</em>').replace('class="ttl"', 'class="ttl t2"') +
   `<div class="vs" style="left:130px;top:410px;width:460px;height:330px">
      <img class="vb" src="img/cap-thumb.jpg" style="left:24px;top:0;width:420px;height:236px;border-radius:18px;object-fit:cover;border:4px solid #fff;box-shadow:var(--shadow)">
      <div class="vf" style="left:0;top:56px;width:440px;height:248px"><img src="img/rea-t1.jpg" style="left:0;top:0;width:440px;height:248px;border-radius:18px;object-fit:cover;border:4px solid #fff;box-shadow:0 26px 50px -20px rgba(23,19,13,.45)">${F2YT('right:16', 'bottom:16')}</div></div>` +
   [305, 505, 697].map((y, j) => LINE('ln ln' + j, 590, 570, 1316, y, 'var(--line-strong)', 4)).join('') +
   `<div class="gr paper" style="left:100px;top:380px;width:560px;height:400px;border-radius:28px;overflow:hidden">
      <div style="left:32px;top:28px;display:flex;align-items:center;gap:12px;font:700 18px Body;letter-spacing:.16em;color:var(--plum)"><svg class="ic" width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M22 7l-8.5 8.5-5-5L2 17M16 7h6v6"/></svg>REACH</div>
      <div style="left:30px;top:96px;width:500px;height:280px"><svg viewBox="0 0 500 280" overflow="visible">
        <defs><linearGradient id="f2g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7B6CFF" stop-opacity=".45"/><stop offset="1" stop-color="#7B6CFF" stop-opacity="0"/></linearGradient></defs>
        ${[70, 140, 210].map(y => `<line x1="0" x2="500" y1="${y}" y2="${y}" stroke="rgba(23,19,13,.08)" stroke-width="2"/>`).join('')}
        <path class="ga" d="M0 262 L60 258 L120 254 L180 249 L240 241 L300 228 L340 202 L380 152 L420 94 L460 44 L496 14 L496 280 L0 280 Z" fill="url(#f2g)" opacity="0"/>
        <path class="gl" d="M0 262 L60 258 L120 254 L180 249 L240 241 L300 228 L340 202 L380 152 L420 94 L460 44 L496 14" pathLength="1" fill="none" stroke="#4A3AE0" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1"/></svg></div>
      <div class="ua badge" style="left:446px;top:62px;width:84px;height:84px;background:var(--plum)">${IC('up', 42)}</div></div>` +
   [0, 1, 2, 3, 4, 5, 6].map(j => `<i class="dt dt${j}" style="left:0;top:0;width:22px;height:22px;margin:-11px 0 0 -11px;border-radius:50%;background:var(--plum);box-shadow:0 0 0 6px rgba(123,108,255,.28),0 0 22px 4px rgba(123,108,255,.55);opacity:0"></i>`).join('') +
   `<div class="p0" style="left:1330px;top:240px;display:flex;align-items:center;gap:26px"><img src="img/tiktok-icon.png" style="position:static;width:130px;height:130px;border-radius:32px;box-shadow:var(--shadow)"><span style="position:static;font:800 40px Disp;letter-spacing:-.03em">TikTok</span></div>
    <div class="p1" style="left:1330px;top:440px;display:flex;align-items:center;gap:26px"><div style="position:relative;width:130px;height:130px;border-radius:32px;background:#fff;border:1.5px solid var(--line-strong);box-shadow:var(--shadow);display:grid;place-items:center"><img src="img/facebook-logo.png" style="position:static;width:88px;height:88px"></div><span style="position:static;font:800 40px Disp;letter-spacing:-.03em">Facebook</span></div>
    <div class="p2" style="left:1330px;top:655px;width:330px;height:150px">` +
     ['video', 'chat', 'image'].map((i, k) => TILE('q q' + k, k*104, 0, 84, IC(i, 38))).join('') +
     `<div class="pq" style="left:0;top:104px;font:800 32px Disp;letter-spacing:-.02em;white-space:nowrap">+ nền tảng khác</div></div>`,
 anim(tl, $, f, v) {
   tl.set(f, CARD.R.box, 0); tl.set(v, CARD.R.vid, 0); move(tl, f, v, F2C67(), .05, .55);
   const t2 = $('.t2'); tl.set(t2, {opacity: 0}, 0);
   rise(tl, $('.ttl'), .35);
   rise(tl, $('.vs'), .5, 30); tl.fromTo($('.vb'), {rotate: 0, x: 0}, {rotate: -7, x: -10, duration: .45, ease: 'back.out(1.6)'}, .75);
   const dot = (k, t, x0, y0, x1, y1, d = .38) => { const e = $('.dt' + k);
     tl.set(e, {opacity: 1, left: x0, top: y0}, t); tl.to(e, {left: x1, top: y1, duration: d, ease: 'power1.in'}, t); tl.set(e, {opacity: 0}, t + d); };
   [[1.55, 2.0, 305], [2.95, 3.4, 505], [3.85, 4.3, 697]].forEach(([t, tp, y], j) => {
     draw(tl, $('.ln' + j), t, .3); click(tl, $('.vf'), t); dot(j, t + .05, 590, 570, 1316, y);
   });
   pop(tl, $('.p0'), 2.0, .4); pop(tl, $('.p1'), 3.4, .4);
   ['.q0', '.q1', '.q2'].forEach((q, k) => pop(tl, $(q), 4.3 + k*.15, .4)); rise(tl, $('.pq'), 4.45, 14);
   // reach: video stack gives way to the graph, signals flow back from the platforms
   tl.to($('.vs'), {opacity: 0, x: -40, filter: 'blur(8px)', duration: .3}, 4.95); rise(tl, $('.gr'), 5.05, 30);
   tl.to($$('.ln'), {backgroundColor: '#7B6CFF', duration: .3}, 5.2);
   [[3, 5.35, 305], [4, 5.75, 505], [5, 6.15, 697], [6, 6.55, 305]].forEach(([k, t, y]) => dot(k, t, 1316, y, 650, 570, .5));
   tl.to($('.gl'), {attr: {'stroke-dashoffset': .5}, duration: 1.5, ease: 'none'}, 5.4);
   tl.to($('.ttl:not(.t2)'), {opacity: 0, y: -18, duration: .25}, 6.85); rise(tl, t2, 7.0, 20);
   tl.to($('.gl'), {attr: {'stroke-dashoffset': 0}, duration: .6, ease: 'expo.out'}, 7.0); tl.to($('.ga'), {attr: {opacity: 1}, duration: .5}, 7.05);
   tl.set($('.ua'), {opacity: 0}, 0); pop(tl, $('.ua'), 7.9, .3); hop(tl, $('.gr'), 7.9, 16);
 }}
);
