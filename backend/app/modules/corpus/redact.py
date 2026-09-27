"""PII redaction for text going into `training_corpus_item` (spec §5.4).

Two passes:
1. Model-reported spans (`GradingOutcome.pii_spans`) - every occurrence of
   each span's exact text is replaced, longest span first so a shorter span
   nested inside a longer one doesn't get replaced first and break the
   longer match.
2. Regex backups for what the model might miss: a VN phone number, an
   email address, and a standalone 9- or 12-digit sequence (CMND/CCCD-style
   ID numbers).
"""

import re

from app.modules.grading.service import PiiSpan

#: Exact redaction labels per spec §5.4 (Vietnamese, verbatim).
PII_LABELS: dict[str, str] = {
    "name": "[TÊN]",
    "address": "[ĐỊA CHỈ]",
    "phone": "[SĐT]",
    "email": "[EMAIL]",
    "id": "[SỐ GIẤY TỜ]",
    "org": "[TỔ CHỨC]",
}

#: VN phone number backup regex (spec §5.4), e.g. "0912 345 678" or
#: "+84.912.345.678". Greedy reps can swallow one trailing separator
#: character (the last optional `[\s.-]?` before a non-digit) - `_sub_phone`
#: below trims that back off the match instead of consuming it.
#:
#: `(?<!\d)` on the left keeps this from starting mid-digit-run (e.g.
#: matching only the tail "00 000 000" out of a longer non-phone number
#: like "100 000 000 000"). `0(?!0)` on the bare-"0" branch keeps it from
#: starting on a double-zero, which no real VN number does (mobile/landline
#: prefixes are 0[2,3,5,7-9], never 00) - so a plain run of grouped zeroes
#: like "000 000 000" is never mistaken for a phone number either.
_PHONE_RE = re.compile(r"(?<!\d)(\+84|0(?!0))(\d[\s.-]?){8,10}")
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
#: Standalone 9- or 12-digit sequence (CMND/CCCD numbers). Digit boundaries
#: on both sides so this never eats into a longer digit run, and (applied
#: after the phone regex) never matches into whatever the phone pass left
#: behind.
_ID_RE = re.compile(r"(?<!\d)(\d{9}|\d{12})(?!\d)")


def _sub_phone(match: re.Match[str]) -> str:
    matched = match.group(0)
    trimmed = matched.rstrip(" .-")
    trailing_sep = matched[len(trimmed) :]
    return PII_LABELS["phone"] + trailing_sep


def redact(text: str, pii_spans: list[PiiSpan]) -> str:
    """Replace every PII span and regex-backup match in `text` with its
    label. Order matters: model spans first (exact text, all occurrences,
    longest first), then phone, then email, then ID-number regexes - phone
    before ID-number so a phone number's digit run is already gone by the
    time the ID-number regex runs."""
    result = text
    for span in sorted(pii_spans, key=lambda s: len(s.text), reverse=True):
        if not span.text:
            continue
        result = result.replace(span.text, PII_LABELS[span.kind])
    result = _PHONE_RE.sub(_sub_phone, result)
    result = _EMAIL_RE.sub(PII_LABELS["email"], result)
    result = _ID_RE.sub(PII_LABELS["id"], result)
    return result
