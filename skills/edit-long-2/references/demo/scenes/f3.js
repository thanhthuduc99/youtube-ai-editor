// Scenes s68-s70 (intro, video 80.0-101.3): closing line over the face, GitHub repo -> description link -> free download, video agenda.
const F3W = (s, cls) => `<span class="${cls}" style="position:relative;display:inline-block">${s}</span>`;
const F3STEPS = [['file', 'Kịch bản', '3:24'], ['video', 'Quay', '3:49'], ['scissors', 'Cắt vấp', '5:00'], ['wand', 'Edit', '7:27'],
  ['image', 'Thumbnail', '8:26'], ['type', 'Title, mô tả', '9:29'], ['download', 'Cài đặt', '9:55']];
const F3POS = [[935, 340], [1195, 340], [1455, 340], [1715, 340], [1715, 640], [1455, 640], [935, 640]];
SCENES.push(
{id: 's68', clip: 'clips/s68.mp4', dur: 4.6, poster: 4.5, name: 'Câu chốt <em>áp dụng</em>',
 desc: 'Mặt giữ full. Dải ivory dưới: pill "Hệ thống YouTube AI" ở chữ "hệ thống", câu "Hoàn toàn áp dụng được" lên từng chữ theo lời, chip kênh YouTube sáng ở chữ "Youtube", "của bạn" đổi màu ở chữ "bạn".',
 html: () => `<div class="gb" style="left:0;right:0;bottom:0;height:440px;z-index:25;background:linear-gradient(0deg,rgba(250,246,239,.95),rgba(250,246,239,.75) 55%,rgba(250,246,239,0));opacity:0"></div>
   <div style="left:0;right:0;top:712px;z-index:26;display:flex;justify-content:center"><div class="hp" style="position:relative;display:flex;align-items:center;gap:12px;padding:10px 22px;border-radius:999px;background:#fff;border:1.5px solid var(--line-strong);font:700 22px Body;color:var(--plum)">
     <div style="position:relative;width:40px;height:28px;color:var(--plum)">${LOGOS.mark}</div>Hệ thống YouTube AI</div></div>
   <div style="left:0;right:0;top:786px;z-index:26;text-align:center;font:800 100px Disp;letter-spacing:-.04em;white-space:nowrap;line-height:1.1">${F3W('Hoàn toàn', 'w0')} ${F3W('áp dụng', 'w1 em')} ${F3W('được', 'w2')}</div>
   <div style="left:0;right:0;top:922px;z-index:26;display:flex;justify-content:center"><div class="yc" style="position:relative;display:flex;align-items:center;gap:14px;padding:12px 26px 12px 16px;border-radius:999px;background:#fff;border:2.5px solid var(--line-strong);box-shadow:var(--shadow);font:700 28px Body">
     <div style="position:relative;width:46px;height:46px">${LOGOS.youtube}</div><span style="position:relative">Kênh YouTube <span class="yb" style="position:relative">của bạn</span></span>
     <div class="badge yk" style="position:relative;width:38px;height:38px;background:#3E9B6E;opacity:0">${IC('check', 22)}</div></div></div>`,
 anim(tl, $) {
   tl.to($('.gb'), {opacity: 1, duration: .35}, .95); pop(tl, $('.hp'), 1.21, .6);
   rise(tl, $('.w0'), 1.86, 30); rise(tl, $('.w1'), 2.3, 30); rise(tl, $('.w2'), 2.62, 30);
   pop(tl, $('.yc'), 4.0, .5); tl.to($('.yc'), {borderColor: '#4A3AE0', duration: .2}, 4.1);
   tl.to($('.yb'), {color: '#4A3AE0', duration: .2}, 4.4); pop(tl, $('.yk'), 4.4, .3);
 }},

{id: 's69', clip: 'clips/s69.mp4', dur: 6.7, poster: 6.5, name: 'Repo thật → <em>mô tả</em> → tải miễn phí',
 desc: 'Trang GitHub thật của skill, khung sáng ở "skill" và "hướng dẫn". Ở "phần mô tả" khung mô tả YouTube (chữ thật của video) hiện ra, dòng link tài liệu được tô, mũi tên nảy chỉ xuống. Con trỏ bấm ở "tải về", dấu "Miễn phí" đóng ở "miễn phí".',
 html: () => BG + `<div class="bw paper" style="left:330px;top:50px;width:1520px;height:980px;border-radius:24px;overflow:hidden">
     <div style="left:0;right:0;top:0;height:60px;background:var(--ivory);border-bottom:1px solid var(--line);display:flex;align-items:center;gap:10px;padding:0 22px">${DOTS}
       <span class="url" style="position:static;margin-left:20px;flex:1;height:38px;border-radius:12px;background:#fff;border:2px solid var(--line);font:18px Body;color:var(--ink-muted);line-height:34px;padding:0 16px">github.com/thanhthuduc99/youtube-ai-editor</span></div>
     <div style="left:0;top:60px;width:1520px;height:920px;overflow:hidden"><img src="img/web-01-github.png" style="left:0;top:0;width:1520px"></div></div>
   <div class="r1" style="left:494px;top:281px;width:210px;height:52px;border-radius:12px;border:3.5px solid var(--plum);box-shadow:0 0 0 6px rgba(123,108,255,.18)"></div>
   ${PILL('t1', 760, 279, 'Skill', 'wand').replace('background:#fff', 'background:var(--plum);color:#fff;border-color:var(--plum)')}
   <div class="r2" style="left:498px;top:668px;width:878px;height:200px;border-radius:16px;border:3.5px solid var(--plum);box-shadow:0 0 0 6px rgba(123,108,255,.18)"></div>
   ${PILL('t2', 1392, 700, 'Hướng dẫn', 'file').replace('background:#fff', 'background:var(--plum);color:#fff;border-color:var(--plum)')}
   <div class="dc paper" style="left:400px;top:180px;width:1180px;height:690px;border-radius:26px">
     <div style="left:36px;top:30px;display:flex;align-items:center;gap:18px"><div style="position:relative;width:60px;height:60px">${LOGOS.youtube}</div>
       <div style="position:static"><div style="position:static;font:800 32px Disp;letter-spacing:-.02em">Mô tả</div><div class="sub" style="position:static;font-size:18px">Hệ thống YouTube AI · Thành Vũ Đức</div></div></div>
     <i style="left:36px;right:36px;top:124px;height:1.5px;background:var(--line)"></i>
     ${[['Tải tài liệu miễn phí của Thành:', 'contentta.vn/tai-lieu'], ['AI Automation Academy (miễn phí):', 'facebook.com/groups/aiauacademy'],
        ['Skool AI Automation Academy:', 'skool.com/ai-automation-academy…'], ['Xây dựng hệ thống bán hàng bằng AI:', 'contentta.vn/content-funnel'],
        ['Làm việc với AI Agency của Thành:', 'contentta.vn/custom-solutions']].map(([a, b], j) =>
       `<div class="dl dl${j}" style="left:36px;top:${196 + j*62}px;font-size:25px;white-space:nowrap"><span style="position:relative;isolation:isolate">${a} <span style="position:relative;color:#1A63D6">${b}</span>${j ? '' : '<i class="hl" style="left:-10px;right:-10px;top:-4px;bottom:-4px;border-radius:8px;background:rgba(183,168,255,.5);transform-origin:0 50%;z-index:-1"></i>'}</span></div>`).join('')}
     <div style="left:36px;top:530px;font:700 22px Body;letter-spacing:.08em;color:var(--ink-muted)">TIMESTAMPS</div>
     <div style="left:36px;right:36px;top:574px;display:flex;flex-wrap:wrap;gap:12px 26px;font-size:22px">${[['0:00', 'Intro'], ['1:30', 'Demo kết quả'], ['3:24', 'Kịch bản'], ['3:49', 'Quay'], ['5:00', 'Luật "cắt cắt"'], ['6:07', 'Lệnh "Hey Claude"'], ['7:27', 'Edit'], ['8:26', 'Thumbnail'], ['9:29', 'Title, mô tả'], ['9:55', 'Cài đặt']].map(([t, n]) =>
       `<span style="position:relative"><span style="position:relative;color:#1A63D6">${t}</span> ${n}</span>`).join('')}</div>
     <div class="ar" style="left:522px;top:118px;color:var(--plum)"><div style="position:relative;rotate:180deg">${IC('up', 64)}</div></div>
     <div class="dk" style="left:716px;top:186px;display:flex;align-items:center;gap:10px;padding:10px 18px;border-radius:14px;background:var(--ink);color:#fff;font:700 20px Body;overflow:hidden">${IC('download', 22)}<span class="dkt" style="position:relative">Đang tải…</span>
       <i class="dkb" style="left:0;bottom:0;height:4px;width:100%;background:#7B6CFF;transform-origin:0 50%"></i></div>
     <div class="st" style="left:880px;top:26px;padding:10px 26px;border-radius:16px;border:4px solid #3E9B6E;color:#2F7D57;background:rgba(169,224,194,.35);font:800 44px Disp;letter-spacing:-.02em;rotate:-9deg;white-space:nowrap">Miễn phí</div></div>` + CUR('cu', 1500, 820),
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.BL, .05, .5);
   tl.fromTo($('.bw'), {opacity: 0, y: 60, filter: 'blur(10px)'}, {opacity: 1, y: 0, filter: 'blur(0px)', duration: .55, ease: 'expo.out'}, .2);
   tl.to($('.url'), {borderColor: '#4A3AE0', color: '#4A3AE0', duration: .2}, .55);
   tl.fromTo($('.cu'), {opacity: 0}, {opacity: 1, duration: .2}, .5); glide(tl, $('.cu'), .55, 640, 312, .4);
   pop(tl, $('.r1'), .9, .8); pop(tl, $('.t1'), .95, .5);
   glide(tl, $('.cu'), 1.25, 900, 790, .35); tl.to([$('.r1'), $('.t1')], {opacity: 0, duration: .2}, 1.45);
   pop(tl, $('.r2'), 1.54, .9); pop(tl, $('.t2'), 1.6, .5);
   tl.to($('.r2'), {scale: 1.02, duration: .25, yoyo: true, repeat: 3}, 2.2);
   // "bên dưới phần mô tả": the repo window steps back, the real description card comes up
   tl.to([$('.bw'), $('.r2'), $('.t2')], {opacity: 0, scale: .9, y: -50, filter: 'blur(6px)', duration: .4, ease: 'power2.in'}, 3.7);
   tl.to($('.cu'), {opacity: 0, duration: .15}, 3.7);
   tl.fromTo($('.dc'), {opacity: 0, y: 80, filter: 'blur(10px)'}, {opacity: 1, y: 0, filter: 'blur(0px)', duration: .55, ease: 'expo.out'}, 4.0);
   $$('.dl').forEach((e, j) => rise(tl, e, 4.05 + j*.06, 12));
   tl.set($('.hl'), {scaleX: 0}, 0); draw(tl, $('.hl'), 4.52, .35);
   tl.to([$('.dl1'), $('.dl2'), $('.dl3'), $('.dl4')], {opacity: .4, duration: .3}, 4.6);
   pop(tl, $('.ar'), 4.52, .5); [4.95, 5.5, 6.05].forEach(t => { tl.to($('.ar'), {y: 22, duration: .22, ease: 'power2.in'}, t); tl.to($('.ar'), {y: 0, duration: .28, ease: 'power2.out'}, t + .22); });
   tl.set($('.cu'), {left: 1300, top: 900}, 4.4); tl.to($('.cu'), {opacity: 1, duration: .15}, 4.6); glide(tl, $('.cu'), 4.6, 960, 392, .6);
   click(tl, $('.cu'), 5.37); tl.to($('.dl0 .hl'), {backgroundColor: 'rgba(123,108,255,.55)', duration: .15}, 5.37);
   tl.fromTo($('.dk'), {opacity: 0, x: -20}, {opacity: 1, x: 0, duration: .25}, 5.45); tl.fromTo($('.dkb'), {scaleX: 0}, {scaleX: 1, duration: .55, ease: 'none'}, 5.45);
   tl.set($('.dkt'), {innerHTML: 'Đã tải về'}, 6.0); tl.set($('.dk'), {backgroundColor: '#2F7D57'}, 6.0);
   tl.fromTo($('.st'), {opacity: 0, scale: 1.9}, {opacity: 1, scale: 1, duration: .32, ease: 'back.out(2.2)'}, 6.08);
 }},

{id: 's70', clip: 'clips/s70.mp4', dur: 10, poster: 9.8, name: 'Lộ trình video, <em>cài đặt</em> ở cuối',
 desc: 'Các phần của video (tên và mốc thật trong mô tả) xếp thành đường đi. Hiện ra ở "hệ thống YouTube AI", sáng lần lượt từ "ở từng cái phần" tới "giai đoạn". Ở "cuối video" các bước mờ đi, đường nét đứt chạy tới bước cuối kèm nhãn; "Cài đặt" bật sáng ở chữ "cài đặt".',
 html: () => BG + title(1330, 120, 'Demo <em>từng giai đoạn</em>') +
   `<div class="ss" style="left:1330px;top:214px;translate:-50% 0;font-size:28px;color:var(--ink-soft);white-space:nowrap">xem nó làm được gì</div>` +
   [[0, 1], [1, 2], [2, 3], [4, 5]].map(([a, b], j) => { const [x1, y1] = F3POS[a], [x2, y2] = F3POS[b], s = Math.sign(x2 - x1);
     return [LINE(`cn cn${j}`, x1 + s*74, y1 + 60, x2 - s*74, y2 + 60, 'var(--line-strong)'), LINE(`cp cp${j}`, x1 + s*74, y1 + 60, x2 - s*74, y2 + 60, '#4A3AE0')].join(''); }).join('') +
   LINE('cn cv', 1715, 548, 1715, 630, 'var(--line-strong)') + LINE('cp cpv', 1715, 548, 1715, 630, '#4A3AE0') +
   LINE('cn cd', 1381, 700, 1009, 700, 'repeating-linear-gradient(90deg,var(--ink-faint) 0 12px,transparent 12px 24px)') +
   LINE('cp cpd', 1381, 700, 1009, 700, 'repeating-linear-gradient(90deg,#4A3AE0 0 12px,transparent 12px 24px)', 4) +
   F3STEPS.map(([i, n, t], j) => { const [cx, y] = F3POS[j];
     return TILE(`sx sx${j}`, cx - 60, y, 120, IC(i, 50)) + `<div class="tn tn${j}" style="left:${cx - 120}px;top:${y + 132}px;width:240px;text-align:center;font:800 24px Disp;letter-spacing:-.02em;white-space:nowrap">${n}</div>
       <div class="tm tm${j}" style="left:${cx - 50}px;top:${y + 172}px;width:100px;text-align:center;font:600 18px Mono;color:var(--ink-muted)">${t}</div>`; }).join('') +
   `<div class="tg" style="left:935px;top:572px;translate:-50% 0;display:flex;align-items:center;gap:8px;padding:8px 18px;border-radius:999px;background:var(--plum);color:#fff;font:700 20px Body;white-space:nowrap">${IC('clock', 20)}cuối video</div>
   <div class="badge ck" style="left:1000px;top:622px;width:44px;height:44px;background:#3E9B6E;opacity:0">${IC('check', 24)}</div>`,
 anim(tl, $) {
   const f = $('.face'), v = $('.face video');
   tl.set(f, {...CARD.BL.box}, 0); tl.set(v, CARD.BL.vid, 0); move(tl, f, v, CARD.L, .1, .55);
   rise(tl, $('.ttl'), 1.58);
   tl.set($$('.cp'), {scaleX: 0}, 0);
   $$('.sx').forEach((e, j) => { rise(tl, e, 2.8 + j*.15, 24); tl.fromTo([$('.tn' + j), $('.tm' + j)], {opacity: 0}, {opacity: 1, duration: .3}, 2.9 + j*.15); });
   $$('.cn').forEach((e, j) => draw(tl, e, 2.9 + j*.15, .25));
   const lt = [4.3, 4.6, 4.9, 5.2, 5.5, 5.8], cps = ['.cp0', '.cp1', '.cp2', '.cpv', '.cp3'];
   lt.forEach((t, j) => { lit(tl, $('.sx' + j), t); tl.to($('.tm' + j), {color: '#4A3AE0', duration: .2}, t); if (j < 5) draw(tl, $(cps[j]), t + .08, .24); });
   rise(tl, $('.ss'), 6.1, 14);
   // "cuối video": jump to the end of the path
   dim(tl, [...$$('.sx').slice(0, 6), ...$$('.tm').slice(0, 6), ...$$('.tn').slice(0, 6), ...$$('.cn').slice(0, 5), ...$$('.cp').slice(0, 5)], 7.9, .3);
   draw(tl, $('.cpd'), 7.95, .6); pop(tl, $('.tg'), 8.2, .5);
   lit(tl, $('.sx6'), 9.44); tl.to($('.sx6'), {scale: 1.12, duration: .3, ease: 'back.out(2)'}, 9.44);
   tl.to([$('.tn6'), $('.tm6')], {color: '#4A3AE0', duration: .2}, 9.44); pop(tl, $('.ck'), 9.6, .3);
 }},
);
