"""Use case: run one query through the requested methods and time each."""
from __future__ import annotations

import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from searchlab.domain.models import Chunk, ScoredChunk
from searchlab.domain.ports import Retriever
from searchlab.embeddings.cache import CacheMissError


@dataclass(frozen=True)
class MethodResult:
    method: str
    hits: list[ScoredChunk]
    latency_ms: float
    error: str | None = None  # e.g. "embedding_unavailable"; other methods still answer


class SearchService:
    def __init__(self, retrievers: Mapping[str, Retriever], chunks: Sequence[Chunk]) -> None:
        self._retrievers = dict(retrievers)
        self._chunks = {c.chunk_id: c for c in chunks}

    @property
    def methods(self) -> list[str]:
        return list(self._retrievers)

    @property
    def chunk_count(self) -> int:
        return len(self._chunks)

    def titles_by_source(self) -> dict[str, str]:
        return {c.source_id: c.title for c in self._chunks.values()}

    def chunk_counts_by_source(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for c in self._chunks.values():
            counts[c.source_id] = counts.get(c.source_id, 0) + 1
        return counts

    def search(self, query: str, methods: Sequence[str], top_k: int) -> list[MethodResult]:
        """Run each method; a method that needs a missing embedding reports an error instead.

        Raises CacheMissError only when every requested method failed that way.
        """
        out: list[MethodResult] = []
        for m in methods:
            start = time.perf_counter()
            try:
                hits, error = self._retrievers[m].search(query, top_k), None
            except CacheMissError:
                hits, error = [], "embedding_unavailable"
            out.append(MethodResult(m, hits, (time.perf_counter() - start) * 1000, error))
        if out and all(r.error for r in out):
            raise CacheMissError("no method could answer without an embedding")
        return out

    def chunk(self, chunk_id: str) -> Chunk | None:
        return self._chunks.get(chunk_id)
