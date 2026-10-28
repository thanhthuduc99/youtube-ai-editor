# Style nâng cao (học Liam Ottley)

Nguồn: 5 video mới nhất kênh Liam Ottley (859K sub), tải 12/10/2026. Ảnh ở `screenshots/liam-ottley/` (không đưa lên repo vì là khung hình kênh khác, tải lại bằng `tools/ref_frames.py`), contact sheet ở `screenshots/liam-ottley/sheets/`, số đo ở `screenshots/stats.json`.

## Số đo
- Cắt cảnh: 9.5 đến 16.5 lần/phút với video hướng dẫn và case study. Video vlog (nQz6sMBSK4A) lên 30.8.
- Ở video hướng dẫn có quay màn hình (1P5xtV-Kf0o): cứ 15 đến 25 giây có 1 cảnh đồ hoạ toàn khung, xen giữa là quay màn hình và mặt người. Tính cả chip, zoom, logo thì khoảng 6 giây có 1 thay đổi.

## Các loại visual
- **Đồ hoạ toàn khung chèn ngang** (`01`, `02`, `03`, `10`, `16`): thay hình 3 đến 6 giây, giọng vẫn chạy. Nền gradient, các thẻ glass (kính mờ, viền 1px sáng). Gồm:
  - ô logo tool nối nhau bằng đường chấm;
  - sơ đồ trước → sau;
  - lưới icon người xếp thành con số (40%);
  - flow có chấm chạy từ tool sang database;
  - sơ đồ hub (icon xếp vòng quanh 1 lõi).
- **Vật thể 3D** (`05`): quả cầu tối có đế phát sáng, các nhãn "Step 1..8" toả ra xung quanh. Cảnh này lặp lại mỗi khi sang bước mới, bước hiện tại sáng lên.
- **Bản đồ lặp lại** (`13`): 1 sơ đồ "Business Map: Before → After" quay lại nhiều lần trong video, mỗi lần thêm 1 nút. Tạo cảm giác tiến độ.
- **Chip section đánh số** (`06`, `08`): pill glass ở góc trên trái, ví dụ "② The concept", hiện suốt cả section. Dải tiêu đề ở mép trên (`14`) cũng có vai trò như vậy.
- **Lower-third tên** (`11`): tên in hoa đậm + 1 dòng mô tả nhỏ, góc dưới trái.
- **Card glass UI** (`07`, `12`): mockup giao diện (website, lịch) nổi trên gradient.
- **Quay màn hình trên nền gradient** (`04`): màn hình thu nhỏ, card mặt người bo góc ở bên phải.
- **Logo tool đơn** (`09`): 1 pill logo + tên, giữa khung, 1 đến 2 giây, khi nhắc tới tool lần đầu.
- **Cắt cảnh minh hoạ** (`15`, `17`): bảng trắng vẽ tay, ảnh báo chí ghép, B-roll đời thường.

## Chuyển động và âm thanh
- Thẻ glass vào bằng scale 0.92 → 1 + fade, so le 60 đến 120ms. Đường nối vẽ dần. Số đếm chạy lên.
- Đồ hoạ toàn khung vào và ra bằng cắt cứng hoặc blur nhanh.
- Âm thanh mặc định:
  - whoosh khi đồ hoạ toàn khung vào;
  - pop cho từng thẻ hoặc logo;
  - click-soft cho chip;
  - riser 0.8 giây trước cảnh 3D hoặc bản đồ;
  - sparkle khi số đếm dừng.

  Gain từ -14 đến -20 dB, các SFX cách nhau tối thiểu 0.25 giây.

## Áp vào video của mình (light luxe)
- Giữ cấu trúc của Liam, đổi màu:
  - nền gradient tối → ivory `#FAF6EF` có quầng lavender `#B7A8FF` và sky `#9AD0FF` mờ;
  - thẻ glass → trắng 72% có viền `rgba(23,19,13,.08)` và bóng mềm;
  - chữ ink `#17130D`, nhấn plum `#4A3AE0`.
- Vật thể 3D dùng Three.js với vật liệu sáng (ivory, plum, pastel), không dùng đế neon đỏ.
- Mỗi section lớn: chip đánh số suốt section + 1 cảnh bản đồ lặp lại ở đầu section (nút hiện tại sáng lên).
- Mật độ mục tiêu cho video quay màn hình: 1 đồ hoạ toàn khung mỗi 20 đến 40 giây, cộng logo, lower-third, callout và zoom sao cho không có khoảng trống quá 15 giây.
- Overlay chữ (keyword, lower-third, chips) đặt ở **giữa phía dưới** (user chốt ngày 12/10/2026). Chip section giữ ở góc trên phải.
- Webcam của nguồn nằm góc dưới trái: overlay góc không đặt ở đó. Đồ hoạ toàn khung được phép che cả webcam trong 3 đến 6 giây.
