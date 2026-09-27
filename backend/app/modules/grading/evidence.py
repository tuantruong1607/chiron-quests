"""Evidence (quote) verification: a model-reported `Issue.quote` is only
trustworthy if it can actually be found, verbatim modulo whitespace/curly
quotes, in the essay it claims to quote from.
"""

import re

from app.modules.grading.schema import Issue

#: Curly/typographic quotes the model may echo back -> their straight ASCII
#: equivalents, so `normalize_for_match` treats them as identical to what a
#: plain-text essay actually contains.
_QUOTE_MAP = {
    "“": '"',  # “
    "”": '"',  # ”
    "‘": "'",  # ‘
    "’": "'",  # ’
}

_WHITESPACE_RE = re.compile(r"\s+")

#: A controller ruling: a normalized quote shorter than this can't count as
#: evidence, even if it happens to be a verbatim substring (e.g. an empty
#: string, or a 1-2 character fragment like "ca") - it's too small to be
#: meaningful evidence of anything the model actually flagged.
MIN_QUOTE_LENGTH = 3


def normalize_for_match(s: str) -> str:
    """Collapse all whitespace/linebreaks to a single space, normalize
    curly quotes to straight ones, and strip leading/trailing whitespace -
    the shared normalization both sides of a quote comparison go through."""
    for curly, straight in _QUOTE_MAP.items():
        s = s.replace(curly, straight)
    return _WHITESPACE_RE.sub(" ", s).strip()


def verify_quotes(essay: str, issues: list[Issue]) -> tuple[list[Issue], list[Issue]]:
    """Split `issues` into (valid, dropped) by checking whether each one's
    `quote`, after normalization, actually occurs in the (also normalized)
    essay. Order within each returned list matches the input order.

    A quote that normalizes to fewer than `MIN_QUOTE_LENGTH` characters -
    including an empty or whitespace/newline-only quote - is always
    dropped, regardless of whether it "matches": an empty string is
    trivially a substring of anything, and a tiny fragment like "ca" isn't
    meaningful evidence even when it happens to occur verbatim."""
    normalized_essay = normalize_for_match(essay)
    valid: list[Issue] = []
    dropped: list[Issue] = []
    for issue in issues:
        normalized_quote = normalize_for_match(issue.quote)
        if (
            len(normalized_quote) >= MIN_QUOTE_LENGTH
            and normalized_quote in normalized_essay
        ):
            valid.append(issue)
        else:
            dropped.append(issue)
    return valid, dropped
