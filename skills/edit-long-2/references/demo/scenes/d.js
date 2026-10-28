// Scenes s37-s48: terminal card, hot-reload toggle, typed edit + doc update, Claude UI cards (buttons, agents panel, focus box,
// style picker, diff replay, file tree, choice card, delete confirm).
SCENES.push(
{id: 's37', clip: 'clips/s37.mp4', dur: 11.4, poster: 11.2, name: 'Terminal <em>gõ lệnh</em>',
 desc: 'Gốc: "In the terminal: claude update" (RN 10:57): thẻ terminal nhỏ, lệnh gõ dần, dòng kết quả xanh. Bản này: cài YouTube API ở chữ "YouTube API", đăng nhập Codex ở chữ "Codex".',
 html: () => BG + title(1330, 150, 'Thêm <em>YouTube API</em> + Codex', 'để đăng bài và làm thumbnail') +
   `<div class="tm" style="left:860px;top:340px;width:940px;height:400px;border-radius:22px;background:#1F1B16;box-shadow:var(--shadow);overflow:hidden;font:22px Mono;color:#F3ECE0">
     <div style="left:0;right:0;top:0;height:44px;background:#2A251F;display:flex;align-items:center;gap:8px;padding:0 18px">${DOTS}<span style="position:static;margin-left:12px;font:15px Body;color:#8A8073">Terminal</span></div>
     <div style="left:30px;top:80px;white-space:nowrap"><span style="position:static;color:#B7A8FF">$</span> ${chars('pip install google-api-python-client', 'k1')}</div>
     <div class="r1" style="left:30px;top:124px;color:#A9E0C2">✓ YouTube Data API v3 sẵn sàng</div>
     <div style="left:30px;top:200px;white-space:nowrap"><span style="position:static;color:#B7A8FF">$</span> ${chars('codex login', 'k2')}</div>
     <div class="r2" style="left:30px;top:244px;color:#A9E0C2">✓ Logged in with ChatGPT</div>
     <div class="r3" style="left:30px;top:288px;color:#8A8073">image_gen: available</div></div>`,
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.L, .3); rise(tl, $('.ttl'), .6); rise(tl, $('.tm'), .8, 30);
   type(tl, '.k1', 2.6, 3.8); tl.set($$('.r1, .r2, .r3'), {opacity: 0}, 0); tl.to($('.r1'), {opacity: 1, duration: .15}, 4.1);
   type(tl, '.k2', 6.0, 6.8); tl.to($('.r2'), {opacity: 1, duration: .15}, 7.6); tl.to($('.r3'), {opacity: 1, duration: .15}, 9.2);
 }},

{id: 's38', clip: 'clips/s38.mp4', dur: 12.7, poster: 12.4, name: 'Công tắc <em>tải lại</em>',
 desc: 'Gốc: "Hot reloading" (RN 11:18-11:24): khung UI, icon vòng xoay cam, công tắc gạt bật. Bản này: chip ov-3, ov-4, ov-5 hiện đúng lúc bạn đọc số, icon xoay khi "prompt vô", công tắc "Tự cập nhật ảnh mẫu" bật.',
 html: () => BG + title(610, 130, 'Sửa bằng <em>1 câu prompt</em>', 'ảnh mẫu tự cập nhật') +
   WIN('rw', 150, 290, 640, 440, `${['ov-003', 'ov-004', 'ov-005'].map((n, j) => `<div class="oc oc${j}" style="left:${30 + j*200}px;top:80px;width:180px;height:120px;border-radius:14px;border:2px solid var(--line-strong);background:var(--ivory-deep)"><div style="left:14px;top:84px;font:700 17px Mono">${n}</div></div>`).join('')}
     ${LN(30, 240, 560)}${LN(30, 272, 420)}<div class="rf" style="left:270px;top:310px;color:var(--plum)">${IC('refresh', 90)}</div>`, 'review/index.html') +
   `<div class="tg paper" style="left:820px;top:430px;width:300px;height:170px;border-radius:24px"><div style="left:28px;top:26px;font:800 24px Disp;width:250px">Tự cập nhật</div>
     <div class="tr" style="left:28px;top:84px;width:110px;height:58px;border-radius:29px;background:var(--ink-faint)"><div class="kn" style="left:6px;top:6px;width:46px;height:46px;border-radius:50%;background:#fff"></div></div></div>`,
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.R, .3); rise(tl, $('.ttl'), .6); rise(tl, $('.rw'), .8, 40); rise(tl, $('.tg'), 1.0, 30);
   [4.4, 5.4, 6.2].forEach((t, j) => { tl.to($('.oc' + j), {borderColor: '#4A3AE0', backgroundColor: 'rgba(183,168,255,.3)', duration: .2}, t); hop(tl, $('.oc' + j), t, 14); });
   tl.set($('.rf'), {opacity: 0}, 0); tl.to($('.rf'), {opacity: 1, duration: .2}, 9.4); tl.fromTo($('.rf'), {rotation: 0}, {rotation: 540, duration: 2, ease: 'power2.inOut'}, 9.4);
   tl.to($('.tr'), {backgroundColor: '#4A3AE0', duration: .2}, 9.6); tl.to($('.kn'), {x: 52, duration: .3, ease: 'back.out(1.6)'}, 9.6);
 }},

{id: 's39', clip: 'clips/s39.mp4', dur: 11.2, poster: 10.9, name: 'Gõ yêu cầu → <em>tài liệu đổi</em>',
 desc: 'Gốc: "Save it as a plugin" (RN 11:39-11:42): ô nhập gõ lệnh, 2 khung "this session / next session", tick xanh khi lưu. Bản này: gõ "gắn link Topview bên dưới description", khung description có dòng mới, tick "Đã cập nhật YouTube".',
 html: () => BG + title(1330, 110, 'Sửa description <em>bằng lời</em>', 'nó tự gắn lên YouTube') +
   `<div class="ip paper" style="left:860px;top:280px;width:940px;height:84px;border-radius:20px"><div style="left:26px;top:26px;font-size:24px;white-space:nowrap">${chars('gắn link Topview bên dưới description', 'k')}</div></div>` +
   WIN('ds', 860, 400, 940, 420, `${LN(30, 80, 520)}${LN(30, 112, 600)}${LN(30, 144, 440)}${LN(30, 186, 380)}${LN(30, 218, 470)}
     <div class="nl" style="left:20px;top:260px;right:20px;height:56px;border-radius:12px;background:rgba(183,168,255,.3);display:flex;align-items:center;gap:12px;padding:0 14px;font:600 22px Body">${IC('link', 26)}Topview: topview.ai/plugin</div>
     <div class="dn" style="left:30px;top:342px;display:flex;align-items:center;gap:10px;font:700 20px Body;color:#3E9B6E"><span class="badge" style="position:static;width:32px;height:32px;background:#3E9B6E">${IC('check', 18)}</span>Đã cập nhật YouTube</div>`, 'Description'),
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.L, .3); rise(tl, $('.ttl'), .5); rise(tl, $('.ip'), .7, 20); rise(tl, $('.ds'), .9, 30);
   type(tl, '.k', 1.6, 3.6); tl.to($('.ip'), {borderColor: '#4A3AE0', duration: .2}, 1.6);
   tl.fromTo($('.nl'), {opacity: 0, scaleY: 0}, {opacity: 1, scaleY: 1, duration: .35, ease: 'back.out(1.6)'}, 4.4);
   tl.set($('.dn'), {opacity: 0}, 0); pop(tl, $('.dn'), 7.8, .7);
 }},

{id: 's41', clip: 'clips/s41.mp4', dur: 11.3, poster: 11.0, name: 'Thẻ chat có <em>nút bấm</em>',
 desc: 'Gốc: thẻ "You should know" ngay trong khung chat (RN 4:57-5:06), có nút Tell me more / I knew this / Dismiss, con trỏ bấm. Bản này: Claude báo ảnh mẫu xong, con trỏ bấm "Sửa", gõ "ov-003: đổi ảnh", rồi hiện thumbnail.',
 html: () => BG + CLAUDE(CLAUDEMSG('m1', 40, `Xong <b>71 ảnh mẫu</b> B-roll. Mở <span style="position:relative;color:var(--plum)">review/index.html</span> để duyệt.`) +
   `<div class="cd" style="left:96px;top:110px;width:640px;padding:20px 22px;border-radius:18px;border:2px solid var(--line-strong);background:var(--ivory)">
     <div style="position:static;font:700 13px Body;letter-spacing:.16em;color:var(--plum)">CHỜ BẠN DUYỆT</div>
     <div style="position:static;font-size:19px;margin-top:6px">71 overlay, 11 chương. Gõ mã <b>ov-NNN</b> để sửa từng cái.</div>
     <div style="position:static;display:flex;gap:10px;margin-top:14px"><span class="b1" style="position:relative;padding:8px 16px;border-radius:10px;background:var(--plum);color:#fff;font:700 16px Body">Duyệt</span><span class="b2" style="position:relative;padding:8px 16px;border-radius:10px;border:1px solid var(--line-strong);background:#fff;font:700 16px Body">Sửa</span><span style="position:relative;padding:8px 16px;font:600 16px Body;color:var(--ink-muted)">Để sau</span></div></div>
   <div class="m2" style="left:96px;top:330px;display:flex;gap:12px;align-items:center;font-size:18px">${IC('image', 22)} Đang tạo 3 thumbnail…<img src="img/rea-t1.jpg" style="position:relative;width:160px;height:90px;border-radius:10px;object-fit:cover"></div>` +
   INPUT('in', 560, `<div style="left:22px;top:20px;font-size:20px;white-space:nowrap">${chars('ov-003: đổi ảnh trước/sau rộng hơn', 'k')}</div>`)) + CUR('cu', 1300, 900),
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.BL, .3); rise(tl, $('.cw'), .4, 30); rise(tl, $('.m1'), .7, 10); rise(tl, $('.cd'), 1.0, 14);
   tl.fromTo($('.cu'), {opacity: 0}, {opacity: 1, duration: .2}, 2.5); glide(tl, $('.cu'), 2.6, 760, 405, .7); click(tl, $('.b2'), 3.4); tl.to($('.b2'), {borderColor: '#4A3AE0', color: '#4A3AE0', duration: .2}, 3.4);
   type(tl, '.k', 4.0, 5.6); tl.to($('.in'), {borderColor: '#4A3AE0', duration: .2}, 4.0); tl.to($('.in .snd'), {backgroundColor: '#4A3AE0', duration: .2}, 4.0);
   glide(tl, $('.cu'), 5.7, 1715, 950, .5); click(tl, $('.in .snd'), 6.2); tl.set($('.m2'), {opacity: 0}, 0); rise(tl, $('.m2'), 8.6, 10);
 }},

{id: 's42', clip: 'clips/s42.mp4', dur: 11.7, poster: 11.5, name: 'Bảng agent <em>chạy tiến độ</em>',
 desc: 'Gốc: "Launch kit" (RN 0:12-0:17, 2:33-2:57): panel Agents bên phải, mỗi agent 1 dòng có mascot, chi phí, thanh tiến độ chạy song song. Bản này: Cắt vấp, B-roll, Thumbnail, Description chạy đúng lúc bạn kể.',
 html: () => BG + CLAUDE(CLAUDEMSG('m1', 30, `Dùng skill <b>youtube</b>. Chạy 4 việc song song.`) +
   `<div class="pn" style="left:520px;top:20px;width:520px;height:640px;border-radius:18px;border:1px solid var(--line);background:var(--ivory)">
     <div style="left:22px;top:18px;font:800 22px Disp">Agents</div><div class="sub" style="left:22px;top:52px;font-size:15px">4 đang chạy</div>
     ${[['Cắt vấp', '#FFB39C'], ['B-roll', '#9AD0FF'], ['Thumbnail', '#E6B45A'], ['Description', '#A9E0C2']].map(([n, h], j) => `<div class="ag ag${j}" style="left:16px;right:16px;top:${96 + j*130}px;height:112px;border-radius:14px;background:#fff;border:1px solid var(--line)">
       ${MASC('mm', 16, 20, 5, '#4A3AE0', h)}<div style="left:96px;top:20px;font:700 20px Body">${n}</div>
       <div class="st" style="left:96px;top:50px;font:600 14px Mono;color:var(--ink-muted)">đang chạy…</div>
       <div style="left:96px;right:20px;top:80px;height:10px;border-radius:5px;background:var(--ivory-deep)"><i class="pg" style="left:0;top:0;bottom:0;width:100%;border-radius:5px;background:var(--plum);transform-origin:0 50%"></i></div></div>`).join('')}</div>`),
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.BL, .3); rise(tl, $('.cw'), .4, 30); rise(tl, $('.m1'), .9, 10); rise(tl, $('.pn'), 1.2, 20);
   tl.set($$('.ag'), {opacity: 0}, 0); tl.set($$('.pg'), {scaleX: 0}, 0);
   [4.1, 6.9, 8.0, 9.2].forEach((t, j) => { rise(tl, $('.ag' + j), t, 14); tl.to($('.ag' + j + ' .pg'), {scaleX: 1, duration: 3.5 - j*.5, ease: 'power1.inOut'}, t + .2);
     tl.set($('.ag' + j + ' .st'), {innerHTML: 'xong', color: '#3E9B6E'}, t + 3.7 - j*.5); });
 }},

{id: 's43', clip: 'clips/s43.mp4', dur: 11.3, poster: 11.0, name: 'Khung <em>soi 1 dòng</em>, mờ phần còn lại',
 desc: 'Gốc: khung viền cam khoanh đúng dòng đang nói, phần còn lại mờ đi (RN 2:18, 9:24). Bản này: file utterances.txt thật của video này, khoanh dòng [LỆNH CẮT] ở chữ "cắt cắt", rồi khoanh dòng vấp phía trên ở chữ "nói vấp".',
 html: () => { const L = [['U034', 'ha thì sau khi mà mình áp dụng cái hệ thống YouTube AI này vô…'], ['U035', 'Ở trên cái kênh khoảng 1 .000 view'], ['U036', '[LỆNH CẮT] Cắt cắt'],
     ['U037', 'Ở trên cái kênh khoảng 1 .000 subscriber Có nghĩa là nó'], ['U038', 'có cái tỷ lệ là'], ['U039', '10x so với lại'], ['U040', '[LỆNH CẮT] Cắt cắt'], ['U041', 'Có nghĩa là nó có cái tỷ lệ views trên subscriber là gần như là 10x luôn']];
   return BG + CLAUDE(`<div class="cv" style="left:30px;top:24px;right:30px;bottom:24px;border-radius:16px;background:#fff;border:1px solid var(--line);overflow:hidden">
     <div style="left:0;right:0;top:0;height:44px;background:var(--ivory);border-bottom:1px solid var(--line);font:600 15px Mono;color:var(--ink-muted);padding:12px 18px">cut/work/utterances.txt</div>
     ${L.map(([u, t], j) => `<div class="ul ul${j}" style="left:18px;right:18px;top:${62 + j*70}px;height:58px;display:flex;align-items:center;gap:18px;font:17px Mono;white-space:nowrap;overflow:hidden"><span style="position:relative;color:var(--ink-faint)">${u}</span><span style="position:relative;${t.startsWith('[') ? 'color:#D0573A;font-weight:700' : ''}">${t}</span></div>`).join('')}</div>
     <div class="fx" style="left:38px;top:220px;width:994px;height:62px;border-radius:12px;border:3px solid var(--plum);box-shadow:0 0 0 6px rgba(123,108,255,.15);opacity:0"></div>`, 'utterances.txt'); },
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.BL, .3); rise(tl, $('.cw'), .4, 30);
   const box = (j, t) => { tl.to($('.fx'), {opacity: 1, top: 82 + j*70, duration: .4, ease: 'power3.inOut'}, t);
     $$('.ul').forEach((e, k) => tl.to(e, {opacity: k == j ? 1 : .25, filter: k == j ? 'blur(0px)' : 'blur(1.5px)', duration: .3}, t)); };
   box(2, 3.1); box(1, 9.6);
 }},

{id: 's44', clip: 'clips/s44.mp4', dur: 11.3, poster: 10.9, name: 'Lưới mẫu, <em>khung chọn chạy</em>',
 desc: 'Gốc: "Claude Skins" (RN 4:15-4:24): lưới thẻ giao diện, khung chọn viền màu nhảy từ thẻ này sang thẻ khác. Bản này: khung hình thật của các video đã edit, khung chọn chạy theo chữ animation, B-roll, thumbnail, 3D, website.',
 html: () => { const C = [['cap-60.jpg', 'Animation'], ['cap-36.jpg', 'B-roll'], ['rea-600.jpg', 'Thumbnail'], ['rea-330.jpg', '3D'], ['rea-408.jpg', 'Website'], ['rea-12.jpg', 'CRM 3D']];
   return BG + title(1330, 110, 'Đủ kiểu <em>B-roll</em>', 'cùng 1 skill làm hết') +
     C.map(([im, n], j) => `<div class="sk sk${j}" style="left:${860 + (j%3)*325}px;top:${280 + Math.floor(j/3)*265}px;width:300px;height:230px;border-radius:18px;background:#fff;border:1px solid var(--line);box-shadow:var(--shadow);overflow:hidden">
       <img src="img/${im}" style="left:10px;top:10px;width:280px;height:158px;border-radius:10px;object-fit:cover"><div style="left:16px;top:182px;font:800 22px Disp">${n}</div></div>`).join('') +
     `<div class="sel" style="left:852px;top:272px;width:316px;height:246px;border-radius:24px;border:4px solid var(--plum);box-shadow:0 0 0 8px rgba(123,108,255,.15);opacity:0"></div>`; },
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.L, .3); rise(tl, $('.ttl'), .5); $$('.sk').forEach((e, j) => rise(tl, e, .4 + j*.06, 30));
   [[0, .5], [1, 1.4], [2, 2.8], [3, 5.7], [4, 7.5], [5, 9.2]].forEach(([j, t], k) => tl.to($('.sel'), {opacity: 1, left: 852 + (j%3)*325, top: 272 + Math.floor(j/3)*265, duration: k ? .35 : .2, ease: 'power3.inOut'}, t));
 }},

{id: 's45', clip: 'clips/s45.mp4', dur: 11.2, poster: 10.9, name: 'Diff + nút <em>Replay</em>',
 desc: 'Gốc: "Replay Theater" (RN 10:15-10:45): diff code đỏ/xanh, nút "Replay edits" được bấm, chuyển qua edit kế. Bản này: diff thật của edit-plan.json (ov-013 đổi từ th-page sang th-side, ảnh mới), bấm Replay ở chữ "chính xác".',
 html: () => BG + CLAUDE(`<div class="df" style="left:30px;top:24px;right:30px;height:470px;border-radius:16px;background:#fff;border:1px solid var(--line);overflow:hidden;font:17px Mono">
     <div style="left:0;right:0;top:0;height:44px;background:var(--ivory);border-bottom:1px solid var(--line);padding:12px 18px;font:600 15px Mono;color:var(--ink-muted)">work/make_plan.py · 2 dòng đổi</div>
     ${[['  ', "add('chapter', at('Rồi thì bây giờ mình sẽ demo')…", ''], ['- ', "add('th-page', …, {'img': WEB('web-04-rea-desc-crop.png'),", 'del'], ['- ', "     'text': '*11.088* lượt xem'},", 'del'],
        ['+ ', "add('th-side', …, {'img': WEB('web-06-rea-views.png'),", 'add'], ['+ ', "     'badge': 'YouTube', 'text': '*11.088* lượt xem', 'side': 'right'},", 'add'], ['  ', "add('sl-publish', at('description ở đây'), 6.0, …", '']].map(([p, t, k], j) =>
       `<div class="dl dl${j} ${k}" style="left:0;right:0;top:${60 + j*58}px;height:50px;padding:14px 20px;white-space:nowrap;overflow:hidden;background:${k == 'del' ? 'rgba(255,179,156,.28)' : k == 'add' ? 'rgba(169,224,194,.35)' : 'transparent'}"><span style="position:relative;color:${k == 'del' ? '#D0573A' : k == 'add' ? '#2F7D57' : 'var(--ink-faint)'}">${p}</span>${t.replace(/</g, '&lt;')}</div>`).join('')}</div>
   <div class="rb" style="left:30px;top:520px;display:flex;align-items:center;gap:14px"><span class="rp" style="position:relative;padding:10px 18px;border-radius:12px;border:2px solid var(--plum);color:var(--plum);font:700 17px Body">▶ Replay</span><span style="position:relative;padding:10px 18px;border-radius:12px;background:var(--ink);color:#fff;font:700 17px Body">Edit kế</span><span class="sub" style="position:relative;font-size:15px">edit 1 / 3</span></div>`, 'Replay edits') + CUR('cu', 900, 980),
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.BL, .3); rise(tl, $('.cw'), .4, 30);
   tl.set($$('.dl'), {opacity: 0}, 0); [0, 1, 2].forEach(j => tl.to($('.dl' + j), {opacity: 1, duration: .2}, 1.0 + j*.1));
   [3, 4, 5].forEach(j => tl.fromTo($('.dl' + j), {opacity: 0, x: -20}, {opacity: 1, x: 0, duration: .3}, 5.1 + (j - 3)*.25));
   tl.to($$('.del'), {opacity: .45, duration: .3}, 5.1);
   tl.fromTo($('.cu'), {opacity: 0}, {opacity: 1, duration: .2}, 7.6); glide(tl, $('.cu'), 7.7, 555, 815, .7); click(tl, $('.rp'), 8.6);
   tl.to($('.rp'), {backgroundColor: '#4A3AE0', color: '#fff', duration: .2}, 8.6);
   [3, 4].forEach(j => tl.fromTo($('.dl' + j), {backgroundColor: 'rgba(169,224,194,.9)'}, {backgroundColor: 'rgba(169,224,194,.35)', duration: .8}, 8.8 + (j - 3)*.2));
 }},

{id: 's46', clip: 'clips/s46.mp4', dur: 8.8, poster: 8.5, name: 'Cây thư mục <em>sáng file</em>',
 desc: 'Gốc: "Filetree" (RN 6:06-6:57): cây file bên phải, file Claude đụng tới sáng tím kèm nhãn Opened / Edited, thư mục mở ra. Bản này: thư mục Meetings thật, 2 file bạn quay sáng lên, menu "Copy as path" bật ở chữ "copy as path".',
 html: () => { const F = ['2026-10-28 09-36-52.mp4', 'upwork 28 10.mp4', 'Youtube AI system.mp4', 'youtube ai phan 1.mp4', 'youtube ai phan 2.mp4', 'video portfolio.mp4'];
   return BG + title(1330, 120, 'Chọn <em>2 file</em> vừa quay', 'chuột phải, Copy as path') +
     `<div class="ft paper" style="left:900px;top:280px;width:840px;height:560px;border-radius:22px">
       <div style="left:26px;top:22px;display:flex;align-items:center;gap:10px;font:700 20px Body">${IC('folder', 26)} Recordings › Meetings</div>
       ${F.map((n, j) => `<div class="fr fr${j}" style="left:16px;right:16px;top:${80 + j*72}px;height:60px;border-radius:12px;display:flex;align-items:center;gap:14px;padding:0 16px;font:600 20px Body">${IC('video', 24)}${n}<span class="tg" style="position:relative;margin-left:auto;font:700 13px Body;color:#fff;background:var(--plum);padding:4px 10px;border-radius:999px;opacity:0">chọn</span></div>`).join('')}
       <div class="mn" style="left:520px;top:300px;width:260px;padding:10px;border-radius:14px;background:#fff;border:1px solid var(--line-strong);box-shadow:var(--shadow);opacity:0">
         ${['Mở', 'Copy as path', 'Đổi tên'].map((m, j) => `<div class="mi mi${j}" style="position:relative;padding:10px 14px;border-radius:8px;font:600 18px Body">${m}</div>`).join('')}</div></div>` + CUR('cu', 1500, 700); },
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.L, .3); rise(tl, $('.ttl'), .5); rise(tl, $('.ft'), .7, 30);
   [2, 3].forEach((j, k) => { tl.to($('.fr' + j), {backgroundColor: 'rgba(183,168,255,.3)', duration: .2}, 1.0 + k*.4); tl.to($('.fr' + j + ' .tg'), {opacity: 1, duration: .2}, 1.0 + k*.4); });
   tl.fromTo($('.cu'), {opacity: 0}, {opacity: 1, duration: .2}, 5.0); glide(tl, $('.cu'), 5.1, 1300, 625, .6);
   tl.fromTo($('.mn'), {opacity: 0, scale: .9}, {opacity: 1, scale: 1, duration: .2}, 5.9); glide(tl, $('.cu'), 6.2, 1500, 650, .4);
   tl.to($('.mi1'), {backgroundColor: '#4A3AE0', color: '#fff', duration: .15}, 6.4); click(tl, $('.cu'), 7.2); tl.to($('.mn'), {opacity: 0, duration: .2}, 7.5);
 }},

{id: 's47', clip: 'clips/s47.mp4', dur: 10.9, poster: 10.7, name: 'Thẻ <em>2 lựa chọn</em> + bấm',
 desc: 'Gốc: Cache Tax hold (RN 7:42-7:57): thẻ trong chat chặn lại, 2 ô lựa chọn kèm giá, nút "Pay and send" được bấm. Bản này: bản cắt 15:37 xong, 2 ô "Render ngay" và "Sửa tiếp", con trỏ bấm Render ở chữ "render ra đi".',
 html: () => BG + CLAUDE(CLAUDEMSG('m1', 30, `Bản cắt xong: <b>23:53 → 15:37</b>, bỏ 105 đoạn vấp.`) +
   `<div class="cd" style="left:96px;top:96px;width:820px;padding:22px;border-radius:18px;border:2px solid var(--line-strong);background:var(--ivory)">
     <div style="position:static;display:flex;align-items:center;gap:10px;font:700 13px Body;letter-spacing:.16em;color:var(--plum)">${IC('hourglass', 18)} ĐANG CHỜ BẠN</div>
     <div style="position:static;display:flex;gap:16px;margin-top:16px">
      <div class="o1" style="position:relative;flex:1;padding:18px;border-radius:14px;border:2px solid var(--line-strong);background:#fff"><div style="position:static;font:800 22px Disp">Render ngay</div><div class="sub" style="position:static;font-size:15px">ghép B-roll, xuất final</div></div>
      <div class="o2" style="position:relative;flex:1;padding:18px;border-radius:14px;border:2px solid var(--line-strong);background:#fff"><div style="position:static;font:800 22px Disp">Sửa tiếp</div><div class="sub" style="position:static;font-size:15px">gõ mã ov-NNN</div></div></div>
     <div style="position:static;display:flex;gap:10px;margin-top:16px"><span class="go" style="position:relative;padding:10px 18px;border-radius:10px;background:var(--plum);color:#fff;font:700 16px Body">Render</span><span style="position:relative;padding:10px 18px;border-radius:10px;border:1px solid var(--line-strong);background:#fff;font:700 16px Body">Xem lại bản cắt</span></div></div>
   <div class="m2" style="left:96px;top:420px;font-size:18px;display:flex;gap:10px;align-items:center;color:#2F7D57">${IC('check', 22)} Đang render overlay 1/71…</div>`) + CUR('cu', 1300, 950),
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.BL, .3); rise(tl, $('.cw'), .4, 30); rise(tl, $('.m1'), .8, 10); rise(tl, $('.cd'), 1.3, 16);
   tl.to($('.o2'), {borderColor: '#E6B45A', duration: .2}, 4.3); tl.to($('.o2'), {borderColor: 'rgba(23,19,13,.16)', duration: .2}, 7.0);
   tl.fromTo($('.cu'), {opacity: 0}, {opacity: 1, duration: .2}, 8.0); glide(tl, $('.cu'), 8.1, 860, 380, .6); tl.to($('.o1'), {borderColor: '#4A3AE0', backgroundColor: 'rgba(183,168,255,.2)', duration: .2}, 8.7);
   glide(tl, $('.cu'), 9.3, 650, 505, .5); click(tl, $('.go'), 10.2); tl.set($('.m2'), {opacity: 0}, 0); rise(tl, $('.m2'), 10.4, 8);
 }},

{id: 's48', clip: 'clips/s48.mp4', dur: 12.3, poster: 12.1, name: 'Hộp <em>xác nhận</em> có thanh dung lượng',
 desc: 'Gốc: "Blast Radius" (RN 8:24-8:33): Claude định xoá thư mục, hộp xác nhận liệt kê từng file kèm thanh dung lượng, nút "Delete 9 files" / Cancel. Bản này: "Bỏ 105 đoạn vấp", 5 đoạn dài nhất (số thật trong cut-report), bấm "Cắt" ở chữ "cắt hết".',
 html: () => BG + CLAUDE(CLAUDEMSG('m1', 30, `Đọc xong 550 câu. Định bỏ <b>105 đoạn vấp</b>:`) +
   `<div class="cd" style="left:96px;top:90px;width:820px;padding:22px;border-radius:18px;border:2px solid var(--line-strong);background:#fff">
     ${[['3:32', 'bản hỏng phần sườn kịch bản', 21.1], ['9:58', '2 lần hỏng câu "show quy trình"', 20.7], ['1:43', '3 lần hỏng "đây là 1 cái video"', 17.5], ['10:31', 'hỏng câu "app Claude"', 16.2], ['12:32', 'câu dở "Cũng trong"', 9.9]].map(([t, s, v], j) =>
       `<div class="cr cr${j}" style="position:relative;display:flex;align-items:center;gap:14px;height:52px;font-size:17px"><span style="position:relative;font:600 15px Mono;width:56px;color:var(--plum)">${t}</span><span style="position:relative;width:340px;white-space:nowrap;overflow:hidden">${s}</span>
        <span style="position:relative;flex:1;height:10px;border-radius:5px;background:var(--ivory-deep)"><i class="vb" style="left:0;top:0;bottom:0;width:${v*4.5}%;border-radius:5px;background:#F07A5A;transform-origin:0 50%"></i></span><span style="position:relative;font:600 15px Mono;width:56px;text-align:right">${v}s</span></div>`).join('')}
     <div style="position:static;display:flex;gap:10px;margin-top:14px;align-items:center"><span class="go" style="position:relative;padding:10px 18px;border-radius:10px;background:#D0573A;color:#fff;font:700 16px Body">Cắt 105 đoạn</span><span style="position:relative;padding:10px 18px;border-radius:10px;border:1px solid var(--line-strong);font:700 16px Body">Huỷ</span>
      <span style="position:relative;margin-left:auto;font:600 14px Body;color:var(--ink-muted)">đã soát 16 lệnh "cắt cắt"</span></div></div>`) + CUR('cu', 1300, 950),
 anim(tl, $) {
   move(tl, $('.face'), $('.face video'), CARD.BL, .3); rise(tl, $('.cw'), .4, 30); rise(tl, $('.m1'), 4.7, 10); rise(tl, $('.cd'), 5.0, 16);
   $$('.cr').forEach((e, j) => { rise(tl, e, 5.3 + j*.15, 8); draw(tl, e.querySelector('.vb'), 5.5 + j*.15, .5); });
   tl.fromTo($('.cu'), {opacity: 0}, {opacity: 1, duration: .2}, 9.0); glide(tl, $('.cu'), 9.1, 680, 640, .7); click(tl, $('.go'), 10.1);
   tl.to($$('.cr'), {opacity: .25, x: -10, duration: .4, stagger: .06}, 10.3);
 }},
);
