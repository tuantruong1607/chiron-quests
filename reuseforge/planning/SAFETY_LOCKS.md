# SAFETY_LOCKS
- Không đổi hành động tái sử dụng đã duyệt (RF-D-*) mà không có Gate B mới.
- Không đưa code phát âm (CAP-004) vào sản phẩm trước khi Gate B được sửa.
- Không gửi dữ liệu lớp A (bài làm, ghi âm) tới provider không có `no_training: true`.
- Không commit secret (khóa SePay, Azure, OAuth); dùng biến môi trường.
- Không gọi LLM/speech API thật trong CI.
- Không thêm phụ thuộc GPL vào image backend (Kokoro chỉ ở `tools/tts/`).
- Không crawl/dùng đề có bản quyền (PRD §5.3).
