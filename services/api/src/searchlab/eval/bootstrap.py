"""Percentile bootstrap over queries: resample the query set with replacement."""
from __future__ import annotations

from collections.abc import Sequence

import numpy as np

DRAWS = 1000
SEED = 0


def bootstrap_ci(
    values: Sequence[float], draws: int = DRAWS, seed: int = SEED, level: float = 0.95
) -> tuple[float, float]:
    """95% interval for the mean of per-query values. Fixed seed -> reproducible."""
    if not values:
        return (0.0, 0.0)
    arr = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    means = arr[rng.integers(0, len(arr), size=(draws, len(arr)))].mean(axis=1)
    tail = (1 - level) / 2 * 100
    lo, hi = np.percentile(means, [tail, 100 - tail])
    return (float(lo), float(hi))
