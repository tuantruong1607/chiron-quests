import pytest

from app.core.config import settings
from app.modules.guard.service import send_alert


def test_send_alert_noop_when_email_not_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "SMTP_HOST", "")
    monkeypatch.setattr(settings, "ALERT_EMAIL", "ops@example.com")
    # Must not raise even though nothing is actually wired up to send email.
    send_alert("subject", "body")


def test_send_alert_noop_when_no_alert_email(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "SMTP_HOST", "smtp.example.com")
    monkeypatch.setattr(settings, "EMAILS_FROM_EMAIL", "noreply@example.com")
    monkeypatch.setattr(settings, "ALERT_EMAIL", None)
    send_alert("subject", "body")


def test_send_alert_calls_send_email_when_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "SMTP_HOST", "smtp.example.com")
    monkeypatch.setattr(settings, "EMAILS_FROM_EMAIL", "noreply@example.com")
    monkeypatch.setattr(settings, "ALERT_EMAIL", "ops@example.com")

    calls: list[dict[str, str]] = []
    monkeypatch.setattr(
        "app.modules.guard.alerts.send_email",
        lambda **kwargs: calls.append(kwargs),
    )

    send_alert("subject", "body")

    assert calls == [
        {
            "email_to": "ops@example.com",
            "subject": "subject",
            "html_content": "body",
        }
    ]
