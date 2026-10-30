// Gap C scenes s91-s98 (current cut seconds in clips43.txt). Scenes that start right where another one ends begin with the face
// already in that scene's card (at0), then switch side.
const g3at0 = (tl, f, v, to) => { tl.set(f, {...to.box, filter: 'blur(0px)'}, 0); tl.set(v, to.vid, 0); };
const G3THUMB = (cls, x, y, w, im, extra = '') => `<div class="${cls}" style="left:${x}px;top:${y}px;width:${w}px;height:${Math.round(w*9/16)}px;border-radius:${Math.round(w/22)}px;overflow:hidden;box-shadow:0 18px 34px -16px rgba(23,19,13,.45);border:3px solid #fff;${extra}"><img src="img/${im}" style="left:0;top:0;width:100%;height:100%;object-fit:cover"></div>`;
SCENES.push(
{id: 's91', clip: 'clips/s91.mp4', dur: 7.6, poster: 6.8, name: 'Ra lệnh như với <em>editor</em>',
 desc: 'Khung xem trước có khung hình thật của video, ô lệnh gõ "thêm icon" ở chữ "icon", icon bật quanh mặt; lệnh 2 "đổi chữ" ở "edit bất kỳ", gửi ở "ra lệnh", chữ đổi màu; dòng "như nói với editor" ở chữ "editor".',
 html: () => BG + title(620, 96, 'Muốn gì, cứ <em>ra lệnh</em>', '<span class="ed" style="display:inline-block">như đang nói với 1 editor</span>') +
   WIN('pv', 190, 262, 860, 530, `<div style="left:0;top:46px;width:860px;height:484px;overflow:hidden"><img src="img/g3-face.jpg" style="left:0;top:0;width:860px;height:484px;object-fit:cover">
     ${[['sparkles', 150, 90], ['film', 610, 70], ['image', 640, 300], ['wand', 130, 300]].map(([i, x, y], j) => `<div class="pi pi${j}" style="left:${x}px;top:${y}px;width:84px;height:84px;border-radius:24px;background:rgba(255,255,255,.92);display:grid;place-items:center;color:var(--plum);box-shadow:0 10px 24px -10px rgba(23,19,13,.5)">${IC(i, 40)}</div>`).join('')}
     <div class="cpn" style="left:0;right:0;top:404px;text-align:center"><span class="cp" style="position:relative;display:inline-block;padding:8px 20px;border-radius:12px;background:rgba(23,19,13,.72);color:#fff;font:800 34px Disp;letter-spacing:-.02em">AI edit hết</span></div></div>`, 'Xem trước · 7:17') +
   `<div class="ib paper" style="left:190px;top:816px;width:860px;height:84px;border-radius:20px">
     <div class="q1" style="left:26px;top:25px;font-size:24px;white-space:nowrap">${chars('thêm vài icon chạy quanh chỗ này', 'k1')}</div>
     <div class="q2" style="left:26px;top:25px;font-size:24px;white-space:nowrap">${chars('đổi chữ dưới mặt sang màu tím', 'k2')}</div>
     <div class="snd" style="right:14px;top:18px;width:48px;height:48px;border-radius:14px;background:var(--ink-faint);display:grid;place-items:center;color:#fff">${IC('up', 24)}</div></div>`,
 anim(tl, $, f, v) {
   move(tl, f, v, CARD.R, .1); rise(tl, $('.ttl h2'), .4); tl.set($('.ed'), {opacity: 0}, 0); rise(tl, $('.pv'), .5, 40); rise(tl, $('.ib'), .6, 20);
   tl.set($$('.pi'), {opacity: 0}, 0); tl.set($('.q2'), {opacity: 0}, 0);
   type(tl, '.k1', .4, 1.3); tl.to($('.ib'), {borderColor: '#4A3AE0', duration: .2}, .4); tl.to($('.snd'), {backgroundColor: '#4A3AE0', duration: .2}, .4);
   click(tl, $('.snd'), 1.4); tl.to($('.q1'), {opacity: 0, duration: .15}, 1.5);
   $$('.pi').forEach((e, j) => { pop(tl, e, 1.6 + j*.12, .3); tl.fromTo(e, {rotation: -8}, {rotation: 8, duration: 5, ease: 'none'}, 1.6); });
   tl.set($('.q2'), {opacity: 1}, 2.55); type(tl, '.k2', 2.6, 3.6);
   click(tl, $('.snd'), 4.2); tl.to($('.q2'), {opacity: 0, duration: .15}, 4.3);
   tl.to($('.cp'), {backgroundColor: '#4A3AE0', duration: .3}, 4.45); tl.fromTo($('.cp'), {scale: 1.15}, {scale: 1, duration: .45, ease: 'back.out(2)'}, 4.45);
   rise(tl, $('.ed'), 6.2, 12); tl.to($('.ed'), {color: '#4A3AE0', duration: .3}, 6.3);
 }},

{id: 's92', clip: 'clips/s92.mp4', dur: 9.6, poster: 9.3, name: 'Kéo <em>2 file raw</em> vào Claude',
 desc: 'Quy trình edit: 2 file raw thật (youtube ai phan 1/2) sáng vàng ở chữ "màu golden", con trỏ kéo cả 2 vào Claude ở "kéo hai file raw vô trong con Claude", timeline bên dưới bị cắt bỏ các đoạn vấp ở "cắt hết toàn bộ".',
 html: () => BG + title(1330, 96, 'Quy trình <em>edit</em>', 'việc của bạn: kéo 2 file vào') +
   `<div class="lg" style="left:880px;top:300px;display:flex;align-items:center;gap:10px;padding:8px 16px;border-radius:999px;background:rgba(230,180,90,.22);font:700 19px Body;color:#9A6F1E;white-space:nowrap"><i style="position:static;width:14px;height:14px;border-radius:50%;background:var(--gold)"></i>Vàng: bạn làm</div>
    <div class="fs" style="left:880px;top:380px;width:430px;height:220px">
     ${['youtube ai phan 1.mp4', 'youtube ai phan 2.mp4'].map((n, j) => `<div class="fc fc${j}" style="left:0;top:${j*110}px;width:430px;height:92px;border-radius:20px;background:#fff;border:2.5px solid var(--line-strong);box-shadow:var(--shadow);display:flex;align-items:center;gap:16px;padding:0 20px;font:700 22px Body;white-space:nowrap">
       <span class="fi" style="position:relative;width:52px;height:52px;border-radius:14px;background:var(--ivory-deep);display:grid;place-items:center;color:var(--ink-muted)">${IC('video', 28)}</span>${n}</div>`).join('')}</div>
    ${LINE('ar', 1330, 490, 1490, 490, 'var(--line-strong)', 4)}
    <div class="cl paper" style="left:1510px;top:400px;width:180px;height:180px;border-radius:48px;padding:42px">${LOGOS.claude}</div>
    <div class="cln" style="left:1500px;top:596px;width:200px;text-align:center;font:800 24px Disp">Claude Code</div>
    ${PILL('rcv', 900, 455, 'Đã nhận 2 file · 23:53', 'check')}
    <div class="tlw paper" style="left:880px;top:680px;width:940px;height:200px;border-radius:24px">
     <div style="left:26px;top:20px;font:700 15px Body;letter-spacing:.16em;color:var(--ink-muted)">TIMELINE</div>
     <div class="trk" style="left:26px;top:60px;width:888px;height:110px">
      ${[[0, 120, 0], [120, 50, 1], [170, 160, 0], [330, 40, 1], [370, 130, 0], [500, 70, 1], [570, 180, 0], [750, 38, 1], [788, 100, 0]].map(([x, w, bad], j) =>
        `<div class="sg ${bad ? 'bad' : 'ok'}" data-x="${x}" style="left:${x}px;top:0;width:${w - 4}px;height:110px;border-radius:10px;overflow:hidden;background:${bad ? 'rgba(240,122,90,.0)' : 'rgba(183,168,255,.35)'};border:2px solid ${bad ? 'rgba(23,19,13,.16)' : 'rgba(74,58,224,.35)'}">
          ${LN(10, 20, Math.max(10, w - 28), 'rgba(23,19,13,.12)', 10)}<svg viewBox="0 0 100 30" preserveAspectRatio="none" style="position:absolute;left:0;top:56px;width:100%;height:44px"><path d="M0 15 ${Array.from({length: 20}, (_, k) => `L${k*5 + 2.5} ${15 + ((k*7 + j*3) % 11 - 5)*2.4}`).join(' ')} L100 15" fill="none" stroke="${bad ? '#C9B9AE' : '#7B6CFF'}" stroke-width="2"/></svg></div>`).join('')}</div></div>` + CUR('cu', 1300, 820),
 anim(tl, $, f, v) {
   move(tl, f, v, CARD.L, .3); rise(tl, $('.ttl h2'), 1.6); tl.fromTo($('.ttl p'), {opacity: 0}, {opacity: 1, duration: .4}, 2.7);
   $$('.fc').forEach((e, j) => rise(tl, e, 2.7 + j*.12, 24)); pop(tl, $('.cl'), 3.0, .5); rise(tl, $('.cln'), 3.1, 10); draw(tl, $('.ar'), 3.2, .4);
   pop(tl, $('.lg'), 4.4, .6); $$('.fc').forEach((e, j) => { tl.to(e, {borderColor: '#E6B45A', backgroundColor: '#FFF7E6', duration: .3}, 4.5 + j*.1); tl.to(e.querySelector('.fi'), {backgroundColor: 'rgba(230,180,90,.3)', color: '#B7862A', duration: .3}, 4.5 + j*.1); });
   tl.fromTo($('.cu'), {opacity: 0}, {opacity: 1, duration: .2}, 5.5); glide(tl, $('.cu'), 5.6, 1180, 478, .4); click(tl, $('.cu'), 5.95);
   tl.to($('.fs'), {x: 505, y: 0, scale: .36, duration: 1.1, ease: 'power2.inOut'}, 6.2); glide(tl, $('.cu'), 6.2, 1640, 500, 1.1);
   tl.to($('.fs'), {opacity: 0, duration: .25}, 7.15); tl.to($('.cu'), {opacity: 0, duration: .2}, 7.4);
   lit(tl, $('.cl'), 7.4, '#D97757', 'rgba(217,119,87,.12)'); hop(tl, $('.cl'), 7.4, 22);
   pop(tl, $('.rcv'), 7.5, .6); tl.to($('.rcv'), {color: '#2F7D57', borderColor: '#3E9B6E', duration: .2}, 7.6);
   rise(tl, $('.tlw'), 7.6, 30);
   tl.to($$('.sg.bad'), {backgroundColor: 'rgba(240,122,90,.45)', borderColor: '#F07A5A', duration: .2}, 8.7);
   tl.to($$('.sg.bad'), {scaleY: 0, opacity: 0, duration: .3, ease: 'power2.in'}, 8.95);
   let cut = 0; $$('.sg').forEach(e => { if (e.classList.contains('bad')) { cut += parseFloat(e.style.width) + 4; return; }
     if (cut) tl.to(e, {x: -cut, duration: .35, ease: 'power3.inOut'}, 9.15); });
 }},

{id: 's93', clip: 'clips/s93.mp4', dur: 7.1, poster: 6.8, name: 'Điền sẵn để <em>upload</em>',
 desc: 'Nối từ s41 (mặt đang ở góc dưới trái) sang trái. Bảng chi tiết video: mô tả tự điền ở chữ "description", thanh tải lên chạy ở "upload", 3 thumbnail thật của video này bật ở "thumbnail", khung chọn chạy ở "edit".',
 html: () => BG + title(1330, 86, 'Sẵn sàng <em>upload</em>', 'title, mô tả, thumbnail: AI làm') +
   WIN('yt', 860, 236, 960, 640, `
     <div style="left:34px;top:70px;font:700 15px Body;letter-spacing:.14em;color:var(--ink-muted)">TIÊU ĐỀ</div>
     <div style="left:30px;right:30px;top:96px;height:58px;border-radius:12px;border:1.5px solid var(--line-strong);padding:14px 16px;font:700 21px Body;white-space:nowrap;overflow:hidden">Hệ thống YouTube AI: quay xong, Claude Code edit hết</div>
     <div style="left:34px;top:176px;font:700 15px Body;letter-spacing:.14em;color:var(--ink-muted)">MÔ TẢ</div>
     <div class="ds" style="left:30px;right:30px;top:202px;height:176px;border-radius:12px;border:1.5px solid var(--line-strong);padding:12px 16px;font:18px Body;line-height:1.5;overflow:hidden">
       ${['➡️ Tải tài liệu miễn phí: contentta.vn/tai-lieu', '<span style="position:relative;color:#1A66D0">0:00</span> Intro', '<span style="position:relative;color:#1A66D0">0:38</span> Demo CapCut', '<span style="position:relative;color:#1A66D0">1:39</span> Cài Claude Code']
         .map((t, j) => `<div class="dl dl${j}" style="position:relative;white-space:nowrap">${t}</div>`).join('')}</div>
     <div style="left:34px;top:400px;font:700 15px Body;letter-spacing:.14em;color:var(--ink-muted)">THUMBNAIL</div>
     ${['g3-t4.jpg', 'g3-t5.jpg', 'g3-t6.jpg'].map((im, j) => G3THUMB(`th th${j}`, 30 + j*302, 428, 288, im, 'border-color:var(--line)')).join('')}
     <div class="sel" style="left:${30 - 8}px;top:${428 - 8}px;width:304px;height:178px;border-radius:20px;border:4px solid var(--plum);box-shadow:0 0 0 8px rgba(123,108,255,.15);opacity:0"></div>`, 'YouTube Studio · Chi tiết video') +
   `<div class="up" style="left:860px;top:900px;width:960px;height:56px;display:flex;align-items:center;gap:16px;font:700 19px Body;white-space:nowrap">
     <span class="ul" style="position:relative;width:250px;color:var(--ink-soft)">Đang tải lên…</span>
     <span style="position:relative;flex:1;height:14px;border-radius:7px;background:var(--ivory-deep)"><i class="ub" style="left:0;top:0;bottom:0;width:100%;border-radius:7px;background:#FF0000;transform-origin:0 50%"></i></span>
     <span class="up2" style="position:relative;width:70px;text-align:right">100%</span></div>`,
 anim(tl, $, f, v) {
   g3at0(tl, f, v, CARD.BL); move(tl, f, v, CARD.L, .15); rise(tl, $('.ttl'), .35); rise(tl, $('.yt'), .3, 40);
   tl.set($$('.dl'), {opacity: 0}, 0); $$('.dl').forEach((e, j) => tl.fromTo(e, {opacity: 0, x: -12}, {opacity: 1, x: 0, duration: .2}, .6 + j*.18));
   tl.to($('.ds'), {borderColor: '#4A3AE0', duration: .2}, .6); tl.to($('.ds'), {borderColor: 'rgba(23,19,13,.16)', duration: .3}, 1.6);
   rise(tl, $('.up'), 2.4, 10); tl.set($('.ub'), {scaleX: 0}, 0); tl.to($('.ub'), {scaleX: 1, duration: 1.1, ease: 'power1.inOut'}, 2.5);
   tl.set($('.up2'), {opacity: 0}, 0); tl.set($('.up2'), {opacity: 1}, 3.6); tl.set($('.ul'), {innerHTML: 'Đã tải lên', color: '#2F7D57'}, 3.6); tl.to($('.ub'), {backgroundColor: '#3E9B6E', duration: .2}, 3.6);
   tl.set($$('.th'), {opacity: 0}, 0); $$('.th').forEach((e, j) => tl.fromTo(e, {opacity: 0, y: 30, scale: .8}, {opacity: 1, y: 0, scale: 1, duration: .45, ease: 'back.out(1.6)'}, 3.8 + j*.12));
   [[0, 4.5], [1, 5.9]].forEach(([j, t], k) => tl.to($('.sel'), {opacity: 1, left: 22 + j*302, duration: k ? .35 : .2, ease: 'power3.inOut'}, t));
   tl.to($('.th1'), {scale: 1.04, duration: .3, ease: 'back.out(2)'}, 6.0);
 }},

{id: 's94', clip: 'clips/s94.mp4', dur: 10.1, poster: 9.8, name: 'Codex <em>tạo ảnh</em> rất đẹp',
 desc: 'Nối từ s24 (mặt bên phải) sang trái. Cửa sổ Codex gõ lệnh tạo ảnh ở "tạo ảnh", 3 thumbnail thật (t4-t6) xoè ra ở "thumbnail", sáng lên ở "xịn"; chip Website ở "website", Web app ở "web app", "+ nhiều thứ" ở "nhiều thứ".',
 html: () => BG + title(1330, 86, 'Codex vẽ <em>rất đẹp</em>', 'mình mua thêm gói này') +
   `<div class="cx" style="left:880px;top:236px;width:920px;height:170px;border-radius:22px;background:#1F1B16;box-shadow:var(--shadow);overflow:hidden;font:21px Mono;color:#F3ECE0">
     <div style="left:0;right:0;top:0;height:42px;background:#2A251F;display:flex;align-items:center;gap:8px;padding:0 18px">${DOTS}<span style="position:static;margin-left:12px;font:15px Body;color:#8A8073">Codex</span></div>
     <div style="left:28px;top:66px;white-space:nowrap"><span style="position:static;color:#B7A8FF">$</span> ${chars('codex exec "thumbnail AI LÀM HẾT, mặt thật"', 'k')}</div>
     <div class="r1" style="left:28px;top:110px;color:#A9E0C2;white-space:nowrap">✓ image_gen: t4.png  t5.png  t6.png</div></div>` +
   `<div class="gl" style="left:1120px;top:440px;width:460px;height:290px;border-radius:30px;background:radial-gradient(closest-side,rgba(183,168,255,.7),rgba(183,168,255,0));opacity:0;filter:blur(10px)"></div>` +
   [['g3-t4.jpg', -7, 890], ['g3-t5.jpg', 0, 1140], ['g3-t6.jpg', 7, 1390]].map(([im, r, x], j) => G3THUMB(`tt tt${j}`, x, 470, 400, im, `rotate:${r}deg`)).join('') +
   `<div class="sp1" style="left:1560px;top:430px;color:var(--plum)">${IC('sparkles', 54)}</div>` +
   PILL('w1', 950, 800, 'Website', 'monitor') + PILL('w2', 1190, 800, 'Web app', 'code') + PILL('w3', 1430, 800, 'nhiều thứ nữa', 'plus'),
 anim(tl, $, f, v) {
   g3at0(tl, f, v, CARD.R); move(tl, f, v, CARD.L, .2); rise(tl, $('.ttl'), .9); rise(tl, $('.cx'), .5, 30);
   type(tl, '.k', 1.5, 2.6); tl.set($('.r1'), {opacity: 0}, 0); tl.to($('.r1'), {opacity: 1, duration: .15}, 2.65);
   tl.set($$('.tt'), {opacity: 0}, 0); [1, 0, 2].forEach((j, k) => tl.fromTo($('.tt' + j), {opacity: 0, y: -120, scale: .5, x: (1 - j)*250}, {opacity: 1, y: 0, scale: 1, x: 0, duration: .6, ease: 'back.out(1.4)'}, 2.8 + k*.12));
   tl.set($('.tt1'), {zIndex: 3}, 0); tl.to($('.gl'), {opacity: 1, duration: .3}, 4.2); tl.to($('.tt1'), {scale: 1.1, duration: .35, ease: 'back.out(2)'}, 4.2);
   pop(tl, $('.sp1'), 4.25, .3); tl.to($('.sp1'), {rotation: 25, duration: .6, yoyo: true, repeat: 3}, 4.6);
   tl.to($('.gl'), {opacity: 0, duration: .4}, 6.0); tl.to($('.tt1'), {scale: 1, duration: .4}, 6.0); tl.to($('.sp1'), {opacity: 0, duration: .3}, 6.0);
   tl.to($$('.tt'), {y: -20, duration: .4, ease: 'power2.out'}, 7.2);
   pop(tl, $('.w1'), 7.4, .5); lit(tl, $('.w1'), 7.5); pop(tl, $('.w2'), 9.2, .5); lit(tl, $('.w2'), 9.3); pop(tl, $('.w3'), 9.95, .5);
 }},

{id: 's95', clip: 'clips/s95.mp4', dur: 9.2, poster: 9.1, name: '600 nghìn cho 1 <em>editor</em>',
 desc: 'Nối từ s94 (mặt bên trái) sang phải. Thẻ giá "~600.000đ / tháng" bật ở chữ "600 nghìn", mũi tên ra 3 thumbnail thật ở "edit... thumbnail", mascot đội mũ "Editor thumbnail" nhảy ở "editor thực thụ", dấu "Xứng đáng" ở "hoàn toàn xứng đáng".',
 html: () => BG + title(620, 96, 'Như thuê <em>1 editor</em>', 'chỉ khoảng 600 nghìn mỗi tháng') +
   `<div class="pr paper" style="left:150px;top:330px;width:400px;height:330px;border-radius:28px">
     <div style="left:30px;top:30px;width:70px;height:70px;border-radius:18px;overflow:hidden;border:1px solid var(--line)"><img src="img/chatgpt.png" style="left:0;top:0;width:100%;height:100%"></div>
     <div style="left:118px;top:34px;font:800 28px Disp">Gói Codex</div><div class="sub" style="left:118px;top:74px">ChatGPT · tạo ảnh</div>
     <div class="pv" style="left:30px;top:150px;font:800 74px Disp;letter-spacing:-.04em;color:var(--plum)">~600K</div>
     <div class="sub" style="left:32px;top:250px;font-size:22px">đồng / tháng</div></div>
    ${LINE('ar', 570, 495, 690, 495, 'var(--line-strong)', 4)}` +
   [['g3-t4.jpg', 720, 300], ['g3-t5.jpg', 750, 420], ['g3-t6.jpg', 780, 540]].map(([im, x, y], j) => G3THUMB(`tt tt${j}`, x, y, 300, im)).join('') +
   MASC('ms', 760, 760, 11, '#4A3AE0', '#E6B45A') + `<div class="ml" style="left:910px;top:790px;font:800 28px Disp;white-space:nowrap">Editor <span class="em">thực thụ</span></div>
    <div class="ok" style="left:170px;top:720px;display:flex;align-items:center;gap:16px;padding:20px 36px;border-radius:999px;background:#3E9B6E;color:#fff;font:800 48px Disp;white-space:nowrap;rotate:-4deg;box-shadow:0 14px 30px -12px rgba(46,125,87,.6)">${IC('check', 46)}Xứng đáng</div>`,
 anim(tl, $, f, v) {
   g3at0(tl, f, v, CARD.L); move(tl, f, v, CARD.R, 1.0); rise(tl, $('.ttl h2'), 1.4); tl.fromTo($('.ttl p'), {opacity: 0}, {opacity: 1, duration: .4}, 3.4);
   rise(tl, $('.pr'), 2.0, 40); tl.set($('.pv'), {opacity: 0}, 0); pop(tl, $('.pv'), 3.4, .4);
   draw(tl, $('.ar'), 5.0, .4); $$('.tt').forEach((e, j) => tl.fromTo(e, {opacity: 0, x: -60, scale: .7}, {opacity: 1, x: 0, scale: 1, duration: .5, ease: 'back.out(1.6)'}, 6.0 + j*.15));
   pop(tl, $('.ms'), 7.1, .4); rise(tl, $('.ml'), 7.2, 10); hop(tl, $('.ms'), 7.5, 26);
   tl.fromTo($('.ok'), {opacity: 0, scale: 1.8}, {opacity: 1, scale: 1, duration: .35, ease: 'back.out(1.4)'}, 8.9);
 }},

{id: 's96', clip: 'clips/s96.mp4', dur: 7.0, poster: 6.8, name: 'Bị bảo <em>giấu kỹ năng</em>',
 desc: 'Video thật trên kênh (thumbnail + trang REA 11.088 view) hiện ở chữ "chia sẻ ở trên đây", 2 bong bóng lời người xem bật ở "giấu kỹ năng" và "không chia sẻ hết", tiêu đề đổi theo.',
 html: () => BG + `<div class="t0">${title(620, 96, 'Chia sẻ <em>trên kênh</em>', 'video REA, hơn 11 nghìn view')}</div><div class="t1">${title(620, 96, 'Bị bảo <em>giấu kỹ năng</em>', 'nhiều người nói vậy')}</div>
   <div class="vc paper" style="left:170px;top:286px;width:880px;height:560px;border-radius:26px">
     ${G3THUMB('vt', 30, 30, 500, 'rea-t1.jpg', 'border-color:var(--line)')}
     <div style="left:30px;top:340px;width:820px;height:154px;border-radius:12px;overflow:hidden"><img src="img/g3-rea-meta.png" style="left:0;top:0;width:820px"></div>
     <div class="hl" style="left:42px;top:417px;width:144px;height:28px;border-radius:8px;border:3px solid var(--plum);opacity:0"></div></div>
   <div class="b1" style="left:610px;top:330px;padding:20px 26px;border-radius:26px 26px 26px 6px;background:#FFE3D9;border:2px solid #F07A5A;color:#B9472B;font:800 30px Disp;white-space:nowrap;box-shadow:var(--shadow)">"Giấu kỹ năng à?"</div>
   <div class="b2" style="left:680px;top:470px;padding:20px 26px;border-radius:26px 26px 6px 26px;background:#FFE3D9;border:2px solid #F07A5A;color:#B9472B;font:800 30px Disp;white-space:nowrap;box-shadow:var(--shadow)">"Không chia sẻ hết"</div>`,
 anim(tl, $, f, v) {
   move(tl, f, v, CARD.R, .3); tl.set($('.t1'), {opacity: 0}, 0); rise(tl, $('.t0 .ttl'), 1.2); rise(tl, $('.vc'), .8, 40);
   tl.fromTo($('.vt'), {scale: .92}, {scale: 1, duration: .5, ease: 'back.out(2)'}, 2.8); tl.to($('.hl'), {opacity: 1, duration: .25}, 2.9);
   tl.to($('.t0'), {opacity: 0, duration: .25}, 4.4); tl.to($('.t1'), {opacity: 1, duration: .3}, 4.5); rise(tl, $('.t1 .ttl'), 4.5);
   tl.to($('.vc'), {opacity: .55, duration: .3}, 4.5);
   tl.fromTo($('.b1'), {opacity: 0, scale: .4, y: 30}, {opacity: 1, scale: 1, y: 0, duration: .45, ease: 'back.out(1.8)'}, 4.5); tl.to($('.b1'), {x: -8, duration: .06, repeat: 5, yoyo: true}, 5.0);
   tl.fromTo($('.b2'), {opacity: 0, scale: .4, y: 30}, {opacity: 1, scale: 1, y: 0, duration: .45, ease: 'back.out(1.8)'}, 6.2);
 }},

{id: 's97', clip: 'clips/s97.mp4', dur: 5.6, poster: 5.4, name: 'Bậc thang <em>từng bước</em>',
 desc: 'Nối từ s96 (mặt bên phải) sang trái. Mascot đứng dưới chân thang có dấu "?" ở "không có biết", tiêu đề ở "các bạn cần", 4 bậc thật của quy trình (Tải skill, Dán file raw, Duyệt 1 lần, Render + đăng) bật lên và mascot leo ở "hướng dẫn từng bước".',
 html: () => BG + title(1330, 96, 'Bạn cần <em>từng bước</em>', 'mình đã không nghĩ tới') +
   ['Tải skill', 'Dán file raw', 'Duyệt 1 lần', 'Render + đăng'].map((n, j) => `<div class="stp stp${j}" style="left:${900 + j*215}px;top:${740 - j*110}px;width:205px;height:${150 + j*110}px;border-radius:22px 22px 0 0;background:rgba(255,255,255,.85);border:2.5px solid var(--line-strong);border-bottom:none">
     <div class="sn" style="left:18px;top:16px;width:44px;height:44px;border-radius:50%;background:var(--ivory-deep);display:grid;place-items:center;font:800 22px Disp;color:var(--ink-muted)">${j + 1}</div>
     <div style="left:18px;top:74px;font:800 25px Disp;white-space:nowrap">${n}</div></div>`).join('') +
   `<i style="left:880px;top:890px;width:900px;height:3px;background:var(--line-strong);border-radius:2px"></i>` + MASC('ms', 935, 824, 11) +
   `<div class="qm" style="left:1085px;top:744px;width:64px;height:64px;border-radius:50%;background:#fff;border:2px solid var(--line-strong);display:grid;place-items:center;font:800 36px Disp;color:var(--plum);box-shadow:var(--shadow)">?</div>`,
 anim(tl, $, f, v) {
   g3at0(tl, f, v, CARD.R); move(tl, f, v, CARD.L, .2); pop(tl, $('.ms'), .7, .4); pop(tl, $('.qm'), 1.5, .3); hop(tl, $('.qm'), 1.9, 12);
   rise(tl, $('.ttl'), 2.2);
   tl.set($$('.stp'), {opacity: 0}, 0); tl.to($('.qm'), {opacity: 0, duration: .2}, 4.1);
   $$('.stp').forEach((e, j) => { tl.fromTo(e, {opacity: 0, scaleY: 0, transformOrigin: '50% 100%'}, {opacity: 1, scaleY: 1, duration: .35, ease: 'back.out(1.6)'}, 4.0 + j*.15);
     tl.to(e.querySelector('.sn'), {backgroundColor: '#4A3AE0', color: '#fff', duration: .2}, 4.35 + j*.2);
     tl.to($('.ms'), {left: 935 + j*215, top: 674 - j*110, duration: .18, ease: 'power2.out'}, 4.3 + j*.2); });
 }},

{id: 's98', clip: 'clips/s98.mp4', dur: 5.9, poster: 5.2, name: 'Hiểu skill + Claude Code = <em>làm được</em>',
 desc: 'Nối từ s97 (mặt bên trái) sang phải. Bong bóng "mình hình dung" ở chữ "hình dung", ô Skill bật ở "skill", ô Claude Code ở "Claude Code", ra tick "Làm được"; mặt về full khung ngay trước giả lập màn hình Claude.',
 html: () => BG + title(620, 120, 'Hiểu là <em>làm được</em>', 'cách mình hình dung') +
   `<div class="cld" style="left:150px;top:320px;width:940px;height:440px;border-radius:220px;border:3px dashed var(--line-strong);background:rgba(255,255,255,.5)"></div>
    <i class="d1" style="left:1060px;top:780px;width:36px;height:36px;border-radius:50%;border:3px dashed var(--line-strong)"></i><i class="d2" style="left:1110px;top:830px;width:22px;height:22px;border-radius:50%;border:3px dashed var(--line-strong)"></i>` +
   TILE('a1', 250, 430, 150, IC('wand', 64), 'Hiểu skill') +
   `<div class="pl" style="left:445px;top:470px;font:800 70px Disp;color:var(--ink-faint)">+</div>` +
   TILE('a2', 530, 430, 150, `<div style="position:static;width:76px;height:76px">${LOGOS.claude}</div>`, 'Hiểu Claude Code') +
   `<div class="eq" style="left:735px;top:470px;font:800 70px Disp;color:var(--ink-faint)">=</div>
    <div class="ok" style="left:830px;top:430px;width:150px;height:150px;border-radius:50%;background:#3E9B6E;color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -12px rgba(46,125,87,.6)">${IC('check', 76)}</div>
    <div class="okl" style="left:805px;top:596px;width:200px;text-align:center;font:800 24px Disp">Làm được</div>`,
 anim(tl, $, f, v) {
   g3at0(tl, f, v, CARD.L); move(tl, f, v, CARD.R, .2); rise(tl, $('.ttl h2'), 1.4); tl.fromTo($('.ttl p'), {opacity: 0}, {opacity: 1, duration: .4}, 1.5);
   tl.fromTo($('.cld'), {opacity: 0, scale: .85}, {opacity: 1, scale: 1, duration: .5, ease: 'expo.out'}, 1.4); pop(tl, $('.d2'), 1.5, .3); pop(tl, $('.d1'), 1.6, .3);
   pop(tl, $('.a1'), 3.5, .5); lit(tl, $('.a1'), 3.7); pop(tl, $('.pl'), 3.8, .5);
   pop(tl, $('.a2'), 4.75, .5); lit(tl, $('.a2'), 4.9, '#D97757', 'rgba(217,119,87,.12)'); pop(tl, $('.eq'), 4.95, .5); pop(tl, $('.ok'), 5.05, .4); rise(tl, $('.okl'), 5.1, 8);
   move(tl, f, v, FULL, 5.35, .55);
 }},
);
