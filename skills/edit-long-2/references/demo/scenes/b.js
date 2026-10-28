// Scenes s11-s23: section title, orbit, toggle, focus cards, doc stack, venn, mascot team, event flow, tabs, node graph.
SCENES.push(
{id: 's11', clip: 'clips/s11.mp4', dur: 6, poster: 2.6, name: 'Tên phần <em>phía dưới</em> trên mặt',
 desc: 'Gốc: mỗi mod mở bằng tên phần ngay trên khung mặt full (RN 2:03, 4:00, 7:03, 8:15, 9:06, 10:09). Bản này theo ý bạn: chữ hiện bình thường ở phía dưới, không nhiễu chữ. Mở phần "Luật quay".',
 html: () => `<div class="gb" style="left:0;right:0;bottom:0;height:420px;z-index:25;background:linear-gradient(0deg,rgba(250,246,239,.94),rgba(250,246,239,.7) 50%,rgba(250,246,239,0));opacity:0"></div>
   <div class="eb" style="left:0;right:0;top:770px;z-index:26;text-align:center;font:700 22px Body;letter-spacing:.2em;color:var(--plum)">PHẦN 4</div>
   <div class="gt" style="left:0;right:0;top:800px;z-index:26;text-align:center;font:800 100px Disp;letter-spacing:-.04em;white-space:nowrap">Luật <span class="em">quay</span></div>
   <div class="gs" style="left:0;right:0;top:930px;z-index:26;text-align:center;font-size:32px;color:var(--ink-soft)">phần quan trọng nhất của cả hệ thống</div>`,
 anim(tl, $) {
   tl.to($('.gb'), {opacity: 1, duration: .35}, .3); rise(tl, $('.eb'), .35, 10); rise(tl, $('.gt'), .45, 30); rise(tl, $('.gs'), 1.1, 14);
   tl.to([$('.gt'), $('.gs'), $('.eb'), $('.gb')], {opacity: 0, y: 16, duration: .35}, 5.4);
 }},

{id: 's13', clip: 'clips/s13.mp4', dur: 7.8, poster: 7.3, name: 'Icon xoay quanh <em>mascot</em>',
 desc: 'Gốc: "Smarter and faster" (RN 0:24): mascot pixel ở giữa, vòng icon bật lần lượt quanh nó và xoay chậm. Bản này: mascot plum, icon bật đúng lúc nói "tải ảnh", "Google", "ghép", rồi mascot nhảy ở chữ "editor".',
 html: () => { const it = ['search', 'download', 'image', 'layers', 'scissors', 'film', 'type', 'sparkles'];
   return BG + title(1180, 110, 'Như 1 <em>editor</em> thật', 'tải ảnh, ghép, cắt theo yêu cầu') + MASC('ms', 1078, 506, 17) +
     `<div class="ring" style="left:1180px;top:560px;width:0;height:0">` + it.map((n, j) => { const a = j/it.length*Math.PI*2 - Math.PI/2;
       return `<div class="ob ob${j}" style="left:${Math.cos(a)*290 - 46}px;top:${Math.sin(a)*250 - 46}px;width:92px;height:92px;border-radius:26px;border:2.5px solid var(--line-strong);background:rgba(255,255,255,.8);display:grid;place-items:center;color:var(--ink-muted)">${IC(n, 40)}</div>`; }).join('') + `</div>`
     + `<div class="orbit" style="left:890px;top:310px;width:580px;height:500px;border-radius:50%;border:2px dashed var(--line-strong)"></div>`; },
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.BL, .3); rise(tl, $('.ttl'), .6); pop(tl, $('.ms'), .7, .4); tl.fromTo($('.orbit'), {opacity: 0, scale: .8}, {opacity: 1, scale: 1, duration: .6}, .8);
   [0.9, 1.7, 2.7, 3.4, 3.9, 4.5, 5.0, 5.5].forEach((t, j) => { pop(tl, $('.ob' + j), t, .3); if (j < 4) lit(tl, $('.ob' + j), t + .2); });
   tl.fromTo($('.ring'), {rotation: 0}, {rotation: 14, duration: 7, ease: 'none'}, .8);
   $$('.ob').forEach(e => tl.fromTo(e, {rotation: 0}, {rotation: -14, duration: 7, ease: 'none'}, .8));
   hop(tl, $('.ms'), 6.7, 40);
 }},

{id: 's14', clip: 'clips/s14.mp4', dur: 8, poster: 7.4, name: 'Tick → mũi tên → <em>công tắc</em>',
 desc: 'Gốc: "Already switched on" (RN 0:48): ô tick tròn, mũi tên, công tắc gạt sang cam. Bản này: "Ra lệnh" tick khi nói "ra lệnh cho AI", công tắc "Tự đăng YouTube" gạt bật ở chữ "tự động".',
 html: () => BG + title(610, 230, 'Đăng YouTube <em>tự động</em>', 'không cần kéo thả tay') +
   `<div class="ck" style="left:250px;top:470px;width:150px;height:150px;border-radius:50%;border:3px solid var(--line-strong);display:grid;place-items:center;color:var(--ink-faint);background:#fff">${IC('check', 70)}</div>
    <div class="cl" style="left:228px;top:650px;width:200px;text-align:center;font:800 26px Disp">Ra lệnh</div>
    <div class="ar" style="left:450px;top:530px;width:200px;height:30px;color:var(--ink-faint)">${IC('arrow', 30)}</div>
    ${LINE('al', 440, 545, 640, 545)}
    <div class="sw" style="left:680px;top:490px;width:220px;height:112px;border-radius:56px;background:var(--ink-faint)"><div class="kn" style="left:8px;top:8px;width:96px;height:96px;border-radius:50%;background:#fff;box-shadow:0 4px 12px rgba(0,0,0,.2);display:grid;place-items:center;color:var(--ink-faint)">${LOGOS.youtube.replace('<svg ', '<svg style="width:52px;height:52px" ')}</div></div>
    <div class="sl" style="left:690px;top:650px;width:200px;text-align:center;font:800 26px Disp">Tự đăng</div>`,
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.R, .3); rise(tl, $('.ttl'), .7);
   rise(tl, $('.ck'), 1.0, 20); rise(tl, $('.cl'), 1.1, 10); tl.to($('.ck'), {borderColor: '#4A3AE0', color: '#4A3AE0', backgroundColor: 'rgba(183,168,255,.25)', duration: .3}, 1.4);
   draw(tl, $('.al'), 2.0, .5); tl.fromTo($('.ar'), {opacity: 0}, {opacity: 0, duration: .1}, 0);
   rise(tl, $('.sw'), 4.2, 20); rise(tl, $('.sl'), 4.3, 10);
   tl.to($('.sw'), {backgroundColor: '#4A3AE0', duration: .3}, 6.2); tl.to($('.kn'), {x: 108, duration: .35, ease: 'back.out(1.6)'}, 6.2);
 }},

{id: 's15', clip: 'clips/s15.mp4', dur: 16.9, poster: 13.4, name: '3 thẻ, <em>đổi tiêu điểm</em>',
 desc: 'Gốc: Skill / MCP connector / Mod (RN 1:06-1:21): 3 khung wireframe, tiêu điểm chạy từ thẻ này sang thẻ kia, thẻ khác mờ đi, tiêu đề đổi theo. Bản này: Home (chat) → MCP → Code, khớp lúc bạn nói từng cái.',
 html: () => { const c = [['chat', 'Home', 'hỏi đáp'], ['plug', 'MCP', 'nối công cụ'], ['terminal', 'Code', 'làm việc thật']];
   return BG + `<div class="tt0">${title(1330, 140, 'Claude có <em>3 chỗ</em>', 'mình chỉ dùng tab Code')}</div><div class="tt1" style="opacity:0">${title(1330, 140, 'Home: chỉ <em>hỏi đáp</em>', 'chat, trả lời')}</div>
     <div class="tt2" style="opacity:0">${title(1330, 140, 'MCP: nối <em>vài công cụ</em>', 'kết nối cơ bản')}</div><div class="tt3" style="opacity:0">${title(1330, 140, 'Code: <em>làm thật</em>', 'cắt, edit, render, đăng')}</div>` +
     c.map(([i, n, s], j) => `<div class="fc fc${j} paper" style="left:${850 + j*330}px;top:400px;width:290px;height:320px;border-radius:28px">
       <div style="left:20px;top:18px;display:flex;gap:6px">${DOTS}</div>
       <div class="tb" style="left:85px;top:66px;width:120px;height:120px;border-radius:32px;border:2.5px solid var(--line-strong);display:grid;place-items:center;color:var(--ink-muted)">${IC(i, 56)}</div>
       <div style="left:0;right:0;top:210px;text-align:center;font:800 34px Disp">${n}</div><div class="sub" style="left:0;right:0;top:258px;text-align:center">${s}</div></div>`).join(''); },
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.L, .3); rise(tl, $('.tt0 .ttl'), .7); $$('.fc').forEach((e, j) => rise(tl, e, .9 + j*.1, 40));
   const focus = (j, t) => { $$('.fc').forEach((e, k) => { tl.to(e, {opacity: k == j ? 1 : .32, scale: k == j ? 1.05 : .97, duration: .35}, t);
       if (k == j) lit(tl, e, t); });
     [0, 1, 2, 3].forEach(k => tl.to($('.tt' + k), {opacity: k == j + 1 ? 1 : 0, duration: .25}, t)); };
   focus(0, 5.5); focus(1, 11.6); focus(2, 12.8);
   tl.to($$('.fc'), {opacity: 1, scale: 1, duration: .3}, 15.4);
 }},

{id: 's17', clip: 'clips/s17.mp4', dur: 10, poster: 9.4, name: 'Tập tài liệu + <em>mũi tên nảy</em>',
 desc: 'Gốc: "Grab it in the description" (RN 1:45, 1:54, 12:21): xấp PDF xoè ra, mũi tên chỉ xuống nảy liên tục. Bản này: xấp "Hướng dẫn cài" hiện ở chữ "đường link", mũi tên nảy ở "bên dưới phần mô tả".',
 html: () => BG + title(1330, 150, 'Hướng dẫn ở <em>mô tả</em>', 'tải về, làm theo từng bước') +
   [2, 1, 0].map(j => `<div class="dc dc${j} paper" style="left:${1180 + j*14}px;top:${360 + j*10}px;width:300px;height:390px;border-radius:14px;rotate:${(j - 1)*7}deg">
     ${j == 0 ? `<div style="left:28px;top:30px;font:800 30px Disp;line-height:1.1;width:240px">Hướng dẫn cài <span class="em">skill</span></div><div style="left:28px;top:118px;font:600 15px Body;color:var(--plum)">YOUTUBE AI EDITOR</div>${[160, 190, 220, 250, 290, 320].map((y, k) => LN(28, y, k % 3 == 2 ? 160 : 240)).join('')}` : ''}</div>`).join('') +
   `<div class="dn" style="left:1306px;top:790px;color:var(--plum)">${IC('download', 64)}</div>`,
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.L, .3); rise(tl, $('.ttl'), .7);
   rise(tl, $('.dc0'), 5.0, 60); tl.fromTo($('.dc1'), {opacity: 0, rotation: 0}, {opacity: 1, rotation: 0, duration: .5}, 5.1); tl.fromTo($('.dc2'), {opacity: 0, rotation: 0}, {opacity: 1, rotation: 14, duration: .5}, 5.15);
   tl.fromTo($('.dc0'), {rotation: 0}, {rotation: -7, duration: .5}, 5.2);
   pop(tl, $('.dn'), 8.2, .5); [8.7, 9.3].forEach(t => { tl.to($('.dn'), {y: 26, duration: .25, ease: 'power2.in'}, t); tl.to($('.dn'), {y: 0, duration: .3, ease: 'power2.out'}, t + .25); });
 }},

{id: 's19', clip: 'clips/s19.mp4', dur: 10.1, poster: 9.8, name: 'Biểu đồ <em>Venn</em>',
 desc: 'Gốc: "The right mix" (RN 2:06): 2 vòng tròn giao nhau, icon trong mỗi vòng, chỗ giao sáng lên. Bản này: "Cắt, da, B-roll, render" bên trái, "Usage Claude" bên phải, giao nhau là "0 đồng API".',
 html: () => BG + title(610, 160, 'Không tốn <em>tiền API</em>', 'chỉ dùng usage Claude Code') +
   `<div class="v1" style="left:150px;top:350px;width:440px;height:440px;border-radius:50%;border:3px solid var(--line-strong);background:rgba(183,168,255,.12)"></div>
    <div class="v2" style="left:450px;top:350px;width:440px;height:440px;border-radius:50%;border:3px solid var(--line-strong);background:rgba(154,208,255,.12)"></div>
    <div class="l1" style="left:190px;top:470px;width:230px;text-align:center;color:var(--plum)">${IC('scissors', 46)}<div style="position:static;font:800 26px Disp;color:var(--ink);margin-top:10px">Cắt, da, B-roll</div><div class="sub" style="position:static">render trên máy</div></div>
    <div class="l2" style="left:630px;top:470px;width:220px;text-align:center"><div style="position:static;width:52px;height:52px;margin:0 auto">${LOGOS.claude}</div><div style="position:static;font:800 26px Disp;margin-top:10px">Usage Claude</div><div class="sub" style="position:static">gói Pro / Max</div></div>
    <div class="mid" style="left:420px;top:540px;padding:12px 20px;border-radius:999px;background:var(--plum);color:#fff;font:800 26px Disp;white-space:nowrap">0 đồng API</div>`,
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.R, .3); rise(tl, $('.ttl'), .6);
   tl.fromTo($('.v1'), {opacity: 0, x: -80}, {opacity: 1, x: 0, duration: .6, ease: 'expo.out'}, .9); rise(tl, $('.l1'), 1.2, 16);
   tl.fromTo($('.v2'), {opacity: 0, x: 80}, {opacity: 1, x: 0, duration: .6, ease: 'expo.out'}, 7.5); rise(tl, $('.l2'), 7.8, 16);
   pop(tl, $('.mid'), 9.1, .5); tl.to([$('.v1'), $('.v2')], {borderColor: '#4A3AE0', duration: .3}, 9.1);
 }},

{id: 's20', clip: 'clips/s20.mp4', dur: 9.3, poster: 9.0, name: 'Đội <em>mascot</em> có mũ',
 desc: 'Gốc: subagents (RN 2:24-2:51): mascot pixel xuất hiện thành hàng, mỗi con 1 mũ và nhãn vai trò, nhảy lên khi được gọi. Bản này: 3 mascot Thumbnail, SEO, Timestamp, nhảy đúng chữ.',
 html: () => BG + title(1330, 150, 'Cả 1 <em>team</em> phía sau', 'mỗi việc 1 trợ lý') +
   [['Thumbnail', '#FFB39C'], ['Description SEO', '#9AD0FF'], ['Timestamp', '#E6B45A']].map(([n, h], j) =>
     MASC(`mc mc${j}`, 930 + j*300, 430, 16, '#4A3AE0', h) + `<div class="ml ml${j}" style="left:${900 + j*300}px;top:590px;width:252px;text-align:center;font:800 26px Disp">${n}</div>`).join('') +
   `<div style="left:880px;top:680px;width:900px;height:3px;background:var(--line-strong);border-radius:2px"></div>`,
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.L, .3); rise(tl, $('.ttl'), .6);
   [3.2, 4.7, 8.0].forEach((t, j) => { pop(tl, $('.mc' + j), t, .3); rise(tl, $('.ml' + j), t + .1, 10); hop(tl, $('.mc' + j), t + .5); });
   hop(tl, $('.mc0'), 8.6, 22); hop(tl, $('.mc1'), 8.7, 22);
 }},

{id: 's21', clip: 'clips/s21.mp4', dur: 10.3, poster: 9.9, name: 'Tín hiệu chạy <em>theo đường</em>',
 desc: 'Gốc: "A mod listens for events" (RN 3:06-3:15): khung Claude Code phát tín hiệu, chấm sáng chạy theo đường tới hộp mod. Bản này: khung quay video phát lệnh "Hey Claude", chấm chạy tới Claude, ra 2 việc: che mờ, chụp GitHub.',
 html: () => BG + title(1330, 120, 'Nói lệnh, <em>AI làm</em>', 'ngay trong lúc quay') +
   WIN('rec', 840, 380, 300, 230, `<div style="left:24px;top:76px;display:flex;align-items:center;gap:10px;font:700 20px Body"><i class="rd" style="position:static;width:16px;height:16px;border-radius:50%;background:#E5484D"></i>REC</div>${LN(24, 120, 240)}${LN(24, 148, 190)}${LN(24, 176, 220)}`) +
   `<div style="left:860px;top:624px;width:260px;text-align:center;font:800 24px Disp">Video đang quay</div>
    ${LINE('w1', 1150, 495, 1390, 495, 'var(--line-strong)', 3)}<div class="sig" style="left:1150px;top:478px;padding:6px 14px;border-radius:999px;background:var(--plum);color:#fff;font:700 18px Body;white-space:nowrap">Hey Claude</div>
    <div class="cb2 paper" style="left:1400px;top:420px;width:150px;height:150px;border-radius:40px;padding:34px">${LOGOS.claude}</div>
    ${LINE('w2', 1560, 470, 1660, 400, 'var(--line-strong)')}${LINE('w3', 1560, 520, 1660, 590, 'var(--line-strong)')}
    ${PILL('o1', 1670, 370, 'Che mờ', 'blur')}${PILL('o2', 1670, 560, 'Chụp GitHub', 'image')}`,
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.L, .3); rise(tl, $('.ttl'), .6); rise(tl, $('.rec'), .8, 30);
   draw(tl, $('.w1'), 1.2, .4); pop(tl, $('.cb2'), 1.5, .5);
   [0.3, 6.6].forEach(t => { tl.fromTo($('.sig'), {x: 0, opacity: 0}, {x: 0, opacity: 1, duration: .15}, t + .6); tl.to($('.sig'), {x: 140, duration: 1.0, ease: 'power1.inOut'}, t + .75); tl.to($('.sig'), {opacity: 0, duration: .15}, t + 1.7); });
   draw(tl, $('.w2'), 2.8, .3); pop(tl, $('.o1'), 5.7, .5); draw(tl, $('.w3'), 8.0, .3); pop(tl, $('.o2'), 8.3, .5);
   tl.to($('.rd'), {opacity: .2, duration: .4, repeat: 11, yoyo: true}, .8);
 }},

{id: 's22', clip: 'clips/s22.mp4', dur: 11.1, poster: 10.8, name: 'Tab <em>đổi trạng thái</em>',
 desc: 'Gốc: Watch / Change / Handle (RN 3:18-3:45): 3 tab dạng pill, tab sáng đổi theo lời, sơ đồ bên dưới đổi theo tab. Bản này: Che thông tin → Chèn ảnh → Chèn repo.',
 html: () => BG + title(610, 130, 'Lệnh <em>hay dùng</em>', 'nói lúc quay, AI tự làm') +
   ['Che thông tin', 'Chèn ảnh', 'Chèn repo'].map((n, j) => PILL(`tb tb${j}`, 150 + j*270, 300, n, ['blur', 'image', 'link'][j])).join('') +
   WIN('scr', 150, 400, 900, 470, `
     <div class="d0" style="left:40px;top:80px;right:40px;bottom:30px">${[0, 1, 2, 3, 4].map(k => `<div style="left:0;right:0;top:${k*66}px;height:52px;border-radius:12px;background:var(--ivory-deep)">${LN(20, 20, 120)}${LN(170, 20, 200, 'rgba(23,19,13,.1)', 12, 'bl')}${LN(420, 20, 160, 'rgba(23,19,13,.1)', 12, 'bl')}</div>`).join('')}
       <div class="bz" style="left:150px;top:-10px;width:460px;height:340px;border-radius:16px;backdrop-filter:blur(14px);background:rgba(183,168,255,.25);border:2px dashed var(--plum);opacity:0"></div></div>
     <div class="d1" style="left:200px;top:80px;width:500px;height:300px;opacity:0"><img src="img/rea-330.jpg" style="left:0;top:0;width:500px;height:281px;object-fit:cover;border-radius:16px;box-shadow:var(--shadow)"></div>
     <div class="d2" style="left:180px;top:70px;width:540px;height:340px;opacity:0"><img src="img/web-01-github.png" style="left:0;top:0;width:540px;height:304px;object-fit:cover;object-position:top;border-radius:16px;box-shadow:var(--shadow);border:1px solid var(--line)"></div>`, 'video đang edit'),
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.R, .3); rise(tl, $('.ttl'), .6); $$('.tb').forEach((e, j) => rise(tl, e, .8 + j*.08, 14)); rise(tl, $('.scr'), 1.0, 40);
   const tab = (j, t) => { $$('.tb').forEach((e, k) => tl.to(e, {backgroundColor: k == j ? '#4A3AE0' : '#fff', color: k == j ? '#fff' : '#17130D', borderColor: k == j ? '#4A3AE0' : 'rgba(23,19,13,.16)', duration: .25}, t));
     [0, 1, 2].forEach(k => tl.to($('.d' + k), {opacity: k == j ? 1 : 0, duration: .3}, t)); };
   tab(0, 3.5); tl.to($('.bz'), {opacity: 1, duration: .3}, 4.7); tl.to($$('.bl'), {filter: 'blur(6px)', duration: .3}, 4.7);
   tab(1, 8.7); tl.fromTo($('.d1'), {y: 40}, {y: 0, duration: .5, ease: 'expo.out'}, 8.7);
   tab(2, 10.7); tl.fromTo($('.d2'), {y: 40}, {y: 0, duration: .4, ease: 'expo.out'}, 10.7);
 }},

{id: 's23', clip: 'clips/s23.mp4', dur: 9.3, poster: 9.1, name: 'Sơ đồ <em>nút nối</em>',
 desc: 'Gốc: "It watches every helper" (RN 3:24-3:30): mascot nối dây tới từng nút, nút sáng theo lượt. Bản này: 2 việc bạn không cần làm bị gạch, Claude nối dây tới 3 project cũ ở chữ "đọc project".',
 html: () => BG + title(1330, 120, 'Chỉ cần <em>đọc project</em>', 'không quay, không gửi file') +
   PILL('n1', 880, 300, 'Gửi file video', 'video') + PILL('n2', 1240, 300, 'Tự quay lại', 'mic') +
   `<i class="s1" style="left:880px;top:325px;width:280px;height:4px;background:#F07A5A;border-radius:2px;transform-origin:0 50%"></i><i class="s2" style="left:1240px;top:325px;width:250px;height:4px;background:#F07A5A;border-radius:2px;transform-origin:0 50%"></i>
    <div class="hub paper" style="left:900px;top:520px;width:150px;height:150px;border-radius:40px;padding:34px">${LOGOS.claude}</div>` +
   ['rea-yt', 'capcut-ai-yt', 'topview-final'].map((n, j) => LINE(`lk lk${j}`, 1055, 595, 1400, 470 + j*125, 'var(--line-strong)') +
     TILE(`pj pj${j}`, 1410, 430 + j*125, 84, IC('folder', 38)) + `<div class="pn pn${j}" style="left:1510px;top:${458 + j*125}px;font:700 22px Mono">${n}</div>`).join(''),
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.L, .3); rise(tl, $('.ttl'), .6);
   rise(tl, $('.n1'), 3.5, 14); draw(tl, $('.s1'), 4.4, .3); tl.to($('.n1'), {opacity: .45, duration: .3}, 4.4);
   rise(tl, $('.n2'), 5.6, 14); draw(tl, $('.s2'), 6.2, .3); tl.to($('.n2'), {opacity: .45, duration: .3}, 6.2);
   pop(tl, $('.hub'), 7.3, .5);
   [0, 1, 2].forEach(j => { draw(tl, $('.lk' + j), 8.3 + j*.12, .3); pop(tl, $('.pj' + j), 8.45 + j*.12, .4); lit(tl, $('.pj' + j), 8.6 + j*.12); rise(tl, $('.pn' + j), 8.5 + j*.12, 8); });
 }},
);
