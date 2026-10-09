# 05 — Technical Controls on Google Cloud

Platform guardrails are applied **once, centrally**, so every team building on Gemini inherits
them. Application guardrails (`src/gemini_governance`) add use-case-specific checks on top.

## 1. Resource hierarchy

```
Organization
└── folder: ai-platform
    ├── project: ai-sandbox        # experimentation, synthetic data only
    ├── project: ai-nonprod        # registered use cases, test data
    └── project: ai-prod           # registered + approved use cases only
```

Separate projects give separate IAM, quotas, budgets, and VPC-SC perimeters.

## 2. Organization Policy constraints

| Constraint | Purpose | File |
|---|---|---|
| `vertexai.allowedModels` | Only allow-listed Model Garden / Gemini models can be used | `policy/org-policies/vertexai-allowed-models.yaml` |
| `gcp.resourceLocations` | Keep processing and storage in approved regions | `policy/org-policies/resource-locations.yaml` |
| `iam.allowedPolicyMemberDomains` | Only company identities can be granted access | `policy/org-policies/allowed-member-domains.yaml` |
| `iam.disableServiceAccountKeyCreation` | No long-lived SA keys; use WIF / attached SAs | `policy/org-policies/disable-sa-keys.yaml` |

Apply with `scripts/apply-org-policies.sh <PROJECT_ID>`. Test in `ai-sandbox` first.

## 3. Identity & access

- Grant `roles/aiplatform.user` to **service accounts of registered applications**, not to broad groups.
- Humans get access through groups, scoped to non-prod by default.
- CI/CD authenticates with **Workload Identity Federation** (GitHub OIDC or Entra ID) — see `.github/workflows/vertex-eval.yml`. No service-account JSON keys.
- One service account per use case, so audit logs attribute every call to a use case.

## 4. Network & data perimeter

- **VPC Service Controls** perimeter around `aiplatform.googleapis.com`, `storage.googleapis.com`, `bigquery.googleapis.com`, and `dlp.googleapis.com` in `ai-prod`, blocking data exfiltration to projects outside the perimeter.
- **Private Service Connect** / Private Google Access for workloads calling Vertex AI from VPCs.
- **CMEK** with Cloud KMS for Vertex AI resources that store data (datasets, tuned models, vector indexes, batch outputs) in High-tier projects.

## 5. Content safety

- **Gemini safety settings** per risk tier (`policy/governance-policy.yaml` → `safety_threshold`).
- **Model Armor** templates in front of prompts and responses to screen for prompt injection, jailbreaks, malicious URLs, and sensitive data.
- **Sensitive Data Protection (Cloud DLP)** to inspect and de-identify prompts for Confidential/Restricted use cases. The built-in regex redactor in `GovernedGeminiClient` is a fallback, not a replacement.
- **Grounding** (Vertex AI Search or Google Search grounding) for factual use cases to reduce hallucination.

## 6. Logging & audit

- Enable **Data Access audit logs** for `aiplatform.googleapis.com` (`DATA_READ`, `DATA_WRITE`) in non-prod and prod projects.
- Application audit records from `GovernedGeminiClient` are JSON on stdout — Cloud Run and GKE send them to Cloud Logging automatically. They carry `use_case_id`, `risk_tier`, `model`, `decision`, PII counts, and a prompt hash; they never carry raw prompt text.
- Route both to a **log bucket with locked retention** (e.g. 400 days) and a BigQuery sink for governance dashboards.

## 7. Cost controls

- Per-project **budgets and alerts**; per-model **quotas** sized per use case.
- `max_output_tokens` cap per tier, enforced in code.
- Monthly cost review per use case (labels: `ai-use-case`, `ai-risk-tier`).

## 8. Gemini for Google Workspace

- Roll out by **organisational unit**; start with a pilot OU.
- Configure Workspace **DLP rules** and **data regions** before enabling Gemini broadly.
- Audit and fix **over-shared Drive content** — Gemini can surface anything the user can access.
- Retain Gemini conversation history per legal hold requirements (Vault).
- Disable features that are not yet approved (e.g. specific extensions) at the OU level.

## 9. Kill switches

| Scope | Action | Time to effect |
|---|---|---|
| One use case | Set `approved: false` in the registry and redeploy | Minutes |
| One model | Remove it from `vertexai.allowedModels` | Minutes |
| One project | Remove `roles/aiplatform.user` from the app SA | Minutes |
| All Vertex AI | Disable `aiplatform.googleapis.com` in the project | Minutes |
| Workspace | Turn Gemini off for the OU in Admin console | Minutes–hours (propagation) |
