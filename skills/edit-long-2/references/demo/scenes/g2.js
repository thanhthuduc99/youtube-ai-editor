// Scenes s81-s89: fill the plain-face gaps 290-301, 307-327, 351-371, 383-390, 401-424 (gap-B). Times are seconds from scene start, each beat on its word.
(() => {
const EB = (x, y, t, c = 'var(--ink-muted)') => `<div style="left:${x}px;top:${y}px;font:700 14px Body;letter-spacing:.16em;color:${c};white-space:nowrap">${t}</div>`;
const CHK = (cls, x, y, sz = 40, col = 'var(--plum)') => `<div class="badge ${cls}" style="left:${x}px;top:${y}px;width:${sz}px;height:${sz}px;background:${col};opacity:0">${IC('check', sz*.5)}</div>`;
const WAVE = (n, seed, w = 6, gap = 4) => Array.from({length: n}, (_, i) => `<i style="position:static;display:inline-block;flex:none;width:${w}px;margin-right:${gap}px;border-radius:3px;background:currentColor;height:${10 + Math.round(24*Math.abs(Math.sin(i*1.7 + seed)) + 12*Math.abs(Math.sin(i*.6 + seed*2)))}px"></i>`).join('');
const SUB = (cls, x, y, t) => `<div class="${cls}" style="left:${x - 600}px;top:${y}px;width:1200px;text-align:center;font-size:28px;color:var(--ink-soft)">${t}</div>`;
const LIT = (tl, el, t, col = '#4A3AE0', fill = 'rgba(183,168,255,.3)') => { const b = el.querySelector('.tb') || el;
  tl.to(b, {borderColor: col, backgroundColor: fill, color: col, scale: 1.12, duration: .12}, t); tl.to(b, {scale: 1, duration: .4, ease: 'back.out(2)'}, t + .12); };
const WORDS = (s, cls) => s.split(' ').map(w => `<span style="position:relative;display:inline-block;white-space:nowrap">${chars(w, cls)}</span>`).join(' ');
const fade = (tl, els, t, y = -18) => tl.to(els, {opacity: 0, y, duration: .3, ease: 'power2.in'}, t);

SCENES.push(
{id: 's81', clip: 'clips/s81.mp4', dur: 10, poster: 9.7, name: 'Tự đăng YouTube → <em>nhảy qua kịch bản</em>',
 desc: 'Trang tải video lên: thanh tải chạy ở "tự động đăng", logo YouTube bật ở "YouTube", thumbnail thật rơi vào ô ở "thumbnail", mô tả gõ dần ở "description". Rồi hàng 4 công đoạn: "Kịch bản" sáng, slide kịch bản thật hiện ở "slide", bị gạch ở "không cần", mũi tên nhảy sang "Quay" ở "nhảy đến".',
 html: () => BG + `<div class="p1">${title(610, 90, 'AI tự <em>đăng</em> luôn', 'kèm thumbnail và description')}</div>
   <div class="p2">${title(610, 90, 'Khâu <em>kịch bản</em>')}</div>${SUB('p2s', 610, 182, 'không cần, nhảy thẳng tới Record')}` +
   WIN('up', 110, 260, 1000, 560, `
     ${EB(34, 74, 'TIÊU ĐỀ')}
     <div style="left:34px;top:98px;width:560px;height:60px;border-radius:12px;border:1.5px solid var(--line-strong);font:600 19px Body;line-height:57px;padding:0 16px;white-space:nowrap;overflow:hidden">Hệ thống YouTube AI: quay xong, AI edit hết</div>
     ${EB(34, 182, 'MÔ TẢ')}
     <div class="ds" style="left:34px;top:206px;width:560px;height:190px;border-radius:12px;border:1.5px solid var(--line-strong);padding:14px 16px;font:19px/1.55 Body;color:var(--ink-soft)">${WORDS('Quay 1 lần, phần còn lại AI làm: cắt vấp, B-roll, thumbnail, rồi đăng lên YouTube.', 'k')}</div>
     ${CHK('ck2', 572, 190)}
     ${EB(630, 74, 'THUMBNAIL')}
     <div class="slot" style="left:630px;top:98px;width:336px;height:189px;border-radius:14px;border:2px dashed var(--line-strong);display:grid;place-items:center;color:var(--ink-faint);overflow:hidden">${IC('image', 44)}<img class="tn" src="img/g2-t5.jpg" style="left:0;top:0;width:100%;height:100%;object-fit:cover;opacity:0"></div>
     ${CHK('ck1', 944, 80)}
     <div class="pl" style="left:630px;top:318px;font:700 17px Body;color:var(--ink-soft)">Đang tải lên…</div>
     <div class="pd" style="left:630px;top:312px;display:flex;align-items:center;gap:10px;font:700 18px Body;color:#2F7D57;opacity:0"><div style="position:static;width:32px;height:24px">${LOGOS.youtube}</div>Đã đăng lên kênh</div>
     <div style="left:630px;top:356px;width:336px;height:12px;border-radius:6px;background:var(--ivory-deep)"><i class="pb" style="left:0;top:0;bottom:0;width:100%;border-radius:6px;background:var(--plum);transform-origin:0 50%"></i></div>
     <div style="left:34px;top:430px;width:932px;height:1px;background:var(--line)"></div>
     <div style="left:34px;top:458px;display:flex;align-items:center;gap:10px;padding:12px 20px;border-radius:999px;border:1.5px solid var(--line-strong);font:700 18px Body">${IC('eye', 20)}Công khai</div>
     <div class="go" style="right:34px;top:452px;padding:14px 34px;border-radius:14px;background:var(--plum);color:#fff;font:800 22px Disp">Đăng</div>`, 'studio.youtube.com · Tải video lên') +
   `<div class="yt paper" style="left:1050px;top:226px;width:96px;height:96px;border-radius:28px;padding:22px;opacity:0">${LOGOS.youtube}</div>
   <div class="sl paper" style="left:250px;top:262px;width:720px;height:405px;border-radius:18px;overflow:hidden"><img src="img/g2-slide05.jpg" style="left:0;top:0;width:100%;height:100%;object-fit:cover"></div>
   <div class="skip" style="left:840px;top:240px;padding:10px 22px;border-radius:999px;background:#F07A5A;color:#fff;font:800 24px Disp;rotate:6deg;white-space:nowrap">Bỏ qua</div>` +
   [['Kịch bản', 'file', 210], ['Quay', 'video', 472], ['Edit', 'wand', 680], ['Đăng', 'up', 878]].map(([n, i, x], j) => PILL(`sp sp${j}`, x, 720, n, i)).join('') +
   LINE('sa sa0', 392, 746, 460, 746) + LINE('sa sa1', 614, 746, 668, 746) + LINE('sa sa2', 812, 746, 866, 746) +
   `<div class="arc" style="left:280px;top:776px;width:280px;height:110px"><svg viewBox="0 0 280 110" style="overflow:visible"><path class="ap" d="M16 2 Q140 190 258 2" fill="none" stroke="#4A3AE0" stroke-width="4" stroke-linecap="round" stroke-dasharray="400" stroke-dashoffset="400"/><path class="ah" d="M246 16 L258 2 L262 20" fill="none" stroke="#4A3AE0" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" opacity="0"/></svg></div>
   <div class="al2" style="left:330px;top:890px;width:180px;text-align:center;font:700 20px Body;color:var(--plum)">nhảy tới Record</div>`,
 anim(tl, $, f, v) {
   move(tl, f, v, CARD.R, .25); rise(tl, $('.p1 .ttl'), .45); rise(tl, $('.up'), .55, 40);
   tl.fromTo($('.pb'), {scaleX: 0}, {scaleX: 1, duration: 1.0, ease: 'power1.inOut'}, .6); click(tl, $('.go'), .8);
   tl.set($('.pl'), {opacity: 0}, 1.6); rise(tl, $('.pd'), 1.6, 8); pop(tl, $('.yt'), 1.6, .4); tl.to($('.pb'), {backgroundColor: '#3E9B6E', duration: .2}, 1.6);
   tl.fromTo($('.tn'), {opacity: 0, scale: 1.25}, {opacity: 1, scale: 1, duration: .45, ease: 'expo.out'}, 3.0);
   tl.to($('.slot'), {borderStyle: 'solid', borderColor: '#4A3AE0', duration: .2}, 3.0); pop(tl, $('.ck1'), 3.2, .3);
   type(tl, '.ds .k', 4.0, 4.8); tl.to($('.ds'), {borderColor: '#4A3AE0', duration: .2}, 4.0); pop(tl, $('.ck2'), 4.85, .3);
   fade(tl, [$('.p1'), $('.up'), $('.yt')], 5.2);
   rise(tl, $('.p2 .ttl'), 5.6); $$('.sp').forEach((e, j) => rise(tl, e, 5.65 + j*.07, 16)); $$('.sa').forEach((e, j) => draw(tl, e, 5.85 + j*.07, .3));
   LIT(tl, $('.sp0'), 5.8);
   tl.fromTo($('.sl'), {opacity: 0, y: 40, scale: .94, filter: 'blur(8px)'}, {opacity: 1, y: 0, scale: 1, filter: 'blur(0px)', duration: .55, ease: 'expo.out'}, 7.35);
   tl.to($('.sl'), {opacity: .4, filter: 'grayscale(1)', duration: .3}, 8.4); pop(tl, $('.skip'), 8.45, .4); rise(tl, $('.p2s'), 8.4, 10);
   tl.to($('.sp0'), {opacity: .45, duration: .3}, 9.2);
   tl.to($('.ap'), {strokeDashoffset: 0, duration: .45, ease: 'power2.inOut'}, 9.15); tl.to($('.ah'), {opacity: 1, duration: .1}, 9.55); rise(tl, $('.al2'), 9.3, 10);
   LIT(tl, $('.sp1'), 9.55); tl.to($('.sp1'), {backgroundColor: '#4A3AE0', color: '#fff', duration: .2}, 9.55);
   tl.set([$('.p2 .ttl'), $('.p2s'), $('.sl'), $('.skip'), $('.al2')], {opacity: 0}, 0); tl.set($$('.sp'), {opacity: 0}, 0);
 }},

{id: 's82', clip: 'clips/s82.mp4', dur: 9, poster: 8.6, name: 'Không luật thì <em>AI cắt sai</em>',
 desc: 'Timeline video thô (khung hình thật): đầu phát chạy, 3 nhát cắt ở "cắt", vùng bị cắt đỏ lên + chip "cắt nhầm" ở "sai". File luật hiện "0 luật" ở "không có một cái luật nào hết". Ô chat gõ "cắt vấp video này đi" ở "kêu con AI cắt", trả về "Không biết đoạn nào là vấp" ở "không làm được".',
 html: () => BG + title(610, 90, 'AI <em>cắt sai</em>', 'vì lúc quay không có luật nào') +
   `<div class="tp paper" style="left:110px;top:260px;width:1000px;height:320px">
     ${EB(28, 24, 'TIMELINE · VIDEO THÔ')}
     <div style="left:28px;top:58px;width:944px;height:88px;border-radius:10px;overflow:hidden;display:flex">${Array.from({length: 6}, () => `<img src="img/g2-raw.jpg" style="position:static;flex:none;width:157.3px;height:88px;object-fit:cover;border-right:2px solid #fff">`).join('')}</div>
     <div style="left:28px;top:160px;width:944px;height:96px;border-radius:10px;background:rgba(169,224,194,.25);display:flex;align-items:center;padding:0 10px;overflow:hidden;color:#3E9B6E">${WAVE(92, 2)}</div>
     ${[[220, 110], [500, 90], [760, 100]].map(([x, w], j) => `<div class="cz cz${j}" style="left:${x}px;top:52px;width:${w}px;height:210px;border-radius:8px;background:rgba(240,122,90,.32);border:2.5px solid #F07A5A;opacity:0"></div>
       <div class="cm cm${j}" style="left:${x - 18}px;top:262px;color:#F07A5A;opacity:0">${IC('scissors', 34)}</div>`).join('')}
     <div class="ph" style="left:28px;top:50px;width:3px;height:214px;border-radius:2px;background:var(--plum)"></div></div>
   <div class="nz" style="left:568px;top:222px;display:flex;align-items:center;gap:8px;padding:8px 16px;border-radius:999px;background:#F07A5A;color:#fff;font:700 19px Body;white-space:nowrap">${IC('x', 18)}cắt nhầm câu đúng</div>
   <div class="rl paper" style="left:110px;top:620px;width:460px;height:270px;border-radius:22px;overflow:hidden">
     <div style="left:0;right:0;top:0;height:46px;background:var(--ivory);border-bottom:1px solid var(--line);font:600 16px Mono;color:var(--ink-muted);padding:12px 20px">luat-quay.md</div>
     ${[80, 120, 160, 200].map(y => `<i style="left:26px;top:${y}px;width:${y % 80 ? 170 : 210}px;height:12px;border-radius:6px;border:2px dashed var(--line-strong)"></i>`).join('')}
     <div class="zr" style="left:280px;top:90px;width:160px;text-align:center;font:800 96px Disp;line-height:1;color:#F07A5A">0</div>
     <div style="left:280px;top:196px;width:160px;text-align:center;font:800 26px Disp">luật</div></div>
   <div class="cc paper" style="left:600px;top:620px;width:510px;height:270px;border-radius:22px">
     <div class="ub" style="right:24px;top:26px;padding:14px 20px;border-radius:18px;background:var(--ivory-deep);font-size:22px;white-space:nowrap">${chars('cắt vấp video này đi', 'k')}</div>
     <div class="rp" style="left:24px;top:120px;display:flex;align-items:flex-start;gap:12px;font-size:21px;line-height:1.45"><div style="position:static;flex:none;width:28px;height:28px;margin-top:2px">${LOGOS.claude}</div>
       <div style="position:static">Đoạn nào là vấp? Mình <b style="position:static">không rõ</b>.</div></div>
     <div class="fl2" style="left:64px;top:200px;display:flex;align-items:center;gap:8px;padding:8px 16px;border-radius:999px;border:2px solid #F07A5A;color:#D0573A;font:700 19px Body;white-space:nowrap">${IC('alert', 20)}Không làm được</div></div>`,
 anim(tl, $, f, v) {
   move(tl, f, v, CARD.R, .25); rise(tl, $('.ttl h2'), .45); tl.set($('.ttl p'), {opacity: 0}, 0); rise(tl, $('.ttl p'), 4.3, 10);
   rise(tl, $('.tp'), .5, 40); tl.fromTo($('.ph'), {x: 0}, {x: 900, duration: 1.4, ease: 'none'}, .3);
   [0, 1, 2].forEach(j => { pop(tl, $('.cm' + j), .8 + j*.12, .4); tl.to($('.cz' + j), {opacity: 1, duration: .2}, 1.05 + j*.06); });
   tl.to($('.ph'), {opacity: 0, duration: .2}, 1.7); pop(tl, $('.nz'), 1.2, .5);
   rise(tl, $('.rl'), 4.4, 30); tl.fromTo($('.zr'), {scale: 1.5, opacity: 0}, {scale: 1, opacity: 1, duration: .4, ease: 'back.out(2.4)'}, 4.95);
   rise(tl, $('.cc'), 5.4, 30); type(tl, '.ub .k', 6.2, 7.2);
   tl.set($('.rp'), {opacity: 0}, 0); rise(tl, $('.rp'), 7.7, 10); pop(tl, $('.fl2'), 8.05, .5);
   tl.to($('.cc'), {borderColor: '#F07A5A', duration: .25}, 8.05);
 }},

{id: 's83', clip: 'clips/s83.mp4', dur: 9.3, poster: 8.9, name: 'AI cần <em>luật rõ</em>',
 desc: 'Mascot AI có dấu hỏi ở "không rõ về yêu cầu", đoạn giữa của dải câu nháy đỏ + kéo ở "cần phải cắt", thẻ "Luật 1" trượt vào mascot ở "thêm một cái luật", dấu hỏi thành tick. Ở "khi bạn quay video" hiện ô quay, "nói vấp" hiện bong bóng câu vấp thật.',
 html: () => BG + title(1340, 90, 'AI cần <em>luật rõ</em>', 'đoạn nào thì phải cắt') +
   MASC('ms', 920, 392, 20) +
   `<div class="qb" style="left:1166px;top:300px;width:76px;height:76px;border-radius:50%;background:#fff;border:3px solid #F07A5A;color:#F07A5A;display:grid;place-items:center;font:800 44px Disp;opacity:0">?</div>
   <div class="badge okb" style="left:1166px;top:300px;width:76px;height:76px;background:#3E9B6E;opacity:0">${IC('check', 38)}</div>
   ${LINE('ra', 1380, 450, 1190, 450, 'var(--plum)', 3)}
   <div class="rc paper" style="left:1390px;top:330px;width:400px;height:230px;border-radius:24px">
     ${EB(28, 26, 'LUẬT 1', 'var(--plum)')}<div class="rct" style="left:28px;top:58px;font:800 34px Disp;letter-spacing:-.02em;white-space:nowrap">Khi nói vấp thì…</div>
     ${LN(28, 122, 300)}${LN(28, 150, 240)}${LN(28, 178, 270)}
     <div class="badge" style="right:-14px;top:-14px;width:44px;height:44px;background:var(--plum)">${IC('plus', 22)}</div></div>
   <div class="sg" style="left:880px;top:700px;width:920px;height:150px">
     <div style="left:0;top:0;width:280px;height:72px;border-radius:14px;border:2px solid #3E9B6E;background:rgba(169,224,194,.3);font:700 22px Body;line-height:68px;text-align:center">câu nói đúng</div>
     <div class="sgm" style="left:310px;top:0;width:280px;height:72px;border-radius:14px;border:2px dashed var(--line-strong);background:#fff;font:800 30px Disp;line-height:66px;text-align:center;color:var(--ink-muted)">? ? ?</div>
     <div style="left:620px;top:0;width:280px;height:72px;border-radius:14px;border:2px solid #3E9B6E;background:rgba(169,224,194,.3);font:700 22px Body;line-height:68px;text-align:center">câu nói đúng</div>
     <div class="sgs" style="left:428px;top:86px;color:#F07A5A;opacity:0">${IC('scissors', 44)}</div></div>
   <div class="rw" style="left:880px;top:660px;width:940px;height:230px">
     ${TILE('rv', 0, 20, 110, IC('video', 50), 'Quay video')}
     ${LINE('rwa', 140, 75, 210, 75)}
     <div class="sbub paper" style="left:230px;top:14px;width:640px;height:122px;border-radius:26px 26px 26px 6px;display:flex;align-items:center;gap:18px;padding:0 28px">
       <span style="position:static;color:#F07A5A">${IC('mic', 34)}</span><span style="position:static;font:600 27px Body;white-space:nowrap">"mình gọi hết vào 3… <span style="position:relative;color:#D0573A">ờ</span>…"</span></div>
     <div class="vp" style="left:640px;top:160px;padding:8px 18px;border-radius:999px;background:#F07A5A;color:#fff;font:700 20px Body;white-space:nowrap">nói vấp</div></div>`,
 anim(tl, $, f, v) {
   move(tl, f, v, CARD.L, .25); rise(tl, $('.ttl h2'), .4); tl.set($('.ttl p'), {opacity: 0}, 0); rise(tl, $('.ttl p'), 1.3, 10);
   pop(tl, $('.ms'), .5, .4); pop(tl, $('.qb'), .7, .3); tl.to($('.qb'), {rotation: 12, duration: .15, yoyo: true, repeat: 3}, 1.0);
   rise(tl, $('.sg'), 1.0, 20); tl.to($('.sgm'), {borderColor: '#F07A5A', backgroundColor: 'rgba(255,179,156,.35)', color: '#D0573A', borderStyle: 'solid', duration: .25}, 1.95); pop(tl, $('.sgs'), 2.05, .4);
   tl.fromTo($('.rc'), {opacity: 0, x: 220}, {opacity: 1, x: 0, duration: .55, ease: 'expo.out'}, 3.6); draw(tl, $('.ra'), 3.95, .3);
   tl.to($('.qb'), {opacity: 0, scale: .5, duration: .2}, 4.1); pop(tl, $('.okb'), 4.15, .4); hop(tl, $('.ms'), 4.2, 26);
   tl.to($('.rc'), {borderColor: '#4A3AE0', boxShadow: '0 0 0 6px rgba(123,108,255,.18)', duration: .25}, 5.2); hop(tl, $('.rct'), 5.2, 12);
   fade(tl, $('.sg'), 6.0, 16);
   tl.set($('.rw'), {opacity: 0}, 0); tl.set($('.rw'), {opacity: 1}, 6.3); pop(tl, $('.rv'), 6.35, .5); LIT(tl, $('.rv'), 6.6); draw(tl, $('.rwa'), 6.8, .3);
   tl.fromTo($('.sbub'), {opacity: 0, x: -30, scale: .9}, {opacity: 1, x: 0, scale: 1, duration: .45, ease: 'back.out(1.6)'}, 7.85);
   tl.set($('.vp'), {opacity: 0}, 0); pop(tl, $('.vp'), 8.15, .5);
 }},

{id: 's84', clip: 'clips/s84.mp4', dur: 9.9, poster: 9.75, name: 'Sao không dùng <em>1 chữ</em>',
 desc: 'Chữ "cắt" to bật ra ở "dùng chữ Cắt", dấu cảnh báo ở "mình sợ". Ô "nói bình thường" hiện 2 câu thật của chính video này ở "bình thường"; chữ "cắt" trong câu đỏ lên ở "cái chữ này", chip "AI tưởng là lệnh" ở "nghe lộn", cây kéo cắt luôn câu đúng ở "cắt lộn".',
 html: () => BG + title(610, 90, 'Sao không dùng <em>1 chữ</em>?', 'sợ AI nghe lộn') +
   `<div class="kw paper" style="left:400px;top:262px;width:300px;height:118px;border-radius:30px;border:3px solid var(--plum);display:flex;align-items:center;justify-content:center;gap:16px;color:var(--plum)">${IC('scissors', 48)}<span style="position:static;font:800 60px Disp;letter-spacing:-.03em;color:var(--ink)">"cắt"</span></div>
   <div class="kwl" style="left:206px;top:300px;font:800 30px Disp;color:var(--ink-muted);white-space:nowrap">chỉ 1 chữ</div>
   <div class="badge alb" style="left:726px;top:290px;width:64px;height:64px;background:#F07A5A">${IC('alert', 32)}</div>
   <div class="tr paper" style="left:110px;top:430px;width:1000px;height:330px">
     <div style="left:30px;top:26px;display:flex;align-items:center;gap:10px;font:700 14px Body;letter-spacing:.16em;color:var(--ink-muted)">${IC('mic', 18)}NÓI BÌNH THƯỜNG</div>
     <div class="l1" style="left:30px;top:76px;width:940px;height:70px;border-radius:14px;background:var(--ivory-deep);font:600 28px Body;line-height:70px;padding:0 24px;white-space:nowrap;overflow:hidden">…là cái đoạn AI sẽ cần phải <span class="w" style="position:relative;display:inline-block;padding:0 8px;border-radius:8px">cắt</span></div>
     <i class="stk" style="left:46px;top:110px;width:480px;height:4px;border-radius:2px;background:#F07A5A;transform-origin:0 50%"></i>
     <div class="l2" style="left:30px;top:160px;width:940px;height:70px;border-radius:14px;background:var(--ivory-deep);font:600 28px Body;line-height:70px;padding:0 24px;white-space:nowrap;color:var(--ink-soft)">nên là mình phải cho nó thêm một cái luật</div>
     <div class="lx" style="left:560px;top:252px;display:flex;align-items:center;gap:10px;padding:10px 20px;border-radius:999px;background:#F07A5A;color:#fff;font:700 21px Body;white-space:nowrap">${IC('alert', 20)}AI tưởng là lệnh cắt</div>
     <div class="sc" style="left:560px;top:84px;color:#F07A5A">${IC('scissors', 52)}</div>
     <div class="gone" style="left:46px;top:252px;font:700 21px Body;color:#D0573A;white-space:nowrap">câu đúng bị cắt mất</div></div>`,
 anim(tl, $, f, v) {
   move(tl, f, v, CARD.R, .25); rise(tl, $('.ttl h2'), .9); tl.set($('.ttl p'), {opacity: 0}, 0); rise(tl, $('.ttl p'), 2.5, 10);
   pop(tl, $('.kw'), 1.35, .5); rise(tl, $('.kwl'), 1.5, 8); pop(tl, $('.alb'), 2.6, .3);
   rise(tl, $('.tr'), 4.3, 40);
   tl.to($('.w'), {backgroundColor: 'rgba(255,179,156,.75)', color: '#B3412A', scale: 1.3, duration: .12}, 6.75); tl.to($('.w'), {scale: 1, duration: .4, ease: 'back.out(2.5)'}, 6.87);
   tl.set($('.lx'), {opacity: 0}, 0); pop(tl, $('.lx'), 8.85, .5);
   tl.set($('.sc'), {opacity: 0}, 0); tl.to($('.sc'), {opacity: 1, duration: .1}, 9.3); tl.fromTo($('.sc'), {x: 0}, {x: -530, duration: .4, ease: 'power2.in'}, 9.3);
   tl.fromTo($('.stk'), {scaleX: 0}, {scaleX: 1, duration: .4, ease: 'power2.in'}, 9.3);
   tl.to($('.l1'), {backgroundColor: 'rgba(255,179,156,.4)', color: '#B3412A', duration: .2}, 9.45);
   tl.to($('.lx'), {opacity: 0, duration: .15}, 9.45); tl.set($('.gone'), {opacity: 0}, 0); rise(tl, $('.gone'), 9.5, 8);
 }},

{id: 's85', clip: 'clips/s85.mp4', dur: 8, poster: 7.8, name: 'Lệnh cắt <em>của bạn</em>',
 desc: 'Bảng "Luật quay": ô lệnh cắt có 2 chip "cắt" "cắt" (2 chữ), tick ở "Cắt của mình", ô sáng viền ở "luật khác", chip xoá đi và gõ "bỏ đoạn này" ở "chữ khác", tick xanh ở "cũng được". Dòng "Luật 2" hiện ở "Thứ 2", gõ "Hey Claude, …" ở "Hey Claude".',
 html: () => BG + title(1340, 90, 'Lệnh cắt <em>của bạn</em>', 'đổi chữ khác cũng được') +
   `<div class="st paper" style="left:880px;top:270px;width:920px;height:500px">
     <div style="left:32px;top:28px;display:flex;align-items:center;gap:12px;font:800 32px Disp;letter-spacing:-.02em"><span style="position:static;color:var(--plum)">${IC('file', 32)}</span>Luật quay</div>
     <div style="left:32px;top:88px;width:856px;height:1px;background:var(--line)"></div>
     <div class="r1" style="left:0;top:0;width:920px;height:270px">
       <div class="badge" style="left:32px;top:116px;width:40px;height:40px;background:var(--plum);font:800 22px Disp">1</div>
       <div style="left:88px;top:120px;font:700 24px Body">Lệnh cắt câu vấp</div>
       <div class="f1" style="left:88px;top:168px;width:600px;height:76px;border-radius:16px;border:2px solid var(--line-strong);background:#fff;display:flex;align-items:center;gap:12px;padding:0 18px">
         <span class="kc kc1" style="position:relative;padding:8px 20px;border-radius:12px;background:var(--plum);color:#fff;font:800 28px Disp">cắt</span><span class="kc kc2" style="position:relative;padding:8px 20px;border-radius:12px;background:var(--plum);color:#fff;font:800 28px Disp">cắt</span>
         <span class="nw" style="position:relative;font:700 28px Body;white-space:nowrap">${chars('bỏ đoạn này', 'k')}</span><span class="cr" style="position:relative;display:inline-block;width:3px;height:32px;background:var(--plum);opacity:0"></span></div>
       <div class="x2" style="left:704px;top:184px;padding:8px 14px;border-radius:999px;background:rgba(183,168,255,.35);color:var(--plum);font:700 20px Body">2 chữ</div>
       ${CHK('c1', 800, 182, 48, '#3E9B6E')}</div>
     <div class="r2" style="left:0;top:0;width:920px;height:500px">
       <div class="badge b2" style="left:32px;top:290px;width:40px;height:40px;background:var(--gold);font:800 22px Disp">2</div>
       <div style="left:88px;top:294px;font:700 24px Body">Lệnh gọi AI</div>
       <div class="f2" style="left:88px;top:342px;width:600px;height:76px;border-radius:16px;border:2px solid var(--line-strong);background:#fff;font:700 28px Body;line-height:72px;padding:0 20px;white-space:nowrap">${chars('Hey Claude, …', 'q')}</div></div></div>`,
 anim(tl, $, f, v) {
   move(tl, f, v, CARD.L, .25); rise(tl, $('.ttl h2'), .4); tl.set($('.ttl p'), {opacity: 0}, 0); rise(tl, $('.ttl p'), 4.6, 10);
   rise(tl, $('.st'), .45, 40); tl.set($('.r2'), {opacity: 0}, 0);
   pop(tl, $('.kc1'), .6, .5); pop(tl, $('.kc2'), .8, .5); pop(tl, $('.x2'), .95, .5); pop(tl, $('.c1'), 1.6, .3);
   tl.to($('.f1'), {borderColor: '#4A3AE0', boxShadow: '0 0 0 6px rgba(123,108,255,.18)', duration: .25}, 3.5); tl.to($('.c1'), {opacity: 0, duration: .15}, 3.5);
   tl.to([$('.kc1'), $('.kc2'), $('.x2')], {opacity: 0, scale: .6, duration: .2}, 4.15); tl.set([$('.kc1'), $('.kc2')], {display: 'none'}, 4.35);
   tl.set($('.cr'), {opacity: 1}, 4.35); type(tl, '.nw .k', 4.4, 5.0);
   tl.to($('.f1'), {borderColor: '#3E9B6E', boxShadow: '0 0 0 6px rgba(62,155,110,.15)', duration: .25}, 5.2); tl.set($('.cr'), {opacity: 0}, 5.2);
   tl.to($('.c1'), {opacity: 1, duration: .01}, 5.2); tl.fromTo($('.c1'), {scale: .3}, {scale: 1, duration: .4, ease: 'back.out(2)'}, 5.2);
   rise(tl, $('.r2'), 5.85, 20); hop(tl, $('.b2'), 6.3, 16);
   type(tl, '.f2 .q', 7.15, 7.6); tl.to($('.f2'), {borderColor: '#4A3AE0', duration: .2}, 7.15);
 }},

{id: 's86', clip: 'clips/s86.mp4', dur: 6.2, poster: 5.9, name: 'Claude là <em>editor</em> của mình',
 desc: 'Khung hình trượt phải, nửa trái phủ ivory. Logo Claude bật ra kèm bong bóng "Hey Claude" ở "kêu con Claude", thẻ tên "Editor của mình" bật ở "người editor".',
 html: () => `<div class="lp" style="inset:0;z-index:25;background:linear-gradient(90deg,var(--ivory) 0%,var(--ivory) 32%,rgba(250,246,239,.85) 45%,rgba(250,246,239,0) 62%);opacity:0"></div>
   <div class="eb" style="left:120px;top:150px;z-index:26;font:800 72px Disp;letter-spacing:-.04em;white-space:nowrap">Kêu <span class="em">Claude</span></div>
   <div class="cl" style="left:150px;top:300px;z-index:26;width:190px;height:190px;border-radius:48px;background:#fff;box-shadow:var(--shadow);border:1px solid var(--line);padding:40px">${LOGOS.claude}</div>
   <div class="hb" style="left:330px;top:290px;z-index:26;display:flex;align-items:center;gap:10px;padding:14px 24px;border-radius:24px 24px 24px 6px;background:var(--plum);color:#fff;font:700 26px Body;white-space:nowrap">${IC('mic', 24)}Hey Claude, …</div>
   <div class="idc" style="left:120px;top:560px;z-index:26;width:560px;height:170px;border-radius:28px;background:#fff;border:1.5px solid var(--line-strong);box-shadow:var(--shadow)">
     <div style="left:28px;top:33px;width:104px;height:104px;border-radius:28px;background:rgba(183,168,255,.3);border:2.5px solid var(--plum);display:grid;place-items:center;color:var(--plum)">${IC('film', 50)}</div>
     <div style="left:156px;top:30px">${EB(0, 0, 'NHƯ 1 NGƯỜI', 'var(--plum)')}</div>
     <div style="left:156px;top:56px;font:800 40px Disp;letter-spacing:-.03em;white-space:nowrap">Editor <span class="em">của mình</span></div>
     <div class="sub" style="left:156px;top:110px">che, chèn ảnh, chụp web theo lệnh</div></div>`,
 anim(tl, $, f, v) {
   tl.to(f, {left: 520, duration: .6, ease: 'power3.inOut'}, 1.9); tl.to($('.lp'), {opacity: 1, duration: .5}, 2.0);
   rise(tl, $('.eb'), 2.5, 20); pop(tl, $('.cl'), 3.15, .4); pop(tl, $('.hb'), 3.35, .5);
   tl.fromTo($('.idc'), {opacity: 0, y: 40, rotation: -4}, {opacity: 1, y: 0, rotation: 0, duration: .55, ease: 'back.out(1.6)'}, 4.95); hop(tl, $('.cl'), 5.1, 20);
   tl.to([$('.eb'), $('.cl'), $('.hb'), $('.idc')], {opacity: 0, y: -16, duration: .3}, 5.75);
   tl.to($('.lp'), {opacity: 0, duration: .4}, 5.8); tl.to(f, {left: 0, duration: .4, ease: 'power3.inOut'}, 5.8);
 }},

{id: 's87', clip: 'clips/s87.mp4', dur: 6.4, poster: 6.2, name: 'Chụp GitHub → <em>chìm vào video</em>',
 desc: 'Trang GitHub thật của repo, khung chụp + chớp sáng ở "hình ảnh", mảnh chụp nhấc lên ở "GitHub", bay xuống và chìm vào khung hình thật của video ở "chìm vô". "Bạn chỉ ra lệnh" hiện ở "ra lệnh", dòng phụ ở "ra lệnh ngay".',
 html: () => BG + `<div class="bw paper" style="left:330px;top:50px;width:1510px;height:900px;border-radius:26px;overflow:hidden">
     <div style="left:0;right:0;top:0;height:62px;background:var(--ivory);border-bottom:1px solid var(--line);display:flex;align-items:center;gap:10px;padding:0 22px">${DOTS}
       <span style="position:static;margin-left:20px;flex:1;height:38px;border-radius:12px;background:#fff;border:1px solid var(--line);font:18px Body;color:var(--ink-muted);line-height:36px;padding:0 16px">github.com/thanhthuduc99/youtube-ai-editor</span></div>
     <img src="img/web-01-github.png" style="left:0;top:62px;width:1510px"></div>
   <div class="cp" style="left:503px;top:293px;width:858px;height:362px;overflow:hidden;transform-origin:0 0;border-radius:4px;opacity:0;z-index:5"><img src="img/web-01-github.png" style="left:-173px;top:-181px;width:1510px"></div>
   <div class="mq" style="left:495px;top:285px;width:874px;height:378px;border-radius:10px;border:3px dashed var(--plum);opacity:0;z-index:6"></div>
   <div class="vf paper" style="left:900px;top:300px;width:860px;height:484px;border-radius:24px;overflow:hidden;z-index:4"><img src="img/g2-raw.jpg" style="left:0;top:0;width:100%;height:100%;object-fit:cover"></div>
   <div class="vl" style="left:900px;top:254px;font:700 15px Body;letter-spacing:.16em;color:var(--ink-muted)">VIDEO ĐANG EDIT</div>
   <div class="lb" style="left:900px;top:806px;display:flex;align-items:center;gap:10px;padding:12px 22px;border-radius:999px;background:var(--plum);color:#fff;font:700 21px Body;white-space:nowrap">${IC('layers', 22)}B-roll: ảnh GitHub</div>
   <div class="fl" style="inset:0;z-index:30;background:#fff;opacity:0"></div>` +
   title(560, 390, 'Bạn chỉ <em>ra lệnh</em>') + SUB('s2', 560, 480, 'ngay trong lúc quay'),
 anim(tl, $, f, v) {
   move(tl, f, v, CARD.BL, .1, .45); tl.fromTo($('.bw'), {opacity: 0, y: 60, filter: 'blur(10px)'}, {opacity: 1, y: 0, filter: 'blur(0px)', duration: .5, ease: 'expo.out'}, .15);
   tl.fromTo($('.mq'), {opacity: 0, scale: 1.06}, {opacity: 1, scale: 1, duration: .2}, .3);
   tl.to($('.fl'), {opacity: .85, duration: .06}, .5); tl.to($('.fl'), {opacity: 0, duration: .35}, .56);
   tl.set($('.cp'), {opacity: 1}, .52); tl.to($('.mq'), {opacity: 0, duration: .2}, .7); tl.to($('.bw'), {opacity: .35, duration: .3}, .7);
   tl.to($('.cp'), {scale: 1.04, x: -17, y: -7, boxShadow: '0 30px 60px -20px rgba(23,19,13,.45)', borderRadius: 16, duration: .35, ease: 'back.out(2)'}, .85);
   tl.set($('.vf'), {opacity: 0}, 0); rise(tl, $('.vf'), 1.4, 30); rise(tl, $('.vl'), 1.45, 10);
   tl.to($('.cp'), {left: 1250, top: 520, x: 0, y: 0, scale: .55, duration: .6, ease: 'power3.inOut'}, 2.0); tl.to($('.cp'), {boxShadow: '0 10px 24px -10px rgba(23,19,13,.35)', duration: .4}, 2.4);
   tl.to($('.bw'), {opacity: 0, duration: .4}, 2.3); tl.set($('.lb'), {opacity: 0}, 0); pop(tl, $('.lb'), 2.5, .5);
   tl.set($('.ttl'), {opacity: 0}, 0); rise(tl, $('.ttl'), 4.75); tl.set($('.s2'), {opacity: 0}, 0); rise(tl, $('.s2'), 5.75, 10);
 }},

{id: 's88', clip: 'clips/s88.mp4', dur: 8.5, poster: 8.3, name: 'Nói lúc quay vs <em>gõ lại</em>',
 desc: 'So 2 làn. Làn 1 "Nói ngay lúc quay": chip lệnh giọng nói ở "recording này luôn", thanh thời gian ngắn chạy tới Claude ở "đưa vô cho con AI", "nhanh hơn nhiều" ở "nhanh hơn". Làn 2 "Quay xong gõ lại": gõ lại yêu cầu ở "gõ lại", thanh dài đỏ dần, đồng hồ cát ở "rất là lâu".',
 html: () => BG + title(610, 90, 'Nói ngay <em>lúc quay</em>', 'đỡ phải gõ lại từng yêu cầu') +
   `<div class="la paper" style="left:110px;top:260px;width:1000px;height:250px">
     ${TILE('ta', 30, 30, 90, IC('mic', 42))}
     <div style="left:146px;top:34px;font:800 30px Disp;letter-spacing:-.02em">Nói ngay lúc quay</div>
     <div class="vc" style="left:146px;top:84px;display:flex;align-items:center;gap:10px;padding:8px 18px;border-radius:999px;background:rgba(183,168,255,.35);color:var(--plum);font:700 20px Body;white-space:nowrap">${IC('mic', 18)}"Hey Claude, chèn ảnh GitHub vào đây"</div>
     <div style="left:30px;top:170px;width:940px;height:20px;border-radius:10px;background:var(--ivory-deep)"><i class="fa" style="left:0;top:0;bottom:0;width:170px;border-radius:10px;background:#3E9B6E;transform-origin:0 50%"></i></div>
     <div class="ca" style="left:196px;top:156px;width:48px;height:48px;border-radius:50%;background:#fff;border:1px solid var(--line);box-shadow:var(--shadow);padding:10px">${LOGOS.claude}</div>
     <div class="na" style="left:270px;top:160px;display:flex;align-items:center;gap:10px;font:800 26px Disp;color:#2F7D57;white-space:nowrap"><span class="badge" style="position:static;width:36px;height:36px;background:#3E9B6E">${IC('check', 20)}</span>nhanh hơn rất nhiều</div></div>
   <div class="lb2 paper" style="left:110px;top:550px;width:1000px;height:300px">
     ${TILE('tb2', 30, 30, 90, IC('type', 42))}
     <div style="left:146px;top:34px;font:800 30px Disp;letter-spacing:-.02em">Quay xong, gõ lại</div>
     <div class="ib" style="left:146px;top:86px;width:824px;height:64px;border-radius:14px;border:2px solid var(--line-strong);background:#fff;font:20px/60px Body;padding:0 18px;white-space:nowrap;overflow:hidden">${chars('ở đoạn nói về repo, chèn ảnh GitHub; ở đoạn mở bảng, che API key…', 'k')}</div>
     <div style="left:30px;top:200px;width:940px;height:20px;border-radius:10px;background:var(--ivory-deep)"><i class="fb" style="left:0;top:0;bottom:0;width:800px;border-radius:10px;background:#F07A5A;transform-origin:0 50%"></i></div>
     <div class="hg" style="left:842px;top:236px;display:flex;align-items:center;gap:8px;font:800 26px Disp;color:#D0573A;white-space:nowrap">${IC('hourglass', 28)}rất lâu</div></div>`,
 anim(tl, $, f, v) {
   move(tl, f, v, CARD.R, .2); rise(tl, $('.ttl'), .45); rise(tl, $('.la'), .5, 40);
   tl.set($('.vc'), {opacity: 0}, 0); pop(tl, $('.vc'), .75, .6);
   tl.fromTo($('.fa'), {scaleX: 0}, {scaleX: 1, duration: .45, ease: 'power2.out'}, 2.5); tl.set($('.ca'), {opacity: 0}, 0); pop(tl, $('.ca'), 2.85, .4);
   tl.set($('.na'), {opacity: 0}, 0); tl.fromTo($('.na'), {opacity: 0, x: -20}, {opacity: 1, x: 0, duration: .4, ease: 'expo.out'}, 3.4);
   rise(tl, $('.lb2'), 4.3, 40); type(tl, '.ib .k', 5.7, 7.3); tl.to($('.ib'), {borderColor: '#4A3AE0', duration: .2}, 5.7);
   tl.fromTo($('.fb'), {scaleX: 0}, {scaleX: 1, duration: 2.0, ease: 'none'}, 5.8);
   tl.set($('.hg'), {opacity: 0}, 0); pop(tl, $('.hg'), 7.45, .5); tl.to($('.ib'), {borderColor: '#F07A5A', duration: .2}, 7.45);
 }},

{id: 's89', clip: 'clips/s89.mp4', dur: 5.65, poster: 5.5, name: 'Edit <em>trong lúc quay</em>',
 desc: 'Cửa sổ đang quay với khung hình thật và nhãn REC, timeline dài ra liên tục. Ở "edit cái video" các lệnh đã nhận bật lên bên phải và khối lệnh rơi xuống làn dưới; ở "lúc bạn quay" nhãn REC nảy; ở "cực kỳ tiện" bật thẻ xanh.',
 html: () => BG + title(1110, 34, 'Edit <em>trong lúc quay</em>') +
   WIN('ow', 380, 150, 1460, 790, `
     <div style="left:30px;top:70px;width:800px;height:450px;border-radius:16px;overflow:hidden"><img src="img/g2-raw.jpg" style="left:0;top:0;width:100%;height:100%;object-fit:cover"></div>
     <div class="rb" style="left:52px;top:92px;display:flex;align-items:center;gap:10px;padding:8px 16px;border-radius:999px;background:rgba(23,19,13,.72);color:#fff;font:700 20px Mono"><i class="rd" style="position:static;width:14px;height:14px;border-radius:50%;background:#E5484D"></i>REC 06:57</div>
     ${EB(866, 76, 'LỆNH ĐÃ NHẬN')}
     ${[['image', 'Chèn ảnh GitHub'], ['blur', 'Che API key'], ['film', 'Thêm B-roll']].map(([i, n], j) => `<div class="cmd cmd${j}" style="left:866px;top:${112 + j*82}px;width:560px;height:66px;border-radius:16px;border:1.5px solid var(--line-strong);background:#fff;display:flex;align-items:center;gap:14px;padding:0 20px;font:700 22px Body;white-space:nowrap">
       <span style="position:static;color:var(--plum)">${IC(i, 26)}</span>${n}<span class="badge" style="position:static;margin-left:auto;width:34px;height:34px;background:var(--plum)">${IC('check', 18)}</span></div>`).join('')}
     <div style="left:30px;top:548px;width:1400px;height:1px;background:var(--line)"></div>
     ${EB(30, 578, 'VIDEO')}${EB(30, 678, 'LỆNH')}
     <div style="left:150px;top:566px;width:1280px;height:76px;border-radius:12px;background:var(--ivory-deep);overflow:hidden"><div class="vt" style="left:0;top:0;width:1280px;height:76px;border-radius:12px;background:rgba(169,224,194,.55);display:flex;align-items:center;padding:0 12px;overflow:hidden;color:#3E9B6E">${WAVE(124, 5)}</div></div>
     <div style="left:150px;top:664px;width:1280px;height:60px;border-radius:12px;background:var(--ivory-deep)"></div>
     ${[[160, 'ảnh GitHub'], [400, 'che'], [560, 'B-roll']].map(([x, n], j) => `<div class="ob ob${j}" style="left:${150 + x}px;top:668px;width:${j == 1 ? 120 : 170}px;height:52px;border-radius:10px;background:var(--plum);color:#fff;font:700 18px Body;line-height:52px;text-align:center;white-space:nowrap">${n}</div>`).join('')}
     <div class="ph" style="left:150px;top:556px;width:3px;height:180px;border-radius:2px;background:#E5484D"></div>`, 'Đang quay') +
   `<div class="tien" style="left:1470px;top:96px;display:flex;align-items:center;gap:12px;padding:12px 24px;border-radius:999px;background:#3E9B6E;color:#fff;font:800 28px Disp;white-space:nowrap;box-shadow:var(--shadow);z-index:10"><span class="badge" style="position:static;width:36px;height:36px;background:#fff;color:#3E9B6E">${IC('check', 20)}</span>Cực kỳ tiện</div>`,
 anim(tl, $, f, v) {
   move(tl, f, v, CARD.BL, .2); rise(tl, $('.ow'), .35, 40);
   tl.fromTo($('.vt'), {width: 384}, {width: 1216, duration: 5.3, ease: 'none'}, .35); tl.fromTo($('.ph'), {x: 384}, {x: 1216, duration: 5.3, ease: 'none'}, .35);
   tl.to($('.rd'), {opacity: .2, duration: .4, repeat: 7, yoyo: true}, .5);
   tl.set($('.ttl'), {opacity: 0}, 0); rise(tl, $('.ttl'), 2.25);
   $$('.cmd').forEach((e, j) => tl.fromTo(e, {opacity: 0, x: 40}, {opacity: 1, x: 0, duration: .4, ease: 'expo.out'}, 2.3 + j*.2));
   $$('.ob').forEach((e, j) => tl.fromTo(e, {opacity: 0, y: -40}, {opacity: 1, y: 0, duration: .4, ease: 'back.out(1.8)'}, 2.4 + j*.2));
   tl.fromTo($('.rb'), {scale: 1}, {scale: 1.25, duration: .18, yoyo: true, repeat: 1, ease: 'power2.out'}, 4.15);
   tl.set($('.tien'), {opacity: 0}, 0); pop(tl, $('.tien'), 5.35, .5);
 }},
);
})();
