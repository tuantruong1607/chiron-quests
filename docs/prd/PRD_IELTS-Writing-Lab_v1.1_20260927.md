# IELTS Writing Lab — Product Requirements Document (PRD / SRS)

> Chuẩn IIBA BABOK v3 (Agile Perspective) + cấu trúc SRS (BRD + FRD + NFR).
> Thay thế **IELTS Exam Lab PRD v1.0**. Phạm vi Release 1 được thu hẹp theo nguyên tắc
> **"sản phẩm đầu tiên phải dễ làm, dễ bán"**.

---

## Document Control

| Field | Value |
|---|---|
| Document ID | PRD-2026-001 |
| Version | 1.1 |
| Status | Draft — chờ Founder duyệt |
| Owner | Founder (kiêm Sponsor / Product Owner / BA / Developer) |
| Created | 2026-09-27 (v1.0) |
| Last Updated | 2026-09-27 |
| Tên thương hiệu chung | `TBD-02` — ứng viên: "Chiron" (theo tên repo `chiron-quests`) |
| Tên sản phẩm Release 1 | IELTS Writing Lab (tên làm việc) |

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

### Thay đổi so với v1.0 (tóm tắt quyết định đã chốt)

| # | Hạng mục | v1.0 | v1.1 | Lý do |
|---|---|---|---|---|
| 1 | Phạm vi Release 1 | 4 kỹ năng + full mock | **Chỉ Writing** (Academic Task 1 + Task 2) | Dễ làm: không cần audio/STT/sản xuất đề nghe-đọc. Dễ bán: Writing là phần khó tự đánh giá nhất, sẵn sàng trả tiền cao nhất |
| 2 | Loại đề | General Training | **Academic** | Đa số người học IELTS tại VN thi Academic |
| 3 | Giá Premium | 49.000đ/tháng | **69.000đ/tháng** + **gói 3 tháng** | Cải thiện unit economics; khớp chu kỳ ôn thi 2–4 tháng |
| 4 | Quota | 1/ngày (Free), 5/ngày (Premium) | **Credit theo tháng**; Free cấp theo tổng số lượt | Quota theo ngày (150 lượt/tháng) có thể vượt doanh thu |
| 5 | Chiến lược AI | Provider abstraction | + **Phân loại dữ liệu**, **model chấm cố định**, **caching**, **circuit breaker giữa các provider** | Kiểm soát chi phí mà không vi phạm privacy/ToS, giữ điểm nhất quán |
| 6 | Tầm nhìn | Chỉ IELTS | **Nền tảng đa kỳ thi**: IELTS → TOEIC → SAT, có gate KPI | Tăng LTV theo vòng đời người học |
| 7 | KPI | TBD | **Ngưỡng `[Đề xuất]`** chờ duyệt | Cần đo được "thành công" trước beta |
| 8 | Thu tiền | Tuần 10 | **Từ tuần 6**, cho phép xác nhận chuyển khoản thủ công | Kiểm chứng sẵn sàng trả tiền sớm nhất |
| 9 | Upload tài liệu | P1 | **Won't** (hoãn) | Rủi ro bản quyền (người dùng upload sách đề có bản quyền) |

---

## 1. Introduction

### 1.1 Purpose

Tài liệu đặc tả yêu cầu business, chức năng và phi chức năng cho **Release 1 — IELTS Writing Lab**,
đồng thời xác định lộ trình và các ràng buộc kiến trúc để mở rộng sang IELTS 4 kỹ năng, TOEIC và SAT.

### 1.2 Intended Audience

Founder (Sponsor/PO/Dev), cộng tác viên nội dung/QA tương lai, cố vấn pháp lý, chuyên gia IELTS (khi có).

### 1.3 Product Scope

Nền tảng web (responsive + PWA) giúp người học IELTS Academic tại Việt Nam:
nộp bài Writing → nhận **report AI theo 4 tiêu chí, gắn bằng chứng trong bài** → hệ thống
**ghi nhớ lỗi lặp lại** → người học **viết lại / làm đề tương đương** → **kiểm chứng lỗi đã được sửa hay chưa**.

**Định vị:** *"Biết chính xác bạn đang mắc lỗi gì — và đã sửa được chưa."*
Không định vị là "AI chấm IELTS" (tính năng này đã phổ biến). Band do AI tạo ra là **ước lượng phục vụ luyện tập**, không phải điểm chính thức.

### 1.4 References

- IELTS Exam Lab PRD v1.0 (2026-09-27)
- Biên bản đánh giá business (phiên làm việc 2026-09-27)
- IELTS Writing Band Descriptors (public version) — dùng làm cơ sở rubric; không sao chép đề thi có bản quyền

---

## 2. Business Context (BACCM)

### 2.1 Change
Xây mới một sản phẩm luyện thi dựa trên AI, bắt đầu bằng **một kỹ năng duy nhất (Writing)** để ra thị trường và bắt đầu thu tiền từ tuần 6, sau đó mở rộng theo từng release có điều kiện.

### 2.2 Need (giả thuyết cần kiểm chứng trong beta)

| # | Pain point | Bằng chứng hiện có |
|---|---|---|
| N1 | Người tự học không có phản hồi Writing nhất quán, cụ thể | Giả thuyết của Founder — cần xác nhận qua phỏng vấn beta |
| N2 | Chấm chữa bởi giáo viên/khóa học có chi phí cao so với ngân sách học sinh–sinh viên | Giả thuyết |
| N3 | Người học viết nhiều bài nhưng không biết lỗi nào lặp lại, lỗi nào đã sửa được | Giả thuyết |
| N4 | Chatbot AI thông thường không lưu lịch sử lỗi, không có quy trình thi và không đo tiến bộ | Giả thuyết |

### 2.3 Solution (high-level)
Writing Lab gồm: (1) nộp bài Task 1/Task 2 trong Exam Mode hoặc Practice Mode; (2) AI report theo tiêu chí có bằng chứng; (3) Error Memory; (4) Rewrite & Retest; (5) Drill mục tiêu; (6) Credit/Premium; (7) Admin theo dõi chi phí và chất lượng.

### 2.4 Stakeholders — xem §4.

### 2.5 Value — xem §3 (Business Objectives).

### 2.6 Context

| Ràng buộc | Giá trị |
|---|---|
| Nhân lực | Founder solo |
| Ngân sách phát triển ban đầu | < 10.000.000 VNĐ |
| Thời gian | Paid beta từ tuần 6; đánh giá gate Release 2 ở tuần 12 |
| Tech stack | Next.js + TypeScript, FastAPI + Python, PostgreSQL, VPS, Docker Compose |
| Thị trường | Việt Nam, UI tiếng Việt, nội dung đề bằng tiếng Anh |
| Pháp lý | Bảo vệ dữ liệu cá nhân (xem §12); người dùng có thể là người chưa thành niên |
| Chuyên môn | Chưa có chuyên gia IELTS hoặc dataset tham chiếu được cấp phép |

---

## 3. Business Objectives & KPI

> Tất cả ngưỡng dưới đây là **`[Đề xuất]`**, phải được Founder duyệt trước khi mở beta (TBD-01).

| # | Objective | KPI / Success Metric | Deadline |
|---|---|---|---|
| O1 | Chứng minh chất lượng feedback đủ dùng | (a) Tỉ lệ đánh giá 👍 trên report ≥ 70%; (b) chấm lại cùng một bài trong eval set: chênh lệch overall band ≤ 0,5 ở ≥ 90% bài; (c) 0 trường hợp trích dẫn bằng chứng không có trong bài | Tuần 6 (trước paid beta) |
| O2 | Chứng minh learning loop | ≥ 30% người đã nhận report có thực hiện Rewrite hoặc Retest trong 14 ngày | Tuần 12 |
| O3 | Chứng minh sẵn sàng trả tiền | ≥ 10 người trả phí **và** tỉ lệ chuyển đổi ≥ 3% trên người dùng hoạt động (≥ 1 bài nộp) trong 30 ngày | Tuần 12 |
| O4 | Unit economics dương | Chi phí AI ≤ 30% doanh thu thuần/người trả phí; chi phí trung bình ≤ 1.500đ/lượt chấm | Tuần 12 |
| O5 | Activation & retention | ≥ 60% người đăng ký nộp bài đầu tiên trong 7 ngày; ≥ 20% người dùng hoạt động quay lại ở tuần thứ 4 | Tuần 12 |

**Lưu ý:** 300 lượt đăng ký (mục tiêu v1.0) được giữ làm chỉ số theo dõi acquisition, **không** dùng làm tiêu chí thành công.

---

## 4. Stakeholders

| Role | Người/đơn vị | Trách nhiệm | Influence | Interest |
|---|---|---|---|---|
| Sponsor / Product Owner / BA / Dev | Founder | Ngân sách, ưu tiên, phát triển, duyệt | High | High |
| End-user chính | Người học IELTS Academic tại VN (phân khúc cụ thể: `TBD-01`) | Sử dụng, trả phí, phản hồi | Low | High |
| Beta tester | 20–50 người học | Kiểm chứng giả thuyết, UAT | Med | High |
| AI provider | Nhà cung cấp LLM (`TBD-04`) | Chấm bài, tạo nội dung | Med | Low |
| Payment provider | `TBD-07` (ưu tiên hỗ trợ VietQR / ví điện tử) | Thu tiền, webhook | Med | Low |
| Cố vấn pháp lý | `TBD-12` | Privacy, điều khoản, người chưa thành niên | Med | Low |
| Chuyên gia IELTS | Chưa có — tuyển sau | Đánh giá độc lập chất lượng chấm | High (uy tín) | Med |
| Giáo viên / trung tâm (tương lai) | Kênh B2B2C tiềm năng | Dùng công cụ chấm cho học viên | Med | Med |

---

## 5. Scope

### 5.1 Release plan (đa kỳ thi, có gate)

| Release | Nội dung | Điều kiện mở (Gate) | Thời điểm |
|---|---|---|---|
| **R1 — IELTS Writing Lab** | Academic Task 1 + Task 2, AI report, Error Memory, Rewrite/Retest, credit & thanh toán | — | Tuần 1–12 |
| R2 — Speaking | Part 1–3, STT + LLM, chấm phát âm khi có phân tích audio | O1, O3, O4 đạt | Sau tuần 12 |
| R3 — Listening/Reading + Full mock Academic | Chấm khách quan theo answer key, full mock 4 kỹ năng | R2 ổn định; có nguồn nội dung hợp pháp | Sau R2 |
| R4 — TOEIC Listening & Reading | 7 Part, bảng quy đổi điểm, drill từ vựng | IELTS: conversion ≥ 3%, AI cost ≤ 30% doanh thu, W4 retention đạt O5 `[Đề xuất]` | Sau R3 |
| R5 — SAT (Digital) | Adaptive theo module, Math (LaTeX, máy tính), luồng đồng ý của phụ huynh | R4 đạt gate tương đương; rà soát pháp lý cho người chưa thành niên | Sau R4 |

### 5.2 In-Scope (R1)

- ✅ Đăng ký/đăng nhập, quản lý tài khoản, xóa dữ liệu
- ✅ Writing diagnostic khi onboarding (1 bài Task 2)
- ✅ Nộp bài Academic Task 1 và Task 2 (Exam Mode + Practice Mode, autosave)
- ✅ AI report theo 4 tiêu chí, bằng chứng, inline highlight, nhãn "ước lượng — không chính thức"
- ✅ Error Memory, Rewrite (so sánh bản sửa), Retest bằng đề tương đương
- ✅ Drill mục tiêu (nội dung tạo sẵn và cache)
- ✅ Lịch sử & tiến bộ Writing
- ✅ Free / Premium tháng / gói 3 tháng, hệ thống credit, thanh toán
- ✅ AI Gateway: phân loại dữ liệu, model chấm cố định, caching, circuit breaker, trần chi phí
- ✅ Admin: user, usage/cost, feedback, import nội dung
- ✅ Data model sẵn sàng đa kỳ thi (không làm tính năng TOEIC/SAT)

### 5.3 Out-of-Scope (R1)

- ❌ Speaking, Listening, Reading, full mock — R2/R3
- ❌ General Training Task 1 (letter) — có thể thêm sau vì dùng chung engine
- ❌ TOEIC, SAT — R4/R5
- ❌ Upload tài liệu để chuyển thành bài luyện — rủi ro bản quyền
- ❌ AI Companion, Skill Garden 4 kỹ năng, streak/reward nâng cao
- ❌ App native iOS/Android, push notification
- ❌ Marketplace gia sư, social feed, hồ sơ công khai
- ❌ Cam kết độ chính xác band tương đương giám khảo; chứng nhận điểm
- ❌ Huấn luyện model từ dữ liệu người dùng

### 5.4 Boundaries / Interfaces

- Browser/PWA ↔ Next.js ↔ FastAPI (HTTPS)
- FastAPI ↔ AI Gateway ↔ các AI provider bên ngoài
- FastAPI ↔ Payment adapter ↔ Payment provider (webhook)
- FastAPI ↔ Email provider; FastAPI ↔ Google OAuth

---

## 6. Business Requirements

| ID | Description | Priority | Rationale | Source |
|---|---|---|---|---|
| BR-001 | Người học PHẢI nộp được bài IELTS Academic Writing Task 1 và Task 2 và nhận report AI theo 4 tiêu chí, có bằng chứng trong bài | M | Giá trị cốt lõi, lý do trả tiền | O1, N1 |
| BR-002 | Hệ thống PHẢI ghi nhớ lỗi lặp lại và cho phép Rewrite/Retest để kiểm chứng lỗi đã sửa | M | Điểm khác biệt so với chatbot/đối thủ | O2, N3, N4 |
| BR-003 | Hệ thống PHẢI thu phí qua Premium 69.000đ/tháng và gói 3 tháng, dựa trên credit; Free cấp theo tổng số lượt | M | Kiểm chứng sẵn sàng trả tiền | O3 |
| BR-004 | Chi phí AI PHẢI được kiểm soát dưới trần ngân sách theo tháng và theo người dùng | M | Rủi ro tài chính lớn nhất của sản phẩm AI | O4 |
| BR-005 | Bài làm và dữ liệu cá nhân của người dùng CHỈ được gửi tới provider có cam kết không dùng dữ liệu để huấn luyện | M | Privacy, pháp lý, uy tín | §12 |
| BR-006 | Việc chấm PHẢI nhất quán giữa các lần để so sánh tiến bộ có ý nghĩa | M | Error Memory và Retest phụ thuộc vào điểm nhất quán | O1, O2 |
| BR-007 | Tài khoản PHẢI an toàn, dữ liệu giữa người dùng PHẢI được cách ly | M | Bảo mật cơ bản | — |
| BR-008 | Bài đang viết KHÔNG được mất khi reload hoặc mất mạng tạm thời | M | Mất bài = mất niềm tin | O5 |
| BR-009 | Hệ thống PHẢI cung cấp số liệu vận hành (usage, chi phí, lỗi, feedback) cho Founder | M | Điều hành một mình | O1, O4 |
| BR-010 | Data model và entitlement PHẢI hỗ trợ thêm kỳ thi mới mà không đổi cấu trúc lõi | M | Chi phí thấp nếu làm bây giờ, rất cao nếu làm sau | §15 |
| BR-011 | Hệ thống NÊN đề xuất drill mục tiêu dựa trên điểm yếu | S | Tăng giá trị gói Premium | O2 |
| BR-012 | Hệ thống NÊN hiển thị tiến bộ Writing theo thời gian | S | Retention | O5 |
| BR-013 | Người dùng NÊN chia sẻ được report (opt-in) | S | Kênh tăng trưởng tự nhiên | O3 |
| BR-014 | Hệ thống NÊN gửi email nhắc học cho người opt-in | S | Retention | O5 |
| BR-015 | Hệ thống CÓ THỂ có referral có chống lạm dụng | C | Tăng trưởng | O3 |
| BR-016 | Speaking AI grading | W | Chuyển sang R2 | — |
| BR-017 | Listening/Reading + full mock | W | Chuyển sang R3 | — |
| BR-018 | TOEIC, SAT | W | R4/R5 | — |
| BR-019 | Upload tài liệu, AI Companion, gamification nâng cao | W | Rủi ro bản quyền / không phải cốt lõi | — |

### MoSCoW Distribution (R1)

| Priority | Count | % in-scope |
|---|---|---|
| Must | 10 | 67% |
| Should | 4 | 27% |
| Could | 1 | 6% |
| **Total in-scope** | **15** | **100%** |
| Won't (R1) | 4 | — |

> ⚠️ Must chiếm 67% số BR. Theo quy tắc 60/40, **effort** của nhóm Must nên ≤ 60% capacity; §17 đã sắp xếp để các BR Should nằm ở tuần 7–10 và có thể cắt.

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
| P2 — Học sinh xét tuyển / du học | 16–18 tuổi (**có thể chưa thành niên**), mục tiêu 6.5–7.5 | Luyện Writing đều đặn, thấy tiến bộ |
| P3 — Người đi làm tự học | 23–30 tuổi, ít thời gian | Buổi luyện ≤ 30 phút, nhận report ≤ 90 giây (NFR-P01) |

### 7.3 Operating Environment

- Trình duyệt: Chrome, Edge, Safari, Firefox — 2 phiên bản mới nhất; iOS Safari ≥ 16; Android Chrome ≥ 2 phiên bản mới nhất.
- Thiết bị: desktop, tablet, mobile; chiều rộng tối thiểu 360px. Writing Exam Mode khuyến nghị bàn phím vật lý (hiển thị cảnh báo trên mobile).

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
| FR-006 | Hệ thống PHẢI hiển thị điều khoản và thông báo quyền riêng tư (gồm việc xử lý bài làm qua AI provider) và ghi nhận chấp thuận trước lần nộp bài đầu tiên | BR-005 | AC-F1-6 |

**Acceptance Criteria**

- **AC-F1-1** — Given người dùng chưa có tài khoản, When đăng nhập bằng Google và cấp quyền, Then tài khoản được tạo và người dùng vào màn hình onboarding.
- **AC-F1-2** — Given đã đăng ký bằng email, When nhập sai mật khẩu 5 lần trong 15 phút, Then các lần thử tiếp theo bị chặn 15 phút và thông báo không tiết lộ tài khoản có tồn tại.
- **AC-F1-3** — Given link reset đã tạo quá 30 phút, When người dùng mở link, Then hệ thống từ chối và cho phép yêu cầu link mới.
- **AC-F1-4** — Given người dùng A đăng nhập, When gọi API lấy report của người dùng B bằng ID, Then API trả 404 và không lộ dữ liệu.
- **AC-F1-5** — Given người dùng xác nhận xóa tài khoản, When quá trình xóa hoàn tất, Then bài làm/report/Error Memory không còn truy cập được và người dùng nhận email xác nhận.
- **AC-F1-6** — Given người dùng chưa chấp thuận thông báo xử lý dữ liệu, When bấm nộp bài lần đầu, Then hệ thống hiển thị thông báo và chỉ gửi bài đi chấm sau khi người dùng chấp thuận.

### 8.2 Feature F2 — Onboarding & Writing Diagnostic (Priority: M)

| ID | Functional Requirement | Source BR | AC |
|---|---|---|---|
| FR-010 | Hệ thống PHẢI cho phép nhập band mục tiêu và ngày thi dự kiến (không bắt buộc, sửa được) | BR-001 | Có thể bỏ qua; sửa trong Settings |
| FR-011 | Hệ thống PHẢI cung cấp bài diagnostic gồm 1 đề Task 2; lượt chấm diagnostic đầu tiên không trừ credit | BR-001, BR-003 | AC-F2-1 |
| FR-012 | Sau diagnostic, hệ thống PHẢI hiển thị 3 điểm yếu ưu tiên kèm bằng chứng và gợi ý bước tiếp theo | BR-002 | AC-F2-2 |
| FR-013 | Hệ thống PHẢI phân biệt rõ mục tiêu do người dùng khai báo và ước lượng do AI tạo | BR-006 | Nhãn riêng trên UI |

- **AC-F2-1** — Given người dùng mới hoàn tất đăng ký, When nộp bài diagnostic hợp lệ (≥ 150 từ), Then nhận report và số credit không thay đổi.
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
| FR-040 | Hệ thống PHẢI gắn mỗi lỗi với một error tag trong taxonomy chung (domain → subskill → error tag) và lưu bài nguồn | BR-002, BR-010 | AC-F5-1 |
| FR-041 | Hệ thống PHẢI đánh dấu lỗi "lặp lại" khi cùng error tag xuất hiện ở ≥ 2 bài khác nhau | BR-002 | AC-F5-1 |
| FR-042 | Rewrite: người học PHẢI viết lại được bài đã chấm; hệ thống PHẢI so sánh bản gốc và bản sửa, chỉ rõ lỗi nào đã sửa/chưa sửa | BR-002 | AC-F5-2 |
| FR-043 | Retest: hệ thống PHẢI gợi ý đề tương đương (cùng task type, cùng chủ đề/dạng) nhắm vào lỗi lặp lại | BR-002 | AC-F5-3 |
| FR-044 | Ngân hàng đề R1 PHẢI đủ để Retest: ≥ 30 đề Task 2 và ≥ 15 đề Task 1 `[Đề xuất]`, đã qua quality gate §11.3 | BR-002 | Đếm trong admin |
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
| FR-055 | Dashboard NÊN hiển thị: CTA "Viết bài mới", report gần nhất, top 3 lỗi lặp lại, số credit còn lại | BR-012 | 4 khối hiển thị |
| FR-056 | Lịch sử PHẢI liệt kê mọi bài đã nộp, lọc theo Task 1/Task 2 | BR-012 | Lọc hoạt động |
| FR-057 | Biểu đồ tiến bộ NÊN hiển thị band theo tiêu chí qua thời gian, tuân theo FR-045 | BR-012 | AC-F5-4 |

### 8.8 Feature F8 — Gói, credit & thanh toán (Priority: M)

**Business Rules**

| ID | Rule |
|---|---|
| RULE-01 | 1 credit = 1 lượt chấm Writing (Task 1 hoặc Task 2 hoặc bản Rewrite) được xử lý thành công |
| RULE-02 | Free: 3 credit **tổng cộng** cho mỗi tài khoản `[Đề xuất]` + lượt diagnostic miễn phí (FR-011) |
| RULE-03 | Premium tháng: 69.000đ, 30 credit/tháng `[Đề xuất]`; credit không dùng hết hết hạn cuối kỳ |
| RULE-04 | Gói 3 tháng: 179.000đ `[Đề xuất]`, 90 credit dùng trong 3 tháng |
| RULE-05 | Speaking (R2) sẽ tiêu tốn nhiều credit hơn Writing (VD: 2–3 credit/lượt) — chốt ở R2 |
| RULE-06 | Lỗi xử lý, nộp trùng, mở lại report, drill khách quan: không trừ credit |
| RULE-07 | Credit và entitlement dùng chung cho mọi kỳ thi trong tương lai (một ví credit/người dùng) |
| RULE-08 | Mốc reset credit tính theo múi giờ Asia/Ho_Chi_Minh và hiển thị trong UI |
| RULE-09 | Premium chỉ được kích hoạt sau khi thanh toán được xác minh (webhook có chữ ký, hoặc admin xác nhận thủ công có audit log trong giai đoạn beta) |

**Cơ sở con số (RULE-03):** doanh thu thuần ≈ 67.000đ/tháng. Nếu dùng hết 30 credit × 1.500đ = 45.000đ, vẫn dưới doanh thu. Nếu mức dùng trung bình ~30% → ~13.500đ ≈ 20% doanh thu, đạt O4.

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
| **A — Dữ liệu người dùng** | Bài làm, (R2) ghi âm, thông tin cá nhân | **Chỉ gói trả phí** có cam kết bằng văn bản không dùng dữ liệu để huấn luyện; ưu tiên có tùy chọn không lưu trữ |
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
| FR-091 | Hệ thống PHẢI có eval set nội bộ tự biên soạn (≥ 40 bài Task 2, ≥ 20 bài Task 1 `[Đề xuất]`) và chạy lại trước mọi thay đổi prompt/model | BR-006 | Báo cáo eval lưu theo version |
| FR-092 | Sản phẩm KHÔNG được quảng bá độ chính xác band khi chưa có đánh giá độc lập của chuyên gia | BR-001 | Rà soát nội dung landing page |

### 8.12 Feature F12 — Tăng trưởng (Priority: S/C)

| ID | Functional Requirement | Source BR | Priority |
|---|---|---|---|
| FR-095 | Người dùng NÊN tạo được link chia sẻ report (opt-in), xem trước nội dung, thu hồi được link; mặc định ẩn toàn văn bài | BR-013 | S |
| FR-096 | Landing page NÊN có công cụ miễn phí "chấm thử 1 đoạn mở bài" (giới hạn theo IP/thiết bị) | BR-013 | S |
| FR-097 | Hệ thống NÊN gửi email nhắc học (opt-in), có unsubscribe, tối đa 2 email/tuần `[Đề xuất]` | BR-014 | S |
| FR-098 | Hệ thống CÓ THỂ có referral: người giới thiệu và người được giới thiệu nhận credit sau khi người được giới thiệu **thanh toán** (chống lạm dụng) | BR-015 | C |

**Kênh tăng trưởng chính:** chọn **một** kênh ở `TBD-03`. Ứng viên: nhóm Facebook/cộng đồng IELTS (tặng chấm thử để đổi lấy feedback), TikTok/Shorts ("band 5.5 → sửa lên 6.5"), hoặc B2B2C qua giáo viên/trung tâm nhỏ.

---

## 9. Non-Functional Requirements

> Các target có nhãn `[Đề xuất]` chờ duyệt trước tuần 6.

### 9.1 Performance

| ID | Requirement | Metric | Target |
|---|---|---|---|
| NFR-P01 | Thời gian trả report Writing | p50 / p95 từ lúc nộp | ≤ 45s / ≤ 90s `[Đề xuất]` |
| NFR-P02 | API không liên quan AI | p95 latency | ≤ 500ms |
| NFR-P03 | Tải trang trên 4G, điện thoại tầm trung | Largest Contentful Paint | ≤ 2,5s |
| NFR-P04 | Autosave local | Độ trễ sau lần gõ cuối | ≤ 5s |

### 9.2 Reliability & Availability

| ID | Requirement | Target |
|---|---|---|
| NFR-R01 | Uptime hằng tháng (beta) | ≥ 99% `[Đề xuất]` |
| NFR-R02 | Tỉ lệ chấm thành công (sau retry + fallback) | ≥ 98% |
| NFR-R03 | RPO | ≤ 24 giờ (backup hằng ngày, lưu ngoài VPS chính) |
| NFR-R04 | RTO | ≤ 8 giờ `[Đề xuất]`; diễn tập khôi phục ≥ 1 lần/tháng trong beta |
| NFR-R05 | Mất bài đã gõ do lỗi hệ thống | 0 trường hợp được xác nhận |

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

### 9.7 Portability, Scalability & Cost

| ID | Requirement | Target |
|---|---|---|
| NFR-PS01 | Tải đồng thời trên 1 VPS | ≥ 200 người dùng đồng thời `[Đề xuất]` |
| NFR-PS02 | Đổi AI provider/model | Bằng cấu hình, không cần deploy code |
| NFR-PS03 | Đóng gói | Docker Compose chạy được trên VPS mới ≤ 1 giờ |
| NFR-COST01 | Chi phí AI/lượt chấm Writing | Trung bình ≤ 1.500đ `[Đề xuất]` |
| NFR-COST02 | Chi phí hạ tầng hằng tháng (VPS, storage, email) | Trần: `TBD-10` |

---

## 10. External Interface Requirements

| System | Mục đích | Giao thức | Xác thực | Ghi chú |
|---|---|---|---|---|
| Google OAuth | Đăng nhập | OAuth 2.0 / OIDC | Client ID + Secret | — |
| AI provider(s) | Chấm bài (Lớp A), tạo nội dung (Lớp B/C) | HTTPS REST | API key (backend) | `TBD-04`; danh sách Lớp A phải có cam kết không huấn luyện |
| Payment provider | Thu tiền | HTTPS REST + webhook | API key + chữ ký HMAC | `TBD-07`; ưu tiên VietQR / ví điện tử, thanh toán một lần |
| Email provider | Xác thực, nhắc học, cảnh báo chi phí | HTTPS API / SMTP | API key | `TBD-09` |
| Object storage | Ảnh biểu đồ Task 1, (R2) audio | S3-compatible | Access key, URL ký hạn ngắn | `TBD-10` |

---

## 11. Data Requirements

### 11.1 Data model (thiết kế sẵn sàng đa kỳ thi)

| Entity | Trường chính | Ghi chú mở rộng |
|---|---|---|
| `exam_family` | IELTS / TOEIC / SAT | R1 chỉ có IELTS |
| `exam_variant` | Academic / General Training / TOEIC LR / Digital SAT | R1 chỉ có Academic |
| `section`, `task_type` | Writing Task 1/2 … | Cấu trúc section, thời gian và luật điều hướng lưu trong metadata, không hard-code UI |
| `item` (đề) | id, version, nội dung, dữ liệu biểu đồ (Task 1), độ khó, provenance, quyền sử dụng, cờ AI-generated, trạng thái review | Registry dạng câu hỏi mở rộng được (câu nhóm, ảnh, tự điền, LaTeX) |
| `scoring_strategy` | rubric_ai (IELTS Writing), answer_key, raw_to_band, raw_to_scaled (TOEIC), adaptive_module (SAT) | R1 chỉ triển khai rubric_ai |
| `rubric_version` | tiêu chí, prompt version, model chấm chính, JSON schema version | Xem FR-076 |
| `attempt` | user, item, mode, nội dung, version, trạng thái | — |
| `report` | band, tiêu chí, nhận xét + bằng chứng, model/provider, rubric version, cờ fallback | — |
| `error_taxonomy` | domain → subskill → error tag | Dùng chung cho mọi kỳ thi (VD: lỗi ngữ pháp dùng lại cho TOEIC) |
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
| (R2) Audio ghi âm | 30 ngày | Tự động xóa, kể cả bản tạm |
| Log vận hành AI (không có nội dung bài) | 90 ngày `[Đề xuất]` | Xóa |
| Giao dịch thanh toán | Theo nghĩa vụ kế toán/thuế (`TBD-12`) | Lưu trữ |
| Backup | `TBD-10`; công bố cách dữ liệu đã xóa hết vòng đời trong backup | Xoay vòng |

### 11.3 Content Quality Gates (trước khi publish đề)

1. Validate schema. 2. Kiểm tra dữ liệu biểu đồ khớp hình hiển thị (Task 1). 3. Kiểm tra quyền sử dụng & provenance. 4. Review nội dung AI-generated. 5. Nội dung chưa chắc chắn giữ ở trạng thái draft.

---

## 12. Compliance & Legal

| Hạng mục | Áp dụng | Ghi chú |
|---|---|---|
| Luật Bảo vệ dữ liệu cá nhân 2025 và Nghị định 13/2023/NĐ-CP (cùng văn bản hướng dẫn hiện hành) | ✅ | Thông báo & chấp thuận, xóa dữ liệu, chuyển dữ liệu tới AI provider (có thể ở nước ngoài) — **cần rà soát pháp lý `TBD-12`** |
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
| Premium tháng | **69.000đ** | 30/tháng `[Đề xuất]` | Không tự gia hạn trong R1 |
| Gói 3 tháng | 179.000đ `[Đề xuất]` | 90 trong 3 tháng | Khớp chu kỳ ôn thi |

**Công thức theo dõi (O4):**
`AI cost ratio = (credit đã dùng × chi phí trung bình/lượt) ÷ doanh thu thuần` — mục tiêu ≤ 30%.

---

## 14. (Dành chỗ) Speaking — R2

Giữ nguyên nguyên tắc v1.0: STT + LLM, không kết luận phát âm chỉ từ transcript, audio tự xóa sau 30 ngày, trạng thái xử lý, retry an toàn, Speaking tiêu tốn nhiều credit hơn (RULE-05). Đặc tả chi tiết sẽ viết khi R2 qua gate.

---

## 15. Chiến lược đa kỳ thi

### 15.1 Khác biệt giữa các kỳ thi

| | IELTS | TOEIC | SAT (Digital) |
|---|---|---|---|
| Người học VN | 16–25 tuổi | Sinh viên, người đi làm | Học sinh THPT (phần lớn chưa thành niên) |
| Sẵn sàng trả tiền | Trung bình–khá | Thấp, số lượng lớn | Cao (thường phụ huynh trả) |
| Giá trị cốt lõi | Chấm AI Writing/Speaking | Kho đề lớn, phân tích theo Part, từ vựng | Adaptive, Math, mô phỏng giao diện thi |
| Thành phần dùng lại từ R1 | — | Auth, credit/thanh toán, Error Memory, taxonomy, admin | Như TOEIC + engine làm bài |

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
| R8 | Founder solo trễ tiến độ | High | Med | R1 chỉ Writing; Should nằm cuối timeline, cắt được |
| R9 | Người dùng không trả tiền (sai giả thuyết) | Med | High | Thu tiền từ tuần 6; gate ở tuần 12 quyết định tiếp tục/pivot |
| R10 | Người chưa thành niên | Med | Med | Tối thiểu hóa dữ liệu, thông báo viết cho độ tuổi người dùng, rà soát pháp lý trước public launch |
| R11 | Chỉ có Writing khiến sản phẩm "mỏng" | Med | Med | Định vị Error Memory + Rewrite/Retest làm giá trị chính; roadmap R2 công khai |

---

## 17. Roadmap 12 tuần

| Tuần | Milestone | Deliverables | Pass criteria |
|---|---|---|---|
| 1 | M0 — Nền tảng | Schema đề/rubric/taxonomy, data model §11.1, Docker Compose, CI; kiểm tra A1 (AI provider Lớp A) và A2 (payment) | App/API chạy local; 1 đề mẫu validate; có danh sách provider Lớp A |
| 2–4 | M1 — Vertical slice Task 2 | F1, F3 (Task 2), F4, F9 (cơ bản), eval set v1 | Đăng nhập → viết → reload → nộp → report có bằng chứng; O1(b)(c) đạt trên eval set; alpha nội bộ 5 người |
| 5–6 | M2 — Có thể bán | Task 1 Academic, F5 (Error Memory, Rewrite, Retest), F8 (credit + xác nhận chuyển khoản thủ công), F2 | **Mở paid beta 20–50 người**; thanh toán đầu tiên thành công; O1(a) được đo |
| 7–8 | M3 — Giữ chân | F6 drill, F7 dashboard, FR-095 chia sẻ report, tự động hóa thanh toán qua provider | Webhook idempotent đạt test; drill không gọi AI khi đã có trong kho |
| 9–10 | M4 — Vận hành | F10 đầy đủ, FR-074 trần chi phí, FR-097 email, xóa dữ liệu, backup/restore | Diễn tập restore thành công; cảnh báo chi phí hoạt động |
| 11–12 | M5 — Đo & quyết định | Đo O1–O5, phỏng vấn beta | **Gate R2**: đạt → Speaking; không đạt → điều chỉnh giá/định vị/phân khúc |

**Thứ tự cắt scope nếu trễ:** FR-098 referral → FR-096 công cụ miễn phí → FR-057 biểu đồ tiến bộ → F6 drill → tự động hóa thanh toán (giữ xác nhận thủ công).

**Không cắt:** bảo mật & cách ly dữ liệu, nhãn band không chính thức, validate bằng chứng, autosave, credit ở backend, xác minh thanh toán, phân loại dữ liệu Lớp A, quyền nội dung.

---

## 18. Open Issues (TBD)

| ID | Nội dung | Hạn chốt |
|---|---|---|
| TBD-01 | Phân khúc beta (P1/P2/P3) và **duyệt các ngưỡng `[Đề xuất]`** (KPI, credit, giá gói 3 tháng, NFR) | Trước tuần 6 |
| TBD-02 | Tên thương hiệu chung | Trước landing page (tuần 5) |
| TBD-03 | Kênh tăng trưởng chính | Tuần 4 |
| TBD-04 | AI provider/model Lớp A (chấm) và Lớp B/C | Tuần 1 |
| TBD-05 | Rubric mapping chi tiết, JSON schema, taxonomy lỗi v1 | Tuần 2 |
| TBD-06 | Chính sách hoàn tiền | Trước tuần 6 |
| TBD-07 | Payment provider, điều kiện pháp lý, phí | Tuần 1 (kiểm tra), tuần 8 (tích hợp) |
| TBD-08 | Hình thức pháp lý của Founder (cá nhân/hộ kinh doanh/doanh nghiệp) để thu tiền | Tuần 1 |
| TBD-09 | Email provider, lịch nhắc | Tuần 9 |
| TBD-10 | VPS/storage provider, trần chi phí hạ tầng, thời hạn backup | Tuần 1 |
| TBD-11 | Quy trình support và định nghĩa mức độ nghiêm trọng | Trước tuần 6 |
| TBD-12 | Rà soát pháp lý: dữ liệu cá nhân, chuyển dữ liệu ra nước ngoài, người chưa thành niên, điều khoản, lưu chứng từ | Trước public launch |

---

## 19. Traceability Matrix

> Test Case ID được đặt chỗ; nội dung test viết ở giai đoạn phát triển. Status: Todo.

| BR-ID | FR-ID(s) | NFR-ID(s) | Test Case(s) | Status |
|---|---|---|---|---|
| BR-001 | FR-010, FR-011, FR-020, FR-021, FR-022, FR-026, FR-030–FR-036, FR-090, FR-092 | NFR-P01, NFR-U04 | TC-001 – TC-012 | Todo |
| BR-002 | FR-012, FR-040–FR-044, FR-083 | — | TC-020 – TC-025 | Todo |
| BR-003 | FR-011, FR-025, FR-027, FR-038, FR-039, FR-052, FR-060–FR-066, FR-071 | NFR-S08 | TC-030 – TC-040 | Todo |
| BR-004 | FR-051, FR-068, FR-070, FR-071, FR-074 | NFR-COST01, NFR-COST02 | TC-045 – TC-049 | Todo |
| BR-005 | FR-005, FR-006, FR-067, FR-073 | NFR-S06 | TC-050 – TC-053 | Todo |
| BR-006 | FR-013, FR-031, FR-036, FR-037, FR-045, FR-069, FR-072, FR-075, FR-076, FR-091 | NFR-M03 | TC-055 – TC-062 | Todo |
| BR-007 | FR-001–FR-005, FR-084 | NFR-S01–NFR-S05, NFR-S07 | TC-065 – TC-072 | Todo |
| BR-008 | FR-023–FR-025, FR-038, FR-068 | NFR-P04, NFR-R02, NFR-R05 | TC-075 – TC-079 | Todo |
| BR-009 | FR-037, FR-073, FR-080–FR-082, FR-085, FR-090 | NFR-R03, NFR-R04 | TC-080 – TC-085 | Todo |
| BR-010 | FR-040, §11.1 data model | NFR-PS02 | TC-088 – TC-089 | Todo |
| BR-011 | FR-050–FR-052 | — | TC-090 – TC-092 | Todo |
| BR-012 | FR-055–FR-057 | NFR-U01 | TC-095 – TC-097 | Todo |
| BR-013 | FR-095, FR-096 | — | TC-100 – TC-101 | Todo |
| BR-014 | FR-066, FR-097 | — | TC-105 – TC-106 | Todo |
| BR-015 | FR-098 | — | TC-110 | Todo |

**Kiểm tra orphan:** mọi FR trong §8 đều trace về ≥ 1 BR; mọi BR in-scope đều có ≥ 1 FR. BR-016 – BR-019 là Won't, không có FR ở R1.

---

## 20. Glossary

| Term | Định nghĩa |
|---|---|
| Band ước lượng | Điểm do AI tạo ra để luyện tập, không phải điểm IELTS chính thức |
| Credit | Đơn vị tính một lượt chấm AI thành công |
| Error Memory | Kho lỗi của từng người học, gắn error tag và bài nguồn |
| Rewrite | Viết lại bài đã chấm và so sánh với bản gốc |
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
