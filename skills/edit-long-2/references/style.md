# Style edit-long-2 (học từ RoboNuggets, màu Contentta)

Nguồn: "9 NEW Claude Mods that can truly change how you work" của Jay E, kênh RoboNuggets (youtu.be/lDrAZ1wAyVs, 12:47, 861K view). Phân tích ngày 28/10/2026. Ảnh tham chiếu không đưa lên repo vì thuộc kênh khác, xem video gốc trên YouTube.

## Số đo của video gốc
- 52 lần đổi cảnh trong 12:47, khoảng 4 lần/phút. Riêng 60 giây đầu có 14 lần.
- Lấy mẫu 20 giây 1 khung: khoảng 75% thời lượng mặt nằm trong khung bo nhỏ, phần còn lại của màn hình là đồ hoạ. Mặt full khung chỉ khoảng 20%, phần lớn ở đầu và cuối video.
- Không có B-roll quay ngoài. Mọi hình là đồ hoạ dựng lại (UI app, sơ đồ nét mảnh, icon) hoặc ảnh chụp trang thật.
- Chữ trên màn hình rất ít: 1 tiêu đề + 1 dòng phụ, nhãn 1-2 chữ.

## Bảng đủ 50 hiệu ứng (quét 3 giây 1 khung, 28/10/2026)

Mỗi dòng là 1 cảnh trong `demo/` (code ở `template.html` cho s01-s10, `scenes/b.js`-`e.js` cho s11+). Cột "Gốc" ghi giờ trong video RN.

| Mã | Hiệu ứng | Gốc |
|---|---|---|
| s01 | Thẻ tiêu đề lớn | Gốc: thẻ "Mods" (RN 0:02), cắt cứng từ mặt sang 1 thẻ chữ serif + logo, nền có vệt sáng chéo |
| s02 | Mặt thu vào khung bo + sơ đồ | Gốc: chuyển cảnh chữ ký của video (RN 0:40, 1:00): mặt mờ đi, bo góc, thu nhỏ sang 1 bên; bên kia là sơ đồ nét mảnh, tick tròn bật lên theo lời |
| s03 | Lưới icon sáng theo lời | lưới icon viền cam (RN 0:20), mặt thu nhỏ góc dưới trái |
| s04 | Chat trong Claude | giao diện Claude Code desktop dựng lại (RN 0:06-0:17, 4:20), ô nhập viền sáng khi gõ, gửi xong hiện tool call |
| s05 | Timeline tự cắt | các khung UI nét mảnh có thanh tiến độ, phần đổi trạng thái đổi màu (RN 3:20, 3:40) |
| s06 | Thẻ "Bạn nên biết" | thẻ "You Should Know" (RN 5:00, 5:20) có icon, dòng chữ được tô highlight và thanh mức dùng |
| s07 | Logo bật quanh mặt | đoạn giới thiệu (RN 0:27-0:30): khung hình trượt sang phải, nửa trái phủ trắng mờ dần, logo khách hàng bật lên từng cái |
| s08 | Trang thật + zoom số | chụp trang web/cộng đồng toàn khung, mặt ở góc dưới trái (RN 5:40, 6:00) |
| s09 | Gallery duyệt + công tắc | các khung UI có tick và công tắc gạt (RN 11:20 "Hot reloading") |
| s10 | Chữ glitch trên mặt | chữ serif nhiễu ký tự rồi hiện rõ ngay trên khung mặt (RN 9:40 "Terminal Browser") |
| s11 | Tên phần nhiễu chữ trên mặt | mỗi mod mở bằng tên serif nhiễu rồi rõ, ngay trên khung mặt full (RN 2:03 Savvy Progress, 4:00 Claude Skins, 7:03 Cache Tax, 8:15 Blast Radius, 9:06 Reflect, 10:09 Replay Theater) |
| s13 | Icon xoay quanh mascot | "Smarter and faster" (RN 0:24): mascot pixel ở giữa, vòng icon bật lần lượt quanh nó và xoay chậm |
| s14 | Tick → mũi tên → công tắc | "Already switched on" (RN 0:48): ô tick tròn, mũi tên, công tắc gạt sang cam |
| s15 | 3 thẻ, đổi tiêu điểm | Skill / MCP connector / Mod (RN 1:06-1:21): 3 khung wireframe, tiêu điểm chạy từ thẻ này sang thẻ kia, thẻ khác mờ đi, tiêu đề đổi theo |
| s17 | Tập tài liệu + mũi tên nảy | "Grab it in the description" (RN 1:45, 1:54, 12:21): xấp PDF xoè ra, mũi tên chỉ xuống nảy liên tục |
| s19 | Biểu đồ Venn | "The right mix" (RN 2:06): 2 vòng tròn giao nhau, icon trong mỗi vòng, chỗ giao sáng lên |
| s20 | Đội mascot có mũ | subagents (RN 2:24-2:51): mascot pixel xuất hiện thành hàng, mỗi con 1 mũ và nhãn vai trò, nhảy lên khi được gọi |
| s21 | Tín hiệu chạy theo đường | "A mod listens for events" (RN 3:06-3:15): khung Claude Code phát tín hiệu, chấm sáng chạy theo đường tới hộp mod |
| s22 | Tab đổi trạng thái | Watch / Change / Handle (RN 3:18-3:45): 3 tab dạng pill, tab sáng đổi theo lời, sơ đồ bên dưới đổi theo tab |
| s23 | Sơ đồ nút nối | "It watches every helper" (RN 3:24-3:30): mascot nối dây tới từng nút, nút sáng theo lượt |
| s24 | Bảng nhỏ chạy số | "It draws the whole Agents panel" (RN 3:42): bảng agent kèm chi phí từng dòng hiện dần, có thanh mức |
| s25 | Ống dẫn: chat → skill → kết quả | "Describe what you want" (RN 3:54): bong bóng chat → hộp skill có sẵn → mod mới, mũi tên nối dần |
| s26 | Các lớp tách 3D | "A great first mod" (RN 4:27-4:30): khối isometric nhiều lớp tách ra, lớp trên đổi màu, nhãn chỉ vào từng lớp |
| s27 | Nhánh toả từ 1 gốc | "Steer what it looks out for" (RN 5:09-5:15): icon gốc toả 3 nhánh cong tới 3 nhãn, nhãn sáng theo lời |
| s28 | So 2 bên + thanh mức | "It runs a second agent" (RN 5:18-5:27): 2 mascot so token, thanh mức dài ngắn, cột bên cạnh có nhãn "uses an LLM" / "no LLM needed" |
| s29 | Thư mục + lưới file | "Not a developer? still useful across lots of files" (RN 6:36-6:40): 1 thư mục cam rồi lưới file icon hiện ra |
| s30 | Thẻ có đồng hồ + thanh | Prompt cache (RN 7:12-7:36): cột đoạn chat bên trái, thẻ giữa có vòng đồng hồ "~1 hour", thanh Usage chạy |
| s31 | Icon → mũi tên → đồng xu | "A mod that can actually save you money" (RN 7:09): khối Cache Tax → mũi tên → chồng xu |
| s32 | Luồng cảnh báo | "Would your agent ever delete your files?" (RN 8:36-8:45): agent → icon thùng rác → thư mục, mũi tên đỏ, nhãn model |
| s33 | Vòng lặp xoay | "Reflect / Like RLHF" (RN 9:09): vòng chấm và mũi tên xoay quanh 1 tâm, nhãn quanh vòng |
| s34 | 2 cửa sổ gộp làm 1 | "Check every change" → "Everything stays in one place" (RN 10:00-10:06): 2 cửa sổ nối vòng mắt, rồi gộp thành 1 |
| s35 | Hàng 4 bước | "Really easy" (RN 10:51): 4 icon tròn Update, Describe, Tweak, Install, cái đầu sáng |
| s36 | Thanh trượt mốc gói | "Mods need 2.1.287 or newer" (RN 10:54): trục số có mốc, núm trượt tới phiên bản cần |
| s37 | Terminal gõ lệnh | "In the terminal: claude update" (RN 10:57): thẻ terminal nhỏ, lệnh gõ dần, dòng kết quả xanh |
| s38 | Công tắc tải lại | "Hot reloading" (RN 11:18-11:24): khung UI, icon vòng xoay cam, công tắc gạt bật |
| s39 | Gõ yêu cầu → tài liệu đổi | "Save it as a plugin" (RN 11:39-11:42): ô nhập gõ lệnh, 2 khung "this session / next session", tick xanh khi lưu |
| s41 | Thẻ chat có nút bấm | thẻ "You should know" ngay trong khung chat (RN 4:57-5:06), có nút Tell me more / I knew this / Dismiss, con trỏ bấm |
| s42 | Bảng agent chạy tiến độ | "Launch kit" (RN 0:12-0:17, 2:33-2:57): panel Agents bên phải, mỗi agent 1 dòng có mascot, chi phí, thanh tiến độ chạy song song |
| s43 | Khung soi 1 dòng, mờ phần còn lại | khung viền cam khoanh đúng dòng đang nói, phần còn lại mờ đi (RN 2:18, 9:24) |
| s44 | Lưới mẫu, khung chọn chạy | "Claude Skins" (RN 4:15-4:24): lưới thẻ giao diện, khung chọn viền màu nhảy từ thẻ này sang thẻ khác |
| s45 | Diff + nút Replay | "Replay Theater" (RN 10:15-10:45): diff code đỏ/xanh, nút "Replay edits" được bấm, chuyển qua edit kế |
| s46 | Cây thư mục sáng file | "Filetree" (RN 6:06-6:57): cây file bên phải, file Claude đụng tới sáng tím kèm nhãn Opened / Edited, thư mục mở ra |
| s47 | Thẻ 2 lựa chọn + bấm | Cache Tax hold (RN 7:42-7:57): thẻ trong chat chặn lại, 2 ô lựa chọn kèm giá, nút "Pay and send" được bấm |
| s48 | Hộp xác nhận có thanh dung lượng | "Blast Radius" (RN 8:24-8:33): Claude định xoá thư mục, hộp xác nhận liệt kê từng file kèm thanh dung lượng, nút "Delete 9 files" / Cancel |
| s50 | Lệnh "/" + dòng trạng thái | gõ "/keepwarm" hiện menu lệnh, dòng trạng thái dưới ô nhập đổi theo (RN 8:06-8:12) |
| s53 | Bản đồ ghim → lịch ghim ảnh | bản đồ thế giới có ghim và ảnh thành viên bật lên (RN 0:35-0:37) |
| s54 | Bài đăng + tô dòng | bài X của Claude Code ở giữa màn, các dòng quan trọng được tô cam lần lượt (RN 0:40-0:45) |
| s55 | Trang thật cuộn + con trỏ bấm | trang cộng đồng / GitHub thật toàn khung, cuộn xuống, con trỏ di chuyển và bấm, mặt góc dưới trái (RN 5:30-6:00, 9:45-9:54) |
| s56 | Tên lớn + thẻ giới thiệu | đoạn giới thiệu bản thân (RN 0:27-0:32): khung trượt phải, tên "Jay" cỡ lớn bên trái, sau đó thẻ "Education" và logo bật lên |
| s57 | Outro: logo nảy + dải màu quét | cuối video (RN 12:33-12:45) và đoạn chèn thương hiệu (RN 0:36-0:38): khung mặt mờ đi, logo nảy trên nền sáng, dải vàng cong quét ngang |

## 10 hiệu ứng chính và lúc dùng (đối chiếu cảnh demo `sNN`)

| Mã | Gốc (giờ trong video RN) | Mô tả | Khi nào dùng |
|---|---|---|---|
| s01 | Thẻ "Mods" 0:02 | Cắt cứng từ mặt sang thẻ chữ lớn + logo, vệt sáng chéo trôi chậm | Câu nêu tên chủ đề ở hook |
| s02 | 0:40, 1:00, 3:20 | **Chuyển cảnh chữ ký:** mặt mờ đi, bo góc, thu vào khung bo 1 bên trong 0.5s. Bên kia là sơ đồ nét mảnh, tick tròn bật theo lời | Giải thích quy trình, so sánh 2-4 lựa chọn |
| s03 | 0:20 | Lưới icon trong ô viền, ô sáng lên đúng lúc nói | Liệt kê 4-9 thứ |
| s04 | 0:06-0:17, 4:20 | Giao diện chat Claude dựng lại: ô nhập sáng viền, chữ gõ dần, gửi xong hiện tool call | Mọi đoạn nói "mình prompt cho nó…" |
| s05 | 3:40, 7:40 | Khung UI nét mảnh có thanh tiến độ, phần đổi trạng thái đổi màu, phần bị bỏ co lại | Trước/sau, thứ bị bỏ, tiến trình |
| s06 | 5:00, 5:20 | Thẻ "You should know": icon, dòng chữ được tô highlight, thanh mức | Lưu ý, chi phí, cảnh báo |
| s07 | 0:27-0:30 | Khung hình trượt sang phải, nửa trái phủ nền mờ dần, logo bật từng cái | Nhắc tên tool, khách hàng, đối tác |
| s08 | 5:40, 6:00 | Trang web thật toàn khung, mặt góc dưới trái, zoom vào con số | Show kết quả thật, số view, trang repo |
| s09 | 11:20 | Khung UI có tick + công tắc gạt | Duyệt, bật tính năng |
| s10 | 9:40 | Chữ xáo ký tự rồi chốt, ngay trên khung mặt | Câu chốt, câu gây tò mò |

Vị trí khung mặt: `L` (trái lớn, cx 480), `R` (phải lớn, cx 1450), `BL` (góc dưới trái nhỏ, cho UI chiếm gần hết màn). Đổi bên liên tục, không 2 lần liền cùng 1 bên.

## Đổi sang brand Contentta
Video gốc nền tối + cam Claude. Brand Contentta không có dark mode, nên giữ bố cục và chuyển động, đổi màu:

| Gốc | Contentta |
|---|---|
| Nền than `#1C1B19` + dải chấm halftone | Ivory `#FAF6EF` + 3 quầng lavender/peach/sky mờ + dải chấm ink 16% |
| Nét UI kem mảnh | Nét ink 16%, thẻ giấy trắng bo 26-28px, bóng mềm |
| Nhấn cam `#E8743B` | Plum `#4A3AE0` (AI làm), vàng `#E6B45A` (bạn làm), peach `#F07A5A` (lỗi, bị bỏ), sage `#3E9B6E` (đạt) |
| Tiêu đề serif kem | Bricolage Grotesque 800 ink, 1-2 chữ nhấn Lora nghiêng plum |
| Viền trắng sáng quanh khung mặt | Viền trắng 5px + bóng mềm |

Đổi màu sang brand của bạn: sửa các biến `--ivory`, `--plum`... ở đầu `references/demo/template.html`.

## Chuyển động
- Mặt full → khung bo: 0.5-0.55s, `power3.inOut`. Blur 0 → 18px ở nửa đầu, về 0 ở nửa sau. Tâm mặt (`FX, FY`) luôn giữ giữa khung.
- Chữ, thẻ vào: rise 26px + blur 8px → 0, 0.55s `expo.out`. Icon, tick, logo: pop scale 0.6 → 1, `back.out(1.8)`.
- Mọi mốc hiệu ứng khớp đúng chữ trong transcript (giây của từ đó), không đặt theo cảm giác.
- Hết đoạn thì trả mặt về full khung cũng bằng chuyển cảnh blur, không cắt cứng (trừ thẻ tiêu đề s01).
