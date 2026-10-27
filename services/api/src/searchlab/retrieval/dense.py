from __future__ import annotations

from collections.abc import Sequence

from searchlab.domain.models import Chunk, ScoredChunk
from searchlab.domain.ports import Embedder, VectorStore


def chunk_embedding_text(chunk: Chunk) -> str:
    """Same text BM25 indexes, so the two methods see identical content."""
    return f"{chunk.heading}\n{chunk.text}"


def build_dense_index(chunks: Sequence[Chunk], embedder: Embedder, store: VectorStore) -> None:
    vectors = embedder.embed([chunk_embedding_text(c) for c in chunks])
    store.upsert(chunks, vectors)


class DenseRetriever:
    def __init__(self, embedder: Embedder, store: VectorStore) -> None:
        self._embedder = embedder
        self._store = store

    def search(self, query: str, top_k: int) -> list[ScoredChunk]:
        if not query.strip():
            return []
        vector = self._embedder.embed([query])[0]
        return self._store.query(vector, top_k)
