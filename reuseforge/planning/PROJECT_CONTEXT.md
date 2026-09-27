# PROJECT_CONTEXT
- Stack: FastAPI template (Python 3.14, SQLModel, Alembic, Postgres 16, Redis, arq), React+Vite+shadcn; VPS Gold 2 vCPU/4 GB.
- Module đã có: core (redis/time/jobs), guard, ai_gateway (routing, breaker, budget, override_route), grading (Writing), corpus (+eval), analytics (đang làm), free_tools (Task 7).
- Quy tắc: module chỉ gọi nhau qua `service.py`; chỉ ai_gateway gọi SDK AI/speech; không LLM thật trong CI; UI sản phẩm do Founder dựng bằng Antigravity — agent viết API, brief `docs/ui/`, test nghiệm thu `frontend/tests/acceptance/`.
- Cách thực thi: superpowers subagent-driven-development (implementer → task review → fix loop), tuần tự, ledger trong `.superpowers/sdd/`.
