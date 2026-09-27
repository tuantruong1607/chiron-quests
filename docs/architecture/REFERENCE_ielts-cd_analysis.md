# Phân tích tham khảo: `ielts-cd` → bài học cho sản phẩm Cambridge YLE

| Field | Value |
|---|---|
| Nguồn tham khảo | [Abdulloh-Mamanazirov/ielts-cd](https://github.com/Abdulloh-Mamanazirov/ielts-cd) (commit đọc ngày 2026-09-27) |
| Mục đích | Học **ý tưởng, kiến trúc, quy tắc nghiệp vụ** để thiết kế sản phẩm của mình |
| Tác giả tài liệu | BA (Claude) |

> ⚖️ **Ràng buộc pháp lý khi dùng tài liệu này**
> - Repo **không có license** → mọi quyền thuộc tác giả. Tài liệu này chỉ mô tả ý tưởng và cách tổ chức bằng lời của chúng ta; **không chép code, schema, tên hàm hay văn bản** từ repo vào sản phẩm.
> - Repo chứa đề **Cambridge IELTS** (có bản quyền) — **không dùng bất kỳ nội dung đề nào**.
> - Khi triển khai: viết mới trên nền [`fastapi/full-stack-fastapi-template`](https://github.com/fastapi/full-stack-fastapi-template) (MIT). Nếu cần dùng code thật của `ielts-cd`, phải có sự cho phép bằng văn bản của tác giả trước.

---

## 1. Tổng quan

| Hạng mục | `ielts-cd` | Sản phẩm của mình (dự kiến) |
|---|---|---|
| Đối tượng | Người học IELTS Academic của một giáo viên (Uzbekistan) | Trẻ tiểu học luyện Cambridge YLE (Starters/Movers/Flyers), phụ huynh trả tiền |
| Frontend | Next.js (App Router), render phía server | React + Vite (SPA), đóng gói mobile/tablet bằng Capacitor |
| Backend | Chung trong Next.js (API routes + server actions) | FastAPI tách riêng |
| DB | PostgreSQL + Prisma | PostgreSQL + SQLModel/Alembic (theo template) |
| Triển khai | 1 VPS, systemd + nginx, **không container**; CI chạy test với Postgres tạm rồi deploy qua SSH | 1 VPS, Docker Compose + Traefik (theo template) |
| Chấm Writing/Speaking | **Giáo viên chấm tay** (hàng đợi chấm) | AI chấm + chấm phát âm qua API |
| Quy mô code | ~800 file; lõi nghiệp vụ (`lib/`) ~3.600 dòng | — |

**Nhận xét chung:** đây là một codebase kỷ luật tốt — quy tắc nghiệp vụ tách thành hàm thuần (không đụng DB) để test độc lập, có validator tự kiểm tra đề, và tài liệu `ROADMAP` ghi lý do của từng quyết định. Giá trị lớn nhất cho mình là **các quy tắc nghiệp vụ đã được "trả giá" bằng lỗi thật**, không phải code.

---

## 2. Mô hình dữ liệu (diễn giải)

| Nhóm | Thực thể (ý tưởng) | Vai trò |
|---|---|---|
| Tài khoản | Người dùng (vai trò học viên/admin, gói, hạn gói), phiên đăng nhập (token lưu dạng hash), lịch sử đăng nhập để chống dò mật khẩu, token đăng nhập một lần | Auth tự xây, không phụ thuộc dịch vụ ngoài |
| Nội dung | **Đề** (kỹ năng, trạng thái nháp/đã xuất bản/lưu trữ, bộ sách/số tập/số đề, cờ premium, cờ "chỉ dùng trong mock", **nội dung JSON + đáp án JSON tách riêng**), tài sản audio | Đề là dữ liệu, không phải code |
| Làm bài | **Lượt làm bài** (chế độ luyện/thi, trạng thái, bản trả lời dạng map, hạn chót, điểm, band), **full mock** (chuỗi các lượt làm theo thứ tự) | Mỗi kỹ năng trong full mock vẫn là một lượt làm bài bình thường |
| Chấm tay | Bài Writing, bản ghi Speaking, **hàng đợi đáp án lạ** (câu gõ sai nhưng có thể là biến thể hợp lệ) | Giáo viên duyệt |
| Sự kiện | **Buổi thi thử theo lịch** + người tham gia (vào bằng link có token) | Thi thử nhóm có giờ bắt đầu chung |
| Marketing | Kết quả học viên tiêu biểu, cảm nhận | Hiển thị trên trang chủ |
| Cấu hình | Bảng cài đặt dạng JSON (giá gói, quyền lợi, số mock miễn phí…) **gộp đè lên giá trị mặc định theo từng trường** | Admin sửa được mà không cần deploy; thiếu trường không làm trang trống |
| Kênh địa phương | Đăng ký qua **Telegram bot** (kiểm tra thành viên kênh, hỏi tên, cấp link đăng nhập một lần) | Kênh phổ biến ở thị trường của họ |

---

## 3. Quy tắc nghiệp vụ đáng học

### 3.1 Nội dung đề và kiểm tra đề (liên quan trực tiếp FR-213 trong PRD)

1. **Đề là JSON có phiên bản schema**, gồm các phần → nhóm câu hỏi → câu hỏi. Mỗi nhóm có một *loại* (điền chỗ trống trong đoạn văn có ô đánh số, trả lời ngắn, trắc nghiệm, T/F/NG, Y/N/NG, nối với ngân hàng từ, gắn nhãn bản đồ). **Đáp án để ở file riêng** so với nội dung.
2. **Validator bắt buộc trước khi xuất bản**, gồm nhiều lớp:
   - Kiểm tra cấu trúc theo loại nhóm (loại nào cần đoạn văn có ô, loại nào cần danh sách câu, loại nối bắt buộc có ngân hàng từ…).
   - **Tự kiểm tra:** dựng "bài làm hoàn hảo" từ chính đáp án rồi chấm bằng bộ chấm thật — không đạt tuyệt đối nghĩa là nội dung và đáp án lệch nhau.
   - **Kiểm tra chéo loại câu:** đáp án câu T/F/NG chỉ được là một trong ba giá trị, và câu gõ chữ không được có đáp án là các từ đó — bắt lỗi đáp án bị lệch số thứ tự mà bước tự kiểm tra không bắt được.
   - **Đáp án phải xuất hiện trong bài đọc** khi đề yêu cầu lấy từ bài — bắt đúng lỗi *AI diễn đạt lại bài đọc rồi làm hỏng đáp án của chính nó*. ⭐ Rất quan trọng với mình vì đề do AI soạn.
   - Với Writing/Speaking: kiểm tra đề "làm được" (có đề bài, có hình khi cần, tổng thời gian khớp).
   - Không cho xuất bản đề Listening chưa có audio.

### 3.2 Chấm tự động

1. **Chuẩn hóa hai phía** (đáp án chuẩn và bài làm qua cùng một bộ chuẩn hóa) để người soạn viết đáp án tự nhiên.
2. **Số và mã bỏ khoảng trắng nhóm** (số điện thoại, mã bưu chính in cách quãng).
3. **Chính tả Anh–Mỹ tương đương theo danh sách tường minh**, *không* theo quy tắc hậu tố (để không chấp nhận lỗi chính tả thật), và **cố ý loại** những cặp khác nghĩa (story/storey…). Bài học: *chấm sai thành đúng còn tệ hơn vấn đề đang giải*.
4. **Giới hạn số từ theo đề** ("ONE WORD ONLY"…) được thực thi như giám khảo: đúng từ nhưng vượt giới hạn → sai.
5. Câu "chọn hai" chấm theo **tập hợp**, không theo thứ tự.

### 3.3 Vòng đời lượt làm bài

1. Bắt đầu/tiếp tục; **autosave có debounce**; chấm ở server.
2. **Hạn chót tính theo chế độ** (chế độ thi có deadline, luyện thì không) + **khoảng ân hạn** nhỏ cho bài nộp sát giờ.
3. **Hàng đợi đáp án lạ:** chỉ câu *gõ chữ* sai mới vào hàng đợi (chọn sai chữ cái thì đơn giản là sai). Giáo viên chấp nhận → đáp án được bổ sung vào key. Lỗi ở bước này **không được làm hỏng việc nộp bài** (best-effort).
4. **Chấm lại một chiều:** khi key được sửa, chỉ chuyển *sai → đúng*, **không bao giờ trừ điểm** của người đã xem kết quả; chỉ ghi lại các lượt bị ảnh hưởng. ⭐ Áp dụng cho FR-216 (chấm lại khi sửa đáp án).
5. Writing/Speaking chưa chấm thì band để trống — dashboard dựa vào đó phân biệt "chờ chấm" và "đã chấm", và **không đưa bài chưa chấm vào lịch sử band**.

### 3.4 Full mock

1. Thứ tự như thi thật; Speaking để cuối.
2. **Chỉ dùng đề đủ độ dài thật** — một bài đọc 13 câu hay Writing một task là tốt để luyện nhưng *sai* trong mock, vì band báo ra không tái lập được vào ngày thi.
3. Ưu tiên đề **chưa làm**; nếu hết thì lấy đề làm lâu nhất. *Làm lại đề cũ làm band bị thổi phồng.*
4. Đồng hồ từng phần bắt đầu khi mở phần đó và **không reset khi tải lại trang**.
5. Band tổng chỉ ghi khi mọi phần đã có band. Làm tròn overall theo quy tắc IELTS.
6. Quy tắc chọn đề là **hàm thuần, không import DB** → test trực tiếp.

### 3.5 Band và minh bạch

- Bảng quy đổi điểm thô → band là bảng *tham khảo*; mọi band hiển thị đều gắn nhãn ước lượng. Bài ngắn hơn 40 câu được quy đổi tỉ lệ và đánh dấu "chỉ là chỉ báo". (Khớp với nguyên tắc nhãn "chưa hiệu chỉnh" trong PRD.)

### 3.6 Trải nghiệm làm bài

- Giao diện mô phỏng thi trên máy: màn hình chia đôi có thanh kéo (giới hạn tỉ lệ), chuyển thành tab khi màn hình hẹp; thanh điều hướng câu có nhiều trạng thái; đồng hồ; hộp xác nhận nộp.
- **Highlight lưu dưới dạng vị trí ký tự trên văn bản**, không lưu đường dẫn DOM — bền qua render lại, đổi cỡ chữ, và không phải chèn HTML chưa làm sạch.
- Chế độ xem lại có giải thích và **đánh dấu bằng chứng** trong bài đọc.
- Band được "công bố" ở giữa màn hình trước khi hiện bài chấm chi tiết (khoảnh khắc cảm xúc).

### 3.7 Audio

- Phát audio qua route có xác thực, hỗ trợ **range request** (tua/tải từng phần); có cổng chờ buffer; **khóa điều khiển trong chế độ thi**. (Mình sẽ phát từ object storage bằng URL ký hạn ngắn, nhưng giữ nguyên các quy tắc: chờ buffer, khóa tua ở chế độ thi.)

### 3.8 Admin & vận hành

- Hàng đợi chấm Writing/Speaking; hàng đợi đáp án lạ; nhập đề bằng JSON **chạy đúng validator thật**; xuất bản/lưu trữ; cấp premium.
- **Hết hạn gói được tính khi đọc** (so với ngày hết hạn), không cần job định kỳ.
- Gói, giá, quyền lợi lưu trong cài đặt, sửa qua admin.
- i18n: mỗi ngôn ngữ một từ điển, **thiếu khóa nào thì rơi về tiếng Anh** — dịch dở dang vẫn không trống trang. Nội dung bán hàng mang tên người thật thì *không dịch máy*.
- Backup DB bằng script; runbook dựng VPS từ đầu.

---

## 4. Đối chiếu sang sản phẩm Cambridge YLE cho trẻ

| Ý tưởng từ `ielts-cd` | Áp dụng? | Cách áp dụng cho YLE |
|---|---|---|
| Đề là JSON có version, đáp án tách riêng | ✅ | Giữ nguyên nguyên tắc; loại câu hỏi phải thiết kế lại cho trẻ (xem §5) |
| Validator nhiều lớp + tự kiểm tra + đáp án phải có trong nguồn | ✅⭐ | Bắt buộc cho đề AI soạn; thêm kiểm tra: **tranh có đúng các đồ vật mà câu hỏi nhắc tới**, từ vựng nằm trong danh sách từ của cấp độ |
| Chuẩn hóa đáp án, chính tả Anh–Mỹ theo danh sách | ✅ | YLE có phần viết từ đơn; trẻ hay sai chính tả → cần quy tắc chấm riêng theo hướng dẫn chấm YLE (cần kiểm tra handbook) |
| Chấm lại một chiều (chỉ sai → đúng) | ✅⭐ | Áp dụng cho FR-216 |
| Hàng đợi đáp án lạ | ✅ | Admin duyệt biến thể hợp lệ |
| Quy tắc thuần tách khỏi DB để test | ✅ | Áp dụng cho chọn đề mock, quy đổi khiên, điều kiện dự đoán |
| Full mock chỉ dùng đề đủ độ dài, ưu tiên đề chưa làm | ✅⭐ | Trực tiếp cho **dự đoán số khiên** — làm lại đề cũ làm dự đoán sai |
| Band luôn gắn nhãn ước lượng | ✅ | Số khiên dự đoán luôn có nhãn + trạng thái hiệu chỉnh |
| Buổi thi thử theo lịch vào bằng link | ✅ | Nền cho **cohort (C)**: "Ngày thi thử chung" hằng tháng cho các bé cùng cấp độ |
| Đăng ký qua bot của kênh nhắn tin địa phương | ⚠️ | Ý tưởng tương đương với **Zalo OA** cho phụ huynh — cần kiểm tra chính sách (TBD-16) |
| Hết hạn gói tính khi đọc; cài đặt gộp đè mặc định | ✅ | Đơn giản, ít lỗi |
| Highlight theo vị trí ký tự | ⚠️ | Ít cần với trẻ nhỏ; giữ cho Flyers/KET đọc hiểu |
| Chấm Writing/Speaking bằng giáo viên | ❌ | Mình dùng AI + chấm phát âm; có thể giữ "hàng đợi review" cho các ca AI không chắc |
| Next.js SSR, không container | ❌ | Mình chọn Vite SPA + Capacitor (mobile/tablet) và Docker Compose |
| Nội dung đề Cambridge | ❌ | Tuyệt đối không dùng |

---

## 5. Khác biệt lớn của YLE mà `ielts-cd` không có (phải tự thiết kế)

> Cần đối chiếu từng mục với **Handbook for teachers** chính thức của Cambridge trước khi đặc tả chi tiết.

1. **Loại câu hỏi xoay quanh tranh**: chọn tranh đúng, nối từ với tranh, kéo đồ vật vào cảnh, tô màu theo hướng dẫn nghe, viết từ đơn dưới tranh, kể chuyện theo chuỗi tranh.
2. **Speaking là hội thoại dựa trên tranh** với giám khảo (chỉ vào đồ vật, trả lời câu hỏi về tranh, tìm điểm khác nhau, kể chuyện theo tranh, câu hỏi về bản thân) — cần **giám khảo AI giọng thân thiện**, hội thoại ngắn, chờ trẻ trả lời lâu hơn người lớn.
3. **Chấm theo khiên** (mỗi bài thi tối đa 5 khiên, tổng 15) thay cho band.
4. **Người dùng chưa đọc thạo** → hướng dẫn bằng giọng nói, biểu tượng lớn, thao tác chạm/kéo; ưu tiên tablet.
5. **Tài khoản do phụ huynh sở hữu**, nhiều hồ sơ con; cổng phụ huynh cho thanh toán và cài đặt (yêu cầu của App Store Kids / Google Play Families).
6. **Dữ liệu trẻ em**: đồng ý của cha mẹ, giọng nói trẻ em, tối thiểu hóa dữ liệu (Luật BVDLCN 2025).
7. **Nhận dạng giọng trẻ em** kém chính xác hơn người lớn → cần kiểm chứng speech provider trước khi xây.

---

## 6. Ước tính giá trị "đi tắt"

- **Tiết kiệm nhờ học từ `ielts-cd`:** thời gian *thiết kế* và *tránh lỗi* ở engine đề, validator, chấm lại, full mock — ước tính thô 1–2 tuần suy nghĩ/sửa lỗi.
- **Tiết kiệm nhờ template MIT:** hạ tầng auth/user/admin/Docker/CI — ước tính thô 2–3 tuần.
- **Không tiết kiệm được:** loại câu hỏi dựa trên tranh, giám khảo AI cho trẻ, giao diện tablet cho trẻ, nội dung (câu hỏi + tranh + audio), tích hợp chấm phát âm, dự đoán khiên và hiệu chỉnh.
