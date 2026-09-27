"""Enqueue helpers for background jobs run by the arq worker."""

from enum import StrEnum
from typing import Any

from arq import create_pool
from arq.connections import RedisSettings

from app.core.config import settings


class JobName(StrEnum):
    GRADE_FREE_CHECK = "grade_free_check"


async def enqueue(job: JobName, **kwargs: Any) -> str:
    """Enqueue `job` on the arq queue and return the arq job id."""
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
    pool = await create_pool(redis_settings)
    try:
        arq_job = await pool.enqueue_job(job.value, **kwargs)
        assert arq_job is not None
        return arq_job.job_id
    finally:
        await pool.aclose()
