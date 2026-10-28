"""Load labeled query sets."""
from __future__ import annotations

from pathlib import Path

from searchlab.domain.models import LabeledQuery, Split


def load_queries(corpus_dir: Path, split: Split) -> list[LabeledQuery]:
    path = corpus_dir / f"queries.{split}.jsonl"
    lines = path.read_text().splitlines()
    return [LabeledQuery.model_validate_json(line) for line in lines if line]


def page_queries(
    queries: list[LabeledQuery],
    limit: int,
    offset: int,
    query_class: str | None = None,
    text: str | None = None,
) -> tuple[list[LabeledQuery], int]:
    """Filter by class and case-insensitive text, then slice. Returns (page, total matches)."""
    sel = [
        q for q in queries
        if (not query_class or q.query_class == query_class)
        and (not text or text.lower() in q.text.lower())
    ]
    return sel[offset:offset + limit], len(sel)
