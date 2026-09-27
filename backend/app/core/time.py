"""Vietnam-local date helpers, used for daily resets (e.g. AI budget)."""

from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

VIETNAM_TZ = ZoneInfo("Asia/Ho_Chi_Minh")


def vn_today(now: datetime | None = None) -> date:
    """Return today's date in the `Asia/Ho_Chi_Minh` timezone.

    `now` defaults to the current UTC time; pass an aware `datetime` to
    compute the Vietnam-local date for a specific instant.
    """
    if now is None:
        now = datetime.now(UTC)
    return now.astimezone(VIETNAM_TZ).date()
