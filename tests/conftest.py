from pathlib import Path

import pytest

from gemini_governance import Policy

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def policy() -> Policy:
    return Policy.load(
        ROOT / "policy/governance-policy.yaml", ROOT / "policy/use-case-registry.yaml"
    )
