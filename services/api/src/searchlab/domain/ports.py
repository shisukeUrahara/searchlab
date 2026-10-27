"""Narrow interfaces. Concrete adapters live in their own packages."""
from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from searchlab.domain.models import Chunk, ScoredChunk


class Retriever(Protocol):
    def search(self, query: str, top_k: int) -> list[ScoredChunk]:
        """Return up to top_k chunks sorted by score descending, ranks starting at 1."""
        ...


class Embedder(Protocol):
    model_id: str

    def embed(self, texts: Sequence[str]) -> list[list[float]]: ...


class VectorStore(Protocol):
    def upsert(self, chunks: Sequence[Chunk], vectors: Sequence[Sequence[float]]) -> None: ...

    def query(self, vector: Sequence[float], top_k: int) -> list[ScoredChunk]: ...
