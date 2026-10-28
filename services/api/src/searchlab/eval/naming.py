"""Human-readable names for splits and runs."""
from __future__ import annotations

from datetime import datetime

SPLIT_LABEL = {"dev": "Tuning set", "test": "Holdout set"}


def run_label(corpus_label: str, split: str, rrf_k: int, created_at_utc: str) -> str:
    when = datetime.strptime(created_at_utc, "%Y-%m-%dT%H:%M:%SZ").strftime("%-d %b %Y %H:%M")
    parts = [corpus_label, SPLIT_LABEL.get(split, split), f"RRF k={rrf_k}", f"{when} UTC"]
    return " · ".join(p for p in parts if p)
