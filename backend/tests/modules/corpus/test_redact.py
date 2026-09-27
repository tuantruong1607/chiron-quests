from app.modules.corpus.redact import redact
from app.modules.grading.service import PiiSpan


def test_redact_uses_model_spans_and_regex_backup():
    out = redact(
        "Dear Mr Nam, call me at 0912 345 678 or nam@x.vn",
        [PiiSpan(text="Mr Nam", kind="name")],
    )
    assert out == "Dear [TÊN], call me at [SĐT] or [EMAIL]"


def test_redact_handles_address_org_and_id_number():
    out = redact(
        "Nam lives at 12 Le Loi, works at Acme Corp, CCCD 123456789012",
        [
            PiiSpan(text="12 Le Loi", kind="address"),
            PiiSpan(text="Acme Corp", kind="org"),
        ],
    )
    assert out == "Nam lives at [ĐỊA CHỈ], works at [TỔ CHỨC], CCCD [SỐ GIẤY TỜ]"
    # "12 Le Loi" contains digits that are part of a redacted span, not the
    # standalone ID-number regex, so this also guards that spans are applied
    # before the ID regex could otherwise misfire on them.


def test_redact_regex_backup_alone_with_no_model_spans():
    out = redact("Call 0987654321 or email me at test.user@example.com", [])
    assert out == "Call [SĐT] or email me at [EMAIL]"


def test_redact_nine_digit_id_number():
    out = redact("So CMND cua toi la 123456789.", [])
    assert out == "So CMND cua toi la [SỐ GIẤY TỜ]."


def test_redact_longest_span_wins_when_overlapping():
    out = redact(
        "Contact Mr Nam Nguyen today",
        [PiiSpan(text="Nam", kind="name"), PiiSpan(text="Nam Nguyen", kind="name")],
    )
    assert out == "Contact Mr [TÊN] today"
