import pytest

from gemini_governance import GovernedGeminiClient, PolicyViolation


class FakeModel:
    def __init__(self, reply="ok"):
        self.reply = reply
        self.calls = []

    def __call__(self, model, prompt, max_output_tokens, safety_threshold):
        self.calls.append(
            {"model": model, "prompt": prompt, "max": max_output_tokens, "safety": safety_threshold}
        )
        return self.reply


@pytest.fixture
def records():
    return []


def make(policy, records, reply="ok"):
    model = FakeModel(reply)
    return GovernedGeminiClient(policy, generate_fn=model, audit_sink=records.append), model


def test_medium_tier_redacts_prompt_pii(policy, records):
    client, model = make(policy, records)
    resp = client.generate("support-ticket-summary", "Customer jane@example.com is upset")
    assert "jane@example.com" not in model.calls[0]["prompt"]
    assert "[REDACTED:EMAIL]" in model.calls[0]["prompt"]
    assert resp.prompt_pii_types == ["EMAIL"]
    assert model.calls[0]["max"] == 2048
    assert model.calls[0]["safety"] == "BLOCK_MEDIUM_AND_ABOVE"


def test_unregistered_use_case_blocked(policy, records):
    client, model = make(policy, records)
    with pytest.raises(PolicyViolation, match="not registered"):
        client.generate("shadow-ai-app", "hello")
    assert model.calls == []
    assert records[-1]["decision"] == "blocked"


def test_prohibited_use_case_blocked(policy, records):
    client, model = make(policy, records)
    with pytest.raises(PolicyViolation, match="prohibited"):
        client.generate("resume-auto-reject", "reject everyone")
    assert model.calls == []


def test_disallowed_model_blocked(policy, records):
    client, _ = make(policy, records)
    with pytest.raises(PolicyViolation, match="not allowed"):
        client.generate("support-ticket-summary", "hi", model="gemini-2.5-flash-lite")


def test_high_tier_with_allow_pii_passes_pii_through(policy, records):
    client, model = make(policy, records)
    resp = client.generate("claims-triage-assist", "Claimant SIN 046 454 286, water damage")
    assert "046 454 286" in model.calls[0]["prompt"]
    assert resp.human_review_required is True
    assert model.calls[0]["safety"] == "BLOCK_LOW_AND_ABOVE"


def test_output_pii_is_redacted(policy, records):
    client, _ = make(policy, records, reply="Reach the customer at 613-555-0199.")
    resp = client.generate("internal-doc-drafting", "Write a follow-up note")
    assert resp.text == "Reach the customer at [REDACTED:PHONE]."
    assert resp.output_pii_types == ["PHONE"]


def test_audit_record_never_contains_raw_prompt(policy, records):
    client, _ = make(policy, records)
    secret = "card 4111 1111 1111 1111"
    client.generate("internal-doc-drafting", secret, user="u1")
    rec = records[-1]
    assert secret not in str(rec)
    assert rec["event"] == "gemini_governed_call"
    assert rec["decision"] == "allowed"
    assert rec["prompt_pii_types"] == ["CREDIT_CARD"]
    assert len(rec["prompt_sha256"]) == 64


def test_backend_error_is_audited(policy, records):
    def broken(*_):
        raise RuntimeError("vertex unavailable")

    client = GovernedGeminiClient(policy, generate_fn=broken, audit_sink=records.append)
    with pytest.raises(RuntimeError):
        client.generate("internal-doc-drafting", "hello")
    assert records[-1]["decision"] == "error"
