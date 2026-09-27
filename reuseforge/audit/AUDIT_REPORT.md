# AUDIT_REPORT — VSTEP-LAB (reuseforge/1.0) · 2026-09-27

Trạng thái: **AUDIT_COMPLETE** — 27 ứng viên / 14 capability, mỗi ứng viên có đúng 1 trạng thái kiểm toán. Chưa phải quyết định kiến trúc (Gate B).

## Phát hiện bác bỏ quan trọng
1. **Speaking tự host trên VPS Gold không khả thi như dự tính.** faster-whisper (MIT) ước ~10 phút xử lý cho ~12 phút audio trên 2 vCPU; OpenPronounce cần torch + 2 model Wav2Vec2 large. → CAP-003/004 cần **spike** hoặc chuyển sang API trả phí/máy riêng.
2. **Azure Pronunciation Assessment** ≈ 6.500đ nếu chấm toàn bộ ~12 phút audio → vượt trần 4.000đ/bài (PRD F11) → chỉ chấm phát âm trên đoạn mẫu 2–3 phút, hoặc sửa giá.
3. **Model/dataset "mở" nhưng cấm thương mại:** CrisperWhisper weights, ELLIPSE, Write & Improve, phần lớn giọng Piper. Không dùng.
4. **Không có giấy phép → không dùng:** PronunciationCoach, payment-modules, docker-postgres-backup-age, zalo-python-sdk.
5. **GPL-3.0 gián tiếp** (phonemizer/espeak-ng) trong OpenPronounce và Kokoro → dùng phía server/offline không phân phối, nhưng vẫn cần Founder xác nhận.

## Dùng được ngay (VERIFIED)
- CAP-002: `idb-keyval` (Apache-2.0) + MediaRecorder gốc.
- CAP-005: tự tính từ word timestamps.
- CAP-008: `scipy.optimize.isotonic_regression` (BSD) — hoặc giữ PAV tự viết như plan.
- CAP-011: tự viết theo khái niệm đã phân tích.

## Cần spike trước khi chọn
- CAP-001 SurveyJS (MIT): giữ đồng hồ khi tải lại, audio phát 1 lần.
- CAP-003 faster-whisper: đo thời gian thật trên VPS Gold với 3 file 4 phút.
- CAP-004 OpenPronounce: RAM thực tế + độ đúng khi dùng transcript ASR làm câu tham chiếu (nói tự do).

## Trống / tự viết
CAP-014: không có dataset bài viết có điểm được phép dùng thương mại → giữ kế hoạch tự thu thập (corpus có đồng ý + Founder chấm).

Chi tiết từng ứng viên: `CANDIDATE_AUDITS.json`.
