"""Reciprocal Rank Fusion over any retrievers: score = sum(1 / (k + rank))."""
from __future__ import annotations

from collections.abc import Sequence

from searchlab.domain.models import Chunk, ScoredChunk
from searchlab.domain.ports import Retriever


class HybridRetriever:
    def __init__(self, retrievers: Sequence[Retriever], rrf_k: int = 60, depth: int = 50) -> None:
        self._retrievers = list(retrievers)
        self._k = rrf_k
        self._depth = depth

    def search(self, query: str, top_k: int) -> list[ScoredChunk]:
        scores: dict[str, float] = {}
        best_rank: dict[str, int] = {}
        chunks: dict[str, Chunk] = {}
        for retriever in self._retrievers:
            for hit in retriever.search(query, self._depth):
                cid = hit.chunk.chunk_id
                chunks[cid] = hit.chunk
                scores[cid] = scores.get(cid, 0.0) + 1.0 / (self._k + hit.rank)
                best_rank[cid] = min(best_rank.get(cid, hit.rank), hit.rank)
        order = sorted(scores, key=lambda c: (-scores[c], best_rank[c], c))[:top_k]
        return [
            ScoredChunk(chunk=chunks[c], score=scores[c], rank=r)
            for r, c in enumerate(order, start=1)
        ]
