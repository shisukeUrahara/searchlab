from __future__ import annotations

from collections.abc import Sequence

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from searchlab.domain.models import Chunk, ScoredChunk


def _point_id(chunk_id: str) -> int:
    return int(chunk_id, 16)  # 16 hex chars -> fits Qdrant's unsigned 64-bit ids


class QdrantVectorStore:
    """Cosine-similarity store. Pass QdrantClient(':memory:') in tests, a URL in docker."""

    def __init__(self, client: QdrantClient, collection: str = "searchlab") -> None:
        self._client = client
        self._collection = collection

    def upsert(self, chunks: Sequence[Chunk], vectors: Sequence[Sequence[float]]) -> None:
        if not chunks:
            return
        dim = len(vectors[0])
        if not self._client.collection_exists(self._collection):
            self._client.create_collection(
                self._collection, vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
            )
        points = [
            PointStruct(id=_point_id(c.chunk_id), vector=list(v), payload=c.model_dump())
            for c, v in zip(chunks, vectors, strict=True)
        ]
        self._client.upsert(self._collection, points=points)

    def query(self, vector: Sequence[float], top_k: int) -> list[ScoredChunk]:
        if not self._client.collection_exists(self._collection):
            return []
        res = self._client.query_points(
            self._collection, query=list(vector), limit=top_k, with_payload=True
        )
        return [
            ScoredChunk(chunk=Chunk.model_validate(p.payload), score=float(p.score), rank=r)
            for r, p in enumerate(res.points, start=1)
        ]
