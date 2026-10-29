"""Disk cache decorator: same model + same text never hits the API twice.

Storage is one `<model>.npz` per model (sha256 keys + float16 vectors), small enough to commit.
A legacy `<model>.jsonl` (v1 format) is still read if present.
"""
from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from pathlib import Path

import numpy as np

from searchlab.domain.ports import Embedder
from searchlab.embeddings.errors import CacheMissError

__all__ = ["CacheMissError", "CachingEmbedder"]


def _key(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


class CachingEmbedder:
    def __init__(self, cache_dir: Path, model_id: str, inner: Embedder | None = None) -> None:
        self.model_id = model_id
        self._inner = inner
        self._npz = cache_dir / f"{model_id}.npz"
        self._store: dict[str, list[float]] = {}
        legacy = cache_dir / f"{model_id}.jsonl"
        if legacy.exists():
            for line in legacy.read_text().splitlines():
                row = json.loads(line)
                self._store[row["k"]] = row["v"]
        if self._npz.exists():
            data = np.load(self._npz)
            for k, v in zip(data["keys"], data["vectors"], strict=True):
                self._store[str(k)] = v.astype(np.float32).tolist()

    def __len__(self) -> int:
        return len(self._store)

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        missing = list(dict.fromkeys(t for t in texts if _key(t) not in self._store))
        if missing:
            if self._inner is None:
                raise CacheMissError(f"{len(missing)} text(s) not cached for {self.model_id}")
            for text, vec in zip(missing, self._inner.embed(missing), strict=True):
                self._store[_key(text)] = np.asarray(vec, np.float16).astype(np.float32).tolist()
            self.save()
        return [self._store[_key(t)] for t in texts]

    def save(self) -> None:
        self._npz.parent.mkdir(parents=True, exist_ok=True)
        keys = sorted(self._store)
        vectors = np.asarray([self._store[k] for k in keys], dtype=np.float16)
        tmp = self._npz.with_suffix(".tmp.npz")
        np.savez(tmp, keys=np.asarray(keys), vectors=vectors)
        tmp.replace(self._npz)
