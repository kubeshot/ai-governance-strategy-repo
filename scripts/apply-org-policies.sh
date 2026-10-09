#!/usr/bin/env bash
# Apply the AI governance org-policy guardrails to one project.
# Usage: scripts/apply-org-policies.sh <PROJECT_ID> [--dry-run]
set -euo pipefail

PROJECT_ID="${1:?usage: $0 <PROJECT_ID> [--dry-run]}"
DRY_RUN="${2:-}"
POLICY_DIR="$(cd "$(dirname "$0")/../policy/org-policies" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Enabling required APIs on $PROJECT_ID ..."
[[ "$DRY_RUN" == "--dry-run" ]] || gcloud services enable \
  aiplatform.googleapis.com dlp.googleapis.com orgpolicy.googleapis.com logging.googleapis.com \
  --project="$PROJECT_ID"

for f in "$POLICY_DIR"/*.yaml; do
  out="$TMP/$(basename "$f")"
  sed "s/PROJECT_ID/$PROJECT_ID/g" "$f" > "$out"
  if grep -q 'C0xxxxxxx' "$out"; then
    echo "SKIP $(basename "$f") — set your directory customer ID first"
    continue
  fi
  if [[ "$DRY_RUN" == "--dry-run" ]]; then
    echo "--- would apply $(basename "$f")"; cat "$out"
  else
    echo "Applying $(basename "$f") ..."
    gcloud org-policies set-policy "$out"
  fi
done

echo "Done. Verify with: gcloud org-policies list --project=$PROJECT_ID"
