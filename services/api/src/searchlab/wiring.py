"""Composition root: the only place that picks concrete classes."""
from __future__ import annotations

import os
from pathlib import Path

from qdrant_client import QdrantClient

from searchlab.corpus.pipeline import read_chunks
from searchlab.domain.models import Chunk
from searchlab.domain.ports import Embedder, Retriever
from searchlab.embeddings.cache import CachingEmbedder
from searchlab.embeddings.openai_embedder import OpenAIEmbedder
from searchlab.retrieval.bm25 import Bm25Retriever
from searchlab.retrieval.dense import DenseRetriever, build_dense_index
from searchlab.retrieval.hybrid import HybridRetriever
from searchlab.store.qdrant_store import QdrantVectorStore

MODEL_ID = "text-embedding-3-small"


def make_embedder(corpus_dir: Path) -> Embedder:
    """Cached embedder; calls OpenAI only when a text is missing AND a key is set."""
    live = OpenAIEmbedder.from_env(MODEL_ID) if os.environ.get("OPENAI_API_KEY") else None
    return CachingEmbedder(corpus_dir / "embeddings_cache", MODEL_ID, live)


def make_retrievers(
    chunks: list[Chunk], embedder: Embedder, rrf_k: int = 60, qdrant_url: str | None = None
) -> dict[str, Retriever]:
    client = QdrantClient(url=qdrant_url) if qdrant_url else QdrantClient(":memory:")
    store = QdrantVectorStore(client)
    build_dense_index(chunks, embedder, store)
    bm25, dense = Bm25Retriever(chunks), DenseRetriever(embedder, store)
    return {"bm25": bm25, "dense": dense, "hybrid": HybridRetriever([bm25, dense], rrf_k=rrf_k)}


def load_chunks(corpus_dir: Path) -> list[Chunk]:
    return read_chunks(corpus_dir / "chunks.jsonl")
