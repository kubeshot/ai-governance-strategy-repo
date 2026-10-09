# 02 — Gemini Acceptable Use Policy

**Applies to:** all employees, contractors, and partners using Gemini with company data or on
company systems.

## 1. Approved tools

Use only the company-provisioned, enterprise-licensed Gemini surfaces:

- Gemini for Google Workspace (signed in with your **company** account)
- Applications built on **Vertex AI** that are listed in the use-case registry
- Gemini Code Assist (company licence)

**Never** use a personal Google account or the consumer Gemini app for company work.
Consumer terms do not carry the enterprise data-protection commitments.

## 2. You may

- Draft, summarise, and rewrite documents, email, and meeting notes.
- Brainstorm, outline, and research **public** topics.
- Generate and review code in company repositories with Gemini Code Assist.
- Analyse Internal data in Workspace where the data classification matrix allows it.

## 3. You must

- **Review before you rely.** You are accountable for anything you send, publish, or commit — Gemini output can be wrong, outdated, or invented.
- **Follow the data classification matrix** (docs/03) for every prompt and every attached file.
- **Disclose AI assistance** in customer-facing content where required by policy or contract.
- **Keep humans in the loop** for decisions that affect people (hiring, performance, credit, access, discipline).
- **Report** suspected AI incidents — leakage, harmful output, prompt injection — to security within 24 hours.

## 4. You must not

- Enter **Restricted** data (credentials, keys, payment card data, government IDs, health records) into any Gemini prompt unless the use case is explicitly approved for it.
- Paste customer data into Gemini unless the customer contract and the registry entry permit it.
- Use Gemini to make fully automated decisions about individuals.
- Generate content that is deceptive, discriminatory, harassing, or that impersonates a real person.
- Try to bypass safety filters, guardrails, or monitoring (jailbreaks, prompt-injection testing outside an approved red-team exercise).
- Build or deploy a new Gemini-powered application without registering it (docs/04).
- Share API keys or service-account keys. Use Workload Identity Federation for CI/CD.

## 5. Intellectual property

- Check generated code for licence obligations before committing; Code Assist citations must be reviewed.
- Do not present AI-generated work as solely human-authored where that matters contractually.

## 6. Enforcement

Violations are handled under the standard information-security and code-of-conduct process.
Questions go to the AI governance lead.

## 7. Quick reference

| Situation | OK? |
|---|---|
| Summarise a public article in Gemini for Workspace | ✅ |
| Draft an internal project update from your own notes | ✅ |
| Paste a customer's database export into the Gemini app | ❌ |
| Ask Gemini to rank job applicants | ❌ (needs High-risk approval + human decision) |
| Use your personal Gemini account "just this once" | ❌ |
| Prototype on Vertex AI with synthetic data in a sandbox project | ✅ — register before production |
