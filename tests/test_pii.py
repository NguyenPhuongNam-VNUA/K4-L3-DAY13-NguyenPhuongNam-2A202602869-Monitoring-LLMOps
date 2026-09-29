from app.pii import scrub_text


def test_scrub_email() -> None:
    out = scrub_text("Email me at student@vinuni.edu.vn")
    assert "student@" not in out
    assert "REDACTED_EMAIL" in out


def test_scrub_common_vietnamese_phone_formats() -> None:
    phone_numbers = (
        "0901234567",
        "090 123 4567",
        "090.123.4567",
        "090-123-4567",
        "+84 90 123 4567",
    )

    for phone_number in phone_numbers:
        out = scrub_text(f"Contact: {phone_number}")
        assert phone_number not in out
        assert "REDACTED_PHONE_VN" in out


def test_scrub_cccd() -> None:
    cccd_examples = ("001201012345", "079099123456")
    for cccd in cccd_examples:
        out = scrub_text(f"So CCCD cua toi la {cccd}")
        assert cccd not in out
        assert "REDACTED_CCCD" in out


def test_scrub_credit_card() -> None:
    card_numbers = (
        "1234-5678-9012-3456",
        "1234 5678 9012 3456",
        "1234567890123456",
    )
    for card in card_numbers:
        out = scrub_text(f"The thanh toan: {card}")
        assert card not in out
        assert "REDACTED_CREDIT_CARD" in out

