"""Cloudflare Turnstile CAPTCHA verification."""

import httpx

from app.core.config import settings

TURNSTILE_SITEVERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


async def verify_captcha(token: str, ip: str) -> bool:
    """Verify a Turnstile token with Cloudflare's siteverify endpoint.

    Fails closed: any network error, non-2xx response, invalid JSON body,
    or an empty/unconfigured secret all return ``False``.
    """
    if not settings.TURNSTILE_SECRET:
        return False

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                TURNSTILE_SITEVERIFY_URL,
                data={
                    "secret": settings.TURNSTILE_SECRET,
                    "response": token,
                    "remoteip": ip,
                },
            )
            response.raise_for_status()
            body = response.json()
    except httpx.HTTPError:
        return False
    except ValueError:
        return False

    return body.get("success") is True
