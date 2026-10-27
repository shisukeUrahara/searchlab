"""Load labeled query sets."""
from __future__ import annotations

from pathlib import Path

from searchlab.domain.models import LabeledQuery, Split


def load_queries(corpus_dir: Path, split: Split) -> list[LabeledQuery]:
    path = corpus_dir / f"queries.{split}.jsonl"
    lines = path.read_text().splitlines()
    return [LabeledQuery.model_validate_json(line) for line in lines if line]
