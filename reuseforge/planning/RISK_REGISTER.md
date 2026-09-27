# RISK_REGISTER
| ID | Rủi ro | Mức | Giảm thiểu | Task |
|---|---|---|---|---|
| R-01 | WER giọng Việt >15% với base.en | Cao | thử small.en (chép từng phần) → API STT no-training | T-006 |
| R-02 | vCPU VPS chậm hơn spike | TB | đo lại trên VPS; tách speech worker sang máy khác nếu cần | T-006 |
| R-03 | Chưa có chấm phát âm khi ra mắt | TB | report ghi 'chưa đánh giá được'; spike T-009 | T-008, T-009 |
| R-04 | Pháp lý thu tiền (TBD-05) | Cao | xác nhận tay trước; SePay sau khi rõ pháp lý | T-020 |
| R-05 | Thiếu đề (FR-096) | Cao | cắt xuống 3 bộ theo PRD §18 | T-017 |
| R-06 | Safari ghi âm khác codec | TB | backend nhận mp4 và webm; test trên iPhone thật | T-003, T-004 |
| R-07 | RAM VPS vượt 3,5 GB | TB | ngân sách RAM; load gate Task 12 chạy lại sau M2 | T-005 |
