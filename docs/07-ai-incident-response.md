# 07 — AI Incident Response

AI incidents follow the standard security incident process, with the additions below.

## 1. What counts as an AI incident

- **Data leakage** — Restricted or Confidential data in a prompt where it should not be, or exposed in model output.
- **Harmful output** — discriminatory, dangerous, defamatory, or policy-violating content reaching users or customers.
- **Prompt injection / jailbreak** — the model followed malicious instructions from user input or retrieved content.
- **Unsafe action** — an agent or tool call changed a system, sent a message, or spent money without valid authorisation.
- **Shadow AI** — an unregistered application or personal account processing company data.
- **Material quality failure** — incorrect output that caused or nearly caused a business, legal, or customer impact.

## 2. Severity

| Severity | Examples | Response |
|---|---|---|
| **SEV1** | Restricted data exposed externally; unsafe action with customer impact | Page security on-call; kill switch within 1 hour; exec + legal notified |
| **SEV2** | Confidential data exposed internally beyond need-to-know; harmful output to a customer | Respond same business day; consider kill switch |
| **SEV3** | Blocked attempt, contained jailbreak, shadow-AI discovery | Ticket; fix within the sprint |

## 3. Playbook

1. **Contain** — use the narrowest kill switch that stops the harm (docs/05 §9).
2. **Preserve evidence** — export audit records (`use_case_id`, prompt hash, timestamps), Vertex AI Data Access logs, and application logs to the incident bucket.
3. **Assess** — what data, which users or customers, how long, what the model produced or did.
4. **Notify** — privacy/legal decide on regulatory and contractual notification timelines.
5. **Remediate** — fix prompt, retrieval permissions, guardrail config, or model version; add the failing case to the evaluation set.
6. **Re-evaluate** — re-run the use case's evaluation suite before re-enabling.
7. **Review** — blameless post-incident review within 5 business days; update policy and controls.

## 4. Reporting

Anyone can report a suspected AI incident to the security incident channel or
security@ (replace with your address). Reporting in good faith is always encouraged — including
your own mistakes.
