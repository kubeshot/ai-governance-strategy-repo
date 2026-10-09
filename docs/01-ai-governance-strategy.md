# 01 — AI Governance Strategy (Gemini)

## 1. Purpose

Enable the organisation to adopt Google Gemini **quickly and safely**: maximise
productivity and product value while keeping data, customers, and the business protected.
Governance here is an *enabler* — a paved road with guardrails, not a gate that blocks
every request.

## 2. Scope

| Surface | Examples | Primary owner |
|---|---|---|
| Gemini for Google Workspace | Gemini in Gmail, Docs, Sheets, Meet, the Gemini app under enterprise terms | IT / Workspace admins |
| Gemini on Vertex AI | Custom applications, agents, RAG, batch processing via the Gemini API | Platform engineering |
| Gemini Code Assist | IDE code completion, chat, code review | Engineering enablement |
| Consumer Gemini (personal accounts) | gemini.google.com on a personal account | **Out of scope for company data — prohibited** |

## 3. Guiding principles

1. **Accountable humans.** Every AI use case has a named business owner. AI assists; people decide.
2. **Data stays protected.** Data classification rules apply to prompts exactly as they apply to email or file sharing.
3. **Risk-proportionate control.** Low-risk productivity use is self-service; high-risk use needs review and evaluation.
4. **Transparent by default.** Users and customers know when they are interacting with AI-generated content.
5. **Measured, not assumed.** Quality, safety, and cost are evaluated before release and monitored after.
6. **Secure by design.** Platform guardrails (org policies, perimeters, logging) are on by default, not opt-in.
7. **Reversible.** Every AI capability has a documented kill switch.

## 4. Operating model

**AI Governance Council** — meets monthly; approves policy, high-risk use cases, and exceptions.

| Role | Responsibility |
|---|---|
| Executive sponsor | Sets risk appetite, resolves escalations |
| AI governance lead | Owns this strategy, the policy set, and the use-case registry |
| Security (CISO office) | Technical controls, threat modelling, AI incident response |
| Privacy / Legal | Data protection impact assessments, contracts, regulatory mapping |
| Platform engineering | Vertex AI landing zone, guardrail code, monitoring |
| Use-case owners | Business justification, evaluation results, ongoing performance |
| Workspace admins | Gemini for Workspace settings, DLP rules, licensing |

### RACI

| Activity | Gov lead | Security | Privacy/Legal | Platform | Use-case owner |
|---|---|---|---|---|---|
| Maintain AI policies | **A/R** | C | C | C | I |
| Use-case intake & tiering | **A** | C | C | I | **R** |
| High-risk approval | **A** | R | R | C | R |
| Platform guardrails | C | **A** | I | **R** | I |
| Pre-release evaluation | C | C | I | C | **A/R** |
| Production monitoring | I | C | I | **R** | **A** |
| AI incident response | I | **A/R** | R | R | R |

## 5. Mapping to NIST AI RMF

| Function | What we do | Where |
|---|---|---|
| **Govern** | Council, policies, roles, training | This doc, docs/02 |
| **Map** | Use-case intake, context, risk tiering | docs/04, `policy/use-case-registry.yaml` |
| **Measure** | Evaluation, red teaming, metrics | docs/06 |
| **Manage** | Controls, monitoring, incident response, retirement | docs/05, docs/07, `src/` |

## 6. Roadmap

**Days 0–30 — Foundations**
- Publish the acceptable use policy and data classification matrix; launch staff training.
- Enable Gemini for Workspace for a pilot group with DLP and data-region settings configured.
- Stand up the Vertex AI landing zone: org policies, audit logs, VPC-SC perimeter.

**Days 31–60 — Paved road**
- Ship `GovernedGeminiClient` as the default SDK for internal applications.
- Open the use-case intake process; register the first 5–10 use cases.
- Baseline evaluation suite and dashboard (quality, safety, cost, latency).

**Days 61–90 — Scale**
- Expand Workspace rollout organisation-wide.
- First quarterly red-team exercise on high-risk use cases.
- Governance KPIs reported to the executive sponsor.

## 7. KPIs

| KPI | Target |
|---|---|
| Use cases running outside the registry | 0 |
| High-risk use cases with completed evaluation before go-live | 100% |
| Staff completing AI training | ≥ 95% |
| Mean time to disable a misbehaving AI feature | < 1 hour |
| Policy exceptions open > 90 days | 0 |
