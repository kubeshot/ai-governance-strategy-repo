import pytest

from gemini_governance import Policy, RiskTier, UseCase


def test_loads_tiers_and_registry(policy):
    assert set(policy.tiers) == {"low", "medium", "high", "prohibited"}
    uc = policy.use_case("support-ticket-summary")
    assert uc.risk_tier == "medium" and uc.approved
    assert policy.tier_for(uc).prompt_pii_action == "redact"


def test_unknown_use_case_raises(policy):
    with pytest.raises(KeyError, match="not registered"):
        policy.use_case("shadow-ai-app")


def test_prohibited_tier_allows_no_models(policy):
    assert policy.tiers["prohibited"].allowed_models == ()


def test_registry_rejects_unknown_tier():
    tier = RiskTier("low", ("m",), "redact", "redact", "BLOCK_MEDIUM_AND_ABOVE", 10, False)
    bad = UseCase("x", "", "", "extreme", "internal", True)
    with pytest.raises(ValueError, match="unknown risk tier"):
        Policy({"low": tier}, {"x": bad})
