# Style cơ bản (học Ben AI)

Nguồn: 5 video mới nhất kênh Ben AI (253K sub), tải 12/10/2026. Ảnh ở `screenshots/ben-ai/` (không đưa lên repo vì là khung hình kênh khác, tải lại bằng `tools/ref_frames.py`), contact sheet ở `screenshots/ben-ai/sheets/`, số đo ở `screenshots/stats.json`.

## Số đo
- Cắt cảnh: 1.3 đến 3.1 lần/phút, trung vị 2.0. Phần thân video gần như là 1 cảnh quay màn hình dài.
- 60 giây đầu: 1 đến 15 lần cắt. 3/5 video dồn chữ và B-roll dày ở 30 giây đầu, sau đó thưa hẳn.
- Phần thân: khoảng 1 overlay mỗi 1 đến 2 phút.

## Intro (đoạn hook, khoảng 30 giây đầu)
- **Chữ keyword** (`01`, `02`, `05`): 2 đến 4 chữ, chữ đậm, 1 chữ đổi màu nhấn. Đổi mỗi 1 đến 2 giây theo lời nói. Cỡ khoảng 5% chiều cao khung (56 đến 64px ở 1080p). Đặt bên cạnh người nói, không đè mặt.
- **Card B-roll có nhãn** (`03`, `07`, `09`): clip màn hình trong 1 card nổi chiếm 45 đến 50% chiều ngang, nằm bên phải, bo góc, có bóng. Nhãn 2 đến 4 chữ nằm bên trái, căn giữa theo chiều dọc. Nền phía sau là màu trơn của kênh.
- **Hàng pill** (`06`): các bước hoặc tính năng dạng pill màu nhấn, trượt ngang ở 1/4 dưới khung.
- **Logo tool** (`02`, `08`): ô icon khoảng 90px bật lên cạnh chữ keyword, hoặc wordmark lớn.
- **Câu khẳng định** (`04`): 1 dòng chữ đè lên card ảnh chụp sản phẩm.

## Phần thân
- Quay màn hình là chính, webcam PiP bo góc ở 1 góc (`11`).
- **Đổi section** (`12`, `13`): khi sang use case mới hiện 1 dải trắng "Use case: ..." ở mép trên kèm bảng kết quả (tốc độ, chi phí, chất lượng). Đây là mẫu cho banner section.
- **Infographic** (`14`, `15`): bảng hoặc dải highlight xanh/hồng khi giải thích một framework. Chỉ dùng khi lời nói đang liệt kê.

## Chuyển động và âm thanh
- Vào bằng fade + trượt 8 đến 12px, 0.25 đến 0.35 giây. Ra bằng fade. Không có chuyển cảnh phức tạp.
- Ảnh không đo được âm thanh. Mặc định: whoosh-short khi card B-roll vào, pop nhẹ khi banner vào, click-soft cho từng pill. Gain từ -16 đến -20 dB.

## Áp vào video của mình (light luxe)
- Nền card B-roll: ivory `#FAF6EF`, card trắng có bóng, chữ ink `#17130D`, chữ nhấn plum `#4A3AE0`.
- Video nguồn thường là quay màn hình nền sáng + webcam nhỏ góc dưới trái. Overlay chữ đặt ở **giữa phía dưới** (user chốt ngày 12/10/2026), không bao giờ đè vùng webcam (đọc vị trí từ `review/source-grid.jpg`, ghi vào `layout.face`).
- Trên nền màn hình sáng, mọi chữ phải nằm trong card hoặc pill có nền, không đặt chữ trơn.
- Mật độ: intro 4 đến 6 overlay trong 30 giây, phần thân 1 banner mỗi section lớn + 1 callout mỗi 1 đến 2 phút.
