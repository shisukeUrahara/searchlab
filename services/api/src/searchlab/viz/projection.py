"""Vector map data: 2D UMAP layout + k-nearest-neighbour edges, precomputed to graph.json.

UMAP is an optional dependency (`uv sync --group viz`); everything else here is numpy only.
"""
from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np

from searchlab.domain.models import Chunk

KNN = 5
SEED = 42


def normalize(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / np.where(norms == 0, 1, norms)


def knn_edges(vectors: np.ndarray, k: int = KNN) -> list[tuple[int, int, float]]:
    """Undirected edges (i < j) to each node's k most cosine-similar neighbours."""
    unit = normalize(vectors.astype(np.float32))
    sims = unit @ unit.T
    np.fill_diagonal(sims, -np.inf)
    nearest = np.argpartition(-sims, kth=min(k, len(sims) - 1) - 1, axis=1)[:, :k]
    edges: dict[tuple[int, int], float] = {}
    for i, row in enumerate(nearest):
        for j in row:
            a, b = (i, int(j)) if i < j else (int(j), i)
            edges[(a, b)] = round(float(sims[i, j]), 4)
    return sorted((a, b, w) for (a, b), w in edges.items())


def umap_layout(vectors: np.ndarray, seed: int = SEED) -> np.ndarray:
    import umap

    reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, metric="cosine", random_state=seed)
    coords: np.ndarray = reducer.fit_transform(vectors)
    return coords


def scale(coords: np.ndarray, size: float = 1000.0) -> np.ndarray:
    lo, hi = coords.min(axis=0), coords.max(axis=0)
    out: np.ndarray = (coords - lo) / np.where(hi - lo == 0, 1, hi - lo) * size
    return out


def build_graph(
    chunks: Sequence[Chunk],
    coords: np.ndarray,
    edges: list[tuple[int, int, float]],
    docs: Sequence[dict[str, str]],
    meta: dict[str, Any],
) -> dict[str, Any]:
    doc_index = {d["source_id"]: i for i, d in enumerate(docs)}
    return {
        "meta": meta,
        "docs": list(docs),
        "nodes": [
            {
                "id": c.chunk_id,
                "x": round(float(x), 2),
                "y": round(float(y), 2),
                "doc": doc_index.get(c.source_id, -1),
                "heading": c.heading,
                "page": c.page,
            }
            for c, (x, y) in zip(chunks, coords, strict=True)
        ],
        "edges": [[a, b, w] for a, b, w in edges],
    }
