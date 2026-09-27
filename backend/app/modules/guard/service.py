"""Guard module public entry point.

Exposes daily-rotating IP hashing, stable visitor hashing, Turnstile CAPTCHA
verification, per-day submission/success limits, the IP blocklist, AI
budget reservation with threshold alerts, and hourly spike detection. Other
modules must import this module only via ``app.modules.guard.service`` per
the module-boundary rule.
"""

import hashlib
import hmac
from datetime import date

from app.core.config import settings
from app.modules.guard.alerts import send_alert
from app.modules.guard.budget import (
    budget_used,
    maybe_send_budget_alert,
    reserve_budget,
    settle_budget,
)
from app.modules.guard.captcha import verify_captcha
from app.modules.guard.limits import (
    LimitDecision,
    block_ip_hash,
    is_blocked,
    record_success,
    reserve_submission,
    submissions_spike,
)

__all__ = [
    "hash_ip",
    "hash_visitor",
    "verify_captcha",
    "LimitDecision",
    "reserve_submission",
    "record_success",
    "block_ip_hash",
    "is_blocked",
    "submissions_spike",
    "reserve_budget",
    "settle_budget",
    "budget_used",
    "maybe_send_budget_alert",
    "send_alert",
]


def _hmac_hex(key: bytes, msg: str) -> str:
    return hmac.new(key, msg.encode(), hashlib.sha256).hexdigest()


def hash_ip(ip: str, day: date) -> str:
    """Hash an IP address, rotating the derived key every day.

    Two calls for the same IP on the same day produce the same hash; the
    same IP on a different day produces a different hash, so an IP cannot
    be tracked across days from the hash alone.
    """
    secret_key = settings.SECRET_KEY.encode()
    day_key_hex = _hmac_hex(secret_key, "ip:" + day.isoformat())
    day_key = bytes.fromhex(day_key_hex)
    return _hmac_hex(day_key, ip)


def hash_visitor(visitor_id: str) -> str:
    """Hash a visitor id with a stable (non day-rotating) HMAC."""
    secret_key = settings.SECRET_KEY.encode()
    return _hmac_hex(secret_key, "visitor:" + visitor_id)
