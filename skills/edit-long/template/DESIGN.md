# DESIGN: light luxe, video ngang 1920x1080

Token màu và font nằm ở khối `TOKENS` đầu `scripts/components.py`. Đổi brand thì sửa ở đó.

## Palette
- Nền canvas: ivory `#FAF6EF`, có quầng lavender `#B7A8FF`, sky `#9AD0FF`, peach `#FFB39C` mờ và lưới chấm 30px.
- Thẻ: trắng 97% (`.card`) hoặc trắng 78% (`.glass`), viền `rgba(23,19,13,.09)`, bóng mềm. Trên nền màn hình sáng, chữ luôn nằm trong thẻ.
- Chữ: ink `#17130D`, chữ phụ `#4A4339`.
- Nhấn: plum `#4A3AE0`, dùng cho chữ `*nhấn*`, số đếm, nút hiện tại.
- Pastel chỉ dùng cho mặt thẻ và ô màu, không dùng làm màu chữ.

## Chữ
- Bricolage Grotesque 800 (`display.ttf`): tiêu đề, số, keyword.
- Be Vietnam Pro 500/700 (`body.ttf`, `body-bold.ttf`): nhãn, mô tả.
- Đều có đủ dấu tiếng Việt.
- Cỡ chữ:

  | Thành phần | Cỡ |
  |---|---|
  | Keyword | 46-62px, tự thu khi dài |
  | Tiêu đề toàn khung | 58px |
  | Chapter | 70-98px |
  | Số stat | 250px |
  | Nhãn | 22-30px |

## Bố cục
- Lề an toàn 24px. Overlay góc cách mép 72-120px.
- Không đè webcam (`layout.face`) và không đè chữ của slide gốc.
- Overlay chữ (keyword, lower-third, chips) đặt ở giữa phía dưới: căn giữa ngang, mép dưới ở y 910, nằm trên thanh UI của app và taskbar. 2 overlay chữ không hiện cùng lúc.
- Chip section (style nâng cao) giữ ở `top-right`.

## Chuyển động
- Một timeline GSAP paused cho mỗi composition. Vào bằng `fromTo`.
- Overlay góc fade ra 0.22-0.3 giây.
- Toàn khung cắt cứng vào và ra.
- Ease: power3.out; back.out(1.6-1.8) chỉ dùng cho ô, icon, pill.
- Không dùng `repeat:-1`, `Math.random`, đồng hồ, `onUpdate`, tween `className`.
