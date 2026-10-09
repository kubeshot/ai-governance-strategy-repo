# AI Use-Case Intake Form

Copy this file, fill it in, and submit it to the AI governance lead.

## 1. Overview

| Field | Answer |
|---|---|
| Use-case name | |
| Proposed ID (kebab-case) | |
| Business owner (name, role) | |
| Technical owner | |
| Business problem / expected benefit | |
| Users (internal / customers / public) | |
| Expected volume (requests per day) | |
| Target go-live date | |

## 2. Model & architecture

| Field | Answer |
|---|---|
| Gemini surface (Workspace / Vertex AI / Code Assist) | |
| Model(s) requested | |
| Grounding / RAG data sources | |
| Tools or actions the model can trigger | |
| Where it runs (project, region) | |

## 3. Data

| Field | Answer |
|---|---|
| Highest data classification in prompts | Public / Internal / Confidential / Restricted |
| Personal data involved? Which categories? | |
| Customer data involved? Contract allows it? | |
| Data residency requirements | |
| Output stored where, for how long? | |

## 4. Risk questions

| Question | Yes / No | Notes |
|---|---|---|
| Output reaches customers or the public without human review? | | |
| Model can take actions without per-action human approval? | | |
| Could it affect a person's rights, employment, finances, health, or access? | | |
| Regulated domain? | | |
| Failure would cause material financial or reputational harm? | | |

## 5. Controls & evaluation plan

- Human-in-the-loop design:
- Evaluation dataset and pass criteria:
- Monitoring and feedback:
- Kill-switch plan:

## 6. Decision (governance use only)

| Field | Value |
|---|---|
| Risk tier | Low / Medium / High / Prohibited |
| Conditions | |
| Approved by / date | |
| Next review date | |
