import pytest

from searchlab.domain.models import Chunk, LabeledQuery, ScoredChunk
from searchlab.eval.metrics import hit_at_k, mean, reciprocal_rank_at_k
from searchlab.eval.runner import evaluate, summarize


def test_hit_at_k_boundaries() -> None:
    ranked = ["a", "b", "c", "d", "e", "f"]
    assert hit_at_k(ranked, {"e"}, 5) is True
    assert hit_at_k(ranked, {"f"}, 5) is False
    assert hit_at_k(ranked, set(), 5) is False


def test_reciprocal_rank() -> None:
    assert reciprocal_rank_at_k(["a", "b", "c"], {"a"}, 10) == 1.0
    assert reciprocal_rank_at_k(["a", "b", "c"], {"c", "b"}, 10) == 0.5  # first gold at rank 2
    assert reciprocal_rank_at_k(["a"] * 3 + ["g"], {"g"}, 3) == 0.0  # beyond cutoff
    assert mean([]) == 0.0


class Canned:
    def __init__(self, table: dict[str, list[str]]) -> None:
        self._t = table

    def search(self, query: str, top_k: int) -> list[ScoredChunk]:
        return [
            ScoredChunk(
                chunk=Chunk(chunk_id=i, source_id="s", title="T", heading="H", text="", url="u"),
                score=1.0,
                rank=r,
            )
            for r, i in enumerate(self._t.get(query, [])[:top_k], start=1)
        ]


def q(qid: str, cls: str, gold: str) -> LabeledQuery:
    return LabeledQuery(
        query_id=qid, text=qid, query_class=cls, split="dev", gold_chunk_ids=(gold,)  # type: ignore[arg-type]
    )


def test_summary_hand_computed() -> None:
    queries = [q("q1", "exact_id", "a"), q("q2", "exact_id", "b"), q("q3", "paraphrase", "c")]
    r = Canned({"q1": ["a"], "q2": ["x", "b"], "q3": ["x", "y", "z"]})
    rows = summarize(evaluate({"m": r}, queries))
    by = {x.query_class: x for x in rows}
    assert by["all"].n == 3
    assert by["all"].recall_at_5 == pytest.approx(2 / 3)
    assert by["all"].mrr_at_10 == pytest.approx((1 + 0.5 + 0) / 3)
    assert by["exact_id"].recall_at_5 == 1.0 and by["exact_id"].n == 2
    assert by["paraphrase"].recall_at_5 == 0.0


def test_each_method_scored_on_same_queries() -> None:
    queries = [q("q1", "exact_id", "a")]
    results = evaluate({"good": Canned({"q1": ["a"]}), "bad": Canned({})}, queries)
    assert {(r.method, r.hit_at_5) for r in results} == {("good", True), ("bad", False)}
