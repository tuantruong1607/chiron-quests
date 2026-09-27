from app.modules.grading.evidence import normalize_for_match, verify_quotes
from app.modules.grading.schema import Issue


def issue(
    quote: str, explanation_vi: str = "giải thích", suggestion: str = "sửa"
) -> Issue:
    return Issue(quote=quote, explanation_vi=explanation_vi, suggestion=suggestion)


def test_normalize_collapses_whitespace_and_curly_quotes() -> None:
    s = "  I  think\n\n“online   learning”  is ‘good’.  "
    assert normalize_for_match(s) == "I think \"online learning\" is 'good'."


def test_quote_matches_despite_curly_quotes_and_linebreaks() -> None:  # Review Focus #2
    essay = 'I think  "online\nlearning" is good.'
    ok, bad = verify_quotes(essay, [issue(quote="“online learning” is good")])
    assert len(ok) == 1
    assert bad == []


def test_fabricated_quote_dropped() -> None:
    ok, bad = verify_quotes("I like cats.", [issue(quote="I love dogs")])
    assert ok == []
    assert len(bad) == 1


def test_double_spaces_in_essay_and_quote_still_match() -> None:
    essay = "This  is   a  test essay about  climate change."
    ok, bad = verify_quotes(essay, [issue(quote="is a test essay")])
    assert len(ok) == 1
    assert bad == []


def test_verify_quotes_preserves_model_order() -> None:
    essay = "First point. Second point. Third point."
    issues = [
        issue(quote="Third point"),
        issue(quote="fabricated quote"),
        issue(quote="First point"),
    ]
    ok, bad = verify_quotes(essay, issues)
    assert [i.quote for i in ok] == ["Third point", "First point"]
    assert [i.quote for i in bad] == ["fabricated quote"]


def test_verify_quotes_empty_issues_returns_empty_lists() -> None:
    ok, bad = verify_quotes("Any essay text.", [])
    assert ok == []
    assert bad == []
