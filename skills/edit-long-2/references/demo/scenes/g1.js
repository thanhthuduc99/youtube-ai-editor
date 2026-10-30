// Gap A fill: s71-s75 (109-149 s, REA proof + thumbnails + style + skin), s76-s79 (205-234 s, skill steps: outline, freestyle, record).
{
// face card of the scene that ends right where this one starts (same video frame, so start from its card and slide on)
const cardOf = (id, side) => { const F0 = FACE; FACE = FACES[id] || F0; const c = CARD[side]; FACE = F0; return c; };
const startAt = (tl, f, v, c) => { tl.set(f, {...c.box, filter: 'blur(0px)'}, 0); tl.set(v, c.vid, 0); };
const fadeOut = (tl, els, t) => tl.to(els, {opacity: 0, y: -16, duration: .35, ease: 'power2.in'}, t);
const HL = (cls, x, y, w, h) => `<i class="${cls}" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;border-radius:10px;border:3px solid var(--plum);background:rgba(183,168,255,.18);transform-origin:0 50%;opacity:0"></i>`;
const TAG = (cls, x, y, txt, bg = 'var(--plum)') => `<div class="${cls}" style="left:${x}px;top:${y}px;padding:8px 16px;border-radius:999px;background:${bg};color:#fff;font:700 19px Body;white-space:nowrap;display:flex;align-items:center;gap:8px;opacity:0">${txt}</div>`;
const PHONE = (cls, x, y, w, h, img, rec = true) => `<div class="${cls}" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;border-radius:${w*.16}px;background:#17130D;box-shadow:var(--shadow);padding:0">
  <div style="left:${w*.045}px;top:${w*.045}px;right:${w*.045}px;bottom:${w*.045}px;border-radius:${w*.12}px;overflow:hidden;background:#000">
   <img src="img/${img}" style="left:0;top:0;width:100%;height:100%;object-fit:cover">
   ${rec ? `<div style="left:16px;top:18px;display:flex;align-items:center;gap:8px;padding:6px 12px;border-radius:999px;background:rgba(0,0,0,.45);color:#fff;font:700 16px Body"><i class="rd" style="position:static;width:12px;height:12px;border-radius:50%;background:#F0453A"></i>REC</div>` : ''}</div>
  <i style="left:${w*.39}px;top:${w*.075}px;width:${w*.22}px;height:${Math.max(4, w*.04)}px;border-radius:7px;background:#17130D"></i></div>`;

SCENES.push(

{id: 's71', clip: 'clips/s71.mp4', dur: 7.66, poster: 6.8, name: 'Mô tả + timestamp + <em>thumbnail</em> do AI',
 desc: 'Nối từ s08 (mặt góc dưới trái trượt sang trái). Phần mô tả thật của video REA: "do con AI" khoanh đoạn mô tả, "timestamp" khoanh khối timestamp, "thumbnail" bật thumbnail thật của video REA, "xem thử" con trỏ bấm vào thumbnail.',
 html: () => BG + `<div class="ttl" style="left:1330px;top:70px"><h2><span class="w w0" style="color:var(--ink-faint)">Mô tả</span>, <span class="w w1" style="color:var(--ink-faint)">timestamp</span>, <span class="w w2 em" style="color:var(--ink-faint)">thumbnail</span></h2><p class="tp">con AI làm hết</p></div>` +
   `<div class="dsc paper" style="left:820px;top:240px;width:1000px;height:486px;border-radius:24px;overflow:hidden">
     <img src="img/web-04-rea-desc-crop.png" style="left:0;top:-50px;width:1000px">
     ${HL('h0', 14, 262, 972, 52)}${HL('h1', 14, 336, 290, 140)}</div>` +
   TAG('tg0', 1560, 222, IC('sparkles', 20) + 'AI viết') + TAG('tg1', 1130, 650, IC('clock', 20) + 'AI chia mốc') +
   `<div class="th paper" style="left:1390px;top:650px;width:440px;height:300px;border-radius:22px;rotate:-3deg;opacity:0">
     <img src="img/rea-t1.jpg" style="left:12px;top:12px;width:416px;height:234px;border-radius:14px;object-fit:cover">
     <div style="left:18px;top:256px;font:800 24px Disp;letter-spacing:-.02em">Thumbnail</div>
     <div style="right:18px;top:254px;padding:4px 12px;border-radius:999px;background:rgba(183,168,255,.35);color:var(--plum);font:700 17px Body">AI làm</div></div>` +
   CUR('cur', 1900, 1080),
 anim(tl, $, f, v) {
   startAt(tl, f, v, cardOf('s08', 'BL')); move(tl, f, v, CARD.L, .15);
   rise(tl, $('.ttl'), .35); tl.set($('.tp'), {opacity: 0}, 0); rise(tl, $('.tp'), 1.76, 12); rise(tl, $('.dsc'), .5, 40);
   tl.to($('.w0'), {color: '#17130D', duration: .25}, 1.06); tl.fromTo($('.h0'), {opacity: 1, scaleX: 0}, {scaleX: 1, duration: .45, ease: 'power2.out'}, 1.06); pop(tl, $('.tg0'), 1.3, .5);
   tl.to($('.w1'), {color: '#17130D', duration: .25}, 2.46); tl.fromTo($('.h1'), {opacity: 1, scaleX: 0}, {scaleX: 1, duration: .45, ease: 'power2.out'}, 2.46); pop(tl, $('.tg1'), 2.7, .5);
   tl.to($('.w2'), {color: '#4A3AE0', duration: .25}, 4.36); tl.fromTo($('.th'), {opacity: 0, y: 60, scale: .7}, {opacity: 1, y: 0, scale: 1, duration: .55, ease: 'back.out(1.6)'}, 4.36);
   glide(tl, $('.cur'), 6.2, 1640, 790, .7); click(tl, $('.th'), 7.06);
 }},

{id: 's72', clip: 'clips/s72.mp4', dur: 4.4, poster: 4.2, name: 'Nhiều thumbnail, <em>A/B test</em>',
 desc: '6 thumbnail thật hệ thống làm cho chính video này xếp ra ở chữ "tạo ra nhiều thumbnail"; "AB testing" thì 3 bản gắn nhãn A, B, C, các bản còn lại mờ đi, thanh lượt xem chạy song song.',
 html: () => BG + title(610, 100, 'Nhiều thumbnail, <em>A/B test</em>', 'để YouTube chọn bản thắng') +
   [1, 2, 3, 4, 5, 6].map((n, j) => `<div class="tc tc${j}" style="left:${136 + (j%3)*324}px;top:${330 + Math.floor(j/3)*262}px;width:300px;height:169px;border-radius:16px;overflow:hidden;box-shadow:var(--shadow);border:2px solid #fff">
     <img src="img/g1-t${n}.jpg" style="left:0;top:0;width:100%;height:100%;object-fit:cover"></div>`).join('') +
   ['A', 'B', 'C'].map((k, j) => `<div class="badge ab ab${j}" style="left:${120 + j*324}px;top:312px;width:56px;height:56px;background:var(--plum);font:800 28px Disp;opacity:0">${k}</div>
     <div class="bt" style="left:${136 + j*324}px;top:514px;width:300px;height:12px;border-radius:6px;background:var(--line);opacity:0"><i class="bf bf${j}" style="left:0;top:0;height:12px;width:300px;border-radius:6px;background:${['var(--plum)', 'var(--gold)', 'var(--plum2)'][j]};transform-origin:0 50%"></i></div>`).join(''),
 anim(tl, $, f, v) {
   startAt(tl, f, v, CARD.L); move(tl, f, v, CARD.R, .1);
   rise(tl, $('.ttl h2'), .45); tl.set($('.ttl p'), {opacity: 0}, 0); rise(tl, $('.ttl p'), 3.3, 12);
   $$('.tc').forEach((e, j) => tl.fromTo(e, {opacity: 0, y: 40, scale: .75, rotation: (j%2 ? 6 : -6)}, {opacity: 1, y: 0, scale: 1, rotation: 0, duration: .5, ease: 'back.out(1.5)'}, 1.5 + j*.08));
   $$('.ab').forEach((e, j) => pop(tl, e, 3.0 + j*.1, .3)); dim(tl, [$('.tc3'), $('.tc4'), $('.tc5')], 3.0, .28);
   tl.to($$('.bt'), {opacity: 1, duration: .2}, 3.3); [.62, .85, .48].forEach((w, j) => tl.fromTo($('.bf' + j), {scaleX: 0}, {scaleX: w, duration: .9, ease: 'power2.out'}, 3.35 + j*.05));
 }},

{id: 's73', clip: 'clips/s73.mp4', dur: 12.0, poster: 11.6, name: 'Kênh phụ khoá → <em>xem ở mô tả</em>',
 desc: '"Kênh YouTube khác" bật thẻ Kênh phụ (thumbnail che mờ), "kênh chính" bật thẻ kênh Thành Vũ Đức, "không show" khoá thẻ kênh phụ. "Lát nữa" chuyển sang khung mô tả, "thumbnail mẫu" tô dòng link, "bên dưới" mũi tên nảy xuống.',
 html: () => BG + `<div class="p1">${title(1330, 100, 'Kênh <em>phụ</em> của mình', 'không phải kênh chính')}
   <div class="kp paper" style="left:880px;top:300px;width:900px;height:330px;border-radius:26px">
     <div style="left:30px;top:26px;width:70px;height:70px;border-radius:50%;background:var(--ivory-deep);border:2px solid var(--line)"></div>
     <div style="left:118px;top:28px;font:800 32px Disp;letter-spacing:-.02em">Kênh phụ</div><div class="sub" style="left:118px;top:70px">thumbnail làm bằng cùng hệ thống</div>
     ${['g1-t4.jpg', 'cap-thumb.jpg', 'g1-t6.jpg', 'rea-t1.jpg'].map((im, j) => `<div style="left:${30 + j*212}px;top:130px;width:196px;height:110px;border-radius:12px;overflow:hidden"><img class="sk" src="img/${im}" style="left:-10px;top:-10px;width:216px;height:130px;object-fit:cover;filter:blur(7px)"></div>`).join('')}
     ${[0, 1, 2, 3].map(j => LN(30 + j*212, 256, 160) + LN(30 + j*212, 280, 100, 'rgba(23,19,13,.07)')).join('')}
     <div class="lk" style="left:390px;top:110px;width:120px;height:120px;border-radius:50%;background:var(--peach);color:#17130D;display:grid;place-items:center;box-shadow:0 10px 30px -10px rgba(23,19,13,.4);opacity:0">${IC('eye', 54)}<i style="left:22px;top:57px;width:76px;height:6px;border-radius:3px;background:#17130D;rotate:-40deg"></i></div>
     ${TAG('ns', 520, 150, 'Không show được', '#E2654A')}</div>
   <div class="kc paper" style="left:880px;top:680px;width:900px;height:150px;border-radius:26px">
     <img src="img/chan-avatar.png" style="left:30px;top:30px;width:90px;height:90px;border-radius:50%">
     <div style="left:142px;top:34px;font:800 34px Disp;letter-spacing:-.02em">Thành Vũ Đức</div><div class="sub" style="left:142px;top:82px">kênh chính, video này</div>
     <div class="ck badge" style="right:30px;top:49px;background:var(--plum)">${IC('check', 26)}</div></div></div>
   <div class="p2">${title(1330, 100, 'Thumbnail mẫu ở <em>mô tả</em>', 'link ngay dưới video')}
   <div class="ds paper" style="left:900px;top:300px;width:860px;height:420px;border-radius:26px">
     <div style="left:34px;top:28px;font:800 28px Disp;letter-spacing:-.02em">Mô tả</div>
     ${LN(34, 90, 600)}${LN(34, 122, 480)}${LN(34, 154, 540)}
     <i class="hl" style="left:22px;top:196px;width:816px;height:64px;border-radius:14px;background:rgba(183,168,255,.35);transform-origin:0 50%"></i>
     <div class="ml" style="left:34px;top:208px;display:flex;align-items:center;gap:12px;font:700 26px Body;color:var(--ink)"><span style="position:static;color:var(--plum)">${IC('link', 28)}</span>Thumbnail mẫu kênh phụ: <span style="position:static;color:var(--plum)">link</span></div>
     ${LN(34, 292, 560)}${LN(34, 324, 420)}${LN(34, 356, 500)}</div>
   <div class="dn badge" style="left:1270px;top:760px;width:110px;height:110px;background:var(--plum)"><span style="position:static;rotate:180deg;display:block">${IC('up', 56)}</span></div></div>`,
 anim(tl, $, f, v) {
   startAt(tl, f, v, CARD.R); move(tl, f, v, CARD.L, .1);
   rise(tl, $('.p1 .ttl h2'), .45); tl.set($('.p1 .ttl p'), {opacity: 0}, 0); rise(tl, $('.p1 .ttl p'), 3.2, 12);
   rise(tl, $('.kp'), 1.6, 40); rise(tl, $('.kc'), 3.2, 40); pop(tl, $('.kc .ck'), 3.5, .3);
   tl.to($$('.kp .sk'), {filter: 'blur(16px)', opacity: .75, duration: .4}, 4.6); pop(tl, $('.lk'), 4.6, .4); pop(tl, $('.ns'), 4.85, .5);
   fadeOut(tl, [$('.p1 .ttl'), $('.kp'), $('.kc')], 8.0);
   tl.set($('.p2'), {opacity: 0}, 0); tl.set($('.p2'), {opacity: 1}, 8.3); rise(tl, $('.p2 .ttl'), 8.35); rise(tl, $('.ds'), 8.45, 40);
   tl.set($('.hl'), {scaleX: 0}, 0); draw(tl, $('.hl'), 9.6, .45);
   pop(tl, $('.dn'), 11.0, .5); [11.4].forEach(t => { tl.to($('.dn'), {y: 24, duration: .22, ease: 'power2.in'}, t); tl.to($('.dn'), {y: 0, duration: .3, ease: 'power2.out'}, t + .22); });
 }},

{id: 's74', clip: 'clips/s74.mp4', dur: 8.0, poster: 7.6, name: 'Chạy thử + <em>tắt tiếng</em>',
 desc: 'Trình xem bản edit thật của video REA. "Chạy" con trỏ bấm play, khung hình đổi theo các kiểu edit (B-roll 3D, slide) và chip style sáng lần lượt ở "style edit"; "tắt tiếng" con trỏ bấm loa, sóng âm xẹp; "bật video" hiện nhãn đang phát không tiếng.',
 html: () => {
   const FR = ['rea-330.jpg', 'rea-396.jpg', 'rea-408.jpg', 'rea-600.jpg'];
   let wave = ''; for (let k = 0; k < 92; k++) { const h = 10 + Math.abs(Math.sin(k*1.7) + Math.sin(k*.53))*24; wave += `<i class="wv" style="left:${k*11.6}px;top:${45 - h/2}px;width:6px;height:${h}px;border-radius:3px;background:var(--plum2)"></i>`; }
   return BG + WIN('pl', 360, 50, 1500, 980, `
     <div class="pv" style="left:36px;top:70px;width:1060px;height:596px;border-radius:16px;overflow:hidden;background:#000">
       ${FR.map((im, j) => `<img class="fr fr${j}" src="img/${im}" style="left:0;top:0;width:100%;height:100%;object-fit:cover;opacity:${j ? 0 : 1}">`).join('')}
       <div class="pb" style="left:470px;top:238px;width:120px;height:120px;border-radius:50%;background:rgba(255,255,255,.9);display:grid;place-items:center;box-shadow:0 10px 30px rgba(0,0,0,.35)"><svg viewBox="0 0 24 24" style="width:52px;height:52px;margin-left:8px"><path d="M6 4l14 8-14 8z" fill="#17130D"/></svg></div>
       ${TAG('np', 22, 22, '<i style="position:static;width:10px;height:10px;border-radius:50%;background:#fff"></i>Đang phát, không tiếng', 'rgba(23,19,13,.7)')}</div>
     <div style="left:36px;top:684px;width:1060px;height:52px;display:flex;align-items:center;gap:18px">
       <div style="position:relative;width:24px;height:24px"><svg viewBox="0 0 24 24" style="width:24px;height:24px"><path d="M6 4l14 8-14 8z" fill="#17130D"/></svg></div>
       <div style="position:relative;flex:1;height:8px;border-radius:4px;background:var(--line)"><i class="pg" style="left:0;top:0;height:8px;width:100%;border-radius:4px;background:var(--plum);transform-origin:0 50%"></i></div>
       <div class="spk" style="position:relative;width:48px;height:48px;border-radius:12px;display:grid;place-items:center;color:var(--ink)">
         <svg viewBox="0 0 24 24" style="width:30px;height:30px" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H2v6h4l5 4z" fill="currentColor"/><path class="sw1" d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/><path class="sx" d="M16 9l6 6M22 9l-6 6" style="opacity:0"/></svg></div></div>
     <div class="tln" style="left:36px;top:756px;width:1060px;height:190px;border-radius:16px;background:var(--ivory);border:1px solid var(--line)">
       <div style="left:14px;top:22px;font:700 15px Mono;color:var(--ink-muted)">V1</div><div style="left:14px;top:120px;font:700 15px Mono;color:var(--ink-muted)">A1</div>
       <div style="left:56px;top:12px;width:990px;height:72px;display:flex;gap:4px;overflow:hidden;border-radius:8px">${[0, 1, 2, 3, 0, 1, 2, 3].map(j => `<img src="img/${FR[j]}" style="position:static;width:121px;height:72px;object-fit:cover;flex:none">`).join('')}</div>
       <div class="wvb" style="left:56px;top:96px;width:990px;height:90px;overflow:hidden">${wave}</div>
       <i class="ph" style="left:56px;top:4px;width:3px;height:182px;background:#E2654A;border-radius:2px"></i></div>
     <div style="left:1124px;top:70px;font:700 15px Body;letter-spacing:.16em;color:var(--ink-muted)">STYLE EDIT</div>
     ${[['film', 'B-roll 3D'], ['user', 'Mặt góc nhỏ'], ['layers', 'Slide vẽ tay'], ['image', 'Thumbnail']].map(([i, n], j) =>
       `<div class="sc sc${j}" style="left:1124px;top:${110 + j*92}px;width:340px;height:76px;border-radius:18px;border:2px solid var(--line-strong);background:#fff;display:flex;align-items:center;gap:14px;padding:0 18px;font:800 24px Disp;letter-spacing:-.02em;color:var(--ink-muted)"><span style="position:static;display:grid">${IC(i, 28)}</span>${n}</div>`).join('')}
     ${TAG('mt', 1124, 690, IC('x', 18) + 'Tắt tiếng', '#E2654A')}`, 'Xem thử: rea-yt_final.mp4') + CUR('cur', 1100, 1080);
 },
 anim(tl, $, f, v) {
   startAt(tl, f, v, CARD.L); move(tl, f, v, CARD.BL, .1);
   rise(tl, $('.pl'), .35, 40);
   glide(tl, $('.cur'), .7, 950, 580, .6); click(tl, $('.pb'), 1.4); tl.to($('.pb'), {opacity: 0, scale: 1.3, duration: .3}, 1.5);
   [[1, 2.6], [2, 3.8], [3, 5.0], [0, 6.2], [1, 7.3]].forEach(([j, t]) => { tl.set($$('.fr'), {opacity: 0}, t); tl.set($('.fr' + j), {opacity: 1}, t); });
   tl.fromTo($('.pg'), {scaleX: 0}, {scaleX: .55, duration: 6.6, ease: 'none'}, 1.4);
   tl.fromTo($('.ph'), {x: 0}, {x: 545, duration: 6.6, ease: 'none'}, 1.4);
   [[0, 2.6], [1, 2.9], [2, 3.8], [3, 5.0]].forEach(([j, t]) => lit(tl, $('.sc' + j), t));
   tl.to($$('.sc'), {color: '#4A3AE0', duration: .2}, 5.2);
   glide(tl, $('.cur'), 3.6, 1408, 790, .6); click(tl, $('.spk'), 4.3);
   tl.to($('.spk'), {backgroundColor: 'rgba(226,101,74,.15)', color: '#E2654A', duration: .2}, 4.3); tl.set($('.sw1'), {opacity: 0}, 4.3); tl.set($('.sx'), {opacity: 1}, 4.3);
   tl.to($$('.wv'), {scaleY: .12, opacity: .35, duration: .35, ease: 'power2.out'}, 4.35); pop(tl, $('.mt'), 4.45, .5);
   glide(tl, $('.cur'), 5.0, 1900, 1100, .7); pop(tl, $('.np'), 6.7, .6);
 }},

{id: 's75', clip: 'clips/s75.mp4', dur: 8.84, poster: 6.9, name: 'Chỉnh da: <em>thanh trượt</em>',
 desc: 'Khung hình thật của video REA trong bảng chỉnh da. "Chỉnh lại" bảng beauty.py hiện, thanh làm mịn kéo lên; "da" khoanh vùng mặt; "dở hơn" kính lúp soi da; "chỉnh nhẹ nhàng" núm trượt về mức Nhẹ, tick xanh. Cuối cảnh mặt về full để nối s44.',
 html: () => BG + title(610, 70, 'AI chỉnh <em>da</em>', 'nhẹ thôi, vẫn là mặt thật') +
   `<div class="fm paper" style="left:120px;top:220px;width:980px;height:551px;border-radius:22px;overflow:hidden">
     <img src="img/rea-12.jpg" style="left:0;top:0;width:980px;height:551px;object-fit:cover">
     <i class="ov" style="left:438px;top:137px;width:180px;height:230px;border-radius:50%;border:4px dashed #fff;box-shadow:0 0 0 3px rgba(74,58,224,.7);opacity:0"></i></div>
   <div class="mg" style="left:770px;top:150px;width:300px;height:300px;border-radius:50%;overflow:hidden;border:6px solid #fff;box-shadow:0 0 0 4px var(--plum),0 24px 50px -16px rgba(23,19,13,.5);opacity:0">
     <img src="img/rea-12.jpg" style="left:-1434px;top:-621px;width:2940px;height:1653px"></div>
   ${TAG('mgl', 840, 466, IC('search', 18) + 'Soi gần', 'var(--ink)')}
   <div class="pn paper" style="left:120px;top:800px;width:980px;height:200px;border-radius:24px">
     <div style="left:32px;top:26px;display:flex;align-items:center;gap:12px;font:800 28px Disp;letter-spacing:-.02em"><span style="position:static;color:var(--plum);display:grid">${IC('sparkles', 28)}</span>Chỉnh da<span style="position:static;font:600 18px Mono;color:var(--ink-muted)">beauty.py</span></div>
     <div class="vl" style="right:32px;top:24px;padding:6px 16px;border-radius:999px;background:rgba(183,168,255,.3);color:var(--plum);font:700 20px Body"><span class="v0" style="position:relative">Gốc</span><span class="v1" style="left:16px;top:6px;opacity:0">Mạnh</span><span class="v2" style="left:16px;top:6px;opacity:0">Nhẹ</span></div>
     <div style="left:32px;top:96px;font:700 20px Body;color:var(--ink-soft)">Làm mịn</div>
     <div style="left:180px;top:104px;width:760px;height:10px;border-radius:5px;background:var(--line)"><i class="fl" style="left:0;top:0;width:760px;height:10px;border-radius:5px;background:var(--plum);transform-origin:0 50%"></i></div>
     <div class="kn" style="left:166px;top:94px;width:30px;height:30px;border-radius:50%;background:#fff;border:3px solid var(--plum);box-shadow:0 3px 8px rgba(0,0,0,.2)"></div>
     ${[['Gốc', 0], ['Nhẹ', .3], ['Vừa', .6], ['Mạnh', 1]].map(([n, p]) => `<div style="left:${180 + p*760 - 40}px;top:140px;width:80px;text-align:center;font:600 17px Body;color:var(--ink-muted)">${n}</div>`).join('')}
     <div class="ok badge" style="left:930px;top:-20px;background:var(--sage);color:#17130D;opacity:0">${IC('check', 26)}</div></div>`,
 anim(tl, $, f, v) {
   startAt(tl, f, v, CARD.BL); move(tl, f, v, CARD.R, .1);
   rise(tl, $('.ttl h2'), .4); tl.set($('.ttl p'), {opacity: 0}, 0); rise(tl, $('.ttl p'), 6.6, 12);
   rise(tl, $('.fm'), .5, 40); rise(tl, $('.pn'), 2.1, 30);
   const knob = (p, t, d, lab) => { tl.to($('.kn'), {x: p*760, duration: d, ease: 'power2.inOut'}, t); tl.to($('.fl'), {scaleX: p, duration: d, ease: 'power2.inOut'}, t);
     tl.set($$('.vl span'), {opacity: 0}, t + d*.6); tl.set($('.' + lab), {opacity: 1}, t + d*.6); };
   tl.set($('.fl'), {scaleX: 0}, 0); knob(.85, 2.3, 1.0, 'v1');
   tl.fromTo($('.ov'), {opacity: 0, scale: .7}, {opacity: 1, scale: 1, duration: .45, ease: 'back.out(1.8)'}, 2.5);
   tl.fromTo($('.mg'), {opacity: 0, scale: .4}, {opacity: 1, scale: 1, duration: .5, ease: 'back.out(1.6)'}, 4.7); pop(tl, $('.mgl'), 4.9, .5);
   tl.to([$('.mg'), $('.mgl')], {opacity: 0, scale: .8, duration: .3}, 6.3);
   knob(.3, 6.5, .8, 'v2'); pop(tl, $('.ok'), 7.2, .3);
   move(tl, f, v, FULL, 8.29, .5);
 }},

{id: 's76', clip: 'clips/s76.mp4', dur: 6.86, poster: 6.2, name: 'Skill youtube = <em>hệ thống</em>',
 desc: 'Nối từ s53 (mặt phải trượt sang trái). "Skill" bật thư mục skill youtube thật với các file; "hệ thống youtube" đổi tiêu đề; "làm cái gì" hiện 4 bước mờ; "Đầu tiên" bước Sườn sáng plum.',
 html: () => BG + `<div class="t0">${title(1330, 100, 'Skill <em>youtube</em>', 'một thư mục trong Claude Code')}</div><div class="t1">${title(1330, 100, 'Hệ thống <em>YouTube AI</em>', 'cũng chính là skill này')}</div>` +
   `<div class="fd paper" style="left:900px;top:290px;width:860px;height:400px;border-radius:24px;overflow:hidden">
     <div style="left:0;right:0;top:0;height:64px;background:var(--ivory);border-bottom:1px solid var(--line);display:flex;align-items:center;gap:12px;padding:0 26px;font:700 22px Mono"><span style="position:static;color:var(--gold);display:grid">${IC('folder', 26)}</span>~/.claude/skills/youtube</div>
     ${[['file', 'SKILL.md', 1], ['file', 'references/description.md'], ['file', 'references/thumbnail.md'], ['folder', 'template/cut/'], ['folder', 'template/thumbnail/'], ['code', 'template/update_description.py'], ['code', 'template/upload_youtube.py']].map(([i, n, b], j) =>
       `<div class="fr" style="left:26px;top:${82 + j*43}px;display:flex;align-items:center;gap:12px;font:${b ? 700 : 500} 21px Mono;color:${b ? 'var(--plum)' : 'var(--ink-soft)'}"><span style="position:static;display:grid;color:var(--ink-muted)">${IC(i, 22)}</span>${n}</div>`).join('')}</div>` +
   [['file', 'Sườn'], ['video', 'Quay'], ['wand', 'Edit'], ['eye', 'Duyệt']].map(([i, n], j) =>
     `<div class="sp sp${j}" style="left:${900 + j*220}px;top:730px;width:200px;height:84px;border-radius:22px;border:2px solid var(--line-strong);background:#fff;display:flex;align-items:center;gap:12px;padding:0 18px;color:var(--ink-muted)">
       <div class="nb" style="position:relative;width:40px;height:40px;border-radius:50%;background:var(--ink-faint);color:#fff;display:grid;place-items:center;font:800 20px Disp">${j + 1}</div>
       <span style="position:static;font:800 26px Disp;letter-spacing:-.02em">${n}</span></div>`).join(''),
 anim(tl, $, f, v) {
   startAt(tl, f, v, cardOf('s53', 'R')); move(tl, f, v, CARD.L, .2);
   rise(tl, $('.t0 .ttl'), .6); rise(tl, $('.fd'), .76, 40); $$('.fd .fr').forEach((e, j) => tl.fromTo(e, {opacity: 0, x: -14}, {opacity: 1, x: 0, duration: .3}, .95 + j*.07));
   tl.set($('.t1'), {opacity: 0}, 0); fadeOut(tl, $('.t0 .ttl'), 2.2); tl.set($('.t1'), {opacity: 1}, 2.36); rise(tl, $('.t1 .ttl'), 2.36);
   $$('.sp').forEach((e, j) => rise(tl, e, 3.66 + j*.08, 24));
   tl.to($('.sp0'), {borderColor: '#4A3AE0', backgroundColor: 'rgba(183,168,255,.3)', color: '#4A3AE0', duration: .25}, 4.16);
   tl.to($('.sp0 .nb'), {backgroundColor: '#4A3AE0', duration: .25}, 4.16); tl.fromTo($('.sp0'), {scale: 1.14}, {scale: 1, duration: .45, ease: 'back.out(2)'}, 4.16);
   dim(tl, [$('.sp1'), $('.sp2'), $('.sp3')], 4.16, .45);
 }},

{id: 's77', clip: 'clips/s77.mp4', dur: 10.4, poster: 10.0, name: 'Claude <em>lên sườn</em>',
 desc: 'Giao diện Claude Code: "call" ô nhập sáng, gõ yêu cầu lên sườn, gửi. Claude trả sườn: "code hook" dòng Hook sáng, "những phần gì" hiện Phần 1-3, "gạch đầu dòng" hiện các gạch, "mục" tô các gạch.',
 html: () => BG + CLAUDE(`
   <div class="ub" style="right:60px;top:26px;max-width:700px;padding:14px 20px;border-radius:18px;background:var(--ivory-deep);font-size:19px;opacity:0">lên sườn video "Hệ thống YouTube AI", có hook</div>
   ${CLAUDEMSG('cm', 96, 'Sườn video, mỗi phần có gạch đầu dòng để bạn nói theo:')}
   <div class="doc paper" style="left:96px;top:144px;width:880px;height:392px;border-radius:16px">
     <div class="hk" style="left:18px;top:16px;width:844px;height:52px;border-radius:12px;display:flex;align-items:center;gap:12px;padding:0 14px;font:700 20px Body">
       <span style="position:static;padding:3px 10px;border-radius:8px;background:var(--plum);color:#fff;font:700 15px Body">HOOK</span>Quay xong là xong, AI edit hết</div>
     ${[['Phần 1: Kết quả thật', 'video REA 11.000 view, CapCut AI'], ['Phần 2: Hệ thống làm gì', 'sườn → quay → edit → duyệt'], ['Phần 3: Cài skill', 'link tải ở mô tả']].map(([h, b], j) =>
       `<div class="ph ph${j}" style="left:32px;top:${86 + j*102}px;font:800 22px Disp;letter-spacing:-.01em">${h}</div>
        <i class="mk mk${j}" style="left:44px;top:${122 + j*102}px;width:${b.length*10.2 + 30}px;height:34px;border-radius:8px;background:rgba(230,180,90,.35);transform-origin:0 50%"></i>
        <div class="bl bl${j}" style="left:52px;top:${126 + j*102}px;font:18px Body;color:var(--ink-soft);white-space:nowrap">• ${b}</div>`).join('')}</div>
   ${INPUT('inp', 560, `<div class="tx" style="left:22px;top:22px;font-size:20px;white-space:nowrap">${chars('lên sườn video "Hệ thống YouTube AI", có hook', 'k')}</div>`)}`),
 anim(tl, $, f, v) {
   startAt(tl, f, v, CARD.L); move(tl, f, v, CARD.BL, .1);
   rise(tl, $('.cw'), .2, 30);
   tl.to($('.inp'), {borderColor: '#4A3AE0', boxShadow: '0 0 0 6px rgba(123,108,255,.18)', duration: .3}, .3);
   type(tl, '.k', .5, 1.4); tl.set($('.snd'), {backgroundColor: '#4A3AE0'}, 1.45); click(tl, $('.snd'), 1.6);
   tl.set($('.tx'), {opacity: 0}, 1.7); rise(tl, $('.ub'), 1.7, 14);
   tl.to($('.inp'), {borderColor: 'rgba(23,19,13,.16)', boxShadow: '0 0 0 0 rgba(123,108,255,0)', duration: .3}, 1.8); tl.set($('.snd'), {backgroundColor: '#BDB4A6'}, 1.8);
   rise(tl, $('.cm'), 2.0, 12); rise(tl, $('.doc'), 2.2, 20);
   tl.set($$('.ph, .bl'), {opacity: 0}, 0); tl.set($$('.mk'), {scaleX: 0}, 0); tl.set($('.hk'), {opacity: 0}, 0);
   tl.fromTo($('.hk'), {opacity: 0, x: -14}, {opacity: 1, x: 0, duration: .35}, 2.8); tl.to($('.hk'), {backgroundColor: 'rgba(183,168,255,.3)', duration: .3}, 2.9);
   $$('.ph').forEach((e, j) => rise(tl, e, 4.4 + j*.15, 12));
   $$('.bl').forEach((e, j) => tl.fromTo(e, {opacity: 0, x: -12}, {opacity: 1, x: 0, duration: .3}, 8.0 + j*.15));
   $$('.mk').forEach((e, j) => draw(tl, e, 9.1 + j*.15, .35));
 }},

{id: 's78', clip: 'clips/s78.mp4', dur: 7.4, poster: 7.0, name: 'Lười thì <em>freestyle</em>',
 desc: '"Lười" công tắc Lên sườn trước đang bật, "không lên sườn" gạt tắt, "freestyle" đổi tiêu đề, "điện thoại" bật khung điện thoại đang quay (khung hình thật), "nói" sóng âm chạy, "ổn" tick xanh Vẫn ổn.',
 html: () => { let bars = ''; for (let k = 0; k < 26; k++) bars += `<i class="br" style="left:${110 + k*15}px;top:30px;width:8px;height:60px;border-radius:4px;background:var(--plum2);transform-origin:50% 50%"></i>`;
   return BG + `<div class="t0">${title(610, 110, 'Không có <em>sườn</em>?', 'lười thì bỏ bước này')}</div><div class="t1">${title(610, 110, 'Cứ <em>freestyle</em>', 'bật điện thoại lên rồi nói')}</div>` +
   `<div class="tg paper" style="left:120px;top:390px;width:560px;height:130px;border-radius:26px">
     <div style="left:32px;top:24px;font:800 30px Disp;letter-spacing:-.02em">Lên sườn trước</div><div class="sub" style="left:32px;top:70px">bước 1, không bắt buộc</div>
     <div class="sw" style="left:420px;top:37px;width:108px;height:56px;border-radius:28px;background:var(--plum)"><div class="kb" style="left:56px;top:4px;width:48px;height:48px;border-radius:50%;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.2)"></div></div></div>
   <div class="mc paper" style="left:120px;top:560px;width:560px;height:120px;border-radius:26px">
     <div style="left:30px;top:30px;width:60px;height:60px;border-radius:18px;background:rgba(183,168,255,.3);color:var(--plum);display:grid;place-items:center">${IC('mic', 32)}</div>${bars}</div>` +
   PHONE('ph', 760, 250, 340, 680, 'f1-s1.jpg') +
   `<div class="ok" style="left:120px;top:720px;display:flex;align-items:center;gap:12px;padding:14px 28px;border-radius:999px;background:var(--sage);font:800 32px Disp;white-space:nowrap;opacity:0">${IC('check', 24)}Vẫn ổn</div>`; },
 anim(tl, $, f, v) {
   startAt(tl, f, v, CARD.BL); move(tl, f, v, CARD.R, .1);
   rise(tl, $('.t0 .ttl h2'), .45); tl.set($('.t0 .ttl p'), {opacity: 0}, 0); rise(tl, $('.t0 .ttl p'), 1.1, 12);
   rise(tl, $('.tg'), .6, 30);
   tl.to($('.sw'), {backgroundColor: '#BDB4A6', duration: .3}, 2.3); tl.to($('.kb'), {x: -52, duration: .35, ease: 'back.out(1.6)'}, 2.3);
   tl.to($('.tg'), {opacity: .55, duration: .3}, 2.7);
   tl.set($('.t1'), {opacity: 0}, 0); fadeOut(tl, $('.t0 .ttl'), 2.75); tl.set($('.t1'), {opacity: 1}, 3.0); rise(tl, $('.t1 .ttl h2'), 3.0);
   tl.set($('.t1 .ttl p'), {opacity: 0}, 0); rise(tl, $('.t1 .ttl p'), 4.2, 12);
   tl.fromTo($('.ph'), {opacity: 0, y: 80, rotation: 6, scale: .85}, {opacity: 1, y: 0, rotation: -3, scale: 1, duration: .6, ease: 'back.out(1.4)'}, 4.2);
   [4.6, 5.4, 6.2, 7.0].forEach(t => tl.to($('.rd'), {opacity: .2, duration: .2, yoyo: true, repeat: 1}, t));
   rise(tl, $('.mc'), 4.8, 24);
   $$('.br').forEach((e, k) => tl.fromTo(e, {scaleY: .12}, {scaleY: .25 + .75*Math.abs(Math.sin(k*1.3)), duration: .22, yoyo: true, repeat: 11, ease: 'sine.inOut'}, 5.0 + (k%5)*.04));
   tl.fromTo($('.ok'), {opacity: 0, scale: .5}, {opacity: 1, scale: 1, duration: .45, ease: 'back.out(1.8)'}, 6.3);
 }},

{id: 's79', clip: 'clips/s79.mp4', dur: 4.64, poster: 3.9, name: 'Bước 2: <em>quay</em>',
 desc: '"Cái thứ 2" bật số 2 và tiêu đề Quay, "OBS" thẻ máy tính sáng, "điện thoại" thẻ điện thoại sáng. Cuối cảnh mặt về full để nối s02.',
 html: () => BG + `<div class="n2 badge" style="left:1060px;top:104px;width:76px;height:76px;background:var(--plum);font:800 44px Disp">2</div>` +
   `<div class="ttl" style="left:1380px;top:100px"><h2>Bước 2: <em>quay</em></h2><p>quay bằng 2 thứ</p></div>` +
   `<div class="dv dv0 paper" style="left:880px;top:330px;width:420px;height:400px;border-radius:28px">
     <div class="tb" style="left:110px;top:50px;width:200px;height:150px;border-radius:30px;border:2.5px solid var(--line-strong);display:grid;place-items:center;color:var(--ink-muted)">${IC('monitor', 92)}</div>
     <div style="left:0;right:0;top:236px;text-align:center;font:800 44px Disp;letter-spacing:-.02em">OBS</div><div class="sub" style="left:0;right:0;top:300px;text-align:center">trên máy tính</div></div>
   <div class="dv dv1 paper" style="left:1340px;top:330px;width:420px;height:400px;border-radius:28px">
     <div class="tb" style="left:110px;top:50px;width:200px;height:150px;border-radius:30px;border:2.5px solid var(--line-strong)"></div>
     ${PHONE('pp', 176, 38, 68, 136, 'f1-s2.jpg', false)}
     <div style="left:0;right:0;top:236px;text-align:center;font:800 44px Disp;letter-spacing:-.02em">Điện thoại</div><div class="sub" style="left:0;right:0;top:300px;text-align:center">quay mặt</div></div>`,
 anim(tl, $, f, v) {
   startAt(tl, f, v, CARD.R); move(tl, f, v, CARD.L, .1);
   pop(tl, $('.n2'), .7, .3); rise(tl, $('.ttl'), .75);
   $$('.dv').forEach((e, j) => rise(tl, e, .9 + j*.1, 40)); tl.to($$('.dv'), {opacity: .5, duration: .2}, 1.5);
   [[0, 2.9], [1, 3.5]].forEach(([j, t]) => { tl.to($('.dv' + j), {opacity: 1, duration: .2}, t); lit(tl, $('.dv' + j), t); });
   move(tl, f, v, FULL, 4.09, .5);
 }},

);
}
