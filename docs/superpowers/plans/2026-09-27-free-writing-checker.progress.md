# SDD ledger — plan: docs/superpowers/plans/2026-09-27-free-writing-checker.md
Spec: docs/superpowers/specs/2026-09-27-vstep-lab-architecture-design.md (reachable)
Branch: claude/beautiful-knuth-enswgg; plan-start commit ef66e78

## Pre-flight scan
| Pair / task | Produces vs consumes | Finding |
|---|---|---|
| T1→T3,T7 | get_redis, vn_today, enqueue, JobName | T1 Interfaces says `vn_today()`, Step 5 uses `vn_today(now=...)` → R2 |
| T2→T3,T7 | hash_ip/hash_visitor/verify_captcha | hash_visitor algorithm unspecified → R3 |
| T3→T4,T7,T12 | reserve_budget/settle/alert; limits | T12 needs LOADTEST_BYPASS_LIMITS "in T3/7 if missing" → R4 |
| T4→T5,T16 | complete, routing.yaml | T5 reads prompt_version/active_calibration from routing.yaml but T4 schema lacks them (T16 adds); grading must not import ai_gateway internals → R5 |
| T5→T6,T7,T14 | GradingOutcome, grade_writing | consistent |
| T6→T7,T13,T14,T15 | add_item, eval_cli, import_cli | compute_metrics(labels, runs) has no injection flag input → R6 |
| T8→T7,T9 | record_event, funnel | order 8 before 7 matches dependency list; ok |
| T7→T9,T10,T14 | routes, check list with ip_hash | T9 "lấy ip_hash từ danh sách check gần đây" needs a list endpoint → R7 |
| T9 | self | Step text "bảng đơn giản bằng shadcn Table" contradicts no-UI constraint → R8 |
| T10 | self | needs docker compose for client generation; no docker daemon here → R1 |
| T11,T12,T13 | self | real VPS/DNS/secrets/API keys/founder labels are external side effects → R9 |
| T14,T16 | frontend | already converted to briefs + acceptance tests; ok |
| T15→T16 | select_few_shot, fit_calibration | consistent |
| T1 | self | Step 1/6 require docker compose → R1 |

## Rulings
Ruling: R1 No Docker daemon in this container — tests run natively (uv, Python 3.14, local Postgres 16 + Redis on default ports); compose files are still written/updated and validated by parsing — costs if wrong: compose runtime issues surface only on Founder's machine/VPS.
Ruling: R2 `vn_today(now: datetime | None = None) -> date` — Step 5 test is the concrete contract — costs: none.
Ruling: R3 `hash_visitor(v) = HMAC-SHA256(SECRET_KEY, "visitor:" + v).hexdigest()` (not day-rotating; limits are per-day keys anyway) — costs: one-line change.
Ruling: R4 LOADTEST_BYPASS_LIMITS + X-Loadtest-Key implemented in Task 7 route layer (guard stays pure), default off — costs: small rework if moved.
Ruling: R5 Task 4 routing.yaml `writing_grade` includes `prompt_version: writing-p1`, `active_calibration: writing-c0`, `few_shot_ids: []` from the start; ai_gateway.service exposes `task_config(task_key) -> dict` which grading uses — costs: T16 only edits values.
Ruling: R6 compute_metrics gains optional `injection_flags: list[bool] | None` (+ runs on those items must not score above their label) — costs: signature tweak.
Ruling: R7 Task 9 adds `GET /api/v1/admin/recent-checks` (check_id, created_at, status, ip_hash) via free_tools.service — costs: small extra endpoint.
Ruling: R8 Task 9 is backend-only (no shadcn UI) per Global Constraint — costs: none.
Ruling: R9 Agent implements code/tests/docs for T11/T12/T13; steps needing VPS purchase, DNS, secrets, real API keys, remote k6 run, or founder-labeled essays are left as Founder steps and recorded, not faked — costs: those gates stay open until Founder acts.
Task 1: dispatched (BASE ef66e78, implementer agent a762bec5723bfc45b, model sonnet)
Task 1: implementer DONE_WITH_CONCERNS at b6bbece — pydantic pinned <2.13 (crash on py3.14.0rc2), arq health_check job registered (arq needs ≥1 fn)
Ruling: R10 Accept pydantic pin `>=2.12.0,<2.13.0` as a temporary env workaround (uv only offers 3.14.0rc2 here); revisit when image uses 3.14 final — costs: missing pydantic 2.13 fixes until unpinned.
Ruling: R11 Task 1 review package = diff of repo vs upstream template (excluding frontend/lockfiles) instead of the full import diff — costs: unchanged template files aren't re-reviewed (they're upstream MIT code).
Task 1: review — spec ✅, quality Approved but 1 Important: boundary detector misses relative imports crossing modules (from ..b import models) → fix round 1
Task 1: minor (deferred): enqueue opens/closes a new arq pool per call; cache pool when volume matters (revisit in Task 7/12)
Task 1: minor (deferred): get_redis lru_cache client never closed; add lifespan shutdown hook
Task 1: fix round 1/5 (1 addressed, 0 open; commits b6bbece..a3b8c13)
Task 1: minor (deferred): _containing_package redundant if/else; add literal tests for `from .. import b` and `from ..b.models import X`
Task 1: complete (commits ef66e78..a3b8c13, review clean)
Task 2: dispatched (BASE a3b8c13, implementer a32683e3189370f9d, sonnet)
Task 2: implementer DONE at 1675ae4 (anyio pytest plugin convention; pytest-httpx dev dep)
Task 2: review ✅ Approved; ⚠️ VN-day for hash_ip is caller's job → resolved: Task 7 must pass vn_today() (carried in Task 7 dispatch)
Task 2: complete (commits a3b8c13..1675ae4, review clean)
Task 3: dispatched (BASE 1675ae4)
Task 3: implementer aa1a0aa9e16df4b77 (sonnet)
Ruling: R12 Spike detection: hourly counter TTL 8 days (exception to 48h TTL, needs 7-day history); with zero history alert only when current hour ≥ 20 submissions — avoids alerts on first users; costs: an early real spike under 20/h goes unalerted.
Ruling: R13 reserve_submission check order blocked → successes → submissions; cap chosen by the current request's consent flag — costs: a user could toggle consent to get the 3rd success (acceptable, consent is real opt-in).
Task 3: implementer DONE at 530f80b
Task 3: review ✅ Approved; ⚠️ reserve→alert→settle sequencing belongs to Task 4 ai_gateway.complete (carried in dispatch)
Task 3: complete (commits 1675ae4..530f80b, review clean)
Task 4: dispatched (BASE 530f80b, implementer aeb7c81e8dd660cc6, sonnet)
Ruling: R14 complete() sequence: route → breaker (open→fallback or circuit_open) → estimate → reserve_budget → call w/ retries → settle(actual; 0 if no tokens) → budget alert → one log row per call; fallback also used when primary exhausts retries on retryable error; schema errors not retried at gateway (grading retries content) — costs: double-spend risk if fallback also fails is bounded by settle.
Ruling: R15 FakeAdapter default response is a fixed writing_grade-shaped JSON constant; fake latency via settings AI_FAKE_LATENCY_MIN_S/MAX_S (10/40) so Task 10 overrides by env — costs: Task 5 must keep schema aligned with the constant.
Task 4: implementer DONE at 444bfd0
Task 4: review Needs fixes — Important: (1) budget leak/no log on non-AIError paths after reserve; (2) breaker closed by stray failure while open, half-open no single trial, retries continue after reopen; (3) circuit_open no-fallback writes no log row → fix round 1
Ruling: R16 Promote two review Minors into Task 4 fix round: gateway-enforced 60 s timeout (spec §4.2 rule) and atomic breaker update (multiple workers in prod) — costs: slightly bigger fix diff.
Task 4: minor (deferred): cache routing/pricing YAML loads; check fallback's own breaker; alert on refused-budget path; breaker window not sliding; thin RED evidence
Task 4: fix round 1/5 (4 addressed, 1 open — cancellation handler not shielded so settle/log never run; commits 444bfd0..fec2f16)
Task 4: minor (deferred): trial token TTL should exceed TIMEOUT_S and be released on budget-refused/adapter-missing paths; non-AIError/invalid_request count toward breaker; is_open docstring side effect; fallback breaker unchecked
Ruling: R17 Promote trial-token TTL (> TIMEOUT_S) and release-on-unrecorded-paths into Task 4 round 2 — concurrent double trial is a correctness bug in multi-worker prod — costs: tiny extra diff.
Task 4: fix round 2/5 (2 addressed, 1 new open — blanket token-less trial release can delete another worker's trial; commits fec2f16..ec83883)
Task 4: minor (deferred): cancel between trial claim and reserve_budget not covered by try (narrow window)
Task 4: fix round 3/5 (1 addressed, 0 open; commits ec83883..7d47b8d)
Task 4: minor (deferred): exits between try_claim and try-block (estimate/reserve raising, cancel during reserve) leave trial until TTL; release_trial raising before settle/log when Redis down; duplicated pricing test helper
Task 4: complete (commits 530f80b..7d47b8d, review clean)
Task 5: dispatched (BASE 7d47b8d, implementer a0e77c251c91ac77f, sonnet)
Ruling: R18 Grading content retry: schema failure or all returned quotes invalid → retry (max 3 calls) then GradingFailed; non-schema AIError kinds → GradingFailed(kind) at once; zero issues from model is valid; criteria keys must match rubric exactly — costs: a strict model that finds no issues is accepted rather than re-asked.
Ruling: R19 Calibration file formats: identity; linear {a,b}; isotonic {x[],y[]} piecewise-linear with end clamps; output clamped [0,10] — Task 15 must write this format.
Task 5: implementer DONE at 8a1d5db (edited FakeAdapter default constant to match schema)
Task 5: review Needs fixes — Important: (1) empty/whitespace quotes verify; (2) essay/prompt can close </essay> tag early; (3) schema-failed attempts' cost missing from cost_vnd → fix round 1 (R20: fix 3 by carrying cost_vnd/latency_ms on AIError)
Ruling: R20 Carry cost_vnd/latency_ms on AIError (schema kind at least) and sum in grading — keeps "cost summed over retries" true for analytics — costs: small ai_gateway API change.
Task 5: minor (deferred): criterion keys hardcoded instead of from rubric; assert isinstance under -O; isotonic x/y validation; load_rubric error type inconsistent
Task 5: fix round 1/5 (3 addressed, 1 new open — tag regex misses attribute variants like </essay x>; commits 8a1d5db..ea2df57)
Task 5: minor (deferred): cost accumulated before final GradingFailed is discarded (gateway log rows still carry it)
Task 5: fix round 2/5 (1 addressed, 0 open; commits ea2df57..41ec05f)
Task 5: minor (deferred): tag regex over-matches <essay-x>/<essay.x> (escaped only, harmless)
Task 5: complete (commits 7d47b8d..41ec05f, review clean)
Task 6: dispatched (BASE 41ec05f, implementer a4853ad49960395f6, sonnet)
Ruling: R21 training_corpus_item gains check_id (for mark_thumbs_down) and is_injection (for injection metric) beyond spec §5.1 — costs: two extra columns.
Ruling: R22 eval_cli overrides route via ai_gateway.service.override_route(task_key, **fields) contextvar (in-process only) — costs: gateway API grows by one helper.
Ruling: R23 compute_metrics takes optional attempt/schema/quote counters + injection_flags (extends R6); injection_ok = flagged items' mean run score ≤ label + 0.5 — costs: threshold 0.5 is a guess, Founder may tune.
Ruling: R24 purge_expired = created_at older than 730 days (≈24 months) — costs: off by ~1 day vs calendar months.
Task 6: implementer DONE at c3a856a (quote_valid_rate stubbed 1.0; override_route added)
Task 6: review Needs fixes — Critical: ai_result stores raw PII (pii_spans text, issue quotes); Important: quote_valid_rate/defaults print PASS unmeasured, empty eval passes; eval can silently use fallback provider; import leaves orphan item on bad line → fix round 1 (+ minor 6 phone left boundary, minor 5 half-step, minor 7 override field validation promoted: cheap correctness)
Task 6: minor (deferred): consistency inflated when repeats fail; no (dataset_version, split) index / N+1; eval_run metrics omit item ids/counts (§7.4) — promote item ids into round 1
Task 6: fix round 1/5 (8 addressed, 0 open; commit 0e7b7a1) — reuseforge/ commits 8f8e0dc/9972138 in range are controller docs, not Task 6
Task 6: minor (deferred): GradingFailed drops quote counts; empty eval prints PASS rows for mae/p95/cost (Overall INCOMPLETE); one flaky item → INCOMPLETE; import TypeError tracebacks for wrong types; exit codes untested
Task 6: complete (commits 41ec05f..0e7b7a1, review clean)
Task 8: dispatched (BASE 9972138, implementer a5872fb08b0c08167, sonnet)
Ruling: R25 Funnel counts DISTINCT visitor_hash per event kind (people, not clicks); /events hashes visitor_id server-side via guard.hash_visitor; props ≤20 keys/2KB — costs: click volume not visible in funnel.
Task 8: review ✅ Approved
Task 8: minor (deferred): no rate limit on public POST /events (add guard limit in Task 7/12); check_id unvalidated; purge_events loads ids then deletes
Task 8: complete (commits 9972138..e2d3d42, review clean)
PAUSED by Founder after Task 8 (Founder pulls repo to run locally). Next: Task 7.
