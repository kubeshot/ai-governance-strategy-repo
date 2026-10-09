"""Load and query the machine-readable governance policy and use-case registry."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

PII_ACTIONS = {"redact", "block", "allow"}


@dataclass(frozen=True)
class RiskTier:
    name: str
    allowed_models: tuple[str, ...]
    prompt_pii_action: str
    output_pii_action: str
    safety_threshold: str
    max_output_tokens: int
    human_review_required: bool


@dataclass(frozen=True)
class UseCase:
    id: str
    description: str
    owner: str
    risk_tier: str
    data_classification: str
    approved: bool
    allow_pii: bool = False


class Policy:
    def __init__(self, tiers: dict[str, RiskTier], use_cases: dict[str, UseCase]):
        self.tiers = tiers
        self.use_cases = use_cases
        for uc in use_cases.values():
            if uc.risk_tier not in tiers:
                raise ValueError(f"use case {uc.id!r} has unknown risk tier {uc.risk_tier!r}")

    @classmethod
    def load(cls, policy_path: str | Path, registry_path: str | Path) -> Policy:
        raw_policy = yaml.safe_load(Path(policy_path).read_text())
        raw_registry = yaml.safe_load(Path(registry_path).read_text())

        tiers = {}
        for name, t in raw_policy["risk_tiers"].items():
            for key in ("prompt_pii_action", "output_pii_action"):
                if t[key] not in PII_ACTIONS:
                    raise ValueError(f"tier {name!r}: {key} must be one of {sorted(PII_ACTIONS)}")
            tiers[name] = RiskTier(
                name=name,
                allowed_models=tuple(t.get("allowed_models") or ()),
                prompt_pii_action=t["prompt_pii_action"],
                output_pii_action=t["output_pii_action"],
                safety_threshold=t["safety_threshold"],
                max_output_tokens=int(t["max_output_tokens"]),
                human_review_required=bool(t["human_review_required"]),
            )

        use_cases = {}
        for u in raw_registry["use_cases"]:
            use_cases[u["id"]] = UseCase(
                id=u["id"],
                description=u.get("description", ""),
                owner=u.get("owner", ""),
                risk_tier=u["risk_tier"],
                data_classification=u.get("data_classification", "internal"),
                approved=bool(u.get("approved", False)),
                allow_pii=bool(u.get("allow_pii", False)),
            )
        return cls(tiers, use_cases)

    def use_case(self, use_case_id: str) -> UseCase:
        try:
            return self.use_cases[use_case_id]
        except KeyError:
            raise KeyError(f"use case {use_case_id!r} is not registered") from None

    def tier_for(self, use_case: UseCase) -> RiskTier:
        return self.tiers[use_case.risk_tier]
