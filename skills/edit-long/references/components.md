# Components

Code ở `template/scripts/components.py`. Chữ nhấn viết `*chữ*`.

**Overlay chữ mặc định đặt ở giữa phía dưới** (`pos: bottom`, mép dưới ở y 910, nằm trên thanh UI của app và taskbar). User muốn như vậy. Chỉ đổi `pos` khi user yêu cầu. Các giá trị khác:
- `right`, `left`, `center`, `top`;
- `top-right`, `top-left`, `bottom-right`.

Nếu thư viện không có visual cần dùng, thêm 1 hàm builder mới vào `components.py` (trả về `html`, `css`, `js`, `enter`, `exit`, `hero`, `sfx`, `full`) và đăng ký trong `BUILDERS`. Muốn dùng Three.js thì trả thêm `module`.

## Overlay góc (đè lên video, nền trong suốt)

| type | props | Dùng khi | Mặc định SFX |
|---|---|---|---|
| `keyword` | `text`, `pos` (mặc định `bottom`), `sub?`, `logo?`, `size?` | 2-5 chữ chốt ý câu đang nói. Text dài tự thu cỡ, không xuống dòng | pop |
| `lower-third` | `name`, `desc`, `logo?`, `pos` (mặc định `bottom`) | Lần đầu nhắc tên tool, model, link | pop |
| `chips` | `items[]`, `times[]?` (giây tương đối, khớp lúc nói), `pos`: `bottom` (mặc định), `top`, `center` | Liệt kê 2-4 ý, mỗi pill hiện đúng lúc nói | click-soft mỗi pill |
| `banner` | `n`, `title`, `meta[]`, `pos` | Banner góc (dùng khi nguồn là talking head, không có slide) | whoosh-short, pop |
| `section-chip` | `n`, `title`, `pos` (mặc định `top-right`) | Nâng cao: nhãn section suốt section | click-soft |

## Toàn khung (cắt cứng, che video, giọng vẫn chạy)

| type | props | Dùng khi | Mặc định SFX |
|---|---|---|---|
| `chapter` | `n`, `total`, `title`, `meta[]`, `parts[]`, `img?` | Cơ bản: mở đầu mỗi section, 3 giây | whoosh, pop |
| `broll` | `label`, `eyebrow?`, `sub?`, `badge?` + `clip` | Intro cơ bản: clip tua nhanh trong card bên phải, nhãn bên trái | whoosh-short |
| `broll-full` | `label?` + `clip` | Intro nâng cao: clip tua nhanh toàn khung + pill nhãn | whoosh-short |
| `stat` | `value`, `from?`, `decimals?`, `prefix?`, `suffix?`, `label`, `note?`, `title?` | 1 con số có trong transcript/outline | whoosh, sparkle |
| `tiles` | `title`, `items[{name, logo?, hot?}]`, `center?{name, logo?}` | Bộ tool, các nguồn, các ý tưởng | whoosh, pop |
| `flow` | `title`, `steps[{t, s?, img?, logo?, hot?}]`, `gap?` | Quy trình 3-5 bước, có chấm chạy | whoosh, pop mỗi bước |
| `compare` | `title`, `left{img,label}`, `right{img,label}`, `mid` (`→`, `+`, `vs`) | Trước/sau, thật/3D, 2 phương án | whoosh, pop |
| `image` | `img`, `title?`, `caption?` | 1 ảnh lớn (bảng, screenshot) có Ken Burns nhẹ | whoosh |
| `journey` | `title`, `items[]`, `current` | Nâng cao: bản đồ section lặp lại, nút hiện tại sáng | riser (trước 0.8s), whoosh, sparkle |
| `units` | `title`, `groups[{n, label, color}]`, `cols?` | Đếm theo đơn vị (34 món: 32 code, 1 AI, 1 Poly Haven) | whoosh, typing, sparkle |
| `three` | `mode`: `model` hoặc `orb`, `model` (.glb, hỗ trợ Draco), `title`, `caption?`, `spin`, `scale`, `swatches[{name,hex}]?`, `swatch_step?`, `labels[]?`+`current?` (orb) | Vật thể 3D xoay trên đế: xe, đồ nội thất, model AI | riser, whoosh-cinematic |

## Slide giữa phần (`slides.py`, toàn khung, 5-6 giây, ít chữ)

**Luật: chỉ dùng chất liệu thật** (user chê bản vẽ placeholder là "giả quá", 13/10/2026). Không vẽ thanh xám, chấm màu, khung trống giả UI. Mỗi slide lấy:
- khung hình, clip thật của chính video (`src:<giây>`, `<file video>@<giây>`, `ctx['vclip']`);
- dữ liệu thật của pipeline: transcript, `cuts.json`, `edit-plan.json`, log render, ảnh mẫu đã duyệt, gallery `review/index.html` (`shot:`);
- khung app dựng đúng như thật: Chrome, VS Code, terminal Claude Code, YouTube, dùng icon thật (Material Symbols `m-*`, codicons `c-*` trong `assets/ui/icons/`), font Inter (UI) và Roboto (YouTube), con trỏ macOS (`assets/ui/cursor.svg`, `hand.svg`);
- vật thể 3D thật: MacBook GLB (`assets/models/macbook.glb`, pmndrs examples, MIT), tile logo 3D và mascot Claude Code.

Mọi slide nhận `title` (ngắn, có `*nhấn*`). Ảnh nhận mọi dạng của `img()`: `src:12.5`, `D:/…/raw.mp4@44`, `shot:D:/…/index.html`, đường dẫn ảnh.

| type | Hình | props |
|---|---|---|
| `sl-system` | 4 cửa sổ nhỏ chứa ảnh thật của từng bước, tile icon 3D góc, mascot nhảy qua, đường nối sáng dần | `steps[{label, img, icon, progress?}]` (icon: scissors, layers, wand, play) |
| `sl-cut` | Timeline NLE tối: dải khung hình thật, waveform thật, chữ từng câu; thanh quét đi qua, chỗ cắt đỏ lên rồi bị rút ra, phần sau dồn lại | `file` (video raw), `a`, `b` (cửa sổ giây), `cuts[[start, end, nhãn]]`, `words[[start, end, chữ]]`, `clip_name`, `caption` |
| `sl-transcript` | VS Code mở `utterances.txt` thật, vệt đọc chạy xuống, dòng vấp đỏ + gạch rồi co lại, thẻ lý do của Claude | `lines[[id, start, end, gap, chữ]]`, `first_line`, `strike[ids]`, `reason`, `file`, `crumb`, `project` |
| `sl-stack` | Exploded view: khung video thật, lớp overlay thật (PNG alpha), code thật của overlay; tách lớp rồi gộp thành khung final | `base` (ảnh khung), `layer` (PNG alpha, lấy từ `cache/*.mkv` của bản đã render), `code[]`, `file`, `labels[3]` |
| `sl-fan` | 5 khung component đã render xoè ra 3D, chip tên loại | `cards[{img, label}]` |
| `sl-edit` | MacBook 3D (GLB) mở nắp, màn hình (CSS3D) chạy editor: `edit-plan.json` gõ dần, preview đổi theo, block hiện trên timeline; tile Claude, ChatGPT hai bên | `json[[dòng, block]]`, `blocks[{label, at, img, color}]`, `base`, `strip[]`, `wave_file`, `duration`, `left/right`, `camY/camZ/lookY/py/open/rx` |
| `sl-terminal` | Terminal Claude Code thật (khung chào, prompt gõ, `● Tool(...)` + `⎿ kết quả`), mascot ngồi trên nóc | `prompt`, `steps[[tool/say, chữ, kết quả]]`, `cwd`, `thinking`, `bar` |
| `sl-approve` | Chrome mở gallery ảnh mẫu thật, trang cuộn, con trỏ đi qua, ô Claude Code gõ "duyệt", tick xanh lần lượt | `page` (file gallery), `url`, `tab`, `reply`, `done`, `sel` |
| `sl-render` | Terminal chạy log render thật, khung thật của bản final bay ra xếp lưới, rồi player phát bản final | `log[[cmd/out/bar/ok, chữ]]`, `frames[]`, `clip[file, giây]`, `name` |
| `sl-publish` | Trang xem YouTube (Chrome) phát clip final thật, chương thật từ `chapters.txt`, avatar thật, con trỏ bấm Đăng ký, tile YouTube 3D | `clip[file, giây]`, `video_title`, `channel`, `avatar`, `chapters[[mm:ss, tên, ảnh]]`, `time`, `now`, `progress` |

Kit dùng chung để viết slide mới:
- khung app: `chrome(id, x, y, w, h, url, inner, tab)`, `term(id, x, y, w, h, title, inner)`, `TL3` (3 đèn macOS), `ui(tên, cỡ, màu)` icon thật, `cursor(id, x, y)`;
- `tile3d(id, x, y, size, inner)`: tile logo đùn lớp CSS 3D; `mascot(id, x, y, scale)`: mascot Claude Code, chân đặt tại (x, y);
- `logo(ctx, slug, màu)`, `icon(tên)`, `shadow()`, `hl_code()`, `hl_json()` (tô màu code kiểu VS Code Dark+);
- tween: `win_in`, `enter3d`, `drift`, `floaty`, `pop`, `show`, `hop`, `typed`;
- `ctx`: `img(spec, w)`, `shot(page, w, h, sel)` (trả cả toạ độ phần tử), `wave(file, a, b, n)`, `vclip(file, giây)`, `model(glb)`.

Lưu ý kỹ thuật:
- Phần tử phẳng đặt trên cửa sổ đang xoay 3D (ô chat, con trỏ) phải nằm NGOÀI `.scene`, không thì 2 mặt phẳng cắt nhau.
- `<video>` trong slide phải là con trực tiếp của 1 khối `position:absolute` (HyperFrames chèn `<img>` khung hình ngay cạnh video).
- MacBook GLB: mặt trước nhìn về +Z, không xoay π. Vật liệu `screen.001` có sẵn ảnh desktop, phải thay bằng màu đen.

## Talking head (`talking.py`, kiểu Ben AI, cho đoạn người nói nhìn thẳng camera)

Dùng khi video là mặt người nói (không quay màn hình). Loại toàn khung nhúng chính đoạn video gốc của giây đó (khớp từng khung, tiếng gốc vẫn chạy bên dưới), cho khung hình trượt sang 1 bên, làm mờ + phủ đen, rồi trả về y như cũ ở khung cuối nên lúc cắt vào/ra không thấy vết. Loại chữ là overlay trong suốt.

| type | Hình | props |
|---|---|---|
| `th-text` | Chữ lớn 2 dòng 1 bên, khung hình nhích mặt sang bên NGƯỢC LẠI 300 px, chữ giữ chỗ cũ (x 1200 / 110), lớp gradient tối kéo từ phía chữ tới sát mặt; có thể kèm 1 hoặc 1 hàng tile logo 3D phía trên | `text`, `sub`, `side` (right/left), `logo` + `logo_color` hoặc `logos[[slug, màu]]` |
| `th-center` | Chữ giữa, ngay dưới cằm, hiện như gõ; lớp đen mờ dần ở đáy khung, mặt và 2 bên giữ nguyên | `text`, `sub`, `logos[[slug, màu]]` (tile nhỏ trước chữ), `top` (px, mặc định 800) |
| `th-chips` | Các pill chạy từ phải vào nối đuôi ở 1/3 dưới, có motion blur | `items[]` (chữ nhấn `*...*` thành pill tím) |
| `th-lower` | Tên + vai trò góc dưới trái | `name`, `role` |
| `th-side` | Khung hình trượt trái (hoặc phải), mép mờ dần vào nền tối mờ; bên trống hiện card ảnh thật hoặc clip tua nhanh + chú thích | `img` hoặc `clip[file, giây, tốc độ]`, `badge`, `text`, `sub`, `side` |
| `th-blurcard` | Lớp mờ + đen phủ lên, chữ bên trái, card clip nguồn tua nhanh bên phải | `text`, `sub`, `clip[file, giây, tốc độ]`, `badge` |
| `th-pip` | Mặt thu nhỏ về góc (PiP) trong khi clip nguồn tua nhanh chiếm toàn khung, rồi phóng lại | `clip[file, giây, tốc độ]`, `label`, `corner` (bl: che luôn webcam có sẵn trong bản quay màn hình) |
| `th-wall` | Tường thumbnail/khung hình thật nghiêng, các hàng chạy ngược chiều, pill tiêu đề giữa | `imgs[]`, `text`, `tilt` |
| `th-column` | Khung hình trượt trái, bên phải 2 cột thumbnail nghiêng chạy dọc ngược chiều | `imgs[]`, `text`, `sub` |
| `th-page` | Ảnh chụp trang thật nghiêng 3D, zoom chậm, pill tiêu đề dưới | `img`, `text`, `zoom` |
| `th-row` | Lớp mờ đen, tile logo 3D giữa, 1 hàng card ảnh thật nhô lên, 1 dòng chữ dưới | `cards[{img, label}]`, `logo`, `text` |

Chất liệu: tìm trong máy trước khi làm. Thường có sẵn:
- bản quay màn hình và video portfolio cùng thư mục với video;
- thumbnail kênh ở `2 MARKETING & SALE/YOUTUBE/thumbnail/`;
- khung hình của các video đã edit.

Ví dụ đã chạy: `references/talking-example.py` → `talking-example.json` (video intro Upwork).

Lưu ý:
- `layout.face` của talking head chỉ khoanh đầu (vd `[740,140,1180,600]`), không cả người. Chữ được phép nằm ngang vai.
- Nền chữ tối: chữ trắng, nhấn màu `#A99BFF`. Video sáng (phòng màu be) phải có lớp gradient tối bên chữ, không thì chữ trắng không đọc được.
- Lớp nền trang trí phủ toàn khung gắn class `deco` để preview không báo tràn mép.

## Logo

`logo` là slug của simple-icons (`claude`, `threedotjs`, `blender`, `vercel`, `mercedes`, `googlechrome`...). Logo được tải lúc build và cache ở `assets/logos/`. Không có slug thì hiện ô chữ cái đầu. Cũng có thể truyền đường dẫn file `.svg`/`.png`.

## Màu `units`

Dùng token: `lav`, `plum`, `sage`, `sky`, `peach`, `gold`.
