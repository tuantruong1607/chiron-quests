# SYSTEM_ARCHITECTURE — phần mở rộng R1 (ReuseForge) · VSTEP-LAB

Nền giữ nguyên spec `2026-09-27-vstep-lab-architecture-design.md` (modular monolith FastAPI + arq + Postgres + Redis trên VPS Gold). Bổ sung:

## Thành phần mới
- **Exam player (CAP-001)** — React/shadcn, Founder dựng. Đề = JSON có version. Hạn nộp do server giữ (`attempt.started_at + duration`); client đếm ngược từ `deadline` server trả → tải lại trang không reset (AC-F3-3).
- **Recorder (CAP-002)** — hook MediaRecorder + idb-keyval; mỗi phần là 1 Blob có `attempt_id/part`; upload idempotent (PUT theo khóa phần) → mất mạng thì tự thử lại (AC-F3-4).
- **Speech pipeline (CAP-003/004/005)** — upload phần → job arq ở hàng đợi `speech` (concurrency 1): ASR cục bộ faster-whisper base.en int8 (adapter trong ai_gateway) → số đo trôi chảy (tự viết) → [chờ RF-D-004] phát âm qua adapter dịch vụ trên đoạn mẫu → khi đủ 3 phần, job chấm Speaking (LLM) như Writing. Speech chỉ đi qua ai_gateway (giữ quy tắc module).
- **Audio đề (CAP-006)** — sinh offline bằng Kokoro trên máy Founder, lưu file tĩnh.
- **Thanh toán (CAP-010)** — payment adapter: tạo đơn (mã duy nhất) → QR SePay → webhook (xác minh khóa, idempotent theo mã giao dịch) + màn xác nhận tay có audit log.
- **Backup (CAP-013)** — `backup.sh` tự viết: pg_dump | age (public key) → bucket có lifecycle.

## Ngân sách RAM (4 GB)
Postgres 600 · Redis 80 · backend 350 · worker 300 · speech worker 800 · Traefik 60 · dự phòng OS 800 ⇒ ~3,0 GB.

## Seam kiểm chứng
- ASR: đo WER trên 20 mẫu giọng Việt (≤15%) + chạy lại spike trên VPS.
- Phát âm: 10 bài so với nhận định Founder; chi phí/bài ≤ 4.000đ.
- Player: test nghiệm thu reload phút 20; recorder: tắt/bật mạng.
