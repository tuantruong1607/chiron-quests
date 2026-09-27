# DECISION_REPORT — VSTEP-LAB · Gate B (đề xuất)

| Cap | Quyết định | Bằng chứng |
|---|---|---|
| 001 Player | REIMPLEMENT (server giữ hạn nộp); SurveyJS loại | IMPLEMENTATION_VERIFIED |
| 002 Ghi âm | USE_AS_IS idb-keyval + hook tự viết | SOURCE_VERIFIED |
| 003 ASR | WRAP faster-whisper base.en | **SPIKE_VERIFIED** (RTF 0,098, 711 MB) |
| 004 Phát âm | **RUN_SPIKE** (hướng: Azure PA trên đoạn mẫu; OpenPronounce loại trên VPS) | SOURCE_VERIFIED |
| 005 Trôi chảy | REIMPLEMENT | ASSUMPTION |
| 006 TTS | USE_AS_IS Kokoro offline | IMPLEMENTATION_VERIFIED |
| 007 Chấm chuẩn | REIMPLEMENT (giữ Task 14) | SOURCE_VERIFIED |
| 008 Hiệu chỉnh | REIMPLEMENT (PAV tự viết) | SOURCE_VERIFIED |
| 009 PII | REIMPLEMENT (giữ LLM + regex) | SOURCE_VERIFIED |
| 010 VietQR | WRAP SePay + khái niệm agentpay-vn | SOURCE_VERIFIED |
| 011 Kiểm tra đề | REIMPLEMENT | USER_PROVIDED |
| 012 Nhắc học | REIMPLEMENT | SOURCE_VERIFIED |
| 013 Backup | EXTRACT_CONCEPT pg-s3-backup | SOURCE_VERIFIED |
| 014 Dataset | REJECT (phi thương mại) | SOURCE_VERIFIED |

## Tổ hợp bị loại
- Tự host toàn bộ Speaking (faster-whisper + OpenPronounce) trên VPS 4 GB: vượt RAM.
- small.en cho mọi bài: ~173 s/bài 12 phút nếu chép một lần → vượt p95 120 s; chỉ ổn khi chép từng phần.
- Dataset ELLIPSE/W&I cho hiệu chỉnh sản phẩm: vi phạm giấy phép.

## Chặn Gate B
RF-D-004 còn RUN_SPIKE → theo policy phải **loại khỏi phạm vi duyệt** hoặc giải quyết trước. RF-D-003 có 2 câu hỏi mở (WER giọng Việt, chạy lại trên VPS) — không chặn kiến trúc nhưng là điều kiện nghiệm thu M2.
