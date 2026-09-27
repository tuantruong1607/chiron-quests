from datetime import date

from app.modules.guard.service import hash_ip, hash_visitor


def test_same_ip_same_day_same_hash() -> None:
    assert hash_ip("1.2.3.4", date(2026, 10, 1)) == hash_ip(
        "1.2.3.4", date(2026, 10, 1)
    )


def test_same_ip_different_day_different_hash() -> None:
    assert hash_ip("1.2.3.4", date(2026, 10, 1)) != hash_ip(
        "1.2.3.4", date(2026, 10, 2)
    )


def test_hash_does_not_contain_ip() -> None:
    assert "1.2.3.4" not in hash_ip("1.2.3.4", date(2026, 10, 1))


def test_hash_ip_is_64_hex_chars() -> None:
    digest = hash_ip("1.2.3.4", date(2026, 10, 1))
    assert len(digest) == 64
    int(digest, 16)  # raises if not valid hex


def test_hash_visitor_is_deterministic() -> None:
    assert hash_visitor("visitor-abc") == hash_visitor("visitor-abc")


def test_hash_visitor_differs_per_visitor() -> None:
    assert hash_visitor("visitor-abc") != hash_visitor("visitor-xyz")


def test_hash_visitor_does_not_contain_visitor_id() -> None:
    assert "visitor-abc" not in hash_visitor("visitor-abc")
