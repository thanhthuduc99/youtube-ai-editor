---
name: youtube
description: Làm trọn 1 video YouTube từ file quay thô. User dán đường dẫn video (1 hoặc nhiều phần), Claude tự cắt vấp (bỏ câu nói hỏng, câu bỏ dở, tiếng đệm, lệnh "Hey Ryan, cắt đoạn này", rút khoảng lặng theo nhịp của user, tăng tốc 1.1x, chỉnh da bằng beauty.py), edit thêm B-roll (kể cả B-roll user ra lệnh ngay lúc quay bằng "Hey Claude, ...") và motion graphics bằng skill edit-long, và tạo thumbnail kiểu Ben AI bằng Codex (mặt thật, logo thật, UI thật). Duyệt 1 lần (bản cắt + ảnh mẫu B-roll + 3 thumbnail) rồi mới render. Dùng khi user nói "youtube", "/youtube", "làm video youtube", "edit video này lên youtube", "cắt vấp + edit + thumbnail", hoặc dán 1 video raw muốn ra bản đăng YouTube.
---

# YouTube: video thô → cắt vấp → B-roll → thumbnail → up YouTube

**Đầu vào:** đường dẫn 1 file raw, hoặc nhiều phần quay nối nhau theo thứ tự.

**Đầu ra** (tất cả nằm trong `projects/<slug>/`):

| File | Nội dung |
|---|---|
| `cut/renders/cut.mp4` + `cut/cut-report.md` | Bản đã cắt vấp, kèm danh sách chỗ cắt |
| `renders/final.mp4` | Bản đăng YouTube: cut + B-roll + chữ + SFX |
| `chapters.txt` | Chương để dán vào mô tả |
| `thumbnail/out/thumbnail-youtube.jpg` | Thumbnail 1280x720, dưới 2 MB |
| Link YouTube (private) | Bước 7, up kèm title, description, thumbnail |
| 5-7 title đề xuất + description (khối đầu cố định + tóm tắt + timestamp) | Gửi trong tin nhắn |

**Chi phí:**
- Miễn phí: whisper, cắt, đồ hoạ và render đều chạy trên máy.
- Thumbnail tốn quota Codex gói trả phí, khoảng 25-45k token mỗi ảnh. Mỗi video làm 3 ảnh.

Skill này gồm 3 phần:
1. **Cắt vấp:** `template/cut/`. Đã test trên video showroom 3D, bắt được 92.5% phần user tự cắt.
2. **Edit:** gọi skill `edit-long`. Đọc `~/.claude/skills/edit-long/SKILL.md` khi tới bước 3.
3. **Thumbnail:** `template/thumbnail/` và `references/thumbnail.md`.

## Quy trình

Bước 1-4 chạy liền, không hỏi. Bước 5 là **điểm dừng duy nhất**.

### 0. Đầu vào
- **Chỉ hỏi nếu thiếu đường dẫn video.**
- Không hỏi tên video: Claude tự đề xuất 5-7 title ở bước 5.
- Tìm thêm trong Obsidian (outline, script, slide) và trong thư mục của video (bản quay màn hình, video portfolio, ảnh). Đây là chất liệu thật cho B-roll và thumbnail.

### 1. Dựng project
```bash
SK=~/.claude/skills; P="projects/<slug>"
cp -r "$SK/edit-long/template" "$P"
cp -r "$SK/youtube/template/cut" "$P/cut"
cp -r "$SK/youtube/template/thumbnail" "$P/thumbnail"
cd "$P"; PYTHONUTF8=1 python scripts/setup_assets.py
```

Nếu video gồm nhiều phần, ghép theo thứ tự trước khi cắt:
- Cùng codec: `ffmpeg -f concat -safe 0 -i list.txt -c copy cut/work/raw.mp4`.
- Khác codec hoặc khác size: bỏ `-c copy`, encode lại bằng `-c:v h264_nvenc -cq 18 -c:a aac`.

### 2. Cắt vấp
```bash
PYTHONUTF8=1 python cut/scripts/analyze.py "<raw.mp4>"     # run_in_background; whisper medium CPU, khoảng 2/3 thời lượng video
```
- Script tách câu theo khoảng lặng thật (RMS + Silero) và gắn chữ whisper vào từng câu.
- Lệnh "Hey Ryan, cắt đoạn này" và lệnh ngắn "cắt", "cắt cắt", "cut" được tách thành dòng `[LỆNH CẮT]`.
- Lệnh "Hey Claude, <yêu cầu edit>" (vd "chèn ảnh chụp trang này", "quay màn hình đoạn này", "thêm B-roll ... vào đây") được tách thành dòng `[LỆNH EDIT]` (user dặn 21/10/2026). Lệnh bị cắt khỏi video và thành note `"kind": "edit"` (luật 8 ở đầu `utterances.txt`).
- Kết quả ghi ra `cut/work/utterances.txt`. **Luật cắt nằm ở đầu file này.**
- Câu user dặn editor (vd "editor che lại... thông tin khách hàng") bị bỏ khỏi video và chép vào `notes` trong `cuts.json`. Phải làm theo từng note:
  - che mờ: xem khung full-res có lưới (`drawgrid`), ghi vùng cần che vào `cut/work/blur.json` (chừa webcam và tiêu đề cột), chạy `python cut/scripts/blur.py --range a,b` để soát, rồi `blur.py` ra `cut-blur.mp4` (dùng file này thay `cut.mp4`). Che theo từng màn hình, đừng sót cột nào (editor từng sót cột Lost);
  - "cắt đoạn X đi" ở cuối video = kết thúc video sau X;
  - `kind: edit` (lệnh "Hey Claude"): ở bước 3 phải có 1 overlay làm ĐÚNG yêu cầu, đặt ở câu `for` (đổi giờ raw sang giờ bản cắt bằng `assets/transcript.json` hoặc `shift_plan.py --from-raw`). Chụp trang thì dùng `shot:<url>`. Quay màn hình thì quay bằng Playwright (`browser_*`, ghi video) hoặc lấy đoạn quay màn hình có sẵn, tua nhanh. B-roll thì dựng slide `sl-*` / `th-*` từ chất liệu thật. Không làm được thì ghi rõ trong tin nhắn duyệt. Tin nhắn duyệt phải liệt kê từng lệnh edit kèm mã `ov-NNN` đã làm cho nó.

**Quyết định cắt:**
- Video dưới 10 phút: tự đọc `utterances.txt`.
- Video dài hơn: giao 1 subagent cho đỡ tốn context. Prompt cho subagent: "đọc hết `cut/work/utterances.txt`, làm đúng luật ở đầu file, ghi `cut/work/cuts.json`, trả về số đoạn bỏ và lý do".
- Chỉ bỏ vấp: câu nói lại, câu bỏ dở, lặp đầu câu, tiếng đệm, lệnh cắt, lệnh edit "Hey Claude". **Không bỏ nội dung vì thấy thừa.** Không chắc thì giữ.

```bash
PYTHONUTF8=1 python cut/scripts/render_cut.py            # khoảng 1 phút; --speed 1.0 nếu không muốn tăng tốc
```
- Script cắt tại khung yên nhất và tăng tốc ×1.1 (đúng như user tự edit).
- Khoảng lặng theo nhịp editor (đo trên video REA 16/10/2026): dưới 0.4s giữ nguyên, dài hơn rút về khoảng 0.26s, chỗ im từ 3s trở lên chỉ giữ khoảng 0.4s. Bản cắt REA ra nhịp gần như trùng editor: trung vị 0.20s, p90 0.40s.
- Đo lại khi có bản editor mới: `align.py` (dò bản Final về raw bằng phổ âm, thử `--speed 1.0` và `1.1`) + `compare2.py` trong `projects/rea-cut-test/`.
- Ra 4 thứ:
  - `cut/renders/cut.mp4`;
  - `cut/cut-report.md`;
  - `assets/transcript.json` + `.txt` đã dời theo thời gian bản cắt;
  - `cut/work/jumps.json`: các jump cut người xem sẽ thấy (chỗ bỏ vấp, hoặc chỗ bỏ từ 2s im lặng trở lên).
- **Kiểm tra:**
  - dòng `WARNING` (đoạn ngay trước lệnh cắt vẫn còn giữ);
  - đọc `cut-report.md`;
  - nghe 2-3 mối nối của chỗ cắt lớn nhất (trích đoạn ±3s bằng ffmpeg).

**Chỉnh da** (user chốt 21/10/2026, bản OpenCV cũ ngày 14/10 bị chê và đã bỏ): `cut/scripts/beauty.py`, MediaPipe FaceLandmarker + OpenCV.
- Thông số mặc định là bộ user chốt: clear 29, smooth 29, blemish 14, facelift 12, even 11, không làm trắng, không đổi tông da. Đừng đổi.
- Cần `mediapipe` và `~/.cache/mediapipe/face_landmarker.task`.
- Chậm, khoảng 10-15 phút cho 1 phút video full khung. Chạy `python cut/scripts/beauty.py in.mp4 out.mp4 --workers 4` bằng run_in_background.
- Talking head thì chạy full khung. Bản quay màn hình chỉ có ô webcam nhỏ: crop riêng ô webcam (phóng to nếu mặt nhỏ), chạy beauty, rồi overlay lại đúng chỗ. Không chạy cả khung 1920x1080.
- Chạy sau `render_cut.py`, trước `prepare.py`. Trích ảnh so trước/sau cho user duyệt.
- **Da trắng K2, chỉ chỉnh da** (user chốt 21/10/2026, mặc định từ nay). Nền, tóc, áo, màu phía sau giữ nguyên như bản beauty thường:
  1. `beauty.py in out-base.mp4` (thông số mặc định);
  2. `beauty.py in out-w.mp4 --whitening 15 --pink 6`, rồi `ffmpeg -i out-w.mp4 -vf "$(cat cut/scripts/k2-look.txt)" out-k2.mp4` (filter Hàn nhẹ);
  3. `python cut/scripts/skin_merge.py out-base.mp4 out-k2.mp4 out.mp4`: lấy vùng da (người theo MediaPipe selfie segmenter × màu da) từ bản K2, còn lại từ base. Cần `~/.cache/mediapipe/selfie_segmenter.tflite`.
  - Bước 1 và 2 phải cắt cùng đoạn, cùng cách (cùng `--ss/--t` hoặc cùng file vào) để khung khớp nhau.
  - Không phủ filter lên cả khung (bản cả khung K1-K3 nền ngả tím, user không muốn).

Chỉnh màu: chỉ làm khi có bản mẫu user tự chỉnh trong CapCut (cùng clip, không cắt, không tăng tốc). `python cut/scripts/fit_grade.py <raw> <capcut>` học ra `cut/work/grade.cube`, áp bằng `-vf lut3d=file=...`. Script báo luôn CapCut có làm mịn da không (LUT không chép được phần đó).

### 3. Edit B-roll (skill `edit-long`)
Làm theo `edit-long/SKILL.md`, từ bước 2 tới bước 4, với 2 chỗ khác:
- Video nguồn là `cut/renders/cut.mp4`: chạy `PYTHONUTF8=1 python scripts/prepare.py cut/renders/cut.mp4`.
- **Bỏ `transcribe.py`**: transcript đã có từ bước 2.

Phần còn lại giữ nguyên:
- Style mặc định theo `edit-long/references/style.md`: chapter card đầu mỗi phần, chữ giữa dưới, slide B-roll `sl-*` khoảng 2 phút 1 cái.
- Đoạn mặt người nói dùng các template `th-*`.
- **Chất liệu phải thật.**

**Làm mượt jump cut** (luật của user), sau khi viết xong plan:
```bash
PYTHONUTF8=1 python cut/scripts/jump_fx.py
```
- Jump cut đã có B-roll che: thêm tiếng `mouse-click` lúc chuyển từ mặt sang B-roll. Luật `switch_sfx` áp cho mọi lần chuyển mặt → B-roll, không riêng chỗ cắt.
- Jump cut mặt → mặt: mặc định KHÔNG thêm gì, script chỉ liệt kê làm ứng viên. User 21/10/2026 chê film burn ở mọi mối cắt ("nhìn kì") và bảo bỏ hết. Chỉ đặt film burn ở vài chỗ thật hợp lý sau khi hỏi user: `jump_fx.py --at 57.5,120.3` (`--burn` = mọi chỗ, cách cũ, đừng dùng).
- Có burn thì script báo overlay nào bắt đầu ngay sau burn. Dời overlay đó ra sau burn ít nhất 0.9s.
- Mỗi lần sửa plan thì chạy lại script. Nó thay transition cũ do chính nó thêm.
- Nên đặt 1 B-roll ngay trên chỗ cắt vấp lớn: che được mối cắt, lại có hình minh hoạ.

Chạy `build.py` → `preview.py`. Chưa render.

### 4. Thumbnail (chạy song song với bước 3)
Đọc `references/thumbnail.md` (luật của user, 5 khuôn bố cục, 15 prompt đã duyệt), rồi:

1. **Chọn 3 hướng khác nhau.** Mỗi hướng gồm khuôn A-E, chữ 2-4 từ IN HOA và 1 màu chủ đạo theo logo của tool chính trong video.
   - Chữ trên thumbnail là cảm xúc hoặc lời hứa, không lặp lại title.
   - Ít nhất 1 mẫu có mặt.
2. **Logo thật:** `python thumbnail/scripts/fetch_logo.py <tên> --term "<app>" --seller "<hãng>"` (hoặc `--wiki`, `--domain`). Mở ảnh ra xem đúng chưa. Logo có sẵn thì dùng luôn.
3. **UI thật:** crop từ khung video (`ffmpeg -ss <t> -i cut/renders/cut.mp4 -frames:v 1`) hoặc từ `review/frames/*-hero.jpg` của bước 3. Lưu vào `thumbnail/assets/ui/`.
4. **Viết prompt:** viết 3 mục `### t1/t2/t3` vào `thumbnail/prompts.md` theo khuôn của các ví dụ, rồi chạy `python thumbnail/scripts/build_prompts.py`.
5. **Tạo ảnh:** chạy `python thumbnail/scripts/gen_thumb.py tN --face ... --asset "vai trò=đường dẫn"` cho cả 3 mẫu, song song, bằng `run_in_background`.
6. **Soát từng ảnh:**
   - mặt giống user;
   - chữ đúng dấu tiếng Việt;
   - logo đúng hình, đúng màu;
   - không có thứ model tự vẽ thêm;
   - góc phải dưới trống.

   Ảnh nào hỏng thì sửa prompt rồi chạy lại riêng ảnh đó.
7. **Gom ảnh:** `python thumbnail/scripts/finalize.py t1 t2 t3` → `thumbnail/out/review.jpg` (có cả bản cỡ điện thoại).

### 5. DỪNG: duyệt 1 lần
Gửi user trong 1 tin nhắn:
- **Bản cắt:** link `cut/renders/cut.mp4`. Ghi raw dài bao nhiêu, ra bao nhiêu, và 3-5 chỗ cắt lớn nhất (giờ ở bản cắt + lý do). Bảng đầy đủ ở `cut/cut-report.md`.
- **B-roll:** link `review/index.html`.
- **Thumbnail:** link `thumbnail/out/review.jpg`, kèm 1 dòng mô tả mỗi mẫu.
- **5-7 title đề xuất để user chọn** (user muốn có nhiều lựa chọn, 21/10/2026), mỗi cái 1 góc khác nhau (kết quả, cách làm, so sánh, tò mò, con số thật):
  - có từ khoá chính;
  - dưới 70 ký tự;
  - bổ sung cho chữ trên thumbnail, không lặp.
- **Description:** khối đầu cố định + tóm tắt + timestamp, theo `references/description.md`.

Sửa theo góp ý:
- **Góp ý về cắt:**
  1. Sửa `cut/work/cuts.json`, chạy lại `render_cut.py`.
  2. Chạy `python cut/scripts/shift_plan.py` để dời mốc giờ trong `edit-plan.json` theo bản cắt mới.
  3. Chạy `prepare.py cut/renders/cut.mp4` → `build.py` → `preview.py`.
- **Góp ý về B-roll:** theo `edit-long`, sửa theo mã `ov-NNN`.
- **Góp ý về thumbnail:** sửa prompt của mẫu đó, chạy lại riêng mẫu đó.

Lặp tới khi user nói "duyệt".

### 6. Sau khi duyệt
- **Video:** chạy bước 5 của `edit-long`:
  1. `render_overlays.py`
  2. `sound_mix.py`
  3. `composite.py`
  4. `final_qa.py`
- **Thumbnail:** `python thumbnail/scripts/finalize.py --pick tN` → `thumbnail/out/thumbnail-youtube.jpg`.
- **Lưu bản giao** (user dặn 16/10/2026). Đặt `<tên>` = tên ngắn + title không dấu, vd `REA - clone moi phan mem`. Tháng lấy theo ngày làm, folder tên dạng `thang 10-2026`, chưa có thì tạo:
  - video: `2 MARKETING & SALE/YOUTUBE/<năm>/thang <M>-<năm>/<tên>/<tên>_final.mp4`. Folder nguồn của video (raw, intro...) chuyển luôn vào `<tên>/`;
  - thumbnail: `2 MARKETING & SALE/YOUTUBE/thumbnail/thang <M>-<năm>/<tên>_thumb.jpg`;
  - sửa `source` trong `project.json` theo đường dẫn mới.
- **Báo user:**
  - đường dẫn video và thumbnail đã lưu;
  - nội dung `chapters.txt`;
  - title đã chốt, hoặc 5-7 title để chọn;
  - description theo `references/description.md` (khối đầu cố định, tóm tắt, timestamp). Up YouTube thì dùng đúng description này;
  - số liệu QA.

### 7. Up YouTube (user dặn 27/10/2026)
Chỉ chạy khi user đã chốt title. Ghi description cuối vào `work/description.txt`, rồi:
```bash
cp ~/.claude/skills/youtube/template/upload_youtube.py work/
PYTHONUTF8=1 python work/upload_youtube.py "<video>_final.mp4" "<title>" work/description.txt --thumb "<tên>_thumb.jpg"   # run_in_background
```
- Mặc định `--privacy private`. User tự bấm công khai trong Studio. Chỉ dùng `unlisted` (gửi khách/nhà tài trợ duyệt) hoặc `public` khi user nói rõ.
- OAuth đọc từ biến môi trường hoặc file `.env` (`YOUTUBE_OAUTH_REFRESH_TOKEN`, `YOUTUBE_OAUTH_CLIENT_ID`, `YOUTUBE_OAUTH_CLIENT_SECRET`; đổi file bằng `YOUTUBE_ENV`), không in ra, không chép key vào script.
- Title tối đa 100 ký tự, description tối đa 5000 byte (script tự kiểm).
- Báo user link `youtu.be/<id>` + link Studio, ghi id vào memory project của video.
- Sửa description sau khi up (thêm link...): sửa `work/description.txt` rồi `python work/update_description.py <id> work/description.txt` (chép từ `template/update_description.py`). Đọc description đang có trên YouTube trước, user có thể đã tự sửa trong Studio.

## Mẹo quay cho user (nhắc khi user hỏi; rút từ 2 lần so với editor, 16/10/2026)
- **Lệnh cắt:** nói "cắt cắt" thành 1 câu riêng, ngừng khoảng 1s trước và sau. Không cần "Hey Ryan". Chỉ nói "cắt" 1 lần dễ lẫn khi nội dung video có chữ "cắt video".
- **Nói lại từ đầu câu,** mở đầu bằng đúng mấy chữ như lần hỏng. AI dựa vào chữ mở đầu để biết phải lùi tới đâu. Nói lại bằng câu khác hẳn thì AI lùi không đủ xa (lỗi "button menu giá" ở video Sonnet vs Opus).
- **Lặng sau lệnh 1-2s là đủ.** Lặng 5s cũng không sao, script tự rút về khoảng 0.4s.
- **Vấp giữa câu, tự sửa số** ("15 đô, 16 đô"), lỡ lặp vài chữ: đừng nói tiếp, nói "cắt cắt" rồi nói lại cả câu. Đây là loại AI hay sót nhất.
- **Dặn editor:** mở đầu bằng "ghi chú editor", nói rõ cần làm gì và ở đâu ("che tên khách ở bảng này"), giữ màn hình đứng yên lúc nói. Kết video thì nói "hết video".
- **Yêu cầu B-roll ngay lúc quay:** nói "Hey Claude, ..." thành 1 câu riêng, ngừng khoảng 1s trước và sau, nói rõ cần gì và minh hoạ câu nào ("Hey Claude, chèn ảnh chụp trang GitHub repo này vào câu vừa rồi"). Có link hay tên file thì đọc ra hoặc để sẵn trên màn hình.
- **Âm thanh:** tắt tiếng web/video demo khi đang nói, Whisper hay nghe tiếng ồn thành chữ ("Tạm biệt, tạm biệt").
- **Nhiều phần quay:** đặt tên file theo thứ tự (`phan 1`, `phan 2`). Skill sẽ ghép đúng thứ tự.

## Luật kỹ thuật (đã gặp thật)

| Luật | Lý do |
|---|---|
| Điểm cắt lấy từ âm thanh (RMS), chữ whisper chỉ để hiểu nghĩa | Whisper gộp mất pause ngắn và hay ghi chỗ lặp thành 1 lần |
| Đoạn im dài, whisper hay bịa câu ("hãy subscribe...") | `analyze.py` lọc các câu này. Đoạn `[không rõ]` ngắn hơn 0.6s thì bỏ |
| Lỗi cấp từ ("vào trong", "cái phần") AI còn sót | Đã biết từ test showroom 3D. Ghi rõ trong tin nhắn duyệt để user nghe lại |
| Codex nhận tối đa 5 ảnh tham chiếu | `gen_thumb.py` tự gộp ảnh dư vào 1 sheet có nhãn |
| Codex CLI gói Free không có tool tạo ảnh | Dùng gói đang login trong `~/.codex`. Muốn free thì dán prompt vào ChatGPT web gói Free |
| Không đổi `cut.mp4` sau khi đã lên plan mà không chạy `shift_plan.py` | Mốc giờ overlay sẽ lệch khỏi câu nói |
