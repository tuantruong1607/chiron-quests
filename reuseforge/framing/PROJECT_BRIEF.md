# PROJECT_BRIEF — VSTEP-LAB (reuseforge/1.0)

**Project ID:** VSTEP-LAB · **State:** FRAMING (chờ Gate A)
**Nguồn:** `docs/prd/PRD_VSTEP-Lab_v3.0_20260927.md` (USER_PROVIDED, đã được duyệt), `docs/superpowers/specs/2026-09-27-vstep-lab-architecture-design.md` (đã duyệt).

## Vấn đề
Người học cần bậc B1/B2 (VSTEP) thiếu công cụ luyện thi rẻ, đúng định dạng, có AI chấm Writing/Speaking đáng tin. Founder làm một mình, cần ra mắt ở tuần 10 với chi phí thấp → phải **tái sử dụng** tối đa thành phần mã nguồn mở/dịch vụ có sẵn cho phần **chưa xây**.

## Kết quả mong muốn
Với mỗi capability chưa xây trong R1/R1.1, có danh sách ứng viên tái sử dụng đã được kiểm toán (giấy phép, runtime, chất lượng), để quyết định dùng lại / bọc / tự viết trước khi viết code.

## Người dùng & bên liên quan
Thí sinh VSTEP (sinh viên, người đi làm); Founder (dev + soạn đề + chấm chuẩn); admin.

## Đầu vào / đầu ra
Vào: PRD v3.0, spec kiến trúc, stack hiện có (FastAPI template + module đã xây). Ra: capability graph → (sau Gate A) danh sách ứng viên + kiểm toán.

## Đã có — KHÔNG tìm lại (non-goals)
- Nền FastAPI/SQLModel/React (template MIT), Redis + arq worker, guard (hash IP, Turnstile, giới hạn, ngân sách), AI Gateway đa provider, chấm Writing (rubric/prompt/schema/trích dẫn/làm tròn/hiệu chỉnh), corpus + eval (đang xây), analytics funnel, admin cơ bản — đã có trong kế hoạch `2026-09-27-free-writing-checker.md`.
- Không tìm/crawl đề thi có bản quyền, đề thật do thí sinh nhớ lại (PRD §5.3).
- Không sao chép mã không có giấy phép (quyết định trước đó với `ielts-cd`).
- Không B2B, không app store trong R1.

## Giả định
- ASSUMPTION: Speaking dùng speech provider trả phí hoặc model tự host chạy CPU; chưa chọn (PRD TBD-04).
- ASSUMPTION: Thanh toán giai đoạn đầu xác nhận thủ công; webhook tự động là bước sau (FR-102).
- ASSUMPTION: VPS 2 vCPU / 4 GB / không GPU là môi trường chạy duy nhất trong R1.

## Domain profile
EdTech luyện thi tiếng Anh (VSTEP) cho thị trường Việt Nam; web/PWA mobile-first; dữ liệu cá nhân + ghi âm giọng nói.

## Thành công
Mỗi capability `required` có ≥ 1 ứng viên `VERIFIED`/`PARTIALLY_VERIFIED` hoặc kết luận rõ "tự viết" có lý do; không ứng viên nào vượt qua kiểm toán nếu giấy phép chưa rõ.
