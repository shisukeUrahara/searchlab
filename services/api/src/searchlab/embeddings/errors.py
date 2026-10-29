"""Embedding failures that callers can degrade around (e.g. fall back to BM25)."""
from __future__ import annotations


class EmbeddingError(RuntimeError):
    """Base: a text could not be turned into a vector."""


class CacheMissError(EmbeddingError):
    """The vector is not cached and no live embedder is configured."""


class EmbeddingProviderError(EmbeddingError):
    """The live embedder failed: bad or revoked key, rate limit, network, provider outage."""
