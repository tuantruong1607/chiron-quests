# VSTEP Lab — Kiến trúc tổng thể & lát cắt đầu tiên "Chấm thử Writing"

| Field | Value |
|---|---|
| Ngày | 2026-09-27 |
| Trạng thái | Chờ Founder duyệt spec |
| Quy trình | superpowers/brainstorming — đường **Architectural** |
| Liên quan | `docs/prd/PRD_VSTEP-Lab_v3.0_20260927.md`, `docs/architecture/REFERENCE_ielts-cd_analysis.md` |

---

## 1. Mục tiêu & phạm vi

### 1.1 Mục tiêu
- Chốt **kiến trúc tổng thể** cho VSTEP Lab để một người xây và vận hành, ưu tiên ra sản phẩm nhanh, vừa với VPS 2 vCPU / 4 GB / 30 GB.
- Thiết kế chi tiết **lát cắt đầu tiên**: công cụ miễn phí **"Chấm thử Writing"** (PRD FR-010, FR-012, FR-013), chạy public ở **cuối tuần 2** để kiểm chứng P0 (mục tiêu O1: ≥ 200 lượt dùng từ seeding).

### 1.2 Quyết định đã chốt trong buổi brainstorming

| # | Quyết định |
|---|---|
| D1 | Spec gồm kiến trúc tổng thể + lát cắt "Chấm thử Writing" |
| D2 | AI Gateway không phụ thuộc provider; chọn provider bằng **thi đấu thử ở tuần 1** |
| D3 | Công cụ miễn phí không cần đăng ký; chống lạm dụng bằng CAPTCHA vô hình + giới hạn theo IP/thiết bị + trần chi phí ngày |
| D4 | Mua VPS Gold ngay tuần 1; triển khai đúng kiến trúc cuối cùng |
| D5 | **Modular monolith + worker** trên nền `fastapi/full-stack-fastapi-template` (MIT) |
| D6 | Giữ bài viết để cải thiện bộ chấm **chỉ khi người dùng đồng ý** (ô tick mặc định không chọn), đã ẩn thông tin cá nhân |
| D7 | Giữ FastAPI, kèm **cổng kiểm chứng tải ở tuần 1** (§8.4); không đạt thì đổi stack trước khi xây tiếp |

### 1.3 Ngoài phạm vi spec này
Engine thi 4 kỹ năng, chấm Speaking, soạn đề, dự đoán bậc, gói & thanh toán, cohort — mỗi phần có spec riêng sau này, dựa trên kiến trúc ở §2.

---

## 2. Kiến trúc tổng thể

### 2.1 Thành phần

```
Trình duyệt (React SPA / PWA, mobile-first)
        │ HTTPS
        ▼
Traefik (HTTPS tự động, định tuyến)
        │
        ▼
backend (FastAPI: /api/* + phục vụ SPA đã build)
        │
   ┌────┼──────────────┬───────────────────────────┐
   ▼    ▼              ▼                           ▼
PostgreSQL   Redis (hàng đợi, giới hạn   Dịch vụ ngoài: LLM provider(s),
             lượt, ngân sách, circuit    Cloudflare Turnstile, email,
             breaker)                     (sau này: speech, VietQR, object storage)
                ▲
                │
            worker (cùng codebase): chấm AI, dọn dữ liệu, gửi email
```

### 2.2 Module backend

Mỗi module là một package Python; **`service.py` là cửa ngõ duy nhất** cho module khác gọi vào.

| Module | Trách nhiệm | Lát cắt 1 |
|---|---|---|
| `core` | Cấu hình, DB session, logging, lỗi chung | ✅ |
| `auth` | Tài khoản (theo template) | Tối thiểu (admin) |
| `guard` | CAPTCHA, giới hạn lượt, trần chi phí, chặn tạm | ✅ |
| `ai_gateway` | Gọi LLM qua adapter; phân loại dữ liệu; model cố định; retry; circuit breaker; ghi chi phí | ✅ |
| `grading` | Rubric có version, dựng prompt, kiểm tra output & bằng chứng, tính điểm, ẩn thông tin cá nhân | ✅ (Writing) |
| `free_tools` | API "Chấm thử Writing" | ✅ |
| `corpus` | Kho bài đã ẩn danh (có đồng ý), eval set, eval run | ✅ |
| `analytics` | Sự kiện funnel theo mã nguồn | ✅ tối giản |
| `admin` | Trang xem chi phí, log, funnel, gắn điểm chuẩn cho corpus | ✅ tối giản |
| `exams`, `content`, `prediction`, `billing`, `cohort` | Theo PRD v3.0 | ❌ |

**Quy tắc ranh giới:**
1. Module chỉ import `service.py` của module khác; không import model/bảng của module khác. Một test tự động quét import để bắt vi phạm.
2. Chỉ `ai_gateway` được gọi LLM.
3. API và worker dùng chung service; chỉ khác điểm khởi chạy.

### 2.3 Frontend
React + Vite + Tailwind + shadcn/ui (từ template). Lát cắt 1 gồm: trang công cụ `/cham-thu-writing` (không đăng nhập) và trang admin tối giản.

---

## 3. Luồng "Chấm thử Writing"

1. Người dùng mở `/cham-thu-writing?src=<mã-nhóm>`. Frontend tạo `visitor_id` ngẫu nhiên (localStorage), ghi sự kiện `tool_view` kèm `src`.
2. Chọn Task 1 (thư/email) hoặc Task 2 (bài luận); dán đề bài hoặc chọn 1 trong 10 đề mẫu; dán bài viết. Tùy chọn tick ô **"Cho phép dùng bài viết (đã ẩn thông tin cá nhân) để cải thiện chất lượng chấm"** — mặc định không chọn; tick được thêm 1 lượt thành công trong ngày.
3. Kiểm tra phía trình duyệt: bài 50–600 từ, đề ≤ 300 từ, phát hiện sơ bộ là tiếng Anh. Turnstile lấy token.
4. `POST /api/free/writing-checks` với `{task_type, prompt, essay, captcha_token, visitor_id, src, consent_training}`. `guard`:
   - xác minh Turnstile ở server;
   - giới hạn theo `ip_hash` và `visitor_hash`: **2 kết quả thành công/ngày** (3 nếu đồng ý đóng góp bài), **tối đa 5 lần gửi/ngày**;
   - kiểm tra ngân sách AI còn lại trong ngày;
   - chống trùng theo `hash(prompt + essay + rubric_version)` → trả kết quả cũ, không tính lượt.
   Tạo bản ghi `free_writing_check` (`status=queued`, `purge_at = +24h`), đẩy job. Trả `202 {check_id, poll_token}`.
5. Worker: `grading.grade_writing(...)` → `ai_gateway.complete(task_key="writing_grade", data_class="A", rubric_version)`. Kiểm tra JSON theo schema và khoảng điểm; **mọi trích dẫn phải khớp nguyên văn bài** (chuẩn hóa khoảng trắng), nhận xét không khớp bị loại; schema sai hoặc 0 nhận xét hợp lệ → retry tối đa 2 lần → `failed`. Tính điểm 0–10 làm tròn 0,5. Nếu `consent_training` → ẩn thông tin cá nhân (§5) và ghi `training_corpus_item`. Lưu kết quả, `status=done`.
6. Frontend gọi `GET /api/free/writing-checks/{id}?t=<poll_token>` mỗi 2 giây trong 90 giây, sau đó mỗi 5 giây tới 5 phút.
   - `done`: điểm ước lượng + 3 lỗi chính (trích đoạn tô sáng, giải thích tiếng Việt, gợi ý sửa) + nhãn "Điểm ước lượng bởi AI — không phải kết quả chính thức" + nút "Đăng ký để lưu" + nút "Chia sẻ thẻ kết quả" (chỉ có điểm, không có nội dung bài) + mã yêu cầu xóa nếu đã đồng ý đóng góp.
   - `failed`: thông báo + nút thử lại; **không mất lượt**.
7. Job dọn dẹp mỗi giờ: với bản ghi quá `purge_at`, xóa `essay_text`, `prompt_text`, `ip_hash`, `visitor_hash`; giữ điểm, số từ, trạng thái, `src`.
8. Sự kiện funnel: `tool_view → submit → result_view → share_click / signup_click`, tất cả kèm `src`.

---

## 4. AI Gateway

### 4.1 Giao diện
`ai_gateway.complete(request) -> AIResult`, với `request = {task_key, data_class (A/B/C), messages, response_schema, max_output_tokens, correlation_id}`.

- **Bảng định tuyến** (file cấu hình có version trong repo): `task_key → {provider, model, params, fallback?}`. Mỗi `rubric_version` gắn cố định một model; đổi model = tạo rubric version mới và chạy lại eval.
- **Adapter mỗi provider** chuẩn hóa: gọi API, số token (input/output/cached), chi phí VNĐ theo bảng giá trong cấu hình, phân loại lỗi (`rate_limit`, `timeout`, `server`, `invalid_request`, `content_filter`).

### 4.2 Quy tắc

| Quy tắc | Cách thực hiện |
|---|---|
| Phân loại dữ liệu | Provider chỉ nhận lớp A khi cấu hình có `no_training: true` kèm đường dẫn tới bằng chứng điều khoản đã đọc |
| Output có cấu trúc | JSON mode/tool-calling của provider; kiểm tra lại bằng Pydantic |
| Retry | Tối đa 2 lần với `rate_limit`, `timeout`, `server`; backoff 2 s, 4 s |
| Circuit breaker | Theo provider, trạng thái trong Redis: mở sau 3 lỗi liên tiếp trong 60 s; half-open sau 60 s |
| Fallback | Chỉ khi task có cấu hình `fallback`; kết quả gắn `fallback=true` |
| Timeout | 60 s mỗi lần gọi |
| Ngân sách | Trước khi gọi: trừ tạm chi phí tối đa ước tính khỏi `budget:{ngày}` (Redis); sau khi gọi: điều chỉnh theo chi phí thật. Trần ngày mặc định **200.000đ**; cảnh báo email ở 50/80/100% |
| Prompt caching | Hướng dẫn hệ thống và rubric đặt đầu prompt |
| Log | Ghi `ai_request_log` (không chứa nội dung bài) |

### 4.3 Thi đấu thử chọn provider (tuần 1)

- **Ứng viên:** model tầm trung của Anthropic, OpenAI, Google — chọn theo bảng giá tại thời điểm thử.
- **Dữ liệu:** 30 bài (15 Task 1 + 15 Task 2) từ tình nguyện viên có đồng ý hoặc Founder tự viết ở nhiều trình độ; **Founder chấm điểm chuẩn**; lưu trong `eval_item`, không đưa vào git. Có ít nhất 2 bài chứa prompt injection.
- **Ngưỡng đạt** (mặc định, Founder có thể chỉnh sau khi xem kết quả):

| Tiêu chí | Ngưỡng |
|---|---|
| Sai số tuyệt đối trung bình so với điểm Founder | ≤ 0,75 |
| Chấm mỗi bài 3 lần, chênh lệch tối đa | ≤ 0,5 ở ≥ 90% bài |
| Trích dẫn khớp nguyên văn | ≥ 95% |
| JSON hợp lệ | ≥ 98% |
| Độ trễ p95 | ≤ 60 s |
| Chi phí mỗi bài | ≤ 1.500đ |
| Bài chứa injection | Điểm không bị kéo lên so với cùng bài không có injection |
| Điều khoản không huấn luyện trên dữ liệu API | Bắt buộc |

- **Quy tắc chọn:** loại provider trượt điều khoản hoặc chi phí; chọn provider có sai số thấp nhất; provider thứ hai làm fallback.
- **Đầu ra:** `eval_run` cho từng provider + `rubric writing-v1` cố định model đã chọn.

---

## 5. Dữ liệu

### 5.1 Bảng PostgreSQL

| Bảng | Trường chính | Vòng đời |
|---|---|---|
| `user` | Theo template + `role` | — |
| `free_writing_check` | `id` uuid, `task_type`, `prompt_text`, `essay_text`, `essay_hash`, `word_count`, `status`, `fail_reason`, `result` JSON, `score`, `rubric_version`, `fallback`, `visitor_hash`, `ip_hash`, `src`, `consent_training`, `poll_token_hash`, `purge_at`, `created_at` | Sau 24 h xóa nội dung và định danh; giữ số liệu |
| `training_corpus_item` | `id`, `source`, `task_type`, `prompt_redacted`, `essay_redacted`, `ai_result`, `rubric_version`, `model`, `delete_code_hash`, `human_score`, `human_notes`, `created_at` | Chỉ khi đồng ý; 24 tháng hoặc đến khi có yêu cầu xóa |
| `ai_request_log` | `id`, `task_key`, `data_class`, `provider`, `model`, `prompt_version`, `input_tokens`, `output_tokens`, `cached_tokens`, `cost_vnd`, `latency_ms`, `status`, `error_type`, `retry_count`, `fallback`, `correlation_id`, `created_at` | 90 ngày |
| `analytics_event` | `id`, `event`, `visitor_hash`, `src`, `check_id`, `props` JSON, `created_at` | 90 ngày |
| `eval_item` | `id`, `task_type`, `prompt_text`, `essay_text`, `human_score`, `consent_source`, `dataset_version` | Theo đồng ý của người đóng góp |
| `eval_run` | `id`, `rubric_version`, `provider`, `model`, `dataset_version`, `metrics` JSON, `created_at` | Lâu dài |

### 5.2 Redis
`rate:ip:{ip_hash}:{ngày}`, `rate:visitor:{visitor_hash}:{ngày}`, `budget:{ngày}`, `cb:{provider}`, hàng đợi job, danh sách chặn tạm theo ngày.

### 5.3 Bảo vệ định danh & đồng ý
- `ip_hash = HMAC(IP, khóa_ngày)`; khóa đổi mỗi ngày, không lưu IP thô.
- `poll_token`, `delete_code` chỉ lưu hash.
- **Ẩn thông tin cá nhân** trước khi ghi `training_corpus_item`: model trả danh sách đoạn chứa thông tin cá nhân trong cùng lượt chấm + regex dự phòng (số điện thoại, email, số dạng CMND/CCCD) → thay bằng `[TÊN]`, `[SĐT]`, `[EMAIL]`, `[ĐỊA CHỈ]`, `[SỐ GIẤY TỜ]`. Founder kiểm tra ngẫu nhiên 5% mỗi tuần.
- Kho corpus dùng cho: eval set, tinh chỉnh prompt/rubric/taxonomy lỗi. **Không** gửi đi để huấn luyện model của provider; **không** dùng để hiệu chỉnh dự đoán bậc.
- Thông báo xử lý dữ liệu hiển thị cạnh form: bài được gửi tới AI provider để chấm; bài gốc xóa sau 24 giờ; nội dung ô đồng ý.

---

## 6. Xử lý lỗi & chống lạm dụng

| Tình huống | Hệ thống | Người dùng | Mất lượt |
|---|---|---|---|
| CAPTCHA sai | 403, không tạo job | "Vui lòng thử lại" | Không |
| Vượt giới hạn ngày | 429 + thời điểm reset | Giờ reset + mời đăng ký | — |
| Chạm trần chi phí ngày | 503 + email admin | "Công cụ tạm nghỉ hôm nay" + ô để lại email | — |
| Dữ liệu không hợp lệ | 422 (kiểm tra ở cả client và server) | Lỗi cụ thể | Không |
| Provider lỗi | Retry → circuit breaker → fallback → `failed` | "Chấm chưa thành công, thử lại" | Không |
| JSON sai / trích dẫn không khớp | Retry ≤ 2; bỏ nhận xét sai; 0 hợp lệ → `failed` | Như trên | Không |
| Job kẹt > 3 phút | Đẩy lại 1 lần → `failed` | Như trên | Không |
| Chấm > 90 s | Frontend chuyển sang hỏi chậm, tới 5 phút | "Đang xử lý lâu hơn dự kiến" | — |
| Redis lỗi | Đóng công cụ miễn phí (503) | "Tạm bảo trì" | — |
| Prompt injection | Bài luôn được bọc là dữ liệu; kiểm tra khoảng điểm; có trong eval set | Chấm bình thường | — |

Chống lạm dụng bổ sung: giới hạn độ dài, chống trùng, cảnh báo khi lượt gửi mỗi giờ vượt 5 lần trung bình 7 ngày, chặn tạm `ip_hash` bất thường trong ngày.

---

## 7. Kiểm thử

| Lớp | Nội dung | Khi nào |
|---|---|---|
| Unit | Guard (giới hạn, ngân sách), so khớp trích dẫn, làm tròn điểm, ẩn thông tin cá nhân, circuit breaker, kiểm tra file định tuyến, test ranh giới import | CI mỗi commit |
| Contract | Adapter từng provider với phản hồi ghi sẵn; **không gọi API thật trong CI** | CI |
| Tích hợp | API → hàng đợi → worker → DB với provider giả, Postgres tạm | CI |
| E2E | Playwright, khung điện thoại: thành công, lỗi provider, vượt giới hạn | CI |
| Eval hồi quy | Chạy lại eval set khi đổi prompt/model/rubric; phải đạt ngưỡng §4.3 | Chạy tay |
| Tải | Xem §8.4 | Tuần 1 và trước ra mắt |

---

## 8. Triển khai & vận hành

### 8.1 Container trên VPS Gold (2 vCPU / 4 GB / 30 GB NVMe)

| Container | RAM ước tính |
|---|---|
| `traefik` | ~50 MB |
| `backend` (FastAPI, 2 worker, phục vụ SPA) | ~350 MB |
| `worker` | ~250 MB |
| `postgres` | ~1 GB |
| `redis` | ~100 MB |
| Hệ điều hành + dự phòng | ~700 MB |
| **Tổng** | **~2,5 GB** |

### 8.2 CI/CD
1. Mỗi commit: lint, kiểm tra kiểu, unit, contract, tích hợp, E2E.
2. Nhánh `main`: build image trên CI → GHCR → SSH vào VPS: `docker compose pull && docker compose up -d`; migration Alembic chạy trước khi backend khởi động. Rollback bằng cách triển khai lại tag image trước.
3. **Staging:** không có ở P0 (kiểm thử bằng Docker trên máy cá nhân); **bắt buộc có trước khi ra mắt tuần 10**.

### 8.3 Vận hành
- DNS & Turnstile: Cloudflare.
- Secrets: `.env` trên server (quyền 600); SSH key deploy trong GitHub Secrets.
- Backup: `pg_dump` hằng ngày → mã hóa → bucket ở nhà cung cấp khác; giữ 7 ngày + 4 tuần; diễn tập khôi phục hằng tháng.
- Giám sát: ping uptime từ bên ngoài; Sentry (free tier); trang admin chi phí; email cảnh báo ngân sách; cảnh báo ổ đĩa > 75%.
- Ổ đĩa: log Docker 10 MB × 3 file/container; `docker system prune` hằng tuần.
- Bảo mật: SSH chỉ bằng key; tường lửa 22/80/443; fail2ban; tự cập nhật bản vá; Postgres/Redis không mở ra ngoài.
- Runbook: `docs/runbook.md` (dựng VPS, deploy, rollback, khôi phục).

### 8.4 Cổng kiểm chứng tải (tuần 1, trước khi xây tiếp)
- **Môi trường:** VPS Gold thật, stack đầy đủ, **provider giả** trả kết quả sau độ trễ ngẫu nhiên 10–40 s.
- **Công cụ:** k6 hoặc Locust chạy từ máy khác.
- **Kịch bản:** 500 người dùng ảo đồng thời, mỗi người gửi 1 bài rồi hỏi trạng thái mỗi 2 giây cho tới khi có kết quả; cộng tải nền `GET` trang công cụ.
- **Đạt khi:** endpoint gửi bài và hỏi trạng thái đạt **≥ 200 request/giây với p95 < 300 ms**, tỉ lệ lỗi < 0,1%, **không mất job nào**, RAM < 3,5 GB.
- **Không đạt:** phân tích nguyên nhân (số worker, pool DB, truy vấn, cấu hình Redis). Nếu nguyên nhân nằm ở framework thì chọn lại stack trước khi viết thêm code.

---

## 9. Định nghĩa "xong" cho lát cắt 1 (cuối tuần 2)

- [ ] Công cụ chạy public trên domain thật qua HTTPS, dùng tốt trên điện thoại.
- [ ] Cổng kiểm chứng tải §8.4 đạt.
- [ ] Đã thi đấu thử provider; `rubric writing-v1` cố định model.
- [ ] CAPTCHA, giới hạn lượt, trần chi phí, chống trùng hoạt động (có test).
- [ ] Ô đồng ý đóng góp bài + ẩn thông tin cá nhân + mã yêu cầu xóa hoạt động.
- [ ] Funnel đo được theo `src`; trang admin xem chi phí và funnel.
- [ ] Backup hằng ngày chạy và đã khôi phục thử một lần.
- [ ] Đã đăng vào 3–5 nhóm cộng đồng.
