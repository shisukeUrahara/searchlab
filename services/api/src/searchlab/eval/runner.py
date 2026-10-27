"""Run every retriever over a labeled query set and aggregate Recall@5 / MRR@10."""
from __future__ import annotations

from collections.abc import Mapping, Sequence

from pydantic import BaseModel

from searchlab.domain.models import LabeledQuery
from searchlab.domain.ports import Retriever
from searchlab.eval.metrics import hit_at_k, mean, reciprocal_rank_at_k

RECALL_K = 5
MRR_K = 10


class CaseResult(BaseModel):
    query_id: str
    query_class: str
    method: str
    ranked_chunk_ids: list[str]
    gold_chunk_ids: list[str]
    hit_at_5: bool
    reciprocal_rank_at_10: float


class ScoreRow(BaseModel):
    method: str
    query_class: str  # "all" or a class name
    n: int
    recall_at_5: float
    mrr_at_10: float


def evaluate(
    retrievers: Mapping[str, Retriever], queries: Sequence[LabeledQuery]
) -> list[CaseResult]:
    results: list[CaseResult] = []
    for method, retriever in retrievers.items():
        for q in queries:
            ranked = [h.chunk.chunk_id for h in retriever.search(q.text, MRR_K)]
            gold = set(q.gold_chunk_ids)
            results.append(
                CaseResult(
                    query_id=q.query_id,
                    query_class=q.query_class,
                    method=method,
                    ranked_chunk_ids=ranked,
                    gold_chunk_ids=list(q.gold_chunk_ids),
                    hit_at_5=hit_at_k(ranked, gold, RECALL_K),
                    reciprocal_rank_at_10=reciprocal_rank_at_k(ranked, gold, MRR_K),
                )
            )
    return results


def summarize(results: Sequence[CaseResult]) -> list[ScoreRow]:
    rows: list[ScoreRow] = []
    methods = list(dict.fromkeys(r.method for r in results))
    classes = ["all", *dict.fromkeys(r.query_class for r in results)]
    for method in methods:
        for cls in classes:
            sel = [r for r in results if r.method == method and cls in ("all", r.query_class)]
            rows.append(
                ScoreRow(
                    method=method,
                    query_class=cls,
                    n=len(sel),
                    recall_at_5=mean([1.0 if r.hit_at_5 else 0.0 for r in sel]),
                    mrr_at_10=mean([r.reciprocal_rank_at_10 for r in sel]),
                )
            )
    return rows
