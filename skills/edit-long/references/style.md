# Style chuẩn (gộp cơ bản + nâng cao, user chốt 12/10/2026)

Mặc định áp cho mọi video, trừ khi user yêu cầu khác. Hai file `style-basic.md` (Ben AI) và `style-advanced.md` (Liam Ottley) là ghi chép nghiên cứu tham chiếu, không phải luật.

## Intro (đoạn hook trước section 1)
- 4 đến 6 card `broll`: clip tua nhanh 2.5-3 lần, cắt từ những đoạn đẹp nhất của chính video, đè lên giọng nói của hook.
- Thêm 1 `keyword` ở cuối hook.

## Body
1. **Chữ** (`keyword`, `chips`, `lower-third`):
   - đặt ở giữa phía dưới (`pos: bottom`);
   - khoảng 1 overlay mỗi 1 đến 2 phút;
   - mỗi overlay 2 đến 5 chữ.
2. **Slide đầu mỗi phần** (`chapter`): 3 giây, toàn khung, có ảnh kết quả của phần đó.
3. **Slide giữa phần** (các type `sl-*` trong `slides.py`):
   - khoảng 2 phút có 1 slide, dài 5-6 giây, toàn khung;
   - dùng vật thể 3D và chuyển động: tile logo 3D (Claude, ChatGPT...), mascot Claude Code, MacBook 3D, terminal, trình duyệt, exploded layers;
   - **chỉ chất liệu thật** (user chê bản vẽ placeholder "giả quá"): khung hình và clip thật của video, file thật (transcript, plan, code, log), ảnh chụp trang thật, khung app đúng như thật với icon thật. Không vẽ thanh xám hay ô màu thay nội dung. Chi tiết ở `components.md`;
   - **ít chữ**: chỉ 1 tiêu đề ngắn và nhãn 1-3 chữ;
   - **không làm màn hình số to** kiểu `stat` (user không thích);
   - chọn slide khớp ý đang nói. Không có slide khớp thì viết builder mới trong `slides.py` theo cùng kit (`tile3d`, `mascot`, `enter3d`, `drift`, `hop`...).

## Đoạn mặt người nói (talking head, kiểu Ben AI)
Video hoặc đoạn mà người nói nhìn thẳng camera dùng các type `th-*` (`talking.py`, bảng props ở `components.md`):
- **Nhịp:** khoảng 10-25 giây có 1 cái, xen kẽ loại chữ (`th-text`, `th-chips`, `th-lower`) với loại toàn khung (`th-side`, `th-blurcard`, `th-pip`, `th-wall`, `th-column`, `th-page`, `th-row`).
- **Chữ và hình hiện 2 bên mặt:**
  - khung hình trượt trái/phải để chừa chỗ;
  - nền là bản mờ + phủ đen của chính cảnh đó;
  - xong thì trả về đúng khung gốc.
- **Hình phải thật:**
  - clip nguồn tua nhanh (bản quay màn hình, video portfolio);
  - ảnh chụp trang thật;
  - thumbnail thật của kênh;
  - khung hình của video đã edit.
- Chữ ở đây được đặt 2 bên mặt, không theo luật "giữa dưới" (user yêu cầu 14/10/2026). Chữ trắng, nhấn `#A99BFF`, luôn có gradient tối phía sau.
- **Mặt luôn né chữ** (user yêu cầu 16/10/2026): hiệu ứng có chữ hoặc hình ở 1 bên thì khung hình trượt mặt sang bên ngược lại (`th-side`, `th-column` 440 px). `th-text` chỉ nhích mặt 300 px, chữ giữ chỗ cũ, lớp đen kéo tới sát mặt để không có khoảng sáng trống giữa mặt và chữ (giống card "Claude Motion" của Ben AI). Chữ đặt giữa thì dùng `th-center`: dưới cằm, lớp đen ở đáy, 2 bên giữ nguyên.
- **Xáo thứ tự** (user yêu cầu 16/10/2026): chọn loại hiệu ứng hơi ngẫu nhiên, không đi theo thứ tự bảng, không lặp trái, phải, trái, phải. Không đặt 2 overlay cùng loại liền nhau, xen loại toàn khung với loại giữ mặt.
- Video ngắn (dưới 1 phút) làm nhịp nhanh: khoảng 3 giây đổi 1 visual. Không dùng `zooms` (user bỏ 16/10/2026: zoom không có hiệu ứng nhìn như lỗi).

## Không dùng (trừ khi user yêu cầu)
- `zooms`.
- `stat`, `units`: màn hình số to.
- `journey`, `section-chip`: kiểu Liam, dày đặc.

## SFX
Chỉ SFX offline, không nhạc nền:
- whoosh khi slide toàn khung vào;
- pop, click khi vật thể xuất hiện;
- sparkle khi kết thúc.
