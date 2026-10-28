// Scenes s24-s36: mini table, pipeline, isometric layers, branches, cost bars, file grid, timer card, icon→coins, warning flow, loop, two windows, steps row, tier slider.
SCENES.push(
{id: 's24', clip: 'clips/s24.mp4', dur: 11.5, poster: 11.2, name: 'Bảng nhỏ <em>chạy số</em>',
 desc: 'Gốc: "It draws the whole Agents panel" (RN 3:42): bảng agent kèm chi phí từng dòng hiện dần, có thanh mức. Bản này: Claude Max 111 đô hiện ở chữ "111", Codex 22 đô ở chữ "Codex", dòng tổng chốt cuối.',
 html: () => BG + title(610, 150, 'Chi phí <em>mỗi tháng</em>', 'số thật của mình') +
   `<div class="tbw paper" style="left:140px;top:320px;width:940px;height:470px">
     <div style="left:40px;top:34px;right:40px;display:flex;justify-content:space-between;font:700 15px Body;letter-spacing:.16em;color:var(--ink-muted)"><span style="position:static">GÓI</span><span style="position:static">ĐÔ / THÁNG</span></div>
     ${[['claude', 'Claude Max', 'chạy Claude Code', 111, '#D97757'], ['codex', 'Codex (ChatGPT)', 'tạo thumbnail', 22, '#10A37F']].map(([k, n, s, v, c], j) => `<div class="rw rw${j}" style="left:40px;right:40px;top:${84 + j*130}px;height:110px;border-bottom:1px solid var(--line)">
       <div style="left:0;top:18px;width:70px;height:70px;border-radius:18px;background:#fff;border:1px solid var(--line);padding:${k == 'codex' ? 0 : 14}px;overflow:hidden">${k == 'codex' ? '<img src="img/chatgpt.png" style="position:static;width:100%;height:100%">' : LOGOS.claude}</div>
       <div style="left:94px;top:20px;font:800 30px Disp">${n}</div><div class="sub" style="left:94px;top:62px">${s}</div>
       <div style="left:430px;top:46px;width:260px;height:14px;border-radius:7px;background:var(--ivory-deep)"><i class="bar" style="left:0;top:0;bottom:0;width:${v/1.2}%;border-radius:7px;background:${j ? 'var(--sky)' : 'var(--plum)'};transform-origin:0 50%"></i></div>
       <div class="vv" style="right:0;top:28px;font:800 44px Disp">${v}</div></div>`).join('')}
     <div class="tot" style="left:40px;right:40px;top:360px;display:flex;justify-content:space-between;align-items:center"><span style="position:static;font:800 30px Disp">Tổng</span><span style="position:static;font:800 52px Disp;color:var(--plum)">133 đô</span></div></div>`,
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.R, .3); rise(tl, $('.ttl'), .6); rise(tl, $('.tbw'), .8, 40);
   [[5.0, 6.8], [10.4, 10.6]].forEach(([t, tb], j) => { rise(tl, $('.rw' + j), t, 16); draw(tl, $('.rw' + j + ' .bar'), tb, .6); pop(tl, $('.rw' + j + ' .vv'), tb, .6); });
   rise(tl, $('.tot'), 10.9, 12);
 }},

{id: 's25', clip: 'clips/s25.mp4', dur: 16.5, poster: 16.3, name: 'Ống dẫn: chat → skill → <em>kết quả</em>',
 desc: 'Gốc: "Describe what you want" (RN 3:54): bong bóng chat → hộp skill có sẵn → mod mới, mũi tên nối dần. Bản này: repo GitHub hiện ở "copy", bong bóng "setup cho tôi", ra 3 chip Node.js, Python, ffmpeg.',
 html: () => BG + title(1330, 120, 'Dán link, <em>nó tự cài</em>', 'không cần gõ lệnh') +
   `<div class="rp paper" style="left:860px;top:420px;width:260px;height:200px;border-radius:26px"><div style="left:90px;top:30px;width:80px;height:80px">${LOGOS.github}</div><div style="left:0;right:0;top:130px;text-align:center;font:700 17px Mono">youtube-ai-editor</div></div>
    ${LINE('p1', 1125, 520, 1210, 520, 'var(--line-strong)')}
    <div class="bb" style="left:1215px;top:470px;padding:22px 26px;border-radius:24px 24px 24px 6px;background:var(--plum);color:#fff;font:700 26px Body;white-space:nowrap">"setup cho tôi"</div>
    ${LINE('p2', 1490, 520, 1560, 520, 'var(--line-strong)')}` +
   [['Node.js', 'code'], ['Python', 'terminal'], ['ffmpeg', 'film']].map(([n, i], j) => PILL(`oc oc${j}`, 1570, 390 + j*90, n, i)).join(''),
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.L, .3); rise(tl, $('.ttl'), .6);
   rise(tl, $('.rp'), .6, 30); tl.to($('.rp'), {borderColor: '#4A3AE0', duration: .3}, 9.0); hop(tl, $('.rp'), 9.0, 18);
   draw(tl, $('.p1'), 11.4, .3); pop(tl, $('.bb'), 11.9, .6);
   draw(tl, $('.p2'), 13.4, .3); [13.7, 14.8, 16.0].forEach((t, j) => { pop(tl, $('.oc' + j), t, .5); tl.to($('.oc' + j), {borderColor: '#3E9B6E', duration: .2}, t + .3); });
 }},

{id: 's26', clip: 'clips/s26.mp4', dur: 10.1, poster: 9.8, name: 'Các lớp <em>tách 3D</em>',
 desc: 'Gốc: "A great first mod" (RN 4:27-4:30): khối isometric nhiều lớp tách ra, lớp trên đổi màu, nhãn chỉ vào từng lớp. Bản này: khung mặt thật, lớp B-roll thật, lớp chữ tách ra ở "style edit", sáng màu ở "B-roll", nhãn "3D".',
 html: () => BG + title(610, 130, 'Nhiều <em>lớp</em> chồng lên', 'video gốc, B-roll, chữ') +
   `<div class="iso" style="left:330px;top:470px;width:520px;height:300px;transform:rotateX(58deg) rotateZ(-38deg);transform-style:preserve-3d">
     ${[['img/ov-027-hero.jpg', 'Video gốc'], ['img/rea-330.jpg', 'B-roll'], ['', 'Chữ + SFX']].map(([im, n], j) => `<div class="ly ly${j}" style="left:0;top:0;width:520px;height:292px;border-radius:18px;border:3px solid ${j == 2 ? 'var(--plum)' : 'var(--line-strong)'};background:${j == 2 ? 'rgba(183,168,255,.35)' : '#fff'};overflow:hidden;box-shadow:0 30px 40px -20px rgba(23,19,13,.35)">
       ${im ? `<img class="li" src="${im}" style="left:0;top:0;width:100%;height:100%;object-fit:cover;filter:grayscale(1);opacity:.55">` : `<div style="left:40px;top:200px;font:800 46px Disp;color:var(--plum)">Bullet <span class="em">là đủ</span></div>`}</div>`).join('')}</div>` +
   ['Video gốc', 'B-roll', 'Chữ + SFX'].map((n, j) => `<div class="lb lb${j}" style="left:880px;top:${640 - j*150}px;font:800 26px Disp;white-space:nowrap">${n}</div>`).join(''),
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.R, .3); rise(tl, $('.ttl'), .6); tl.fromTo($('.iso'), {opacity: 0}, {opacity: 1, duration: .4}, .7);
   [0, 1, 2].forEach(j => tl.fromTo($('.ly' + j), {z: 0}, {z: j*120, duration: .8, ease: 'expo.out'}, 2.2 + j*.08));
   [0, 1, 2].forEach(j => rise(tl, $('.lb' + j), 2.5 + j*.12, 10));
   tl.to($$('.li'), {filter: 'grayscale(0)', opacity: 1, duration: .5}, 7.1);
   tl.to($('.lb1'), {color: '#4A3AE0', duration: .3}, 7.1);
   tl.fromTo($('.iso'), {rotationZ: -38}, {rotationZ: -30, duration: 9, ease: 'none'}, .7);
 }},

{id: 's27', clip: 'clips/s27.mp4', dur: 11.6, poster: 11.0, name: 'Nhánh toả từ <em>1 gốc</em>',
 desc: 'Gốc: "Steer what it looks out for" (RN 5:09-5:15): icon gốc toả 3 nhánh cong tới 3 nhãn, nhãn sáng theo lời. Bản này: kênh đối thủ toả 3 nhánh Bố cục, Màu, Chữ, rồi ra 1 thumbnail thật của kênh.',
 html: () => BG + title(1330, 120, 'Học từ <em>đối thủ</em>', 'rồi làm thumbnail cho kênh mình') +
   TILE('src', 870, 470, 120, `<div style="position:static;width:70px;height:70px">${LOGOS.youtube}</div>`, 'Kênh đối thủ') +
   ['Bố cục', 'Màu', 'Chữ'].map((n, j) => LINE(`br br${j}`, 995, 530, 1135, 410 + j*120, 'var(--line-strong)') + PILL(`bp bp${j}`, 1140, 385 + j*120, n)).join('') +
   LINE('to', 1330, 530, 1440, 530, 'var(--line-strong)') +
   `<div class="res paper" style="left:1450px;top:420px;width:400px;height:250px;border-radius:20px;padding:10px"><img src="img/rea-t1.jpg" style="left:10px;top:10px;width:380px;height:214px;object-fit:cover;border-radius:12px"></div>
    <div class="rl" style="left:1450px;top:690px;width:400px;text-align:center;font:800 24px Disp">Thumbnail <span class="em">kênh mình</span></div>
    <div class="ben" style="left:860px;top:690px;padding:8px 16px;border-radius:999px;background:var(--ivory-deep);font:700 18px Body;white-space:nowrap">học từ kênh Ben AI</div>`,
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.L, .3); rise(tl, $('.ttl'), .6); pop(tl, $('.src'), 2.0, .5); lit(tl, $('.src'), 3.5, '#FF0000', 'rgba(255,0,0,.08)');
   [0, 1, 2].forEach(j => { draw(tl, $('.br' + j), 4.0 + j*.3, .3); pop(tl, $('.bp' + j), 4.2 + j*.3, .5); });
   draw(tl, $('.to'), 5.8, .3); rise(tl, $('.res'), 6.0, 30); rise(tl, $('.rl'), 6.2, 10); pop(tl, $('.ben'), 10.5, .6);
 }},

{id: 's28', clip: 'clips/s28.mp4', dur: 16.1, poster: 15.6, name: 'So 2 bên + <em>thanh mức</em>',
 desc: 'Gốc: "It runs a second agent" (RN 5:18-5:27): 2 mascot so token, thanh mức dài ngắn, cột bên cạnh có nhãn "uses an LLM" / "no LLM needed". Bản này: HeyGen avatar vs tự quay, thanh chi phí và 2 nhận xét của bạn.',
 html: () => BG + title(610, 130, 'HeyGen <em>chưa đáng</em>', 'mình vẫn tự quay') +
   [['HeyGen avatar', 'user', '#F07A5A', '30-40 đô / video'], ['Tự quay', 'video', '#3E9B6E', '0 đồng']].map(([n, i, c, v], j) => `<div class="cp cp${j}" style="left:${170 + j*440}px;top:330px;width:380px">
     ${TILE('ti', 130, 0, 120, IC(i, 56))}<div style="left:0;right:0;top:140px;text-align:center;font:800 28px Disp">${n}</div>
     <div style="left:20px;right:20px;top:200px;height:18px;border-radius:9px;background:var(--ivory-deep)"><i class="cb" style="left:0;top:0;bottom:0;width:${j ? 6 : 92}%;border-radius:9px;background:${c};transform-origin:0 50%"></i></div>
     <div class="cv" style="left:0;right:0;top:232px;text-align:center;font:700 22px Body;color:${c}">${v}</div></div>`).join('') +
   PILL('k1', 200, 640, 'AI còn hơi dở', 'alert') + PILL('k2', 520, 640, 'Hơi mắc', 'coin'),
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.R, .3); rise(tl, $('.ttl'), .6);
   rise(tl, $('.cp0'), .5, 30); rise(tl, $('.cp1'), 3.2, 30);
   pop(tl, $('.k1'), 9.6, .5); tl.to($('.k1'), {color: '#F07A5A', borderColor: '#F07A5A', duration: .2}, 9.8);
   pop(tl, $('.k2'), 11.8, .5); tl.to($('.k2'), {color: '#F07A5A', borderColor: '#F07A5A', duration: .2}, 12.0);
   draw(tl, $('.cp0 .cb'), 15.0, .8); draw(tl, $('.cp1 .cb'), 15.2, .4); pop(tl, $('.cp0 .cv'), 15.3, .6); pop(tl, $('.cp1 .cv'), 15.4, .6);
 }},

{id: 's29', clip: 'clips/s29.mp4', dur: 12.6, poster: 12.4, name: 'Thư mục + <em>lưới file</em>',
 desc: 'Gốc: "Not a developer? still useful across lots of files" (RN 6:36-6:40): 1 thư mục cam rồi lưới file icon hiện ra. Bản này: thư mục "edit whole youtube" hiện ở chữ "folder", mở ra ở "open folder", lưới file của project hiện.',
 html: () => BG + title(1330, 120, 'Chọn <em>1 folder</em> bất kỳ', 'lưu hết trên máy bạn') +
   `<div class="fd" style="left:1270px;top:300px;color:var(--plum)">${IC('folder', 120)}</div>
    <div class="fn" style="left:1030px;top:440px;width:600px;text-align:center;font:700 24px Mono">edit whole youtube video</div>` +
   ['mp4', 'json', 'py', 'jpg', 'md', 'wav', 'html', 'mp4', 'json', 'py', 'png', 'txt'].map((e, j) => `<div class="fl fl${j}" style="left:${900 + (j%6)*150}px;top:${520 + Math.floor(j/6)*170}px;width:110px;text-align:center;color:var(--ink-muted)">${IC('file', 64)}<div style="position:static;font:600 17px Mono;margin-top:6px">.${e}</div></div>`).join(''),
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.L, .3); rise(tl, $('.ttl'), .6);
   pop(tl, $('.fd'), 5.6, .4); rise(tl, $('.fn'), 5.8, 10);
   hop(tl, $('.fd'), 9.6, 20); $$('.fl').forEach((e, j) => rise(tl, e, 9.9 + j*.06, 20));
   [1, 4, 7].forEach((j, k) => tl.to($('.fl' + j), {color: '#4A3AE0', duration: .2}, 11.2 + k*.15));
 }},

{id: 's30', clip: 'clips/s30.mp4', dur: 11.0, poster: 10.6, name: 'Thẻ có <em>đồng hồ</em> + thanh',
 desc: 'Gốc: Prompt cache (RN 7:12-7:36): cột đoạn chat bên trái, thẻ giữa có vòng đồng hồ "~1 hour", thanh Usage chạy. Bản này: cột đoạn video được xem từng cái (làm tay), đồng hồ đếm, rồi AI điền timestamp 1 phát.',
 html: () => BG + title(610, 120, 'Timestamp làm tay <em>rất lâu</em>', 'xem từng đoạn, ghi từng mốc') +
   [0, 1, 2, 3, 4, 5, 6].map(j => `<div class="sg sg${j}" style="left:${150 + (j%2)*40}px;top:${290 + j*66}px;width:${200 + (j*37 % 90)}px;height:46px;border-radius:12px;border:2px solid var(--line-strong);background:#fff"></div>`).join('') +
   `<div class="tc paper" style="left:520px;top:300px;width:420px;height:420px">
     <div style="left:34px;top:30px;display:flex;align-items:center;gap:10px;font:800 28px Disp">${IC('clock', 30)}Timestamp</div>
     ${['0:00 Intro', '1:33 Demo', '3:27 Kịch bản', '3:52 Quay', '5:03 Luật cắt cắt'].map((s, j) => `<div class="ts ts${j}" style="left:34px;top:${96 + j*44}px;font:600 22px Mono;white-space:nowrap"><span style="position:relative;color:var(--plum)">${s.split(' ')[0]}</span> ${s.split(' ').slice(1).join(' ')}</div>`).join('')}
     <div class="ck2" style="right:30px;top:24px;width:96px;height:96px;border-radius:50%;border:4px solid var(--line-strong)"><i class="hand" style="left:44px;top:12px;width:4px;height:36px;background:var(--ink);border-radius:2px;transform-origin:50% 100%"></i></div>
     <div style="left:34px;right:34px;top:340px;height:16px;border-radius:8px;background:var(--ivory-deep)"><i class="ub" style="left:0;top:0;bottom:0;width:100%;border-radius:8px;background:#F07A5A;transform-origin:0 50%"></i></div>
     <div class="ul" style="left:34px;top:366px;font:600 17px Body;color:var(--ink-muted)">làm tay ~30 phút</div></div>
    <div class="ai" style="left:960px;top:330px;color:var(--plum)">${IC('sparkles', 56)}</div>`,
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.R, .3); rise(tl, $('.ttl'), .6); $$('.sg').forEach((e, j) => rise(tl, e, .7 + j*.05, 14)); rise(tl, $('.tc'), 1.0, 30);
   tl.set($$('.ts'), {opacity: 0}, 0); tl.fromTo($('.hand'), {rotation: 0}, {rotation: 360*2, duration: 5, ease: 'none'}, 2.0);
   draw(tl, $('.ub'), 2.0, 5); $$('.sg').forEach((e, j) => { tl.to(e, {borderColor: '#F07A5A', backgroundColor: 'rgba(255,179,156,.3)', duration: .15}, 4.5 + j*.25); tl.to(e, {borderColor: 'rgba(23,19,13,.16)', backgroundColor: '#fff', duration: .15}, 4.75 + j*.25); });
   pop(tl, $('.ai'), 7.7, .4); $$('.ts').forEach((e, j) => tl.to(e, {opacity: 1, duration: .1}, 8.0 + j*.08));
   tl.to($('.ub'), {backgroundColor: '#3E9B6E', scaleX: .06, duration: .4}, 8.4); tl.set($('.ul'), {innerHTML: 'AI làm: vài giây'}, 8.4);
 }},

{id: 's31', clip: 'clips/s31.mp4', dur: 8.7, poster: 8.5, name: 'Icon → mũi tên → <em>đồng xu</em>',
 desc: 'Gốc: "A mod that can actually save you money" (RN 7:09): khối Cache Tax → mũi tên → chồng xu. Bản này: chỉnh da, whisper chạy trên máy → mũi tên → "0 đồng".',
 html: () => BG + title(1330, 140, 'Tool <em>miễn phí</em>', 'chạy ngay trên máy bạn') +
   TILE('t1', 900, 420, 140, IC('sparkles', 64), 'Chỉnh da') + TILE('t2', 1080, 420, 140, IC('mic', 64), 'Whisper') +
   LINE('ar', 1250, 490, 1440, 490, 'var(--line-strong)', 4) +
   `<div class="cs" style="left:1470px;top:400px;width:180px;height:200px">${[0, 1, 2, 3].map(k => `<i class="cn cn${k}" style="left:20px;top:${130 - k*30}px;width:140px;height:44px;border-radius:50%;background:#E6B45A;border:3px solid #C9962F"></i>`).join('')}</div>
    <div class="zv" style="left:1450px;top:620px;width:220px;text-align:center;font:800 40px Disp;color:var(--plum)">0 đồng</div>`,
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.L, .3); rise(tl, $('.ttl'), .6);
   pop(tl, $('.t1'), 4.0, .5); lit(tl, $('.t1'), 4.2); pop(tl, $('.t2'), 5.2, .5); lit(tl, $('.t2'), 5.4);
   draw(tl, $('.ar'), 7.2, .4); [0, 1, 2, 3].forEach(k => tl.fromTo($('.cn' + k), {y: -120, opacity: 0}, {y: 0, opacity: 1, duration: .35, ease: 'bounce.out'}, 7.6 + k*.12));
   pop(tl, $('.zv'), 8.1, .5);
 }},

{id: 's32', clip: 'clips/s32.mp4', dur: 6.5, poster: 6.2, name: 'Luồng <em>cảnh báo</em>',
 desc: 'Gốc: "Would your agent ever delete your files?" (RN 8:36-8:45): agent → icon thùng rác → thư mục, mũi tên đỏ, nhãn model. Bản này: Claude → thumbnail, dấu X đỏ ở chữ "rất là xấu".',
 html: () => BG + title(610, 160, 'Claude Code <em>chưa</em> vẽ đẹp', 'thumbnail tự tạo nhìn rất xấu') +
   `<div class="c1 paper" style="left:180px;top:420px;width:170px;height:170px;border-radius:44px;padding:38px">${LOGOS.claude}</div>
    ${LINE('a1', 360, 505, 560, 505, '#F07A5A', 4)}
    <div class="im paper" style="left:570px;top:400px;width:340px;height:210px;border-radius:20px;display:grid;place-items:center;color:var(--ink-faint)">${IC('image', 90)}</div>
    <div class="xx" style="left:830px;top:370px;width:84px;height:84px;border-radius:50%;background:#F07A5A;color:#fff;display:grid;place-items:center">${IC('x', 44)}</div>
    <div class="wl" style="left:570px;top:630px;width:340px;text-align:center;font:800 26px Disp;color:#D0573A">thumbnail xấu</div>`,
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.R, .3); rise(tl, $('.ttl'), .6); pop(tl, $('.c1'), .8, .5);
   draw(tl, $('.a1'), 1.6, .4); rise(tl, $('.im'), 1.9, 20);
   pop(tl, $('.xx'), 4.4, .3); rise(tl, $('.wl'), 4.5, 10); tl.to($('.im'), {x: -10, duration: .06, repeat: 5, yoyo: true}, 4.4);
 }},

{id: 's33', clip: 'clips/s33.mp4', dur: 11.2, poster: 10.8, name: 'Vòng lặp <em>xoay</em>',
 desc: 'Gốc: "Reflect / Like RLHF" (RN 9:09): vòng chấm và mũi tên xoay quanh 1 tâm, nhãn quanh vòng. Bản này: Quay → Ra lệnh → AI edit → Duyệt, tâm là "Luật của bạn", nút sáng ở "đổi luật", "nâng cấp", "animation".',
 html: () => { const n = [['Quay', 'video'], ['Ra lệnh', 'mic'], ['AI edit', 'wand'], ['Duyệt', 'eye']];
   return BG + title(1330, 100, 'Luật <em>tự nâng cấp</em>', 'đổi, thêm yêu cầu bất kỳ lúc nào') +
     `<div class="rg" style="left:1130px;top:310px;width:400px;height:400px;border-radius:50%;border:3px dashed var(--line-strong)"></div>
      <div class="sp" style="left:1130px;top:310px;width:400px;height:400px"><i style="left:186px;top:-14px;width:28px;height:28px;border-radius:50%;background:var(--plum)"></i></div>
      <div class="ctr" style="left:1230px;top:470px;width:200px;text-align:center;font:800 28px Disp;line-height:1.15">Luật<br><span class="em">của bạn</span></div>` +
     n.map(([l, i], j) => { const a = j*Math.PI/2 - Math.PI/2; return TILE(`nd nd${j}`, 1330 + Math.cos(a)*200 - 48, 510 + Math.sin(a)*200 - 48, 96, IC(i, 44), l); }).join(''); },
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.L, .3); rise(tl, $('.ttl'), .6);
   tl.fromTo($('.rg'), {opacity: 0, scale: .7}, {opacity: 1, scale: 1, duration: .6}, .7); rise(tl, $('.ctr'), .9, 10); $$('.nd').forEach((e, j) => pop(tl, e, 1.0 + j*.1, .4));
   tl.fromTo($('.sp'), {rotation: 0}, {rotation: 720, duration: 10, ease: 'none'}, 1.0);
   lit(tl, $('.nd1'), 1.3); lit(tl, $('.nd2'), 5.7); lit(tl, $('.nd3'), 9.4); hop(tl, $('.ctr'), 5.9, 14);
 }},

{id: 's34', clip: 'clips/s34.mp4', dur: 12.4, poster: 12.3, name: '2 cửa sổ <em>gộp làm 1</em>',
 desc: 'Gốc: "Check every change" → "Everything stays in one place" (RN 10:00-10:06): 2 cửa sổ nối vòng mắt, rồi gộp thành 1. Bản này: VS Code và Claude desktop, tới chữ "update" thì gộp hết vào Claude desktop.',
 html: () => BG + title(610, 120, 'Chuyển hẳn sang <em>desktop</em>', 'Claude Code trên app') +
   WIN('w1', 140, 330, 380, 270, `<div style="left:24px;top:70px;color:#0078D4">${IC('code', 44)}</div>${LN(24, 140, 300)}${LN(24, 170, 240)}${LN(24, 200, 280)}`, 'VS Code') +
   WIN('w2', 700, 330, 380, 270, `<div style="left:24px;top:66px;width:46px;height:46px">${LOGOS.claude}</div>${LN(24, 140, 300, 'rgba(183,168,255,.6)')}${LN(24, 170, 240)}${LN(24, 200, 280)}`, 'Claude desktop') +
   `<div class="ey" style="left:578px;top:430px;width:64px;height:64px;border-radius:50%;background:#fff;border:2px solid var(--line-strong);display:grid;place-items:center;color:var(--ink-muted)">${IC('eye', 30)}</div>
    ${LINE('lp1', 525, 410, 695, 410, 'var(--line-strong)')}${LINE('lp2', 525, 520, 695, 520, 'var(--line-strong)')}
    <div class="lb" style="left:700px;top:620px;width:380px;text-align:center;font:800 26px Disp">Claude <span class="em">Code 2.0</span></div>`,
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.R, .3); rise(tl, $('.ttl'), .5); rise(tl, $('.w1'), .6, 30); rise(tl, $('.w2'), .75, 30);
   draw(tl, $('.lp1'), 1.0, .4); draw(tl, $('.lp2'), 1.1, .4); pop(tl, $('.ey'), 1.3, .5);
   tl.to($('.w2'), {borderColor: '#4A3AE0', duration: .3}, 4.9); hop(tl, $('.w2'), 5.0, 16); rise(tl, $('.lb'), 10.3, 10);
   tl.to([$('.lp1'), $('.lp2'), $('.ey')], {opacity: 0, duration: .3}, 12.0); tl.to($('.w1'), {left: 700, opacity: 0, scale: .8, duration: .5, ease: 'power3.in'}, 12.0);
   tl.to($('.w2'), {left: 420, duration: .5, ease: 'power3.inOut'}, 12.0); tl.to($('.lb'), {left: 420, duration: .5, ease: 'power3.inOut'}, 12.0);
 }},

{id: 's35', clip: 'clips/s35.mp4', dur: 10.6, poster: 10.4, name: 'Hàng <em>4 bước</em>',
 desc: 'Gốc: "Really easy" (RN 10:51): 4 icon tròn Update, Describe, Tweak, Install, cái đầu sáng. Bản này: Tải Claude, Copy GitHub, Setup, Dán video, sáng lần lượt khi bạn nói "quy trình", tick hết ở "từng bước".',
 html: () => BG + title(1330, 150, 'Làm <em>từng bước</em>', 'không giấu bước nào') +
   [['download', 'Tải Claude'], ['link', 'Copy GitHub'], ['wand', 'Setup'], ['video', 'Dán video']].map(([i, n], j) => `<div class="sx sx${j}" style="left:${860 + j*250}px;top:420px;width:150px;text-align:center">
     <div class="tb" style="position:relative;width:130px;height:130px;margin:0 auto;border-radius:50%;border:3px solid var(--line-strong);background:#fff;display:grid;place-items:center;color:var(--ink-muted)">${IC(i, 54)}</div>
     <div style="position:static;margin-top:14px;font:800 24px Disp;white-space:nowrap">${n}</div>
     <div class="badge sk" style="right:-6px;top:-10px;width:42px;height:42px;background:#3E9B6E;opacity:0">${IC('check', 22)}</div></div>` + (j < 3 ? LINE(`sl sl${j}`, 1010 + j*250, 485, 1100 + j*250, 485, 'var(--line-strong)') : '')).join(''),
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.L, .3); rise(tl, $('.ttl'), .6);
   $$('.sx').forEach((e, j) => rise(tl, e, 2.0 + j*.3, 30)); $$('.sl').forEach((e, j) => draw(tl, e, 2.2 + j*.3, .25));
   lit(tl, $('.sx0'), 4.9); $$('.sk').forEach((e, j) => pop(tl, e, 7.7 + j*.18, .3));
 }},

{id: 's36', clip: 'clips/s36.mp4', dur: 10.7, poster: 10.4, name: 'Thanh trượt <em>mốc gói</em>',
 desc: 'Gốc: "Mods need 2.1.287 or newer" (RN 10:54): trục số có mốc, núm trượt tới phiên bản cần. Bản này: trục Free / Pro / Max, núm trượt qua Pro ở chữ "Pro" rồi tới Max, Free bị đánh dấu không dùng được.',
 html: () => BG + title(610, 160, 'Cần gói <em>trả phí</em>', 'Claude Pro hoặc Max') +
   `<div class="ax" style="left:160px;top:520px;width:880px;height:6px;border-radius:3px;background:var(--line-strong)"></div>
    <div class="ok2" style="left:600px;top:520px;width:440px;height:6px;border-radius:3px;background:var(--plum);transform-origin:0 50%"></div>` +
   [['Free', 160], ['Pro', 600], ['Max', 1040]].map(([n, x], j) => `<i class="tk tk${j}" style="left:${x - 3}px;top:500px;width:6px;height:46px;border-radius:3px;background:var(--ink-faint)"></i><div class="tn tn${j}" style="left:${x - 80}px;top:570px;width:160px;text-align:center;font:800 32px Disp">${n}</div>`).join('') +
   `<div class="kb" style="left:136px;top:499px;width:48px;height:48px;border-radius:50%;background:#fff;border:4px solid var(--plum);box-shadow:0 4px 12px rgba(74,58,224,.35)"></div>
    <div class="nx" style="left:120px;top:400px;padding:8px 16px;border-radius:999px;background:rgba(255,179,156,.4);color:#D0573A;font:700 20px Body;white-space:nowrap;opacity:0">không chạy được</div>`,
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.R, .3); rise(tl, $('.ttl'), .6); tl.fromTo($('.ax'), {scaleX: 0}, {scaleX: 1, duration: .6, transformOrigin: '0 50%'}, 4.4); tl.set($('.ok2'), {scaleX: 0}, 0);
   $$('.tn').forEach((e, j) => rise(tl, e, 4.6 + j*.1, 10)); pop(tl, $('.kb'), 4.9, .5); pop(tl, $('.nx'), 7.0, .6);
   tl.to($('.kb'), {left: 576, duration: .5, ease: 'power3.inOut'}, 8.6); tl.to($('.tn1'), {color: '#4A3AE0', duration: .2}, 8.8);
   tl.to($('.kb'), {left: 1016, duration: .5, ease: 'power3.inOut'}, 9.5); tl.to($('.tn2'), {color: '#4A3AE0', duration: .2}, 9.8); draw(tl, $('.ok2'), 8.7, 1.2);
 }},
);
