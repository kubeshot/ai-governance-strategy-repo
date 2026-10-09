"""Example: summarise a support ticket through the governed client.

Runs against Gemini on Vertex AI:
    pip install -e ".[vertex]"
    export GOOGLE_CLOUD_PROJECT=my-project
    python examples/summarize_support_ticket.py

Without GCP, pass --offline to use a stub model and see the guardrails work.
"""

import os
import sys
from pathlib import Path

from gemini_governance import GovernedGeminiClient, Policy, PolicyViolation

ROOT = Path(__file__).resolve().parent.parent

TICKET = """Customer Jane Doe (jane.doe@example.com, 613-555-0199) reports that invoices
since March show the wrong tax rate. She paid with card 4111 1111 1111 1111 and wants a refund
of the difference. Account tier: Business. Previous ticket closed without resolution."""


def stub_model(model, prompt, max_output_tokens, safety_threshold):
    header = f"[{model} | max {max_output_tokens} tokens | {safety_threshold}]"
    return f"{header} Summary of: {prompt[:120]}..."


def main() -> None:
    policy = Policy.load(
        ROOT / "policy/governance-policy.yaml", ROOT / "policy/use-case-registry.yaml"
    )
    offline = "--offline" in sys.argv
    client = GovernedGeminiClient(
        policy,
        generate_fn=stub_model if offline else None,
        project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    )

    prompt = "Summarise this support ticket in 3 bullet points for the agent:\n\n" + TICKET
    resp = client.generate("support-ticket-summary", prompt, user="agent-42")
    print("\n--- response ---\n" + resp.text)
    print(f"\nPII redacted from prompt: {resp.prompt_pii_types}")

    try:
        client.generate("resume-auto-reject", "Reject candidates without a degree.")
    except PolicyViolation as exc:
        print(f"\nBlocked as expected: {exc}")


if __name__ == "__main__":
    main()
