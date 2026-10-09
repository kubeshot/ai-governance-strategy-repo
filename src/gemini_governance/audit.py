"""Structured audit records for governed Gemini calls.

Records are single-line JSON on stdout, which Cloud Run and GKE forward to Cloud
Logging as jsonPayload. Raw prompt and response text is never logged.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

AuditSink = Callable[[dict[str, Any]], None]


def stdout_sink(record: dict[str, Any]) -> None:
    print(json.dumps(record, sort_keys=True), file=sys.stdout, flush=True)


def prompt_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def build_record(**fields: Any) -> dict[str, Any]:
    severity = "WARNING" if fields.get("decision") == "blocked" else "INFO"
    return {
        "event": "gemini_governed_call",
        "severity": severity,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        **fields,
    }
