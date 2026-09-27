# IELTS Lab "Band thật" — Product Requirements Document (PRD / SRS)

> Chuẩn IIBA BABOK v3 (Agile Perspective) + cấu trúc SRS (BRD + FRD + NFR).
> Thay thế PRD v1.0 – v1.2. Lợi thế cạnh tranh chuyển từ **tính năng AI** (ChatGPT đã làm tốt, xem §2.7)
> sang hai thứ ChatGPT về cấu trúc không có: **(A) dự đoán band được hiệu chỉnh bằng điểm thi thật của người Việt**
> và **(C) cohort có cam kết, chủ động đồng hành đến ngày thi**. Đủ 4 kỹ năng (Listening, Reading, Speaking, Writing) là công cụ đo, để dự đoán cả **band overall**.

---

## Document Control

| Field | Value |
|---|---|
| Document ID | PRD-2026-001 |
| Version | 2.1 |
| Status | Draft — chờ Founder duyệt |
| Owner | Founder (kiêm Sponsor / Product Owner / BA / Developer) |
| Created | 2026-09-27 (v1.0) |
| Last Updated | 2026-09-27 |
| Tên thương hiệu chung | `TBD-02` — ứng viên: "Chiron" (theo tên repo `chiron-quests`) |
| Tên sản phẩm Release 1 | IELTS Lab "Band thật" (tên làm việc) |

### Quy ước

- **PHẢI** (Must) — bắt buộc; thiếu = không phát hành. **NÊN** (Should) — khuyến nghị. **CÓ THỂ** (Could) — tùy chọn.
- Priority theo **MoSCoW**: `M` Must · `S` Should · `C` Could · `W` Won't (không làm trong release này).
- **`[Đề xuất]`** — con số/ngưỡng do BA đề xuất, **chưa được Founder duyệt**. Phải chốt trước mốc ghi trong §19.
- **`TBD-xx`** — quyết định còn mở, xem §19.

### Change Log

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-09-27 | Founder | Baseline: IELTS 4 kỹ năng, General Training, 49k/tháng, quota theo ngày |
| 1.1 | 2026-09-27 | BA (Claude) + Founder | Xem bảng "Thay đổi so với v1.0" bên dưới |
| 1.2 | 2026-09-27 | BA (Claude) + Founder | Release 1 = Speaking + Writing; định vị cạnh tranh với ChatGPT; xem bảng "Thay đổi so với v1.1" |
| 2.0 | 2026-09-27 | BA (Claude) + Founder | Định vị "Band thật" (A) + Cohort cam kết (C); chiến lược dữ liệu nguồn 4 → open beta → hiệu chỉnh bằng nguồn 1; xem bảng "Thay đổi so với v1.2" |
| 2.1 | 2026-09-27 | BA (Claude) + Founder | Thêm Listening & Reading **trước open beta**; đề do AI soạn + người duyệt (không crawl); dự đoán band overall; roadmap 22 tuần; xem bảng "Thay đổi so với v2.0" |

### Thay đổi so với v2.0 (Founder duyệt 2026-09-27)

| # | Hạng mục | v2.0 | v2.1 | Lý do |
|---|---|---|---|---|
| 1 | Kỹ năng trong R1 | Speaking + Writing | **Thêm Listening + Reading** (Academic), trước open beta | Người học quan tâm band **overall**; L/R chấm theo đáp án nên dễ dự đoán nhất |
| 2 | Nguồn đề L/R | — | **AI soạn + người duyệt**; audio Listening bằng TTS nhiều giọng; **không crawl** đề trên mạng, không dùng đề sách có bản quyền hay đề thi thật do thí sinh nhớ lại (FR-215) | Crawl = vi phạm bản quyền/bảo mật đề; phá uy tín "band thật"; đề crawl có đáp án sai và độ khó không rõ |
| 3 | Dự đoán | Speaking, Writing | + **Listening, Reading và overall** | Hoàn thiện lợi thế A |
| 4 | Quy đổi band L/R | — | **Bảng quy đổi riêng cho từng đề**, khởi đầu bằng bảng tham chiếu, hiệu chỉnh bằng thống kê câu hỏi và cặp điểm thật (F24) | Đề tự soạn có độ khó khác đề thật |
| 5 | Roadmap | Open beta tuần 10 | **Open beta tuần 16**; roadmap 22 tuần | Founder chọn có L/R trước open beta |

### Thay đổi so với v1.2 (Founder duyệt 2026-09-27)

| # | Hạng mục | v1.2 | v2.0 | Lý do |
|---|---|---|---|---|
| 1 | Lợi thế cạnh tranh | 5 tính năng AI (mô phỏng phòng thi, chấm phát âm…) | **A: dự đoán band thật được hiệu chỉnh bằng kết quả thi thật** + **C: cohort cam kết** | Nghiên cứu 09/2026: ChatGPT voice (GPT-Live, free) đã làm tốt hội thoại luyện thi; tính năng AI bị bắt kịp trong vài tháng (§2.7) |
| 2 | Định vị | "Phòng luyện nói và viết cho người Việt" | **"Biết trước điểm thật của bạn — và đi cùng bạn đến ngày thi"** | Câu mà ChatGPT không thể nói vì không có dữ liệu điểm thật |
| 3 | Chiến lược dữ liệu | — | **Nguồn 4** (dữ liệu công khai, qua kiểm tra license) → **open beta** → **nguồn 1** (người vừa thi xong) để hiệu chỉnh; cohort nuôi dữ liệu lâu dài (§16) | Founder chọn thứ tự này |
| 4 | Beta | Beta kín tuần 8, bán tuần 9 | **Open beta tuần 10**, bắt đầu bán cùng lúc | Cần nhiều người dùng để có dữ liệu |
| 5 | Tính năng mới | — | F16 Dự đoán band, F17 Thu thập kết quả thi thật, F18 Hiệu chỉnh, F19 Cohort, F20 Nhắc học chủ động, F21 Quản lý bộ dữ liệu & license | Hiện thực A + C |
| 6 | Cam kết hoàn tiền theo kết quả | — | **Chỉ bật khi sai số đạt ngưỡng** trên dữ liệu thật (FR-175) | Tránh rủi ro tài chính và quảng cáo sai sự thật |
| 7 | Speaking/Writing | Là lợi thế chính | Là **công cụ đo** cho dự đoán; giữ nguyên yêu cầu chức năng | Chấm nhất quán trở thành điều kiện sống còn cho hiệu chỉnh |

### Thay đổi so với v1.1 (Founder duyệt 2026-09-27)

| # | Hạng mục | v1.1 | v1.2 | Lý do |
|---|---|---|---|---|
| 1 | Phạm vi Release 1 | Chỉ Writing | **Speaking (Part 1–3) + Writing (Task 1, Task 2)**; Listening/Reading vẫn để sau | Chỉ có Writing thì cạnh tranh trực diện với ChatGPT miễn phí ở đúng phần ChatGPT mạnh nhất |
| 2 | Định vị | "Biết lỗi gì, sửa được chưa" | **"Phòng luyện nói và viết IELTS dành riêng cho người Việt"**, Speaking là tính năng chính (§2.7) | Speaking là nơi ChatGPT yếu nhất: không mô phỏng phòng thi, không có điểm phát âm định lượng |
| 3 | Tính năng mới | — | Mô phỏng phòng thi Speaking, chấm phát âm dựa trên audio, **lỗi đặc trưng của người Việt**, **insight xuyên kỹ năng** Writing ↔ Speaking | Những điều ChatGPT không làm được |
| 4 | Thu tiền | Tuần 6 | **Beta kín miễn phí tuần 8, bắt đầu bán tuần 9** | Chỉ bán khi đã có Speaking, tức lý do để không dùng ChatGPT |
| 5 | Credit | Writing 1 credit | Writing 1 credit; Speaking **1 credit/Part, 3 credit/bài thi đủ 3 Part** | Chi phí Speaking cao hơn |
| 6 | Multimodal | — | Hiểu là **Speaking + Writing** (kỹ năng sản sinh), **không** phải đủ 4 kỹ năng | Listening/Reading cạnh tranh bằng số lượng đề, AI ít tạo khác biệt |

### Thay đổi so với v1.0 (tóm tắt quyết định đã chốt ở v1.1)

| # | Hạng mục | v1.0 | v1.1 | Lý do |
|---|---|---|---|---|
| 1 | Phạm vi Release 1 | 4 kỹ năng + full mock | Chỉ Writing — **đã thay bởi v1.2** (Speaking + Writing) | Dễ làm: không cần sản xuất đề nghe-đọc |
| 2 | Loại đề | General Training | **Academic** | Đa số người học IELTS tại VN thi Academic |
| 3 | Giá Premium | 49.000đ/tháng | **69.000đ/tháng** + **gói 3 tháng** | Cải thiện unit economics; khớp chu kỳ ôn thi 2–4 tháng |
| 4 | Quota | 1/ngày (Free), 5/ngày (Premium) | **Credit theo tháng**; Free cấp theo tổng số lượt | Quota theo ngày (150 lượt/tháng) có thể vượt doanh thu |
| 5 | Chiến lược AI | Provider abstraction | + **Phân loại dữ liệu**, **model chấm cố định**, **caching**, **circuit breaker giữa các provider** | Kiểm soát chi phí mà không vi phạm privacy/ToS, giữ điểm nhất quán |
| 6 | Tầm nhìn | Chỉ IELTS | **Nền tảng đa kỳ thi**: IELTS → TOEIC → SAT, có gate KPI | Tăng LTV theo vòng đời người học |
| 7 | KPI | TBD | **Ngưỡng `[Đề xuất]`** chờ duyệt | Cần đo được "thành công" trước beta |
| 8 | Thu tiền | Tuần 10 | Từ tuần 6 — **v1.2 đổi thành tuần 9**; vẫn cho phép xác nhận chuyển khoản thủ công | Kiểm chứng sẵn sàng trả tiền |
| 9 | Upload tài liệu | P1 | **Won't** (hoãn) | Rủi ro bản quyền (người dùng upload sách đề có bản quyền) |

---

## 1. Introduction

### 1.1 Purpose

Tài liệu đặc tả yêu cầu business, chức năng và phi chức năng cho **Release 1 — IELTS Lab "Band thật"**,
đồng thời xác định lộ trình và các ràng buộc kiến trúc để mở rộng sang Listening/Reading, TOEIC và SAT.

### 1.2 Intended Audience

Founder (Sponsor/PO/Dev), cộng tác viên nội dung/QA tương lai, cố vấn pháp lý, chuyên gia IELTS (khi có).

### 1.3 Product Scope

Nền tảng web (responsive + PWA) giúp người học IELTS Academic tại Việt Nam **biết trước band Speaking và Writing khi đi thi thật** và **được đồng hành đến ngày thi**:

- **Dự đoán band thật (A):** từ các bài thi thử trên hệ thống, dự đoán band Speaking và Writing khi thi thật, kèm khoảng sai số. Dự đoán được hiệu chỉnh bằng các cặp "bài thi thử + phiếu điểm thật" do người dùng tự nguyện gửi.
- **Cohort cam kết (C):** nhóm học 8 tuần có ngày thi mục tiêu, được nhắc luyện chủ động mỗi ngày, có đặt cọc hoàn lại khi hoàn thành.

Công cụ đo là đủ 4 kỹ năng:
- **Speaking:** thi thử Part 1 → 2 → 3 với giám khảo AI, đúng thời gian như phòng thi → report theo 4 tiêu chí, **phát âm được chấm bằng phân tích audio**, chỉ ra **lỗi đặc trưng của người Việt**.
- **Writing:** nộp Task 1/Task 2 → report theo 4 tiêu chí, gắn bằng chứng trong bài.
- **Listening & Reading:** bài thi đủ 40 câu mỗi kỹ năng, đúng thời gian, chấm theo đáp án, quy đổi band theo bảng riêng của từng đề. Đề do AI soạn và được người duyệt; audio Listening bằng TTS nhiều giọng.

Cả hai kỹ năng dùng chung **Error Memory**: hệ thống ghi nhớ lỗi lặp lại, kể cả lỗi xuất hiện ở cả nói và viết → người học **làm lại / làm đề tương đương** → **kiểm chứng lỗi đã được sửa hay chưa**.

**Định vị:** *"Biết trước điểm thật của bạn — và đi cùng bạn đến ngày thi."*
Không định vị là "AI chấm IELTS" (ChatGPT đã làm tốt). Mọi band là **ước lượng/dự đoán**, không phải điểm chính thức. Chỉ được công bố độ chính xác dự đoán bằng số liệu thật đã đo (FR-174).

### 1.4 References

- IELTS Exam Lab PRD v1.0 (2026-09-27)
- Biên bản đánh giá business (phiên làm việc 2026-09-27)
- IELTS Writing và Speaking Band Descriptors (public version) — dùng làm cơ sở rubric; không sao chép đề thi có bản quyền
- Nghiên cứu cạnh tranh và bộ dữ liệu công khai (09/2026) — nguồn liệt kê ở §2.7 và §16

---

## 2. Business Context (BACCM)

### 2.1 Change
Xây mới một sản phẩm luyện thi có lợi thế dựa trên **dữ liệu điểm thật** và **cam kết đồng hành**, dùng đủ 4 kỹ năng làm công cụ đo. Trình tự: chuẩn bị bộ chấm bằng dữ liệu công khai hợp lệ (nguồn 4) và xây kho đề L/R → open beta tuần 16 → hiệu chỉnh dự đoán bằng kết quả thi thật (nguồn 1) → bật cam kết theo kết quả khi đủ dữ liệu.

### 2.2 Need (giả thuyết cần kiểm chứng trong beta)

| # | Pain point | Bằng chứng hiện có |
|---|---|---|
| N1 | Người tự học không có phản hồi Writing nhất quán, cụ thể | Giả thuyết của Founder — cần xác nhận qua phỏng vấn beta |
| N2 | Chấm chữa bởi giáo viên/khóa học có chi phí cao so với ngân sách học sinh–sinh viên | Giả thuyết |
| N3 | Người học viết nhiều bài nhưng không biết lỗi nào lặp lại, lỗi nào đã sửa được | Giả thuyết |
| N4 | Chatbot AI thông thường không lưu lịch sử lỗi, không có quy trình thi và không đo tiến bộ | Giả thuyết |
| N5 | Người tự học không có môi trường luyện nói giống phòng thi (thời gian, cue card, câu hỏi nối tiếp) và không biết chính xác mình phát âm sai âm nào | Giả thuyết — cần xác nhận qua phỏng vấn beta |
| N6 | Gia sư Speaking 1-1 có chi phí cao và khó sắp lịch luyện thường xuyên | Giả thuyết |
| N7 | Người học không biết mình đã đủ điểm để đăng ký thi hay chưa; lệ phí thi IELTS ở mức vài triệu đồng/lần nên thi trượt mục tiêu rất tốn kém | Giả thuyết — cần xác nhận qua phỏng vấn |
| N8 | Người tự học bỏ cuộc giữa chừng vì không có ai đồng hành, không có hạn chót | Giả thuyết |

### 2.3 Solution (high-level)
Sản phẩm gồm: (0) **dự đoán band thật** có khoảng sai số và **cohort cam kết** có nhắc học chủ động — hai lợi thế chính; (1) thi thử Speaking Part 1–3 với giám khảo AI; (2) chấm phát âm dựa trên audio và phát hiện lỗi đặc trưng của người Việt; (3) nộp bài Writing Task 1/Task 2 trong Exam Mode hoặc Practice Mode; (4) AI report theo tiêu chí có bằng chứng cho cả hai kỹ năng; (5) Error Memory và insight xuyên kỹ năng; (6) Redo/Rewrite & Retest; (7) Drill mục tiêu; (8) Credit/Premium; (9) Admin theo dõi chi phí và chất lượng.

### 2.4 Stakeholders — xem §4.

### 2.5 Value — xem §3 (Business Objectives).

### 2.6 Context

| Ràng buộc | Giá trị |
|---|---|
| Nhân lực | Founder solo |
| Ngân sách phát triển ban đầu | < 10.000.000 VNĐ |
| Thời gian | Nguồn 4 tuần 1–3; L/R tuần 9–14; open beta + bắt đầu bán tuần 16; chiến dịch nguồn 1 từ tuần 16; cohort đầu tiên tuần 18; cam kết hoàn tiền chỉ bật khi đạt ngưỡng dữ liệu (dự kiến tháng 8–11) |
| Tech stack | Next.js + TypeScript, FastAPI + Python, PostgreSQL, VPS, Docker Compose |
| Thị trường | Việt Nam, UI tiếng Việt, nội dung đề bằng tiếng Anh |
| Pháp lý | Bảo vệ dữ liệu cá nhân (xem §12); người dùng có thể là người chưa thành niên |
| Chuyên môn | Chưa có chuyên gia IELTS hoặc dataset tham chiếu được cấp phép |
| Cạnh tranh | ChatGPT/AI tổng quát miễn phí; các nền tảng luyện thi IELTS trong nước |

### 2.7 Định vị cạnh tranh (cập nhật theo nghiên cứu 09/2026)

**ChatGPT hiện đã làm được** (có nguồn):

| Thời điểm | Cập nhật | Hệ quả |
|---|---|---|
| 06/2026 | Hướng dẫn phát âm từ kèm audio mẫu, 60+ ngôn ngữ | Dạy phát âm; chưa thấy nguồn nói có *chấm* phát âm người dùng |
| 07/2026 | GPT-Live-1 / mini: nghe-nói đồng thời, ngắt lời tự nhiên; **người dùng free có bản mini** | Thi thử Speaking dạng hội thoại dùng miễn phí được, rất tự nhiên |
| 09/2026 | Voice chạy trên các model GPT-6, có plugin | Chất lượng hội thoại tiếp tục tăng |
| 2025–2026 | Study mode + memory, theo dõi tiến độ qua phiên (nguồn thứ ba) | "ChatGPT không nhớ lịch sử" không còn đúng |

**Đánh giá lại các lợi thế dựa trên tính năng AI:**

| Lợi thế ở v1.2 | Còn đứng vững? |
|---|---|
| Mô phỏng phòng thi Speaking | ❌ Yếu đi nhiều |
| Chấm phát âm định lượng theo âm vị | ⚠️ Nhiều khả năng ChatGPT chưa có, nhưng ai cũng mua được API; app chuyên phát âm đã làm từ lâu |
| Lỗi đặc trưng của người Việt | ⚠️ Trùng với các app phát âm hiện có |
| Insight xuyên kỹ năng | ✅ Riêng nhưng khó bán |
| Điểm nhất quán | ✅ Đúng (IELTS 04/2026 nêu hạn chế về chuẩn hóa của AI hội thoại) — giờ là **nền móng** cho hiệu chỉnh |

**Lợi thế v2.0 — thứ ChatGPT về cấu trúc không có:**

| # | Lợi thế | Vì sao ChatGPT không làm được | Bền vững? |
|---|---|---|---|
| A | **Dự đoán band thật**, công bố sai số đo trên N kết quả thi thật của người Việt | Không có dữ liệu ghép cặp "bài luyện ↔ điểm thật"; không chịu trách nhiệm về kết quả | **Có** — dữ liệu tích lũy theo thời gian, đối thủ đến sau không sao chép được |
| C | **Cohort cam kết**: hạn chót, đặt cọc, nhắc học chủ động mỗi ngày | Chỉ phản hồi khi người dùng hỏi; không có cơ chế cam kết | Trung bình — cộng đồng cohort tạo gắn kết |
| A+C | **Cohort nuôi dữ liệu cho A**: điều kiện hoàn cọc gồm gửi phiếu điểm thật | — | Vòng quay dữ liệu tự vận hành |

**Nguồn:** [TechCrunch 07/2026](https://techcrunch.com/2026/07/08/openai-releases-new-voice-models-for-more-natural-live-conversations/) · [9to5Mac 09/2026](https://9to5mac.com/2026/09/23/openai-just-upgraded-chatgpt-voice-in-three-ways/) · [Windows Report — pronunciation audio](https://windowsreport.com/chatgpt-gets-pronunciation-audio-world-cup-hub-faster-photo-uploads-more/) · [IELTS 04/2026](https://ielts.org/news-and-insights/exploring-the-potential-of-conversational-ai-in-speaking-assessment) · [OpenAI Help — Study mode](https://help.openai.com/en/articles/11780217-chatgpt-study-mode-faq) · [Twilio — OpenAI + Azure pronunciation](https://www.twilio.com/en-us/blog/ai-voice-analyze-pronunciation-twilio-programmable-voice-openai-azure-speech)

---

## 3. Business Objectives & KPI

> Tất cả ngưỡng dưới đây là **`[Đề xuất]`**, phải được Founder duyệt trước khi mở beta (TBD-01).

| # | Objective | KPI / Success Metric | Deadline |
|---|---|---|---|
| O1 | Chứng minh chất lượng feedback đủ dùng | (a) Tỉ lệ đánh giá 👍 trên report ≥ 70% (đo riêng từng kỹ năng); (b) chấm lại cùng một bài trong eval set: chênh lệch overall band ≤ 0,5 ở ≥ 90% bài; (c) 0 trường hợp trích dẫn bằng chứng không có trong bài/transcript | Tuần 15 (trước open beta) |
| O2 | Chứng minh learning loop | ≥ 30% người đã nhận report có thực hiện Redo/Rewrite hoặc Retest trong 14 ngày | Tuần 22 |
| O3 | Chứng minh sẵn sàng trả tiền | ≥ 10 người trả phí **và** tỉ lệ chuyển đổi ≥ 3% trên người dùng hoạt động (≥ 1 bài nộp) trong 30 ngày | Tuần 22 |
| O4 | Unit economics dương | Chi phí AI ≤ 30% doanh thu thuần/người trả phí; chi phí trung bình ≤ 1.500đ/lượt Writing và ≤ 5.000đ/bài thi Speaking đủ 3 Part | Tuần 22 |
| O5 | Activation & retention | ≥ 60% người đăng ký nộp bài đầu tiên trong 7 ngày; ≥ 20% người dùng hoạt động quay lại ở tuần thứ 4 | Tuần 22 |
| O6 | Chứng minh "Band thật" là lý do mua | ≥ 50% người trả phí đã xem Dự đoán band trước khi thanh toán; ≥ 50% người trả lời khảo sát chọn dự đoán band hoặc cohort là lý do chính | Tuần 22 |
| O7 | Thu thập dữ liệu điểm thật (nguồn 1 + cohort) | ≥ 50 cặp hợp lệ/kỹ năng trước tuần 22; ≥ 300 cặp/kỹ năng trước tháng 8 | Tuần 22 / tháng 8 |
| O8 | Độ chính xác dự đoán | Sai số tuyệt đối trung bình (MAE) ≤ 0,5 band trên ≥ 100 cặp kiểm tra/kỹ năng không dùng để hiệu chỉnh | Tháng 8–11 |
| O9 | Cohort | ≥ 60% thành viên hoàn thành ≥ 80% lộ trình; ≥ 70% thành viên đã thi gửi phiếu điểm | Sau cohort thứ 2 |
| O10 | Chất lượng đề L/R | 100% đề publish qua quality gate L/R (§11.3); ≤ 2% câu hỏi bị báo lỗi đáp án được xác nhận sau khi publish; mỗi đề dùng cho dự đoán có ≥ 50 lượt làm để kiểm tra thống kê `[Đề xuất]` | Tuần 22 |

**Lưu ý:** 300 lượt đăng ký (mục tiêu v1.0) được giữ làm chỉ số theo dõi acquisition, **không** dùng làm tiêu chí thành công.

---

## 4. Stakeholders

| Role | Người/đơn vị | Trách nhiệm | Influence | Interest |
|---|---|---|---|---|
| Sponsor / Product Owner / BA / Dev | Founder | Ngân sách, ưu tiên, phát triển, duyệt | High | High |
| End-user chính | Người học IELTS Academic tại VN (phân khúc cụ thể: `TBD-01`) | Sử dụng, trả phí, phản hồi | Low | High |
| Beta tester | 20–50 người học | Kiểm chứng giả thuyết, UAT | Med | High |
| AI provider | Nhà cung cấp LLM (`TBD-04`) | Chấm bài, tạo nội dung | Med | Low |
| Speech provider | Nhà cung cấp STT và chấm phát âm (`TBD-04`) | Chuyển giọng nói thành văn bản, phân tích phát âm | Med | Low |
| Payment provider | `TBD-07` (ưu tiên hỗ trợ VietQR / ví điện tử) | Thu tiền, webhook | Med | Low |
| Cố vấn pháp lý | `TBD-12` | Privacy, điều khoản, người chưa thành niên | Med | Low |
| Chuyên gia IELTS | Chưa có — tuyển sau | Đánh giá độc lập chất lượng chấm | High (uy tín) | Med |
| Giáo viên / trung tâm (tương lai) | Kênh B2B2C tiềm năng | Dùng công cụ chấm cho học viên | Med | Med |

---

## 5. Scope

### 5.1 Release plan (đa kỳ thi, có gate)

| Release | Nội dung | Điều kiện mở (Gate) | Thời điểm |
|---|---|---|---|
| **R1 — IELTS Lab "Band thật"** | Đủ 4 kỹ năng Academic làm công cụ đo (Listening, Reading, Speaking Part 1–3, Writing Task 1/2); dự đoán band từng kỹ năng + overall; thu thập & hiệu chỉnh bằng điểm thật; Cohort cam kết + nhắc học; credit & thanh toán | — | Tuần 1–22 (roadmap §18) |
| R1.5 — Cam kết theo kết quả | Hoàn tiền nếu điểm thật thấp hơn dự đoán quá ngưỡng | **O8 đạt** + rà soát pháp lý (TBD-18) | Dự kiến tháng 8–11 |
| ~~R2 — Listening/Reading~~ | Đã gộp vào R1 ở v2.1 | — | — |
| R3 — TOEIC Listening & Reading | 7 Part, bảng quy đổi điểm, drill từ vựng | IELTS: conversion ≥ 3%, AI cost ≤ 30% doanh thu, W4 retention đạt O5 `[Đề xuất]` | Sau R2 |
| R4 — SAT (Digital) | Adaptive theo module, Math (LaTeX, máy tính), luồng đồng ý của phụ huynh | R3 đạt gate tương đương; rà soát pháp lý cho người chưa thành niên | Sau R3 |

### 5.2 In-Scope (R1)

- ✅ Đăng ký/đăng nhập, quản lý tài khoản, xóa dữ liệu
- ✅ Diagnostic khi onboarding: 1 lượt Speaking Part 1 (mặc định) + 1 bài Writing Task 2 (tùy chọn)
- ✅ **Speaking Part 1–3**: mô phỏng phòng thi với giám khảo AI, ghi âm, transcript, report 4 tiêu chí
- ✅ **Chấm phát âm dựa trên audio** và **lỗi đặc trưng của người Việt**
- ✅ Nộp bài Writing Academic Task 1 và Task 2 (Exam Mode + Practice Mode, autosave)
- ✅ AI report theo 4 tiêu chí, bằng chứng, inline highlight, nhãn "ước lượng — không chính thức"
- ✅ Error Memory **xuyên kỹ năng**, Redo (Speaking) / Rewrite (Writing), Retest bằng đề tương đương
- ✅ Drill mục tiêu (nội dung tạo sẵn và cache)
- ✅ Lịch sử & tiến bộ Speaking và Writing
- ✅ Free / Premium tháng / gói 3 tháng, hệ thống credit, thanh toán
- ✅ AI Gateway: phân loại dữ liệu, model chấm cố định, caching, circuit breaker, trần chi phí
- ✅ Admin: user, usage/cost, feedback, import nội dung
- ✅ Data model sẵn sàng đa kỳ thi (không làm tính năng TOEIC/SAT)
- ✅ **Nguồn 4:** đăng ký bộ dữ liệu công khai kèm license; chỉ dùng bộ có quyền thương mại (F21)
- ✅ **Dự đoán band Speaking và Writing** có khoảng sai số; trạng thái "chưa hiệu chỉnh" trước khi đủ dữ liệu (F16)
- ✅ **Thu thập kết quả thi thật** tự nguyện, có phần thưởng, xác minh và bảo vệ dữ liệu (F17)
- ✅ **Hiệu chỉnh** và công bố sai số đo được (F18)
- ✅ **Cohort 8 tuần** có ngày thi mục tiêu, đặt cọc hoàn lại (F19) và **nhắc học chủ động** (F20)
- ✅ **Listening & Reading Academic** đủ 40 câu mỗi kỹ năng, đề AI soạn + người duyệt, bảng quy đổi band riêng từng đề (F22–F24)
- ✅ **Full mock 4 kỹ năng** liền mạch (Listening → Reading → Writing, Speaking làm riêng như thi thật)

### 5.3 Out-of-Scope (R1)

- ❌ Listening/Reading dạng General Training
- ❌ General Training Task 1 (letter) — có thể thêm sau vì dùng chung engine
- ❌ TOEIC, SAT — R3/R4
- ❌ Hội thoại Speaking tự do ngoài cấu trúc bài thi, luyện giọng bản ngữ theo vùng miền
- ❌ Upload tài liệu để chuyển thành bài luyện — rủi ro bản quyền
- ❌ AI Companion, Skill Garden 4 kỹ năng, streak/reward nâng cao
- ❌ App native iOS/Android, push notification
- ❌ Marketplace gia sư, social feed, hồ sơ công khai
- ❌ Cam kết hoàn tiền theo kết quả — chỉ bật ở R1.5 khi O8 đạt
- ❌ Chứng nhận điểm; tuyên bố tương đương giám khảo
- ❌ Crawl hoặc nhập đề từ sách có bản quyền, website luyện thi, hay đề thi thật do thí sinh nhớ lại (FR-215)
- ❌ Huấn luyện foundation model; dữ liệu người dùng chỉ dùng cho hiệu chỉnh khi có consent riêng (FR-171)
- ❌ Thu thập hoặc lưu nội dung câu hỏi của đề thi thật
- ❌ Cào dữ liệu từ mạng xã hội

### 5.4 Boundaries / Interfaces

- Browser/PWA ↔ Next.js ↔ FastAPI (HTTPS)
- FastAPI ↔ AI Gateway ↔ các AI provider và speech provider bên ngoài (STT, chấm phát âm, TTS giọng giám khảo)
- FastAPI ↔ Payment adapter ↔ Payment provider (webhook)
- FastAPI ↔ Email provider; FastAPI ↔ Google OAuth; FastAPI ↔ kênh nhắn tin (Zalo OA hoặc thay thế, `TBD-16`)

---

## 6. Business Requirements

| ID | Description | Priority | Rationale | Source |
|---|---|---|---|---|
| BR-001 | Người học PHẢI nộp được bài IELTS Academic Writing Task 1 và Task 2 và nhận report AI theo 4 tiêu chí, có bằng chứng trong bài | M | Kỹ năng thứ hai của R1 | O1, N1 |
| BR-002 | Hệ thống PHẢI ghi nhớ lỗi lặp lại ở cả Speaking và Writing và cho phép Redo/Rewrite/Retest để kiểm chứng lỗi đã sửa | M | Điểm khác biệt so với chatbot/đối thủ | O2, N3, N4 |
| BR-003 | Hệ thống PHẢI thu phí qua Premium 69.000đ/tháng và gói 3 tháng, dựa trên credit; Free cấp theo tổng số lượt | M | Kiểm chứng sẵn sàng trả tiền | O3 |
| BR-004 | Chi phí AI PHẢI được kiểm soát dưới trần ngân sách theo tháng và theo người dùng | M | Rủi ro tài chính lớn nhất của sản phẩm AI | O4 |
| BR-005 | Bài làm và dữ liệu cá nhân của người dùng CHỈ được gửi tới provider có cam kết không dùng dữ liệu để huấn luyện | M | Privacy, pháp lý, uy tín | §12 |
| BR-006 | Việc chấm PHẢI nhất quán giữa các lần để so sánh tiến bộ có ý nghĩa | M | Error Memory và Retest phụ thuộc vào điểm nhất quán | O1, O2 |
| BR-007 | Tài khoản PHẢI an toàn, dữ liệu giữa người dùng PHẢI được cách ly | M | Bảo mật cơ bản | — |
| BR-008 | Bài đang viết và bản ghi âm đã thu KHÔNG được mất khi reload hoặc mất mạng tạm thời | M | Mất bài = mất niềm tin | O5 |
| BR-009 | Hệ thống PHẢI cung cấp số liệu vận hành (usage, chi phí, lỗi, feedback) cho Founder | M | Điều hành một mình | O1, O4 |
| BR-010 | Data model và entitlement PHẢI hỗ trợ thêm kỳ thi mới mà không đổi cấu trúc lõi | M | Chi phí thấp nếu làm bây giờ, rất cao nếu làm sau | §15 |
| BR-011 | Hệ thống NÊN đề xuất drill mục tiêu dựa trên điểm yếu | S | Tăng giá trị gói Premium | O2 |
| BR-012 | Hệ thống NÊN hiển thị tiến bộ Speaking và Writing theo thời gian | S | Retention | O5 |
| BR-013 | Người dùng NÊN chia sẻ được report (opt-in) | S | Kênh tăng trưởng tự nhiên | O3 |
| BR-014 | Hệ thống NÊN gửi email nhắc học cho người opt-in | S | Retention | O5 |
| BR-015 | Hệ thống CÓ THỂ có referral có chống lạm dụng | C | Tăng trưởng | O3 |
| BR-016 | Người học PHẢI luyện được Speaking Part 1–3 trong môi trường mô phỏng phòng thi và nhận report theo 4 tiêu chí, trong đó phát âm được đánh giá bằng phân tích audio | M | **Tính năng chính**, lý do không dùng ChatGPT | O1, O6, N5, N6 |
| BR-017 | Người học PHẢI làm được bài Listening và Reading Academic đủ 40 câu, đúng thời gian, chấm theo đáp án và quy đổi band theo bảng riêng của từng đề | M | Cần cho dự đoán overall (A) | O6, O8 |
| BR-018 | TOEIC, SAT | W | R3/R4 | — |
| BR-019 | Upload tài liệu, AI Companion, gamification nâng cao | W | Rủi ro bản quyền / không phải cốt lõi | — |
| BR-020 | Hệ thống PHẢI nhận diện và giải thích các lỗi đặc trưng của người Việt trong phát âm và ngữ pháp | M | Khác biệt so với feedback chung chung của AI tổng quát | O6, N5 |
| BR-021 | Hệ thống NÊN chỉ ra lỗi xuất hiện ở cả Speaking và Writing (insight xuyên kỹ năng) | S | Chỉ có được khi một hệ thống thấy cả hai kỹ năng | O2 |
| BR-022 | Hệ thống PHẢI dự đoán band Listening, Reading, Speaking, Writing và overall khi thi thật, kèm khoảng sai số và nêu rõ đã/chưa được hiệu chỉnh | M | **Lợi thế A** | O6, O8, N7 |
| BR-023 | Hệ thống PHẢI cho phép người dùng tự nguyện gửi kết quả thi thật, có consent riêng, xác minh chống gian lận và phần thưởng | M | Nguồn dữ liệu cho A | O7 |
| BR-024 | Hệ thống PHẢI hiệu chỉnh dự đoán bằng dữ liệu điểm thật và chỉ công bố độ chính xác bằng số liệu đo được | M | Tuyên bố trung thực, tránh quảng cáo sai | O8 |
| BR-025 | Mọi bộ dữ liệu bên ngoài PHẢI được đăng ký kèm license; chỉ bộ có quyền dùng thương mại mới được đưa vào phát triển/đánh giá sản phẩm | M | Rủi ro pháp lý (đa số bộ dữ liệu phù hợp là phi thương mại, §16) | §12 |
| BR-026 | Người học PHẢI tham gia được cohort 8 tuần có ngày thi mục tiêu và lộ trình | M | **Lợi thế C**; nguồn dữ liệu cao chất lượng cho A | O9, N8 |
| BR-027 | Hệ thống NÊN chủ động nhắc học mỗi ngày qua kênh người học dùng (email, Zalo nếu khả thi) | S | ChatGPT chỉ phản hồi khi được hỏi | O5, O9 |
| BR-028 | Cohort NÊN có đặt cọc hoàn lại khi hoàn thành lộ trình và gửi phiếu điểm | S | Cơ chế cam kết; cần rà soát pháp lý | O9, O7 |
| BR-029 | Hoàn tiền theo kết quả thi thật | W | Chỉ bật ở R1.5 khi O8 đạt | — |
| BR-030 | Đề Listening/Reading PHẢI do hệ thống tự soạn (AI + người duyệt) hoặc có quyền sử dụng; KHÔNG crawl, KHÔNG dùng đề có bản quyền hay đề thi thật | M | Pháp lý và uy tín của "band thật" | O10, §12 |

### MoSCoW Distribution (R1)

| Priority | Count | % in-scope |
|---|---|---|
| Must | 19 | 70% |
| Should | 7 | 26% |
| Could | 1 | 4% |
| **Total in-scope** | **27** | **100%** |
| Won't (R1) | 3 | — |

> ⚠️ Must chiếm 70% số BR; Speaking và kho đề L/R làm tăng effort đáng kể. Theo quy tắc 60/40, **effort** của nhóm Must nên ≤ 60% capacity; §18 đưa các BR Should về cuối timeline và liệt kê thứ tự cắt scope.

---

## 7. Overall Description

### 7.1 User Classes

| Class | Mô tả | Tech Skill | Frequency |
|---|---|---|---|
| Guest | Truy cập landing page, thử công cụ miễn phí | Low | Một lần |
| Free Learner | Có tài khoản, dùng credit miễn phí | Low–Med | Hàng tuần |
| Premium Learner | Trả phí theo tháng hoặc gói 3 tháng | Low–Med | 3–5 lần/tuần |
| Admin | Founder | High | Hằng ngày |

### 7.2 Persona (giả thuyết, chờ xác nhận ở TBD-01)

| Persona | Mô tả | Nhu cầu chính |
|---|---|---|
| P1 — Sinh viên cần chuẩn đầu ra | 19–22 tuổi, mục tiêu 5.5–6.5 Academic | Biết lỗi, lên band với chi phí thấp |
| P2 — Học sinh xét tuyển / du học | 16–18 tuổi (**có thể chưa thành niên**), mục tiêu 6.5–7.5 | Luyện nói và viết đều đặn, thấy tiến bộ |
| P3 — Người đi làm tự học | 23–30 tuổi, ít thời gian | Buổi luyện ≤ 30 phút, nhận report ≤ 90 giây (NFR-P01) |

### 7.3 Operating Environment

- Trình duyệt: Chrome, Edge, Safari, Firefox — 2 phiên bản mới nhất; iOS Safari ≥ 16; Android Chrome ≥ 2 phiên bản mới nhất.
- Thiết bị: desktop, tablet, mobile; chiều rộng tối thiểu 360px. Writing Exam Mode khuyến nghị bàn phím vật lý (hiển thị cảnh báo trên mobile).
- Speaking cần micro và quyền ghi âm của trình duyệt; khuyến nghị tai nghe có micro, phòng yên tĩnh. Danh sách trình duyệt/thiết bị ghi âm được hỗ trợ: `TBD-14`.

### 7.4 Design & Implementation Constraints

- Stack: xem §2.6. API key AI/payment chỉ nằm ở backend.
- Không train foundation model; dùng AI API bên ngoài qua AI Gateway.
- Nội dung đề: tự biên soạn hoặc có quyền sử dụng; biểu đồ Task 1 do hệ thống tự tạo từ dữ liệu.

### 7.5 Assumptions & Dependencies

| ID | Assumption / Dependency |
|---|---|
| A1 | Có ít nhất một AI provider trả phí có cam kết không huấn luyện trên dữ liệu API, với chi phí chấm ≤ 1.500đ/bài `[Đề xuất]` — cần xác minh ở tuần 1 |
| A2 | Founder đủ điều kiện pháp lý (cá nhân/hộ kinh doanh/doanh nghiệp) để mở tài khoản với payment provider — cần xác minh ở tuần 1 |
| A3 | Founder hoặc cộng tác viên biên soạn đủ đề Writing cho R1 (xem FR-044) |
| A4 | Người học chấp nhận band là ước lượng nếu feedback cụ thể và có bằng chứng |
| A5 | Có speech provider (STT + chấm phát âm ở mức âm/từ) có cam kết không huấn luyện trên dữ liệu, chi phí ≤ 5.000đ/bài thi Speaking đủ 3 Part `[Đề xuất]` — **phải xác minh ở tuần 1**; nếu vượt thì xem lại giá/credit |
| A6 | STT đủ chính xác với giọng tiếng Anh của người Việt để transcript dùng làm bằng chứng — kiểm chứng bằng eval set Speaking ở tuần 3 |
| A7 | Người vừa thi IELTS sẵn sàng làm 1 bài thi thử và gửi phiếu điểm để đổi phần thưởng — **kiểm chứng bằng bài đăng mời thử trong tuần 1** (≥ 20 người đồng ý `[Đề xuất]`) |
| A8 | Xin được license thương mại cho ít nhất một bộ dữ liệu có người nói tiếng Việt, **hoặc** tự xây eval set đủ dùng từ tình nguyện viên có consent (TBD-15) |
| A9 | Có kênh nhắn tin chủ động hợp lệ (Zalo OA hoặc thay thế) với chi phí chấp nhận được (TBD-16) |
| D1 | Google OAuth, email provider, object storage, VPS hoạt động ổn định |

---

## 8. Functional Requirements

> Mỗi FR trace về BR. AC viết theo Given-When-Then cho kịch bản chính và kịch bản lỗi; FR đơn giản dùng danh sách tiêu chí.

### 8.1 Feature F1 — Tài khoản & bảo mật (Priority: M)

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-001 | Hệ thống PHẢI cho phép đăng ký/đăng nhập bằng Google OAuth | BR-007 | AC-F1-1 |
| FR-002 | Hệ thống PHẢI cho phép đăng ký/đăng nhập bằng email + mật khẩu (mật khẩu hash, không lưu plaintext) | BR-007 | AC-F1-2 |
| FR-003 | Hệ thống PHẢI cho phép reset mật khẩu bằng link hết hạn sau ≤ 30 phút, không tiết lộ email có tồn tại hay không | BR-007 | AC-F1-3 |
| FR-004 | Hệ thống PHẢI kiểm tra quyền sở hữu ở server cho mọi bài làm, report, giao dịch | BR-007 | AC-F1-4 |
| FR-005 | Hệ thống PHẢI cho phép người dùng xóa tài khoản và dữ liệu học tập, hiển thị rõ dữ liệu nào bị xóa/giữ lại theo nghĩa vụ pháp lý (VD: chứng từ thanh toán) | BR-005, BR-007 | AC-F1-5 |
| FR-006 | Hệ thống PHẢI hiển thị điều khoản và thông báo quyền riêng tư (gồm việc xử lý bài làm và **ghi âm giọng nói** qua AI/speech provider, thời hạn lưu audio 30 ngày) và ghi nhận chấp thuận trước lần nộp bài hoặc ghi âm đầu tiên | BR-005 | AC-F1-6 |

**Acceptance Criteria**

- **AC-F1-1** — Given người dùng chưa có tài khoản, When đăng nhập bằng Google và cấp quyền, Then tài khoản được tạo và người dùng vào màn hình onboarding.
- **AC-F1-2** — Given đã đăng ký bằng email, When nhập sai mật khẩu 5 lần trong 15 phút, Then các lần thử tiếp theo bị chặn 15 phút và thông báo không tiết lộ tài khoản có tồn tại.
- **AC-F1-3** — Given link reset đã tạo quá 30 phút, When người dùng mở link, Then hệ thống từ chối và cho phép yêu cầu link mới.
- **AC-F1-4** — Given người dùng A đăng nhập, When gọi API lấy report của người dùng B bằng ID, Then API trả 404 và không lộ dữ liệu.
- **AC-F1-5** — Given người dùng xác nhận xóa tài khoản, When quá trình xóa hoàn tất, Then bài làm/report/Error Memory không còn truy cập được và người dùng nhận email xác nhận.
- **AC-F1-6** — Given người dùng chưa chấp thuận thông báo xử lý dữ liệu, When bấm nộp bài lần đầu, Then hệ thống hiển thị thông báo và chỉ gửi bài đi chấm sau khi người dùng chấp thuận.

### 8.2 Feature F2 — Onboarding & Diagnostic (Priority: M)

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-010 | Hệ thống PHẢI cho phép nhập band mục tiêu và ngày thi dự kiến (không bắt buộc, sửa được) | BR-001 | Có thể bỏ qua; sửa trong Settings |
| FR-011 | Hệ thống PHẢI cung cấp diagnostic gồm 1 lượt **Speaking Part 1** (4–5 câu, mặc định) và 1 bài **Writing Task 2** (tùy chọn); các lượt chấm diagnostic không trừ credit | BR-016, BR-001, BR-003 | AC-F2-1 |
| FR-012 | Sau diagnostic, hệ thống PHẢI hiển thị 3 điểm yếu ưu tiên kèm bằng chứng và gợi ý bước tiếp theo | BR-002 | AC-F2-2 |
| FR-013 | Hệ thống PHẢI phân biệt rõ mục tiêu do người dùng khai báo và ước lượng do AI tạo | BR-006 | Nhãn riêng trên UI |

- **AC-F2-1** — Given người dùng mới hoàn tất đăng ký, When hoàn thành Speaking Part 1 diagnostic (và nộp Writing Task 2 nếu chọn), Then nhận report cho từng phần đã làm và số credit không thay đổi.
- **AC-F2-2** — Given report diagnostic có ≥ 3 lỗi được phân loại, When hiển thị kết quả, Then có đúng 3 điểm yếu ưu tiên, mỗi điểm có ≥ 1 trích dẫn từ bài và 1 nút "Luyện điểm này".

### 8.3 Feature F3 — Làm bài Writing (Priority: M)

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-020 | Hệ thống PHẢI hỗ trợ Academic Task 1 (mô tả biểu đồ/bảng/quy trình/bản đồ) và Task 2 (essay) | BR-001 | AC-F3-1 |
| FR-021 | Exam Mode PHẢI có đồng hồ đếm ngược (Task 1: 20 phút, Task 2: 40 phút, cấu hình theo metadata đề), đếm số từ, không hiển thị gợi ý trước khi nộp | BR-001 | AC-F3-2 |
| FR-022 | Practice Mode PHẢI cho phép tạm dừng/tiếp tục, không giới hạn thời gian | BR-001 | Pause/resume hoạt động |
| FR-023 | Hệ thống PHẢI lưu bản nháp local ≤ 5 giây sau lần gõ cuối và đồng bộ server khi online, hiển thị trạng thái đồng bộ | BR-008 | AC-F3-3 |
| FR-024 | Hệ thống PHẢI dùng version/timestamp để không ghi đè bản mới hơn bằng bản cũ; khi xung đột, cho người dùng chọn bản giữ lại | BR-008 | AC-F3-4 |
| FR-025 | Bài đã nộp PHẢI ở chế độ chỉ đọc; nộp lặp không tạo lượt chấm trùng và không trừ credit hai lần | BR-003, BR-008 | AC-F3-5 |
| FR-026 | Hệ thống PHẢI cảnh báo (không chặn) khi bài dưới số từ tối thiểu (150/250) | BR-001 | Cảnh báo hiển thị trước khi nộp |
| FR-027 | Hệ thống PHẢI kiểm tra số credit trước khi nộp và hiển thị số credit còn lại | BR-003 | AC-F3-6 |

- **AC-F3-1** — Given đề Task 1 dạng biểu đồ cột, When người học mở đề, Then biểu đồ hiển thị rõ trên màn hình ≥ 360px và có thể phóng to.
- **AC-F3-2** — Given Exam Mode Task 2 đang chạy, When hết 40 phút, Then bài được tự động nộp (hoặc lưu chờ nộp nếu offline) và người học được thông báo.
- **AC-F3-3** — Given người học đang viết, When reload trình duyệt, Then nội dung đã gõ đến trước thời điểm reload ≤ 5 giây được khôi phục.
- **AC-F3-4** — Given bài được mở trên 2 tab, When tab cũ đồng bộ bản cũ hơn, Then server không ghi đè bản mới hơn và tab cũ nhận thông báo xung đột.
- **AC-F3-5** — Given người học bấm "Nộp" 2 lần liên tiếp, When hệ thống xử lý, Then chỉ có 1 lượt chấm và trừ tối đa 1 credit.
- **AC-F3-6** — Given người dùng Free đã hết credit, When bấm "Nộp", Then bài vẫn được lưu, hệ thống hiển thị lựa chọn nâng cấp và không gửi đi chấm.

### 8.4 Feature F4 — AI Writing Report (Priority: M)

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-030 | Report PHẢI có band ước lượng cho 4 tiêu chí (Task Achievement/Task Response, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy) và overall | BR-001 | AC-F4-1 |
| FR-031 | Mỗi nhận xét quan trọng PHẢI trỏ tới đoạn/câu trong bài (vị trí + trích đoạn); trích đoạn PHẢI khớp nguyên văn với bài nộp | BR-001, BR-006 | AC-F4-2 |
| FR-032 | Report PHẢI có inline highlight: lỗi, giải thích, gợi ý sửa | BR-001 | Click highlight mở giải thích |
| FR-033 | Report PHẢI có mục điểm mạnh, điểm yếu và 1–3 hành động tiếp theo | BR-001 | Có đủ 3 mục |
| FR-034 | Mọi band PHẢI có nhãn "Ước lượng bởi AI — không phải điểm IELTS chính thức" | BR-001 | Nhãn hiển thị cạnh mọi band |
| FR-035 | Với Task 1, AI PHẢI nhận dữ liệu gốc của biểu đồ để kiểm tra độ chính xác số liệu người học mô tả | BR-001 | AC-F4-3 |
| FR-036 | Khi bài quá ngắn, lạc đề hoặc không phải tiếng Anh, report PHẢI nêu giới hạn và không đưa band cho tiêu chí không đủ bằng chứng | BR-006 | AC-F4-4 |
| FR-037 | Report PHẢI lưu model, provider, phiên bản prompt và phiên bản rubric đã dùng | BR-006, BR-009 | Metadata có trong DB và trang admin |
| FR-038 | Trạng thái chấm PHẢI hiển thị: đang chờ / đang chấm / hoàn tất / lỗi; lỗi cho phép thử lại mà không trừ credit | BR-003, BR-008 | AC-F4-5 |
| FR-039 | Mở lại report cũ KHÔNG trừ credit | BR-003 | Credit không đổi |

- **AC-F4-1** — Given bài Task 2 hợp lệ, When chấm hoàn tất, Then report có 4 band tiêu chí + overall, mỗi band là bội số của 0,5 trong khoảng 0–9.
- **AC-F4-2** — Given output AI chứa trích đoạn không có trong bài, When hệ thống validate, Then nhận xét đó bị loại (hoặc chấm lại) và sự kiện được ghi log; người học không bao giờ thấy trích đoạn không tồn tại.
- **AC-F4-3** — Given biểu đồ Task 1 có giá trị 45% và bài viết ghi 54%, When chấm, Then report đánh dấu sai số liệu tại câu tương ứng.
- **AC-F4-4** — Given bài Task 2 dài 60 từ, When chấm, Then report ghi rõ "bài quá ngắn để ước lượng đáng tin cậy" và không hiển thị overall band.
- **AC-F4-5** — Given provider trả lỗi sau khi đã retry và fallback, When lượt chấm thất bại, Then trạng thái là "lỗi", credit không bị trừ và người học có nút "Thử lại".

### 8.5 Feature F5 — Error Memory, Rewrite & Retest (Priority: M) — *điểm khác biệt chính*

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-040 | Hệ thống PHẢI gắn mỗi lỗi (Speaking hoặc Writing) với một error tag trong taxonomy chung (domain → subskill → error tag) và lưu bài/bản ghi nguồn | BR-002, BR-010 | AC-F5-1 |
| FR-041 | Hệ thống PHẢI đánh dấu lỗi "lặp lại" khi cùng error tag xuất hiện ở ≥ 2 bài khác nhau | BR-002 | AC-F5-1 |
| FR-042 | Rewrite (Writing) / Redo (Speaking): người học PHẢI làm lại được bài/câu trả lời đã chấm; hệ thống PHẢI so sánh bản gốc và bản làm lại, chỉ rõ lỗi nào đã sửa/chưa sửa | BR-002 | AC-F5-2 |
| FR-043 | Retest: hệ thống PHẢI gợi ý đề tương đương (cùng kỹ năng, cùng task type/Part, cùng chủ đề/dạng) nhắm vào lỗi lặp lại | BR-002 | AC-F5-3 |
| FR-044 | Ngân hàng đề R1 PHẢI đủ để Retest: ≥ 30 đề Writing Task 2, ≥ 15 đề Task 1, ≥ 20 chủ đề Speaking Part 1 (mỗi chủ đề 4–5 câu), ≥ 30 cue card Part 2 kèm câu hỏi Part 3, ≥ 6 bộ Listening và ≥ 6 bộ Reading trước open beta (≥ 12 mỗi loại trước tuần 22) `[Đề xuất]`, đã qua quality gate §11.3 | BR-002, BR-016, BR-017 | Đếm trong admin |
| FR-045 | Báo cáo tiến bộ PHẢI chỉ so sánh các report chấm cùng rubric version và cùng model chấm chính (xem FR-076) | BR-006 | AC-F5-4 |

- **AC-F5-1** — Given người học mắc lỗi "subject–verb agreement" ở 2 bài khác nhau, When report thứ hai hoàn tất, Then Error Memory hiển thị lỗi này là "lặp lại 2 lần" kèm liên kết tới cả 2 bài.
- **AC-F5-2** — Given bản gốc có 5 lỗi được gắn tag, When người học nộp bản sửa, Then report so sánh liệt kê từng lỗi với trạng thái "đã sửa" / "chưa sửa" / "lỗi mới".
- **AC-F5-3** — Given có lỗi lặp lại "thiếu ví dụ minh họa luận điểm", When người học bấm "Retest", Then hệ thống đề xuất ≥ 1 đề Task 2 chưa làm và ghi rõ lỗi đang được kiểm tra.
- **AC-F5-4** — Given 2 report dùng rubric version khác nhau, When hiển thị biểu đồ tiến bộ, Then 2 điểm được đánh dấu "khác phiên bản chấm" và không nối thành một đường xu hướng.

### 8.6 Feature F6 — Drill mục tiêu (Priority: S)

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-050 | Hệ thống NÊN mở drill ngắn (≤ 10 phút) từ một điểm yếu trong report | BR-011 | Nút "Luyện điểm này" mở drill đúng error tag |
| FR-051 | Drill do AI tạo PHẢI được gắn nhãn "AI tạo", qua kiểm tra cấu trúc và được **tạo sẵn, lưu và dùng lại** cho mọi người dùng (không tạo mới cho từng lượt) | BR-011, BR-004 | Drill chỉ gọi AI khi chưa có trong kho |
| FR-052 | Làm drill (chấm khách quan) KHÔNG trừ credit | BR-003 | Credit không đổi |

### 8.7 Feature F7 — Dashboard & lịch sử (Priority: S)

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-055 | Dashboard NÊN hiển thị: CTA "Thi thử Speaking" (nổi bật nhất) và "Viết bài mới", report gần nhất, top 3 lỗi lặp lại (đánh dấu lỗi xuyên kỹ năng), số credit còn lại | BR-012, BR-021 | 5 khối hiển thị |
| FR-056 | Lịch sử PHẢI liệt kê mọi bài đã nộp, lọc theo kỹ năng (Speaking/Writing) và Part/Task | BR-012 | Lọc hoạt động |
| FR-057 | Biểu đồ tiến bộ NÊN hiển thị band theo tiêu chí qua thời gian, tuân theo FR-045 | BR-012 | AC-F5-4 |

### 8.8 Feature F8 — Gói, credit & thanh toán (Priority: M)

**Business Rules**

| ID | Rule |
|---|---|
| RULE-01 | 1 credit = 1 lượt chấm Writing (Task 1 hoặc Task 2 hoặc bản Rewrite) **hoặc** 1 Part Speaking (Part 1, 2 hoặc 3, kể cả Redo) được xử lý thành công |
| RULE-02 | Free: 3 credit **tổng cộng** cho mỗi tài khoản `[Đề xuất]` + lượt diagnostic miễn phí (FR-011) |
| RULE-03 | Premium tháng: 69.000đ, 30 credit/tháng `[Đề xuất]`; credit không dùng hết hết hạn cuối kỳ |
| RULE-04 | Gói 3 tháng: 179.000đ `[Đề xuất]`, 90 credit dùng trong 3 tháng |
| RULE-05 | Bài thi Speaking đủ 3 Part = 3 credit `[Đề xuất]` |
| RULE-06 | Lỗi xử lý, nộp trùng, mở lại report, drill khách quan: không trừ credit |
| RULE-07 | Credit và entitlement dùng chung cho mọi kỳ thi trong tương lai (một ví credit/người dùng) |
| RULE-08 | Mốc reset credit tính theo múi giờ Asia/Ho_Chi_Minh và hiển thị trong UI |
| RULE-09 | Premium chỉ được kích hoạt sau khi thanh toán được xác minh (webhook có chữ ký, hoặc admin xác nhận thủ công có audit log trong giai đoạn beta) |

**Cơ sở con số (RULE-03, RULE-05):** doanh thu thuần ≈ 67.000đ/tháng.
- Trường hợp xấu nhất, dùng hết 30 credit cho Speaking: 10 bài thi × 5.000đ = 50.000đ, vẫn dưới doanh thu (≈ 75%).
- Dùng hết 30 credit cho Writing: 30 × 1.500đ = 45.000đ (≈ 67%).
- Mức dùng trung bình ~30–40% → chi phí ≈ 15.000–20.000đ ≈ 22–30% doanh thu, đạt O4.
- Nếu A5 cho thấy chi phí Speaking > 5.000đ/bài thi, phải tăng credit/Part hoặc giảm credit/tháng trước khi bán (tuần 16).

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-060 | Trang gói PHẢI hiển thị Free/Premium tháng/gói 3 tháng, số credit, giá, thời hạn, điều kiện hoàn tiền trước khi thanh toán | BR-003 | Đủ 5 thông tin |
| FR-061 | Hệ thống PHẢI tạo đơn thanh toán qua payment adapter tách biệt với provider | BR-003 | Đổi provider không đổi logic entitlement |
| FR-062 | Hệ thống PHẢI xử lý webhook/xác nhận thanh toán idempotent: sự kiện lặp không cấp quyền hay ghi giao dịch hai lần | BR-003 | AC-F8-1 |
| FR-063 | Hệ thống PHẢI quản lý trạng thái đơn: pending / paid / expired / failed / refunded và lưu lịch sử sự kiện, không lưu thông tin thẻ | BR-003 | Trạng thái hiển thị trong admin |
| FR-064 | Giai đoạn beta, admin CÓ THỂ xác nhận chuyển khoản thủ công (VietQR) với mã đơn duy nhất; mọi xác nhận được ghi audit log | BR-003 | AC-F8-2 |
| FR-065 | Người dùng PHẢI xem được gói hiện tại, ngày hết hạn, số credit còn lại và lịch sử giao dịch | BR-003 | Trang "Gói của tôi" |
| FR-066 | Hệ thống KHÔNG tự gia hạn trong R1; gửi email nhắc trước khi hết hạn 3 ngày (nếu opt-in) | BR-003, BR-014 | Không có giao dịch tự động |

- **AC-F8-1** — Given webhook "paid" cho đơn X đã được xử lý, When provider gửi lại cùng webhook, Then hệ thống trả 200, không cộng thêm credit và ghi log "duplicate".
- **AC-F8-2** — Given admin xác nhận đơn chuyển khoản, When xác nhận thành công, Then người dùng nhận Premium ≤ 1 phút và audit log ghi admin, thời gian, mã đơn, số tiền.

### 8.9 Feature F9 — AI Gateway (Priority: M)

**Phân loại dữ liệu (Business Rule)**

| Lớp | Dữ liệu | Provider được phép |
|---|---|---|
| **A — Dữ liệu người dùng** | Bài làm, **ghi âm giọng nói**, transcript, thông tin cá nhân | **Chỉ gói trả phí** có cam kết bằng văn bản không dùng dữ liệu để huấn luyện; ưu tiên có tùy chọn không lưu trữ |
| **B — Nội dung của hệ thống** | Tạo drill, giải thích, đề mẫu, biến thể đề từ nội dung của Founder | Bất kỳ provider nào, kể cả gói miễn phí |
| **C — Dev / đánh giá nội bộ** | Eval set tự biên soạn, dữ liệu tổng hợp | Bất kỳ, kể cả gói miễn phí |

**Quy tắc chung:** mỗi provider dùng **một tài khoản hợp lệ** theo điều khoản của provider đó; **không** tạo nhiều tài khoản/key để vượt hạn mức miễn phí.

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-076 | Mỗi rubric version PHẢI gắn với **một model chấm chính cố định**; đổi model chính = tạo rubric/prompt version mới và chạy lại eval set trước khi áp dụng | BR-006 | AC-F9-1 |
| FR-067 | Gateway PHẢI chặn mọi request Lớp A tới provider/model không nằm trong danh sách "được phép Lớp A" | BR-005 | AC-F9-2 |
| FR-068 | Gateway PHẢI có circuit breaker theo từng provider: mở mạch sau 3 lỗi (5xx/429/timeout) liên tiếp trong 60 giây, thử lại (half-open) sau 60 giây `[Đề xuất]`; khi mở mạch chuyển sang provider dự phòng đã cấu hình | BR-004, BR-008 | AC-F9-3 |
| FR-069 | Ưu tiên fallback cùng model qua provider khác; nếu phải dùng model khác, report PHẢI ghi "chấm bằng model dự phòng" và không đưa vào đường xu hướng (FR-045) | BR-006 | AC-F9-3 |
| FR-070 | Gateway PHẢI dùng prompt caching của provider cho phần rubric/system prompt cố định (đặt ở đầu prompt) | BR-004 | Tỉ lệ token được cache hiển thị trong admin |
| FR-071 | Gateway PHẢI chống chấm trùng: cùng (user, đề, nội dung bài đã chuẩn hóa, rubric version) → trả lại report đã có, không gọi AI, không trừ credit | BR-003, BR-004 | AC-F9-4 |
| FR-072 | Gateway KHÔNG được dùng semantic cache (trả kết quả của bài "gần giống") cho việc chấm | BR-006 | Kiểm tra code review |
| FR-073 | Gateway PHẢI ghi log cho mỗi request: provider, model, phiên bản prompt, latency, token, chi phí ước tính, trạng thái, retry/fallback — **không** ghi toàn văn bài làm vào log vận hành | BR-009, BR-005 | Log đủ trường, không có nội dung bài |
| FR-074 | Gateway PHẢI có trần chi phí theo tháng (toàn hệ thống) và theo provider; cảnh báo ở 50%/80%/100%; khi đạt 100%, tạm dừng tác vụ Lớp B/C trước, Lớp A tiếp tục đến trần khẩn cấp do Founder cấu hình | BR-004 | AC-F9-5 |
| FR-075 | Output AI PHẢI được validate theo JSON schema và khoảng điểm hợp lệ trước khi lưu | BR-006 | Output sai schema → retry tối đa 2 lần rồi báo lỗi |

- **AC-F9-1** — Given rubric v2 đang dùng model M1, When Founder đổi sang model M2, Then hệ thống yêu cầu tạo rubric v3 và chỉ kích hoạt sau khi eval set đạt ngưỡng O1(b).
- **AC-F9-2** — Given provider P chỉ có trong danh sách Lớp B, When có request chấm bài (Lớp A) được định tuyến tới P do cấu hình sai, Then gateway từ chối request và ghi cảnh báo.
- **AC-F9-3** — Given provider chính trả 429 ba lần trong 60 giây, When có bài mới cần chấm, Then bài được chuyển sang provider dự phòng, report ghi nhận fallback, và provider chính được thử lại sau 60 giây.
- **AC-F9-4** — Given người học nộp lại đúng nội dung bài đã chấm, When xử lý, Then trả report cũ trong ≤ 2 giây và credit không đổi.
- **AC-F9-5** — Given chi phí tháng đạt 80% trần, When vượt ngưỡng, Then Founder nhận email cảnh báo trong ≤ 15 phút.

### 8.10 Feature F10 — Admin & vận hành (Priority: M)

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-080 | Admin PHẢI xem danh sách người dùng, gói, credit, hoạt động gần nhất | BR-009 | Trang Users |
| FR-081 | Admin PHẢI xem AI usage: số request, token, chi phí ước tính theo ngày/provider/model, tỉ lệ lỗi, latency p50/p95, tỉ lệ cache | BR-009, BR-004 | Trang AI Usage |
| FR-082 | Admin PHẢI xem hộp feedback/báo lỗi AI, lọc theo loại (scoring, explanation, content, billing, account, technical) | BR-009 | Trang Feedback |
| FR-083 | Admin PHẢI import đề bằng JSON/Markdown, có validate schema, và chỉ publish khi qua quality gate §11.3 | BR-002 | Đề sai schema bị từ chối kèm lỗi cụ thể |
| FR-084 | Mọi hành động admin PHẢI được phân quyền và ghi audit log | BR-007 | Audit log có actor, action, time |
| FR-085 | Admin PHẢI xem funnel: đăng ký → nộp bài đầu → xem report → rewrite/retest → chạm hết credit → thanh toán | BR-009 | Trang Funnel, số liệu cho O2/O3/O5 |

### 8.11 Feature F11 — Feedback & chất lượng AI (Priority: M)

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-090 | Mỗi report PHẢI có 👍/👎 và nút "Báo feedback sai" | BR-001, BR-009 | Lưu kèm report ID, model, prompt version |
| FR-091 | Hệ thống PHẢI có eval set nội bộ tự biên soạn (≥ 40 bài Task 2, ≥ 20 bài Task 1, ≥ 30 bản ghi Speaking có người nói giọng Việt đã đồng ý cho dùng nội bộ `[Đề xuất]`) và chạy lại trước mọi thay đổi prompt/model/speech provider | BR-006, BR-016 | Báo cáo eval lưu theo version |
| FR-092 | Sản phẩm KHÔNG được quảng bá độ chính xác band khi chưa có đánh giá độc lập của chuyên gia | BR-001 | Rà soát nội dung landing page |

### 8.12 Feature F12 — Tăng trưởng (Priority: S/C)

| ID | Functional Requirement | Source BR | Priority |
|---|---|---|---|
| FR-095 | Người dùng NÊN tạo được link chia sẻ report (opt-in), xem trước nội dung, thu hồi được link; mặc định ẩn toàn văn bài | BR-013 | S |
| FR-096 | Landing page NÊN có công cụ miễn phí **"đọc thử 3 câu, xem bạn sai âm nào"** (giới hạn theo IP/thiết bị) để trình diễn chấm phát âm | BR-013, BR-020 | S |
| FR-097 | Hệ thống NÊN gửi email nhắc học (opt-in), có unsubscribe, tối đa 2 email/tuần `[Đề xuất]` | BR-014 | S |
| FR-098 | Hệ thống CÓ THỂ có referral: người giới thiệu và người được giới thiệu nhận credit sau khi người được giới thiệu **thanh toán** (chống lạm dụng) | BR-015 | C |

**Kênh tăng trưởng chính:** chọn **một** kênh ở `TBD-03`. Ứng viên: nhóm Facebook/cộng đồng IELTS (tặng chấm thử để đổi lấy feedback), TikTok/Shorts ("người Việt hay sai 5 âm này", "Speaking 5.5 → 6.5"), hoặc B2B2C qua giáo viên/trung tâm nhỏ.

### 8.13 Feature F13 — Speaking: mô phỏng phòng thi (Priority: M) — *tính năng chính*

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-100 | Hệ thống PHẢI cho phép thi thử Speaking đủ 3 Part liên tiếp hoặc luyện từng Part riêng | BR-016 | AC-F13-1 |
| FR-101 | Giám khảo AI PHẢI đọc câu hỏi bằng giọng nói (TTS) và hiển thị câu hỏi dạng chữ (có thể ẩn trong Exam Mode) | BR-016 | Câu hỏi phát bằng âm thanh; nút hiện/ẩn chữ |
| FR-102 | Part 1 PHẢI gồm 4–5 câu hỏi theo 1–2 chủ đề quen thuộc; mỗi câu trả lời được ghi âm riêng, tối đa 60 giây/câu `[Đề xuất]` | BR-016 | Ghi âm dừng ở 60 giây |
| FR-103 | Part 2 PHẢI hiển thị cue card, cho 1 phút chuẩn bị (có ô ghi chú), sau đó ghi âm tối đa 2 phút và tự dừng | BR-016 | AC-F13-2 |
| FR-104 | Part 3 PHẢI gồm 4–5 câu hỏi thảo luận liên quan chủ đề Part 2; **ít nhất 1 câu hỏi nối tiếp được tạo từ nội dung câu trả lời trước** (dựa trên transcript) | BR-016 | AC-F13-3 |
| FR-105 | Exam Mode Speaking KHÔNG cho nghe lại hay ghi âm lại trong lúc thi và không hiển thị feedback trước khi kết thúc; Practice Mode cho phép ghi âm lại từng câu | BR-016 | Nút ghi lại chỉ có ở Practice Mode |
| FR-106 | Trước bài thi, hệ thống PHẢI kiểm tra micro (quyền truy cập, mức âm, tạp âm) và hướng dẫn khắc phục khi không đạt | BR-016, BR-008 | AC-F13-4 |
| FR-107 | Mỗi bản ghi PHẢI được lưu local cho đến khi server xác nhận nhận đủ; mất mạng không làm mất bản ghi đã thu, và upload tự thử lại khi có mạng | BR-008 | AC-F13-5 |
| FR-108 | Bài thi bị gián đoạn (đóng tab, mất mạng) PHẢI tiếp tục được từ câu chưa hoàn thành; các câu đã ghi được giữ nguyên | BR-008 | AC-F13-6 |

- **AC-F13-1** — Given người học chọn "Thi thử đủ 3 Part", When hoàn thành Part 3, Then hệ thống nộp cả bài một lần, trừ 3 credit sau khi chấm thành công và hiển thị một report chung có phần riêng cho từng Part.
- **AC-F13-2** — Given Part 2 đang ở giai đoạn chuẩn bị, When hết 60 giây, Then ghi âm tự bắt đầu và tự dừng sau 2 phút; ghi chú của người học vẫn hiển thị trong lúc nói.
- **AC-F13-3** — Given ở Part 2 người học nói về "một chuyến đi đáng nhớ", When sang Part 3, Then có ≥ 1 câu hỏi nhắc tới nội dung người học vừa nói.
- **AC-F13-4** — Given trình duyệt bị từ chối quyền micro, When người học bấm "Bắt đầu thi", Then hệ thống không bắt đầu tính giờ và hiển thị hướng dẫn cấp quyền cho trình duyệt đang dùng.
- **AC-F13-5** — Given người học mất mạng sau khi ghi xong câu 3, When có mạng trở lại, Then bản ghi câu 3 được upload tự động và không phải ghi lại.
- **AC-F13-6** — Given người học đóng tab ở câu 2 của Part 3, When mở lại bài trong 24 giờ, Then bài tiếp tục từ câu 2 của Part 3.

### 8.14 Feature F14 — Speaking report & chấm phát âm (Priority: M)

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-110 | Report Speaking PHẢI có band ước lượng cho 4 tiêu chí (Fluency & Coherence, Lexical Resource, Grammatical Range & Accuracy, Pronunciation) và overall, kèm nhãn không chính thức | BR-016 | AC-F14-1 |
| FR-111 | Hệ thống PHẢI hiển thị transcript từng câu trả lời; nhận xét về từ vựng/ngữ pháp PHẢI trỏ tới đoạn trong transcript và trích đoạn PHẢI khớp nguyên văn transcript | BR-016, BR-006 | Validate như AC-F4-2 |
| FR-112 | Tiêu chí Pronunciation CHỈ được chấm khi có kết quả phân tích audio từ speech provider; KHÔNG suy ra phát âm từ transcript | BR-016 | AC-F14-2 |
| FR-113 | Report PHẢI đánh dấu từ/âm phát âm sai trên transcript; bấm vào từ PHẢI nghe lại được đoạn audio của chính người học và nghe mẫu phát âm chuẩn (TTS) | BR-016, BR-020 | AC-F14-3 |
| FR-114 | Fluency PHẢI dựa trên số liệu đo từ audio: tốc độ nói (từ/phút), số và độ dài khoảng ngừng, từ đệm (uh, um…) | BR-016 | Các số liệu hiển thị trong report |
| FR-115 | Khi audio kém (tạp âm, quá nhỏ) hoặc câu trả lời quá ngắn (< 10 giây/câu Part 1, < 45 giây Part 2 `[Đề xuất]`), report PHẢI nêu giới hạn và không đưa band cho tiêu chí thiếu bằng chứng | BR-006, BR-016 | AC-F14-4 |
| FR-116 | Hệ thống PHẢI hiển thị trạng thái xử lý (đang upload / đang chấm / hoàn tất / lỗi); lỗi cho phép thử lại mà không trừ credit và không phải ghi âm lại | BR-003, BR-008 | Như AC-F4-5 |
| FR-117 | Người học PHẢI xem được transcript để phát hiện chỗ STT nghe sai và báo lỗi transcript; lỗi chấm do STT sai (được xác nhận) được hoàn credit | BR-006, BR-009 | Nút "Transcript sai" trên từng câu |

- **AC-F14-1** — Given bài thi Speaking đủ 3 Part hợp lệ, When chấm hoàn tất, Then report có 4 band tiêu chí + overall, mỗi band là bội số của 0,5 trong khoảng 0–9, trong ≤ 120 giây (p95, NFR-P05).
- **AC-F14-2** — Given speech provider không trả được kết quả phân tích phát âm (lỗi hoặc không hỗ trợ), When tạo report, Then tiêu chí Pronunciation hiển thị "Chưa đánh giá được", không có band, và overall ghi rõ chỉ dựa trên 3 tiêu chí.
- **AC-F14-3** — Given từ "think" bị phát âm thành /tɪŋk/, When người học bấm vào từ đó trong report, Then nghe được đoạn audio của mình, nghe mẫu /θɪŋk/ và đọc giải thích lỗi /θ/.
- **AC-F14-4** — Given câu trả lời Part 2 chỉ dài 25 giây, When chấm, Then report ghi rõ "câu trả lời quá ngắn để ước lượng Fluency đáng tin cậy" và không hiển thị band Fluency cho Part 2.

### 8.15 Feature F15 — Lỗi đặc trưng của người Việt & insight xuyên kỹ năng (Priority: M/S)

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-120 | Taxonomy lỗi PHẢI có nhóm **"lỗi đặc trưng của người Việt"** cho phát âm và ngữ pháp (danh sách khởi đầu ở §14), mỗi lỗi có giải thích bằng tiếng Việt và bài luyện | BR-020 | AC-F15-1 |
| FR-121 | Report Speaking và Writing PHẢI gắn nhãn "lỗi thường gặp ở người Việt" cho các lỗi thuộc nhóm này và giải thích nguyên nhân (VD: tiếng Việt không có âm cuối bật hơi) | BR-020 | AC-F15-1 |
| FR-122 | Hệ thống NÊN tạo insight xuyên kỹ năng khi cùng một gốc lỗi xuất hiện ở cả Speaking và Writing (VD: bỏ -s ngôi thứ ba khi viết **và** nuốt âm /s/ cuối khi nói) trong 30 ngày gần nhất | BR-021 | AC-F15-2 |
| FR-123 | Insight xuyên kỹ năng CHỈ được hiển thị khi có ≥ 2 lần xuất hiện ở mỗi kỹ năng, kèm liên kết bằng chứng; không suy diễn từ tín hiệu yếu | BR-021, BR-006 | AC-F15-3 |
| FR-124 | Drill phát âm NÊN có dạng "nghe mẫu → đọc lại → chấm ngay" cho từng âm/lỗi đặc trưng; drill này dùng 0 credit và có giới hạn số lượt/ngày để kiểm soát chi phí (`[Đề xuất]` 20 lượt/ngày) | BR-011, BR-020, BR-004 | Drill hoạt động; vượt giới hạn → thông báo |

- **AC-F15-1** — Given người học bỏ âm /t/ cuối trong "want", "just", "most" ở bài Speaking, When report hoàn tất, Then các từ này được gắn nhãn "mất âm cuối — lỗi thường gặp ở người Việt" kèm giải thích tiếng Việt và nút "Luyện âm cuối".
- **AC-F15-2** — Given trong 30 ngày người học có 2 bài Writing bỏ -s ngôi thứ ba và 2 bài Speaking nuốt âm /s/ cuối ở động từ, When mở Dashboard, Then thấy insight "Lỗi -s xuất hiện ở cả nói và viết" kèm liên kết 4 bằng chứng.
- **AC-F15-3** — Given lỗi -s chỉ xuất hiện 1 lần ở Speaking, When tính insight, Then không hiển thị insight xuyên kỹ năng.

### 8.16 Feature F16 — Dự đoán band thật (Priority: M) — *lợi thế A*

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-150 | Hệ thống PHẢI hiển thị dự đoán band **Listening, Reading, Speaking, Writing** riêng biệt và **overall** dưới dạng khoảng (VD: 6.0–6.5); overall chỉ hiển thị khi cả 4 kỹ năng có dự đoán | BR-022 | AC-F16-1 |
| FR-151 | Dự đoán CHỈ dựa trên bài làm Exam Mode đủ điều kiện: Listening/Reading là bài đủ 40 câu trên đề đã hiệu chỉnh bảng quy đổi (FR-222); Speaking đủ 3 Part; Writing có Task 2 (Task 1 nếu có); ≥ 2 bài thi thử mỗi kỹ năng trong 14 ngày gần nhất `[Đề xuất]` | BR-022 | AC-F16-2 |
| FR-152 | Trước khi calibration model đạt điều kiện công bố (FR-174), nhãn PHẢI là "Ước lượng AI — **chưa được hiệu chỉnh** bằng điểm thật" và không hiển thị con số sai số; sau khi đạt: "Dự đoán band thật X–Y · sai số trung bình Z trên N kết quả thật · cập nhật ngày D" | BR-022, BR-024 | AC-F16-3 |
| FR-153 | Mỗi dự đoán PHẢI lưu rubric version, calibration model version và danh sách bài làm đầu vào | BR-022, BR-006 | Metadata có trong DB |
| FR-154 | Bài chấm bằng model dự phòng (FR-069) KHÔNG được dùng làm đầu vào dự đoán | BR-006, BR-022 | Bài fallback bị loại |
| FR-155 | Hệ thống NÊN hiển thị "Sẵn sàng đi thi?" so sánh dự đoán với band mục tiêu (FR-010) và gợi ý số tuần luyện thêm | BR-022 | Hiển thị khi có band mục tiêu |

- **AC-F16-1** — Given người học có đủ bài thi thử hợp lệ cả 4 kỹ năng, When mở trang Dự đoán, Then thấy 4 khoảng band riêng và 1 khoảng band overall; nếu thiếu một kỹ năng thì overall không hiển thị và hệ thống chỉ rõ kỹ năng còn thiếu.
- **AC-F16-2** — Given người học mới chỉ có 1 bài Speaking Part 1, When mở trang Dự đoán, Then hệ thống không đưa dự đoán Speaking và chỉ rõ còn thiếu gì ("cần 2 bài thi đủ 3 Part trong 14 ngày").
- **AC-F16-3** — Given calibration model chưa đạt FR-174, When hiển thị dự đoán, Then nhãn là "chưa được hiệu chỉnh" và không có chữ "sai số".

### 8.17 Feature F17 — Thu thập kết quả thi thật (Priority: M) — *nguồn dữ liệu cho A*

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-160 | Người dùng PHẢI gửi được kết quả thi: ngày thi, dạng thi (Academic/GT, máy/giấy), band Listening, Reading, Speaking, Writing và overall | BR-023 | Form validate band 0–9, bước 0,5 |
| FR-161 | Người dùng PHẢI tải ảnh phiếu điểm để xác minh; hệ thống PHẢI hướng dẫn che ảnh chân dung và số giấy tờ trước khi tải; ảnh tự xóa ≤ 7 ngày sau khi xác minh hoặc từ chối | BR-023, BR-005 | AC-F17-1 |
| FR-162 | Hệ thống PHẢI lấy **consent riêng** (tách khỏi điều khoản chung) cho việc dùng kết quả để hiệu chỉnh; người dùng rút consent được bất cứ lúc nào | BR-023, BR-005 | AC-F17-2 |
| FR-163 | Hệ thống PHẢI chống gửi trùng bằng mã phiếu điểm (lưu dạng hash); một cặp chỉ hợp lệ khi có bài thi thử đủ điều kiện trong khoảng **28 ngày trước hoặc sau ngày thi** `[Đề xuất]`, và ghi lại khoảng cách ngày | BR-023 | AC-F17-3 |
| FR-164 | Admin PHẢI duyệt được từng kết quả (chờ duyệt / đã xác minh / từ chối kèm lý do) và thấy cờ bất thường (VD: band thật lệch ≥ 2 so với ước lượng) | BR-023 | Trang Verification trong admin |
| FR-165 | Phần thưởng PHẢI cấp sau khi xác minh: 2 tháng Premium `[Đề xuất]`, **như nhau cho mọi mức band** | BR-023 | Credit cộng tự động sau khi "đã xác minh" |
| FR-166 | Hệ thống PHẢI có luồng **"Vừa thi xong"** (nguồn 1): đăng ký → thi thử Speaking đủ 3 Part + Writing Task 2 (Task 1 tùy chọn), không trừ credit → gửi kết quả; Listening + Reading tùy chọn, có thưởng thêm 1 tháng Premium `[Đề xuất]` | BR-023 | AC-F17-4 |
| FR-167 | Hệ thống KHÔNG được hỏi, nhận hoặc lưu nội dung câu hỏi của đề thi thật; form không có ô nhập tự do về đề thi | BR-023 | Kiểm tra form & review |

- **AC-F17-1** — Given admin đã xác minh kết quả lúc T, When đến T + 7 ngày, Then ảnh phiếu điểm bị xóa khỏi storage và chỉ còn các con số đã nhập.
- **AC-F17-2** — Given người dùng rút consent hiệu chỉnh, When chạy hiệu chỉnh lần tiếp theo, Then cặp dữ liệu của họ không được dùng.
- **AC-F17-3** — Given mã phiếu điểm đã được gửi bởi tài khoản khác, When người dùng gửi lại mã đó, Then hệ thống từ chối và gắn cờ cho admin.
- **AC-F17-4** — Given người dùng vào luồng "Vừa thi xong" và thi ngày 01/10, When làm bài thi thử ngày 20/10 và gửi kết quả, Then cặp được ghi nhận với khoảng cách 19 ngày và chờ duyệt.

### 8.18 Feature F18 — Hiệu chỉnh & công bố độ chính xác (Priority: M)

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-170 | Admin PHẢI xem bảng cặp dữ liệu hợp lệ theo kỹ năng, mức band thật, khoảng cách ngày và nguồn (1, 3, cohort) | BR-024 | Trang Calibration Data |
| FR-171 | Chỉ cặp có consent hiệu chỉnh còn hiệu lực mới được dùng; xóa tài khoản hoặc rút consent → loại khỏi lần chạy kế tiếp | BR-024, BR-005 | AC-F17-2 |
| FR-172 | Mỗi lần hiệu chỉnh PHẢI tạo calibration model version mới, gắn với rubric version, và giữ riêng tập kiểm tra (holdout ≥ 30% số cặp, không dùng để hiệu chỉnh) | BR-024 | Version lưu trong DB |
| FR-173 | Mỗi version PHẢI có báo cáo: MAE, tỉ lệ lệch ≤ 0,5 band, độ lệch có hướng (chấm cao/thấp hơn) theo từng mức band (≤ 5.0, 5.5, 6.0, 6.5, 7.0, ≥ 7.5) và số cặp mỗi mức | BR-024 | AC-F18-1 |
| FR-174 | Độ chính xác CHỈ được công bố ra ngoài khi holdout ≥ 100 cặp/kỹ năng `[Đề xuất]`; câu công bố PHẢI gồm N, MAE, ngày cập nhật, và không làm tròn theo hướng có lợi | BR-024 | AC-F18-2 |
| FR-175 | Cam kết hoàn tiền (R1.5) CHỈ bật được cho mức band có MAE ≤ 0,5 và ≥ 30 cặp holdout ở mức đó `[Đề xuất]`, sau khi pháp lý duyệt (TBD-18); có công tắc bật/tắt theo từng mức band | BR-029, BR-024 | Công tắc bị khóa khi chưa đạt điều kiện |
| FR-176 | Đổi rubric/model chấm chính (FR-076) PHẢI kích hoạt hiệu chỉnh lại; dự đoán dùng version cũ bị gắn nhãn "phiên bản cũ" | BR-024, BR-006 | AC-F18-3 |

- **AC-F18-1** — Given calibration v3 có 40 cặp holdout ở mức 6.0 và 4 cặp ở mức ≥ 7.5, When xem báo cáo, Then mức ≥ 7.5 được đánh dấu "không đủ dữ liệu".
- **AC-F18-2** — Given holdout Speaking mới có 80 cặp, When admin bấm "Công bố độ chính xác", Then hệ thống từ chối và hiển thị số cặp còn thiếu.
- **AC-F18-3** — Given rubric Speaking đổi từ v2 sang v3, When người học mở dự đoán cũ, Then thấy nhãn "phiên bản cũ" và được mời làm bài thi thử mới.

### 8.19 Feature F19 — Cohort cam kết (Priority: M/S) — *lợi thế C*

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-180 | Admin PHẢI tạo được cohort: ngày bắt đầu, 8 tuần, sĩ số tối đa, khoảng ngày thi mục tiêu | BR-026 | Trang Cohort trong admin |
| FR-181 | Người học PHẢI đăng ký cohort kèm ngày thi dự kiến và band mục tiêu | BR-026 | Form bắt buộc 2 trường |
| FR-182 | Lộ trình PHẢI có 1 nhiệm vụ/ngày ≤ 20 phút `[Đề xuất]` và 1 bài thi thử đủ 4 kỹ năng mỗi 2 tuần (được chia nhiều ngày trong cùng tuần) để cập nhật dự đoán (F16) | BR-026, BR-022 | AC-F19-1 |
| FR-183 | Hệ thống PHẢI hiển thị % hoàn thành cá nhân; bảng tiến độ nhóm NÊN có, ẩn danh mặc định, hiện tên khi người học opt-in | BR-026 | Bảng tiến độ ẩn danh mặc định |
| FR-184 | Cohort NÊN có đặt cọc 100.000đ `[Đề xuất]`, hoàn lại khi (a) hoàn thành ≥ 80% nhiệm vụ **và** (b) gửi kết quả thi thật hợp lệ (F17) trong 30 ngày sau ngày thi; điều khoản hiển thị trước khi nộp cọc; người học chọn nhận lại tiền hoặc đổi thành credit — **chỉ bật sau khi pháp lý duyệt (TBD-18)** | BR-028 | AC-F19-2 |
| FR-185 | Người học PHẢI cập nhật được ngày thi; điều kiện hoàn cọc tính theo ngày mới, lùi tối đa 60 ngày `[Đề xuất]` | BR-026, BR-028 | Lịch sử thay đổi ngày thi được lưu |
| FR-186 | Phí cohort PHẢI bao gồm quyền Premium trong suốt 8 tuần | BR-026, BR-003 | Entitlement Premium tự cấp khi vào cohort |

- **AC-F19-1** — Given người học ở tuần 4 của cohort, When hoàn thành bài thi thử định kỳ, Then dự đoán band được cập nhật và so sánh với lần trước.
- **AC-F19-2** — Given người học hoàn thành 85% nhiệm vụ nhưng chưa gửi phiếu điểm sau 30 ngày kể từ ngày thi, When hết hạn, Then cọc không được hoàn và người học đã được nhắc ít nhất 2 lần trước hạn.

### 8.20 Feature F20 — Nhắc học chủ động (Priority: S)

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-190 | Hệ thống NÊN gửi nhiệm vụ hằng ngày qua kênh người học chọn (email mặc định; Zalo nếu TBD-16 khả thi) vào khung giờ người học chọn | BR-027 | AC-F20-1 |
| FR-191 | Tin nhắc NÊN chứa liên kết mở thẳng trang trả lời 1 câu Speaking Part 1; liên kết đăng nhập một lần, hết hạn sau 24 giờ | BR-027, BR-007 | Liên kết hết hạn sau 24 giờ |
| FR-192 | Tối đa 1 tin nhắc/ngày + 1 tin nhắc lại nếu chưa làm; không gửi 22:00–07:00 `[Đề xuất]`; tắt nhắc bằng 1 chạm | BR-027 | AC-F20-2 |
| FR-193 | Câu trả lời từ tin nhắc dùng 0 credit và tính vào giới hạn drill hằng ngày (FR-124) | BR-027, BR-004 | Không trừ credit |

- **AC-F20-1** — Given người học chọn nhận nhắc lúc 20:00 qua email, When đến 20:00, Then email nhiệm vụ trong ngày được gửi.
- **AC-F20-2** — Given người học đã hoàn thành nhiệm vụ lúc 19:00, When đến giờ nhắc lại, Then không có tin nhắc lại.

### 8.21 Feature F21 — Quản lý bộ dữ liệu & license (Priority: M) — *nguồn 4*

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-195 | Admin PHẢI đăng ký mỗi bộ dữ liệu bên ngoài: tên, nguồn, license, **được phép thương mại (Có/Không)**, yêu cầu ghi công, hạn chế chia sẻ, file license/thỏa thuận, ngày duyệt | BR-025 | Trang Dataset Registry |
| FR-196 | Pipeline đánh giá/hiệu chỉnh PHẢI từ chối bộ dữ liệu có "được phép thương mại = Không", trừ khi đã lưu license thương mại riêng | BR-025 | AC-F21-1 |
| FR-197 | Mỗi báo cáo eval PHẢI ghi rõ bộ dữ liệu và phiên bản đã dùng | BR-025, BR-006 | Báo cáo có danh sách bộ dữ liệu |

- **AC-F21-1** — Given bộ ELLIPSE được đăng ký với license CC BY-NC-SA, When chạy eval có chọn bộ này, Then pipeline dừng và báo "cần license thương mại".

### 8.22 Feature F22 — Listening & Reading: làm bài (Priority: M)

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-200 | Listening PHẢI có 4 phần, tổng 40 câu; Reading PHẢI có 3 bài đọc, tổng 40 câu, 60 phút; cấu trúc và thời gian lưu trong metadata đề | BR-017 | AC-F22-1 |
| FR-201 | Dạng câu hỏi bắt buộc: Multiple Choice (1 và nhiều đáp án), Form/Note/Table/Sentence/Summary Completion (có giới hạn số từ), True/False/Not Given, Yes/No/Not Given, Matching Headings, Matching Information/Features | BR-017 | Mỗi dạng có renderer và chấm tự động |
| FR-202 | Dạng câu hỏi NÊN có: Map/Plan/Diagram Labelling, Short-answer Questions | BR-017 | — |
| FR-203 | Exam Mode Listening PHẢI phát audio **một lần**, không tua, không dừng; audio PHẢI được tải đủ trước khi bắt đầu để mất mạng không làm gián đoạn | BR-017, BR-008 | AC-F22-2 |
| FR-204 | Practice Mode Listening PHẢI cho phép tua, nghe lại, xem transcript sau khi nộp | BR-017 | Nút tua và transcript chỉ có ở Practice Mode |
| FR-205 | Chấm tự động PHẢI hỗ trợ biến thể đáp án được chấp nhận, không phân biệt hoa/thường, và quy tắc giới hạn số từ ("NO MORE THAN TWO WORDS"); đáp án vượt giới hạn tính sai | BR-017 | AC-F22-3 |
| FR-206 | Sau khi nộp, người học PHẢI xem đáp án đúng, giải thích và vị trí bằng chứng trong bài đọc/transcript | BR-017 | Bấm câu hỏi → highlight đoạn chứa đáp án |
| FR-207 | Autosave và khôi phục bài L/R PHẢI theo FR-023, FR-024; Listening bị gián đoạn trong Exam Mode được đánh dấu "không đủ điều kiện dự đoán" | BR-008, BR-022 | AC-F22-4 |
| FR-208 | Lỗi L/R PHẢI được gắn error tag theo dạng câu hỏi và kỹ năng con (VD: "bẫy paraphrase", "không nghe được số", "sai chính tả đáp án") vào Error Memory | BR-002 | Error Memory có nhóm L/R |
| FR-209 | Chấm L/R KHÔNG trừ credit; Free được làm 1 bộ Listening + 1 bộ Reading, Premium làm toàn bộ kho đề `[Đề xuất]` | BR-003 | Kiểm tra entitlement |

- **AC-F22-1** — Given đề Reading đủ điều kiện publish, When người học bắt đầu Exam Mode, Then đồng hồ 60 phút chạy, có 3 bài đọc và 40 câu, tự nộp khi hết giờ.
- **AC-F22-2** — Given người học mất mạng ở phút 12 của Listening Exam Mode, When audio đang phát, Then audio tiếp tục phát (đã tải trước) và câu trả lời được lưu local.
- **AC-F22-3** — Given đáp án chuẩn "train station" với giới hạn "NO MORE THAN TWO WORDS", When người học điền "the train station", Then câu được chấm sai; When điền "Train Station", Then chấm đúng.
- **AC-F22-4** — Given người học đóng tab giữa Listening Exam Mode, When mở lại, Then bài được lưu nhưng gắn nhãn "không đủ điều kiện dự đoán" và người học được mời làm lại đề khác.

### 8.23 Feature F23 — Quy trình soạn đề L/R (Priority: M)

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-210 | Đề L/R PHẢI được tạo qua quy trình: AI soạn nháp (bài đọc/kịch bản nghe + câu hỏi + đáp án + giải thích) → kiểm tra tự động → người duyệt → pilot → publish | BR-030 | Trạng thái đề: draft / reviewed / pilot / published |
| FR-211 | Bài đọc PHẢI là văn bản gốc do AI viết hoặc dựa trên nguồn có quyền sử dụng đã đăng ký (F21); lưu provenance cho từng bài | BR-030, BR-025 | Đề thiếu provenance không publish được |
| FR-212 | Audio Listening PHẢI tạo bằng TTS có quyền dùng thương mại (TBD-19), nhiều giọng (Anh, Úc, Bắc Mỹ…), có hội thoại nhiều người; audio được tạo một lần và cache | BR-017, BR-030 | Mỗi đề có ≥ 2 giọng khác nhau |
| FR-213 | Kiểm tra tự động PHẢI xác nhận: mỗi đáp án xuất hiện đúng trong bài đọc/transcript; đáp án tuân thủ giới hạn số từ; câu hỏi đúng thứ tự xuất hiện (khi dạng câu hỏi yêu cầu); không có hai đáp án cùng đúng ở câu trắc nghiệm một đáp án | BR-030 | AC-F23-1 |
| FR-214 | Người duyệt PHẢI hoàn thành checklist (đáp án duy nhất, phương án nhiễu hợp lý, độ dài bài đọc theo chuẩn, audio rõ, đúng tốc độ) trước khi chuyển sang pilot | BR-030 | Checklist bắt buộc trong admin |
| FR-215 | Hệ thống và quy trình KHÔNG được crawl hoặc nhập đề từ sách có bản quyền, website luyện thi, hay đề thi thật do thí sinh nhớ lại; công cụ import từ chối đề không có provenance hợp lệ | BR-030 | AC-F23-2 |
| FR-216 | Người học PHẢI báo lỗi được từng câu hỏi; câu có lỗi đáp án được xác nhận thì sửa và chấm lại cho mọi bài đã làm | BR-030, BR-009 | AC-F23-3 |

- **AC-F23-1** — Given AI soạn câu Completion có đáp án "renewable energy" nhưng cụm này không có trong bài đọc, When chạy kiểm tra tự động, Then đề bị chặn ở trạng thái draft kèm lỗi cụ thể.
- **AC-F23-2** — Given admin import một đề với provenance "website X", When validate, Then import bị từ chối.
- **AC-F23-3** — Given câu 17 được xác nhận sai đáp án, When admin sửa, Then mọi bài đã làm đề đó được chấm lại và band quy đổi được cập nhật.

### 8.24 Feature F24 — Bảng quy đổi band L/R theo từng đề (Priority: M)

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-220 | Mỗi đề L/R PHẢI có bảng quy đổi điểm thô (0–40) → band riêng, có version; bảng khởi đầu là bảng tham chiếu công khai (gần đúng) | BR-017 | Mỗi đề có bảng v1 |
| FR-221 | Hệ thống PHẢI tính thống kê từng câu (tỉ lệ đúng, độ phân biệt) và từng đề (điểm trung bình so với các đề khác cùng nhóm người làm); gắn cờ câu quá dễ/quá khó hoặc có độ phân biệt âm | BR-017, BR-024 | Báo cáo item statistics trong admin |
| FR-222 | Đề CHỈ được dùng cho dự đoán (F16) khi có ≥ 50 lượt làm Exam Mode `[Đề xuất]` và bảng quy đổi đã được điều chỉnh theo độ khó quan sát được; trước đó đề chỉ dùng để luyện, band hiển thị kèm nhãn "đề mới, chưa hiệu chỉnh" | BR-022, BR-024 | AC-F24-1 |
| FR-223 | Khi có cặp điểm thật L/R (F17), bảng quy đổi PHẢI được hiệu chỉnh tiếp theo quy trình F18, tạo version mới | BR-024 | Version bảng quy đổi gắn với calibration model |

- **AC-F24-1** — Given đề Listening #7 mới có 20 lượt làm, When người học làm đề này ở Exam Mode, Then band hiển thị có nhãn "đề mới, chưa hiệu chỉnh" và bài không được dùng làm đầu vào dự đoán.


---

## 9. Non-Functional Requirements

> Các target có nhãn `[Đề xuất]` chờ duyệt trước tuần 15.

### 9.1 Performance

| ID | Requirement | Metric | Target |
|---|---|---|---|
| NFR-P01 | Thời gian trả report Writing | p50 / p95 từ lúc nộp | ≤ 45s / ≤ 90s `[Đề xuất]` |
| NFR-P02 | API không liên quan AI | p95 latency | ≤ 500ms |
| NFR-P03 | Tải trang trên 4G, điện thoại tầm trung | Largest Contentful Paint | ≤ 2,5s |
| NFR-P04 | Autosave local | Độ trễ sau lần gõ cuối | ≤ 5s |
| NFR-P05 | Thời gian trả report Speaking đủ 3 Part | p50 / p95 từ lúc nộp | ≤ 60s / ≤ 120s `[Đề xuất]` |
| NFR-P06 | Độ trễ giữa hai câu hỏi của giám khảo AI | Từ lúc dừng ghi âm đến lúc phát câu hỏi tiếp theo | ≤ 2s; câu hỏi nối tiếp Part 3 ≤ 5s |
| NFR-P07 | Cập nhật dự đoán band | Từ lúc bài thi thử đủ điều kiện được chấm xong | ≤ 5 phút |

### 9.2 Reliability & Availability

| ID | Requirement | Target |
|---|---|---|
| NFR-R01 | Uptime hằng tháng (beta) | ≥ 99% `[Đề xuất]` |
| NFR-R02 | Tỉ lệ chấm thành công (sau retry + fallback) | ≥ 98% |
| NFR-R03 | RPO | ≤ 24 giờ (backup hằng ngày, lưu ngoài VPS chính) |
| NFR-R04 | RTO | ≤ 8 giờ `[Đề xuất]`; diễn tập khôi phục ≥ 1 lần/tháng trong beta |
| NFR-R05 | Mất bài đã gõ hoặc bản ghi âm đã thu do lỗi hệ thống | 0 trường hợp được xác nhận |
| NFR-R06 | Tỉ lệ ghi âm/upload thành công trên các trình duyệt được hỗ trợ | ≥ 99% `[Đề xuất]` |

### 9.3 Security

| ID | Requirement | Standard |
|---|---|---|
| NFR-S01 | Mã hóa đường truyền | HTTPS bắt buộc, TLS ≥ 1.2 |
| NFR-S02 | Mật khẩu | Argon2id hoặc bcrypt |
| NFR-S03 | Phân quyền | Kiểm tra quyền sở hữu tại server cho mọi resource; admin theo role |
| NFR-S04 | Audit log admin & thanh toán | Lưu ≥ 1 năm |
| NFR-S05 | Rate limit nộp bài | ≤ 10 lần/phút/người dùng; đăng nhập theo AC-F1-2 |
| NFR-S06 | Secrets | Chỉ ở backend/biến môi trường; CI quét secret trên mỗi commit |
| NFR-S07 | OWASP Top 10 | Rà soát trước public launch |
| NFR-S08 | Webhook | Xác minh chữ ký + idempotency key |
| NFR-S09 | Audio | Lưu ở storage riêng tư, chỉ truy cập qua URL ký hạn ≤ 15 phút; tự xóa sau 30 ngày |
| NFR-S10 | Ảnh phiếu điểm | Mã hóa khi lưu; chỉ admin được chỉ định xem; mọi lần xem ghi audit log; xóa ≤ 7 ngày (FR-161) |
| NFR-S11 | Mã phiếu điểm | Chỉ lưu dạng hash có salt, không lưu bản rõ |

### 9.4 Usability

| ID | Requirement | Target |
|---|---|---|
| NFR-U01 | Từ đăng ký đến nộp bài diagnostic | Trung vị ≤ 5 phút (không tính thời gian viết) |
| NFR-U02 | Accessibility luồng chính | WCAG 2.1 AA: điều khiển bằng bàn phím, focus rõ, tương phản |
| NFR-U03 | Ngôn ngữ | UI tiếng Việt; nội dung đề tiếng Anh; UI tiếng Anh ở release sau |
| NFR-U04 | Minh bạch AI | Nhãn "ước lượng — không chính thức" hiển thị ở 100% vị trí có band; nhãn trạng thái hiệu chỉnh ở 100% vị trí có dự đoán |

### 9.5 Maintainability

| ID | Requirement | Target |
|---|---|---|
| NFR-M01 | Automated test cho các luồng quan trọng | Auth & cách ly dữ liệu, autosave/nộp idempotent, credit, webhook, validate output AI, xóa dữ liệu — 100% có test |
| NFR-M02 | Code coverage module lõi backend | ≥ 70% `[Đề xuất]` |
| NFR-M03 | Versioning | Prompt, rubric, JSON schema, taxonomy lỗi đều có version và lưu vào report |
| NFR-M04 | Môi trường | Staging tách biệt production; release qua staging |

### 9.6 Compatibility

| ID | Requirement |
|---|---|
| NFR-C01 | Chrome, Edge, Safari, Firefox — 2 phiên bản mới nhất |
| NFR-C02 | iOS Safari ≥ 16, Android Chrome 2 phiên bản mới nhất |
| NFR-C03 | Chiều rộng màn hình 360px → 2560px |
| NFR-C04 | Ghi âm Speaking hoạt động trên Chrome/Edge desktop, Safari macOS, iOS Safari ≥ 16, Android Chrome — danh sách cuối cùng và codec: `TBD-14` |

### 9.7 Portability, Scalability & Cost

| ID | Requirement | Target |
|---|---|---|
| NFR-PS01 | Tải đồng thời trên 1 VPS | ≥ 200 người dùng đồng thời `[Đề xuất]` |
| NFR-PS02 | Đổi AI provider/model | Bằng cấu hình, không cần deploy code |
| NFR-PS03 | Đóng gói | Docker Compose chạy được trên VPS mới ≤ 1 giờ |
| NFR-COST01 | Chi phí AI/lượt chấm Writing | Trung bình ≤ 1.500đ `[Đề xuất]` |
| NFR-COST03 | Chi phí AI + speech/bài thi Speaking đủ 3 Part (STT + chấm phát âm + LLM + TTS) | Trung bình ≤ 5.000đ `[Đề xuất]` |
| NFR-COST02 | Chi phí hạ tầng hằng tháng (VPS, storage, email) | Trần: `TBD-10` |

---

## 10. External Interface Requirements

| System | Mục đích | Giao thức | Xác thực | Ghi chú |
|---|---|---|---|---|
| Google OAuth | Đăng nhập | OAuth 2.0 / OIDC | Client ID + Secret | — |
| AI provider(s) | Chấm bài (Lớp A), tạo nội dung (Lớp B/C) | HTTPS REST | API key (backend) | `TBD-04`; danh sách Lớp A phải có cam kết không huấn luyện |
| Speech provider(s) | STT, chấm phát âm ở mức âm/từ (Lớp A); TTS giọng giám khảo, mẫu phát âm và **audio Listening** (Lớp B, cache lại) | HTTPS REST / streaming | API key (backend) | `TBD-04`; cùng yêu cầu Lớp A như AI provider; TTS phải cho phép dùng thương mại (`TBD-19`) |
| Payment provider | Thu tiền | HTTPS REST + webhook | API key + chữ ký HMAC | `TBD-07`; ưu tiên VietQR / ví điện tử, thanh toán một lần |
| Email provider | Xác thực, nhắc học, cảnh báo chi phí | HTTPS API / SMTP | API key | `TBD-09` |
| Kênh nhắn tin chủ động | Nhắc học hằng ngày (F20) | Theo nhà cung cấp (VD: Zalo OA) | Theo nhà cung cấp | `TBD-16`; kiểm tra chính sách gửi tin chủ động và chi phí |
| Bộ dữ liệu công khai | Đánh giá bộ chấm (nguồn 4) | Tải thủ công | Theo thỏa thuận license | Chỉ bộ có quyền thương mại (F21, §16) |
| Object storage | Ảnh biểu đồ Task 1, audio ghi âm, audio TTS đã cache | S3-compatible | Access key, URL ký hạn ngắn | `TBD-10` |

---

## 11. Data Requirements

### 11.1 Data model (thiết kế sẵn sàng đa kỳ thi)

| Entity | Trường chính | Ghi chú mở rộng |
|---|---|---|
| `exam_family` | IELTS / TOEIC / SAT | R1 chỉ có IELTS |
| `exam_variant` | Academic / General Training / TOEIC LR / Digital SAT | R1 chỉ có Academic |
| `section`, `task_type` | Listening Part 1–4, Reading Passage 1–3, Writing Task 1/2, Speaking Part 1/2/3 … | Cấu trúc section, thời gian (chuẩn bị, thời lượng nói, thời gian làm bài) và luật điều hướng (audio phát một lần) lưu trong metadata, không hard-code UI |
| `item` (đề) | id, version, nội dung, dữ liệu biểu đồ (Task 1), độ khó, provenance, quyền sử dụng, cờ AI-generated, trạng thái review | Registry dạng câu hỏi mở rộng được (câu nhóm, ảnh, tự điền, LaTeX) |
| `scoring_strategy` | rubric_ai (IELTS Writing), speech_rubric_ai (IELTS Speaking), answer_key + raw_to_band theo đề (IELTS L/R), raw_to_scaled (TOEIC), adaptive_module (SAT) | R1 triển khai rubric_ai, speech_rubric_ai, answer_key + raw_to_band |
| `rubric_version` | tiêu chí, prompt version, model chấm chính, JSON schema version | Xem FR-076 |
| `attempt` | user, item, mode, nội dung, version, trạng thái | — |
| `recording` | attempt, câu hỏi, đường dẫn audio, thời lượng, trạng thái upload, hạn xóa | Tự xóa sau 30 ngày; transcript và kết quả giữ lại |
| `speech_analysis` | recording, transcript, độ tin cậy STT, kết quả phát âm theo từ/âm, tốc độ nói, khoảng ngừng | Nguồn bằng chứng cho F14 |
| `report` | band, tiêu chí, nhận xét + bằng chứng, model/provider, rubric version, cờ fallback | — |
| `error_taxonomy` | domain → subskill → error tag, cờ `l1_vietnamese`, `root_cause` (gốc lỗi chung giữa nói và viết) | Dùng chung cho mọi kỳ thi (VD: lỗi ngữ pháp dùng lại cho TOEIC); `root_cause` phục vụ insight xuyên kỹ năng |
| `error_occurrence` | user, error tag, attempt nguồn, vị trí, độ tin cậy | Nền tảng của Error Memory |
| `credit_wallet`, `credit_ledger` | số dư, cộng/trừ, lý do, idempotency key | Một ví/người dùng, dùng chung mọi kỳ thi |
| `entitlement` | gói, phạm vi sản phẩm/kỳ thi, hiệu lực | — |
| `payment_order`, `payment_event` | trạng thái, provider reference, lịch sử | Không lưu dữ liệu thẻ |
| `ai_request_log` | provider, model, token, chi phí, latency, trạng thái | Không lưu toàn văn bài |
| `official_result` | user, ngày thi, dạng thi, band S/W (L/R/overall tùy chọn), hash mã phiếu, trạng thái xác minh, consent hiệu chỉnh, nguồn (1/3/cohort) | Ảnh phiếu điểm lưu tạm, xóa ≤ 7 ngày |
| `calibration_pair` | official_result, các attempt đầu vào, khoảng cách ngày, tập (hiệu chỉnh/holdout) | Loại khi rút consent |
| `calibration_model` | version, kỹ năng, rubric version, tham số, báo cáo MAE theo mức band, trạng thái công bố | Không chứa dữ liệu cá nhân |
| `prediction` | user, kỹ năng, khoảng band, calibration version, attempt đầu vào, thời điểm | — |
| `cohort`, `cohort_member` | lịch, ngày thi mục tiêu, % hoàn thành, trạng thái cọc | — |
| `deposit` | số tiền, trạng thái (đã nộp/đã hoàn/không hoàn/đổi credit), lý do | Liên kết `payment_order` |
| `dataset_registry` | tên, nguồn, license, cờ thương mại, file thỏa thuận | F21 |
| `conversion_table` | đề, version, ánh xạ 0–40 → band, trạng thái hiệu chỉnh | F24 |
| `item_stats` | câu hỏi, số lượt, tỉ lệ đúng, độ phân biệt, cờ | F24 |
| `content_review` | đề, người duyệt, checklist, kết quả kiểm tra tự động, trạng thái | F23 |

> ⚠️ Chỉ đặt đúng tên và trường ở R1. Phần triển khai dùng chung thực sự làm khi bắt tay vào R4 (TOEIC), tránh trừu tượng hóa quá sớm.

### 11.2 Data Retention

| Loại dữ liệu | Thời hạn | Xử lý khi hết hạn |
|---|---|---|
| Bài làm, report, Error Memory | Đến khi người dùng xóa hoặc xóa tài khoản | Xóa vĩnh viễn |
| Audio ghi âm | 30 ngày | Tự động xóa, kể cả bản tạm và bản local đã upload xong |
| Log vận hành AI (không có nội dung bài) | 90 ngày `[Đề xuất]` | Xóa |
| Ảnh phiếu điểm | ≤ 7 ngày sau khi xác minh/từ chối | Xóa vĩnh viễn |
| Kết quả thi (con số) và cặp hiệu chỉnh | Đến khi người dùng rút consent, xóa dữ liệu hoặc xóa tài khoản | Xóa; loại khỏi lần hiệu chỉnh kế tiếp |
| Giao dịch thanh toán | Theo nghĩa vụ kế toán/thuế (`TBD-12`) | Lưu trữ |
| Backup | `TBD-10`; công bố cách dữ liệu đã xóa hết vòng đời trong backup | Xoay vòng |

### 11.3 Content Quality Gates (trước khi publish đề)

1. Validate schema. 2. Kiểm tra dữ liệu biểu đồ khớp hình hiển thị (Task 1). 3. Nghe lại audio TTS câu hỏi Speaking. 4. **L/R: kiểm tra tự động (FR-213), checklist người duyệt (FR-214), nghe lại toàn bộ audio Listening, pilot trước khi dùng cho dự đoán (FR-222).** 5. Kiểm tra quyền sử dụng & provenance; không có đề crawl (FR-215). 6. Review nội dung AI-generated. 7. Nội dung chưa chắc chắn giữ ở trạng thái draft.

---

## 12. Compliance & Legal

| Hạng mục | Áp dụng | Ghi chú |
|---|---|---|
| Luật Bảo vệ dữ liệu cá nhân 2025 và Nghị định 13/2023/NĐ-CP (cùng văn bản hướng dẫn hiện hành) | ✅ | Thông báo & chấp thuận, xóa dữ liệu, chuyển dữ liệu tới AI/speech provider (có thể ở nước ngoài) — **cần rà soát pháp lý `TBD-12`** |
| Giọng nói (ghi âm) | ✅ | Cần xác định giọng nói có thuộc nhóm dữ liệu cá nhân nhạy cảm theo quy định hiện hành hay không; chấp thuận riêng trước khi ghi âm; không dùng để nhận dạng danh tính — **`TBD-12`** |
| Người chưa thành niên (P2) | ✅ | Thông báo viết cho độ tuổi người dùng, tối thiểu hóa dữ liệu; cơ chế đồng ý của cha mẹ/người giám hộ theo quy định — bắt buộc trước R4 (SAT), rà soát cho R1 (đặc biệt với phiếu điểm và đặt cọc) |
| Kết quả thi thật & phiếu điểm | ✅ | Consent riêng cho mục đích hiệu chỉnh; tối thiểu hóa (che ảnh, số giấy tờ; xóa ảnh ≤ 7 ngày); quyền rút consent — **`TBD-12`** |
| Bảo mật đề thi | ✅ | Không thu thập nội dung câu hỏi đề thi thật (FR-167) |
| Nguồn đề L/R | ✅ | Chỉ đề tự soạn/có quyền; không crawl; không dùng sách đề có bản quyền hay đề thi thật do thí sinh nhớ lại (FR-215) |
| Giọng TTS | ✅ | Điều khoản TTS phải cho phép phân phối audio trong sản phẩm thương mại (`TBD-19`) |
| License bộ dữ liệu | ✅ | Đa số bộ phù hợp là phi thương mại (§16); chỉ dùng khi có quyền thương mại (F21) |
| Quảng cáo độ chính xác | ✅ | Chỉ công bố số liệu đo được, kèm N và ngày (FR-174) — **`TBD-18`** |
| Đặt cọc & cam kết hoàn tiền | ✅ | Cần xác định khung pháp lý phù hợp trước khi bật FR-184 và FR-175 — **`TBD-18`** |
| Bảo vệ người tiêu dùng / thương mại điện tử | ✅ | Hiển thị giá, điều kiện hoàn tiền, không tự gia hạn ngầm |
| Bản quyền nội dung đề | ✅ | Chỉ nội dung tự biên soạn/có quyền; không dùng đề thi thật có bản quyền |
| Điều khoản sử dụng của AI provider | ✅ | Mỗi provider một tài khoản hợp lệ; không lách hạn mức miễn phí |
| PCI-DSS | ❌ | Không lưu dữ liệu thẻ |

---

## 13. Monetization & Unit Economics

| Gói | Giá | Credit | Ghi chú |
|---|---|---|---|
| Free | 0đ | Diagnostic + 3 credit tổng `[Đề xuất]` + 1 bộ Listening + 1 bộ Reading | Đủ trải nghiệm vòng lặp chấm → rewrite và thấy dự đoán |
| Premium tháng | **69.000đ** | 30/tháng `[Đề xuất]` (VD: 10 bài thi Speaking đủ 3 Part, hoặc 30 bài Writing, hoặc kết hợp); **Listening/Reading không tốn credit**, làm toàn bộ kho đề | Không tự gia hạn trong R1 |
| Gói 3 tháng | 179.000đ `[Đề xuất]` | 90 trong 3 tháng | Khớp chu kỳ ôn thi |
| **Cohort 8 tuần** | 199.000đ `[Đề xuất]` + cọc 100.000đ hoàn lại (FR-184) | Premium trong 8 tuần | Lợi thế C; nguồn dữ liệu chất lượng cao cho A |
| Cam kết theo kết quả (R1.5) | `TBD` | — | Chỉ bật khi O8 đạt (FR-175) |

**Chi phí phần thưởng dữ liệu (FR-165):** chi phí biên của 2 tháng Premium chủ yếu là chi phí AI thực dùng. Chiến dịch nguồn 1 tốn khoảng 5.000–10.000đ chi phí AI cho bài thi thử của mỗi người; 300 cặp ≈ 1,5–3 triệu đồng `[Đề xuất]`.

**Công thức theo dõi (O4):**
`AI cost ratio = Σ(credit đã dùng theo loại × chi phí trung bình/credit của loại đó) ÷ doanh thu thuần` — mục tiêu ≤ 30%. Theo dõi riêng Speaking và Writing.

---

## 14. Lỗi đặc trưng của người Việt — danh sách khởi đầu

> Đây là **giả thuyết ban đầu** dựa trên các lỗi phổ biến của người học tiếng Anh có tiếng mẹ đẻ là tiếng Việt. Phải kiểm chứng và tinh chỉnh bằng eval set Speaking/Writing (FR-091) và người review có chuyên môn (`TBD-13`) trước tuần 15.

| Nhóm | Lỗi | Ví dụ | Kỹ năng | `root_cause` (dùng cho insight xuyên kỹ năng) |
|---|---|---|---|---|
| Phát âm | Mất/nuốt âm cuối | want → /wɒn/, most → /məʊs/ | Speaking | `final_consonant` |
| Phát âm | Bỏ âm /s/ /z/ cuối (số nhiều, ngôi thứ ba) | He like it; two book | Speaking | `inflection_s` |
| Phát âm | Bỏ âm /t/ /d/ của đuôi -ed | I walk yesterday | Speaking | `inflection_ed` |
| Phát âm | /θ/ /ð/ thay bằng /t/ /d/ hoặc /s/ /z/ | think → /tɪŋk/, this → /dɪs/ | Speaking | — |
| Phát âm | /ʃ/ thay bằng /s/ | she → /siː/ | Speaking | — |
| Phát âm | Rút gọn cụm phụ âm | street → /sə'triːt/ | Speaking | — |
| Phát âm | Sai trọng âm từ | 'develop' nhấn âm đầu | Speaking | — |
| Phát âm | Ngữ điệu phẳng, nhấn mọi từ như nhau | — | Speaking | — |
| Ngữ pháp | Thiếu -s ngôi thứ ba / số nhiều | He go to school; many student | Writing + Speaking | `inflection_s` |
| Ngữ pháp | Không chia thì quá khứ | Last year I visit Hanoi | Writing + Speaking | `inflection_ed` |
| Ngữ pháp | Thiếu/sai mạo từ a/an/the | I have car | Writing + Speaking | `article` |
| Ngữ pháp | Thiếu động từ to be | She very happy | Writing + Speaking | `copula` |
| Ngữ pháp | Dịch sát cấu trúc tiếng Việt | "Although… but…", "Because… so…" | Writing + Speaking | `l1_transfer_connector` |

**Nguyên tắc:** các lỗi có cùng `root_cause` ở cả hai kỹ năng là nguồn của insight xuyên kỹ năng (FR-122).

---

## 15. Chiến lược đa kỳ thi

### 15.1 Khác biệt giữa các kỳ thi

| | IELTS | TOEIC | SAT (Digital) |
|---|---|---|---|
| Người học VN | 16–25 tuổi | Sinh viên, người đi làm | Học sinh THPT (phần lớn chưa thành niên) |
| Sẵn sàng trả tiền | Trung bình–khá | Thấp, số lượng lớn | Cao (thường phụ huynh trả) |
| Giá trị cốt lõi | Speaking mô phỏng phòng thi + chấm phát âm; Writing có Error Memory | Kho đề lớn, phân tích theo Part, từ vựng | Adaptive, Math, mô phỏng giao diện thi |
| Thành phần dùng lại từ R1 | — | Auth, credit/thanh toán, Error Memory, taxonomy (gồm lỗi đặc trưng của người Việt), speech pipeline cho TOEIC Speaking sau này, admin | Như TOEIC + engine làm bài |

### 15.2 Lợi thế vòng đời
`SAT (15–17 tuổi) → IELTS (17–22) → TOEIC (20–25)` — một tài khoản, một ví credit, lịch sử học liên tục qua nhiều năm.

### 15.3 Gate mở kỳ thi mới — xem §5.1.

---

## 16. Chiến lược dữ liệu & hiệu chỉnh

> Dữ liệu cần có: **cặp "bài thi thử trên hệ thống ↔ band thật"** của cùng một người, trong thời gian gần nhau. Dữ liệu này không mua hay cào được, phải tự tạo ra.

### 16.1 Trình tự (Founder duyệt)

| Bước | Nguồn | Mục đích | Được dùng để |
|---|---|---|---|
| 1 (tuần 1–3) | **Nguồn 4 — dữ liệu công khai** + eval set tự xây (kho đề L/R xây ở tuần 9–15) | Kiểm tra và làm vững bộ chấm trước khi mở beta | Đánh giá nội bộ bộ chấm; **không** hiệu chỉnh theo band IELTS |
| 2 (tuần 16) | Open beta | Có người dùng và bài thi thử | — |
| 3 (từ tuần 16) | **Nguồn 1 — người vừa thi xong** (luồng FR-166) | Tạo cặp dữ liệu nhanh, không phải chờ người học đi thi | **Hiệu chỉnh** dự đoán band thật |
| 4 (từ tuần 18) | Cohort (F19) | Cặp chất lượng cao, có lịch sử 8 tuần | Hiệu chỉnh, lâu dài |
| Sau | Nguồn 3 — trung tâm/giáo viên | Mở rộng số cặp theo lớp | Hiệu chỉnh + cửa vào B2B |

### 16.2 Nguồn 4 — bộ dữ liệu công khai (tra cứu 09/2026)

⚠️ **Phát hiện quan trọng:** đa số bộ dữ liệu phù hợp chỉ cho phép **dùng phi thương mại**. Với một sản phẩm thu phí, việc dùng các bộ này kể cả để đánh giá nội bộ có rủi ro vi phạm license. Cách hiểu thận trọng: **không dùng khi chưa có license thương mại** (xác nhận với luật sư, TBD-15).

| Bộ dữ liệu | Nội dung | Người Việt? | License | Dùng được? |
|---|---|---|---|---|
| **speechocean762** | 5.000 câu tiếng Anh, điểm phát âm mức âm/từ/câu do 5 chuyên gia chấm | Không (người nói tiếng Trung) | **CC BY 4.0** — cho phép thương mại | ✅ Kiểm tra bộ chấm phát âm của speech provider (A5) |
| L2-ARCTIC | Giọng tiếng Anh của 24 người, **có 4 người Việt**, có chú thích lỗi phát âm | **Có** | CC BY-NC 4.0 | ❌ Cần xin license thương mại |
| Speak & Improve Corpus 2025 (Cambridge) | ~315 giờ nói, nhãn CEFR | Nhiều L1 | Phi thương mại, không chia sẻ, cần duyệt | ❌ Cần xin license thương mại |
| Write & Improve Corpus 2024 (Cambridge) | 23.000+ bài viết, nhãn CEFR; tiếng Việt là một trong các L1 phổ biến | **Có** | Theo thỏa thuận license — cần đọc | ⚠️ Kiểm tra điều khoản |
| ICNALE | Bài nói và viết của sinh viên châu Á, có module gồm Việt Nam | **Có** | CC BY-NC-ND 3.0 | ❌ Cần xin license thương mại |
| ELLIPSE | ~6.500 bài viết học sinh ELL tại Mỹ, điểm phân tích | Không rõ | CC BY-NC-SA 4.0 | ❌ Cần xin license thương mại |

**Hệ quả cho bước 1:**
1. Dùng ngay **speechocean762** để đánh giá speech provider.
2. **Gửi yêu cầu license thương mại** cho L2-ARCTIC, Cambridge (S&I, W&I), ICNALE ngay tuần 1 (TBD-15); có thể không được hoặc mất phí.
3. **Tự xây eval set** từ tình nguyện viên người Việt có consent (≥ 30 bản ghi Speaking, ≥ 40 bài Writing, FR-091). Đây là nguồn chắc chắn nhất của bước 1.
4. Nhãn CEFR ≠ band IELTS: dữ liệu nguồn 4 chỉ kiểm tra bộ chấm có phân biệt đúng trình độ hay không, **không** dùng để khẳng định band.

Nguồn: [speechocean762 — OpenSLR](https://www.openslr.org/101/) · [L2-ARCTIC — Texas A&M](https://psi.engr.tamu.edu/l2-arctic-corpus-docs/) · [Speak & Improve Corpus 2025](https://researchdatasets.cambridge.org/datasets/speak-and-improve-corpus-2025) · [Write & Improve Corpus 2024](https://researchdatasets.cambridge.org/datasets/write-and-improve-corpus-2024) · [ICNALE](https://language.sakura.ne.jp/icnale/) · [ELLIPSE — GitHub](https://github.com/scrosseye/ELLIPSE-Corpus)

### 16.3 Nguồn 1 — người vừa thi xong

- **Kênh mời:** nhóm Facebook IELTS Việt Nam (văn hóa khoe điểm sau khi thi). Chỉ **đăng lời mời**; không cào bài đăng hay ảnh phiếu điểm người khác đã đăng.
- **Lời mời mẫu:** "Vừa thi IELTS xong? Làm 1 bài thi thử 30 phút, gửi phiếu điểm, nhận 2 tháng Premium."
- **Điều kiện cặp hợp lệ:** bài thi thử trong vòng 28 ngày trước hoặc sau ngày thi (FR-163); khoảng cách ngày được ghi làm biến trong hiệu chỉnh.
- **Kiểm chứng A7 ở tuần 1:** đăng lời mời thử vào 2–3 nhóm; ≥ 20 người đồng ý → tiếp tục; < 5 → xem lại phần thưởng hoặc hướng đi.

### 16.4 Cần bao nhiêu cặp (ước tính thô, tính lại khi có dữ liệu)

| Mốc | Số cặp/kỹ năng | Được làm gì |
|---|---|---|
| ~50 | Hiệu chỉnh nội bộ lần đầu | Không công bố gì |
| ~100 holdout | Ước lượng MAE với độ chính xác khoảng ±0,1 | **Công bố độ chính xác** (FR-174) |
| ~200–300, trải đều các mức 5.0–7.5 | Hiệu chỉnh riêng từng mức band | **Bật cam kết hoàn tiền** cho mức đạt ngưỡng (FR-175) |

### 16.5 Rủi ro riêng của dữ liệu

| Rủi ro | Giảm thiểu |
|---|---|
| Phiếu điểm giả để lấy thưởng | Thưởng chỉ sau khi làm bài thi thử; hash mã phiếu; cờ bất thường; duyệt tay giai đoạn đầu (FR-163, FR-164) |
| Chỉ người điểm cao mới gửi (thiên lệch) | Thưởng như nhau mọi mức band; theo dõi phân bố; báo cáo theo mức band (FR-173) |
| Khoảng cách ngày làm sai lệch | Giới hạn 28 ngày; khoảng cách là biến hiệu chỉnh |
| Bộ chấm thay đổi làm hỏng hiệu chỉnh | Rubric/model cố định (FR-076); đổi thì hiệu chỉnh lại (FR-176) |
| Rò rỉ dữ liệu phiếu điểm | Che thông tin trước khi tải, mã hóa, xóa ≤ 7 ngày (NFR-S10) |

---

## 17. Risks & Mitigations

| ID | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| R1 | AI chấm thiếu nhất quán | Med | High | Model cố định theo rubric version (FR-076), eval set (FR-091), validate bằng chứng (FR-031) |
| R2 | Chưa có chuyên gia/dataset tham chiếu | High | Med | Định vị "feedback luyện tập"; không quảng bá độ chính xác (FR-092); tuyển chuyên gia sau beta |
| R3 | Chi phí AI vượt ngân sách | Med | High | Credit theo tháng, prompt caching, chống chấm trùng, trần chi phí (FR-074) |
| R4 | Provider khóa tài khoản / gói miễn phí thay đổi | Med | Med | Không dùng gói miễn phí cho Lớp A; mỗi provider một tài khoản hợp lệ; fallback nhiều provider |
| R5 | Điểm không nhất quán do fallback sang model khác | Med | Med | FR-069: ghi nhận fallback, loại khỏi đường xu hướng |
| R6 | Vi phạm bản quyền đề | Low | High | Tự biên soạn, biểu đồ tự tạo, provenance, hoãn upload |
| R7 | Chậm onboarding payment provider | Med | Med | Xác nhận chuyển khoản thủ công có audit log (FR-064); kiểm tra điều kiện ở tuần 1 |
| R8 | Founder solo trễ tiến độ (Speaking làm tăng khối lượng) | High | High | Writing chỉ dựng lõi ở tuần 4–5; Should nằm cuối timeline; thứ tự cắt scope ở §18 (cắt Writing Task 1 trước lõi A + C) |
| R9 | Người dùng không trả tiền (sai giả thuyết) | Med | High | Open beta + bán từ tuần 16; đo O6; quyết định tiếp tục/điều chỉnh ở tuần 22 |
| R10 | Người chưa thành niên | Med | Med | Tối thiểu hóa dữ liệu, thông báo viết cho độ tuổi người dùng, rà soát pháp lý trước public launch |
| R11 | Người học thấy ChatGPT (kể cả chế độ giọng nói) "đủ dùng" để luyện | High | High | Không cạnh tranh ở tính năng luyện; cạnh tranh bằng dự đoán band thật (A) và cohort (C) (§2.7); đo O6 |
| R12 | Chấm phát âm không chính xác với giọng người Việt | Med | High | Xác minh speech provider ở tuần 1 (A5) và eval set Speaking (FR-091); chỉ hiện lỗi phát âm có độ tin cậy trên ngưỡng; nút báo sai |
| R13 | STT nghe sai khiến nhận xét ngữ pháp/từ vựng sai | Med | Med | Hiển thị transcript, báo lỗi transcript, hoàn credit khi xác nhận (FR-117) |
| R14 | Ghi âm lỗi trên một số trình duyệt, đặc biệt iOS | Med | Med | Kiểm tra micro trước khi thi (FR-106), lưu local và tự upload lại (FR-107), ma trận thiết bị `TBD-14` |
| R15 | Chi phí Speaking vượt 5.000đ/bài thi | Med | High | Kiểm tra ở tuần 1; cache TTS; điều chỉnh credit trước khi bán |
| R16 | License phi thương mại chặn nguồn 4 | High | Med | speechocean762 (CC BY) + eval set tự xây; xin license thương mại (TBD-15) |
| R17 | Quá ít người gửi phiếu điểm | Med | High | Kiểm chứng A7 ở tuần 1; điều chỉnh phần thưởng; cohort gắn hoàn cọc với gửi phiếu điểm |
| R18 | Dự đoán lệch nhiều khi đã công bố | Med | High | Chỉ công bố khi đủ holdout; hiển thị N và MAE thật; theo dõi liên tục sau công bố |
| R19 | Đặt cọc/hoàn tiền vướng pháp lý | Med | Med | Chỉ bật sau khi pháp lý duyệt (TBD-18); cohort vẫn chạy được khi không có cọc |
| R20 | ChatGPT/đối thủ cũng thu thập điểm thật | Low | High | Đi trước về dữ liệu người Việt; công bố sớm con số thật; cohort tạo cộng đồng |
| R21 | Đề L/R do AI soạn có đáp án sai hoặc mơ hồ | Med | High | Kiểm tra tự động (FR-213), checklist duyệt (FR-214), pilot + thống kê câu hỏi (FR-221), báo lỗi và chấm lại (FR-216) |
| R22 | Sản xuất đề L/R chiếm quá nhiều thời gian của Founder | High | High | Mục tiêu tối thiểu 6 bộ mỗi loại trước beta; có thể giảm còn 4 (§18); cân nhắc cộng tác viên duyệt (TBD-20) |
| R23 | Độ khó đề tự soạn khác đề thật làm lệch dự đoán L/R | Med | High | Bảng quy đổi riêng từng đề, chỉ dùng đề đã pilot cho dự đoán (FR-222), hiệu chỉnh bằng cặp điểm thật (FR-223) |
| R24 | Áp lực dùng đề crawl để có nhiều đề nhanh | Med | High | Cấm trong quy trình và công cụ import (FR-215); provenance bắt buộc |

---

## 18. Roadmap 22 tuần

| Tuần | Milestone | Deliverables | Pass criteria |
|---|---|---|---|
| 1–3 | **P0 — Nguồn 4 & nền tảng** | F21 dataset registry; đánh giá speech provider bằng speechocean762; gửi yêu cầu license (TBD-15); tuyển tình nguyện viên xây eval set; kiểm tra A1, A5, A2; chọn TTS (TBD-19); **đăng lời mời thử kiểm chứng A7**; data model §11.1 | Có danh sách provider Lớp A; chi phí Speaking ≤ 5.000đ/bài thi; eval set ≥ 30 Speaking + ≥ 40 Writing; A7 có kết quả |
| 4–5 | M1 — Lõi + Writing Task 2 | F1, F3 (Task 2), F4, F9 cơ bản | O1(b)(c) đạt trên eval set Writing |
| 6–8 | M2 — Speaking | F13, F14, taxonomy lỗi người Việt v1 (§14) | Thi đủ 3 Part → report ≤ 120s (p95); ghi âm chạy trên ma trận `TBD-14`; O1(b) đạt trên eval set Speaking |
| 9–11 | M3 — Listening & Reading engine | F22 (dạng câu hỏi bắt buộc, audio phát một lần, chấm tự động), F23 quy trình soạn đề + kiểm tra tự động, F24 bảng quy đổi v1 | Làm đủ 1 bộ L + 1 bộ R đầu-cuối; kiểm tra tự động bắt được lỗi đáp án cài sẵn |
| 9–15 | Song song — Sản xuất đề | Soạn, duyệt, pilot với tình nguyện viên | **≥ 6 bộ Listening + ≥ 6 bộ Reading** published trước tuần 16 `[Đề xuất]` |
| 12–13 | M4 — Dự đoán & thu thập | F16 (4 kỹ năng + overall, "chưa hiệu chỉnh"), F17 + luồng "Vừa thi xong", F8 credit + xác nhận chuyển khoản thủ công, F2, full mock | Luồng gửi phiếu điểm → duyệt → thưởng chạy đầu-cuối; ảnh tự xóa ≤ 7 ngày |
| 14–15 | M5 — Ổn định & pháp lý | Hardening, landing page theo §2.7, rà soát TBD-12, backup/restore | Không còn lỗi critical; TBD-12 đã có kết luận |
| 16 | **M6 — Open beta + bắt đầu bán** | Chiến dịch nguồn 1 | Thanh toán đầu tiên; cặp dữ liệu đầu tiên được xác minh |
| 17–18 | M7 — Cohort | F19 (chưa có cọc nếu TBD-18 chưa xong), F20 qua email, F18 trang dữ liệu hiệu chỉnh | **Cohort #1 khai giảng tuần 18** |
| 19–22 | M8 — Hoàn thiện & đo | F5, Writing Task 1, F10 đầy đủ, FR-074 trần chi phí; hiệu chỉnh bảng quy đổi L/R (FR-222) và hiệu chỉnh nội bộ lần đầu khi ≥ 50 cặp/kỹ năng; thêm đề đến ≥ 12 bộ mỗi loại | Đo O1–O7, O10; quyết định tiếp tục/điều chỉnh |
| Tháng 6–11 | M9 — Công bố & cam kết | Cohort #2–#4; ≥ 300 cặp/kỹ năng; công bố độ chính xác (FR-174); R1.5 khi O8 đạt | O8 đạt → bật FR-175 theo từng mức band |

**Thứ tự cắt scope nếu trễ:** FR-098 referral → FR-095 chia sẻ report → F6/FR-124 drill → FR-057 biểu đồ tiến bộ → FR-122 insight xuyên kỹ năng → FR-202 dạng câu hỏi L/R bổ sung → tự động hóa thanh toán (giữ xác nhận thủ công) → **Writing Task 1** (giữ Task 2) → kênh Zalo (giữ email) → đặt cọc (cohort vẫn chạy không cọc) → **giảm số bộ đề L/R trước open beta xuống 4 mỗi loại**.

**Không cắt:** F16 dự đoán, F17 thu thập kết quả, F18 hiệu chỉnh, F19 cohort cơ bản, Speaking (F13, F14), L/R engine và kiểm tra đáp án (F22, FR-213, FR-214) — đây là lõi của lợi thế A + C.

**Cũng không cắt:** bảo mật & cách ly dữ liệu, nhãn band không chính thức và nhãn trạng thái hiệu chỉnh, validate bằng chứng, autosave/lưu bản ghi, credit ở backend, xác minh thanh toán, phân loại dữ liệu Lớp A, không suy ra phát âm từ transcript, xóa audio sau 30 ngày, consent & xóa ảnh phiếu điểm, kiểm tra license dữ liệu, quyền nội dung.

---

## 19. Open Issues (TBD)

| ID | Nội dung | Hạn chốt |
|---|---|---|
| TBD-01 | Phân khúc beta (P1/P2/P3) và **duyệt các ngưỡng `[Đề xuất]`** (KPI, credit, giá gói, cohort, phần thưởng, NFR) | Trước tuần 15 |
| TBD-02 | Tên thương hiệu chung | Trước landing page (tuần 14) |
| TBD-03 | Kênh tăng trưởng chính | Tuần 4 |
| TBD-04 | AI provider/model Lớp A (chấm) và Lớp B/C; **speech provider** (STT, chấm phát âm, TTS) | Tuần 1 |
| TBD-05 | Rubric mapping chi tiết (Writing tuần 2, Speaking tuần 5), JSON schema, taxonomy lỗi v1 | Tuần 2 / tuần 5 |
| TBD-06 | Chính sách hoàn tiền | Trước tuần 16 |
| TBD-07 | Payment provider, điều kiện pháp lý, phí | Tuần 1 (kiểm tra), tuần 18 (tích hợp tự động) |
| TBD-08 | Hình thức pháp lý của Founder (cá nhân/hộ kinh doanh/doanh nghiệp) để thu tiền | Tuần 1 |
| TBD-09 | Email provider, lịch nhắc | Tuần 17 |
| TBD-10 | VPS/storage provider, trần chi phí hạ tầng, thời hạn backup | Tuần 1 |
| TBD-11 | Quy trình support và định nghĩa mức độ nghiêm trọng | Trước tuần 16 |
| TBD-12 | Rà soát pháp lý: dữ liệu cá nhân, **ghi âm giọng nói**, **phiếu điểm**, chuyển dữ liệu ra nước ngoài, người chưa thành niên, điều khoản, lưu chứng từ | Trước open beta (tuần 16) |
| TBD-13 | Người review có chuyên môn cho danh sách lỗi đặc trưng của người Việt (§14) và eval set Speaking | Tuần 3 |
| TBD-14 | Ma trận trình duyệt/thiết bị hỗ trợ ghi âm, định dạng/codec audio, thời lượng tối đa | Tuần 6 |
| TBD-15 | License thương mại cho bộ dữ liệu nguồn 4 (L2-ARCTIC, Cambridge S&I/W&I, ICNALE…) và xác nhận pháp lý về việc dùng bộ phi thương mại | Gửi yêu cầu tuần 1; kết luận tuần 3 |
| TBD-16 | Kênh nhắn tin chủ động (Zalo OA hoặc thay thế): chính sách, chi phí, điều kiện đăng ký | Tuần 16 |
| TBD-17 | Phần thưởng và điều kiện cặp dữ liệu hợp lệ (mức thưởng, cửa sổ 28 ngày) | Tuần 12 |
| TBD-18 | Pháp lý cho đặt cọc cohort, cam kết hoàn tiền theo kết quả, và quảng cáo độ chính xác | Đặt cọc: trước tuần 18; hoàn tiền: trước R1.5 |
| TBD-19 | Nhà cung cấp TTS cho audio Listening: chất lượng giọng, đa giọng, **quyền dùng thương mại** audio | Tuần 3 |
| TBD-20 | Người duyệt đề L/R (Founder hay cộng tác viên), định mức thời gian duyệt/bộ đề | Tuần 8 |

---

## 20. Traceability Matrix

> Test Case ID được đặt chỗ; nội dung test viết ở giai đoạn phát triển. Status: Todo.

| BR-ID | FR-ID(s) | NFR-ID(s) | Test Case(s) | Status |
|---|---|---|---|---|
| BR-001 | FR-010, FR-011, FR-020, FR-021, FR-022, FR-026, FR-030–FR-036, FR-090, FR-092 | NFR-P01, NFR-U04 | TC-001 – TC-012 | Todo |
| BR-002 | FR-012, FR-040–FR-044, FR-083, FR-208 | — | TC-020 – TC-025 | Todo |
| BR-003 | FR-011, FR-025, FR-027, FR-038, FR-039, FR-052, FR-060–FR-066, FR-071, FR-116, FR-209 | NFR-S08 | TC-030 – TC-040 | Todo |
| BR-004 | FR-051, FR-068, FR-070, FR-071, FR-074, FR-124 | NFR-COST01, NFR-COST02, NFR-COST03 | TC-045 – TC-049 | Todo |
| BR-005 | FR-005, FR-006, FR-067, FR-073 | NFR-S06, NFR-S09 | TC-050 – TC-053 | Todo |
| BR-006 | FR-013, FR-031, FR-036, FR-037, FR-045, FR-069, FR-072, FR-075, FR-076, FR-091, FR-111, FR-115, FR-117, FR-123 | NFR-M03 | TC-055 – TC-062 | Todo |
| BR-007 | FR-001–FR-005, FR-084 | NFR-S01–NFR-S05, NFR-S07 | TC-065 – TC-072 | Todo |
| BR-008 | FR-023–FR-025, FR-038, FR-068, FR-106–FR-108, FR-116, FR-203, FR-207 | NFR-P04, NFR-R02, NFR-R05, NFR-R06 | TC-075 – TC-079 | Todo |
| BR-009 | FR-037, FR-073, FR-080–FR-082, FR-085, FR-090, FR-117, FR-216 | NFR-R03, NFR-R04 | TC-080 – TC-085 | Todo |
| BR-010 | FR-040, §11.1 data model | NFR-PS02 | TC-088 – TC-089 | Todo |
| BR-011 | FR-050–FR-052, FR-124 | — | TC-090 – TC-092 | Todo |
| BR-012 | FR-055–FR-057 | NFR-U01 | TC-095 – TC-097 | Todo |
| BR-013 | FR-095, FR-096 | — | TC-100 – TC-101 | Todo |
| BR-014 | FR-066, FR-097 | — | TC-105 – TC-106 | Todo |
| BR-015 | FR-098 | — | TC-110 | Todo |
| BR-016 | FR-011, FR-044, FR-091, FR-100–FR-117 | NFR-P05, NFR-P06, NFR-R06, NFR-C04, NFR-S09 | TC-120 – TC-140 | Todo |
| BR-020 | FR-096, FR-113, FR-120, FR-121, FR-124 | — | TC-145 – TC-150 | Todo |
| BR-021 | FR-055, FR-122, FR-123 | — | TC-155 – TC-158 | Todo |
| BR-022 | FR-150–FR-155, FR-182, FR-207, FR-222 | NFR-P07, NFR-U04 | TC-160 – TC-166 | Todo |
| BR-023 | FR-160–FR-167 | NFR-S10, NFR-S11 | TC-170 – TC-178 | Todo |
| BR-024 | FR-152, FR-170–FR-174, FR-176, FR-221–FR-223 | — | TC-180 – TC-186 | Todo |
| BR-025 | FR-195–FR-197, FR-211 | — | TC-190 – TC-192 | Todo |
| BR-026 | FR-180–FR-183, FR-185, FR-186 | — | TC-195 – TC-200 | Todo |
| BR-027 | FR-190–FR-193 | — | TC-205 – TC-208 | Todo |
| BR-028 | FR-184, FR-185 | — | TC-210 – TC-212 | Todo |
| BR-017 | FR-044, FR-200–FR-206, FR-209, FR-212, FR-220–FR-223 | — | TC-220 – TC-235 | Todo |
| BR-030 | FR-210, FR-211, FR-213–FR-216 | — | TC-240 – TC-246 | Todo |

**Kiểm tra orphan:** mọi FR trong §8 đều trace về ≥ 1 BR; mọi BR in-scope đều có ≥ 1 FR. BR-018, BR-019 là Won't, không có FR ở R1. BR-029 (Won't ở R1) có FR-175 được xây sẵn công tắc nhưng khóa cho tới R1.5.

---

## 21. Glossary

| Term | Định nghĩa |
|---|---|
| Band ước lượng | Điểm do AI tạo ra để luyện tập, không phải điểm IELTS chính thức |
| Credit | Đơn vị tính một lượt chấm AI thành công |
| Error Memory | Kho lỗi của từng người học, gắn error tag và bài nguồn |
| Rewrite | Viết lại bài Writing đã chấm và so sánh với bản gốc |
| Redo | Trả lời lại câu/Part Speaking đã chấm và so sánh với lần trước |
| Chấm phát âm (pronunciation assessment) | Phân tích audio để đánh giá phát âm ở mức âm/từ; không suy ra từ transcript |
| STT / TTS | Chuyển giọng nói thành văn bản / chuyển văn bản thành giọng nói |
| Lỗi đặc trưng của người Việt | Lỗi phát âm/ngữ pháp phổ biến do ảnh hưởng tiếng Việt (§14) |
| Insight xuyên kỹ năng | Cảnh báo khi cùng một gốc lỗi (`root_cause`) xuất hiện ở cả Speaking và Writing |
| Band thật / dự đoán band | Dự đoán band khi thi thật, được hiệu chỉnh bằng kết quả thi thật (khác với band ước lượng theo rubric) |
| Cặp dữ liệu | Bài thi thử trên hệ thống và band thật của cùng người, trong khoảng ≤ 28 ngày |
| Hiệu chỉnh (calibration) | Điều chỉnh ánh xạ từ band ước lượng sang band thật dựa trên cặp dữ liệu |
| MAE | Sai số tuyệt đối trung bình giữa dự đoán và band thật |
| Holdout | Tập cặp dữ liệu giữ riêng để đo sai số, không dùng để hiệu chỉnh |
| Cohort | Nhóm học 8 tuần có ngày thi mục tiêu và lộ trình chung |
| Phiếu điểm (TRF) | Test Report Form — phiếu kết quả IELTS chính thức |
| Nguồn 1 / 3 / 4 | Người vừa thi xong / trung tâm–giáo viên / bộ dữ liệu công khai (§16) |
| Bảng quy đổi (conversion table) | Ánh xạ điểm thô 0–40 của một đề L/R sang band, riêng cho từng đề |
| Pilot | Giai đoạn đề mới được làm thử để đo độ khó trước khi dùng cho dự đoán |
| Item statistics | Thống kê từng câu hỏi: tỉ lệ đúng, độ phân biệt |
| Retest | Làm đề tương đương để kiểm tra lỗi lặp lại đã được sửa hay chưa |
| Lớp A / B / C | Phân loại dữ liệu gửi tới AI provider (§8.9) |
| Circuit breaker | Cơ chế tạm ngừng gọi provider đang lỗi và chuyển sang provider dự phòng |
| Prompt caching | Tính năng của provider giảm chi phí cho phần prompt lặp lại |
| Gate | Bộ điều kiện KPI phải đạt trước khi mở release/kỳ thi tiếp theo |
| Rubric version | Phiên bản bộ tiêu chí + prompt + model chấm chính + JSON schema |

---

## 22. Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Sponsor / Product Owner | Founder | | |
| Business Analyst | Claude (hỗ trợ soạn thảo) | — | 2026-09-27 |
