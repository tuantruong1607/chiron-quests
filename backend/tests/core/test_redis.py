from datetime import UTC, date, datetime

import pytest

from app.core.jobs import JobName, enqueue
from app.core.redis import get_redis
from app.core.time import vn_today


def test_vn_today_rolls_over_at_vietnam_midnight() -> None:
    assert vn_today(now=datetime(2026, 10, 1, 16, 59, tzinfo=UTC)) == date(2026, 10, 1)
    assert vn_today(now=datetime(2026, 10, 1, 17, 0, tzinfo=UTC)) == date(2026, 10, 2)


@pytest.mark.anyio
async def test_enqueue_puts_job_on_the_arq_queue() -> None:
    redis = get_redis()
    queue_key = "arq:queue"
    before = await redis.zcard(queue_key)

    job_id = await enqueue(JobName.GRADE_FREE_CHECK, submission_id="abc123")

    assert job_id
    after = await redis.zcard(queue_key)
    assert after == before + 1
    assert await redis.exists(f"arq:job:{job_id}")
