# AI Governance Strategy — Gemini on Google Cloud

Reference strategy, policies, and working guardrail code for governing **Google Gemini**
across an enterprise: Gemini in Google Workspace, Gemini models on **Vertex AI**, and
Gemini Code Assist.

> **Status:** sample / starter kit. Adapt the policies to your organisation, legal
> obligations, and contracts before adopting them.

## What's in here

| Path | What it is |
|---|---|
| [`docs/01-ai-governance-strategy.md`](docs/01-ai-governance-strategy.md) | Vision, principles, operating model, RACI, 30/60/90 roadmap |
| [`docs/02-gemini-acceptable-use-policy.md`](docs/02-gemini-acceptable-use-policy.md) | What staff may and may not do with Gemini |
| [`docs/03-data-classification-and-handling.md`](docs/03-data-classification-and-handling.md) | Which data classes may go to which Gemini surface |
| [`docs/04-risk-tiering-and-use-case-intake.md`](docs/04-risk-tiering-and-use-case-intake.md) | Risk tiers, required controls, approval path |
| [`docs/05-technical-controls-gcp.md`](docs/05-technical-controls-gcp.md) | Org policies, VPC-SC, CMEK, audit logs, Model Armor, WIF |
| [`docs/06-evaluation-and-monitoring.md`](docs/06-evaluation-and-monitoring.md) | Pre-release evaluation, red teaming, production monitoring |
| [`docs/07-ai-incident-response.md`](docs/07-ai-incident-response.md) | AI incident severities, playbook, kill switches |
| [`docs/templates/`](docs/templates/) | Use-case intake form and model card templates |
| [`policy/governance-policy.yaml`](policy/governance-policy.yaml) | Machine-readable policy: risk tiers, allowed models, PII handling |
| [`policy/use-case-registry.yaml`](policy/use-case-registry.yaml) | Registry of approved AI use cases |
| [`policy/org-policies/`](policy/org-policies/) | GCP Organization Policy constraints for Vertex AI |
| [`src/gemini_governance/`](src/gemini_governance/) | `GovernedGeminiClient` — policy-enforcing wrapper around Gemini |
| [`scripts/apply-org-policies.sh`](scripts/apply-org-policies.sh) | Applies the org-policy guardrails to a project |

## How the layers fit together

```
Strategy (docs/01)  ──▶  Policies (docs/02-04)  ──▶  Machine-readable policy (policy/*.yaml)
                                                          │
                     Platform guardrails (org policies, VPC-SC, audit logs)   ◀── docs/05
                                                          │
                     Application guardrails (GovernedGeminiClient)            ◀── src/
                                                          │
                     Evaluation, monitoring, incident response                ◀── docs/06-07
```

Every Gemini call made through `GovernedGeminiClient`:

1. must reference a **registered, approved use case** (`policy/use-case-registry.yaml`);
2. may only use a model **allow-listed for that use case's risk tier**;
3. is scanned for **PII** in the prompt — redacted or blocked depending on the tier;
4. runs with the tier's **safety settings** and output-token cap;
5. has its **output scanned** for PII leakage;
6. emits a **structured audit record** (hash of the prompt, never the raw text).

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q                      # runs fully offline — no GCP needed
```

Calling Gemini on Vertex AI for real:

```bash
pip install -e ".[vertex]"
export GOOGLE_CLOUD_PROJECT=my-project
python examples/summarize_support_ticket.py
```

## Frameworks referenced

- NIST AI Risk Management Framework (AI RMF 1.0) — Govern / Map / Measure / Manage
- ISO/IEC 42001:2023 — AI management systems
- EU AI Act risk categories (for organisations in scope)
- Google Secure AI Framework (SAIF)
