# TECHNICAL_PLAN
Thứ tự thực thi (tuần tự, theo pha): P-01: T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 → T-008 → T-009 → T-010 · P-02: T-011 → T-012 → T-013 → T-014 → T-015 → T-016 → (T-017 Founder) · P-03: T-018 → T-019 → T-020 → T-021 → T-022 → T-023.
Mỗi task theo hợp đồng trong `TASK_GRAPH.json` (phạm vi đọc/ghi, lệnh, kiểm chứng). Mỗi task tạo tối đa 1 migration Alembic. Trước mỗi pha: `superpowers:writing-plans` chuyển các task của pha thành plan chi tiết TDD (như plan Writing checker) rồi mới dispatch.
