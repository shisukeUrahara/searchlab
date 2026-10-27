"""Deterministic offline embedder for tests and CI: hashed bag-of-words, L2 normalised."""
from __future__ import annotations

import hashlib
import math
import re
from collections.abc import Sequence


class FakeEmbedder:
    def __init__(self, dim: int = 64) -> None:
        self.model_id = f"fake-{dim}"
        self._dim = dim

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._one(t) for t in texts]

    def _one(self, text: str) -> list[float]:
        vec = [0.0] * self._dim
        for word in re.findall(r"[a-z0-9]+", text.lower()):
            h = int(hashlib.md5(word.encode()).hexdigest(), 16)
            vec[h % self._dim] += 1.0
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]
