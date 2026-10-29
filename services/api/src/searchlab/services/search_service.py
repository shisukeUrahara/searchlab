"""Use case: run one query through the requested methods and time each."""
from __future__ import annotations

import logging
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from searchlab.domain.models import Chunk, ScoredChunk
from searchlab.domain.ports import Retriever
from searchlab.embeddings.errors import CacheMissError, EmbeddingError

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class MethodResult:
    method: str
    hits: list[ScoredChunk]
    latency_ms: float
    error: str | None = None  # "embedding_unavailable" | "embedding_failed"; others still answer


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
        """Run each method; a method whose embedding fails reports an error instead.

        Re-raises the embedding error only when every requested method failed.
        """
        out: list[MethodResult] = []
        last: EmbeddingError | None = None
        for m in methods:
            start = time.perf_counter()
            try:
                hits, error = self._retrievers[m].search(query, top_k), None
            except EmbeddingError as exc:
                last = exc
                if isinstance(exc, CacheMissError):
                    error = "embedding_unavailable"
                else:
                    error = "embedding_failed"
                    log.warning("embedding failed for method %s: %s", m, exc)
                hits = []
            out.append(MethodResult(m, hits, (time.perf_counter() - start) * 1000, error))
        if last is not None and all(r.error for r in out):
            raise last
        return out

    def chunk(self, chunk_id: str) -> Chunk | None:
        return self._chunks.get(chunk_id)
