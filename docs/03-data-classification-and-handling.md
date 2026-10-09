# 03 — Data Classification & Handling for Gemini

## 1. Classification levels

| Level | Definition | Examples |
|---|---|---|
| **Public** | Approved for public release | Published blog posts, marketing pages, public docs |
| **Internal** | Day-to-day business information | Internal wiki, project plans, non-sensitive email |
| **Confidential** | Harm if disclosed | Customer names and contracts, financials, source code, architecture diagrams |
| **Restricted** | Severe harm or legal breach if disclosed | Credentials, keys, payment card data, government IDs (SIN/SSN), health data, regulated customer data |

## 2. Where each level may go

| Level | Gemini for Workspace (enterprise) | Vertex AI app (registered) | Gemini Code Assist | Consumer Gemini |
|---|---|---|---|---|
| Public | ✅ | ✅ | ✅ | ⚠️ Avoid — no company work |
| Internal | ✅ | ✅ | ✅ | ❌ |
| Confidential | ✅ within existing sharing permissions | ✅ if the use case is approved for Confidential | ✅ company repositories | ❌ |
| Restricted | ❌ | ⚠️ Only High-tier use cases with a DPIA, redaction, and CMEK | ❌ | ❌ |

## 3. Enterprise data commitments to confirm in your contract

Under Google Cloud and Google Workspace enterprise terms, Google states that customer data is
not used to train its foundation models without permission, and that prompts and responses
are handled under the Cloud Data Processing Addendum. **Verify these against your own
agreement** — do not rely on this document as legal advice.

Also confirm:

- **Data residency** — the regions where Vertex AI processing happens (`gcp.resourceLocations` org policy) and the Workspace data-region setting.
- **Retention** — Vertex AI request/response caching and logging settings; Workspace Vault retention for Gemini conversations.
- **Access transparency / approval** — enabled for Restricted workloads where available.

## 4. Handling rules

1. **Minimise.** Send Gemini only the fields the task needs. Prefer IDs over names.
2. **Redact before sending.** Applications use Sensitive Data Protection (Cloud DLP) or the built-in redactor in `GovernedGeminiClient` to remove PII before the prompt leaves the trust boundary.
3. **Ground, don't paste.** For large Confidential corpora, use Vertex AI Search / RAG with IAM-aware retrieval rather than pasting documents into prompts.
4. **Treat output with the highest input classification.** A summary of a Confidential document is Confidential.
5. **Log metadata, not content.** Audit logs store prompt hashes, sizes, and PII-type counts — never raw Restricted text.
6. **Workspace permissions are the boundary.** Gemini for Workspace only sees what the user can already open; fix over-shared Drive content *before* broad rollout.

## 5. PII handling by risk tier (enforced in code)

| Tier | PII found in prompt | PII found in output |
|---|---|---|
| Low | Redact | Redact |
| Medium | Redact | Redact |
| High | **Block** unless the use case has `allow_pii: true` | Redact + flag for human review |
| Prohibited | Not allowed to run | — |

See `policy/governance-policy.yaml`.
