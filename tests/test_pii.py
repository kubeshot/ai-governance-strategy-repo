from gemini_governance import detect_pii, redact


def types(text):
    return [f.type for f in detect_pii(text)]


def test_detects_common_pii():
    text = "Mail jane.doe@example.com or call 613-555-0199."
    assert types(text) == ["EMAIL", "PHONE"]


def test_credit_card_requires_valid_luhn():
    assert types("card 4111 1111 1111 1111") == ["CREDIT_CARD"]
    assert types("card 4111 1111 1111 1112") == []


def test_canadian_sin_requires_valid_luhn():
    assert types("SIN 046 454 286") == ["CA_SIN"]
    assert types("SIN 046 454 287") == []


def test_us_ssn():
    assert types("SSN 123-45-6789") == ["US_SSN"]


def test_redact_replaces_spans():
    out = redact("Contact jane.doe@example.com, card 4111-1111-1111-1111.")
    assert out == "Contact [REDACTED:EMAIL], card [REDACTED:CREDIT_CARD]."


def test_clean_text_unchanged():
    text = "Summarise the Q3 roadmap for the platform team."
    assert detect_pii(text) == []
    assert redact(text) == text
