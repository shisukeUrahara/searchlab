"""Pure metric functions. ranked_ids is best-first; gold is the set of acceptable chunk IDs."""
from __future__ import annotations

import math
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


def first_gold_rank(ranked_ids: Sequence[str], gold: Collection[str]) -> int | None:
    for rank, cid in enumerate(ranked_ids, start=1):
        if cid in gold:
            return rank
    return None


def ndcg_at_k(ranked_ids: Sequence[str], gold: Collection[str], k: int) -> float:
    """Binary-relevance nDCG: each gold chunk in the top k counts 1/log2(rank+1)."""
    dcg = sum(1.0 / math.log2(r + 1) for r, cid in enumerate(ranked_ids[:k], 1) if cid in gold)
    ideal = sum(1.0 / math.log2(r + 1) for r in range(1, min(len(gold), k) + 1))
    return dcg / ideal if ideal else 0.0


def recall_curve(first_ranks: Sequence[int | None], k_max: int = 10) -> list[float]:
    """Share of queries whose first gold chunk is within rank k, for k = 1..k_max."""
    n = len(first_ranks)
    return [
        sum(1 for r in first_ranks if r is not None and r <= k) / n if n else 0.0
        for k in range(1, k_max + 1)
    ]
