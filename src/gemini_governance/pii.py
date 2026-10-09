"""Lightweight, offline PII detection and redaction.

This is a fallback for tests and low-risk use cases. For Confidential or Restricted
data, use Sensitive Data Protection (Cloud DLP) — see docs/05.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    type: str
    start: int
    end: int


def _luhn_ok(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


# Order matters: earlier detectors win when spans overlap.
_DETECTORS: list[tuple[str, re.Pattern[str], bool]] = [
    ("CREDIT_CARD", re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)"), True),
    ("US_SSN", re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)"), False),
    ("CA_SIN", re.compile(r"(?<!\d)\d{3}[ -]?\d{3}[ -]?\d{3}(?!\d)"), True),
    ("EMAIL", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), False),
    ("PHONE", re.compile(r"(?<!\d)(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]?\d{3}[ .-]?\d{4}(?!\d)"), False),
]


def detect_pii(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for pii_type, pattern, needs_luhn in _DETECTORS:
        for m in pattern.finditer(text):
            if needs_luhn and not _luhn_ok(re.sub(r"\D", "", m.group())):
                continue
            if any(m.start() < f.end and f.start < m.end() for f in findings):
                continue
            findings.append(Finding(pii_type, m.start(), m.end()))
    return sorted(findings, key=lambda f: f.start)


def redact(text: str, findings: list[Finding] | None = None) -> str:
    findings = detect_pii(text) if findings is None else findings
    out, pos = [], 0
    for f in findings:
        out.append(text[pos:f.start])
        out.append(f"[REDACTED:{f.type}]")
        pos = f.end
    out.append(text[pos:])
    return "".join(out)
