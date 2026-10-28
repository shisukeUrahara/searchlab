"""Run every retriever over a labeled query set and aggregate rank metrics with 95% CIs."""
from __future__ import annotations

from collections.abc import Mapping, Sequence

from pydantic import BaseModel

from searchlab.domain.models import LabeledQuery
from searchlab.domain.ports import Retriever
from searchlab.eval.bootstrap import bootstrap_ci
from searchlab.eval.metrics import (
    first_gold_rank,
    hit_at_k,
    mean,
    ndcg_at_k,
    reciprocal_rank_at_k,
)

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
    first_gold_rank: int | None = None
    ndcg_at_10: float = 0.0


class ScoreRow(BaseModel):
    method: str
    query_class: str  # "all" or a class name
    n: int
    recall_at_5: float
    mrr_at_10: float
    recall_at_1: float = 0.0
    recall_at_3: float = 0.0
    recall_at_10: float = 0.0
    ndcg_at_10: float = 0.0
    mrr_ci: tuple[float, float] | None = None
    recall_at_5_ci: tuple[float, float] | None = None


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
                    first_gold_rank=first_gold_rank(ranked, gold),
                    ndcg_at_10=ndcg_at_k(ranked, gold, MRR_K),
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
            hits5 = [1.0 if r.hit_at_5 else 0.0 for r in sel]
            rrs = [r.reciprocal_rank_at_10 for r in sel]

            def within(k: int, sel: list[CaseResult] = sel) -> float:
                return mean([1.0 if r.first_gold_rank and r.first_gold_rank <= k else 0.0
                             for r in sel])

            rows.append(
                ScoreRow(
                    method=method,
                    query_class=cls,
                    n=len(sel),
                    recall_at_5=mean(hits5),
                    mrr_at_10=mean(rrs),
                    recall_at_1=within(1),
                    recall_at_3=within(3),
                    recall_at_10=within(10),
                    ndcg_at_10=mean([r.ndcg_at_10 for r in sel]),
                    mrr_ci=bootstrap_ci(rrs),
                    recall_at_5_ci=bootstrap_ci(hits5),
                )
            )
    return rows
