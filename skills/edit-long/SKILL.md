---
name: edit-long
description: Edit video YouTube dài 10-40 phút (ngang 1920x1080, quay màn hình + webcam hoặc talking head) hoàn toàn bằng code, không dùng API trả phí. Style mặc định là bản gộp - chapter card đầu mỗi phần, chữ giữa dưới, cứ khoảng 2 phút 1 slide B-roll 3D dựng từ chất liệu thật (khung hình, file, giao diện app thật, MacBook 3D, logo 3D, mascot Claude Code). Đoạn mặt người nói (talking head) có bộ template kiểu Ben AI - khung hình trượt trái phải, lớp mờ đen, chữ và hình hiện 2 bên mặt, clip nguồn tua nhanh, PiP, tường thumbnail nghiêng chạy. Gốc là 2 style - cơ bản (học Ben AI - chapter card đầu mỗi phần, ít chữ keyword, intro là các đoạn cắt từ video tua nhanh đè lên đoạn hook) và nâng cao (học Liam Ottley - đồ hoạ toàn khung mỗi 10-20 giây, model 3D Three.js, ảnh so sánh, số đếm, sơ đồ, chip section, punch-in zoom, SFX). Luôn render ảnh mẫu đặt lên khung hình thật cho user duyệt trước, duyệt xong mới render video. Dùng khi user nói "edit video dài", "edit youtube", "edit long", "edit cơ bản", "edit nâng cao", "edit kiểu Ben AI", "edit kiểu Liam Ottley", hoặc gửi 1 video ngang dài muốn thêm motion graphics.
---

# Edit Long: video YouTube dài, 2 style

Đầu vào: 1 video ngang dài (mp4/mov, HEVC cũng được). Đầu ra: `renders/final.mp4` 1920x1080 30fps, tiếng gốc giữ nguyên + SFX, kèm `chapters.txt` để dán vào mô tả YouTube và `renders/qa-report.json`.

Chi phí: 0 đồng API. Transcript chạy local (faster-whisper), đồ hoạ là HTML/SVG/Three.js do Claude viết, render bằng HyperFrames + ffmpeg trên máy. Chỉ tốn usage Claude Code. Nếu tính theo giá API Opus 5.5, 10 slide B-roll khi skill đã có builder sẵn tốn khoảng 5-10 USD; phải viết builder mới thì khoảng 10-18 USD (đo thật ngày 13/10/2026).

## Kiến trúc (đọc 1 lần)

- **Video gốc không vào Chrome.** Mỗi overlay là 1 composition HyperFrames ngắn (`compositions/ov-NNN.html`, 2-7 giây). Chỉ những file này được render.
- **Overlay góc** (keyword, lower-third, chips, chip section) render ra RGBA, lưu FFV1 lossless. Overlay giữ lâu (chip section 2-5 phút) chỉ render đoạn vào + ra, `composite.py` lặp khung đứng yên ở giữa.
- **Overlay toàn khung** (chapter, B-roll, stat, flow, compare, 3D...) cắt cứng vào/ra, đục từ khung đầu, lưu H.264 4:4:4.
- **Ghép:** 1 lệnh ffmpeg (`movie=` + `overlay`) ghép tất cả lên video gốc, cộng zoom và SFX, encode h264_nvenc. Tốc độ 2.4 đến 5.5 lần realtime tuỳ số overlay. Video 12 phút có 20 overlay mất 5 phút.
- **Ảnh mẫu:** Playwright seek từng overlay, chụp nền trong suốt, dán lên khung gốc đúng giây đó. Không cần render video để duyệt.

## Yêu cầu máy

- Node 22+, ffmpeg/ffprobe trên PATH. HyperFrames qua `npx.cmd --yes hyperframes@0.8.143` (đã pin trong `common.py`).
- Python 3.10+ có sẵn `faster-whisper`, `playwright` (chromium), `pillow`, `numpy`.
- GPU NVIDIA cho h264_nvenc. Không có GPU thì đổi encoder trong `composite.py`/`build.py` sang libx264.

## Quy trình

Làm đúng thứ tự. Bước 4 luôn dừng chờ user duyệt.

### 1. Hỏi đầu vào (gom 1 lượt)

- Đường dẫn video.
- Style: cơ bản hay nâng cao.
- Tên video.

Tìm trong Obsidian outline/script/slide của video trước, để lấy số liệu thật cho banner. Tìm luôn asset có sẵn: ảnh trong slide Excalidraw, file `.glb` trong project liên quan. Không hỏi lại thứ đã tìm được.

### 2. Dựng project + transcript

```bash
SKILL=~/.claude/skills/edit-long
cp -r "$SKILL/template" "projects/<slug>"; cd "projects/<slug>"
# sửa project.json: id, name, style
PYTHONUTF8=1 python scripts/prepare.py "<video>"     # probe, chỉ re-encode khi VFR/HEVC/lệch size, speech.wav, review/source-grid.jpg
PYTHONUTF8=1 python scripts/setup_assets.py          # fonts, GSAP, Three.js + Draco (CDN free, 1 lần)
PYTHONUTF8=1 python scripts/transcribe.py            # chạy bằng Bash run_in_background; 12 phút audio mất khoảng 8 phút CPU
```

- Đọc `review/source-grid.jpg` để xác định layout, ghi vào `edit-plan.json` → `layout`:
  - `face`: khung webcam `[x0,y0,x1,y1]`. Overlay góc không được đè vùng này.
  - `clip_crop`: vùng nội dung `[x,y,w,h]`, bỏ thanh trình duyệt, taskbar và webcam. Áp cho clip B-roll và ảnh `src:`.
- Cần đo chính xác thì crop 1 khung full-res kèm `drawgrid`.
- Đọc `assets/transcript.txt`. Thuật ngữ nhận sai (Three.js thành "3JS") chỉ cần nhớ khi viết chữ. Không thêm `hotwords`, vì whisper sẽ diễn đạt lại câu.

### 3. Viết edit-plan.json

1. Chia section theo transcript. Câu chuyển phần thường là "đầu tiên", "ví dụ thứ hai", "cái cuối cùng".
2. Đọc style guide trước khi viết:
   - `references/style.md` (style chuẩn, mặc định). `style-basic.md` và `style-advanced.md` chỉ là ghi chép nghiên cứu Ben AI / Liam Ottley;
   - xem 5-10 ảnh trong `references/screenshots/<kênh>/`;
   - schema ở `references/edit-plan.md`, component và props ở `references/components.md`.
3. Mỗi overlay đặt `at` bằng giây bắt đầu của câu nói tương ứng (lấy từ transcript), ghi câu đó vào `say`.
4. **Không bịa số.** Chỉ dùng số có trong transcript, outline hoặc slide.
5. Chữ tiếng Việt có dấu. Đánh dấu chữ nhấn bằng `*chữ*` (màu plum).
6. Trích khung nguồn mỗi 10 giây thành contact sheet để chọn đoạn B-roll đẹp (`src`) và kiểm tra khung nào là slide, khung nào là demo.
7. **Slide B-roll `sl-*`: chỉ dùng chất liệu thật**, không vẽ placeholder (user chê "giả quá"). Với mỗi slide, ghi rõ từng prop lấy từ đâu:
   - khung hình, clip: `src:<giây>`, `<file video>@<giây>`, `vclip`;
   - dữ liệu thật: transcript, `cuts.json`, `edit-plan.json`, log, `chapters.txt`;
   - trang thật: `shot:<file html hoặc url>`;
   - overlay đã render có alpha: trích từ `cache/<id>.<hash>.mkv` bằng ffmpeg (`select=eq(n\,N)`, `-pix_fmt rgba`).

   Ví dụ đã được duyệt: `references/slides-example.py` (script lấy dữ liệu) và `references/slides-example.json` (plan nó sinh ra).
8. **Đoạn mặt người nói** (talking head): dùng các type `th-*` (luật trong `references/style.md`, props trong `components.md`, ví dụ `references/talking-example.py`).
   - `layout.face` chỉ khoanh vùng đầu.
   - Tìm chất liệu trong máy trước: bản quay màn hình và video portfolio cùng thư mục với video, thumbnail kênh (`2 MARKETING & SALE/YOUTUBE/thumbnail/`). Bảng props đầy đủ ở `references/components.md`. Chủ đề không khớp slide nào thì viết builder mới trong `slides.py` bằng kit sẵn có (`chrome`, `term`, `ui`, `cursor`, `tile3d`, `mascot`, MacBook GLB).

### 4. Ảnh mẫu duyệt (DỪNG)

```bash
PYTHONUTF8=1 python scripts/build.py     # dừng nếu trùng chỗ, sai tên SFX; cảnh báo khoảng trống >15s ở style nâng cao
PYTHONUTF8=1 python scripts/preview.py   # review/index.html, review/contact-*.jpg, review/preview-qa.json
```

- Yêu cầu trước khi gửi user:
  - `with_problems: 0` (không lỗi JS, không fallback font, không tràn mép, không đè webcam);
  - `build.py` không còn cảnh báo khoảng trống.
- Tự mở **mọi** contact sheet và soi bằng mắt:
  - chữ rớt 1 từ xuống dòng;
  - overlay đè chữ của slide gốc;
  - 3D đè tiêu đề;
  - ảnh còn dính webcam.

  Sửa xong chạy lại `preview.py <id...>` cho những cái đã sửa.
- Gửi user đường dẫn `review/index.html`, rồi **dừng**. Sửa theo góp ý (theo mã `ov-NNN`), lặp tới khi user nói duyệt.
- Muốn user xem chuyển động của từng slide (không ghép full video): render riêng các overlay đó (`render_overlays.py ov-…`), chạy `sound_mix.py`, rồi `clips.py ov-…`. Lệnh này xuất mỗi overlay 1 clip có SFX vào `review/clips/`, gallery tự đổi ảnh thành player.

### 5. Render (sau khi duyệt)

```bash
PYTHONUTF8=1 python scripts/render_overlays.py   # run_in_background; overlay góc ~15-30s, toàn khung ~70-110s, slide sl-* 60-170s mỗi cái (20 overlay: ~17 phút)
PYTHONUTF8=1 python scripts/sound_mix.py         # assets/sfx-bed.wav từ cue trong overlays.json
PYTHONUTF8=1 python scripts/composite.py --range 0,60   # nháp 1 đoạn, xem trước khi chạy full
PYTHONUTF8=1 python scripts/composite.py          # renders/final.mp4
PYTHONUTF8=1 python scripts/final_qa.py           # exit 1 nếu lệch khung, lệch tiếng >40ms, khung hero khác ảnh đã duyệt
```

Mở `renders/frames/FINAL-heroes-*.jpg` xem lại. Báo user kèm đường dẫn `final.mp4`, nội dung `chapters.txt` và số liệu QA.

## Luật kỹ thuật (đã gặp lỗi thật)

| Luật | Lý do |
|---|---|
| Không `hotwords`/`initial_prompt` khi transcribe | Whisper diễn đạt lại câu ("mình" thành "tôi"), có lúc sinh chữ Trung |
| Root composition không có `data-start`; `<video>` nằm trong wrapper không có `data-start` | Lint HyperFrames chặn video lồng trong phần tử có thời gian |
| Overlay toàn khung không fade, đục từ frame 0 | Lưu H.264 không có alpha. Fade sẽ thành khung đen |
| Không tween `className` | GSAP 3 bỏ tính năng này; dùng `opacity` của phần tử con |
| Số đếm: tween `innerText` + `modifiers` + `tl.set` giá trị cuối | `onUpdate` không chạy khi seek |
| `wait_for_function` trả boolean (`!!window.__timelines[id]`) | Trả object GSAP thì Playwright treo |
| Preview tự tạo `window.__timelines` | Ngoài runtime HyperFrames thì registry chưa có |
| QA so khung hero: ngưỡng 12 cho B-roll, 4 cho overlay khác | Khung video giải mã trong Chrome và ffmpeg lệch màu nhẹ |
| Video quay slide (Excalidraw) đã có sẵn tiêu đề phần | Banner góc sẽ đè chữ. Dùng `chapter` toàn khung |
| Overlay chữ (keyword, lower-third, chips) để `pos: bottom` (giữa phía dưới), không xếp 2 cái cùng lúc | User muốn vậy. `build.py` báo lỗi khi 2 overlay cùng `pos` cùng lúc |
| Slide có chữ ở giữa dưới thì dời overlay chữ sang lúc màn hình chuyển sang demo, hoặc báo user | Ở giữa dưới, overlay sẽ đè dòng chú thích của slide |
| Job dài chạy bằng Bash `run_in_background` | `Start-Process` làm mất log và exit code |
| `data-duration` không được làm tròn lên (`build.dur()`) | HyperFrames render `ceil(D*fps)` khung: 191/30 ghi thành 6.3667 sẽ ra 192 khung và `render_overlays.py` dừng |
| Server của `preview.py` phải trả byte range (206) | Không có range thì Chrome không tua được `<video>`, ảnh mẫu luôn hiện khung đầu |
| Preview vẽ khung video đã tua vào 1 `<img>` cạnh video (giống HyperFrames) | `<video>` nằm trong lớp xoay 3D bị chụp ra khung cũ |
| Ô chat, con trỏ đặt trên cửa sổ đang xoay 3D thì để ngoài `.scene` | Trong `.scene` (preserve-3d), 2 mặt phẳng cắt nhau thành đường chéo |
| `render_overlays.py` tự thử lại 3 lần | Windows đôi lúc khoá thư mục PNG vừa ghi, HyperFrames báo `EPERM ... rename` |
| MacBook GLB: không xoay π, thay vật liệu `screen.001` bằng màu đen | Mặt trước model nhìn về +Z; vật liệu màn hình có sẵn ảnh desktop sẽ lộ ra quanh màn CSS3D |
| Chỉnh da chỉ bằng `beauty.py` (skill youtube, `template/cut/scripts/beauty.py`), không tự viết bản khác | Bản OpenCV tự viết ngày 14/10/2026 bị chê. Bản MediaPipe của Content Agent được user test và chốt ngày 21/10/2026 |
| QA so khung hero: transition ngưỡng 20, template `th-*` toàn khung ngưỡng 12 | Film burn chớp đổi mỗi khung; cột/tường thumbnail chạy liên tục nên lệch vài px giữa preview và render |

## Cập nhật tham chiếu

Lấy 5 video mới nhất của 1 kênh rồi trích khung + contact sheet + số lần cắt/phút:

```bash
yt-dlp --flat-playlist --playlist-end 5 --print id "https://www.youtube.com/@<kênh>/videos"
yt-dlp -f "136/bv*[height<=720]" -o "<kênh>-%(id)s.%(ext)s" <ids...>         # tải về scratchpad, không để trong skill
python -I "$SKILL/tools/ref_frames.py" <out_dir> <video...>
```

Đọc các sheet, cập nhật `references/style-*.md`, chép ảnh tiêu biểu vào `references/screenshots/<kênh>/`.
