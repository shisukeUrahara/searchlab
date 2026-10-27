"""Disk cache decorator: same model + same text never hits the API twice."""
from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from pathlib import Path

from searchlab.domain.ports import Embedder


class CacheMissError(RuntimeError):
    """Raised when a vector is not cached and no live embedder is available."""


def _key(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


class CachingEmbedder:
    def __init__(self, cache_dir: Path, model_id: str, inner: Embedder | None = None) -> None:
        self.model_id = model_id
        self._inner = inner
        self._path = cache_dir / f"{model_id}.jsonl"
        self._store: dict[str, list[float]] = {}
        if self._path.exists():
            for line in self._path.read_text().splitlines():
                row = json.loads(line)
                self._store[row["k"]] = row["v"]

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        missing = list(dict.fromkeys(t for t in texts if _key(t) not in self._store))
        if missing:
            if self._inner is None:
                raise CacheMissError(f"{len(missing)} text(s) not cached for {self.model_id}")
            vectors = self._inner.embed(missing)
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open("a") as f:
                for text, vec in zip(missing, vectors, strict=True):
                    rounded = [round(x, 6) for x in vec]
                    self._store[_key(text)] = rounded
                    f.write(json.dumps({"k": _key(text), "v": rounded}) + "\n")
        return [self._store[_key(t)] for t in texts]
