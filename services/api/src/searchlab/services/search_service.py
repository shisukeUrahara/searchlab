"""Use case: run one query through the requested methods and time each."""
from __future__ import annotations

import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from searchlab.domain.models import Chunk, ScoredChunk
from searchlab.domain.ports import Retriever


@dataclass(frozen=True)
class MethodResult:
    method: str
    hits: list[ScoredChunk]
    latency_ms: float


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

    def search(self, query: str, methods: Sequence[str], top_k: int) -> list[MethodResult]:
        out: list[MethodResult] = []
        for m in methods:
            start = time.perf_counter()
            hits = self._retrievers[m].search(query, top_k)
            out.append(MethodResult(m, hits, (time.perf_counter() - start) * 1000))
        return out

    def chunk(self, chunk_id: str) -> Chunk | None:
        return self._chunks.get(chunk_id)
