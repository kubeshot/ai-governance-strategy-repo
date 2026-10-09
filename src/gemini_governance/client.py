"""GovernedGeminiClient: enforce the governance policy around every Gemini call."""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field

from .audit import AuditSink, build_record, prompt_hash, stdout_sink
from .pii import detect_pii, redact
from .policy import Policy, RiskTier

# (model, prompt, max_output_tokens, safety_threshold) -> response text
GenerateFn = Callable[[str, str, int, str], str]

HARM_CATEGORIES = (
    "HARM_CATEGORY_HATE_SPEECH",
    "HARM_CATEGORY_DANGEROUS_CONTENT",
    "HARM_CATEGORY_HARASSMENT",
    "HARM_CATEGORY_SEXUALLY_EXPLICIT",
)


class PolicyViolation(Exception):
    """Raised when a request is refused by the governance policy."""


@dataclass
class GovernedResponse:
    text: str
    use_case_id: str
    model: str
    human_review_required: bool
    prompt_pii_types: list[str] = field(default_factory=list)
    output_pii_types: list[str] = field(default_factory=list)


def vertex_generate_fn(project: str | None = None, location: str = "us-central1") -> GenerateFn:
    """Default backend: Gemini on Vertex AI via the google-genai SDK (pip install .[vertex])."""
    from google import genai
    from google.genai import types

    client = genai.Client(vertexai=True, project=project, location=location)

    def _generate(model: str, prompt: str, max_output_tokens: int, safety_threshold: str) -> str:
        config = types.GenerateContentConfig(
            max_output_tokens=max_output_tokens,
            safety_settings=[
                types.SafetySetting(category=c, threshold=safety_threshold) for c in HARM_CATEGORIES
            ],
        )
        resp = client.models.generate_content(model=model, contents=prompt, config=config)
        return resp.text or ""

    return _generate


class GovernedGeminiClient:
    def __init__(
        self,
        policy: Policy,
        generate_fn: GenerateFn | None = None,
        audit_sink: AuditSink = stdout_sink,
        project: str | None = None,
        location: str = "us-central1",
    ):
        self.policy = policy
        self._generate = generate_fn or vertex_generate_fn(project, location)
        self._audit = audit_sink

    def generate(
        self, use_case_id: str, prompt: str, model: str | None = None, user: str | None = None
    ) -> GovernedResponse:
        started = time.monotonic()
        audit = {
            "use_case_id": use_case_id,
            "user": user,
            "prompt_sha256": prompt_hash(prompt),
            "prompt_chars": len(prompt),
        }
        try:
            use_case = self.policy.use_case(use_case_id)
            tier = self.policy.tier_for(use_case)
            model = model or (tier.allowed_models[0] if tier.allowed_models else "")
            audit.update(risk_tier=tier.name, model=model)
            self._check_allowed(use_case.approved, tier, model)

            prompt_findings = detect_pii(prompt)
            audit["prompt_pii_types"] = sorted({f.type for f in prompt_findings})
            action = "allow" if use_case.allow_pii else tier.prompt_pii_action
            if prompt_findings and action == "block":
                raise PolicyViolation(
                    f"prompt contains PII ({', '.join(audit['prompt_pii_types'])}); "
                    f"tier {tier.name!r} blocks PII"
                )
            if prompt_findings and action == "redact":
                prompt = redact(prompt, prompt_findings)

            text = self._generate(model, prompt, tier.max_output_tokens, tier.safety_threshold)

            output_findings = detect_pii(text)
            audit["output_pii_types"] = sorted({f.type for f in output_findings})
            if output_findings and tier.output_pii_action == "block":
                raise PolicyViolation("model output contains PII; tier blocks PII in output")
            if output_findings and tier.output_pii_action == "redact":
                text = redact(text, output_findings)

            review = tier.human_review_required or bool(output_findings and tier.name == "high")
            audit.update(decision="allowed", human_review_required=review)
            return GovernedResponse(
                text=text,
                use_case_id=use_case_id,
                model=model,
                human_review_required=review,
                prompt_pii_types=audit["prompt_pii_types"],
                output_pii_types=audit["output_pii_types"],
            )
        except (PolicyViolation, KeyError) as exc:
            audit.update(decision="blocked", reason=str(exc).strip("'\""))
            raise PolicyViolation(audit["reason"]) from exc
        finally:
            audit.setdefault("decision", "error")
            audit["latency_ms"] = round((time.monotonic() - started) * 1000, 1)
            self._audit(build_record(**audit))

    @staticmethod
    def _check_allowed(approved: bool, tier: RiskTier, model: str) -> None:
        if tier.name == "prohibited":
            raise PolicyViolation("use case is in the prohibited risk tier")
        if not approved:
            raise PolicyViolation("use case is not approved")
        if model not in tier.allowed_models:
            raise PolicyViolation(f"model {model!r} is not allowed for tier {tier.name!r}")
