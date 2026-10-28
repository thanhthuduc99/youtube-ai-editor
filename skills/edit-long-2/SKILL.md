---
name: edit-long-2
description: Edit video YouTube dài từ source chỉ có mặt người nói (talking head), theo style RoboNuggets (Jay E) đổi sang màu brand Contentta - mặt thu vào khung bo tròn đổi bên liên tục, slide sơ đồ nét mảnh, lưới icon sáng theo lời, giao diện chat Claude dựng lại có chữ gõ dần và tool call, thẻ "Bạn nên biết", logo bật quanh mặt, trang web thật có zoom, công tắc gạt, chữ glitch. Nền ivory, quầng pastel, nhấn plum, chữ Bricolage + Lora nghiêng. Luôn làm file HTML demo các hiệu ứng trên chính đoạn video đó cho user duyệt trước. Dùng khi user nói "edit long 2", "edit-long-2", "edit kiểu RoboNuggets", "edit giống video Claude Mods", hoặc gửi video chỉ có mặt muốn edit theo style này.
---

# Edit Long 2: talking head → style RoboNuggets, màu Contentta

Đầu vào: 1 video ngang chỉ có mặt người nói (đã cắt vấp, hoặc raw thì chạy skill `youtube` phần cắt trước).
Đầu ra hiện tại: `edit2-demo/index.html`, đủ 50 hiệu ứng của video gốc, mỗi cái chạy trên 1 đoạn thật của video, có tiếng, để user duyệt style.

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

## Dùng chung với edit-long
Hướng đi (user chốt 28/10/2026): 1 video dùng cả 2 bộ hiệu ứng, chung 1 `edit-plan.json` của `edit-long`.
- Đoạn mặt người nói: hiệu ứng edit-long-2 (mặt thu vào khung bo, slide nét mảnh, chat Claude, lưới icon, giả lập quay màn hình Claude).
- Đoạn quay màn hình, slide B-roll, chapter card: template `sl-*`, `th-*` của edit-long.
- Mỗi cảnh edit-long-2 sẽ thành 1 overlay `rn-*` trong plan. Hiện chưa có builder `rn-*` (xem "Chưa làm"), nên video final vẫn render bằng edit-long, trang demo chỉ để duyệt style.

## Chưa làm
- Builder HyperFrames `rn-*` để render vào video final (giống `talking.py` của `edit-long`). Làm sau khi user duyệt demo: port từng cảnh trong `template.html` thành 1 builder, nhúng clip mặt bằng `face(ctx)`, rồi dùng `build.py` → `preview.py` → `render_overlays.py` → `composite.py` của `edit-long`.
- SFX: whoosh khi mặt thu vào khung, pop khi icon/tick bật, click khi gạt công tắc. Thêm lúc làm builder.
