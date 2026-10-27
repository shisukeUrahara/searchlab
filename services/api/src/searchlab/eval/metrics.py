"""Pure metric functions. ranked_ids is best-first; gold is the set of acceptable chunk IDs."""
from __future__ import annotations

from collections.abc import Collection, Sequence


def hit_at_k(ranked_ids: Sequence[str], gold: Collection[str], k: int) -> bool:
    return any(cid in gold for cid in ranked_ids[:k])


def reciprocal_rank_at_k(ranked_ids: Sequence[str], gold: Collection[str], k: int) -> float:
    for rank, cid in enumerate(ranked_ids[:k], start=1):
        if cid in gold:
            return 1.0 / rank
    return 0.0


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0
