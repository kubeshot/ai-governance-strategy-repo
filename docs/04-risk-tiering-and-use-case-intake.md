# 04 — Risk Tiering & Use-Case Intake

Every Gemini-powered application or workflow beyond personal productivity in Workspace must be
**registered** before production use. Registration assigns a risk tier, and the tier decides
the controls.

## 1. Intake process

```
Idea ─▶ Intake form (templates/use-case-intake.md)
          │
          ▼
      Triage by AI governance lead (≤ 3 business days) ─▶ risk tier assigned
          │
   ┌──────┼───────────────┬──────────────────┐
   ▼      ▼               ▼                  ▼
  Low   Medium           High            Prohibited
 self-  Security +       Council          rejected
 serve  Privacy review   approval
   │      │               │
   └──────┴──────┬────────┘
                 ▼
      Entry added to policy/use-case-registry.yaml (approved: true)
                 ▼
      Build with GovernedGeminiClient ─▶ evaluation (docs/06) ─▶ go-live
```

## 2. Risk tiers

| Tier | Typical characteristics | Examples |
|---|---|---|
| **Low** | Internal users, Public/Internal data, human always reviews output, easily reversible | Drafting internal docs, summarising public content, code explanation |
| **Medium** | Confidential data, or output reaches customers after human review | Support-ticket summarisation, sales email drafts, internal knowledge assistant |
| **High** | Restricted data, autonomous actions, decisions affecting individuals, or regulated domains | Claims triage, HR screening assistance, agents that change production systems |
| **Prohibited** | Unacceptable risk | Fully automated decisions on employment/credit/access, covert surveillance, biometric categorisation, social scoring |

### Scoring questions (any "yes" moves the use case up at least one tier)

1. Does it process Confidential data? (→ Medium) Restricted data? (→ High)
2. Does output reach customers or the public without human review? (→ High)
3. Can it take actions (call tools, write to systems) without a human approving each one? (→ High)
4. Could it materially affect a person's rights, employment, finances, health, or access? (→ High)
5. Is it in a regulated domain (financial advice, health, law enforcement, critical infrastructure)? (→ High)

## 3. Required controls by tier

| Control | Low | Medium | High |
|---|---|---|---|
| Registered in use-case registry | ✅ | ✅ | ✅ |
| `GovernedGeminiClient` (or equivalent guardrails) | ✅ | ✅ | ✅ |
| Allow-listed models only | ✅ | ✅ | ✅ (pinned versions) |
| PII redaction | ✅ | ✅ | Block by default |
| Safety threshold | Medium+ | Medium+ | Low+ (strictest) |
| Security review / threat model | — | ✅ | ✅ |
| Privacy impact assessment | — | If personal data | ✅ |
| Documented evaluation before go-live | Smoke test | ✅ | ✅ + red team |
| Human-in-the-loop for actions/decisions | — | Recommended | **Mandatory** |
| Model card (templates/model-card.md) | — | ✅ | ✅ |
| Re-review cadence | Annual | 6 months | Quarterly |

## 4. Exceptions

Exceptions need a written risk acceptance from the use-case owner's VP and the AI governance
lead, expire after 90 days at most, and are tracked in the registry (`exception_expires`).

## 5. Retirement

When a use case is retired: set `approved: false` in the registry (the client then refuses to
serve it), revoke service-account access, and archive evaluation evidence for 3 years.
