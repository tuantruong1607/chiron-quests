# IELTS Speaking & Writing Lab — Product Requirements Document (PRD / SRS)

> Chuẩn IIBA BABOK v3 (Agile Perspective) + cấu trúc SRS (BRD + FRD + NFR).
> Thay thế **IELTS Exam Lab PRD v1.0** và **PRD v1.1**. Release 1 tập trung vào hai kỹ năng
> **Speaking và Writing**, nơi AI tạo khác biệt thật sự so với ChatGPT; **Speaking là tính năng chính**.

---

## Document Control

| Field | Value |
|---|---|
| Document ID | PRD-2026-001 |
| Version | 1.2 |
| Status | Draft — chờ Founder duyệt |
| Owner | Founder (kiêm Sponsor / Product Owner / BA / Developer) |
| Created | 2026-09-27 (v1.0) |
| Last Updated | 2026-09-27 |
| Tên thương hiệu chung | `TBD-02` — ứng viên: "Chiron" (theo tên repo `chiron-quests`) |
| Tên sản phẩm Release 1 | IELTS Speaking & Writing Lab (tên làm việc) |

### Quy ước

- **PHẢI** (Must) — bắt buộc; thiếu = không phát hành. **NÊN** (Should) — khuyến nghị. **CÓ THỂ** (Could) — tùy chọn.
- Priority theo **MoSCoW**: `M` Must · `S` Should · `C` Could · `W` Won't (không làm trong release này).
- **`[Đề xuất]`** — con số/ngưỡng do BA đề xuất, **chưa được Founder duyệt**. Phải chốt trước mốc ghi trong §18.
- **`TBD-xx`** — quyết định còn mở, xem §18.

### Change Log

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-09-27 | Founder | Baseline: IELTS 4 kỹ năng, General Training, 49k/tháng, quota theo ngày |
| 1.1 | 2026-09-27 | BA (Claude) + Founder | Xem bảng "Thay đổi so với v1.0" bên dưới |
| 1.2 | 2026-09-27 | BA (Claude) + Founder | Release 1 = Speaking + Writing; định vị cạnh tranh với ChatGPT; xem bảng "Thay đổi so với v1.1" |

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

Tài liệu đặc tả yêu cầu business, chức năng và phi chức năng cho **Release 1 — IELTS Speaking & Writing Lab**,
đồng thời xác định lộ trình và các ràng buộc kiến trúc để mở rộng sang Listening/Reading, TOEIC và SAT.

### 1.2 Intended Audience

Founder (Sponsor/PO/Dev), cộng tác viên nội dung/QA tương lai, cố vấn pháp lý, chuyên gia IELTS (khi có).

### 1.3 Product Scope

Nền tảng web (responsive + PWA) giúp người học IELTS Academic tại Việt Nam luyện hai kỹ năng sản sinh:
- **Speaking:** thi thử Part 1 → 2 → 3 với giám khảo AI, đúng thời gian như phòng thi → report theo 4 tiêu chí, **phát âm được chấm bằng phân tích audio**, chỉ ra **lỗi đặc trưng của người Việt**.
- **Writing:** nộp Task 1/Task 2 → report theo 4 tiêu chí, gắn bằng chứng trong bài.

Cả hai kỹ năng dùng chung **Error Memory**: hệ thống ghi nhớ lỗi lặp lại, kể cả lỗi xuất hiện ở cả nói và viết → người học **làm lại / làm đề tương đương** → **kiểm chứng lỗi đã được sửa hay chưa**.

**Định vị:** *"Phòng luyện nói và viết IELTS dành riêng cho người Việt — biết bạn sai gì, sửa được chưa."*
Speaking là tính năng chính trong thông điệp bán hàng. Không định vị là "AI chấm IELTS" (tính năng này đã phổ biến). Band do AI tạo ra là **ước lượng phục vụ luyện tập**, không phải điểm chính thức.

### 1.4 References

- IELTS Exam Lab PRD v1.0 (2026-09-27)
- Biên bản đánh giá business (phiên làm việc 2026-09-27)
- IELTS Writing và Speaking Band Descriptors (public version) — dùng làm cơ sở rubric; không sao chép đề thi có bản quyền

---

## 2. Business Context (BACCM)

### 2.1 Change
Xây mới một sản phẩm luyện thi dựa trên AI, bắt đầu bằng **hai kỹ năng sản sinh (Speaking + Writing)**, là nơi AI tạo khác biệt rõ nhất so với ChatGPT. Beta kín từ tuần 8, bắt đầu thu tiền từ tuần 9, sau đó mở rộng theo từng release có điều kiện.

### 2.2 Need (giả thuyết cần kiểm chứng trong beta)

| # | Pain point | Bằng chứng hiện có |
|---|---|---|
| N1 | Người tự học không có phản hồi Writing nhất quán, cụ thể | Giả thuyết của Founder — cần xác nhận qua phỏng vấn beta |
| N2 | Chấm chữa bởi giáo viên/khóa học có chi phí cao so với ngân sách học sinh–sinh viên | Giả thuyết |
| N3 | Người học viết nhiều bài nhưng không biết lỗi nào lặp lại, lỗi nào đã sửa được | Giả thuyết |
| N4 | Chatbot AI thông thường không lưu lịch sử lỗi, không có quy trình thi và không đo tiến bộ | Giả thuyết |
| N5 | Người tự học không có môi trường luyện nói giống phòng thi (thời gian, cue card, câu hỏi nối tiếp) và không biết chính xác mình phát âm sai âm nào | Giả thuyết — cần xác nhận qua phỏng vấn beta |
| N6 | Gia sư Speaking 1-1 có chi phí cao và khó sắp lịch luyện thường xuyên | Giả thuyết |

### 2.3 Solution (high-level)
Speaking & Writing Lab gồm: (1) thi thử Speaking Part 1–3 với giám khảo AI; (2) chấm phát âm dựa trên audio và phát hiện lỗi đặc trưng của người Việt; (3) nộp bài Writing Task 1/Task 2 trong Exam Mode hoặc Practice Mode; (4) AI report theo tiêu chí có bằng chứng cho cả hai kỹ năng; (5) Error Memory và insight xuyên kỹ năng; (6) Redo/Rewrite & Retest; (7) Drill mục tiêu; (8) Credit/Premium; (9) Admin theo dõi chi phí và chất lượng.

### 2.4 Stakeholders — xem §4.

### 2.5 Value — xem §3 (Business Objectives).

### 2.6 Context

| Ràng buộc | Giá trị |
|---|---|
| Nhân lực | Founder solo |
| Ngân sách phát triển ban đầu | < 10.000.000 VNĐ |
| Thời gian | Beta kín từ tuần 8, bắt đầu bán từ tuần 9; đánh giá gate Release 2 ở tuần 12 |
| Tech stack | Next.js + TypeScript, FastAPI + Python, PostgreSQL, VPS, Docker Compose |
| Thị trường | Việt Nam, UI tiếng Việt, nội dung đề bằng tiếng Anh |
| Pháp lý | Bảo vệ dữ liệu cá nhân (xem §12); người dùng có thể là người chưa thành niên |
| Chuyên môn | Chưa có chuyên gia IELTS hoặc dataset tham chiếu được cấp phép |
| Cạnh tranh | ChatGPT/AI tổng quát miễn phí; các nền tảng luyện thi IELTS trong nước |

### 2.7 Định vị cạnh tranh

| Kỹ năng | Đối thủ thật | ChatGPT thay thế được? | AI của sản phẩm tạo khác biệt? | Quyết định |
|---|---|---|---|---|
| **Speaking** | Gia sư 1-1 | Một phần: hội thoại được, nhưng không mô phỏng phòng thi, không đo thời gian, không có điểm phát âm định lượng | **Nhiều nhất** | R1, tính năng chính |
| **Writing** | ChatGPT miễn phí | Gần như hoàn toàn nếu chỉ chấm một bài | Chỉ khi có Error Memory, điểm nhất quán và Retest | R1, kỹ năng thứ hai |
| Listening/Reading | Kho đề miễn phí/giá rẻ | Không liên quan (chấm theo đáp án) | Gần như không | R2 |

**5 điều sản phẩm làm được mà ChatGPT không làm được (phải hiện rõ trên landing page):**

1. Mô phỏng phòng thi Speaking: Part 1 → 2 → 3, 1 phút chuẩn bị, 2 phút nói, câu hỏi nối tiếp (F13).
2. Phát âm được chấm bằng phân tích audio ở mức âm/từ, không suy ra từ transcript (F14).
3. Nhận diện **lỗi đặc trưng của người Việt**: mất âm cuối, bỏ -s/-ed, /θ/ /ð/, trọng âm từ, thiếu mạo từ… (F15, §14).
4. **Insight xuyên kỹ năng:** "bạn bỏ -s ở động từ khi viết và cũng nuốt âm /s/ khi nói" (F15).
5. Điểm nhất quán theo thời gian nhờ model và rubric cố định, nên so sánh được để chứng minh tiến bộ (FR-076).

---

## 3. Business Objectives & KPI

> Tất cả ngưỡng dưới đây là **`[Đề xuất]`**, phải được Founder duyệt trước khi mở beta (TBD-01).

| # | Objective | KPI / Success Metric | Deadline |
|---|---|---|---|
| O1 | Chứng minh chất lượng feedback đủ dùng | (a) Tỉ lệ đánh giá 👍 trên report ≥ 70% (đo riêng Speaking và Writing); (b) chấm lại cùng một bài trong eval set: chênh lệch overall band ≤ 0,5 ở ≥ 90% bài; (c) 0 trường hợp trích dẫn bằng chứng không có trong bài/transcript | Tuần 8 (trước khi bán) |
| O2 | Chứng minh learning loop | ≥ 30% người đã nhận report có thực hiện Redo/Rewrite hoặc Retest trong 14 ngày | Tuần 12 |
| O3 | Chứng minh sẵn sàng trả tiền | ≥ 10 người trả phí **và** tỉ lệ chuyển đổi ≥ 3% trên người dùng hoạt động (≥ 1 bài nộp) trong 30 ngày | Tuần 12 |
| O4 | Unit economics dương | Chi phí AI ≤ 30% doanh thu thuần/người trả phí; chi phí trung bình ≤ 1.500đ/lượt Writing và ≤ 5.000đ/bài thi Speaking đủ 3 Part | Tuần 12 |
| O5 | Activation & retention | ≥ 60% người đăng ký nộp bài đầu tiên trong 7 ngày; ≥ 20% người dùng hoạt động quay lại ở tuần thứ 4 | Tuần 12 |
| O6 | Chứng minh Speaking là lý do mua | ≥ 50% người trả phí đã dùng Speaking trước khi thanh toán; ≥ 60% người trả lời khảo sát chọn Speaking là lý do chính | Tuần 12 |

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
| **R1 — IELTS Speaking & Writing Lab** | Speaking Part 1–3 (mô phỏng phòng thi, chấm phát âm, lỗi của người Việt), Writing Academic Task 1 + Task 2, Error Memory xuyên kỹ năng, Redo/Rewrite/Retest, credit & thanh toán | — | Tuần 1–12 |
| R2 — Listening/Reading + Full mock Academic | Chấm khách quan theo answer key, full mock 4 kỹ năng | O1, O3, O4, O6 đạt; có nguồn nội dung hợp pháp | Sau tuần 12 |
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

### 5.3 Out-of-Scope (R1)

- ❌ Listening, Reading, full mock — R2
- ❌ General Training Task 1 (letter) — có thể thêm sau vì dùng chung engine
- ❌ TOEIC, SAT — R3/R4
- ❌ Hội thoại Speaking tự do ngoài cấu trúc bài thi, luyện giọng bản ngữ theo vùng miền
- ❌ Upload tài liệu để chuyển thành bài luyện — rủi ro bản quyền
- ❌ AI Companion, Skill Garden 4 kỹ năng, streak/reward nâng cao
- ❌ App native iOS/Android, push notification
- ❌ Marketplace gia sư, social feed, hồ sơ công khai
- ❌ Cam kết độ chính xác band tương đương giám khảo; chứng nhận điểm
- ❌ Huấn luyện model từ dữ liệu người dùng

### 5.4 Boundaries / Interfaces

- Browser/PWA ↔ Next.js ↔ FastAPI (HTTPS)
- FastAPI ↔ AI Gateway ↔ các AI provider và speech provider bên ngoài (STT, chấm phát âm, TTS giọng giám khảo)
- FastAPI ↔ Payment adapter ↔ Payment provider (webhook)
- FastAPI ↔ Email provider; FastAPI ↔ Google OAuth

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
| BR-017 | Listening/Reading + full mock | W | Chuyển sang R2 | — |
| BR-018 | TOEIC, SAT | W | R3/R4 | — |
| BR-019 | Upload tài liệu, AI Companion, gamification nâng cao | W | Rủi ro bản quyền / không phải cốt lõi | — |
| BR-020 | Hệ thống PHẢI nhận diện và giải thích các lỗi đặc trưng của người Việt trong phát âm và ngữ pháp | M | Khác biệt so với feedback chung chung của AI tổng quát | O6, N5 |
| BR-021 | Hệ thống NÊN chỉ ra lỗi xuất hiện ở cả Speaking và Writing (insight xuyên kỹ năng) | S | Chỉ có được khi một hệ thống thấy cả hai kỹ năng | O2, O6 |

### MoSCoW Distribution (R1)

| Priority | Count | % in-scope |
|---|---|---|
| Must | 12 | 67% |
| Should | 5 | 28% |
| Could | 1 | 5% |
| **Total in-scope** | **18** | **100%** |
| Won't (R1) | 3 | — |

> ⚠️ Must chiếm 67% số BR, và Speaking làm tăng effort đáng kể. Theo quy tắc 60/40, **effort** của nhóm Must nên ≤ 60% capacity; §17 đưa các BR Should về cuối timeline và liệt kê thứ tự cắt scope.

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
| A6 | STT đủ chính xác với giọng tiếng Anh của người Việt để transcript dùng làm bằng chứng — kiểm chứng bằng eval set Speaking ở tuần 5 |
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
| FR-044 | Ngân hàng đề R1 PHẢI đủ để Retest: ≥ 30 đề Writing Task 2, ≥ 15 đề Task 1, ≥ 20 chủ đề Speaking Part 1 (mỗi chủ đề 4–5 câu), ≥ 30 cue card Part 2 kèm câu hỏi Part 3 `[Đề xuất]`, đã qua quality gate §11.3 | BR-002, BR-016 | Đếm trong admin |
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
- Nếu A5 cho thấy chi phí Speaking > 5.000đ/bài thi, phải tăng credit/Part hoặc giảm credit/tháng trước khi bán (tuần 9).

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

---

## 9. Non-Functional Requirements

> Các target có nhãn `[Đề xuất]` chờ duyệt trước tuần 8.

### 9.1 Performance

| ID | Requirement | Metric | Target |
|---|---|---|---|
| NFR-P01 | Thời gian trả report Writing | p50 / p95 từ lúc nộp | ≤ 45s / ≤ 90s `[Đề xuất]` |
| NFR-P02 | API không liên quan AI | p95 latency | ≤ 500ms |
| NFR-P03 | Tải trang trên 4G, điện thoại tầm trung | Largest Contentful Paint | ≤ 2,5s |
| NFR-P04 | Autosave local | Độ trễ sau lần gõ cuối | ≤ 5s |
| NFR-P05 | Thời gian trả report Speaking đủ 3 Part | p50 / p95 từ lúc nộp | ≤ 60s / ≤ 120s `[Đề xuất]` |
| NFR-P06 | Độ trễ giữa hai câu hỏi của giám khảo AI | Từ lúc dừng ghi âm đến lúc phát câu hỏi tiếp theo | ≤ 2s; câu hỏi nối tiếp Part 3 ≤ 5s |

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

### 9.4 Usability

| ID | Requirement | Target |
|---|---|---|
| NFR-U01 | Từ đăng ký đến nộp bài diagnostic | Trung vị ≤ 5 phút (không tính thời gian viết) |
| NFR-U02 | Accessibility luồng chính | WCAG 2.1 AA: điều khiển bằng bàn phím, focus rõ, tương phản |
| NFR-U03 | Ngôn ngữ | UI tiếng Việt; nội dung đề tiếng Anh; UI tiếng Anh ở release sau |
| NFR-U04 | Minh bạch AI | Nhãn "ước lượng — không chính thức" hiển thị ở 100% vị trí có band |

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
| Speech provider(s) | STT, chấm phát âm ở mức âm/từ (Lớp A); TTS giọng giám khảo và mẫu phát âm (Lớp B, cache lại) | HTTPS REST / streaming | API key (backend) | `TBD-04`; cùng yêu cầu Lớp A như AI provider |
| Payment provider | Thu tiền | HTTPS REST + webhook | API key + chữ ký HMAC | `TBD-07`; ưu tiên VietQR / ví điện tử, thanh toán một lần |
| Email provider | Xác thực, nhắc học, cảnh báo chi phí | HTTPS API / SMTP | API key | `TBD-09` |
| Object storage | Ảnh biểu đồ Task 1, audio ghi âm, audio TTS đã cache | S3-compatible | Access key, URL ký hạn ngắn | `TBD-10` |

---

## 11. Data Requirements

### 11.1 Data model (thiết kế sẵn sàng đa kỳ thi)

| Entity | Trường chính | Ghi chú mở rộng |
|---|---|---|
| `exam_family` | IELTS / TOEIC / SAT | R1 chỉ có IELTS |
| `exam_variant` | Academic / General Training / TOEIC LR / Digital SAT | R1 chỉ có Academic |
| `section`, `task_type` | Writing Task 1/2, Speaking Part 1/2/3 … | Cấu trúc section, thời gian (chuẩn bị, thời lượng nói) và luật điều hướng lưu trong metadata, không hard-code UI |
| `item` (đề) | id, version, nội dung, dữ liệu biểu đồ (Task 1), độ khó, provenance, quyền sử dụng, cờ AI-generated, trạng thái review | Registry dạng câu hỏi mở rộng được (câu nhóm, ảnh, tự điền, LaTeX) |
| `scoring_strategy` | rubric_ai (IELTS Writing), speech_rubric_ai (IELTS Speaking), answer_key, raw_to_band, raw_to_scaled (TOEIC), adaptive_module (SAT) | R1 triển khai rubric_ai và speech_rubric_ai |
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

> ⚠️ Chỉ đặt đúng tên và trường ở R1. Phần triển khai dùng chung thực sự làm khi bắt tay vào R4 (TOEIC), tránh trừu tượng hóa quá sớm.

### 11.2 Data Retention

| Loại dữ liệu | Thời hạn | Xử lý khi hết hạn |
|---|---|---|
| Bài làm, report, Error Memory | Đến khi người dùng xóa hoặc xóa tài khoản | Xóa vĩnh viễn |
| Audio ghi âm | 30 ngày | Tự động xóa, kể cả bản tạm và bản local đã upload xong |
| Log vận hành AI (không có nội dung bài) | 90 ngày `[Đề xuất]` | Xóa |
| Giao dịch thanh toán | Theo nghĩa vụ kế toán/thuế (`TBD-12`) | Lưu trữ |
| Backup | `TBD-10`; công bố cách dữ liệu đã xóa hết vòng đời trong backup | Xoay vòng |

### 11.3 Content Quality Gates (trước khi publish đề)

1. Validate schema. 2. Kiểm tra dữ liệu biểu đồ khớp hình hiển thị (Task 1). 3. Nghe lại audio TTS câu hỏi Speaking. 4. Kiểm tra quyền sử dụng & provenance. 5. Review nội dung AI-generated. 6. Nội dung chưa chắc chắn giữ ở trạng thái draft.

---

## 12. Compliance & Legal

| Hạng mục | Áp dụng | Ghi chú |
|---|---|---|
| Luật Bảo vệ dữ liệu cá nhân 2025 và Nghị định 13/2023/NĐ-CP (cùng văn bản hướng dẫn hiện hành) | ✅ | Thông báo & chấp thuận, xóa dữ liệu, chuyển dữ liệu tới AI/speech provider (có thể ở nước ngoài) — **cần rà soát pháp lý `TBD-12`** |
| Giọng nói (ghi âm) | ✅ | Cần xác định giọng nói có thuộc nhóm dữ liệu cá nhân nhạy cảm theo quy định hiện hành hay không; chấp thuận riêng trước khi ghi âm; không dùng để nhận dạng danh tính — **`TBD-12`** |
| Người chưa thành niên (P2) | ✅ | Thông báo viết cho độ tuổi người dùng, tối thiểu hóa dữ liệu; cơ chế đồng ý của cha mẹ/người giám hộ theo quy định — bắt buộc trước R5 (SAT), rà soát cho R1 |
| Bảo vệ người tiêu dùng / thương mại điện tử | ✅ | Hiển thị giá, điều kiện hoàn tiền, không tự gia hạn ngầm |
| Bản quyền nội dung đề | ✅ | Chỉ nội dung tự biên soạn/có quyền; không dùng đề thi thật có bản quyền |
| Điều khoản sử dụng của AI provider | ✅ | Mỗi provider một tài khoản hợp lệ; không lách hạn mức miễn phí |
| PCI-DSS | ❌ | Không lưu dữ liệu thẻ |

---

## 13. Monetization & Unit Economics

| Gói | Giá | Credit | Ghi chú |
|---|---|---|---|
| Free | 0đ | Diagnostic + 3 credit tổng `[Đề xuất]` | Đủ trải nghiệm vòng lặp chấm → rewrite |
| Premium tháng | **69.000đ** | 30/tháng `[Đề xuất]` (VD: 10 bài thi Speaking đủ 3 Part, hoặc 30 bài Writing, hoặc kết hợp) | Không tự gia hạn trong R1 |
| Gói 3 tháng | 179.000đ `[Đề xuất]` | 90 trong 3 tháng | Khớp chu kỳ ôn thi |

**Công thức theo dõi (O4):**
`AI cost ratio = Σ(credit đã dùng theo loại × chi phí trung bình/credit của loại đó) ÷ doanh thu thuần` — mục tiêu ≤ 30%. Theo dõi riêng Speaking và Writing.

---

## 14. Lỗi đặc trưng của người Việt — danh sách khởi đầu

> Đây là **giả thuyết ban đầu** dựa trên các lỗi phổ biến của người học tiếng Anh có tiếng mẹ đẻ là tiếng Việt. Phải kiểm chứng và tinh chỉnh bằng eval set Speaking/Writing (FR-091) và người review có chuyên môn (`TBD-13`) trước tuần 8.

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

## 16. Risks & Mitigations

| ID | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| R1 | AI chấm thiếu nhất quán | Med | High | Model cố định theo rubric version (FR-076), eval set (FR-091), validate bằng chứng (FR-031) |
| R2 | Chưa có chuyên gia/dataset tham chiếu | High | Med | Định vị "feedback luyện tập"; không quảng bá độ chính xác (FR-092); tuyển chuyên gia sau beta |
| R3 | Chi phí AI vượt ngân sách | Med | High | Credit theo tháng, prompt caching, chống chấm trùng, trần chi phí (FR-074) |
| R4 | Provider khóa tài khoản / gói miễn phí thay đổi | Med | Med | Không dùng gói miễn phí cho Lớp A; mỗi provider một tài khoản hợp lệ; fallback nhiều provider |
| R5 | Điểm không nhất quán do fallback sang model khác | Med | Med | FR-069: ghi nhận fallback, loại khỏi đường xu hướng |
| R6 | Vi phạm bản quyền đề | Low | High | Tự biên soạn, biểu đồ tự tạo, provenance, hoãn upload |
| R7 | Chậm onboarding payment provider | Med | Med | Xác nhận chuyển khoản thủ công có audit log (FR-064); kiểm tra điều kiện ở tuần 1 |
| R8 | Founder solo trễ tiến độ (Speaking làm tăng khối lượng) | High | High | Writing chỉ dựng lõi ở tuần 2–4; Should nằm cuối timeline; thứ tự cắt scope ở §17 (có thể cắt Writing Task 1 trước khi cắt Speaking) |
| R9 | Người dùng không trả tiền (sai giả thuyết) | Med | High | Beta kín tuần 8, bán từ tuần 9; đo O6; gate ở tuần 12 quyết định tiếp tục/pivot |
| R10 | Người chưa thành niên | Med | Med | Tối thiểu hóa dữ liệu, thông báo viết cho độ tuổi người dùng, rà soát pháp lý trước public launch |
| R11 | Người học thấy ChatGPT (kể cả chế độ giọng nói) "đủ dùng" | Med | High | Định vị theo 5 điểm khác biệt ở §2.7; landing page trình diễn chấm phát âm (FR-096); đo O6 |
| R12 | Chấm phát âm không chính xác với giọng người Việt | Med | High | Xác minh speech provider ở tuần 1 (A5) và eval set Speaking (FR-091); chỉ hiện lỗi phát âm có độ tin cậy trên ngưỡng; nút báo sai |
| R13 | STT nghe sai khiến nhận xét ngữ pháp/từ vựng sai | Med | Med | Hiển thị transcript, báo lỗi transcript, hoàn credit khi xác nhận (FR-117) |
| R14 | Ghi âm lỗi trên một số trình duyệt, đặc biệt iOS | Med | Med | Kiểm tra micro trước khi thi (FR-106), lưu local và tự upload lại (FR-107), ma trận thiết bị `TBD-14` |
| R15 | Chi phí Speaking vượt 5.000đ/bài thi | Med | High | Kiểm tra ở tuần 1; cache TTS; điều chỉnh credit trước khi bán |

---

## 17. Roadmap 12 tuần

| Tuần | Milestone | Deliverables | Pass criteria |
|---|---|---|---|
| 1 | M0 — Nền tảng & kiểm chứng speech | Schema đề/rubric/taxonomy, data model §11.1, Docker Compose, CI; kiểm tra A1 (AI provider), **A5 (speech provider: chất lượng với giọng Việt + chi phí/bài thi)**, A2 (payment) | App/API chạy local; có danh sách provider Lớp A; **chi phí Speaking đo được ≤ 5.000đ/bài thi** hoặc có phương án điều chỉnh |
| 2–4 | M1 — Lõi hệ thống qua Writing Task 2 | F1, F3 (Task 2), F4, F9 (cơ bản), Error Memory cơ bản, eval set Writing v1 | Đăng nhập → viết → reload → nộp → report có bằng chứng; O1(b)(c) đạt trên eval set Writing |
| 5–7 | M2 — **Speaking** | F13 (Part 1–3, kiểm tra micro, lưu local/upload lại), F14 (transcript, chấm phát âm, Fluency từ audio), taxonomy lỗi người Việt v1 (§14), eval set Speaking | Thi đủ 3 Part → report ≤ 120s (p95); Pronunciation chỉ từ phân tích audio; ghi âm chạy trên ma trận thiết bị `TBD-14`; alpha nội bộ 5 người |
| 8 | M3 — Beta kín (miễn phí) | F2 diagnostic, F5 Redo/Rewrite/Retest, F15 nhãn lỗi người Việt, F8 credit; tuyển 20–50 beta tester | O1 đo được cho cả hai kỹ năng; không có lỗi mất bản ghi |
| 9–10 | M4 — **Bắt đầu bán** | Xác nhận chuyển khoản thủ công (FR-064), Writing Task 1, insight xuyên kỹ năng (FR-122), FR-096 "đọc thử 3 câu", landing page theo §2.7 | Thanh toán đầu tiên thành công; O6 bắt đầu được đo |
| 11–12 | M5 — Vận hành, đo & quyết định | F10 đầy đủ, FR-074 trần chi phí, xóa dữ liệu + xóa audio 30 ngày, backup/restore; đo O1–O6; phỏng vấn beta | Diễn tập restore thành công; **Gate R2** |

**Thứ tự cắt scope nếu trễ:** FR-098 referral → FR-097 email → FR-095 chia sẻ report → F6/FR-124 drill → FR-057 biểu đồ tiến bộ → tự động hóa thanh toán (giữ xác nhận thủ công) → **Writing Task 1** (giữ Task 2) → FR-122 insight xuyên kỹ năng.

**Không cắt Speaking** (F13, F14): đây là lý do sản phẩm tồn tại so với ChatGPT.

**Không cắt:** bảo mật & cách ly dữ liệu, nhãn band không chính thức, validate bằng chứng, autosave/lưu bản ghi, credit ở backend, xác minh thanh toán, phân loại dữ liệu Lớp A, không suy ra phát âm từ transcript, xóa audio sau 30 ngày, quyền nội dung.

---

## 18. Open Issues (TBD)

| ID | Nội dung | Hạn chốt |
|---|---|---|
| TBD-01 | Phân khúc beta (P1/P2/P3) và **duyệt các ngưỡng `[Đề xuất]`** (KPI, credit, giá gói 3 tháng, NFR) | Trước tuần 8 |
| TBD-02 | Tên thương hiệu chung | Trước landing page (tuần 5) |
| TBD-03 | Kênh tăng trưởng chính | Tuần 4 |
| TBD-04 | AI provider/model Lớp A (chấm) và Lớp B/C; **speech provider** (STT, chấm phát âm, TTS) | Tuần 1 |
| TBD-05 | Rubric mapping chi tiết (Writing tuần 2, Speaking tuần 5), JSON schema, taxonomy lỗi v1 | Tuần 2 / tuần 5 |
| TBD-06 | Chính sách hoàn tiền | Trước tuần 9 |
| TBD-07 | Payment provider, điều kiện pháp lý, phí | Tuần 1 (kiểm tra), tuần 8 (tích hợp) |
| TBD-08 | Hình thức pháp lý của Founder (cá nhân/hộ kinh doanh/doanh nghiệp) để thu tiền | Tuần 1 |
| TBD-09 | Email provider, lịch nhắc | Tuần 9 |
| TBD-10 | VPS/storage provider, trần chi phí hạ tầng, thời hạn backup | Tuần 1 |
| TBD-11 | Quy trình support và định nghĩa mức độ nghiêm trọng | Trước tuần 8 |
| TBD-12 | Rà soát pháp lý: dữ liệu cá nhân, **ghi âm giọng nói**, chuyển dữ liệu ra nước ngoài, người chưa thành niên, điều khoản, lưu chứng từ | Trước beta kín (tuần 8) cho phần ghi âm; trước public launch cho phần còn lại |
| TBD-13 | Người review có chuyên môn cho danh sách lỗi đặc trưng của người Việt (§14) và eval set Speaking | Tuần 5 |
| TBD-14 | Ma trận trình duyệt/thiết bị hỗ trợ ghi âm, định dạng/codec audio, thời lượng tối đa | Tuần 5 |

---

## 19. Traceability Matrix

> Test Case ID được đặt chỗ; nội dung test viết ở giai đoạn phát triển. Status: Todo.

| BR-ID | FR-ID(s) | NFR-ID(s) | Test Case(s) | Status |
|---|---|---|---|---|
| BR-001 | FR-010, FR-011, FR-020, FR-021, FR-022, FR-026, FR-030–FR-036, FR-090, FR-092 | NFR-P01, NFR-U04 | TC-001 – TC-012 | Todo |
| BR-002 | FR-012, FR-040–FR-044, FR-083 | — | TC-020 – TC-025 | Todo |
| BR-003 | FR-011, FR-025, FR-027, FR-038, FR-039, FR-052, FR-060–FR-066, FR-071, FR-116 | NFR-S08 | TC-030 – TC-040 | Todo |
| BR-004 | FR-051, FR-068, FR-070, FR-071, FR-074, FR-124 | NFR-COST01, NFR-COST02, NFR-COST03 | TC-045 – TC-049 | Todo |
| BR-005 | FR-005, FR-006, FR-067, FR-073 | NFR-S06, NFR-S09 | TC-050 – TC-053 | Todo |
| BR-006 | FR-013, FR-031, FR-036, FR-037, FR-045, FR-069, FR-072, FR-075, FR-076, FR-091, FR-111, FR-115, FR-117, FR-123 | NFR-M03 | TC-055 – TC-062 | Todo |
| BR-007 | FR-001–FR-005, FR-084 | NFR-S01–NFR-S05, NFR-S07 | TC-065 – TC-072 | Todo |
| BR-008 | FR-023–FR-025, FR-038, FR-068, FR-106–FR-108, FR-116 | NFR-P04, NFR-R02, NFR-R05, NFR-R06 | TC-075 – TC-079 | Todo |
| BR-009 | FR-037, FR-073, FR-080–FR-082, FR-085, FR-090, FR-117 | NFR-R03, NFR-R04 | TC-080 – TC-085 | Todo |
| BR-010 | FR-040, §11.1 data model | NFR-PS02 | TC-088 – TC-089 | Todo |
| BR-011 | FR-050–FR-052, FR-124 | — | TC-090 – TC-092 | Todo |
| BR-012 | FR-055–FR-057 | NFR-U01 | TC-095 – TC-097 | Todo |
| BR-013 | FR-095, FR-096 | — | TC-100 – TC-101 | Todo |
| BR-014 | FR-066, FR-097 | — | TC-105 – TC-106 | Todo |
| BR-015 | FR-098 | — | TC-110 | Todo |
| BR-016 | FR-011, FR-044, FR-091, FR-100–FR-117 | NFR-P05, NFR-P06, NFR-R06, NFR-C04, NFR-S09 | TC-120 – TC-140 | Todo |
| BR-020 | FR-096, FR-113, FR-120, FR-121, FR-124 | — | TC-145 – TC-150 | Todo |
| BR-021 | FR-055, FR-122, FR-123 | — | TC-155 – TC-158 | Todo |

**Kiểm tra orphan:** mọi FR trong §8 đều trace về ≥ 1 BR; mọi BR in-scope đều có ≥ 1 FR. BR-017 – BR-019 là Won't, không có FR ở R1.

---

## 20. Glossary

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
| Retest | Làm đề tương đương để kiểm tra lỗi lặp lại đã được sửa hay chưa |
| Lớp A / B / C | Phân loại dữ liệu gửi tới AI provider (§8.9) |
| Circuit breaker | Cơ chế tạm ngừng gọi provider đang lỗi và chuyển sang provider dự phòng |
| Prompt caching | Tính năng của provider giảm chi phí cho phần prompt lặp lại |
| Gate | Bộ điều kiện KPI phải đạt trước khi mở release/kỳ thi tiếp theo |
| Rubric version | Phiên bản bộ tiêu chí + prompt + model chấm chính + JSON schema |

---

## 21. Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Sponsor / Product Owner | Founder | | |
| Business Analyst | Claude (hỗ trợ soạn thảo) | — | 2026-09-27 |
