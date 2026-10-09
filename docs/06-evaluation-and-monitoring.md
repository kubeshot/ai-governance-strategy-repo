# 06 — Evaluation & Monitoring

## 1. Pre-release evaluation

Every Medium and High use case ships with an evaluation report attached to its registry entry.

| Dimension | How | Pass bar (example) |
|---|---|---|
| Task quality | Golden dataset (≥ 50 cases for Medium, ≥ 200 for High) scored by rubric — Vertex AI Gen AI evaluation service or human raters | ≥ 90% acceptable |
| Groundedness | Answers checked against source documents | ≥ 95% grounded for factual use cases |
| Safety | Adversarial prompt set: harmful content, jailbreaks, prompt injection via retrieved documents | 0 critical failures |
| Privacy | Prompts containing seeded PII; confirm redaction and that no PII appears in output | 0 leaks |
| Fairness | Paired prompts varying protected attributes (High tier, people-affecting) | No material difference |
| Robustness | Typos, long inputs, other languages, empty input | Graceful handling |
| Cost & latency | p95 latency and cost per request at expected volume | Within budget |

**Model or prompt changes re-trigger evaluation.** Pin model versions for High-tier use cases
and test new versions before switching.

## 2. Red teaming (High tier)

- Quarterly exercise by security plus a domain expert.
- Focus: indirect prompt injection (malicious content in retrieved docs or emails), data exfiltration through tool calls, over-permissive agent actions, harmful output.
- Findings go to the use-case owner with fix-by dates; critical findings block go-live.

## 3. Production monitoring

| Signal | Source | Alert when |
|---|---|---|
| Blocked / redacted requests | `GovernedGeminiClient` audit logs | Spike > 3× 7-day baseline |
| Safety-filter blocks | Gemini response `finish_reason` / safety ratings | Sustained increase |
| User feedback (thumbs down, corrections) | Application | > 10% negative over 7 days |
| Unregistered callers | Vertex AI Data Access audit logs: SA not in registry | Any |
| Latency / errors | Cloud Monitoring | SLO breach |
| Cost | Billing export by `ai-use-case` label | > 120% of forecast |

## 4. Governance dashboard

Built from the BigQuery log sink:

- Requests per use case, tier, and model
- PII detections by type and action (redacted / blocked)
- Decisions: allowed / blocked, with reason
- Use cases due for re-review; open exceptions

## 5. Example: querying audit records

```sql
SELECT
  jsonPayload.use_case_id,
  jsonPayload.decision,
  COUNT(*) AS requests,
  COUNTIF(ARRAY_LENGTH(jsonPayload.prompt_pii_types) > 0) AS with_pii
FROM `ai-prod.governance_logs.stdout`
WHERE timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND jsonPayload.event = "gemini_governed_call"
GROUP BY 1, 2
ORDER BY requests DESC;
```
