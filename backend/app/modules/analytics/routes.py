"""`POST /api/v1/events` (spec §3 step 8, §5.1): frontend funnel pings.

Only `tool_view`/`share_click`/`signup_click` are accepted here -
`submit`/`result_view` are recorded server-side by `free_tools` (Task 7),
which already computed a `visitor_hash` for its own guard checks and calls
`app.modules.analytics.service.record_event` directly."""

import json
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, status
from pydantic import BaseModel, Field, field_validator

from app.modules.analytics import service
from app.modules.guard.service import hash_visitor

router = APIRouter(prefix="/events", tags=["analytics"])

#: Kept in sync with spec §3 step 8 - the events the *frontend* may report.
FrontendEventKind = Literal["tool_view", "share_click", "signup_click"]

MAX_SRC_LENGTH = 64
MAX_PROPS_KEYS = 20
MAX_PROPS_BYTES = 2 * 1024


class EventCreate(BaseModel):
    event: FrontendEventKind
    visitor_id: str
    src: str | None = Field(default=None, max_length=MAX_SRC_LENGTH)
    check_id: UUID | None = None
    props: dict[str, object] | None = None

    @field_validator("props")
    @classmethod
    def _validate_props(
        cls, value: dict[str, object] | None
    ) -> dict[str, object] | None:
        if value is None:
            return value
        if len(value) > MAX_PROPS_KEYS:
            raise ValueError(f"props must have at most {MAX_PROPS_KEYS} keys")
        size = len(json.dumps(value).encode("utf-8"))
        if size > MAX_PROPS_BYTES:
            raise ValueError(f"props must serialize to at most {MAX_PROPS_BYTES} bytes")
        return value


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
def create_event(payload: EventCreate) -> None:
    """Hash `visitor_id` (the raw id is never stored) and record the event.
    No auth - this endpoint is public, matching the free tool it instruments."""
    service.record_event(
        event=payload.event,
        visitor_hash=hash_visitor(payload.visitor_id),
        src=payload.src,
        check_id=payload.check_id,
        props=payload.props,
    )
