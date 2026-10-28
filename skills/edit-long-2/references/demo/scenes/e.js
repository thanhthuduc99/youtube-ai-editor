// Scenes s50-s57: slash command + status line, pinned calendar, post card with highlights, real page scroll + click,
// name intro beside the face, brand outro with ribbon wipe.
SCENES.push(
{id: 's50', clip: 'clips/s50.mp4', dur: 11.9, poster: 11.6, name: 'Lệnh <em>"/"</em> + dòng trạng thái',
 desc: 'Gốc: gõ "/keepwarm" hiện menu lệnh, dòng trạng thái dưới ô nhập đổi theo (RN 8:06-8:12). Bản này: gõ "/upload", menu có private / unlisted, chọn private ở chữ "duyệt chọn", dòng trạng thái chạy render → đã đăng private.',
 html: () => BG + CLAUDE(`<div class="mn" style="left:60px;top:300px;width:520px;padding:10px;border-radius:16px;background:#fff;border:1px solid var(--line-strong);box-shadow:var(--shadow)">
     ${[['/upload private', 'đăng ẩn, bạn tự bật'], ['/upload unlisted', 'gửi link cho khách duyệt'], ['/upload public', 'đăng công khai']].map(([c, d], j) =>
       `<div class="mi mi${j}" style="position:relative;display:flex;gap:16px;align-items:center;padding:12px 14px;border-radius:10px"><span style="position:relative;font:700 17px Mono">${c}</span><span style="position:relative;font-size:15px;color:var(--ink-muted)">${d}</span></div>`).join('')}</div>` +
   INPUT('in', 480, `<div style="left:22px;top:20px;font:20px Mono;white-space:nowrap">${chars('/upload private', 'k')}</div>`) +
   `<div class="sl" style="left:64px;top:612px;display:flex;align-items:center;gap:10px;font:600 15px Mono;color:var(--ink-muted)"><i class="sd" style="position:static;width:10px;height:10px;border-radius:50%;background:#E6B45A"></i><span class="stx" style="position:relative">youtube · đang render final 62%</span></div>`) ,
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.BL, .3); rise(tl, $('.cw'), .4, 30);
   type(tl, '.k', .4, 1.2); tl.to($('.in'), {borderColor: '#4A3AE0', duration: .2}, .4); tl.set($('.mn'), {opacity: 0}, 0); rise(tl, $('.mn'), .9, 10);
   tl.to($('.mi0'), {backgroundColor: 'rgba(183,168,255,.35)', duration: .2}, 2.2); tl.to($('.mn'), {opacity: 0, duration: .2}, 2.8);
   tl.set($('.sl'), {opacity: 0}, 0); rise(tl, $('.sl'), 3.3, 6);
   tl.set($('.stx'), {innerHTML: 'youtube · đang upload 40%'}, 5.4); tl.set($('.stx'), {innerHTML: 'youtube · đã đăng PRIVATE · youtu.be/…'}, 7.6);
   tl.set($('.sd'), {backgroundColor: '#3E9B6E'}, 7.6); tl.set($('.stx'), {color: '#2F7D57'}, 7.6);
 }},

{id: 's53', clip: 'clips/s53.mp4', dur: 10, poster: 9.6, name: 'Bản đồ ghim → <em>lịch ghim ảnh</em>',
 desc: 'Gốc: bản đồ thế giới có ghim và ảnh thành viên bật lên (RN 0:35-0:37). Bản này đổi thành lịch tháng 10: 2 thumbnail thật ghim vào ngày 16 và 21 đúng lúc bạn đọc ngày.',
 html: () => { let cells = ''; for (let d = 1; d <= 31; d++) { const k = d + 2, x = 160 + (k % 7)*126, y = 380 + Math.floor(k/7)*86;
     cells += `<div class="dy dy${d}" style="left:${x}px;top:${y}px;width:116px;height:76px;border-radius:12px;border:1px solid var(--line);background:rgba(255,255,255,.7);font:700 18px Body;padding:8px 10px;color:var(--ink-muted)">${d}</div>`; }
   return BG + title(610, 150, 'Tháng 10: <em>2 video</em>', 'đều làm bằng hệ thống này') +
     `<div style="left:160px;top:330px;display:flex;gap:0;font:700 15px Body;letter-spacing:.12em;color:var(--ink-muted)">${['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN'].map(d => `<span style="position:static;width:126px">${d}</span>`).join('')}</div>` + cells +
     [['16', 'rea-t1.jpg', '11K view'], ['21', 'cap-thumb.jpg', '10K+ view']].map(([d, im, v], j) => { const k = +d + 2, x = 160 + (k % 7)*126, y = 380 + Math.floor(k/7)*86;
       return `<div class="pin pin${j}" style="left:${x - 60}px;top:${j ? y + 86 : y - 180}px;width:240px;height:170px;padding:8px;border-radius:14px;background:#fff;box-shadow:var(--shadow);border:1px solid var(--line)"><img src="img/${im}" style="left:8px;top:8px;width:224px;height:126px;border-radius:8px;object-fit:cover"><div style="left:12px;top:140px;font:800 18px Disp">${v}</div></div>
         <i class="pd pd${j}" style="left:${x + 52}px;top:${y + 30}px;width:16px;height:16px;border-radius:50%;background:var(--plum);box-shadow:0 0 0 6px rgba(123,108,255,.25)"></i>`; }).join(''); },
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.R, .3); rise(tl, $('.ttl'), .5);
   $$('.dy').forEach((e, j) => tl.fromTo(e, {opacity: 0}, {opacity: 1, duration: .2}, .6 + j*.02));
   [[4.9, 16], [5.9, 21]].forEach(([t, d], j) => { tl.to($('.dy' + d), {backgroundColor: 'rgba(183,168,255,.35)', color: '#4A3AE0', duration: .2}, t); pop(tl, $('.pd' + j), t, .3);
     tl.fromTo($('.pin' + j), {opacity: 0, y: 30, scale: .7}, {opacity: 1, y: 0, scale: 1, duration: .5, ease: 'back.out(1.6)'}, t + .1); });
 }},

{id: 's54', clip: 'clips/s54.mp4', dur: 8.9, poster: 8.6, name: 'Bài đăng + <em>tô dòng</em>',
 desc: 'Gốc: bài X của Claude Code ở giữa màn, các dòng quan trọng được tô cam lần lượt (RN 0:40-0:45). Bản này: thẻ dạng bài đăng "Claude đề xuất title", tô title 1 ở chữ "AB testing", title 3 ở chữ "lựa chọn".',
 html: () => BG + `<div class="po paper" style="left:860px;top:150px;width:880px;height:780px;border-radius:24px">
     <div style="left:34px;top:30px;display:flex;align-items:center;gap:14px"><div style="position:relative;width:56px;height:56px;border-radius:50%;background:#fff;border:1px solid var(--line);padding:12px">${LOGOS.claude}</div>
       <div style="position:static"><div style="position:static;font:800 24px Disp">Claude Code</div><div class="sub" style="position:static;font-size:16px">skill youtube · 5 title để chọn</div></div></div>
     ${['Hệ thống YouTube AI: quay xong, Claude Code edit hết', 'Claude Code tự cắt vấp, làm B-roll, thumbnail và đăng YouTube', 'Kênh 1.000 sub có 2 video 10K view nhờ hệ thống AI này', 'Không cần editor: mình để AI làm trọn video YouTube', 'Video này do AI edit: cách mình làm YouTube bằng Claude Code'].map((t, j) =>
       `<div class="pl pl${j}" style="left:34px;right:34px;top:${130 + j*112}px;display:flex;gap:16px;font-size:24px;line-height:1.35"><span style="position:relative;font:800 24px Disp;color:var(--plum)">${j + 1}</span><span style="position:relative;isolation:isolate">${t}<i class="hl" style="left:-6px;right:-6px;top:2px;bottom:0;border-radius:6px;background:rgba(183,168,255,.55);transform-origin:0 50%;z-index:-1"></i></span></div>`).join('')}
     <div style="left:34px;bottom:28px;display:flex;gap:28px;font:600 17px Body;color:var(--ink-muted)"><span style="position:relative">Thumbnail · 3 mẫu</span><span style="position:relative">Description · 12 mốc</span></div></div>`,
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.L, .3); rise(tl, $('.po'), .4, 50);
   tl.set($$('.hl'), {scaleX: 0}, 0); $$('.pl').forEach((e, j) => rise(tl, e, .6 + j*.08, 10));
   draw(tl, $('.pl0 .hl'), 1.0, .4); draw(tl, $('.pl2 .hl'), 2.4, .4);
   tl.to([$('.pl1'), $('.pl3'), $('.pl4')], {opacity: .4, duration: .3}, 2.4);
 }},

{id: 's55', clip: 'clips/s55.mp4', dur: 9.3, poster: 6.9, name: 'Trang thật cuộn + <em>con trỏ bấm</em>',
 desc: 'Gốc: trang cộng đồng / GitHub thật toàn khung, cuộn xuống, con trỏ di chuyển và bấm, mặt góc dưới trái (RN 5:30-6:00, 9:45-9:54). Bản này: repo GitHub thật, con trỏ bấm nút "Code" ở chữ "copy", hiện thẻ đã chép link.',
 html: () => BG + `<div class="bw paper" style="left:330px;top:50px;width:1520px;height:980px;border-radius:24px;overflow:hidden">
     <div style="left:0;right:0;top:0;height:60px;background:var(--ivory);border-bottom:1px solid var(--line);display:flex;align-items:center;gap:10px;padding:0 22px">${DOTS}
       <span style="position:static;margin-left:20px;flex:1;height:38px;border-radius:12px;background:#fff;border:1px solid var(--line);font:18px Body;color:var(--ink-muted);line-height:36px;padding:0 16px">github.com/thanhthuduc99/youtube-ai-editor</span></div>
     <div class="pg" style="left:0;top:60px;width:1520px;height:920px;overflow:hidden"><img class="gi" src="img/web-01-github.png" style="left:0;top:0;width:1520px"></div>
     <div class="toast" style="left:540px;top:430px;display:flex;align-items:center;gap:12px;padding:16px 24px;border-radius:16px;background:var(--ink);color:#fff;font:700 22px Body;opacity:0">${IC('copy', 24)} Đã chép link repo</div></div>` + CUR('cu', 1500, 800),
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.BL, .3); tl.fromTo($('.bw'), {opacity: 0, y: 60, filter: 'blur(10px)'}, {opacity: 1, y: 0, filter: 'blur(0px)', duration: .6, ease: 'expo.out'}, .4);
   tl.fromTo($('.gi'), {y: 40}, {y: 0, duration: 1.2, ease: 'power2.out'}, .5);
   tl.fromTo($('.cu'), {opacity: 0}, {opacity: 1, duration: .2}, 4.2); glide(tl, $('.cu'), 4.3, 1350, 365, .8);
   click(tl, $('.cu'), 6.2); tl.fromTo($('.toast'), {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: .3}, 6.4); tl.to($('.toast'), {opacity: 0, duration: .3}, 8.6);
 }},

{id: 's56', clip: 'clips/s56.mp4', dur: 8.7, poster: 3.6, name: 'Tên lớn + <em>thẻ giới thiệu</em>',
 desc: 'Gốc: đoạn giới thiệu bản thân (RN 0:27-0:32): khung trượt phải, tên "Jay" cỡ lớn bên trái, sau đó thẻ "Education" và logo bật lên. Bản này: tên "Thành" + thẻ Contentta, thẻ kênh YouTube, ở hook đầu video.',
 html: () => `<div class="lp" style="inset:0;z-index:25;background:linear-gradient(90deg,var(--ivory) 0%,var(--ivory) 30%,rgba(250,246,239,.85) 44%,rgba(250,246,239,0) 62%);opacity:0"></div>
   <div class="nm" style="left:110px;top:260px;z-index:26;font:800 190px Disp;letter-spacing:-.05em;line-height:1">Thành</div>
   <div class="c1 paper" style="left:110px;top:500px;z-index:26;width:520px;height:120px;border-radius:24px;display:flex;align-items:center;gap:18px;padding:0 24px">
     <div style="position:relative;width:76px;height:54px;color:var(--plum)">${LOGOS.mark}</div><div style="position:static"><div style="position:static;font:800 28px Disp">Founder Contentta</div><div class="sub" style="position:static">AI Automation + AI Agent</div></div></div>
   <div class="c2 paper" style="left:110px;top:650px;z-index:26;width:520px;height:120px;border-radius:24px;display:flex;align-items:center;gap:18px;padding:0 24px">
     <div style="position:relative;width:64px;height:64px">${LOGOS.youtube}</div><div style="position:static"><div style="position:static;font:800 28px Disp">Kênh Thành Vũ Đức</div><div class="sub" style="position:static">làm content về AI</div></div></div>`,
 anim(tl, $) {
   tl.to($('.face'), {left: 420, duration: .6, ease: 'power3.inOut'}, .3); tl.to($('.lp'), {opacity: 1, duration: .5}, .4);
   tl.fromTo($('.nm'), {opacity: 0, x: -60, filter: 'blur(10px)'}, {opacity: 1, x: 0, filter: 'blur(0px)', duration: .6, ease: 'expo.out'}, .5);
   pop(tl, $('.c1'), 1.4, .7); pop(tl, $('.c2'), 1.9, .7);
   tl.to([$('.nm'), $('.c1'), $('.c2')], {opacity: 0, x: -30, duration: .3}, 7.9); tl.to($('.lp'), {opacity: 0, duration: .4}, 8.0); tl.to($('.face'), {left: 0, duration: .45, ease: 'power3.inOut'}, 8.0);
 }},

{id: 's57', clip: 'clips/s57.mp4', dur: 10.5, poster: 9.9, name: 'Outro: logo nảy + <em>dải màu quét</em>',
 desc: 'Gốc: cuối video (RN 12:33-12:45) và đoạn chèn thương hiệu (RN 0:36-0:38): khung mặt mờ đi, logo nảy trên nền sáng, dải vàng cong quét ngang. Bản này: logo camera Contentta nảy, dải plum + lavender quét, chip Like / Subscribe đúng lúc bạn nói.',
 html: () => `<div class="ov" style="inset:0;z-index:28;background:var(--ivory);opacity:0">${BG}</div>
   <div class="lg" style="left:840px;top:330px;z-index:30;width:240px;height:170px;color:var(--plum);opacity:0">${LOGOS.mark}</div>
   <div class="wm" style="left:0;right:0;top:530px;z-index:30;text-align:center;font:800 64px Disp;letter-spacing:-.03em;opacity:0">Contentta</div>
   <div class="lk" style="left:740px;top:640px;z-index:30;display:flex;gap:16px;opacity:0">${PILL('p1', 0, 0, 'Like', 'thumb').replace('left:0px;top:0px;', 'position:relative;')}${PILL('p2', 0, 0, 'Subscribe', 'bell').replace('left:0px;top:0px;', 'position:relative;')}</div>
   <div class="rb1" style="left:-1500px;top:-300px;z-index:32;width:520px;height:1800px;rotate:24deg;border-radius:260px;background:var(--plum)"></div>
   <div class="rb2" style="left:-1800px;top:-300px;z-index:31;width:380px;height:1800px;rotate:24deg;border-radius:190px;background:var(--lav)"></div>`,
 anim(tl, $) {
   tl.to($('.face'), {filter: 'blur(14px)', scale: 1.05, duration: .6}, 7.2); tl.to($('.ov'), {opacity: 1, duration: .4}, 7.5);
   tl.fromTo($('.lg'), {opacity: 0, y: -140, scale: .6}, {opacity: 1, y: 0, scale: 1, duration: .7, ease: 'bounce.out'}, 7.7);
   rise(tl, $('.wm'), 8.1, 20); tl.to($('.lk'), {opacity: 1, duration: .2}, 8.9); pop(tl, $('.p1'), 9.0, .5); pop(tl, $('.p2'), 9.8, .5);
   tl.fromTo($('.rb2'), {x: 0}, {x: 4200, duration: .9, ease: 'power3.inOut'}, 9.95); tl.fromTo($('.rb1'), {x: 0}, {x: 4200, duration: .9, ease: 'power3.inOut'}, 10.0);
 }},
);
