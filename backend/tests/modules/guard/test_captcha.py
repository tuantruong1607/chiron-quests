import httpx
import pytest
from pytest_httpx import HTTPXMock

from app.core.config import settings
from app.modules.guard.service import verify_captcha

pytestmark = pytest.mark.anyio


async def test_captcha_false_on_network_error(
    httpx_mock: HTTPXMock, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "TURNSTILE_SECRET", "secret")
    httpx_mock.add_exception(httpx.ConnectTimeout("x"))
    assert await verify_captcha("t", "1.2.3.4") is False


async def test_captcha_true_when_cloudflare_success(
    httpx_mock: HTTPXMock, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "TURNSTILE_SECRET", "secret")
    httpx_mock.add_response(json={"success": True})
    assert await verify_captcha("t", "1.2.3.4") is True


async def test_captcha_false_when_cloudflare_rejects(
    httpx_mock: HTTPXMock, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "TURNSTILE_SECRET", "secret")
    httpx_mock.add_response(json={"success": False})
    assert await verify_captcha("t", "1.2.3.4") is False


async def test_captcha_false_on_non_2xx_response(
    httpx_mock: HTTPXMock, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "TURNSTILE_SECRET", "secret")
    httpx_mock.add_response(status_code=500, json={"success": True})
    assert await verify_captcha("t", "1.2.3.4") is False


async def test_captcha_false_on_invalid_json(
    httpx_mock: HTTPXMock, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "TURNSTILE_SECRET", "secret")
    httpx_mock.add_response(content=b"not json")
    assert await verify_captcha("t", "1.2.3.4") is False


async def test_captcha_false_when_secret_not_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "TURNSTILE_SECRET", "")
    assert await verify_captcha("t", "1.2.3.4") is False
