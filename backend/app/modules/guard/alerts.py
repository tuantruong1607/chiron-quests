"""Outbound alert email, isolated so tests can capture an "outbox" by
monkeypatching ``send_alert`` instead of touching a real SMTP server."""

from app.core.config import settings
from app.utils import send_email


def send_alert(subject: str, body: str) -> None:
    """Send an alert email to `settings.ALERT_EMAIL`.

    A no-op when email is not configured (`settings.emails_enabled` is
    False) or no `ALERT_EMAIL` is set.
    """
    if not settings.emails_enabled or not settings.ALERT_EMAIL:
        return
    send_email(email_to=settings.ALERT_EMAIL, subject=subject, html_content=body)
