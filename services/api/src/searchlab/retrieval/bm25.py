from __future__ import annotations

from collections.abc import Callable, Sequence

from rank_bm25 import BM25Okapi

from searchlab.domain.models import Chunk, ScoredChunk
from searchlab.retrieval.tokenize import tokenize


class Bm25Retriever:
    """Lexical baseline. Only chunks sharing at least one token with the query are returned."""

    def __init__(
        self, chunks: Sequence[Chunk], tokenizer: Callable[[str], list[str]] = tokenize
    ) -> None:
        self._chunks = list(chunks)
        self._tokenizer = tokenizer
        self._index = BM25Okapi([tokenizer(f"{c.heading}\n{c.text}") for c in self._chunks])

    def search(self, query: str, top_k: int) -> list[ScoredChunk]:
        tokens = self._tokenizer(query)
        if not tokens:
            return []
        scores = self._index.get_scores(tokens)
        order = sorted(range(len(scores)), key=lambda i: (-scores[i], i))
        hits = [i for i in order if scores[i] > 0][:top_k]
        return [
            ScoredChunk(chunk=self._chunks[i], score=float(scores[i]), rank=r)
            for r, i in enumerate(hits, start=1)
        ]
