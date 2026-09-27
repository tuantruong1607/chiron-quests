# Template origin

VSTEP Lab's `backend/`, `frontend/`, `compose*.yml`, `.github/` and related
root files were imported from:

- Upstream: https://github.com/fastapi/full-stack-fastapi-template
- Commit: `cb740b656d7a0a6c5e12c7bf8e50343ec94ee9c7`
- License: MIT (kept as `LICENSE-template-MIT` at the repo root)

Since import, the template's `.env` was renamed to `.env.example` (with
`PROJECT_NAME` set to `VSTEP Lab` and new keys for Redis/AI-budget/Turnstile/
alerting added), and Redis + an arq worker service were added on top
(`backend/app/core/redis.py`, `backend/app/core/jobs.py`,
`backend/app/worker.py`, `compose.yml`'s `redis` and `worker` services).
