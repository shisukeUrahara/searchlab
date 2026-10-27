import pytest

from searchlab.domain.models import Chunk, ScoredChunk
from searchlab.retrieval.hybrid import HybridRetriever


def c(cid: str) -> Chunk:
    return Chunk(chunk_id=cid, source_id="s", title="T", heading="H", text=cid, url="u")


class Fixed:
    def __init__(self, ids: list[str]) -> None:
        self._ids = ids

    def search(self, query: str, top_k: int) -> list[ScoredChunk]:
        return [
            ScoredChunk(chunk=c(i), score=1.0, rank=r)
            for r, i in enumerate(self._ids[:top_k], start=1)
        ]


def test_item_in_both_lists_beats_item_in_one() -> None:
    hits = HybridRetriever([Fixed(["a", "b", "c"]), Fixed(["c", "d", "a"])]).search("q", 4)
    assert [h.chunk.chunk_id for h in hits][:2] == ["a", "c"]


def test_score_matches_rrf_formula() -> None:
    hits = HybridRetriever([Fixed(["a"]), Fixed(["x", "a"])], rrf_k=60).search("q", 5)
    a = next(h for h in hits if h.chunk.chunk_id == "a")
    assert a.score == pytest.approx(1 / 61 + 1 / 62)


def test_ranks_start_at_one_and_top_k_applies() -> None:
    hits = HybridRetriever([Fixed(["a", "b", "c"])]).search("q", 2)
    assert [h.rank for h in hits] == [1, 2]


def ids(hits: list[ScoredChunk]) -> list[str]:
    return [h.chunk.chunk_id for h in hits]


def test_ties_are_deterministic() -> None:
    one = HybridRetriever([Fixed(["b"]), Fixed(["a"])]).search("q", 2)
    two = HybridRetriever([Fixed(["a"]), Fixed(["b"])]).search("q", 2)
    assert ids(one) == ids(two) == ["a", "b"]


def test_no_results_when_inputs_empty() -> None:
    assert HybridRetriever([Fixed([]), Fixed([])]).search("q", 5) == []
