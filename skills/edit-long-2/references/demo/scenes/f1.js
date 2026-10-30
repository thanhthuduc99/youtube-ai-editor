// Intro B-roll scenes s61-s64 (video 8.7-27.3): workload pile-up, stumble-cut timeline, skin retouch panel, B-roll/animation tracks.
const F1 = {
  shake: (tl, el, t, a = 14) => tl.to(el, {keyframes: {x: [0, -a, a*.85, -a*.6, a*.35, 0]}, duration: .42, ease: 'none'}, t),
  // deterministic waveform bars
  wave: (w, h, seed, col = '#3E9B6E') => {
    let bars = '';
    for (let x = 3, k = 0; x < w - 3; x += 7, k++) {
      const a = Math.abs(Math.sin(k*.55 + seed)*.6 + Math.sin(k*1.7 + seed*3)*.3 + Math.sin(k*.13 + seed)*.25);
      const bh = Math.max(4, Math.min(h - 8, a*h*.9));
      bars += `<rect x="${x}" y="${(h - bh)/2}" width="4" height="${bh}" rx="2" fill="${col}"/>`;
    }
    return `<svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" style="width:${w}px;height:${h}px">${bars}</svg>`;
  },
  setCard: (tl, f, v, c) => { tl.set(f, {...c.box, filter: 'blur(0px)'}, 0); tl.set(v, c.vid, 0); },
};

SCENES.push(
{id: 's61', clip: 'clips/s61.mp4', dur: 3.7, poster: 3.2, name: 'Việc tay <em>chồng chất</em>',
 desc: 'Intro 8.7-12.4: "để viết description và đăng lên youtube". Thẻ việc rơi xuống chồng lên nhau theo lời (Description ở 9.4, Đăng YouTube ở 10.0), tổng giờ tăng dần; ở "vấn đề" thêm việc rơi vào, cả chồng rung, dấu "Hết thời gian".',
 html: () => {
   const rows = [['film', 'Edit video', '3 giờ'], ['image', 'Thumbnail', '1 giờ'], ['file', 'Description', '30 phút'], ['yt', 'Đăng YouTube', '15 phút']];
   const tot = ['0 giờ', '3 giờ', '4 giờ', '4 giờ 30', '4 giờ 45', '7 giờ+'];
   return BG + title(600, 96, '1 video, <em>4 việc tay</em>') +
     `<div class="stk" style="left:0;top:0;width:1200px;height:1080px">` +
     rows.map(([ic, n, d], j) => `<div class="rw rw${j} paper" style="left:200px;top:${290 + j*120}px;width:800px;height:100px;border-radius:24px">
       <div class="ri" style="left:20px;top:16px;width:68px;height:68px;border-radius:20px;border:2.5px solid var(--line-strong);display:grid;place-items:center;color:var(--plum);background:rgba(183,168,255,.18)">${ic == 'yt' ? `<div style="position:relative;width:40px;height:40px">${LOGOS.youtube}</div>` : IC(ic, 36)}</div>
       <div style="left:112px;top:26px;font:800 36px Disp;letter-spacing:-.02em;white-space:nowrap">${n}</div>
       <div class="rd" style="right:24px;top:28px;display:flex;align-items:center;gap:8px;padding:8px 16px;border-radius:999px;background:var(--ivory);border:1.5px solid var(--line);font:600 20px Mono;color:var(--ink-soft);white-space:nowrap">${IC('clock', 20)}${d}</div></div>`).join('') +
     `<div class="tb2 paper" style="left:200px;top:782px;width:800px;height:96px;border-radius:24px;background:var(--ivory)">
       <div class="ck" style="left:24px;top:18px;width:60px;height:60px;color:var(--ink-soft)">${IC('clock', 60)}</div>
       <div style="left:112px;top:26px;font:700 30px Body;color:var(--ink-soft)">Tổng mỗi video</div>
       ${tot.map((s, j) => `<div class="tv tv${j}" style="right:28px;top:18px;font:800 46px Disp;letter-spacing:-.03em;white-space:nowrap;opacity:${j ? 0 : 1}">${s}</div>`).join('')}</div>` +
     [['Cắt vấp', 'scissors', 250, 222, -7], ['B-roll', 'film', 520, 210, 4], ['Chỉnh da', 'sparkles', 760, 226, 8]].map(([n, i, x, y, r], j) =>
       `<div class="mpw mp${j}" style="left:${x}px;top:${y}px;rotate:${r}deg;scale:1.2">${PILL('', 0, 0, n, i).replace('left:0px;top:0px;', 'position:relative;')}</div>`).join('') +
     `</div><div class="stp" style="left:330px;top:500px;z-index:30;rotate:-8deg;display:flex;align-items:center;gap:16px;padding:20px 36px;border-radius:24px;background:#F07A5A;color:#fff;font:800 56px Disp;letter-spacing:-.03em;white-space:nowrap;box-shadow:0 24px 50px -16px rgba(240,122,90,.7);border:5px solid #fff">${IC('alert', 54)}Hết thời gian</div>`;
 },
 anim(tl, $, f, v) {
   move(tl, f, v, CARD.R, 0, .5);
   move(tl, f, v, FULL, 3.2, .5);  // back to full face before s01
   tl.to($('.stp'), {opacity: 0, duration: .25}, 3.2);
   rise(tl, $('.ttl'), .1, 20); rise(tl, $('.tb2'), .12, 30);
   [.15, .4, .7, 1.3].forEach((t, j) => {
     const r = $('.rw' + j);
     tl.fromTo(r, {opacity: 0, y: -90, rotation: j % 2 ? 4 : -4}, {opacity: 1, y: 0, rotation: 0, duration: .38, ease: 'back.out(1.6)'}, t);
     pop(tl, r.querySelector('.rd'), t + .15, .5);
     tl.set($('.tv' + j), {opacity: 0}, t + .2); tl.fromTo($('.tv' + (j + 1)), {opacity: 0, y: 14}, {opacity: 1, y: 0, duration: .25, ease: 'expo.out'}, t + .2);
     if (j) $$('.rw').slice(0, j).forEach(o => tl.fromTo(o, {y: 0}, {keyframes: {y: [0, 6, 0]}, duration: .25, ease: 'none', immediateRender: false}, t + .3));
   });
   tl.to($('.ck svg'), {rotation: 300, duration: 2.1, ease: 'power1.in', transformOrigin: '50% 50%'}, .15);
   [1.75, 1.88, 2.0].forEach((t, j) => tl.fromTo($('.mp' + j), {opacity: 0, y: -160}, {opacity: 1, y: 0, duration: .3, ease: 'bounce.out'}, t));
   // overload at "vấn đề" (~11.0 video = 2.3)
   const t0 = 2.25;
   tl.to($$('.rw'), {borderColor: '#F07A5A', duration: .2}, t0);
   tl.to($$('.ri'), {color: '#F07A5A', borderColor: '#F07A5A', backgroundColor: 'rgba(255,179,156,.25)', duration: .2}, t0);
   tl.to($('.tb2'), {backgroundColor: 'rgba(255,179,156,.35)', borderColor: '#F07A5A', duration: .2}, t0);
   tl.to($('.ck'), {color: '#F07A5A', duration: .2}, t0);
   tl.set($('.tv4'), {opacity: 0}, t0); tl.fromTo($('.tv5'), {opacity: 0, scale: 1.4}, {opacity: 1, scale: 1, duration: .3, ease: 'back.out(2)', color: '#F07A5A'}, t0);
   F1.shake(tl, $('.stk'), t0, 16);
   tl.fromTo($('.stp'), {opacity: 0, scale: 1.8}, {opacity: 1, scale: 1, duration: .32, ease: 'back.out(1.4)'}, t0 + .2);
   F1.shake(tl, $('.stk'), t0 + .8, 9);
 }},

{id: 's62', clip: 'clips/s62.mp4', dur: 3.1, poster: 2.4, name: 'Timeline <em>cắt vấp</em>',
 desc: 'Intro 18.5-21.6: "cắt ra những đoạn mà mình nói vấp". Timeline editor có hình + sóng âm, 3 đoạn vấp tô đỏ, đầu phát chạy, kéo cắt ở "vấp" (19.8), 3 đoạn co lại, khoảng trống tự khép (ripple), tổng thời lượng giảm.',
 html: () => {
   const seg = [200, 90, 180, 70, 190, 80, 170], bad = j => j % 2 == 1;
   let off = 0;
   const cols = seg.map((w, j) => { const o = off; off += w;
     return `<div class="sg sg${j}${bad(j) ? ' bd' : ''}" style="position:relative;flex:none;width:${w}px;height:250px;overflow:hidden">
       <div style="left:2px;right:2px;top:0;height:118px;border-radius:10px;background:url(img/f1-s${j % 4}.jpg) ${-o % 210}px 0/210px 118px repeat-x"></div>
       <div style="left:2px;right:2px;top:132px;height:108px;border-radius:10px;background:rgba(169,224,194,.45);overflow:hidden">${F1.wave(w, 108, j*1.9 + 1, bad(j) ? '#C4553A' : '#3E9B6E')}</div>
       ${bad(j) ? `<div class="bo" style="left:2px;right:2px;top:0;height:240px;border-radius:10px;background:rgba(240,122,90,.38);border:3px solid #F07A5A"></div>
         <div class="bl" style="left:50%;top:92px;translate:-50% 0;padding:4px 10px;border-radius:999px;background:#F07A5A;color:#fff;font:800 18px Disp;white-space:nowrap">vấp</div>` : ''}</div>`; }).join('');
   const tools = ['scissors', 'wand', 'type', 'layers'];
   return BG + title(625, 120, 'AI <em>cắt vấp</em>', 'bỏ đoạn nói hỏng khi quay') +
     WIN('ed', 70, 310, 1110, 460, `
       <div style="left:24px;top:62px;display:flex;gap:10px">${tools.map((n, j) => `<div class="tl tl${j}" style="position:relative;width:48px;height:48px;border-radius:14px;border:2px solid var(--line-strong);display:grid;place-items:center;color:var(--ink-muted);background:#fff">${IC(n, 24)}</div>`).join('')}</div>
       <div class="cutp" style="left:300px;top:68px;display:flex;align-items:center;gap:8px;padding:8px 16px;border-radius:999px;background:rgba(169,224,194,.5);color:#2E7A55;font:800 22px Disp;white-space:nowrap">${IC('check', 22)}Đã cắt 3 chỗ vấp</div>
       <div style="right:24px;top:72px;display:flex;align-items:center;gap:10px;font:600 22px Mono;color:var(--ink-soft)">${IC('clock', 22)}<span class="d0" style="position:relative">03:12</span></div>
       <div class="d1" style="right:24px;top:72px;font:600 22px Mono;color:#2E7A55;background:#fff;padding-left:6px;opacity:0">02:41</div>
       <div style="left:100px;right:30px;top:128px;height:20px">${Array.from({length: 50}, (_, k) => `<i style="left:${k*20}px;top:${k % 5 ? 12 : 4}px;width:2px;height:${k % 5 ? 8 : 16}px;background:var(--ink-faint)"></i>`).join('')}</div>
       <div style="left:24px;top:200px;font:700 20px Mono;color:var(--ink-muted)">V1</div><div style="left:24px;top:330px;font:700 20px Mono;color:var(--ink-muted)">A1</div>
       <div class="trk" style="left:100px;top:160px;width:990px;height:250px;display:flex">${cols}</div>
       ${[1, 3, 5].map(j => { const x = 100 + seg.slice(0, j).reduce((a, b) => a + b, 0) + seg[j]/2;
         return `<div class="sc sc${j}" style="left:${x - 26}px;top:138px;width:52px;height:52px;border-radius:50%;background:#F07A5A;color:#fff;display:grid;place-items:center;z-index:5;box-shadow:0 6px 14px -6px rgba(240,122,90,.8)">${IC('scissors', 28)}</div>`; }).join('')}
       <div class="gone" style="left:844px;top:160px;width:240px;height:240px;border-radius:12px;border:3px dashed #F07A5A;background:rgba(255,179,156,.12);display:grid;place-items:center;color:#C4553A;font:800 30px Disp;white-space:nowrap">−31 giây</div>
       <div class="ph" style="left:110px;top:120px;width:4px;height:300px;background:var(--plum);border-radius:2px;z-index:6"><div style="left:-9px;top:-8px;width:22px;height:18px;border-radius:5px 5px 11px 11px;background:var(--plum)"></div></div>`, 'Timeline') +
     CUR('cur', 900, 760);
 },
 anim(tl, $, f, v) {
   move(tl, f, v, CARD.R, 0, .5);
   rise(tl, $('.ttl'), .1, 20); rise(tl, $('.ed'), .05, 40);
   $$('.sg').forEach((e, j) => tl.fromTo(e, {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: .3, ease: 'expo.out'}, .2 + j*.04));
   tl.fromTo($('.ph'), {x: 0}, {x: 720, duration: 2.8, ease: 'none'}, .3);
   // stumbles flagged while "cắt ra những đoạn" is said
   $$('.bd').forEach((e, j) => { pop(tl, e.querySelector('.bl'), .55 + j*.15, .4); tl.fromTo(e.querySelector('.bo'), {opacity: 0}, {opacity: 1, duration: .2}, .5 + j*.15); });
   glide(tl, $('.cur'), .55, 120, 380, .55); click(tl, $('.cur'), 1.12);
   lit(tl, $('.tl0'), 1.12, '#F07A5A', 'rgba(255,179,156,.3)');
   // cut on "vấp" (19.8 = 1.3)
   [1, 3, 5].forEach((j, k) => {
     tl.fromTo($('.sc' + j), {opacity: 0, scale: .3, rotation: -40}, {opacity: 1, scale: 1, rotation: 0, duration: .25, ease: 'back.out(2)'}, 1.25 + k*.07);
     tl.to($('.sc' + j), {opacity: 0, scale: .6, duration: .2}, 1.62 + k*.07);
     tl.to($('.sg' + j), {width: 0, duration: .32, ease: 'power3.inOut'}, 1.5 + k*.07);
   });
   tl.to($('.cur'), {opacity: 0, duration: .2}, 1.5);
   tl.to($('.d0'), {opacity: 0, duration: .1}, 1.85); tl.fromTo($('.d1'), {opacity: 0, y: -10}, {opacity: 1, y: 0, duration: .25, ease: 'expo.out'}, 1.85);
   pop(tl, $('.cutp'), 1.9, .5); tl.fromTo($('.gone'), {opacity: 0, scaleX: .4, transformOrigin: '0 50%'}, {opacity: 1, scaleX: 1, duration: .35, ease: 'expo.out'}, 1.85);
   // "quay" (21.0 = 2.5): the tidy track gives a small settle bounce
   tl.fromTo($('.trk'), {scale: 1}, {keyframes: {scale: [1, 1.015, 1]}, duration: .3, ease: 'none', immediateRender: false}, 2.5);
 }},

{id: 's63', clip: 'clips/s63.mp4', dur: 2.6, poster: 2.3, name: 'AI <em>chỉnh da</em> nhẹ',
 desc: 'Intro 21.6-24.2: "Nó giúp cho mình chỉnh da ở gương mặt". Mặt ra giữa khung lớn, bảng chỉnh da bên phải bật ở "chỉnh" (22.4), thanh Làm mịn / Sáng da / Đều màu chạy ở "da" (22.8), vạch quét + khung nhận mặt ở "gương mặt" (23.3). Không lọc mạnh lên mặt.',
 html: () => {
   const sl = [['Làm mịn', 35], ['Sáng da', 20], ['Đều màu', 25]];
   return BG + title(1490, 120, 'AI <em>chỉnh da</em>', 'nhẹ, vẫn giữ thật') +
     `<div class="pn paper" style="left:1180px;top:330px;width:620px;height:500px;border-radius:28px">
       <div style="left:30px;top:28px;display:flex;align-items:center;gap:12px;color:var(--plum)">${IC('sparkles', 32)}<span style="position:static;font:800 32px Disp;color:var(--ink)">Chỉnh da</span></div>
       <div class="sw" style="right:30px;top:28px;width:76px;height:42px;border-radius:21px;background:var(--ink-faint)"><div class="kn" style="left:4px;top:4px;width:34px;height:34px;border-radius:50%;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.2)"></div></div>
       <i style="left:30px;right:30px;top:96px;height:1.5px;background:var(--line)"></i>
       ${sl.map(([n, p], j) => `<div class="sr sr${j}" style="left:30px;top:${126 + j*100}px;width:560px;height:80px">
         <div style="left:0;top:0;font:700 24px Body">${n}</div>
         <div class="v0" style="right:0;top:2px;font:600 22px Mono;color:var(--ink-muted)">0%</div>
         <div class="v1" style="right:0;top:2px;font:600 22px Mono;color:var(--plum);opacity:0">${p}%</div>
         <div style="left:0;right:0;top:50px;height:10px;border-radius:5px;background:var(--ivory-deep)"></div>
         <div class="fl" style="left:0;top:50px;width:${p*5.6}px;height:10px;border-radius:5px;background:var(--plum);transform-origin:0 50%"></div>
         <div class="kb" style="left:-15px;top:40px;width:30px;height:30px;border-radius:50%;background:#fff;border:3px solid var(--plum);box-shadow:0 3px 8px rgba(23,19,13,.2)"></div></div>`).join('')}
       <div class="ok" style="left:30px;top:430px;display:flex;align-items:center;gap:8px;padding:6px 14px;border-radius:999px;background:rgba(169,224,194,.5);color:#2E7A55;font:700 24px Body;white-space:nowrap">${IC("check", 24)}Đã nhận gương mặt</div></div>` +
     `<div class="scn" style="left:320px;top:150px;width:760px;height:820px;border-radius:228px;overflow:hidden;z-index:22">
       <div class="sl" style="left:0;top:-170px;width:760px;height:170px;background:linear-gradient(180deg,rgba(183,168,255,0),rgba(183,168,255,.35));border-bottom:4px solid rgba(255,255,255,.95);box-shadow:0 0 24px 4px rgba(123,108,255,.55)"></div></div>` +
     `<div class="fb" style="left:505px;top:380px;width:390px;height:450px;z-index:23">${[[0, 0, '0 0'], [1, 0, '100% 0'], [0, 1, '0 100%'], [1, 1, '100% 100%']].map(([x, y]) =>
       `<i style="${x ? 'right' : 'left'}:0;${y ? 'bottom' : 'top'}:0;width:56px;height:56px;border-${x ? 'right' : 'left'}:6px solid #fff;border-${y ? 'bottom' : 'top'}:6px solid #fff;border-${y ? 'bottom' : 'top'}-${x ? 'right' : 'left'}-radius:18px;filter:drop-shadow(0 0 6px rgba(74,58,224,.7))"></i>`).join('')}</div>` +
     [[420, 290, 64], [940, 410, 48], [450, 770, 44], [890, 820, 56]].map(([x, y, s], j) =>
       `<div class="sp sp${j}" style="left:${x}px;top:${y}px;z-index:24;color:#fff;filter:drop-shadow(0 0 8px rgba(74,58,224,.85))">${IC('sparkles', s)}</div>`).join('');
 },
 anim(tl, $, f, v) {
   F1.setCard(tl, f, v, CARD.R);
   const BIG = card(700, 560, 760, 820);
   move(tl, f, v, BIG, 0, .5);
   rise(tl, $('.ttl'), .15, 20); rise(tl, $('.pn'), .25, 40);
   // "chỉnh" (22.4 = .8): switch on
   tl.to($('.sw'), {backgroundColor: '#4A3AE0', duration: .2}, .75); tl.to($('.kn'), {x: 34, duration: .25, ease: 'back.out(1.6)'}, .75);
   // "da" (22.8 = 1.2): sliders run
   $$('.sr').forEach((r, j) => { const t = 1.0 + j*.2, w = r.querySelector('.fl').offsetWidth || parseFloat(r.querySelector('.fl').style.width);
     tl.fromTo(r.querySelector('.fl'), {scaleX: 0}, {scaleX: 1, duration: .45, ease: 'power2.out'}, t);
     tl.fromTo(r.querySelector('.kb'), {x: 0}, {x: w, duration: .45, ease: 'power2.out'}, t);
     tl.set(r.querySelector('.v0'), {opacity: 0}, t + .3); tl.set(r.querySelector('.v1'), {opacity: 1}, t + .3);
   });
   tl.fromTo(v, {filter: 'brightness(1)'}, {filter: 'brightness(1.03)', duration: .6, ease: 'none'}, 1.1);
   // "gương mặt" (23.3 = 1.7): scan + face box + sparkles
   tl.set($('.scn'), {opacity: 0}, 0); tl.set($('.scn'), {opacity: 1}, 1.6); tl.fromTo($('.sl'), {y: 0}, {y: 1060, duration: .7, ease: 'power1.inOut'}, 1.6); tl.set($('.scn'), {opacity: 0}, 2.32);
   tl.fromTo($('.fb'), {opacity: 0, scale: 1.25}, {opacity: 1, scale: 1, duration: .35, ease: 'expo.out'}, 1.7);
   pop(tl, $('.ok'), 1.85, .5);
   $$('.sp').forEach((e, j) => { tl.fromTo(e, {opacity: 0, scale: .2, rotation: -30}, {opacity: 1, scale: 1, rotation: 0, duration: .3, ease: 'back.out(2)'}, 1.9 + j*.09);
     tl.to(e, {scale: .75, duration: .15, ease: 'power1.inOut', yoyo: true, repeat: 1}, 2.1 + j*.03); });
 }},

{id: 's64', clip: 'clips/s64.mp4', dur: 3.1, poster: 2.6, name: 'Track <em>B-roll</em> + animation',
 desc: 'Intro 24.2-27.3: "Nó giúp cho mình làm những B-roll ... animation". Timeline 3 track: V1 là mặt nói, khung B-roll thật rơi xuống V2 liên tục, khung xem trước lật theo; ở "animation" (25.9) nhãn đổi, cảnh animation rơi vào V3.',
 html: () => {
   const br = ['ov-002', 'ov-008', 'ov-015', 'ov-047'], an = ['ov-025', 'ov-027', 'ov-031'];
   const clip = (cls, im, x, an) => `<div class="cl ${cls}" style="left:${x}px;top:0;width:220px;height:80px;border-radius:10px;overflow:hidden;border:3px solid ${an ? 'var(--plum)' : '#fff'};box-shadow:0 6px 14px -8px rgba(23,19,13,.5)">
     <img src="img/${im}-hero.jpg" style="left:0;top:0;width:100%;height:100%;object-fit:cover">${an ? `<div style="left:6px;top:6px;width:26px;height:26px;border-radius:8px;background:var(--plum);color:#fff;display:grid;place-items:center">${IC('sparkles', 16)}</div>` : ''}</div>`;
   const lane = (y, lab, inner) => `<div style="left:20px;top:${y + 24}px;font:700 20px Mono;color:var(--ink-muted)">${lab}</div>
     <div style="left:100px;top:${y}px;width:1640px;height:80px;border-radius:12px;background:rgba(23,19,13,.04)">${inner}</div>`;
   return BG + WIN('pv', 760, 50, 980, 606, `<div style="left:10px;top:56px;width:960px;height:540px;border-radius:14px;overflow:hidden;background:#000">
       <img class="pi" src="img/f1-s1.jpg" style="left:0;top:0;width:100%;height:100%;object-fit:cover">
       ${[...br, ...an].map((im, j) => `<img class="pi pi${j}" src="img/${im}-hero.jpg" style="left:0;top:0;width:100%;height:100%;object-fit:cover;opacity:0">`).join('')}
       <div class="fl2" style="inset:0;background:#fff;opacity:0"></div></div>`, 'Xem trước') +
     `<div class="lb0" style="left:800px;top:560px;z-index:5;display:flex;align-items:center;gap:12px;padding:12px 24px;border-radius:999px;background:var(--ink);color:#fff;font:800 36px Disp;letter-spacing:-.02em;white-space:nowrap">${IC('film', 32)}B-roll</div>
      <div class="lb1" style="left:800px;top:560px;z-index:6;display:flex;align-items:center;gap:12px;padding:12px 24px;border-radius:999px;background:var(--plum);color:#fff;font:800 36px Disp;letter-spacing:-.02em;white-space:nowrap">${IC('sparkles', 32)}<span class="em" style="color:#fff">animation</span></div>
      <div class="tp paper" style="left:80px;top:700px;width:1760px;height:340px;border-radius:26px">
       <div style="left:100px;top:14px;width:1640px;height:24px">${Array.from({length: 83}, (_, k) => `<i style="left:${k*20}px;top:${k % 5 ? 12 : 4}px;width:2px;height:${k % 5 ? 8 : 16}px;background:var(--ink-faint)"></i>`).join('')}</div>
       ${lane(54, 'V3', an.map((im, j) => clip('a' + j, im, 900 + j*250, 1)).join(''))}
       ${lane(144, 'V2', br.map((im, j) => clip('b' + j, im, 20 + j*250, 0)).join(''))}
       ${lane(234, 'V1', `<div style="inset:0;border-radius:12px;background:url(img/f1-s1.jpg) 0 0/142px 80px repeat-x;opacity:.9"></div>
         <div style="left:12px;top:22px;padding:4px 12px;border-radius:999px;background:rgba(255,255,255,.9);font:700 18px Body;white-space:nowrap">Mặt nói</div>`)}
       <div class="sn" style="left:0;top:40px;width:3px;height:290px;background:var(--gold);opacity:0;z-index:4"></div>
       <div class="ph" style="left:100px;top:10px;width:4px;height:320px;background:var(--plum);border-radius:2px;z-index:6"><div style="left:-9px;top:-6px;width:22px;height:18px;border-radius:5px 5px 11px 11px;background:var(--plum)"></div></div></div>`;
 },
 anim(tl, $, f, v) {
   F1.setCard(tl, f, v, card(700, 560, 760, 820));
   move(tl, f, v, card(330, 350, 480, 540), 0, .5);
   rise(tl, $('.tp'), .05, 60); rise(tl, $('.pv'), .1, 40);
   tl.fromTo($('.ph'), {x: 0}, {x: 1600, duration: 2.9, ease: 'none'}, .2);
   const drop = (el, pi, t, x) => {
     tl.fromTo(el, {opacity: 0, y: -150, scale: 1.15}, {opacity: 1, y: 0, scale: 1, duration: .32, ease: 'back.out(1.5)'}, t);
     tl.fromTo($('.sn'), {opacity: 1, x}, {opacity: 0, x, duration: .35, ease: 'power1.in', immediateRender: false}, t + .28);
     tl.set(pi, {opacity: 1}, t + .2); tl.fromTo(pi, {scale: 1.08}, {scale: 1, duration: .35, ease: 'expo.out', immediateRender: false}, t + .2);
     tl.fromTo($('.fl2'), {opacity: .5}, {opacity: 0, duration: .18, immediateRender: false}, t + .2);
   };
   [.3, .6, .9, 1.2].forEach((t, j) => drop($('.b' + j), $('.pi' + j), t, 120 + j*250));
   tl.fromTo($('.lb0'), {opacity: 0, y: 20, scale: .7}, {opacity: 1, y: 0, scale: 1, duration: .35, ease: 'back.out(1.8)'}, .55);
   tl.set($('.lb1'), {opacity: 0}, 0);
   // "animation" (25.9 = 1.7)
   tl.to($('.lb0'), {opacity: 0, y: -20, duration: .15}, 1.65);
   tl.fromTo($('.lb1'), {opacity: 0, y: 20, scale: .7}, {opacity: 1, y: 0, scale: 1, duration: .35, ease: 'back.out(1.8)', immediateRender: false}, 1.68);
   [1.7, 2.0, 2.3].forEach((t, j) => drop($('.a' + j), $('.pi' + (4 + j)), t, 1000 + j*250));
 }},
);
