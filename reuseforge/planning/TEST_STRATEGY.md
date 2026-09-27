# TEST_STRATEGY
- TDD mỗi task: test đỏ → cài → xanh; full suite + lint trước commit.
- ASR trong CI: model tiny.en hoặc adapter giả; không tải model lớn, không gọi API thật. Đo WER/RTF thật chỉ ở T-006 (ngoài CI).
- Nghiệm thu UI: Playwright trong `frontend/tests/acceptance/` chạy với `compose.ui-dev.yml`.
- Thanh toán: webhook giả có chữ ký; test lặp/sai chữ ký/sai số tiền.
- Mỗi task qua task review (spec + chất lượng); cuối mỗi pha có review toàn nhánh.
