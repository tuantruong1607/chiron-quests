"""arq worker entrypoint: `arq app.worker.WorkerSettings`.

Job functions for each `JobName` (see `app.core.jobs`) are registered here
by the modules that own them (grading, ...) as those are built in later
tasks. `arq.worker.Worker.__init__` raises `RuntimeError('at least one
function or cron_job must be registered')` when `functions` is empty, so
an empty list is not a runnable worker. Until a real job handler exists,
`health_check` is registered instead of an empty/fake placeholder: it is
a genuine, minimal function (usable as an arq liveness probe) rather than
a stand-in for work that isn't implemented yet.
"""

from typing import Any

from arq.connections import RedisSettings

from app.core.config import settings


async def health_check(_ctx: dict[str, Any]) -> str:
    return "ok"


class WorkerSettings:
    functions = [health_check]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
