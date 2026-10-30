---
name: edit-long-2
description: Edit video YouTube dài từ source chỉ có mặt người nói (talking head), theo style RoboNuggets (Jay E) đổi sang màu brand Contentta - mặt thu vào khung bo tròn đổi bên liên tục, slide sơ đồ nét mảnh, lưới icon sáng theo lời, giao diện chat Claude dựng lại có chữ gõ dần và tool call, thẻ "Bạn nên biết", logo bật quanh mặt, trang web thật có zoom, công tắc gạt, chữ glitch. Nền ivory, quầng pastel, nhấn plum, chữ Bricolage + Lora nghiêng. Luôn làm file HTML demo các hiệu ứng trên chính đoạn video đó cho user duyệt trước. Dùng khi user nói "edit long 2", "edit-long-2", "edit kiểu RoboNuggets", "edit giống video Claude Mods", hoặc gửi video chỉ có mặt muốn edit theo style này.
---

# Edit Long 2: talking head → style RoboNuggets, màu Contentta

Đầu vào: 1 video ngang chỉ có mặt người nói (đã cắt vấp, hoặc raw thì chạy skill `youtube` phần cắt trước).
Đầu ra:
1. `edit2-demo/index.html`: các cảnh hiệu ứng chạy trên đoạn thật của video, có tiếng, để user duyệt style.
2. Sau khi duyệt: `renders/final-edit2.mp4`, cả video đã ghép (mục "Render final").

Mặc định (user chốt 29-30/10/2026): **không chỉnh da** (user chê K2, thích da gốc như trong demo), **không nhạc nền** (user bảo xoá nhạc intro). Muốn thêm thì hỏi trước.

## Nhịp (đo trên video RoboNuggets 30/10/2026, user dặn: source chỉ có mặt thì phải edit nhịp nhanh)
- Mặt full khung chỉ chiếm 22% thời lượng. 78% còn lại mặt nằm trong khung bo nhỏ, đồ hoạ chạy theo lời.
- Mỗi đoạn mặt full trung vị 4.5s. Đoạn trên 6s chỉ 5 chỗ trong 12:47, gần như chỉ ở đầu và cuối.
- Luật: **không để đoạn mặt full nào dài quá ~4-5s**. Video 15 phút cần khoảng 70 cảnh (bản Hệ thống YouTube AI: 70 cảnh, đoạn mặt full dài nhất 5.9s).
- Cảnh 3-12s, đổi bên khung mặt (trái, phải, góc dưới trái) giữa 2 cảnh liền nhau. Cảnh nói về 1 bước edit (cắt, chỉnh da, B-roll, thumbnail, đăng) thì dựng UI edit thật: timeline, thanh trượt, layer, con trỏ bấm.
- Intro (khoảng 90s đầu) dày nhất: mỗi ý 1 cảnh 3-4s (vd "cắt vấp", "chỉnh da", "B-roll", "2 video 10k view" mỗi cái 1 cảnh riêng).
- Đo lại khi cần: tải video RN bằng yt-dlp, tỉ lệ pixel nền than `#1C1B19` theo từng giây: dưới 30% là mặt full.

Phân tích style, bảng hiệu ứng và đổi màu: `references/style.md`. Ảnh gốc: xem video RoboNuggets trên YouTube (không kèm trong repo).

## Quy trình

1. **Đọc transcript** (`assets/transcript.json` của project). Chọn 8-12 câu hợp với từng hiệu ứng trong bảng ở `style.md`. Ưu tiên câu có danh sách, quy trình, con số, câu "mình prompt cho nó".
2. **Lấy mốc từng chữ** trong mỗi đoạn (giây tương đối so với đầu clip). Mọi mốc hiệu ứng đặt theo chữ, ví dụ icon "Chỉnh da" sáng đúng lúc nói "chín da".
3. **Cắt clip** 6-14 giây cho mỗi cảnh: `ffmpeg -nostdin -ss a -to b -i cut.mp4 -vf scale=1280:-2 -c:v h264_nvenc -cq 24 -c:a aac edit2-demo/clips/sNN.mp4`.
4. **Chép bản mẫu:** `references/demo/` (template.html, build_demo.py, check.py, scenes/*.js) vào `projects/<slug>/edit2-demo/`, cùng `gsap.min.js`, `fonts/` (display, body, body-bold, mono từ `assets/fonts`), ảnh thật vào `img/`.
5. **Sửa cảnh:** s01-s10 nằm trong `template.html`, s11+ trong `scenes/b.js`-`e.js` (helper chung ở `scenes/kit.js`: WIN, CLAUDE, INPUT, MASC, CUR, TILE, PILL, LINE, lit, hop, draw, type, click, glide). Mỗi phần tử trong `SCENES` là 1 cảnh (`clip`, `dur`, `poster`, `html`, `anim`). Giữ helper `move()` (mặt ↔ khung bo), `rise()`, `pop()`, `CARD.L/R/BL`. Đổi chữ, icon, ảnh theo nội dung video. Chất liệu phải thật: ảnh chụp trang thật, khung review thật, prompt thật.
6. **Build + soát:** `python build_demo.py` → `python check.py` chụp mỗi cảnh 3 mốc vào `screenshots/edit2/`, mở `edit2-sheet.jpg` soi bằng mắt:
   - chữ nhấn Lora không chồng lên chữ khác;
   - icon, logo hiện đủ (không còn `{{...}}`);
   - khung mặt không che chữ, tiêu đề;
   - `errors: []`.
7. **Gửi user** `edit2-demo/index.html`, rồi dừng chờ duyệt.

## Render final (làm từ 29/10/2026, thay cho builder `rn-*`)
Cảnh HTML được render thẳng ra video bằng Chrome: tua clip mặt + tua timeline GSAP tới từng khung, chụp, đẩy vào ffmpeg. Script ở `references/demo/`: `final_plan.py`, `render_scenes.py`, `compose_final.py`, `serve.py`.
1. Mỗi cảnh 1 dòng `<id> <start> <end>` (giây trong `cut/renders/cut.mp4`) trong `clips*.txt`. Đoạn giả lập màn hình đặt id `sim`.
2. `python serve.py 8766` (chạy nền). `python final_plan.py` → `final_plan.json` + clip mặt full HD `clips-hd/<id>.mp4` (`-g 10` cho tua nhanh). Cảnh xen chồng thì cảnh trước dừng khi cảnh sau bắt đầu. Cảnh kết thúc trước 1 khoảng mặt full ≥ 0.6s được thêm `tail` 18 khung: khung mặt phóng về full (`<id>-tail.mp4`).
3. `python render_scenes.py [ids]` → `renders/<id>.mp4`. Khoảng 0.2s/khung, 1 Chrome. Không truyền id thì render mọi cảnh và tail còn thiếu.
4. `python compose_final.py` → `../renders/final-edit2.mp4`: cắt timeline thành từng đoạn (cut gốc / cảnh / tail), encode giống nhau, nối bằng concat, gắn tiếng gốc của cut.
5. Soát: số khung final = số khung cut, đoạn mặt full dài nhất (đếm từ `final_plan.json`), ảnh giữa mỗi cảnh ghép thành 1 tấm, khung cuối mỗi cảnh trước mặt full phải là mặt full (không giật).

**Chia subagent** (user yêu cầu 30/10/2026, cảnh nhiều thì làm vậy): mỗi agent 1 file cảnh riêng (`scenes/f1.js`, `g1.js`...) + 1 file `clips4N.txt` riêng + 1 dải id riêng, thêm thẻ `<script>` cho từng file vào `template.html` TRƯỚC khi giao. Đưa mỗi agent: khoảng thời gian, mốc từng chữ (`briefs/gap-X.txt`), cảnh liền trước/sau, luật nhịp ở trên, cách test (`final_plan.py` → `build_demo.py` → `render_scenes.py <id>` → xem khung bằng Read). 3 agent làm intro + 3 agent lấp khoảng mặt full, khoảng 25 phút cho 46 cảnh. Xong thì tự xem ảnh giữa của mọi cảnh, đừng tin báo cáo.

## Giả lập quay màn hình Claude (`references/demo/sim.html`)
Khi user kể "mình mở Claude, chọn folder, dán link, prompt…" mà không quay màn hình: dựng lại màn hình Windows (1536x864 logic, phóng 1.25), app Claude desktop tab Code, Chrome, File Explorer, hộp chọn folder. Mặt ở khung bo góc phải dưới.
- **Giao diện Claude phải giống app thật nhất có thể** (user dặn 28/10/2026). Trước khi dựng, chụp màn hình thật bằng PowerShell `CopyFromScreen` vào `screenshots/claude-ui/`, rồi đo vị trí, cỡ chữ, màu trên ảnh. Cửa sổ Claude (`.cw`) viết bằng px thật của ảnh 1920x1080, thu `scale:.8` vào màn logic; toạ độ con trỏ dùng `goP/camP` (px thật).
- Bố cục thật (Claude desktop 28/10/2026): thanh bên 280px nền #FAFAFA, nút `Home | Code`, nhóm project in đậm có nút `+`, phiên mới mở bằng `+` của nhóm; góc dưới "Thanh · Max". Màn phiên mới: mascot pixel + thẻ "Choose environment" ở giữa, ô chat "Describe a task or ask a question" ở đáy. **Chip "This computer" và chip folder nằm DƯỚI ô chat** (cùng hàng "Auto", phải là "Opus 5.5 High"); menu của chip mở lên trên. Trong 1 phiên đang chạy, hàng dưới chỉ còn "Auto" + model, placeholder "Type / for commands".
- Icon thật: taskbar là ảnh cắt từ ảnh chụp thật (`img/sim/taskbar.png`), mascot `img/sim/clawd.png`. Icon trong app dùng SVG nét mảnh kiểu lucide (laptop, folder, home, `<>`).
- **Không tự bấm vào app Claude của user để chụp** (tạo phiên mới, mở menu): user chặn 28/10/2026. Chụp màn hình đang có, thiếu gì thì hỏi user tự mở rồi chụp gửi.
- Mọi phần tử con lồng trong flex row phải có class `f` (relative), không thì `.screen *` absolute làm chữ chồng nhau ("Opus 5.5High").
- Mỗi bước đặt theo giờ chữ trong transcript (`at(t)` là giờ trong bản cắt). Helper: `go` (con trỏ tới nơi đúng lúc t), `click`, `type`, `show`, `cam` (zoom vào chỗ thao tác), `front` (đổi cửa sổ).
- Nội dung chat lấy thật: prompt user từng gõ (tìm trong `~/.claude/projects/*/*.jsonl`), lệnh và kết quả tool thật của session, tên file, dung lượng, ngày thật.
- Soát bằng `sim_check.py <giờ...>` (cần `serve.py` chạy ở :8765).

## Luật (đã gặp thật)

| Luật | Lý do |
|---|---|
| `.stage *` là absolute, nên `em`, `b`, `span` trong tiêu đề phải relative | Không thì chữ Lora nghiêng chồng lên chữ sau |
| Icon, logo có tên động trong template literal dùng `IC(name, size)` và `LOGOS[k]`, không dùng `{{...}}` | Python chỉ thay được placeholder tĩnh |
| Không đặt 2 class trùng tên trong 1 cảnh (`.sc` vừa là đoạn timeline vừa là cây kéo) | `$('.sc')` lấy nhầm phần tử, cả đoạn bị bay mất |
| Chữ gõ dần: ẩn bằng `display:none` rồi bật từng chữ | Ẩn bằng opacity thì con trỏ đứng sẵn ở cuối dòng |
| Hiệu ứng tween thuộc tính CSS, không dùng `onUpdate` | Timeline được tua bằng `tl.time()`, callback không chạy khi tua |
| Clip nạp khi cuộn tới (IntersectionObserver), không nạp 50 video cùng lúc | Chrome nghẽn, trang treo |
| Toạ độ con trỏ trong khung CLAUDE: stage = 70 + 1.3*(300 + x), 46 + 1.3*(60 + y) | Khung UI phóng 1.3 lần, tính sai thì con trỏ bấm trượt nút |
| Trang demo phải mở qua `serve.py` (localhost, có Range), không mở bằng khung xem file của app | Khung xem file chỉ dựng bản tĩnh, không chạy JS, không tải clip, nên mọi khung trống |
| GSAP không set được `className`, đổi trạng thái bằng màu/nền trực tiếp | Set className không có tác dụng, tab và menu không đổi |
| Khung mặt: tâm và cỡ lấy theo mặt dò được trong từng clip (`faces.json`), đầu chiếm ~78% chiều cao khung | Đặt tâm cố định thì cắt mất trán, cằm |
| Brand Contentta không có dark mode | Nền tối của RoboNuggets đổi sang ivory + pastel, xem bảng đổi màu |
| Render bằng `channel='chrome'` (Chrome cài sẵn), không dùng Chromium của Playwright | Chromium không giải mã H.264, clip mặt đen |
| Chặn `**/clips/*.mp4` khi render, nạp clip HD bằng tay | Trang demo tự nạp mấy chục clip 1280, máy 16 GB hết RAM, Chrome treo hoặc chụp lỗi |
| Chụp lỗi thì thử lại tới 5 lần; render 1 cảnh 1 lúc mỗi tiến trình | Máy ít RAM (game, job khác) làm `captureScreenshot` lỗi giữa chừng |
| Lỗi `SCENES is not defined` hoặc trang lạ: kiểm tra cổng server | 30/10 cổng 8765 bị 1 project khác chiếm, Chrome tải nhầm trang "Mây kết bạn"; render chuyển sang 8766 |
| Cảnh liền sau 1 cảnh khác thì mở đầu với mặt đúng ở khung của cảnh trước, rồi mới đổi bên | Không thì mặt nháy full khung 1-2 khung giữa 2 cảnh |
| Cảnh đứng ngay trước 1 cảnh mở bằng mặt full mà không đủ chỗ cho tail thì tự `move(..., FULL, dur-0.5)` và ẩn chữ đè trên mặt | Không thì giật từ khung nhỏ sang full |
| Ảnh chụp từ Chrome là JPEG full range BT.601: đổi `scale=in_range=pc:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709` khi ghép | Không thì màu mặt trong cảnh lệch so với đoạn cut gốc |
| Ghép bằng nối từng đoạn (concat), không đè 80 lớp `overlay` trong 1 lệnh ffmpeg | 80 bộ giải mã 1080p mở cùng lúc ăn hết RAM |
| Số liệu trên màn hình phải là số thật (view, sub) hoặc ghi "10.000+"; không có số thật thì không ghi số | Không bịa số trên kênh của user |

## Dùng chung với edit-long
Hướng đi (user chốt 28/10/2026): 1 video dùng cả 2 bộ hiệu ứng, chung 1 `edit-plan.json` của `edit-long`.
- Đoạn mặt người nói: hiệu ứng edit-long-2 (mặt thu vào khung bo, slide nét mảnh, chat Claude, lưới icon, giả lập quay màn hình Claude).
- Đoạn quay màn hình, slide B-roll, chapter card: template `sl-*`, `th-*` của edit-long.
- Video chỉ có mặt (như Hệ thống YouTube AI) thì render final toàn bộ bằng mục "Render final", không cần edit-long.

## Chưa làm
- SFX: whoosh khi mặt thu vào khung, pop khi icon/tick bật, click khi gạt công tắc. Hỏi user trước (user vừa bỏ nhạc nền).
- Video có cả đoạn quay màn hình: chưa ghép chung với overlay `sl-*`/`th-*` của edit-long trong 1 lần render.

## Thư viện cảnh
`references/demo/scenes/`: `b.js`-`e.js` (50 hiệu ứng gốc s11-s57), `f1-f3.js` (intro: việc tay chồng chất, timeline cắt vấp, bảng chỉnh da, track B-roll, thẻ view chạy số, cột 10x, đăng đa nền tảng, link miễn phí, mục lục video), `g1-g3.js` (26 cảnh lấp khoảng mặt full: YouTube Studio, A/B thumbnail, chat lên sườn, luật quay, lệnh "Hey Claude", Codex tạo thumbnail...). Đều viết cho video Hệ thống YouTube AI: chép khuôn, thay chữ, mốc giờ, ảnh theo video mới.
