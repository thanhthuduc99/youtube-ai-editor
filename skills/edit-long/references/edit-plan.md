# edit-plan.json

Claude viết file này từ transcript. `build.py` đọc nó. Mọi thời gian tính bằng giây trên video gốc, được snap về khung 30fps.

```json
{
  "style": "basic | advanced",
  "layout": {
    "face": [34, 858, 322, 1022],
    "clip_crop": [330, 86, 1590, 894]
  },
  "sections": [{"n": 1, "title": "Bản vẽ thành 3D", "start": 33.72, "chapter": "tên chương YouTube (tuỳ chọn)"}],
  "overlays": [
    {"type": "keyword", "at": 27.62, "dur": 5.6, "say": "câu nói tương ứng",
     "props": {"text": "Bước sai, bước sửa, *bước đúng*", "pos": "right"},
     "sfx": [{"name": "pop", "at": 0, "gain": -18}],
     "hold": true,
     "id": "ov-005"}
  ],
  "zooms": [{"at": 41.32, "dur": 3.6, "scale": 1.35, "cx": 0.26, "cy": 0.45}]
}
```

- **`layout.face`**: khung webcam theo pixel 1920x1080. Overlay góc chạm vùng này thì `preview.py` báo `covers-webcam`.
- **`layout.clip_crop`**: `[x, y, w, h]`, vùng nội dung sạch, áp cho clip B-roll và ảnh `src:`. Bỏ trống thì dùng cả khung.
- **`sections`**: sinh `chapters.txt` và nhóm ảnh trong gallery.
- **`overlays[].type`**: một loại trong `components.md`.
- **`overlays[].at`, `dur`**: thời điểm bắt đầu trên video gốc và thời lượng hiển thị.
- **`overlays[].clip`**: chỉ dùng cho `broll` và `broll-full`. Dạng `{"src": giây_nguồn, "speed": 3, "crop": [x,y,w,h]}`. `build.py` cắt đoạn `src` tới `src + dur*speed` rồi tua nhanh.
- **`overlays[].sfx`**: bỏ trống thì dùng SFX mặc định của component, `[]` thì tắt. `at` tính tương đối so với overlay, được phép âm (riser vào trước).
- **`overlays[].hold`**: mặc định `true`. Overlay góc dài hơn đoạn vào + ra + 1.5 giây chỉ render đoạn vào/ra, phần giữa lặp khung đứng yên. Đặt `false` khi overlay có chuyển động liên tục suốt thời lượng.
- **`overlays[].id`**: tự đặt `ov-NNN` theo thứ tự. Gallery và góp ý của user dùng mã này.
- **`zooms`**: punch-in cắt cứng vào video gốc. `cx`, `cy` là tâm vùng phóng (0..1).
- **`transitions`**: `[{"at": 57.49, "kind": "filmburn-01", "gain": -6}]`. Film burn đè lên 1 jump cut mặt → mặt. Khung sáng nhất rơi đúng `at`, tiếng của transition đi kèm.
  - Clip nằm ở `assets/transitions/<kind>.mp4`, chỉnh trên nền đen. File `.json` cùng tên ghi `peak` (giây của khung sáng nhất) và `sfx`.
  - `build.py` đổi clip thành lớp alpha (alpha = kênh sáng nhất, gần giống blend screen), lưu thẳng vào `cache/tr-NN.*.mkv`.
- **`switch_sfx`**: `{"name": "mouse-click", "gain": 0}`. Tiếng phát ở đầu mọi overlay thay mặt bằng B-roll, gồm overlay toàn khung trừ `th-side`, `th-column` và loại chữ. Tiếng này thay tiếng whoosh mặc định của overlay đó.
- **SFX riêng của project**: file trong `assets/sfx/<tên>.wav|mp3` dùng được ngay bằng tên. Có sẵn `mouse-click` (tiếng click của user) và `filmburn-01`. Tên tìm ở đây trước, rồi mới tới thư viện chung.

## Ảnh

`props.img` (và `left.img`, `right.img`, `steps[].img`) nhận:
- `"src:450"`: khung của video gốc ở giây 450 (đã áp `clip_crop`);
- đường dẫn file ảnh: được copy vào `assets/img/`.

## Luật mật độ

- **Cơ bản**:
  - intro (đoạn hook trước section 1): 4 đến 6 overlay, chủ yếu `broll` + 1 `keyword`;
  - mỗi section: 1 `chapter` ở câu mở đầu, rồi khoảng 1 overlay mỗi 1 đến 2 phút (`keyword`, `lower-third`, `chips`).
- **Nâng cao**:
  - mỗi section: `journey` (bản đồ lặp lại, `current` = số thứ tự section, đếm từ 0) dài 3 giây, ngay sau đó là `section-chip` giữ tới hết section;
  - không có khoảng trống quá 15 giây mà không có visual (chip section không tính). `build.py` cảnh báo khi vi phạm;
  - xen kẽ đồ hoạ toàn khung (3-7 giây) với overlay góc và zoom. Không đặt 2 đồ hoạ toàn khung liền nhau quá 2 lần.
- Không đặt 2 overlay cùng `pos` cùng lúc, và không chồng 2 overlay toàn khung. `build.py` dừng khi gặp 1 trong 2 lỗi này.
- SFX cách nhau tối thiểu 0.25 giây. Cue sát hơn bị bỏ và có cảnh báo.
