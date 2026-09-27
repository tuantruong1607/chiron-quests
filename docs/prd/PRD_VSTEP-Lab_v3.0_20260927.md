# VSTEP Lab — Product Requirements Document (PRD / SRS)

> Chuẩn IIBA BABOK v3 (Agile Perspective) + cấu trúc SRS (BRD + FRD + NFR).
> **Đổi thị trường** từ IELTS (PRD v1.0–v2.1) sang **VSTEP** (Bài thi đánh giá năng lực tiếng Anh bậc 3–5 theo Khung năng lực ngoại ngữ 6 bậc dùng cho Việt Nam).
> Chiến lược: **"Đậu B1 nhanh nhất, rẻ nhất"** — sản phẩm ra nhanh hơn, giá thấp hơn rõ rệt so với đối thủ, dự đoán "đủ bậc chưa", cohort theo đợt thi. Tái sử dụng engine chấm, dự đoán và cohort đã thiết kế ở PRD v2.1.

---

## Document Control

| Field | Value |
|---|---|
| Document ID | PRD-2026-002 |
| Version | 3.0 |
| Status | Draft — chờ Founder duyệt |
| Owner | Founder (kiêm Sponsor / PO / BA / Developer) |
| Created | 2026-09-27 |
| Tên sản phẩm | VSTEP Lab (tên làm việc; thương hiệu chung `TBD-01`) |

### Quy ước

- **PHẢI** (Must) · **NÊN** (Should) · **CÓ THỂ** (Could). Priority theo MoSCoW: `M` · `S` · `C` · `W` (không làm trong release này).
- **`[Đề xuất]`** — con số do BA đề xuất, **chưa được Founder duyệt**; chốt trước mốc ghi ở §19.
- **`TBD-xx`** — quyết định còn mở, xem §19.
- **`[Cần kiểm chứng]`** — dữ kiện lấy từ nguồn thứ cấp, phải đối chiếu văn bản chính thức trước khi triển khai.

### Change Log

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 – 2.1 | 2026-09-27 | Founder + BA | Chuỗi PRD cho IELTS (xem `PRD_IELTS-Lab_v2.1_20260927.md`) |
| 3.0 | 2026-09-27 | BA (Claude) + Founder | Đổi thị trường sang VSTEP; chiến lược nhanh-rẻ; bộ nền kỹ thuật MIT; 2 tuần kiểm chứng đầu roadmap |

### Vì sao đổi sang VSTEP (tóm tắt quá trình ra quyết định)

| Thị trường đã xét | Lý do không chọn |
|---|---|
| IELTS (luyện thi chung) | ChatGPT voice miễn phí đã làm tốt luyện nói; Prep, STUDY4 mạnh về kho đề, thương hiệu, giá |
| IELTS One Skill Retake | Founder đánh giá chưa phổ biến ở Việt Nam |
| Cambridge YLE (trẻ em) | FLYER đã rất mạnh (600.000+ người dùng, 6.000+ đề, AI Speaking, 57.000–99.000đ/tháng) |
| HSK/HSKK, TOEIC S&W | Đã có nhiều app AI (HSK); nội dung ETS bảo vệ chặt (TOEIC); không khớp lợi thế của Founder |
| **VSTEP** ✅ | Nhu cầu **bắt buộc**; đối thủ **nhỏ, phân mảnh, giá cao**; khớp 3 lợi thế của Founder (giỏi tiếng Anh, ra sản phẩm nhanh-rẻ, seeding được trong cộng đồng public) |

---

## 1. Introduction

### 1.1 Purpose
Đặc tả yêu cầu business, chức năng và phi chức năng cho **VSTEP Lab — Release 1**: nền tảng luyện thi VSTEP bậc 3–5 (trọng tâm B1) chấm Writing/Speaking bằng AI, thi thử đủ 4 kỹ năng trên giao diện mô phỏng thi máy, dự đoán bậc, và cohort theo đợt thi.

### 1.2 Product Scope
Web app **mobile-first** (PWA), cho người cần chứng chỉ VSTEP — trước hết là **sinh viên cần B1 để tốt nghiệp**.

**Định vị:** *"Đậu B1 nhanh nhất, rẻ nhất — biết trước mình đủ bậc chưa."*
- **Rẻ hơn rõ rệt** so với đối thủ trả phí (VSTEPPRO 299.000–499.000đ/tháng).
- **"Đủ B1 chưa?"** — dự đoán bậc trước khi đóng lệ phí thi (1.200.000–1.800.000đ tùy trường), hiệu chỉnh dần bằng kết quả thi thật (kế thừa lợi thế A của PRD v2.x).
- **Cohort theo đợt thi** — nhóm ôn cùng ngày thi, nhắc học chủ động (kế thừa lợi thế C).

Mọi điểm và bậc do hệ thống đưa ra là **ước lượng**, không phải kết quả chính thức.

### 1.3 References
- Quyết định 729/QĐ-BGDĐT (11/03/2015) về định dạng đề thi VSTEP bậc 3–5.
- Thông tư 09/2026/TT-BGDĐT (hiệu lực 15/04/2026) về tổ chức thi đánh giá năng lực ngoại ngữ `[Cần kiểm chứng: đọc văn bản gốc]`.
- Dự thảo khung năng lực ngoại ngữ 7 bậc, dự kiến hiệu lực 01/01/2027 `[Cần kiểm chứng]`.
- `docs/architecture/REFERENCE_ielts-cd_analysis.md` — bài học kiến trúc (chỉ ý tưởng, không code).
- PRD IELTS Lab v2.1 — engine chấm, dự đoán, cohort, AI Gateway.

---

## 2. Business Context (BACCM)

### 2.1 Change
Xây mới nền tảng luyện thi VSTEP, dựng trên template mã nguồn mở MIT, tái sử dụng thiết kế engine từ PRD v2.1, ra thị trường trong khoảng 10 tuần sau 2 tuần kiểm chứng.

### 2.2 Need

| # | Nhu cầu | Bằng chứng |
|---|---|---|
| N1 | Sinh viên phải có B1 (bậc 3) để đạt chuẩn đầu ra, xét tốt nghiệp | Mục đích sử dụng VSTEP được các đơn vị tổ chức thi công bố `[Xác nhận]`; tỉ lệ trường yêu cầu `[Cần kiểm chứng]` |
| N2 | Học viên cao học, nghiên cứu sinh, giáo viên, một số vị trí cần B1–C1 | `[Cần kiểm chứng theo từng quy định hiện hành]` |
| N3 | Lệ phí thi 1.200.000–1.800.000đ/lần → trượt rất tốn kém; người học muốn biết đủ bậc chưa trước khi đăng ký | Lệ phí `[Xác nhận]`; nhu cầu dự đoán `[Giả thuyết]` |
| N4 | Writing và Speaking là hai kỹ năng khó tự luyện vì cần người chấm | `[Giả thuyết]` — kiểm chứng ở P0 |
| N5 | Các nền tảng trả phí hiện có giá cao so với túi tiền sinh viên | VSTEPPRO 299.000–499.000đ/tháng `[Công bố]`; mức sẵn sàng trả của sinh viên `[Giả thuyết]` |

### 2.3 Solution (high-level)
(1) Công cụ miễn phí để thu hút (chấm thử Writing, "Đủ B1 chưa?" rút gọn); (2) thi thử đủ 4 kỹ năng đúng định dạng VSTEP trên giao diện mô phỏng thi máy; (3) AI chấm Writing/Speaking theo tiêu chí; (4) quy đổi điểm 0–10 và bậc; (5) dự đoán bậc có trạng thái hiệu chỉnh; (6) Error Memory và làm lại; (7) cohort theo đợt thi và nhắc học; (8) gói giá rẻ, thanh toán VietQR.

### 2.4 Context

| Ràng buộc | Giá trị |
|---|---|
| Nhân lực | Founder solo — giỏi tiếng Anh, ra sản phẩm nhanh |
| Ngân sách | < 10.000.000đ phát triển; hạ tầng ~100.000đ/tháng (VPS 2 vCPU/4 GB/30 GB NVMe đã chọn) + object storage |
| Nền kỹ thuật | [`fastapi/full-stack-fastapi-template`](https://github.com/fastapi/full-stack-fastapi-template) (MIT): FastAPI + PostgreSQL + React/Vite + Docker Compose + Traefik + CI |
| Phân phối | Seeding trong cộng đồng public (nhóm Facebook/Zalo ôn thi VSTEP, nhóm sinh viên) — **không có cộng đồng riêng** |
| Pháp lý | Luật Bảo vệ dữ liệu cá nhân 2025; người dùng chủ yếu là người trưởng thành |
| Định dạng đề | Công khai theo Quyết định 729/QĐ-BGDĐT; nội dung đề phải tự soạn |

### 2.5 Định vị cạnh tranh

| Đối thủ | Có gì | Giá | Nhận xét |
|---|---|---|---|
| **VSTEPPRO** (vsteppro.vn) | AI chấm Writing/Speaking, 10.000+ câu hỏi, dự đoán CEFR ("95% accuracy"), khóa học có giảng viên; tự công bố 50.000+ học viên | Free (giới hạn) · Premium 299.000đ/tháng (chỉ AI Writing) · Pro 499.000đ/tháng | Đối thủ trả phí chính; **giá cao** |
| **luyenthivstep.vn** | Thi thử miễn phí, giao diện thi máy, chấm Writing/Speaking (giám khảo + AI), lịch thi, liên kết nhiều trường, khóa B1/B2 có cam kết đầu ra | Không công khai | Mạnh về nội dung SEO và liên kết trường |
| **VSTEPUP** (vstepup.vn) | Thi thử 4 kỹ năng miễn phí, AI chấm Writing/Speaking, Pro cho luyện từng kỹ năng; do một cá nhân vận hành | Freemium | **Cạnh tranh giá trực tiếp** — gần miễn phí |
| **Prep** | Nền tảng lớn; phòng luyện thi ảo AI cho IELTS; có nội dung VSTEP | IELTS PRO: 90 ngày 2.000.000đ (≈ 667.000đ/tháng), 180 ngày 3.400.000đ, 365 ngày 4.800.000đ (≈ 400.000đ/tháng) — theo trang giá ngày 27/09/2026 | Mặt bằng giá của "ông lớn" rất cao → khẳng định có chỗ cho sản phẩm giá thấp |
| ZIM, trung tâm | Bài blog, khóa học VSTEP | Khóa học đắt | Gián tiếp |
| ChatGPT | Chấm bài chung chung nếu biết cách prompt | Miễn phí | Không có giao diện thi, không quy đổi bậc VSTEP, không dự đoán |

**Mặt bằng giá thị trường:** các nền tảng trả phí có AI ở mức **~300.000–670.000đ/tháng** (VSTEPPRO, Prep). Gói tháng đề xuất 99.000đ rẻ hơn 3–6 lần. Lưu ý: ở phân khúc rẻ đã có VSTEPUP (VSTEP, freemium) và STUDY4 (IELTS), nên **giá rẻ là điều kiện cần, không đủ** — phải đi kèm chất lượng chấm đã kiểm chứng.

**Khác biệt phải giữ được:**
1. **Giá** thấp hơn rõ rệt VSTEPPRO, và **gói theo đợt thi** hợp với hành vi mua gần ngày thi.
2. **"Đủ B1 chưa?"** có khoảng sai số, công bố số liệu đo trên kết quả thật khi đủ dữ liệu — thay vì con số "95%" không rõ nguồn.
3. **Cohort theo đợt thi** + nhắc học chủ động.
4. **Chất lượng chấm được kiểm chứng** (eval set, model cố định) — để "rẻ" không đồng nghĩa "kém".

Nguồn: [VSTEPPRO](https://vsteppro.vn/) · [luyenthivstep.vn](https://luyenthivstep.vn/) · [VSTEPUP](https://www.vstepup.vn/)

---

## 3. Business Objectives & KPI

> Mọi ngưỡng là **`[Đề xuất]`**, duyệt trước tuần 3 (`TBD-02`).

| # | Objective | KPI | Deadline |
|---|---|---|---|
| O1 | Kiểm chứng nhu cầu trước khi xây (P0) | ≥ 6/10 sinh viên phỏng vấn nói Writing/Speaking là khó nhất **và** chấp nhận mức giá đề xuất; công cụ miễn phí thử nghiệm đạt ≥ 200 lượt dùng từ seeding | Tuần 2 |
| O2 | Chất lượng chấm đủ dùng | Chấm lại cùng bài trong eval set: chênh ≤ 0,5 điểm ở ≥ 90% bài; 👍 ≥ 70%; 0 trích dẫn không có trong bài/transcript | Tuần 9 |
| O3 | Tăng trưởng từ seeding | ≥ 1.000 người dùng đăng ký sau 4 tuần ra mắt; chi phí quảng cáo ≈ 0 | Tuần 14 |
| O4 | Sẵn sàng trả tiền | ≥ 50 người trả phí và chuyển đổi ≥ 4% người dùng hoạt động trong 30 ngày | Tuần 14 |
| O5 | Unit economics | Chi phí AI ≤ 30% doanh thu thuần; trung bình ≤ 1.500đ/bài Writing, ≤ 4.000đ/bài Speaking đủ 3 phần | Tuần 14 |
| O6 | Dữ liệu kết quả thật | ≥ 100 kết quả thi thật hợp lệ gửi về | Tháng 6 |
| O7 | Độ chính xác dự đoán bậc | Đúng bậc (B1/B2/C1/chưa đạt) ở ≥ 80% trường hợp trên ≥ 100 kết quả kiểm tra | Tháng 6–9 |

---

## 4. Stakeholders

| Role | Người/đơn vị | Trách nhiệm | Influence | Interest |
|---|---|---|---|---|
| Sponsor / PO / BA / Dev / người duyệt đề | Founder | Toàn bộ | High | High |
| Người dùng chính | Sinh viên năm 3–4 cần B1 | Dùng, trả phí, giới thiệu | Low | High |
| Người dùng mở rộng | Học viên cao học (B1/B2), giáo viên (B2/C1), người đi làm | Dùng, trả phí | Low | High |
| Admin nhóm cộng đồng | Nhóm Facebook/Zalo ôn thi VSTEP, nhóm sinh viên | Cho phép/không cho phép đăng bài | Med | Low |
| AI & speech provider | `TBD-04` | Chấm bài, STT, chấm phát âm, TTS | Med | Low |
| Payment provider | `TBD-05` (VietQR/ví điện tử) | Thu tiền | Med | Low |
| Cố vấn pháp lý | `TBD-10` | Privacy, điều khoản, quảng cáo | Med | Low |

---

## 5. Scope

### 5.1 Release plan

| Release | Nội dung | Gate | Thời điểm |
|---|---|---|---|
| **P0 — Kiểm chứng** | Dùng thử đối thủ, phỏng vấn 10 sinh viên, công cụ miễn phí thử nghiệm + seeding, kiểm tra provider | O1 đạt → vào R1; không đạt → xem lại giá/định vị | Tuần 1–2 |
| **R1 — MVP** | Thi thử 4 kỹ năng VSTEP, AI chấm Writing/Speaking, quy đổi bậc, dự đoán (chưa hiệu chỉnh), gói giá rẻ, công cụ miễn phí | P0 đạt | Tuần 3–10 (ra mắt tuần 10) |
| **R1.1 — Giữ chân** | Cohort theo đợt thi, nhắc học, Error Memory đầy đủ, thu thập kết quả thật | O3 đạt | Tuần 11–14 |
| R2 — Hiệu chỉnh & mở rộng | Công bố độ chính xác dự đoán; mở rộng B2/C1 chuyên sâu; app store (Capacitor) | O6, O7 | Tháng 4–9 |
| R3 — Khung 7 bậc | Cập nhật nếu Bộ GD&ĐT ban hành khung/định dạng mới | Văn bản chính thức | Theo quy định |
| R4 — Mở rộng IELTS giá rẻ | Dùng lại engine chấm/dự đoán cho IELTS với cùng chiến lược giá (Prep ≈ 400.000–667.000đ/tháng); tái sử dụng PRD IELTS v2.1 | O3, O4 đạt ở VSTEP; phân biệt được với STUDY4 | Sau R2 |

### 5.2 In-Scope (R1 + R1.1)
- ✅ Công cụ miễn phí: chấm thử Writing VSTEP; "Đủ B1 chưa?" rút gọn
- ✅ Thi thử đủ 4 kỹ năng đúng định dạng VSTEP bậc 3–5, chế độ thi và chế độ luyện
- ✅ AI chấm Writing (2 task) và Speaking (3 phần) theo tiêu chí
- ✅ Quy đổi điểm 0–10 từng kỹ năng, điểm trung bình, bậc
- ✅ Dự đoán "Đủ B1/B2/C1 chưa?" có trạng thái hiệu chỉnh; thu thập kết quả thật
- ✅ Error Memory, làm lại bài, đề tương đương
- ✅ Cohort theo đợt thi + nhắc học (R1.1)
- ✅ Gói giá, thanh toán VietQR (xác nhận thủ công giai đoạn đầu), AI Gateway, admin

### 5.3 Out-of-Scope
- ❌ Khóa học có giảng viên, chấm tay bởi giáo viên
- ❌ VSTEP bậc 2 (A2) — cân nhắc sau
- ❌ App store trong R1 (web/PWA trước; Capacitor ở R2)
- ❌ Crawl hoặc dùng lại đề của đơn vị tổ chức thi, sách có bản quyền, đề thi thật do thí sinh nhớ lại
- ❌ Seeding bằng tài khoản ảo, review giả
- ❌ Cam kết hoàn tiền theo kết quả (xem xét ở R2 khi có dữ liệu)
- ❌ Bán cho trường/doanh nghiệp (B2B)

---

## 6. Business Requirements

| ID | Description | Priority | Rationale | Source |
|---|---|---|---|---|
| BR-01 | Người học PHẢI làm được bài thi thử đủ 4 kỹ năng đúng định dạng VSTEP bậc 3–5 trên giao diện mô phỏng thi máy | M | Giá trị cốt lõi | N1, N2 |
| BR-02 | Writing và Speaking PHẢI được AI chấm theo tiêu chí, có nhận xét gắn bằng chứng, điểm 0–10 | M | Kỹ năng khó tự luyện nhất | N4, O2 |
| BR-03 | Hệ thống PHẢI quy đổi điểm từng kỹ năng, điểm trung bình và bậc theo quy tắc VSTEP | M | Người học cần biết đạt bậc nào | N1 |
| BR-04 | Hệ thống PHẢI dự đoán "đủ bậc mục tiêu chưa" kèm độ tin cậy và trạng thái hiệu chỉnh | M | Khác biệt định vị | N3, O7 |
| BR-05 | Hệ thống PHẢI có công cụ miễn phí dùng được không cần đăng ký để seeding | M | Kênh tăng trưởng duy nhất | O3 |
| BR-06 | Giá PHẢI thấp hơn rõ rệt đối thủ trả phí; có gói theo đợt thi | M | Lợi thế cạnh tranh chính | N5, O4 |
| BR-07 | Chi phí AI PHẢI được kiểm soát dưới trần | M | Giá thấp → biên mỏng | O5 |
| BR-08 | Dữ liệu người dùng CHỈ được gửi tới provider cam kết không huấn luyện trên dữ liệu | M | Privacy | §12 |
| BR-09 | Chấm PHẢI nhất quán giữa các lần (model/rubric cố định) | M | Dự đoán và tiến bộ phụ thuộc vào điều này | O2 |
| BR-10 | Tài khoản an toàn, dữ liệu cách ly; bài làm và ghi âm không bị mất | M | Cơ bản | — |
| BR-11 | Nội dung đề PHẢI tự soạn (AI + Founder duyệt), qua kiểm tra tự động | M | Pháp lý + chất lượng | §12 |
| BR-12 | Hệ thống PHẢI thu thập kết quả thi thật tự nguyện để hiệu chỉnh dự đoán | S | Nền cho độ chính xác dự đoán | O6 |
| BR-13 | Hệ thống NÊN ghi nhớ lỗi lặp lại và gợi ý làm lại/đề tương đương | S | Giữ chân | O4 |
| BR-14 | Hệ thống NÊN có cohort theo đợt thi và nhắc học chủ động | S | Lợi thế C, giữ chân | O4 |
| BR-15 | Người dùng NÊN chia sẻ được thẻ kết quả (opt-in) | S | Lan truyền trong nhóm | O3 |
| BR-16 | Hệ thống PHẢI cung cấp số liệu vận hành cho Founder (usage, chi phí, funnel, feedback) | M | Điều hành một mình | O3–O5 |
| BR-17 | Hệ thống CÓ THỂ có referral thưởng khi người được giới thiệu trả phí | C | Tăng trưởng | O3 |
| BR-18 | App iOS/Android trên store | W | R2 | — |
| BR-19 | Cam kết hoàn tiền theo kết quả | W | Cần dữ liệu (R2) | — |

**MoSCoW (in-scope):** Must 12 (71%) · Should 4 (24%) · Could 1 (6%) · Won't 2.
> ⚠️ Must chiếm 71%. Giảm rủi ro bằng: L/R chỉ có trắc nghiệm (engine đơn giản), dùng template MIT, và thứ tự cắt scope ở §18.

---

## 7. Overall Description

### 7.1 Persona

| Persona | Mô tả | Mục tiêu | Hành vi mua `[Giả thuyết]` |
|---|---|---|---|
| **P1 — Sinh viên cần B1** (chính) | Năm 3–4, trình độ A2–B1, học trên điện thoại | Đạt B1 một lần, tốn ít tiền và thời gian | Mua 4–8 tuần trước ngày thi; rất nhạy giá; tin lời khuyên trong nhóm |
| P2 — Học viên cao học | Đi làm, ít thời gian | B1 hoặc B2 | Sẵn sàng trả hơn P1 |
| P3 — Giáo viên / người đi làm | Cần B2/C1 | Đạt bậc cao | Chú trọng Writing/Speaking |

### 7.2 Nền tảng & thiết bị
- **Web/PWA mobile-first** (P1 học chủ yếu trên điện thoại); giao diện thi đầy đủ tối ưu cho laptop/tablet (thi thật trên máy tính).
- Speaking cần micro; hỗ trợ ghi âm trên Chrome/Safari di động và desktop.
- R2: đóng gói iOS/Android bằng Capacitor (MIT) khi cần có mặt trên store.

### 7.3 Ràng buộc thiết kế
- Frontend React + Vite (SPA) từ template; landing page SEO làm riêng dạng tĩnh.
- API key AI/payment chỉ ở backend. Audio và ảnh lưu trên object storage, không trên VPS.

### 7.4 Assumptions & Dependencies

| ID | Nội dung |
|---|---|
| A1 | Có AI provider (Lớp A) chấm Writing ≤ 1.500đ/bài và speech provider cho Speaking ≤ 4.000đ/bài đủ 3 phần `[Đề xuất]` — kiểm chứng tuần 1 |
| A2 | Sinh viên chấp nhận mức giá đề xuất (§13) — kiểm chứng ở P0 |
| A3 | Admin các nhóm cộng đồng cho phép chia sẻ công cụ miễn phí có giá trị — kiểm chứng ở P0 |
| A4 | Định dạng VSTEP bậc 3–5 không đổi trong 2026; theo dõi dự thảo khung 7 bậc từ 2027 |
| A5 | Founder đủ năng lực tiếng Anh để duyệt đề và kiểm tra chất lượng chấm |
| A6 | Người thi sẵn sàng gửi kết quả thi thật đổi lấy phần thưởng — kiểm chứng sau ra mắt |

---

## 8. Functional Requirements

### 8.1 F1 — Tài khoản & bảo mật (M)

| ID | Requirement | BR | AC |
|---|---|---|---|
| FR-001 | Đăng ký/đăng nhập bằng Google và email + mật khẩu (hash an toàn) | BR-10 | Theo template; khóa tạm 15 phút sau 5 lần sai liên tiếp |
| FR-002 | Reset mật khẩu bằng link hết hạn ≤ 30 phút, không tiết lộ email có tồn tại | BR-10 | Link quá hạn bị từ chối |
| FR-003 | Kiểm tra quyền sở hữu ở server cho mọi bài làm, ghi âm, giao dịch | BR-10 | Truy cập tài nguyên người khác → 404 |
| FR-004 | Xóa tài khoản và dữ liệu; thông báo rõ dữ liệu giữ lại theo nghĩa vụ pháp lý | BR-08, BR-10 | Sau xóa, bài làm/ghi âm không truy cập được |
| FR-005 | Thông báo xử lý dữ liệu (bài viết, **ghi âm**, gửi AI provider, lưu audio 30 ngày) và ghi nhận đồng ý trước lần nộp đầu | BR-08 | Chưa đồng ý → không gửi đi chấm |

### 8.2 F2 — Công cụ miễn phí để seeding (M)

| ID | Requirement | BR | AC |
|---|---|---|---|
| FR-010 | **Chấm thử Writing VSTEP:** dán bài Task 1 hoặc Task 2, nhận điểm ước lượng 0–10 + 3 lỗi chính + gợi ý sửa, **không cần đăng ký** | BR-05 | AC-F2-1 |
| FR-011 | **"Đủ B1 chưa?" rút gọn:** ~15 phút (một phần Nghe, một bài Đọc, 1 câu Speaking Part 1), trả về bậc ước lượng kèm cảnh báo "rút gọn, độ tin cậy thấp" | BR-04, BR-05 | AC-F2-2 |
| FR-012 | Giới hạn dùng miễn phí theo thiết bị/IP (VD: 2 lượt chấm Writing/ngày `[Đề xuất]`); vượt giới hạn → mời đăng ký | BR-07 | Lượt thứ 3 trong ngày hiển thị lời mời đăng ký |
| FR-013 | Kết quả công cụ có nút lưu (cần đăng ký) và nút chia sẻ thẻ kết quả (không lộ nội dung bài) | BR-05, BR-15 | Thẻ chia sẻ chỉ có điểm/bậc và tên nếu người dùng chọn |

- **AC-F2-1** — Given khách chưa đăng nhập, When dán bài Task 2 dài 260 từ và bấm "Chấm", Then nhận điểm ước lượng và 3 lỗi chính trong ≤ 60 giây, mỗi lỗi có trích đoạn khớp nguyên văn bài.
- **AC-F2-2** — Given khách làm xong bài rút gọn, When xem kết quả, Then thấy bậc ước lượng kèm nhãn "bài rút gọn — độ tin cậy thấp, làm bài thi thử đầy đủ để chính xác hơn".

### 8.3 F3 — Engine đề & giao diện thi (M)

| ID | Requirement | BR | AC |
|---|---|---|---|
| FR-020 | **Nghe:** 3 phần, 35 câu trắc nghiệm, ~40 phút; audio phát **một lần** trong chế độ thi, tải đủ trước khi bắt đầu | BR-01 | AC-F3-1 |
| FR-021 | **Đọc:** 4 bài đọc (tổng ~1.900–2.050 từ), 40 câu trắc nghiệm, 60 phút | BR-01 | Đồng hồ 60 phút, tự nộp khi hết giờ |
| FR-022 | **Viết:** 60 phút cho 2 task — Task 1 thư/email ~120 từ (1/3 điểm), Task 2 bài luận ~250 từ (2/3 điểm); đếm từ; cảnh báo (không chặn) khi thiếu từ | BR-01 | Đếm từ cập nhật khi gõ |
| FR-023 | **Nói:** 3 phần, ~12 phút — Part 1 giao tiếp xã hội (3–6 câu về 2 chủ đề), Part 2 thảo luận giải pháp (có 1 phút chuẩn bị), Part 3 phát triển chủ đề (kèm câu hỏi mở rộng); ghi âm từng phần, câu hỏi phát bằng giọng đọc | BR-01 | AC-F3-2 |
| FR-024 | Cấu trúc đề, thời gian, số câu lưu trong metadata có version (không hard-code UI) | BR-01 | Đổi định dạng không cần sửa code giao diện |
| FR-025 | **Chế độ thi** mô phỏng thi máy (đồng hồ, điều hướng câu, đánh dấu câu, xác nhận nộp); **chế độ luyện** cho tạm dừng, xem giải thích sau từng phần | BR-01 | Hai chế độ tách biệt |
| FR-026 | **Thi thử đầy đủ** Nghe → Đọc → Viết → Nói (~172 phút) hoặc từng kỹ năng; đồng hồ mỗi phần không reset khi tải lại trang | BR-01 | AC-F3-3 |
| FR-027 | Autosave local ≤ 5 giây và đồng bộ server; bản ghi âm lưu local đến khi server xác nhận; tiếp tục được sau gián đoạn | BR-10 | AC-F3-4 |
| FR-028 | Nộp lặp không tạo lượt chấm trùng, không trừ lượt hai lần | BR-07, BR-10 | 2 lần bấm nộp → 1 lượt chấm |
| FR-029 | Sau khi nộp: xem đáp án, giải thích, đánh dấu vị trí bằng chứng trong bài đọc/transcript | BR-01 | Bấm câu → highlight đoạn chứa đáp án |

- **AC-F3-1** — Given đang làm Nghe ở chế độ thi, When mất mạng giữa chừng, Then audio vẫn phát tiếp (đã tải trước) và câu trả lời lưu local.
- **AC-F3-2** — Given Part 2, When hết 1 phút chuẩn bị, Then ghi âm tự bắt đầu và tự dừng khi hết thời gian của phần.
- **AC-F3-3** — Given đang làm Đọc phút thứ 20, When tải lại trang, Then đồng hồ tiếp tục từ phút 20, không quay về 60.
- **AC-F3-4** — Given đã ghi xong Part 1 rồi mất mạng, When có mạng lại, Then bản ghi tự upload, không phải ghi lại.

### 8.4 F4 — AI chấm Writing (M)

| ID | Requirement | BR | AC |
|---|---|---|---|
| FR-030 | Chấm mỗi task theo **tiêu chí chấm Writing VSTEP** (bộ tiêu chí chính thức: `TBD-06`), điểm task và điểm Writing 0–10 theo trọng số 1/3 – 2/3 | BR-02, BR-03 | AC-F4-1 |
| FR-031 | Nhận xét quan trọng PHẢI trỏ tới câu trong bài, trích đoạn khớp nguyên văn | BR-02, BR-09 | Trích đoạn không khớp → loại và ghi log |
| FR-032 | Highlight lỗi trong bài, giải thích bằng tiếng Việt, gợi ý sửa | BR-02 | Bấm highlight mở giải thích |
| FR-033 | Bài quá ngắn, lạc đề, sai dạng (VD Task 1 không viết dạng thư) → nêu rõ và giới hạn điểm theo tiêu chí | BR-02, BR-09 | AC-F4-2 |
| FR-034 | Lưu model, provider, prompt version, rubric version cho mỗi lượt chấm | BR-09, BR-16 | Có trong DB và admin |
| FR-035 | Nhãn "Điểm ước lượng bởi AI — không phải kết quả chính thức" ở mọi vị trí có điểm | BR-02 | 100% vị trí có điểm |

- **AC-F4-1** — Given Task 1 được 6,0 và Task 2 được 5,0, When tính điểm Writing, Then điểm = 6,0 × 1/3 + 5,0 × 2/3 = 5,33 → làm tròn theo quy tắc §8.6.
- **AC-F4-2** — Given Task 1 là bài luận thay vì thư, When chấm, Then nhận xét nêu "sai dạng bài" và tiêu chí hoàn thành nhiệm vụ bị giới hạn.

### 8.5 F5 — AI chấm Speaking (M)

| ID | Requirement | BR | AC |
|---|---|---|---|
| FR-040 | Chấm theo **tiêu chí chấm Speaking VSTEP** (bộ tiêu chí chính thức: `TBD-06`; nguồn thứ cấp nêu: ngữ pháp, từ vựng, phát âm, độ trôi chảy & phát triển ý, mạch lạc), điểm 0–10 | BR-02 | AC-F5-1 |
| FR-041 | Hiển thị transcript từng phần; nhận xét trỏ tới đoạn transcript khớp nguyên văn; người dùng báo được "transcript sai" | BR-02, BR-09 | Báo sai được xác nhận → hoàn lượt |
| FR-042 | Phát âm CHỈ đánh giá từ phân tích audio (speech provider), không suy ra từ transcript; không có dữ liệu audio → ghi "chưa đánh giá được" | BR-02, BR-09 | AC-F5-2 |
| FR-043 | Độ trôi chảy dựa trên số đo từ audio (tốc độ nói, khoảng ngừng, từ đệm) | BR-02 | Số đo hiển thị trong report |
| FR-044 | Bấm từ phát âm sai → nghe lại đoạn của mình + nghe mẫu (TTS) | BR-02 | Hoạt động trên mobile |
| FR-045 | Trạng thái xử lý (đang upload/đang chấm/xong/lỗi); lỗi được thử lại, không trừ lượt, không phải ghi âm lại | BR-07, BR-10 | Lỗi provider → trạng thái "lỗi", lượt không bị trừ |

- **AC-F5-1** — Given bài nói đủ 3 phần hợp lệ, When chấm xong, Then có điểm Speaking 0–10 bước 0,5 và nhận xét theo từng tiêu chí trong ≤ 120 giây (p95).
- **AC-F5-2** — Given speech provider lỗi phần phân tích phát âm, When tạo report, Then tiêu chí phát âm ghi "chưa đánh giá được" và điểm tổng nêu rõ dựa trên các tiêu chí còn lại.

### 8.6 F6 — Quy đổi điểm & bậc (M)

**Business Rules** `[Cần kiểm chứng với quy định chính thức]`

| ID | Rule |
|---|---|
| RULE-01 | Mỗi kỹ năng chấm thang 0–10, làm tròn đến 0,5 |
| RULE-02 | Điểm trung bình = trung bình cộng 4 kỹ năng đã làm tròn, làm tròn đến 0,5: phần lẻ từ ,25 đến ,74 → ,5; từ ,75 trở lên → lên số nguyên kế tiếp; dưới ,25 → xuống số nguyên |
| RULE-03 | Quy đổi bậc: 4,0–5,5 → **Bậc 3 (B1)**; 6,0–8,0 → **Bậc 4 (B2)**; 8,5–10 → **Bậc 5 (C1)**; dưới 4,0 → **chưa đạt bậc 3** |
| RULE-04 | Nghe/Đọc: số câu đúng → điểm 0–10 theo **bảng quy đổi riêng của từng đề**; bảng khởi đầu là tỉ lệ tuyến tính `[Đề xuất]`, sau đó hiệu chỉnh bằng thống kê câu hỏi và kết quả thật |

| ID | Requirement | BR | AC |
|---|---|---|---|
| FR-050 | Tính điểm từng kỹ năng, điểm trung bình và bậc theo RULE-01 – RULE-04 | BR-03 | AC-F6-1 |
| FR-051 | Thiếu một kỹ năng → không hiển thị bậc tổng, chỉ hiển thị điểm kỹ năng đã có | BR-03 | Bậc tổng ẩn khi thiếu kỹ năng |
| FR-052 | Mỗi đề có bảng quy đổi Nghe/Đọc có version; đề mới gắn nhãn "chưa hiệu chỉnh" đến khi đủ ≥ 50 lượt làm `[Đề xuất]` | BR-03, BR-04 | Nhãn hiển thị cạnh điểm |

- **AC-F6-1** — Given Nghe 6,0, Nói 6,0, Đọc 6,5, Viết 5,5, When tính, Then trung bình 6,0 → Bậc 4 (B2).

### 8.7 F7 — Dự đoán "Đủ bậc chưa?" & kết quả thật (M/S)

| ID | Requirement | BR | AC |
|---|---|---|---|
| FR-060 | Người dùng chọn bậc mục tiêu (B1/B2/C1) và ngày thi dự kiến | BR-04 | Sửa được trong Settings |
| FR-061 | Dự đoán dựa trên ≥ 2 bài thi thử đầy đủ trong 21 ngày gần nhất `[Đề xuất]`, chỉ dùng đề đủ độ dài và **ưu tiên đề chưa làm** (làm lại đề cũ làm điểm bị thổi phồng) | BR-04, BR-09 | AC-F7-1 |
| FR-062 | Hiển thị: bậc dự đoán, xác suất đạt bậc mục tiêu dạng mức (Cao/Trung bình/Thấp), kỹ năng kéo điểm, và trạng thái "chưa được hiệu chỉnh bằng kết quả thật" cho đến khi đạt FR-066 | BR-04 | AC-F7-2 |
| FR-063 | Bài chấm bằng model dự phòng hoặc đề "chưa hiệu chỉnh" không dùng làm đầu vào dự đoán | BR-04, BR-09 | Bị loại khỏi tính toán |
| FR-064 | Người dùng gửi được kết quả thi thật (điểm 4 kỹ năng, ngày thi, đơn vị tổ chức, ảnh phiếu điểm để xác minh); ảnh tự xóa ≤ 7 ngày; consent riêng cho mục đích hiệu chỉnh; thưởng 1 tháng gói `[Đề xuất]` sau xác minh | BR-12 | AC-F7-3 |
| FR-065 | Chống gian lận: không nhận trùng số báo danh + ngày thi (lưu hash); chỉ tính khi có bài thi thử trong 28 ngày trước ngày thi; admin duyệt | BR-12 | Gửi trùng → từ chối và gắn cờ |
| FR-066 | Chỉ công bố độ chính xác dự đoán khi có ≥ 100 kết quả kiểm tra; câu công bố gồm số lượng, tỉ lệ đúng bậc, ngày cập nhật | BR-04, BR-12 | Nút công bố bị khóa khi chưa đủ |

- **AC-F7-1** — Given người dùng làm lại đề #3 lần thứ hai, When tính dự đoán, Then lượt làm lại không được dùng nếu còn đề đầy đủ chưa làm.
- **AC-F7-2** — Given chưa đủ dữ liệu hiệu chỉnh, When hiển thị dự đoán, Then có nhãn "chưa được hiệu chỉnh bằng kết quả thật" và không có con số độ chính xác.
- **AC-F7-3** — Given kết quả được xác minh lúc T, When đến T + 7 ngày, Then ảnh phiếu điểm bị xóa, chỉ còn các con số.

### 8.8 F8 — Error Memory & làm lại (S)

| ID | Requirement | BR | AC |
|---|---|---|---|
| FR-070 | Gắn mỗi lỗi Writing/Speaking với error tag (taxonomy có version, gồm nhóm lỗi thường gặp của người Việt) | BR-13 | Lỗi có tag trong DB |
| FR-071 | Đánh dấu lỗi lặp lại khi cùng tag xuất hiện ở ≥ 2 bài | BR-13 | Dashboard hiện top 3 lỗi lặp lại |
| FR-072 | Viết lại bài Writing / nói lại phần Speaking; so sánh lỗi đã sửa / chưa sửa / lỗi mới | BR-13 | Report so sánh 3 trạng thái |
| FR-073 | Gợi ý đề tương đương chưa làm nhắm vào lỗi lặp lại | BR-13 | Có ≥ 1 gợi ý khi còn đề |

### 8.9 F9 — Cohort theo đợt thi & nhắc học (S)

| ID | Requirement | BR | AC |
|---|---|---|---|
| FR-080 | Admin tạo cohort theo **đợt thi** (đơn vị tổ chức + ngày thi), bắt đầu 4–6 tuần trước ngày thi `[Đề xuất]` | BR-14 | Trang Cohort trong admin |
| FR-081 | Lộ trình: 1 nhiệm vụ/ngày ≤ 20 phút + 1 bài thi thử đầy đủ mỗi tuần | BR-14 | Hiển thị % hoàn thành |
| FR-082 | Bảng tiến độ nhóm ẩn danh mặc định; hiện tên khi opt-in | BR-14 | Mặc định ẩn danh |
| FR-083 | Nhắc học qua email (mặc định) hoặc Zalo (`TBD-08`); tối đa 1 tin/ngày; không gửi 22:00–07:00; tắt bằng 1 chạm | BR-14 | Không có tin trong giờ yên lặng |
| FR-084 | Sau ngày thi, nhắc gửi kết quả thật (F7) | BR-12, BR-14 | Tối đa 2 lần nhắc |

### 8.10 F10 — Quy trình soạn đề (M)

| ID | Requirement | BR | AC |
|---|---|---|---|
| FR-090 | Đề đi qua: AI soạn nháp → **kiểm tra tự động** → Founder duyệt → pilot → xuất bản; lưu provenance | BR-11 | Trạng thái draft/reviewed/pilot/published |
| FR-091 | Kiểm tra tự động Nghe/Đọc (trắc nghiệm): mỗi câu có **đúng một** đáp án; đáp án đúng có căn cứ trong bài đọc/transcript; phương án nhiễu không trùng nghĩa với đáp án; số câu và số từ bài đọc đúng định dạng | BR-11 | AC-F10-1 |
| FR-092 | **Tự kiểm tra:** chấm "bài làm hoàn hảo" dựng từ đáp án phải đạt tuyệt đối | BR-11 | Không đạt → chặn xuất bản |
| FR-093 | Audio Nghe tạo bằng TTS có quyền dùng thương mại (`TBD-07`), nhiều giọng; Founder nghe lại toàn bộ trước khi xuất bản | BR-11 | Checklist duyệt audio bắt buộc |
| FR-094 | Báo lỗi từng câu; sửa đáp án → **chấm lại một chiều** (chỉ sai → đúng, không trừ điểm người đã xem kết quả) | BR-11 | AC-F10-2 |
| FR-095 | Công cụ import từ chối đề không có provenance hợp lệ; không crawl, không dùng đề có bản quyền hay đề thi thật | BR-11 | Import thiếu provenance bị từ chối |
| FR-096 | Ngân hàng đề trước ra mắt: ≥ 5 bộ đề đầy đủ 4 kỹ năng + ≥ 20 đề Writing mỗi task + ≥ 20 bộ câu hỏi Speaking `[Đề xuất]` | BR-01 | Đếm trong admin |

- **AC-F10-1** — Given AI soạn câu Đọc có hai phương án cùng đúng, When chạy kiểm tra tự động, Then đề bị giữ ở draft kèm lỗi cụ thể.
- **AC-F10-2** — Given câu 12 được sửa đáp án từ B sang C, When chấm lại, Then người đã chọn C được cộng điểm, người đã chọn B **không bị trừ**.

### 8.11 F11 — Gói giá & thanh toán (M)

**Business Rules**

| ID | Rule `[Đề xuất]` |
|---|---|
| RULE-10 | **Free:** công cụ miễn phí (F2), 1 bài thi thử đầy đủ/tháng, 2 lượt chấm Writing/ngày |
| RULE-11 | **Gói "Đến ngày thi":** 199.000đ, dùng đến ngày thi + 7 ngày (tối đa 90 ngày); 30 lượt chấm Writing + 15 bài Speaking đủ 3 phần |
| RULE-12 | **Gói tháng:** 99.000đ/tháng; 20 lượt Writing + 10 bài Speaking |
| RULE-13 | Nghe/Đọc không tốn lượt |
| RULE-14 | Lỗi xử lý, nộp trùng, mở lại report: không trừ lượt |
| RULE-15 | Chỉ kích hoạt gói sau khi thanh toán được xác minh (webhook có chữ ký, hoặc admin xác nhận chuyển khoản thủ công có audit log giai đoạn đầu) |

**Cơ sở giá:** VSTEPPRO 299.000–499.000đ/tháng → gói tháng rẻ hơn ≥ 3 lần. Trường hợp xấu nhất gói "Đến ngày thi": 30 × 1.500đ + 15 × 4.000đ = 105.000đ chi phí AI trên ~193.000đ doanh thu thuần (~54%); mức dùng trung bình dự kiến 30–40% → ~20% doanh thu, đạt O5.

| ID | Requirement | BR | AC |
|---|---|---|---|
| FR-100 | Trang giá hiển thị gói, quyền lợi, thời hạn, điều kiện hoàn tiền trước khi thanh toán | BR-06 | Đủ 4 thông tin |
| FR-101 | Thanh toán VietQR qua payment adapter; mã đơn duy nhất; xử lý idempotent | BR-06 | Webhook lặp không cộng lượt hai lần |
| FR-102 | Giai đoạn đầu: admin xác nhận chuyển khoản thủ công, ghi audit log | BR-06 | Log có admin, thời gian, mã đơn, số tiền |
| FR-103 | Trang "Gói của tôi": gói, hạn, lượt còn lại, lịch sử giao dịch | BR-06 | Hiển thị đúng |
| FR-104 | Không tự gia hạn trong R1 | BR-06 | Không có giao dịch tự động |

### 8.12 F12 — AI Gateway (M)

Kế thừa thiết kế PRD v2.1 §8.9, rút gọn:

| ID | Requirement | BR | AC |
|---|---|---|---|
| FR-110 | Phân loại dữ liệu: **Lớp A** (bài làm, ghi âm) chỉ tới provider trả phí cam kết không huấn luyện; **Lớp B/C** (soạn đề, dev) được dùng gói miễn phí hợp lệ — mỗi provider một tài khoản | BR-08 | Request Lớp A tới provider không được phép → bị chặn |
| FR-111 | Mỗi rubric version gắn **một model chấm cố định**; đổi model = rubric mới + chạy lại eval set | BR-09 | Không đổi model ngầm |
| FR-112 | Circuit breaker theo provider (mở sau 3 lỗi liên tiếp/60 giây, thử lại sau 60 giây `[Đề xuất]`); fallback ghi nhận trong report | BR-07, BR-10 | Fallback được ghi nhận |
| FR-113 | Prompt caching cho phần rubric cố định; chống chấm trùng theo hash nội dung | BR-07 | Nộp lại y hệt → trả report cũ, không trừ lượt |
| FR-114 | Trần chi phí tháng; cảnh báo 50/80/100% qua email | BR-07 | Email khi vượt 80% |
| FR-115 | Validate output theo JSON schema và khoảng điểm hợp lệ | BR-09 | Sai schema → retry ≤ 2 lần rồi báo lỗi |
| FR-116 | Log provider, model, token, chi phí, latency, trạng thái — **không** log toàn văn bài làm | BR-08, BR-16 | Log không chứa nội dung bài |

### 8.13 F13 — Admin & số liệu (M)

| ID | Requirement | BR | AC |
|---|---|---|---|
| FR-120 | Quản lý người dùng, gói, lượt | BR-16 | Trang Users |
| FR-121 | AI usage & chi phí theo ngày/provider/model, tỉ lệ lỗi, latency | BR-16, BR-07 | Trang AI Usage |
| FR-122 | **Funnel seeding:** nguồn truy cập (mã nhóm/UTM) → dùng công cụ miễn phí → đăng ký → thi thử → trả phí | BR-16, BR-05 | Funnel theo từng nguồn |
| FR-123 | Hộp feedback & báo lỗi (chấm, đề, transcript, thanh toán) | BR-16 | Lọc theo loại |
| FR-124 | Duyệt đề, duyệt kết quả thật, xác nhận thanh toán; audit log mọi hành động admin | BR-16, BR-10 | Có actor, action, thời gian |

### 8.14 F14 — Lan truyền (S/C)

| ID | Requirement | BR | Priority |
|---|---|---|---|
| FR-130 | Thẻ kết quả chia sẻ (opt-in): điểm/bậc, không lộ nội dung bài; link có mã nguồn để đo funnel | BR-15 | S |
| FR-131 | Referral: cả hai bên nhận thêm lượt khi người được giới thiệu **trả phí** | BR-17 | C |

---

## 9. Non-Functional Requirements

| ID | Nhóm | Requirement | Target |
|---|---|---|---|
| NFR-P01 | Performance | Report Writing | p95 ≤ 60 giây |
| NFR-P02 | Performance | Report Speaking đủ 3 phần | p95 ≤ 120 giây `[Đề xuất]` |
| NFR-P03 | Performance | Tải trang trên 4G, điện thoại tầm trung | LCP ≤ 2,5 giây |
| NFR-P04 | Performance | API không liên quan AI | p95 ≤ 500 ms |
| NFR-R01 | Reliability | Uptime tháng | ≥ 99% `[Đề xuất]` |
| NFR-R02 | Reliability | Chấm thành công sau retry/fallback | ≥ 98% |
| NFR-R03 | Reliability | Backup DB hằng ngày ra storage ngoài VPS; diễn tập khôi phục hằng tháng | RPO ≤ 24h, RTO ≤ 8h |
| NFR-R04 | Reliability | Mất bài/bản ghi do lỗi hệ thống | 0 trường hợp |
| NFR-S01 | Security | HTTPS, hash mật khẩu, phân quyền ở server, rate limit nộp bài ≤ 10/phút/người | Bắt buộc |
| NFR-S02 | Security | Audio và ảnh phiếu điểm trên storage riêng tư, URL ký hạn ≤ 15 phút; audio tự xóa sau 30 ngày | Bắt buộc |
| NFR-S03 | Security | Secrets chỉ ở backend; CI quét secret | Bắt buộc |
| NFR-U01 | Usability | Dùng công cụ miễn phí từ lúc mở link đến lúc có kết quả | ≤ 3 thao tác, không cần đăng ký |
| NFR-U02 | Usability | Mobile-first; giao diện thi đầy đủ dùng tốt từ 360px, tối ưu cho ≥ 1024px | Kiểm tra trên 2 điện thoại + 1 laptop |
| NFR-U03 | Usability | Nhãn "ước lượng" ở 100% vị trí có điểm/bậc; nhãn trạng thái hiệu chỉnh ở 100% vị trí có dự đoán | Bắt buộc |
| NFR-M01 | Maintainability | Test tự động cho: auth, autosave/nộp idempotent, quy đổi điểm/bậc (RULE-01–04), lượt/gói, webhook, validate output AI, kiểm tra đề | 100% có test |
| NFR-C01 | Cost | Chi phí AI/bài Writing; /bài Speaking đủ 3 phần | ≤ 1.500đ; ≤ 4.000đ `[Đề xuất]` |
| NFR-C02 | Cost | Hạ tầng tháng | ~100.000đ VPS + storage (đã chọn gói 2 vCPU/4 GB/30 GB) |

---

## 10. External Interfaces

| System | Mục đích | Ghi chú |
|---|---|---|
| Google OAuth | Đăng nhập | — |
| AI provider(s) | Chấm Writing/Speaking (Lớp A), soạn đề (Lớp B) | `TBD-04` |
| Speech provider(s) | STT, chấm phát âm (Lớp A); TTS audio Nghe và câu hỏi Nói (Lớp B, cache) | `TBD-04`, `TBD-07` |
| Payment | VietQR/ví điện tử, webhook có chữ ký | `TBD-05` |
| Email / Zalo | Nhắc học, xác thực, cảnh báo chi phí | `TBD-08` |
| Object storage | Audio, ảnh phiếu điểm, audio TTS | S3-compatible, lifecycle xóa 30 ngày |

---

## 11. Data Requirements

### 11.1 Data model (ý tưởng; triển khai mới trên template)

| Entity | Trường chính |
|---|---|
| `user`, `session` | Theo template; thêm bậc mục tiêu, ngày thi dự kiến |
| `test_form` | version, trạng thái, provenance, cờ AI-generated, cấu trúc phần/câu (metadata), bảng quy đổi Nghe/Đọc có version |
| `item` | kỹ năng, phần, nội dung, phương án, đáp án đúng, giải thích, vị trí bằng chứng, thống kê (tỉ lệ đúng, độ phân biệt) |
| `attempt` | user, đề, chế độ, trạng thái, câu trả lời, hạn chót từng phần, điểm từng kỹ năng |
| `writing_submission`, `speaking_recording` | nội dung/đường dẫn audio, transcript, số đo audio, hạn xóa audio |
| `assessment` | điểm tiêu chí, nhận xét + bằng chứng, model/provider/prompt/rubric version, cờ fallback |
| `error_tag`, `error_occurrence` | taxonomy có version; lỗi theo người dùng, bài nguồn |
| `prediction` | bậc dự đoán, mức xác suất, đầu vào, calibration version |
| `official_result` | điểm 4 kỹ năng, ngày thi, đơn vị, hash số báo danh, trạng thái xác minh, consent hiệu chỉnh |
| `cohort`, `cohort_member` | đợt thi, lịch, % hoàn thành |
| `plan`, `entitlement`, `payment_order`, `payment_event` | gói, lượt, hạn, giao dịch |
| `ai_request_log`, `free_tool_usage` | chi phí, latency; lượt dùng công cụ miễn phí theo thiết bị/IP, nguồn seeding |

### 11.2 Retention

| Dữ liệu | Thời hạn |
|---|---|
| Bài làm, report, Error Memory | Đến khi người dùng xóa |
| Audio ghi âm | 30 ngày, tự xóa |
| Ảnh phiếu điểm | ≤ 7 ngày sau xác minh/từ chối |
| Bài dán vào công cụ miễn phí (khách chưa đăng ký) | ≤ 24 giờ `[Đề xuất]`, rồi xóa |
| Log vận hành AI | 90 ngày `[Đề xuất]` |

---

## 12. Compliance & Legal

| Hạng mục | Ghi chú |
|---|---|
| Luật Bảo vệ dữ liệu cá nhân 2025 | Thông báo & đồng ý, xóa dữ liệu, chuyển dữ liệu tới AI provider nước ngoài — **rà soát pháp lý `TBD-10`** |
| Giọng nói | Đồng ý riêng trước khi ghi âm; không dùng để nhận dạng danh tính |
| Nội dung đề | Tự soạn; định dạng đề công khai nhưng **không** sao chép đề mẫu/đề thật của đơn vị tổ chức thi |
| Tên gọi & thương hiệu | Không gây hiểu nhầm là sản phẩm của Bộ GD&ĐT hay đơn vị tổ chức thi; ghi rõ "luyện thi theo định dạng VSTEP" |
| Quảng cáo | Không tuyên bố độ chính xác chưa đo được; mọi con số công bố kèm số lượng mẫu và ngày |
| Seeding | Đăng bằng danh tính thật, theo luật từng nhóm; không tài khoản ảo, không review giả |
| Thanh toán | Không lưu dữ liệu thẻ |

---

## 13. Go-to-Market (seeding cộng đồng public)

| Bước | Hành động | Đo lường |
|---|---|---|
| 1 | Liệt kê 15–20 nhóm Facebook/Zalo ôn thi VSTEP và nhóm sinh viên các trường có yêu cầu B1; đọc luật từng nhóm | Danh sách + luật |
| 2 | Đóng góp nội dung trước: lịch thi, mẹo, chữa bài mẫu | Tương tác |
| 3 | Chia sẻ **công cụ miễn phí** (FR-010, FR-011) với link có mã nhóm | Funnel theo nhóm (FR-122) |
| 4 | Thẻ kết quả chia sẻ (FR-130) tạo lan truyền tự nhiên | Lượt truy cập từ thẻ |
| 5 | Cohort theo đợt thi của từng trường | Số người vào cohort |

---

## 14. Risks & Mitigations

| ID | Risk | Prob. | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Chiến tranh giá (VSTEPUP gần miễn phí) | High | High | Cạnh tranh bằng chất lượng chấm đã kiểm chứng + dự đoán + cohort, không chỉ giá |
| R2 | Đối thủ hạ giá khi thấy mình | Med | Med | Chi phí vận hành thấp (1 người, VPS rẻ); gói theo đợt thi |
| R3 | Chất lượng chấm AI kém làm mất uy tín | Med | High | Eval set, model cố định, nhãn ước lượng, báo lỗi |
| R4 | Admin nhóm cấm đăng | Med | High | Đóng góp giá trị trước; công cụ miễn phí thật sự hữu ích; nhiều nhóm |
| R5 | Định dạng/khung thay đổi (dự thảo 7 bậc từ 2027) | Med | Med | Định dạng trong metadata (FR-024); theo dõi văn bản chính thức |
| R6 | Sinh viên chỉ mua sát ngày thi rồi rời đi | High | Med | Gói "Đến ngày thi" đúng hành vi; referral; mở rộng B2/C1 |
| R7 | Chi phí Speaking vượt ngân sách | Med | High | Kiểm tra A1 tuần 1; giới hạn lượt; cache TTS |
| R8 | Đề AI soạn sai đáp án | Med | High | Kiểm tra tự động + Founder duyệt + pilot + chấm lại một chiều |
| R9 | Founder quá tải (dev + soạn đề + seeding) | High | High | L/R chỉ trắc nghiệm; template MIT; thứ tự cắt scope §18 |
| R10 | Tiêu chí chấm chính thức khác nguồn thứ cấp | Med | Med | Đối chiếu văn bản chính thức (`TBD-06`) trước tuần 3 |

---

## 15. Kế thừa từ PRD IELTS v2.1 và từ phân tích tham khảo

| Thành phần | Nguồn | Thay đổi cho VSTEP |
|---|---|---|
| AI Gateway (phân loại dữ liệu, model cố định, caching, circuit breaker, trần chi phí) | PRD v2.1 §8.9 | Giữ nguyên, rút gọn |
| Dự đoán + hiệu chỉnh bằng kết quả thật | PRD v2.1 F16–F18 | Dự đoán **bậc** thay cho band; ngưỡng công bố thấp hơn |
| Cohort + nhắc học | PRD v2.1 F19–F20 | Theo **đợt thi của từng đơn vị** |
| Kiểm tra đề, tự kiểm tra, chấm lại một chiều | `REFERENCE_ielts-cd_analysis.md` §3 | Đơn giản hơn nhiều vì Nghe/Đọc chỉ trắc nghiệm |
| Full mock chỉ dùng đề đủ độ dài, ưu tiên đề chưa làm | Như trên §3.4 | Áp dụng cho dự đoán bậc (FR-061) |
| Hạ tầng auth/user/admin/Docker/CI | `fastapi/full-stack-fastapi-template` (MIT) | Dùng làm nền |

---

## 16. Kiến trúc & triển khai (tóm tắt)

- **Nền:** `fastapi/full-stack-fastapi-template` (MIT) — FastAPI, PostgreSQL, SQLModel, Alembic, React + Vite + Tailwind + shadcn/ui, Docker Compose, Traefik, CI/CD.
- **Thêm:** worker xử lý job chấm (hàng đợi + Redis), object storage cho audio, TTS cache.
- **Hạ tầng:** 1 VPS 2 vCPU / 4 GB / 30 GB NVMe (~100.000đ/tháng); build image trên CI, không build trên VPS; audio phát từ object storage.
- **Mobile:** PWA ở R1; Capacitor (MIT) + plugin ghi âm (MIT) ở R2.

---

## 17. Glossary

| Term | Định nghĩa |
|---|---|
| VSTEP | Bài thi đánh giá năng lực tiếng Anh bậc 3–5 theo Khung năng lực ngoại ngữ 6 bậc dùng cho Việt Nam |
| Bậc 3 / 4 / 5 | Tương ứng B1 / B2 / C1 |
| Đợt thi | Một ngày thi của một đơn vị được cấp phép tổ chức |
| Lượt chấm | Một lần chấm AI thành công (Writing hoặc Speaking) |
| Bảng quy đổi | Ánh xạ số câu đúng Nghe/Đọc sang điểm 0–10, riêng từng đề |
| Hiệu chỉnh | Điều chỉnh dự đoán bằng kết quả thi thật |
| Seeding | Chia sẻ sản phẩm vào cộng đồng có sẵn để thu hút người dùng |

---

## 18. Roadmap

| Tuần | Milestone | Deliverables | Pass criteria |
|---|---|---|---|
| **1–2** | **P0 — Kiểm chứng** | Dùng thử VSTEPPRO, VSTEPUP, luyenthivstep (ghi điểm mạnh/yếu); phỏng vấn 10 sinh viên cần B1; bản thử công cụ "Chấm thử Writing" (đơn giản) đăng vào 3–5 nhóm; kiểm tra A1 (chi phí AI/speech); đối chiếu định dạng và tiêu chí chính thức (`TBD-06`) | **O1 đạt** → R1; không đạt → xem lại giá/định vị |
| 3–4 | M1 — Nền + Writing | Dựng template; F1; F4 (Writing) + eval set Writing; F2 bản chính thức (FR-010) | O2 đạt trên eval set Writing |
| 5–6 | M2 — Speaking | F5; ghi âm mobile; eval set Speaking | Report Speaking ≤ 120 giây (p95) |
| 7–8 | M3 — Nghe/Đọc + đề | F3 (engine trắc nghiệm, giao diện thi); F10 (soạn đề, kiểm tra tự động); sản xuất ≥ 5 bộ đề | 5 bộ đề qua kiểm tra |
| 9 | M4 — Bậc, dự đoán, thanh toán | F6, F7 (FR-060–063), F11 (xác nhận thủ công), F13, FR-011 | Thanh toán thử thành công |
| **10** | **M5 — Ra mắt** | Landing page; seeding theo §13 | Người trả phí đầu tiên |
| 11–14 | R1.1 — Giữ chân | F8, F9, FR-064–066, F14, thêm đề | Đo O3–O5 |
| Tháng 4–9 | R2 | Công bố độ chính xác (khi đủ dữ liệu); Capacitor; B2/C1 chuyên sâu | O6, O7 |

**Thứ tự cắt scope nếu trễ:** FR-131 referral → FR-082 bảng tiến độ nhóm → F8 so sánh bài làm lại → Zalo (giữ email) → giảm số bộ đề trước ra mắt xuống 3 → FR-011 "Đủ B1 chưa?" rút gọn (giữ FR-010).

**Không cắt:** công cụ chấm thử Writing (kênh tăng trưởng duy nhất), AI chấm Writing/Speaking, engine thi 4 kỹ năng, quy đổi bậc, nhãn ước lượng, kiểm tra đề tự động, xác minh thanh toán, bảo mật & dữ liệu.

---

## 19. Open Issues (TBD)

| ID | Nội dung | Hạn |
|---|---|---|
| TBD-01 | Tên thương hiệu, domain | Tuần 9 |
| TBD-02 | Duyệt các ngưỡng `[Đề xuất]` (KPI, giá, lượt, số đề) | Tuần 3 |
| TBD-03 | Danh sách nhóm cộng đồng mục tiêu và luật đăng bài | Tuần 1 |
| TBD-04 | AI provider (Writing) và speech provider (STT, phát âm, TTS) | Tuần 1 |
| TBD-05 | Payment (VietQR), hình thức pháp lý để thu tiền | Tuần 2 |
| TBD-06 | **Tiêu chí chấm Writing/Speaking chính thức**, quy tắc làm tròn và quy đổi bậc — đối chiếu Quyết định 729 và Thông tư 09/2026 | Tuần 2 |
| TBD-07 | TTS có quyền dùng thương mại | Tuần 3 |
| TBD-08 | Kênh nhắc học Zalo OA (chính sách, chi phí) | Tuần 11 |
| TBD-09 | Chính sách hoàn tiền | Tuần 9 |
| TBD-10 | Rà soát pháp lý: dữ liệu cá nhân, ghi âm, chuyển dữ liệu ra nước ngoài, điều khoản, quảng cáo | Tuần 9 |

---

## 20. Traceability Matrix

| BR | FR | NFR | Test Case | Status |
|---|---|---|---|---|
| BR-01 | FR-020–FR-029, FR-096 | NFR-P03, NFR-U02 | TC-001 – TC-015 | Todo |
| BR-02 | FR-030–FR-033, FR-035, FR-040–FR-045 | NFR-P01, NFR-P02, NFR-U03 | TC-020 – TC-035 | Todo |
| BR-03 | FR-030, FR-050–FR-052 | NFR-M01 | TC-040 – TC-046 | Todo |
| BR-04 | FR-011, FR-052, FR-060–FR-063, FR-066 | NFR-U03 | TC-050 – TC-058 | Todo |
| BR-05 | FR-010–FR-013, FR-122 | NFR-U01 | TC-060 – TC-065 | Todo |
| BR-06 | FR-100–FR-104 | — | TC-070 – TC-075 | Todo |
| BR-07 | FR-012, FR-028, FR-045, FR-112–FR-114, FR-121 | NFR-C01, NFR-C02 | TC-080 – TC-085 | Todo |
| BR-08 | FR-004, FR-005, FR-110, FR-116 | NFR-S02, NFR-S03 | TC-090 – TC-094 | Todo |
| BR-09 | FR-031, FR-033, FR-034, FR-041, FR-042, FR-061, FR-063, FR-111, FR-115 | NFR-M01 | TC-100 – TC-108 | Todo |
| BR-10 | FR-001–FR-005, FR-027, FR-028, FR-045, FR-112, FR-124 | NFR-R01–NFR-R04, NFR-S01 | TC-110 – TC-120 | Todo |
| BR-11 | FR-090–FR-095 | NFR-M01 | TC-125 – TC-132 | Todo |
| BR-12 | FR-064, FR-065, FR-066, FR-084 | NFR-S02 | TC-135 – TC-140 | Todo |
| BR-13 | FR-070–FR-073 | — | TC-145 – TC-149 | Todo |
| BR-14 | FR-080–FR-084 | — | TC-150 – TC-155 | Todo |
| BR-15 | FR-013, FR-130 | — | TC-160 – TC-161 | Todo |
| BR-16 | FR-034, FR-116, FR-120–FR-124 | — | TC-165 – TC-170 | Todo |
| BR-17 | FR-131 | — | TC-175 | Todo |

**Kiểm tra orphan:** mọi FR trace về ≥ 1 BR; mọi BR in-scope có ≥ 1 FR. BR-18, BR-19 là Won't.

---

## 21. Approval

| Role | Name | Date |
|---|---|---|
| Sponsor / PO | Founder | |
| BA | Claude (hỗ trợ soạn thảo) | 2026-09-27 |

---

## Nguồn

- [Cấu trúc đề thi VSTEP bậc 3–5 — Đại học Ngoại thương](https://vstep.ftu.edu.vn/ky-thi-vstep/cau-truc-de-thi-vstep/cau-truc-de-thi-bac-3-5-cua-bai-thi-danh-gia-nang-luc-ngoai-ngu-tieng-anh-tu-bac-3-den-bac-5-theo-khung-nlnn-6-bac-dung-cho-viet-nam/) · [Định dạng đề thi VSTEP.3-5 — ULIS-VNU](https://vstep.vnu.edu.vn/dinh-dang-de-thi-vstep-3-5/) · [Quyết định áp dụng đề thi bậc 3–5](https://vstep.edu.vn/quyet-dinh-ap-dung-de-thi-danh-gia-nang-luc-tieng-anh-bac-3-5)
- [Thang điểm VSTEP — ZIM](https://zim.vn/thang-diem-vstep) · [Thang điểm VSTEP — luyenthivstep.vn](https://luyenthivstep.vn/kien-thuc-vstep/thang-diem-vstep)
- [Lệ phí thi VSTEP 2026 — ELSA](https://vn.elsaspeak.com/le-phi-thi-vstep/) · [Kỳ thi VSTEP là gì — ZIM](https://zim.vn/vstep-la-gi) · [Danh sách 38 đơn vị tổ chức thi VSTEP](https://vstepeasy.edu.vn/thi-vstep)
- [Phân tích Thông tư 09/2026/TT-BGDĐT — luyenthivstep.vn](https://luyenthivstep.vn/cam-nang-vstep/thong-tu-09-2026-tt-bgddt-quy-dinh-to-chuc-thi-nang-luc-ngoai-ngu-vstep-va-tieng-viet)
- [Cấu trúc Speaking VSTEP — luyenthivstep.vn](https://luyenthivstep.vn/cam-nang-vstep/cau-truc-speaking-vstep-b1-b2-c1) · [VSTEP Speaking — Prep](https://prepedu.com/vi/blog/bai-thi-vstep-speaking)
- [VSTEPPRO](https://vsteppro.vn/) · [luyenthivstep.vn](https://luyenthivstep.vn/) · [VSTEPUP](https://www.vstepup.vn/)
- [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) · [Capacitor](https://github.com/ionic-team/capacitor)
